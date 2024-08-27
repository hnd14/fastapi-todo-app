from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from exception import JWTTokenException, UnauthorizedException
from schemas import User
from settings import JWT_ALGORITHM, JWT_SECRET, SYSTEM_COMPANY_ID

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
        "is_admin": user.is_admin,
        "company_id": str(user.company_id)
    }
    expire = datetime.now(timezone.utc) + expires if expires else datetime.now(timezone.utc) + expires + timedelta(minutes=10)
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)

def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username = payload.get("sub")
        user.id = UUID(payload.get("id"))
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")
        user.company_id = UUID(payload.get("company_id"))
        
        if user.username is None or user.id is None:
            raise JWTTokenException()
        return user
    except JWTError:
        raise JWTTokenException()

def requires_system_admin(func):
    def decorate(user: User, *args, **kwargs):
        if user.company_id != UUID(SYSTEM_COMPANY_ID) or not user.is_admin:
            raise UnauthorizedException()
        return func(user, *args, **kwargs)