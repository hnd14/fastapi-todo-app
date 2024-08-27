from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from exception import JWTTokenException
from schemas import User
from settings import JWT_ALGORITHM, JWT_SECRET

bcrypt_context = CryptContext(schemes=["bcrypt"])

def get_hashed_password(raw_password:str):
    return bcrypt_context.hash(raw_password)

def verify_password(raw_password, hashed_password):
    return bcrypt_context.verify(raw_password, hashed_password)

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(username: str, password: str, db: Session):
    user = db.scalars(select(User).filter(User.username == username)).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if not user.is_active:
        return False
    
    return user

def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin
    }
    expire = datetime.now(timezone.utc) + expires if expires else datetime.now(timezone.utc) + expires + timedelta(minutes=10)
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)
