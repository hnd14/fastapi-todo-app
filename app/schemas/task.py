from sqlalchemy import Column, String, Enum, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from schemas.base_entity import BaseEntity
from schemas.enum import Priority, Status
from schemas.user import User
from schemas.company import Company

class Task(Base, BaseEntity):
    __tablename__ = "tasks"
    
    title = Column(String, nullable=False)
    summary = Column(String)
    status = Column(Enum(Status), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    created_by_id = Column(Uuid, ForeignKey(User.id))
    assigned_to_id = Column(Uuid, ForeignKey(User.id))
    company_id = Column(Uuid, ForeignKey(Company.id))
    
    created_by = relationship("User", back_populates="tasks_created",
                              foreign_keys="Task.created_by_id", lazy="joined")
    assigned_to = relationship("User", back_populates="tasks_assigned",
                               foreign_keys="Task.assigned_to_id", lazy="joined")
    company = relationship("Company", back_populates="tasks")