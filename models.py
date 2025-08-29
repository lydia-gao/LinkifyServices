from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, func
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True) 
    first_name = Column(String)
    last_name = Column(String) 
    hashed_password = Column(String) # encrypted password, not plain text

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
    