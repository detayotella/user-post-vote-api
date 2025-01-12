from typing import Literal 
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel): 
    title: str
    content: str 
    published: bool = True 

class PostCreate(PostBase): 
    # same things as postbase 
    pass 


class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

class Post(BaseModel): 
    id: int 
    title: str 
    content: str 
    published: bool 
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config: 
        from_attributes = True  # Allow SQLAlchemy model to be used with Pydantic model


class UserCreate(BaseModel): 
    email: EmailStr
    password: str 

    class Config: 
        from_attributes = True 

class PostOut(BaseModel): 
    Post: Post
    votes: int

class UserLogin(BaseModel): 
    email: EmailStr 
    password: str 

class Token(BaseModel): 
    access_token: str 
    token_type: str 

class TokenData(BaseModel): 
    id: int | None = None  


class Vote(BaseModel):
    post_id: int 
    dir: Literal[0, 1] 

