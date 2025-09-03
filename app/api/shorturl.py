from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from fastapi.responses import RedirectResponse
from pydantic import Field, AnyUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import ShortUrl
from app.database.database import SessionLocal
from typing import Annotated, Optional
from app.api.auth import get_current_user
from app.core.config import settings
from app.utils.redirect_utils import redirect_to_original
from app.services.shorturl_service import (
	create_short_url_logic, check_alias_logic, update_alias_logic, get_alias_logic, remove_alias_logic
)

router = APIRouter(
	prefix="/shorturls",
	tags=["shorturls"]
)


# Use shared dependencies
from app.database.dependencies import db_dependency, user_dependency


from app.schemas.shorturl import AliasRequest, ShortenRequest, ShortenResponse

# Alias



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
	try:
		return create_short_url_logic(user.get("id"), req, db)
	except ValueError as e:
		raise HTTPException(status_code=409, detail=str(e))

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
	try:
		available = check_alias_logic(payload.alias, db)
		return {"available": available}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{short_code}/alias")
async def update_alias(short_code: str, payload: AliasRequest, db: db_dependency):
	try:
		update_alias_logic(short_code, payload.alias, db)
		return {"ok": True}
	except ValueError as e:
		raise HTTPException(status_code=409, detail=str(e))
	except LookupError as e:
		raise HTTPException(status_code=404, detail=str(e))

# 2.4. Get Alias
@router.get("/{short_code}/alias")
async def get_alias(short_code: str, db: db_dependency):
	try:
		return get_alias_logic(short_code, db)
	except LookupError as e:
		raise HTTPException(status_code=404, detail=str(e))

# 2.5. Remove Alias
@router.delete("/{short_code}/alias", status_code=204)
async def remove_alias(short_code: str, db: db_dependency):
	try:
		remove_alias_logic(short_code, db)
		return Response(status_code=204)
	except LookupError as e:
		raise HTTPException(status_code=404, detail=str(e))
