from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserPostModel, UserViewModel
from services import user as UserService
from services.auth import requires_system_admin, token_interceptor, requires_company_admin
from schemas.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/system-admin", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
def register_system_admin(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor)):
    requires_system_admin(user)
    return UserService.register_system_admin(db, request)


@router.post("/company-admin", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
def register_company_admin(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor)):
    requires_system_admin(user)
    return UserService.register_admin(db, request)

@router.post("/employee", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
def register_company_employee(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor)):
    requires_company_admin(user)
    return UserService.register_company_employee(db, request, user)

@router.post("/unaffiliated", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
def register_unaffiliated_user(request:UserPostModel, 
                          db: Session = Depends(get_db_context)):
    return UserService.register_unaffiliated_user(db, request)
    
@router.get("/employees", response_model=List[UserViewModel])
def get_all_employees_from_same_company(db: Session = Depends(get_db_context),
                            user:User = Depends(token_interceptor)):
    requires_company_admin(user)
    return UserService.get_all_employees(db, user.company_id)