from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter, status, Query
from sqlalchemy.orm import Session

from database import get_db_context
from models.task import TaskPostModel, TaskViewModel, TaskAssigneePatchModel, TaskInfoPatchModel
from schemas.enum import Status
from schemas.user import User
from services import task as TaskService
from services.auth import token_interceptor, requires_company_admin

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
def create_new_task(request: TaskPostModel,
                    db: Session = Depends(get_db_context),
                    user: User = Depends(token_interceptor(requires_company_admin))):
    return TaskService.create_task(db, request, user)

@router.get("", response_model=List[TaskViewModel])
def get_tasks_with_filter(assignee_id: UUID | None = Query(default=None),
                                 creator_id: UUID | None = Query(default=None),
                                 status: Status | None = Query(default=None), 
                                 db: Session = Depends(get_db_context),
                                 user: User = Depends(token_interceptor(requires_company_admin))):
    return TaskService.find_task_with_filters(db, assignee_id, creator_id, status, user)

@router.get("/me/assigned", response_model=List[TaskViewModel])
def get_my_assigned_tasks(status: Status | None = Query(default=None),
                          db: Session = Depends(get_db_context),
                          user: User = Depends(token_interceptor)):
    return TaskService.find_task_with_filters(db, user.id, None, status, user)

@router.get("/me/created", response_model=List[TaskViewModel])
def get_my_created_tasks(status: Status | None = Query(default=None),
                          db: Session = Depends(get_db_context),
                          user: User = Depends(token_interceptor)):
    return TaskService.find_task_with_filters(db, None, user.id, status, user)

@router.patch("/info/{id}", response_model=TaskViewModel)
def update_task_info(id: UUID,
                     request: TaskInfoPatchModel,
                     db: Session = Depends(get_db_context),
                     _: User = Depends(token_interceptor)):
    return TaskService.update_task_info(db, id, request)

@router.patch("/assignee/{id}", response_model=TaskViewModel)
def update_task_info(id: UUID,
                     request: TaskAssigneePatchModel,
                     db: Session = Depends(get_db_context),
                     user: User = Depends(token_interceptor(requires_company_admin))):
    return TaskService.update_task_assignee(db, id, request, user)