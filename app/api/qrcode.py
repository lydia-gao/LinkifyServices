import base64
from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from fastapi.responses import RedirectResponse
from pydantic import Field, AnyUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Qrcode
from app.database.database import SessionLocal
import string
from typing import Annotated, Optional
from app.api.auth import get_current_user
from app.core.config import settings
from app.utils.qrcode_utils import to_qr_code
from app.utils.random_id import generate_random_id
from app.utils.redirect_utils import redirect_to_original

router = APIRouter(
	prefix="/qrcodes",
	tags=["qrcodes"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


from app.schemas.qrcode import QRCodeRequest, QRCodeResponse


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Qrcode).filter(Qrcode.user_id == user.get('id')).all()

# 3.1. Generate QR Code
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_qrcode(
	user: user_dependency,
	req: QRCodeRequest,
	db: Session = Depends(get_db) 
):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
	
	for _ in range(5):
		qr_code_id = generate_random_id(10) 
		qr_code = Qrcode(
            original_url=str(req.original_url),
            title=req.title,
            description=req.description,
            user_id=user.get("id"),
            qr_code_id=qr_code_id,
        )

		db.add(qr_code)
		try:
			db.commit()
			db.refresh(qr_code)
			break
		except IntegrityError:
			db.rollback()
	else:
		raise HTTPException(status_code=409, detail="Failed to generate unique qr_code_id after retries")


	qr_code_url = f"{settings.base_url}/qrcode/{qr_code.qr_code_id}"

	qr_code_image = to_qr_code(original_url=qr_code_url, file_path=None)
	qr_code_image_str = base64.b64encode(qr_code_image.getvalue()).decode("utf-8")

	return QRCodeResponse(
		original_url=str(req.original_url),
		qr_code_id=qr_code.qr_code_id,
		qr_code_image=qr_code_image_str,
		title=req.title,
		description=req.description,
		scans=0,
		user_id=qr_code.user_id,
		created_at=qr_code.created_at.isoformat()
	)


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
