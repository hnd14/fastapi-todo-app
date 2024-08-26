from typing import List
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.company import CompanyPostModel
from schemas import Company

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