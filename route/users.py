from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from schema.users import User, UserCreate, Token
from utils.auth import create_access_token
from db.database import get_db
from crud import users, login

user_router = APIRouter()


@user_router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code = 400, detail="Username already exists")
    user_mail= users.get_user_email(db, email=user.email)
    if user_mail:
        raise HTTPException(status_code = 400, detail="Email already exists")
    user = users.create_user(user=user, db=db)
    return {"detail": "New user was created successfully"}

@user_router.get("/users", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    db_users = users.get_users(db=db)
    return db_users

@user_router.post("/login", response_model=Token)
def log_user(user: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    db_user = login.validate_user(db=db, user=user)

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(
        data={"sub": user.username}
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    
    token = jsonable_encoder(access_token)
    content = {"detail": "You've successfully logged in. Wellcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )
    return response


