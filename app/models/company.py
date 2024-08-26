from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class CompanyPostModel(BaseModel):
    name: str = Field(min_length=1)
    description :str = Field(max_length=255)
    mode: str = Field(max_length=50)
    
class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: str
    created_at: datetime
    updated_at: datetime