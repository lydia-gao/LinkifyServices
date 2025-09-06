from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

SECRET_KEY = 'c376b1e1b6112627129877f30793f8b00598adb28659f1f5f8fb6614ce38540e'
ALGORITHM = 'HS256'  # algorithm used to encode the JWT token 

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def create_access_token(username: str, user_id: int, auth_provider: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'auth_provider': auth_provider}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
