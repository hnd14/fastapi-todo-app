from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from schemas.enum import Mode


class CompanyPostModel(BaseModel):
    name: str = Field(min_length=1)
    description :str = Field(max_length=255)
    mode: Mode = Field()
    
class CompanyPatchModel(BaseModel):
    description :str = Field(max_length=255)
    mode: Mode = Field()
    
class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: Mode
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True