from celery import shared_task
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.qrcode import QRCodeRequest
from app.schemas.barcode import BarcodeRequest
from app.services.qrcode_service import create_qrcode_logic
from app.services.barcode_service import create_barcode_logic


def _with_db(fn):
    """Utility: provide a DB session to the wrapped function. Compatible with bind=True tasks."""
    def wrapper(*args, **kwargs):
        db: Session = SessionLocal()
        try:
            # 不去动 *args，只加 kwargs
            return fn(*args, db=db, **kwargs)
        finally:
            db.close()
    return wrapper



@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="qrcode:create_qrcode_task",
)
@_with_db
def create_qrcode_task(self, user_id: int, req_data: dict, db: Session = None):
    """Create a QR code via service. req_data must match QRCodeRequest model."""
    req = QRCodeRequest(**req_data)
    return create_qrcode_logic(user_id, req, db).model_dump()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="barcode:create_barcode_task",
)
@_with_db
def create_barcode_task(self, user_id: int, req_data: dict, db: Session = None):
    """Create a Barcode via service. req_data must match BarcodeRequest model."""
    req = BarcodeRequest(**req_data)
    return create_barcode_logic(user_id, req, db).model_dump()
