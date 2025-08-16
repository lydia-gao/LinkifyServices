from fastapi import APIRouter, HTTPException, status, Depends, Response
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from ..database import SessionLocal
import string

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

class QRCodeRequest(BaseModel):
	target_url: HttpUrl

class QRCodeResponse(BaseModel):
	original_url: str
	qr_code_id: str
	qr_code_url: str
	title: str = None
	scans: int
	user_id: int = None
	created_at: str

# 3.1. Generate QR Code
@router.post("/", response_model=QRCodeResponse, status_code=201)
def generate_qrcode(req: QRCodeRequest, db: Session = Depends(get_db)):
	# No auth required, mock response for testing
	return QRCodeResponse(
		original_url=str(req.target_url),
		qr_code_id="qr123",
		qr_code_url="http://localhost:8000/qrcode/qr123",
		title="Example Website Homepage",
		scans=0,
		user_id=1,
		created_at="2025-05-15T14:30:00Z"
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
