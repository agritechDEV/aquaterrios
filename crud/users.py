from sqlalchemy.orm import Session

from db import models
from schema.users import UserCreate
from utils.auth import get_hashed_password



def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

def get_user_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: UserCreate):
    db_user = models.User(email=user.email, username = user.username, hashed_password=get_hashed_password(user.password), 
        name=user.name, surname=user.surname, address=user.address, admin=user.admin, premium=user.premium, delisted=user.delisted)
    if db_user.username == "admin":
        db_user.delisted = False
        db_user.admin = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user