from fastapi import APIRouter, HTTPException, status, Response
from app.models import Qrcode
from app.core.config import settings
from app.services.qrcode_service import create_qrcode_logic, get_all_qrcodes_for_user
from app.celery_app import get_task_info
from app.celery_tasks.tasks import create_qrcode_task
from starlette.responses import JSONResponse
from app.utils.qrcode_utils import to_qr_code
from app.utils.cache import cache_get_bytes, cache_set_bytes
from app.utils.redirect_utils import redirect_to_original
from app.core.dependencies import db_dependency, user_dependency
from app.schemas.qrcode import QRCodeRequest


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
    # Celery任务参数必须是dict，且用 model_dump() 传递
    task = create_qrcode_task.apply_async(args=[user.get("id"), req.model_dump()])
    return {"task_id": task.id, "status": "pending"}


# Task status

# 3.4. Get QR Code Task Status (Celery)
@router.get("/task/{task_id}")
async def get_qrcode_task_status(task_id: str):
    info = get_task_info(task_id)
    # 兼容API文档格式
    return {
        "task_id": info["task_id"],
        "status": info["task_status"],
        "result": info["task_result"] if info["task_status"] == "SUCCESS" else None
    }


# 3.2. Get QR Code Image
@router.get("/{qr_code_id}/image")
async def get_qrcode_image(qr_code_id: str, db: db_dependency):
    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="QR Code not found")

    # buffer is an in-memory bytes container (RAM).
    # Python exposes it as a file-like object, so you can use file operations (read, write, seek) without disk IO.
    cache_key = f"qrcode:image:{obj.qr_code_id}"
    cached = cache_get_bytes(cache_key)
    if cached:
        return Response(content=cached, media_type="image/png")

    buffer = to_qr_code(
        original_url=f"{settings.base_url}/qrcode/{obj.qr_code_id}", 
    )
    img_bytes = buffer.getvalue()
    cache_set_bytes(cache_key, img_bytes, ttl_seconds=3600)
    return Response(content=img_bytes, media_type="image/png")


# 3.3. Redirect from QR Code
@router.get("/{qr_code_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_from_qrcode(qr_code_id: str, db: db_dependency):
    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if obj:
        obj.scans += 1
        db.commit()
    return redirect_to_original(obj)
