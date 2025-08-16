from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from pydantic import BaseModel, HttpUrl, Field
from sqlalchemy.orm import Session
from ..models import ShortUrl
from ..database import SessionLocal
import string

router = APIRouter(
	prefix="/shorten",
	tags=["shorturl"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

BASE62 = string.digits + string.ascii_letters
def encode_base62(num):
	if num == 0:
		return BASE62[0]
	arr = []
	base = len(BASE62)
	while num:
		num, rem = divmod(num, base)
		arr.append(BASE62[rem])
	arr.reverse()
	return ''.join(arr)

class ShortenRequest(BaseModel):
	target_url: HttpUrl
	alias: str = Field(None, min_length=3, max_length=30, pattern="^[A-Za-z0-9_-]+$")

class ShortenResponse(BaseModel):
	original_url: str
	short_code: str
	alias: str = None
	short_url: str
	title: str = None
	clicks: int
	user_id: int = None
	created_at: str

@router.post("/", response_model=ShortenResponse, status_code=201)
def create_short_url(
	req: ShortenRequest,
	db: Session = Depends(get_db)
):
	# No auth required, mock response for testing
	return ShortenResponse(
		original_url=str(req.target_url),
		short_code="abc123",
		alias=req.alias,
		short_url=f"http://localhost:8000/{req.alias or 'abc123'}",
		title="Example Website Homepage",
		clicks=0,
		user_id=1,
		created_at="2025-05-15T14:30:00Z"
	)

# 2.2. Redirect from Short URL
from fastapi.responses import RedirectResponse
@router.get("/{short_code}", status_code=307)
def redirect_short_url(short_code: str, db: Session = Depends(get_db)):
	obj = db.query(ShortUrl).filter(
		(ShortUrl.short_code == short_code) | (ShortUrl.alias == short_code)
	).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	obj.clicks += 1
	db.commit()
	return RedirectResponse(url=obj.original_url, status_code=307)

# 2.3. Set or Update Alias
class AliasRequest(BaseModel):
	alias: str = Field(..., min_length=3, max_length=30, pattern="^[A-Za-z0-9_-]+$")

@router.patch("/urls/{short_code}", response_model=ShortenResponse)
def set_or_update_alias(short_code: str, req: AliasRequest, db: Session = Depends(get_db)):
	obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	if db.query(ShortUrl).filter(ShortUrl.alias == req.alias).first():
		raise HTTPException(status_code=409, detail="Alias already taken")
	obj.alias = req.alias
	db.commit()
	db.refresh(obj)
	short_url = f"http://localhost:8000/{obj.alias or obj.short_code}"
	return ShortenResponse(
		original_url=obj.original_url,
		short_code=obj.short_code,
		alias=obj.alias,
		short_url=short_url,
		title=obj.title,
		clicks=obj.clicks,
		user_id=obj.user_id,
		created_at=obj.created_at.isoformat()
	)

# 2.4. Get Alias
@router.get("/urls/{short_code}/alias")
def get_alias(short_code: str, db: Session = Depends(get_db)):
	obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	return {"short_code": obj.short_code, "alias": obj.alias}

# 2.5. Remove Alias
@router.delete("/urls/{short_code}/alias", status_code=204)
def remove_alias(short_code: str, db: Session = Depends(get_db)):
	obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	obj.alias = None
	db.commit()
	return Response(status_code=204)
