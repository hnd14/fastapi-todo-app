"""create company table

Revision ID: ff596d4aad55
Revises: 
Create Date: 2024-08-23 15:54:21.324975

"""
from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

from schemas.enum import Mode
from settings import SYSTEM_COMPANY_ID, NONE_COMPANY_ID


# revision identifiers, used by Alembic.
revision: str = 'ff596d4aad55'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company_table = op.create_table("companies",
                    sa.Column("id", sa.Uuid, nullable=False, primary_key=True),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("description", sa.String, nullable=True),
                    sa.Column("mode", sa.Enum(Mode), nullable=False),
                    sa.Column("created_at", sa.DateTime, nullable=False),
                    sa.Column("updated_at", sa.DateTime, nullable=False),
                    )
    
    op.bulk_insert(company_table, [
        {
            "id":SYSTEM_COMPANY_ID,
            "name": "System management",
            "description": "The system administrators.",
            "mode": Mode.SYSTEM,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id":NONE_COMPANY_ID,
            "name": "None",
            "description": "Unaffiliated",
            "mode": Mode.SYSTEM,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])

def downgrade() -> None:
     op.drop_table("companies")
     op.execute ("DROP TYPE mode;")
