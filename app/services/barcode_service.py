from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Barcode
from app.schemas.barcode import BarcodeRequest, BarcodeResponse
from app.utils.barcode_utils import to_barcode
from app.utils.random_id import generate_random_id
from app.core.config import settings
from typing import Optional

def create_barcode_logic(user_id: int, req: BarcodeRequest, db: Session) -> BarcodeResponse:
    for _ in range(5):
        barcode_id = generate_random_id(10)
        barcode = Barcode(
            original_url=str(req.original_url),
            title=req.title,
            description=req.description,
            user_id=user_id,
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
        raise ValueError("Failed to generate unique barcode_id after several attempts.")

    barcode_image = to_barcode(barcode.original_url)
    return BarcodeResponse(
        original_url=barcode.original_url,
        barcode_id=barcode.barcode_id,
        barcode_image=barcode_image,
        title=barcode.title,
        description=barcode.description,
        scans=barcode.scans,
        user_id=barcode.user_id,
        created_at=barcode.created_at.isoformat()
    )

def get_all_barcodes_for_user(user_id: int, db: Session):
    return db.query(Barcode).filter(Barcode.user_id == user_id).all()
