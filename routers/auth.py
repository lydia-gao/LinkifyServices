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

# use interceptor

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def get_current_user():
	# Mock user, always returns a default user dict
	return {"id": 1, "username": "testuser", "is_active": True}


# SECRET_KEY = 'c376b1e1b6112627129877f30793f8b00598adb28659f1f5f8fb6614ce38540e'
# ALGORITHM = 'HS256'  # algorithm used to encode the JWT token 

# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") 


# class CreateUserRequest(BaseModel):
#     username: str
#     email: str 
#     first_name: str
#     last_name: str
#     password: str


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# def get_db():
#     # dependency injection
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# db_dependency = Annotated[Session, Depends(get_db)]

# ### Endpoints ###


# def authenticate_user(db, username: str, password: str):
#     # db: Session is not required, Python is a dynamic language, you can omit the type
#     user = db.query(Users).filter(Users.username == username).first()
#     if not user:
#         return False
#     if not bcrypt_context.verify(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
#     encode = {'sub':username, 'id':user_id, 'role':role}
#     expires = datetime.now(timezone.utc) + expires_delta
#     encode.update({'exp': expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    

# async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):      
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get('sub')
#         user_id: str = payload.get('id')
#         if username is None or user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                                 detail="Could not validate user.",)
#         return {'username': username, 'id': user_id}
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                             detail="Could not validate user.",)
                                                                        


# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
#     create_user_model = Users(
#         username=create_user_request.username,
#         email=create_user_request.email,
#         first_name=create_user_request.first_name,
#         last_name=create_user_request.last_name,
#         hashed_password=bcrypt_context.hash(create_user_request.password),
#     )

#     db.add(create_user_model)
#     db.commit()


# @router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
# async def login_for_access_token(db: db_dependency, 
#                                  form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                             detail="Could not validate user.",)
#     token = create_access_token(user.username, user.id, timedelta(minutes=20))
#     return {'access_token': token, 'token_type': 'bearer'}
