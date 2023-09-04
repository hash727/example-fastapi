from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class User(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
#    rating: Optional[int] = None

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class config:
        orm_mode=True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class config:
        orm_mode=True
        
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)