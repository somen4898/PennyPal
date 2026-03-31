"""add unique constraint on group_members (group_id, user_id)

Revision ID: a1b2c3d4e5f6
Revises: 5624dc19be0a
Create Date: 2026-03-31 01:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"  # pragma: allowlist secret
down_revision = "5624dc19be0a"  # pragma: allowlist secret
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_group_member", "group_members", ["group_id", "user_id"])


def downgrade() -> None:
    op.drop_constraint("uq_group_member", "group_members", type_="unique")
