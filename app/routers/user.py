from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserPostModel, UserViewModel
from services import user as UserService
from services.auth import requires_system_admin, token_interceptor
from schemas.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@requires_system_admin
@router.post("/system-admin", response_model=UserViewModel)
def register_system_admin(request:UserPostModel, 
                          db: Session = Depends(get_db_context), 
                          user:User = Depends(token_interceptor)):
    return UserService.register_system_admin(db, request)
    