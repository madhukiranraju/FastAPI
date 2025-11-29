from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


#USER SCHEMAS

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



#POST SCHEMAS


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value is True

class PostCreate(PostBase):
    pass


# Forcing request body to be a dictionary
class Post(PostBase):
    id: Optional[int] = None  # Optional field
    owner_id: int
    created_at: datetime
    owner: UserOut
    class Config: ## this is required when returning the 
        from_attributes = True



# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True  # Default value is True


# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool  # Default value is True




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    class Config:
        from_attributes = True


class VoteBase(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) = 0 #type: ignore # 1 for upvote, 0 for remove vote 

class PostVoteOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True  