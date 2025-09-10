from typing import Optional, Annotated
from pydantic import BaseModel, Field, AnyUrl


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
    user_id: int | None = None
    created_at: str
