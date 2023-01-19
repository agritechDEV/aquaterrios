from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from schema import users


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str
    address: str
    admin: bool
    premium: bool
        
    
class UserCreate(UserBase):
    password: str
    delisted: bool = True
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()
        
class User(UserBase):
    updated_at: datetime
    created_at: datetime
    systems: list[users.System] = []
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    address: Optional[str]
    email: Optional[EmailStr]
    updated_at: datetime = datetime.now()
    delisted: Optional[bool]
    
