from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(10), nullable=False)
    role_description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(Text, nullable=True)
    username = Column(String(30), nullable=False)
    banned = Column(Boolean, nullable=False, default=False)
    avatar = Column(LargeBinary, nullable=True)
    phone = Column(String(11), nullable=True)
    email = Column(String(255), nullable=True)
    hash_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    role = relationship("Role", back_populates="users")