from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import SessionLocal

router = APIRouter(
	prefix="/history",
	tags=["history"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# 5.1. Get URL History
@router.get("/urls")
def get_url_history(page: int = 1, limit: int = 20, sort: str = "created_at", order: str = "desc"):
	# No auth required, mock response for testing
	return {"page": page, "limit": limit, "total": 2, "urls": [
		{"original_url": "https://example.com/your/long/url", "short_code": "abc123", "short_url": "http://localhost:8000/abc123", "title": "Example Website Homepage", "clicks": 42, "created_at": "2025-05-15T14:30:00Z"},
		{"original_url": "https://example.com/another/page", "short_code": "def456", "short_url": "http://localhost:8000/def456", "title": "Another Example Page", "clicks": 18, "created_at": "2025-05-16T10:15:00Z"}
	]}

# 5.2. Get QR Code History
@router.get("/qrcodes")
def get_qrcode_history(page: int = 1, limit: int = 20, sort: str = "created_at", order: str = "desc"):
	# No auth required, mock response for testing
	return {"page": page, "limit": limit, "total": 2, "qrcodes": [
		{"original_url": "https://example.com/your/long/url", "qr_code_id": "qr123", "qr_code_url": "http://localhost:8000/qrcode/qr123", "title": "Example Website Homepage", "scans": 35, "created_at": "2025-05-15T14:30:00Z"},
		{"original_url": "https://example.com/another/url", "qr_code_id": "qr456", "qr_code_url": "http://localhost:8000/qrcode/qr456", "title": "Another Example Page", "scans": 24, "created_at": "2025-05-16T10:15:00Z"}
	]}

# 5.3. Get Barcode History
@router.get("/barcodes")
def get_barcode_history(page: int = 1, limit: int = 20, sort: str = "created_at", order: str = "desc"):
	# No auth required, mock response for testing
	return {"page": page, "limit": limit, "total": 2, "barcodes": [
		{"original_url": "https://example.com/your/long/url", "barcode_id": "bar123", "barcode_url": "http://localhost:8000/barcode/bar123", "title": "Example Website Homepage", "scans": 28, "created_at": "2025-05-15T14:30:00Z"},
		{"original_url": "https://example.com/another/url", "barcode_id": "bar456", "barcode_url": "http://localhost:8000/barcode/bar456", "title": "Another Example Page", "scans": 16, "created_at": "2025-05-16T10:15:00Z"}
	]}
