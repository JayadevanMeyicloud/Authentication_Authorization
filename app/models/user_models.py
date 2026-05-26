#DB creation
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(String, nullable=False)

    role = Column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False
    )
