from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional


#Pump's schemas    
class Flow(BaseModel):
    pump_id: str
    capacity: float | None = None
    max_flow: float | None = None
    available: float | None = None
    current: float | None = None
    

class AddPump(Flow):
    system_id: int
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

class UpdatePump(BaseModel):
    current: float
    updated_at: datetime = datetime.now()

class Pump(Flow):
    system_id: int
    updated_at: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class FlowData(BaseModel):
    pump_id: str
    flow_rate: float
    updated_at: datetime = datetime.now()
    
    class Config:
        orm_mode = True
    

#Valve's schemas
class ValveBase(BaseModel):
    valve_id: str
    status: bool | None = None
    mode: str 
    shift_id: Optional[int]
    
class AddValve(ValveBase):
    system_id: int
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

class UpdateValve(BaseModel):
    status: Optional[bool]
    mode: Optional[str]
    shift_id: Optional[bool]
    updated_at: datetime = datetime.now()

class Valve(ValveBase):
    system_id: int
    updated_at: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True

#Sensor's schemas        
class SensorBase(BaseModel):
    sensor_id: str
    readings: float | None = None
    level_1: bool
    level_2: bool
    level_3: bool
    shift_id: int | None = None
    
    
class AddSensor(SensorBase):
    system_id: int
    updated_at: datetime = datetime.now() 
    created_at: datetime = datetime.now()

class UpdateSensor(SensorBase):
    readings: Optional[float]
    shift_id: Optional[int]
    level_1: Optional[bool]
    level_2: Optional[bool]
    level_3: Optional[bool]
    updated_at: datetime = datetime.now() 

class Sensor(SensorBase):
    system_id: int
    
    class Config:
        orm_mode = True


class SensorData(BaseModel):
    sensor_id: str
    updated_at: datetime = datetime.now()
    bat_level: float
    level_1: float
    level_2: float
    level_3: float
    temperature: float
    moisture: float
    
    class Config:
        orm_mode = True   
        

class ShiftBase(BaseModel):
    mode: str 
    turn_on: float | None = None
    turn_off: float | None = None
    Mon: bool | None = None
    Tue: bool | None = None
    Wed: bool | None = None
    Thu: bool | None = None
    Fri: bool | None = None
    Sat: bool | None = None
    Sun: bool | None = None
    start: time | None = None
    stop: time | None = None

class AddShift(ShiftBase):
    system_id: int
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()
    
class UpdateShift(BaseModel):
    mode: Optional[str] 
    turn_on: Optional[float]
    turn_off: Optional[float]
    Mon: Optional[bool]
    Tue: Optional[bool]
    Thu: Optional[bool]
    Wed: Optional[bool]
    Fri: Optional[bool]
    Sat: Optional[bool]
    Sun: Optional[bool]
    start: Optional[time]
    stop: Optional[time]
    updated_at: datetime = datetime.now()

class Shifts(ShiftBase):
    system_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    
        
class SystemBase(BaseModel):
    name: str
    location: str
        
class SystemCreate(SystemBase):
    owner: str
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()
    

class SystemUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    updated_at: datetime = datetime.now()
    
class System(SystemBase):
    id: int
    owner: str
    pumps: list[Pump] = []
    valves: list[Valve] = []
    sensors: list[Sensor]= []
    shifts: list[Shifts]= []
    
    class Config:
        orm_mode = True