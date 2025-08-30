import base64
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, AnyUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Barcode
from database import SessionLocal
from typing import Annotated, Optional
from routers.auth import get_current_user
from config import settings
from utils.barcode_utils import to_barcode
from utils.random_id import generate_random_id
from utils.redirect_utils import redirect_to_original


router = APIRouter(
    prefix="/barcodes",
    tags=["barcodes"]
)


# ---------- DB dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------- Request / Response Models ----------
class BarcodeRequest(BaseModel):
    original_url: AnyUrl
    title: str = Field(None, max_length=256)
    description: Optional[str] = None


class BarcodeResponse(BaseModel):
    original_url: str
    barcode_id: str
    barcode_image: str
    title: str = None
    description: Optional[str] = None
    scans: int
    user_id: int = None
    created_at: str


# ---------- Endpoints ----------

# 1. Read all barcodes for user
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Barcode).filter(Barcode.user_id == user.get('id')).all()


# 2. Generate Barcode
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_barcode(
    user: user_dependency,
    req: BarcodeRequest,
    db: Session = Depends(get_db) 
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    for _ in range(5):
        barcode_id = generate_random_id(10)
        barcode = Barcode(
            original_url=str(req.original_url),
            title=req.title,
            description=req.description,
            user_id=user.get("id"),
            barcode_id=barcode_id,
        )

        db.add(barcode)
        try:
            db.commit()
            db.refresh(barcode)
            break
        except IntegrityError:
            db.rollback()
    else:
        raise HTTPException(status_code=409, detail="Failed to generate unique barcode_id after retries")

    barcode_url = f"{settings.base_url}/barcodes/{barcode.barcode_id}"
    barcode_image = to_barcode(original_url=barcode_url, file_path=None)
    barcode_image_str = base64.b64encode(barcode_image.getvalue()).decode("utf-8")

    return BarcodeResponse(
        original_url=str(req.original_url),
        barcode_id=barcode.barcode_id,
        barcode_image=barcode_image_str,
        title=req.title,
        description=req.description,
        scans=0,
        user_id=barcode.user_id,
        created_at=barcode.created_at.isoformat()
    )


# 3. Get Barcode Image
@router.get("/{barcode_id}/image")
async def get_barcode_image(barcode_id: str, db: db_dependency):
    obj = db.query(Barcode).filter(Barcode.barcode_id == barcode_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Barcode not found")

    buffer = to_barcode(
        original_url=f"{settings.base_url}/barcodes/{obj.barcode_id}",
        file_path=None
    )
    return Response(content=buffer.getvalue(), media_type="image/png")


# 4. Redirect from Barcode
@router.get("/{barcode_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_from_barcode(barcode_id: str, db: db_dependency):
    obj = db.query(Barcode).filter(Barcode.barcode_id == barcode_id).first()
    if obj:
        obj.scans += 1
        db.commit()
    return redirect_to_original(obj)
