from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    vehicle_type: Optional[str] = None

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False



class UserCreate(UserBase):
    email: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


# class UserInDBBase(UserBase):
#     id: Optional[str] = None

#     class Config:
#         orm_mode = True


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    hashed_password: str