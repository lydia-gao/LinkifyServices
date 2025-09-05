from app.db.init_db import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    auth_provider = Column(String, default="local")
    auth_provider_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
