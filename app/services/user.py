from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from exception import DuplicatedResourceException, handle_unknown_exception
from services.auth import get_hashed_password
from models.user import UserPostModel
from schemas.user import User
from settings import SYSTEM_COMPANY_ID, NONE_COMPANY_ID

def handle_unique__user_constraint(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if "uq_user_name" in str(e.orig):
                raise DuplicatedResourceException("Username")
            if "uq_email" in str(e.orig):
                raise DuplicatedResourceException("Email")
            raise e
    return decorate

@handle_unknown_exception
@handle_unique__user_constraint
def register_system_admin(db:Session, data:UserPostModel)->User:
    new_user = User(**data.model_dump())
    new_user.password = get_hashed_password(data.password)
    new_user.is_admin = True
    new_user.created_at = datetime.now(timezone.utc)
    new_user.updated_at = datetime.now(timezone.utc)
    new_user.company_id = UUID(SYSTEM_COMPANY_ID)
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@handle_unknown_exception
@handle_unique__user_constraint
def register_admin(db:Session, data:UserPostModel)->User:
    new_user = User(**data.model_dump())
    new_user.password = get_hashed_password(data.password)
    new_user.is_admin = True
    new_user.created_at = datetime.now(timezone.utc)
    new_user.updated_at = datetime.now(timezone.utc)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@handle_unknown_exception
@handle_unique__user_constraint
def register_company_employee(db:Session, data:UserPostModel, admin:User)->User:
    new_user = User(**data.model_dump())
    new_user.password = get_hashed_password(data.password)
    new_user.company_id = admin.company_id
    new_user.created_at = datetime.now(timezone.utc)
    new_user.updated_at = datetime.now(timezone.utc)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@handle_unknown_exception
@handle_unique__user_constraint
def register_unaffiliated_user(db:Session, data:UserPostModel)->User:
    new_user = User(**data.model_dump())
    new_user.password = get_hashed_password(data.password)
    new_user.company_id = UUID(NONE_COMPANY_ID)
    new_user.created_at = datetime.now(timezone.utc)
    new_user.updated_at = datetime.now(timezone.utc)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_all_employees(db:Session, company_id: UUID):
    query = select(User).where(User.company_id == company_id)
    return db.scalars(query).all()