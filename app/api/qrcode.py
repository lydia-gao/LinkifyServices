from fastapi import APIRouter, HTTPException, status, Response
from app.models import Qrcode
from app.core.config import settings
from app.services.qrcode_service import create_qrcode_logic, get_all_qrcodes_for_user
from app.utils.qrcode_utils import to_qr_code
from app.utils.redirect_utils import redirect_to_original
from app.db.dependencies import db_dependency, user_dependency
from app.schemas.qrcode import QRCodeRequest


router = APIRouter(
	prefix="/qrcodes",
	tags=["qrcodes"]
)



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
	return get_all_qrcodes_for_user(user.get('id'), db)

# 3.1. Generate QR Code
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_qrcode(
	user: user_dependency,
	req: QRCodeRequest,
	db: db_dependency
):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
	try:
		return create_qrcode_logic(user.get("id"), req, db)
	except ValueError as e:
		raise HTTPException(status_code=409, detail=str(e))


# 3.2. Get QR Code Image
@router.get("/{qr_code_id}/image")
async def get_qrcode_image(qr_code_id: str, db: db_dependency):
    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="QR Code not found")

	# buffer is an in-memory bytes container/memory space (in RAM). 
	# Python exposes it as a file-like object, so we can use file operations (read, write, seek) without touching disk.

    buffer = to_qr_code(
        original_url=f"{settings.base_url}/qrcode/{obj.qr_code_id}", 
        file_path=None
    )
    return Response(content=buffer.getvalue(), media_type="image/png")


# 3.3. Redirect from QR Code
@router.get("/{qr_code_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_from_qrcode(qr_code_id: str, db: db_dependency):
    obj = db.query(Qrcode).filter(Qrcode.qr_code_id == qr_code_id).first()
    if obj:
        obj.scans += 1
        db.commit()
    return redirect_to_original(obj)
