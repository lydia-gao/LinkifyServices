from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from pydantic import BaseModel, Field, AnyUrl
from sqlalchemy.orm import Session
from models import Url
from database import SessionLocal
import string
from typing import Annotated, Optional
from routers.auth import get_current_user
from config import settings

router = APIRouter(
	prefix="/url",
	tags=["url"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = 62

def to_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    s = []
    while num:
        num, r = divmod(num, BASE)
        s.append(ALPHABET[r])
    return ''.join(reversed(s))

def from_base62(code: str) -> int:
    n = 0
    for ch in code:
        n = n * BASE + ALPHABET.index(ch)
    return n

class ShortenRequest(BaseModel):
	original_url: AnyUrl
	alias: Optional[str] = Field(None, min_length=3, max_length=30, pattern="^[A-Za-z0-9_-]+$")
	title: str = Field(None, max_length=256)
	description: Optional[str] = None

class ShortenResponse(BaseModel):
	original_url: str
	short_code: str
	alias: str = None
	short_url: str
	title: str
	clicks: int
	user_id: int = None
	created_at: str

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Url).filter(Url.user_id == user.get('id')).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_short_url(
	user: user_dependency,
	req: ShortenRequest,
	db: Session = Depends(get_db) 
):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')

	url_obj = Url(**req.model_dump(), user_id=user.get('id'), short_code="temp")

	db.add(url_obj)
	db.flush()

	url_obj.short_code = to_base62(url_obj.id)

	db.commit()
	db.refresh(url_obj)

	short_url = f"http://{settings.base_url}/{url_obj.short_code}"

	return ShortenResponse(
		original_url=url_obj.original_url,
		short_code=url_obj.short_code,
		alias=url_obj.alias,
		short_url=short_url,
		title=url_obj.title,
		clicks=url_obj.clicks,
		user_id=url_obj.user_id,
		created_at=url_obj.created_at.isoformat()
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
