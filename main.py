from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: EmailStr
    password: str

@app.get("/")
async def home():
    return [{"name": "Nikola", "gender": "male", "age": 46}, 
            {"name": "Gordana", "gender": "female", "age": 47}]
    
@app.post("/")
async def create_user(user: User):
    return user