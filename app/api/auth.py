
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, CreateUserRequest
from app.core.dependencies import db_dependency
from app.services.auth_service import create_user_logic, authenticate_user
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, req: CreateUserRequest):
    try:
        user = create_user_logic(req, db)
        return {"username": user.username, "email": user.email, "msg": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Incorrect username or password"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expire = getattr(settings, "access_token_expire_minutes", 20)
    token = create_access_token(
        user.username, user.id, user.auth_provider, timedelta(minutes=token_expire)
    )
    return {"access_token": token, "token_type": "bearer"}