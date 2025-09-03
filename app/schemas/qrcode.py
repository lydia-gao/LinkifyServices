from typing import Optional
from pydantic import BaseModel, Field, AnyUrl


class QRCodeRequest(BaseModel):
    original_url: AnyUrl
    title: str = Field(None, max_length=256)
    description: Optional[str] = None


class QRCodeResponse(BaseModel):
    original_url: str
    qr_code_id: str
    qr_code_image: str
    title: str | None = None
    description: Optional[str] = None
    scans: int
    user_id: int | None = None
    created_at: str
