from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from database import Base
from schemas.base_entity import BaseEntity
from schemas.enum import Mode

class Company(Base, BaseEntity):
    __tablename__ = "companies"
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(Enum(Mode), nullable=True)
    
    employees = relationship("User", back_populates="company")