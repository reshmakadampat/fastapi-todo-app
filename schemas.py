from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)