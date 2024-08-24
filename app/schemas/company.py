from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base
from schemas.base_entity import BaseEntity

class Company(Base, BaseEntity):
    __tablename__ = "companies"
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    
    employees = relationship("User", back_populates="company")