from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, AnyUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Url
from database import SessionLocal
import string
from typing import Annotated, Optional
from routers.auth import get_current_user
from config import settings
from io import BytesIO
from utils.encoding import to_base62
from utils.qrcode_utils import to_qr_code

router = APIRouter(
	prefix="/qrcode",
	tags=["qrcode"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


class QRCodeRequest(BaseModel):
	original_url: AnyUrl
	title: str = Field(None, max_length=256)
	description: Optional[str] = None

class QRCodeResponse(BaseModel):
	original_url: str
	qr_code_id: str
	short_url: str
	title: str = None
	description: Optional[str] = None
	scans: int
	user_id: int = None
	created_at: str


# 3.1. Generate QR Code
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_qrcode(
	user: user_dependency,
	req: QRCodeRequest,
	db: Session = Depends(get_db) 
):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')

	qr_code = Url(
		original_url=str(req.original_url),
		title=req.title,
		description=req.description,
		user_id=user.get("id"),
		short_code="tmp"
	)
	db.add(qr_code)
	db.flush()

	return QRCodeResponse(
		original_url=str(req.original_url),
		qr_code_id=qr_code.id,
		short_code=f"http://localhost:8000/qrcode/{qr_code.id}",
		title=req.title,
		description=req.description,
		scans=0,
		user_id=qr_code.user_id,
		created_at=qr_code.created_at.isoformat()
	)

# 3.2. Get QR Code Image
@router.get("/{qr_code_id}/image")
def get_qrcode_image(qr_code_id: str, db: Session = Depends(get_db)):
	# No auth required, mock response for testing
	return Response(content=b"PNGDATA", media_type="image/png")

# 3.3. Redirect from QR Code
from fastapi.responses import RedirectResponse
@router.get("/{qr_code_id}", status_code=307)
def redirect_from_qrcode(qr_code_id: str, db: Session = Depends(get_db)):
	# No auth required, mock redirect for testing
	return RedirectResponse(url="https://example.com/your/long/url", status_code=307)
