from app.db.init_db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func

class Qrcode(Base):
    __tablename__ = 'qrcodes'
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    qr_code_id = Column(String(16), unique=True, index=True, nullable=False)
    title = Column(String(256), nullable=True)
    scans = Column(Integer, default=0)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(Text, nullable=True)
