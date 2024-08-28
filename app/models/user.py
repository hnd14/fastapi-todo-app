from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from settings import NONE_COMPANY_ID

class UserPostModel(BaseModel):
    email: str = Field(pattern=".+@.+\..+")
    username: str = Field(min_length=6)
    first_name: str = Field(min_length=1) 
    last_name: str = Field(min_length=1) 
    password: str = Field(min_length=8) 
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False) 
    company_id: UUID = Field(default=UUID(NONE_COMPANY_ID))
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@sample.com",
                "username": "exampleUser",
                "first_name": "example",
                "last_name": "user",
                "password": "exUser123"
            }
        }
        
class UserViewModel(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str  
    is_active: bool
    is_admin: bool 
    company_id: UUID