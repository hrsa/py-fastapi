from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = "Anonymous"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class Vote(BaseModel):
    post_id: int
    value: conint(ge=0, le=1)


class VoteResponse(BaseModel):
    user_id: int
    post_id: int
    status: Optional[str]


class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    rating: Optional[int] = None


class PostCreate(PostBase):
    published: Optional[bool] = True


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = False
    rating: Optional[int] = None


class PostResponse(PostBase):
    id: int
    likes: int
    author_id: int
    rating: Optional[int]
    created_at: datetime
    author: UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    email: EmailStr
