from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from schemas.base_entity import BaseEntity
from database import Base

class User(Base, BaseEntity):
    __tablename__ = "users"
    
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    
    company = relationship("Company", back_populates="employees")
    tasks_created = relationship("Task", back_populates="created_by")