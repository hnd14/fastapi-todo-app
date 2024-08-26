from sqlalchemy import Column, Uuid, Time
from uuid import uuid4

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)