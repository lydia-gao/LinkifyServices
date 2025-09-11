from typing import Optional
from pydantic import BaseModel, Field, AnyUrl


class BarcodeRequest(BaseModel):
    original_url: AnyUrl
    title: str = Field(None, max_length=256)
    description: Optional[str] = None


class BarcodeResponse(BaseModel):
    original_url: str
    barcode_id: str
    image_url: str
    title: str | None = None
    description: Optional[str] = None
    scans: int
    user_id: int | None = None
    created_at: str
