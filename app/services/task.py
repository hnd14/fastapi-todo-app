from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.enum import Status
from exception import InvalidActionException, ResourceNotFoundException, handle_unknown_exception
from schemas.task import Task
from schemas.user import User
from services.user import get_user_by_id
from models.task import TaskPostModel, TaskAssigneePatchModel, TaskInfoPatchModel

def verify_assignee(assignee: User, user: User):
    if assignee.company_id != user.company_id:
        raise InvalidActionException("You cannot assign task to a user from a different company")

@handle_unknown_exception
def create_task(db:Session, data: TaskPostModel, user: User):
    assignee = get_user_by_id(db, data.assigned_to_id)
    
    if assignee is None and data.assigned_to_id is not None:
        raise ResourceNotFoundException("Assignee")
    
    if assignee is not None:
        verify_assignee(assignee, user)
    
    task = Task(**data.model_dump())
    task.created_by_id = user.id
    task.company_id = user.company_id
    task.created_at = datetime.now(timezone.utc)
    task.updated_at = datetime.now(timezone.utc)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

@handle_unknown_exception
def find_task_with_filters(db: Session,
                           assignee_id: UUID | None, 
                           creator_id: UUID | None,
                           status: Status | None,
                           user: User):
    query = select(Task)
    query = query.filter_by(assigned_to_id = assignee_id) if assignee_id is not None else query
    query = query.filter_by(created_by_id = creator_id) if creator_id is not None else query
    query = query.filter_by(status = status) if status is not None else query
    query = query.filter_by(company_id = user.company_id)
    
    return db.scalars(query).all()

@handle_unknown_exception
def get_task_by_id(db: Session, id: UUID):
    return db.scalars(select(Task).filter_by(id=id)).first()

@handle_unknown_exception
def update_task_assignee(db: Session, id: UUID, data: TaskAssigneePatchModel, user: User):
    assignee = get_user_by_id(db, data.assigned_to_id)
    
    if assignee is None:
        raise ResourceNotFoundException("Assignee")
    
    verify_assignee(assignee, user)
        
    task = get_task_by_id(db, id)
    
    if task is None:
        raise ResourceNotFoundException("Task")
    
    task.assigned_to_id = data.assigned_to_id
    
    db.commit()
    db.refresh(task)
    
    return task
    
@handle_unknown_exception
def update_task_info(db: Session, id: UUID, data: TaskInfoPatchModel):
    task = get_task_by_id(db, id)
    
    if task is None:
        raise ResourceNotFoundException("Task")
    
    task.priority = data.priority or task.priority
    task.title = data.title or task.title
    task.summary = data.summary or task.summary
    task.status = data.status or task.status
    
    db.commit()
    db.refresh(task)
    
    return task
