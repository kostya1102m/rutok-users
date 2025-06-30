from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(String(10), nullable=False, unique=True)
    role_description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(Text, nullable=True)
    user_name = Column(String(30), nullable=False)
    banned = Column(Boolean, nullable=False, default=False)
    avatar = Column(LargeBinary, nullable=True)
    phone = Column(String(11), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    hash_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)

    role = relationship("Role", back_populates="users")