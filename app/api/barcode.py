from fastapi import APIRouter, HTTPException, status, Response
from app.core.config import settings
from app.models import Barcode
from app.services.barcode_service import create_barcode_logic, get_all_barcodes_for_user
from app.utils.barcode_utils import to_barcode
from app.utils.redirect_utils import redirect_to_original
# Use shared dependencies
from app.db.dependencies import db_dependency, user_dependency
# Request / Response Models
from app.schemas.barcode import BarcodeRequest

router = APIRouter(
    prefix="/barcodes",
    tags=["barcodes"]
)


# ---------- Endpoints ----------

# 1. Read all barcodes for user
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return get_all_barcodes_for_user(user.get('id'), db)


# 2. Generate Barcode
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_barcode(
    user: user_dependency,
    req: BarcodeRequest,
    db: db_dependency
):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    try:
        return create_barcode_logic(user.get("id"), req, db)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


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
