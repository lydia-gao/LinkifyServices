from app.core.security import bcrypt_context
from app.models import User


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
    hashed_password = bcrypt_context.hash(req.hashed_password)
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



             

