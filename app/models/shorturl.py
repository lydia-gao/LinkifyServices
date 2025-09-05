from app.db.init_db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func

class ShortUrl(Base):
    __tablename__ = 'short_urls'
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(16), unique=True, index=True, nullable=False)
    alias = Column(String(30), unique=True, index=True, nullable=True)
    title = Column(String(256), nullable=True)
    clicks = Column(Integer, default=0)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(Text, nullable=True)
