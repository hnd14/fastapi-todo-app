from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from schemas.enum import Status, Priority
from models.user import UserViewModel

class TaskPostModel(BaseModel):
    title: str = Field(min_length=1)
    summary: str = Field(default=None)
    status: Status = Field(default=Status.NEW)
    priority: Priority = Field(default=Priority.MEDIUM)
    assigned_to_id: UUID = Field(default=None)
    
class TaskViewModel(BaseModel):
    id: UUID
    title: str
    summary: str
    status: Status
    priority: Priority
    
    created_by: UserViewModel
    assigned_to: UserViewModel | None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
