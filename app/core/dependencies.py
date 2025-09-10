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


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):      
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user.",)
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user.",)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]