from sqlalchemy import Column, String, Integer, Enum
from app.db.db import Base
import enum

class UserRole(str, enum.Enum):
    admin = "Admin"
    customer = "Customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)