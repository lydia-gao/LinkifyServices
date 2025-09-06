from datetime import timedelta, timezone
import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import bcrypt_context, SECRET_KEY, ALGORITHM
from fastapi import Depends, Depends, HTTPException, status
from models import User


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") 

def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_user_logic(req, db):
    user = db.query(User).filter(User.username == req.username).first()
    if user:
        raise Exception("Username already exists")
    hashed_password = bcrypt_context.hash(req.password)
    new_user = User(
        username=req.username,
        email=req.email,
        hashed_password=hashed_password,
        auth_provider='local'
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



             

