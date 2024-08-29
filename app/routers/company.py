from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db_context
from exception import ResourceNotFoundException, ForbiddenOperationException
from models.company import CompanyViewModel, CompanyPostModel
from schemas.user import User
from services import  company as CompanyService
from services.auth import requires_system_admin, token_interceptor
from settings import SYSTEM_COMPANY_ID, NONE_COMPANY_ID

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("")
def find_all_company_with_filter(*, search_kw: str = Query(default=""),
                                 page_size: int = Query(default=10, ge=1, le=100),
                                 page_number: int = Query(default=1, ge=1), 
                                 db:Session = Depends(get_db_context)):
    return CompanyService.find_all_company_with_filter(db, search_kw=search_kw,
                                        page_number=page_number,
                                        page_size=page_size,
                                        )
@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
def create_company(request: CompanyPostModel,
                   db: Session = Depends(get_db_context),
                   user: User = Depends(token_interceptor)):
    requires_system_admin(user)
    return CompanyService.create_company(db, request)

@router.put("/{id}", response_model=CompanyViewModel)
def update_company(id: UUID, request: CompanyPostModel, db: Session = Depends(get_db_context), 
                   user: User = Depends(token_interceptor)):
    requires_system_admin(user)
    if id == UUID(SYSTEM_COMPANY_ID) or id == UUID(NONE_COMPANY_ID):
        raise ForbiddenOperationException
    return CompanyService.update_company(db, id, request)

@router.get("/{id}", response_model=CompanyViewModel)
def get_one_company(id: UUID, db: Session = Depends(get_db_context)):
    company = CompanyService.get_company_by_id(db, id)
    if company is None:
        raise ResourceNotFoundException("Company")
    return company

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_company(id: UUID, db: Session = Depends(get_db_context), 
                   user: User = Depends(token_interceptor)):
    requires_system_admin(user)
    if id == UUID(SYSTEM_COMPANY_ID) or id == UUID(NONE_COMPANY_ID):
        raise ForbiddenOperationException()
    CompanyService.delete_company(db, id)