from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import ShortUrl
from app.schemas.shorturl import ShortenRequest, ShortenResponse, AliasRequest
from app.utils.encoding_base62 import to_base62
from app.core.config import settings
from typing import Optional


def normalize_alias(alias: str) -> str:
    return alias.strip()

def shortpath_exists(code: str, db: Session) -> bool:
    return db.query(ShortUrl).filter(
        (ShortUrl.short_code == code) | (ShortUrl.alias == code)
    ).first() is not None

def create_short_url_logic(user_id: int, req: ShortenRequest, db: Session) -> ShortenResponse:
    alias = None
    if req.alias:
        alias = normalize_alias(req.alias)
        if shortpath_exists(alias, db):
            raise ValueError("Alias already taken")

    url_obj = ShortUrl(
        original_url=str(req.original_url),
        alias=alias,
        title=req.title,
        description=req.description,
        user_id=user_id,
        short_code="tmp"
    )
    db.add(url_obj)
    db.flush()
    final_code = to_base62(url_obj.id)
    if shortpath_exists(final_code, db):
        raise ValueError("Short code collision, please retry")
    url_obj.short_code = final_code
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Unique constraint violation, please retry")
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

def check_alias_logic(alias: str, db: Session) -> bool:
    alias = normalize_alias(alias)
    return not shortpath_exists(alias, db)

def update_alias_logic(short_code: str, new_alias: str, db: Session) -> bool:
    new_alias = normalize_alias(new_alias)
    if shortpath_exists(new_alias, db):
        raise ValueError("Alias already taken")
    obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
    if not obj:
        raise LookupError("Short URL not found")
    obj.alias = new_alias
    db.commit()
    return True

def get_alias_logic(short_code: str, db: Session) -> dict:
    obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
    if not obj:
        raise LookupError("Short URL not found")
    return {"short_code": obj.short_code, "alias": obj.alias}

def remove_alias_logic(short_code: str, db: Session) -> bool:
    obj = db.query(ShortUrl).filter(ShortUrl.short_code == short_code).first()
    if not obj:
        raise LookupError("Short URL not found")
    obj.alias = None
    db.commit()
    return True
