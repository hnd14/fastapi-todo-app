from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from exception import DuplicatedResourceException, UnauthorizedException, ResourceNotFoundException, InvalidActionException, handle_unknown_exception
from services.auth import get_hashed_password, verify_password
from models.user import UserPostModel, UserPatchInfoModel, UserPatchPasswordModel
from schemas.user import User
from settings import SYSTEM_COMPANY_ID, NONE_COMPANY_ID

def handle_unique_username_constraint(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if "uq_user_name" in str(e.orig):
                raise DuplicatedResourceException("Username")
            raise e
    return decorate

def handle_unique_email_constraint(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if "uq_email" in str(e.orig):
                raise DuplicatedResourceException("Email")
            raise e
    return decorate

@handle_unknown_exception
@handle_unique_username_constraint
@handle_unique_email_constraint
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
@handle_unique_username_constraint
@handle_unique_email_constraint
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
@handle_unique_username_constraint
@handle_unique_email_constraint
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
@handle_unique_username_constraint
@handle_unique_email_constraint
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

@handle_unknown_exception
def get_all_employees(db: Session, company_id: UUID):
    query = select(User).where(User.company_id == company_id)
    return db.scalars(query).all()

@handle_unknown_exception
def get_user_by_id(db: Session, id: UUID) -> User:
    query = select(User).filter(User.id == id)
    
    return db.scalars(query).first() 

@handle_unknown_exception
@handle_unique_email_constraint
def update_user_info(db: Session, user_id:UUID, data: UserPatchInfoModel, user: User):
    user_to_update = get_user_by_id(db, user_id)
    if not user_to_update.company_id == user.company_id:
        raise UnauthorizedException
    
    user_to_update.first_name = data.first_name or user_to_update.first_name
    user_to_update.last_name = data.last_name or user_to_update.last_name
    user_to_update.email = data.email or user_to_update.email
    user_to_update.is_admin = data.is_admin if data.is_admin != None else user_to_update.is_admin
    user_to_update.is_active = data.is_active if data.is_active != None else user_to_update.is_active
    
    db.commit()
    db.refresh(user_to_update)
    
    return user_to_update

@handle_unknown_exception
def update_password(db: Session, data: UserPatchPasswordModel, user: User):
    user_to_update = get_user_by_id(db, user.id)
    if verify_password(data.new_password, user_to_update.password):
        raise UnauthorizedException()
    user_to_update.password = get_hashed_password(data.new_password)
    db.commit()

@handle_unknown_exception
def add_to_company(db:Session, employee_id: UUID, user: User):
    employee = get_user_by_id(db, employee_id)
    if employee is None:
        raise ResourceNotFoundException("User")
    
    if employee.company_id != UUID(NONE_COMPANY_ID):
        raise InvalidActionException("User belongs to another company")
    
    employee.company_id = user.company_id
    
    db.commit()
    db.refresh(employee)
    
    return employee

@handle_unknown_exception
def remove_from_company(db:Session, employee_id: UUID, user: User):
    employee = get_user_by_id(db, employee_id)
    if employee is None:
        raise ResourceNotFoundException("User")
    
    if employee.company_id != user.company_id:
        raise InvalidActionException("User belongs to another company")
    
    employee.company_id = UUID(NONE_COMPANY_ID)
    employee.is_admin = False
    
    db.commit()
    db.refresh(employee)
    
    return employee
