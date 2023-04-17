from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schema.devices import System, Pump, Valve, Sensor, Shifts
from crud import devices


general_router = APIRouter()

@general_router.get("/systems", response_model=list[System])
def read_systems(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    db_systems = devices.get_systems(db=db, skip=skip, limit=limit)
    return db_systems

@general_router.get("/pumps", response_model=list[Pump])
def read_pumps(db: Session = Depends(get_db), skip: int=0, limit: int = 50):
    db_pumps = devices.get_pumps(db=db, skip=skip, limit=limit)
    return db_pumps

@general_router.get("/valves", response_model=list[Valve])
def read_valves(db: Session = Depends(get_db), skip: int=0, limit: int = 50):
    db_valves = devices.get_valves(db=db, skip=skip, limit=limit)
    return db_valves