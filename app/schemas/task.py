from sqlalchemy import Column, String, Enum, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from schemas.base_entity import BaseEntity
from schemas.enum import Priority, Status
from schemas.user import User

class Task(Base, BaseEntity):
    __tablename__ = "tasks"
    
    summary = Column(String)
    status = Column(Enum(Status), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    created_by_id = Column(Uuid, ForeignKey(User.id))
    assigned_to_id = Column(Uuid, ForeignKey(User.id))
    
    created_by = relationship("User", back_populates="tasks_created", foreign_keys="Task.created_by_id")
    assigned_to = relationship("User", back_populates="tasks_assigned", foreign_keys="Task.assigned_to_id")