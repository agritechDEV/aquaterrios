from sqlalchemy.orm import Session
from db import models


async def get_user(db: Session, username: str):
    return await db.query(models.User).filter(models.User.username == username).first()