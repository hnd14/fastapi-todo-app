from typing import List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.company import CompanyPostModel
from schemas import Company
from exception import ResourceNotFoundException

def find_all_company_with_filter(db: Session, /, *, search_kw = "", page_size = 10, page_number = 1) -> List[Company]:
    query = select(Company).where(Company.name.like(f"%{search_kw}%"))\
            .offset((page_number-1)*page_size) \
            .limit(page_size)
    return db.scalars(query).all()

def create_company(db: Session, data: CompanyPostModel) -> Company:
    company = Company(**data.model_dump())
    company.created_at = datetime.now(timezone.utc)
    company.updated_at = datetime.now(timezone.utc)
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company

def get_company_by_id(db: Session, id: UUID) -> Company:
    query = select(Company).filter(Company.id == id)
    
    return db.scalars(query).first()

def update_company(db: Session, id:UUID, data: CompanyPostModel) -> Company:
    company = get_company_by_id(db, id)
    
    if company is None:
        raise ResourceNotFoundException("Company")
    
    company.name = data.name
    company.description = data.description
    company.mode = data.mode
    company.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(company)
    
    return company