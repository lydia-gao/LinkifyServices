from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Qrcode
from app.schemas.qrcode import QRCodeRequest, QRCodeResponse
from app.utils.qrcode_utils import to_qr_code
from app.utils.random_id import generate_random_id
from app.core.config import settings
from typing import Optional

def create_qrcode_logic(user_id: int, req: QRCodeRequest, db: Session) -> QRCodeResponse:
    for _ in range(5):
        qr_code_id = generate_random_id(10)
        qr_code = Qrcode(
            original_url=str(req.original_url),
            title=req.title,
            description=req.description,
            user_id=user_id,
            qr_code_id=qr_code_id,
        )
        db.add(qr_code)
        try:
            db.commit()
            db.refresh(qr_code)
            break
        except IntegrityError:
            db.rollback()
    else:
        raise ValueError("Failed to generate unique QR code ID after several attempts.")

    image_url = f"{settings.base_url}/qrcodes/{qr_code.qr_code_id}/image"
    return QRCodeResponse(
        original_url=qr_code.original_url,
        qr_code_id=qr_code.qr_code_id,
        image_url=image_url,
        title=qr_code.title,
        description=qr_code.description,
        scans=qr_code.scans,
        user_id=qr_code.user_id,
        created_at=qr_code.created_at.isoformat()
    )

def get_all_qrcodes_for_user(user_id: int, db: Session):
    return db.query(Qrcode).filter(Qrcode.user_id == user_id).all()
