from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, AnyUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import ShortUrl
from app.database.database import SessionLocal
from typing import Annotated, Optional
from app.api.auth import get_current_user
from app.core.config import settings
from app.utils.encoding_base62 import to_base62
from app.utils.redirect_utils import redirect_to_original

router = APIRouter(
	prefix="/shorturls",
	tags=["shorturls"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


AliasStr = Annotated[str, Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")]

class AliasRequest(BaseModel):
    alias: AliasStr

class ShortenRequest(BaseModel):
	original_url: AnyUrl
	alias: Optional[AliasStr] = None
	title: str = Field(None, max_length=256)
	description: Optional[str] = None

class ShortenResponse(BaseModel):
	original_url: str
	short_code: str
	alias: Optional[str] = None
	short_url: str
	title: str
	description: Optional[str] = None
	clicks: int
	user_id: int = None
	created_at: str

# Alias

def normalize_alias(alias: str) -> str:
    alias = alias.strip()
    return alias

def shortpath_exists(code: str, db: Session) -> bool:
    return db.query(ShortUrl).filter(
        (ShortUrl.short_code == code) | (ShortUrl.alias == code)
    ).first() is not None



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(ShortUrl).filter(ShortUrl.user_id == user.get('id')).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_short_url(
	user: user_dependency,
	req: ShortenRequest,
	db: db_dependency 
):
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
      
	alias = None
	if req.alias:
		alias = normalize_alias(req.alias)
		if shortpath_exists(alias, db):
			raise HTTPException(status_code=409, detail="Alias already taken")

	url_obj = ShortUrl(
		original_url=str(req.original_url),
		alias=alias,
		title=req.title,
		description=req.description,
		user_id=user.get("id"),
		short_code="tmp"
	)

	db.add(url_obj)
	db.flush()

	final_code = to_base62(url_obj.id)
	if shortpath_exists(final_code, db):
		raise HTTPException(status_code=409, detail="Short code collision, please retry")
	url_obj.short_code = final_code

	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="Unique constraint violation, please retry")
	db.refresh(url_obj)

	short_url = f"{settings.base_url}/url/{url_obj.short_code}"

	return ShortenResponse(
		original_url=url_obj.original_url,
		short_code=url_obj.short_code,
		alias=url_obj.alias,
		short_url=short_url,
		title=url_obj.title,
		description=url_obj.description,
		clicks=url_obj.clicks,
		user_id=url_obj.user_id,
		created_at=url_obj.created_at.isoformat()
	)

# 2.2. Redirect from Short URL
@router.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_short_url(short_code: str, db: db_dependency):
    obj = db.query(ShortUrl).filter(
        (ShortUrl.short_code == short_code) | (ShortUrl.alias == short_code)
    ).first()
    if obj:
        obj.clicks += 1
        db.commit()
    return redirect_to_original(obj)


@router.post("/aliases/check")
async def check_alias(payload: AliasRequest, db: db_dependency):
    # Normalize (e.g., lower, trim) before checking
    alias = normalize_alias(payload.alias)
    return {"available": not shortpath_exists(alias, db)}

@router.patch("/{short_code}/alias")
async def update_alias(short_code: str, payload: AliasRequest, db: db_dependency):
    new_alias = normalize_alias(payload.alias)
    if shortpath_exists(new_alias, db):
        raise HTTPException(409, detail="Alias already taken")
    obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Short URL not found")
    obj.alias = new_alias
    db.commit()
    return {"ok": True}

# 2.4. Get Alias
@router.get("/{short_code}/alias")
async def get_alias(short_code: str, db: db_dependency):
	obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	return {"short_code": obj.short_code, "alias": obj.alias}

# 2.5. Remove Alias
@router.delete("/{short_code}/alias", status_code=204)
async def remove_alias(short_code: str, db: db_dependency):
	obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
	if not obj:
		raise HTTPException(status_code=404, detail="Short URL not found")
	obj.alias = None
	db.commit()
	return Response(status_code=204)
