from fastapi import APIRouter, HTTPException, status, Depends, Response
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal
import string

router = APIRouter(
	prefix="/barcode",
	tags=["barcode"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

class BarcodeRequest(BaseModel):
	target_url: HttpUrl

class BarcodeResponse(BaseModel):
	original_url: str
	barcode_id: str
	barcode_url: str
	title: str = None
	scans: int
	user_id: int = None
	created_at: str

# 4.1. Generate Barcode
@router.post("/", response_model=BarcodeResponse, status_code=201)
def generate_barcode(req: BarcodeRequest, db: Session = Depends(get_db)):
	# No auth required, mock response for testing
	return BarcodeResponse(
		original_url=str(req.target_url),
		barcode_id="bar123",
		barcode_url="http://localhost:8000/barcode/bar123",
		title="Example Website Homepage",
		scans=0,
		user_id=1,
		created_at="2025-05-15T14:30:00Z"
	)

# 4.2. Get Barcode Image
@router.get("/{barcode_id}/image")
def get_barcode_image(barcode_id: str, db: Session = Depends(get_db)):
	# No auth required, mock response for testing
	return Response(content=b"PNGDATA", media_type="image/png")

# 4.3. Redirect from Barcode
from fastapi.responses import RedirectResponse
@router.get("/{barcode_id}", status_code=307)
def redirect_from_barcode(barcode_id: str, db: Session = Depends(get_db)):
	return RedirectResponse(url="https://example.com/your/long/url", status_code=307)
