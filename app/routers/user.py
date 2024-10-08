from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserPostModel, UserViewModel, UserPatchInfoModel, UserPatchPasswordModel
from services import user as UserService
from services.auth import requires_system_admin, token_interceptor, requires_company_admin
from schemas.user import User

router = APIRouter(prefix="/users")

@router.post("/system-admin", response_model=UserViewModel, status_code=status.HTTP_201_CREATED, tags=["Required System Admin"])
def register_system_admin(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor(requires_system_admin))):
    return UserService.register_system_admin(db, request)


@router.post("/company-admin", response_model=UserViewModel, status_code=status.HTTP_201_CREATED, tags=["Required System Admin"])
def register_company_admin(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor(requires_system_admin))):
    return UserService.register_admin(db, request)

@router.post("/employee", response_model=UserViewModel, status_code=status.HTTP_201_CREATED,  tags=["Required company admin"])
def register_company_employee(request:UserPostModel, 
                          db: Session = Depends(get_db_context),
                          user:User = Depends(token_interceptor(requires_company_admin))):
    return UserService.register_company_employee(db, request, user)

@router.post("/unaffiliated", response_model=UserViewModel, status_code=status.HTTP_201_CREATED, tags=["Public"])
def register_unaffiliated_user(request:UserPostModel, 
                          db: Session = Depends(get_db_context)):
    return UserService.register_unaffiliated_user(db, request)
    
@router.get("/employees", response_model=List[UserViewModel],  tags=["Required company admin"])
def get_all_employees_from_same_company(db: Session = Depends(get_db_context),
                            user:User = Depends(token_interceptor(requires_company_admin))):
    return UserService.get_all_employees(db, user.company_id)

@router.patch("/info/me", response_model=UserViewModel, tags=["User info"])
def edit_employee_info(request: UserPatchInfoModel,
                       db: Session = Depends(get_db_context),
                       user: User = Depends(token_interceptor(None))):
    return UserService.update_user_info(db, user.id, request, user)

@router.patch("/password/me", status_code=status.HTTP_204_NO_CONTENT, tags=["User info"])
def edit_employee_info(request: UserPatchPasswordModel,
                       db: Session = Depends(get_db_context),
                       user: User = Depends(token_interceptor(None))):
    return UserService.update_password(db, request, user)

@router.patch("/info/employees/{id}", response_model=UserViewModel, tags=["Required company admin"])
def edit_employee_info(id: UUID, 
                       request: UserPatchInfoModel,
                       db: Session = Depends(get_db_context),
                       user: User = Depends(token_interceptor(requires_company_admin))):
    return UserService.update_user_info(db, id, request, user)

@router.patch("/add-to-company/employees/{id}", response_model=UserViewModel, tags=["Required company admin"])
def edit_employee_info(id: UUID,
                       db: Session = Depends(get_db_context),
                       user: User = Depends(token_interceptor(requires_company_admin))):
    return UserService.add_to_company(db, id, user)

@router.patch("/remove-from-company/employees/{id}", response_model=UserViewModel, tags=["Required company admin"])
def edit_employee_info(id: UUID,
                       db: Session = Depends(get_db_context),
                       user: User = Depends(token_interceptor(requires_company_admin))):
    return UserService.remove_from_company(db, id, user)