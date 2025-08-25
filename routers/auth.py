from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path, status, Request
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def get_current_user():
	# Mock user, always returns a default user dict
	return {"id": 1, "username": "testuser", "is_active": True}
