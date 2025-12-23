"""create categories

Revision ID: ba8ca2de27a9
Revises: c11a09ed5954
Create Date: 2025-12-07 19:56:00.242954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba8ca2de27a9'
down_revision: Union[str, Sequence[str], None] = 'c11a09ed5954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    meta = sa.MetaData()
    expense_category = sa.Table('expense_category',meta,autoload_with=op.get_bind())
    op.bulk_insert(expense_category,
                   [ {"category":e} for e in ["Groceries","Leisure","Electronics","Clothing","Health","Others"]]
                   )


def downgrade() -> None:
    """Downgrade schema."""
    meta = sa.MetaData()
    expense_category = sa.Table('expense_category',meta,autoload_with=op.get_bind())
    stmt = sa.delete(expense_category)
    op.execute(stmt)
