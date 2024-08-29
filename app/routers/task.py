from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from database import get_db_context
from models.task import TaskPostModel, TaskViewModel
from schemas.user import User
from services import task as TaskService
from services.auth import token_interceptor, requires_company_admin

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
def create_new_task(request: TaskPostModel,
                    db: Session = Depends(get_db_context),
                    user: User = Depends(token_interceptor)):
    requires_company_admin(user)
    return TaskService.create_task(db, request, user)
