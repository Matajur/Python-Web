"""Init

Revision ID: bbe4d32807e9
Revises: 
Create Date: 2023-08-21 00:12:56.928726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbe4d32807e9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups')
    op.drop_table('professors')
    op.drop_table('disciplines')
    op.drop_table('students')
    op.drop_table('grades')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('grade', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date_of', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('discipline_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.id'], name='grades_discipline_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='grades_student_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='grades_pkey')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='students_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='students_pkey')
    )
    op.create_table('disciplines',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('professor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['professor_id'], ['professors.id'], name='disciplines_professor_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='disciplines_pkey'),
    sa.UniqueConstraint('name', name='disciplines_name_key')
    )
    op.create_table('professors',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='professors_pkey'),
    sa.UniqueConstraint('fullname', name='professors_fullname_key')
    )
    op.create_table('groups',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='groups_pkey'),
    sa.UniqueConstraint('name', name='groups_name_key')
    )
    # ### end Alembic commands ###