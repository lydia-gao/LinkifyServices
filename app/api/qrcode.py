from uuid import uuid4

from celery import chord
from fastapi import APIRouter, HTTPException, status, Response

from app.models import Qrcode
from app.core.config import settings
from app.services.qrcode_service import create_qrcode_logic, get_all_qrcodes_for_user
from app.celery_app import get_task_info
from app.celery_tasks.tasks import create_qrcode_task, notify_batch_complete
from app.utils.cache import cache_get_s3_url, cache_set_s3_url
from app.utils.s3_utils import generate_presigned_url
from app.utils.redirect_utils import redirect_to_original
from app.utils.redis_client import build_ws_channel
from app.core.dependencies import db_dependency, user_dependency
from app.schemas.qrcode import QRCodeBatchRequest, QRCodeRequest


router = APIRouter(
	prefix="/qrcodes",
	tags=["qrcodes"]
)



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
	return get_all_qrcodes_for_user(user.get('id'), db)

# 3.1. Generate QR Code
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_qrcode(
	user: user_dependency,
	req: QRCodeRequest,
	db: db_dependency
):
	try:
		return create_qrcode_logic(user.get("id"), req, db)
	except ValueError as e:
		raise HTTPException(status_code=409, detail=str(e))


# 3.1.b. Generate QR Code (async via Celery)

# 3.1.b. Generate QR Code (Async, Celery)
@router.post("/async", status_code=status.HTTP_202_ACCEPTED)
async def create_qrcode_async(
    user: user_dependency,
    req: QRCodeRequest
):
    task = create_qrcode_task.apply_async(args=[user.get("id"), req.model_dump()])
    return {
        "success": True,
        "task_id": task.id,
        "status": "pending",
        "poll_url": f"{settings.base_url}/qrcodes/task/{task.id}"
    }


@router.post("/batch", status_code=status.HTTP_202_ACCEPTED)
async def create_qrcode_batch(user: user_dependency, payload: QRCodeBatchRequest):
    if not payload.items:
        raise HTTPException(status_code=400, detail="At least one QR code payload is required")

    user_id = user.get("id")
    batch_id = str(uuid4())
    signatures = [create_qrcode_task.s(user_id, item.model_dump()) for item in payload.items]
    callback = notify_batch_complete.s(user_id=user_id, batch_id=batch_id, entity="qrcode")
    chord_result = chord(signatures)(callback)
    return {
        "success": True,
        "batch_id": batch_id,
        "task_id": chord_result.id,
        "status": "pending",
        "websocket_channel": build_ws_channel(user_id),
    }


# Task status

# 3.4. Get QR Code Task Status (Celery)
@router.get("/task/{task_id}")
async def get_qrcode_task_status(task_id: str):
    info = get_task_info(task_id)
    error = None
    if info["task_status"] == "FAILURE":
        error = str(info["task_result"])
    return {
        "success": info["task_status"] == "SUCCESS",
        "task_id": info["task_id"],
        "status": info["task_status"],
        "result": info["task_result"] if info["task_status"] == "SUCCESS" else None,
        "error": error,
        "poll_url": f"{settings.base_url}/qrcodes/task/{task_id}"
    }


# 3.2. Get QR Code Image
@router.get("/{qr_code_id}/image")
async def get_qrcode_image(qr_code_id: str, db: db_dependency):
    cache_key = f"qrcode:s3key:{qr_code_id}"
    cached_url = cache_get_s3_url(cache_key)
    if cached_url:
        # 预签名 URL 已经缓存，直接 307 重定向
        return Response(status_code=307, headers={"Location": cached_url})

    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="QR Code not found")

    try:
        presigned_url = generate_presigned_url(obj.s3_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate QR Code image URL")

    cache_set_s3_url(cache_key, presigned_url, ttl_seconds=300)
    return Response(status_code=307, headers={"Location": presigned_url})


# 3.3. Redirect from QR Code
@router.get("/{qr_code_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_from_qrcode(qr_code_id: str, db: db_dependency):
    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if obj:
        obj.scans += 1
        db.commit()
    return redirect_to_original(obj)
