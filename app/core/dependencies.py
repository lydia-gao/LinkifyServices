from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from typing import Annotated
from fastapi import Depends
from app.core.security import oauth2_bearer, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi import HTTPException, status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _auth_failure() -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user.",
    )


def decode_jwt_token(token: str) -> dict:
    if not token:
        _auth_failure()
    normalized = token.strip()
    if normalized.lower().startswith("bearer "):
        normalized = normalized[7:].strip()
    try:
        payload = jwt.decode(normalized, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        ) from exc
    username: str | None = payload.get('sub')
    user_id: str | None = payload.get('id')
    user_role: str | None = payload.get('role')
    if username is None or user_id is None:
        _auth_failure()
    return {'username': username, 'id': user_id, 'user_role': user_role}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):	  
    return decode_jwt_token(token)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]