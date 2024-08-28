"""create user table

Revision ID: 1e3fe4085d90
Revises: ff596d4aad55
Create Date: 2024-08-23 16:06:04.454182

"""
from typing import Sequence, Union
from uuid import uuid4
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

from services.auth import get_hashed_password
from settings import ADMIN_DEFAULT_PASSWORD, SYSTEM_COMPANY_ID


# revision identifiers, used by Alembic.
revision: str = '1e3fe4085d90'
down_revision: Union[str, None] = 'ff596d4aad55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table("users",
                    sa.Column("id", sa.Uuid, nullable=False, primary_key=True),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("username", sa.String, nullable=False),
                    sa.Column("first_name", sa.String, nullable=False),
                    sa.Column("last_name", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("is_active", sa.Boolean, nullable=False),
                    sa.Column("is_admin", sa.Boolean, nullable=False),
                    sa.Column("created_at", sa.DateTime, nullable=False),
                    sa.Column("updated_at", sa.DateTime, nullable=False),
                    sa.Column("company_id", sa.Uuid, nullable=False))
    op.create_foreign_key("fk_users_comp", "users", "companies", ["company_id"], ["id"])
    
    op.bulk_insert(user_table, [{
        "id" : uuid4(),
        "email": "admin@todoapp.com",
        "username": "todo_admin",
        "first_name": "admin",
        "last_name": "admin",
        "password": get_hashed_password(ADMIN_DEFAULT_PASSWORD),
        "is_admin": True,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc), 
        "company_id": SYSTEM_COMPANY_ID
    }])


def downgrade() -> None:
    op.drop_table("users")
