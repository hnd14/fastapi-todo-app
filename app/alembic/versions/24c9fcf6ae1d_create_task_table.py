"""create_task_table

Revision ID: 24c9fcf6ae1d
Revises: 1e3fe4085d90
Create Date: 2024-08-23 16:30:55.551129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas.enum import Priority, Status


# revision identifiers, used by Alembic.
revision: str = '24c9fcf6ae1d'
down_revision: Union[str, None] = '1e3fe4085d90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tasks",
                    sa.Column("id", sa.Uuid, primary_key=True),
                    sa.Column("title", sa.String),
                    sa.Column("summary", sa.String),
                    sa.Column("status", sa.Enum(Status), nullable=False),
                    sa.Column("priority", sa.Enum(Priority), nullable=False),
                    sa.Column("created_at", sa.DateTime, nullable=False),
                    sa.Column("updated_at", sa.DateTime, nullable=False),
                    sa.Column("created_by_id", sa.Uuid, nullable=False),
                    sa.Column("assigned_to_id", sa.Uuid, nullable=True), 
                    sa.Column("company_id", sa.Uuid, nullable=False))
    op.create_foreign_key("fk_tasks_creator", "tasks", "users", ["created_by_id"], ["id"])
    op.create_foreign_key("fk_tasks_assignee", "tasks", "users", ["assigned_to_id"], ["id"])
    op.create_foreign_key("fk_tasks_company", "tasks", "companies", ["company_id"], ["id"])

def downgrade() -> None:
    op.drop_table("tasks")
    op.execute("DROP TYPE status;")
    op.execute("DROP TYPE priority;")
