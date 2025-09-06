from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.models import User
from app.db.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from passlib.context import CryptContext
from app.core.dependencies import db_dependency, user_dependency


router = APIRouter(
    prefix='/users',
    tags=['users']
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from app.schemas.users import UserVerification


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):

    return db.query(User).filter(User.id == user.get('id')).first()

