from typing import Any, Dict, List

from celery import shared_task
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.qrcode import QRCodeRequest
from app.schemas.barcode import BarcodeRequest
from app.schemas.shorturl import ShortenRequest
from app.services.qrcode_service import create_qrcode_logic
from app.services.barcode_service import create_barcode_logic
from app.services.shorturl_service import create_short_url_logic
from app.utils.redis_client import publish_ws_event

logger = get_task_logger(__name__)

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


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="shorturl:create_shorturl_task",
)
@_with_db
def create_shorturl_task(self, user_id: int, req_data: dict, db: Session = None):
    """Create a Short URL via service. req_data must match ShortenRequest model."""
    req = ShortenRequest(**req_data)
    return create_short_url_logic(user_id, req, db).model_dump()


@shared_task(name="ws:notify_batch_complete")
def notify_batch_complete(results: List[Dict[str, Any]], user_id: int, batch_id: str, entity: str) -> dict:
    payload = {
        "type": "batch_completed",
        "entity": entity,
        "batch_id": batch_id,
        "count": len(results),
        "items": results,
    }
    logger.info(
        "notify_batch_complete user_id=%s batch_id=%s count=%s redis_url=%s",
        user_id,
        batch_id,
        len(results),
        settings.redis_url,
    )
    publish_ws_event(user_id, payload)
    return payload
