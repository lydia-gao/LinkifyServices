from app.db.init_db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func

class Barcode(Base):
    __tablename__ = "barcodes"
    id = Column(Integer, primary_key=True, index=True)
    barcode_id = Column(String(20), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    title = Column(String(256))
    description = Column(Text)
    scans = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
