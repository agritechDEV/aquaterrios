from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from route.users import user_router
from webroutes.admin import web_router
from route.protected import base_router
from route.general import general_router
from route.api import api_router

origins = ["http://localhost:3000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router, tags=["users"])
app.include_router(web_router)
app.include_router(base_router, prefix="/base", tags=["base"])
app.include_router(general_router, prefix="/general", tags=["general"])
app.include_router(api_router, prefix="/api", tags=["API"])




