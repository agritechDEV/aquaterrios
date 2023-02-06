from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from schema.users import User
from crud.login import get_current_user
from crud.users import  get_users
from db.database import get_db



web_router = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")


@web_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@web_router.get("/profile", response_model=User)
def current_user(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    users = get_users(db=db)
    if not user:
        return {"detail": "You are not logged in"}
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": user, "users": users})
