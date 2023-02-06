from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from schema.devices import System


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    
class Login(BaseModel):
    username: str
    password: str
    

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str
    address: str
    admin: bool = False
    premium: bool = False
        
    
class UserCreate(UserBase):
    password: str
    delisted: bool = True
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()
        
class User(UserBase):
    delisted: bool
    updated_at: datetime
    created_at: datetime
    systems: list[System] = []
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    address: Optional[str]
    email: Optional[EmailStr]
    updated_at: datetime = datetime.now()
    delisted: Optional[bool]
    
