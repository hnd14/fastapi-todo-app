from sqlalchemy import Column, String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from schemas.base_entity import BaseEntity
from schemas.company import Company
from database import Base

class User(Base, BaseEntity):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    company_id = Column(Uuid, ForeignKey(Company.id))
    
    company = relationship("Company", back_populates="employees")
    tasks_created = relationship("Task", back_populates="created_by",
                                 foreign_keys="Task.created_by_id")
    tasks_assigned = relationship("Task", back_populates="assigned_to",
                                  foreign_keys="Task.assigned_to_id")