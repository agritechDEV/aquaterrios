from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from crud.users import get_user
from utils.auth import oauth2_scheme, verify_token, verify_password



async def get_current_user(db: Session, token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)  
    current_user = await get_user(db, username=token_data.username)
    if current_user is None:
        raise credentials_exception
    
    return current_user


async def validate_user(db: Session, user: OAuth2PasswordRequestForm = Depends()):
    try:
        db_user = await get_user(db=db, username=user.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )   

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user