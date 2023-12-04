import enum

from sqlalchemy import Column, Boolean, Date, Enum, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"  # type: ignore
    moderator: str = "moderator"  # type: ignore
    user: str = "user"  # type: ignore


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False, index=True)
    thurname = Column(String(30), nullable=False, index=True)
    email = Column(String(20), nullable=False, unique=True, index=True)
    phone = Column(String(20), unique=True)
    birthday = Column(Date)
    notes = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column("crated_at", DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column("roles", Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    password_needs_reset = Column(Boolean, default=False)


# alembic init migrations
# alembic revision --autogenerate -m "init" <- create first migration
# alembic upgrade heads <- to apply migration
# alembic revision --autogenerate -m "add user"
# alembic revision --autogenerate -m "add user role"
# alembic revision --autogenerate -m "add field confirmed"
# alembic revision --autogenerate -m "add reset password"
