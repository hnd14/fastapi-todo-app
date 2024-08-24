from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from database import Base
from schemas.base_entity import BaseEntity
from schemas.enum import Priority, Status

class Task(Base, BaseEntity):
    __tablename__ = "tasks"
    
    summary = Column(String)
    status = Column(Enum(Status), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    
    created_by = relationship("Users", back_populates="tasks_created")