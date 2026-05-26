
from pydantic import BaseModel, EmailStr
from typing import Optional
from models import UserRole

# Request Schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role:UserRole = UserRole.user


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# -----------------------------
# User Data Schema
# -----------------------------

class UserData(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# -----------------------------
# Response Schemas
# -----------------------------

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserData


class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str

class changePasswordRequest(BaseModel):
    old_password:str
    new_password:str


class AllUsersResponse(BaseModel):
    success: bool
    message: str
    data: list[UserData]

class PaginationMeta(BaseModel):
    skip: int
    limit: int
    total: int

class PaginatedUserResponse(BaseModel):
    success: bool
    message: str
    data: list[UserData]
    meta: PaginationMeta
