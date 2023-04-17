from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, Union


#Pump's schemas    
class Flow(BaseModel):
    pump_id: str
    capacity: Union[float, None] = None
    available: Union[float, None] = None
    current: Union[float, None] = None
    

class AddPump(Flow):
    system_id: int

class UpdatePump(BaseModel):
    current: float
    updated_at: datetime = datetime.now()
    

class Pump(Flow):
    system_id: int
    updated_at: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class AddFlowData(BaseModel):
    pump_id: str
    flow_rate: float

class GetFlowData(BaseModel):
    flow_rate: float
    date: datetime
    
    class Config:
        orm_mode = True
    

#Valve's schemas
class ValveBase(BaseModel):
    valve_id: str
    status: Union[bool, None] = None
    mode: str 
    shift_id: Union[int, None] = None
    
class AddValve(ValveBase):
    system_id: int

class UpdateValve(BaseModel):
    status: Optional[bool]
    mode: Optional[str]
    shift_id: Optional[int]
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
    readings: Optional[float] = 50
    set_lvl_1: bool = False
    set_lvl_2: bool = True
    set_lvl_3: bool = False
    shift_id: int | None = None
    
    
class AddSensor(SensorBase):
    system_id: int

class UpdateSensor(BaseModel):
    shift_id: Optional[int]
    set_lvl_1: Optional[bool]
    set_lvl_2: Optional[bool]
    set_lvl_3: Optional[bool]
    updated_at: datetime = datetime.now()


class Sensor(SensorBase):
    system_id: int
    updated_at: datetime
    created_at: datetime
    
    class Config:
        orm_mode = True


class AddSensorData(BaseModel):
    sensor_id: str
    bat_level: float
    level_1: float
    level_2: float
    level_3: float
    temperature: float
    moisture: float


class SensorData(BaseModel):
    date: datetime
    bat_level: float
    level_1: float
    level_2: float
    level_3: float
    temperature: float
    moisture: float
    
    class Config:
        orm_mode = True   
        

class ShiftSensorBase(BaseModel):
    mode: str = "SENSOR"
    sensors_settings: str = "AVG"
    turn_on: float = 45
    turn_off: float = 65
    
class ShiftTimerBase(BaseModel):
    mode: str = "TIMER"
    sensors_settings: str = "N/A"
    Mon: bool = True
    Tue: bool = False
    Wed: bool = True
    Thu: bool = False
    Fri: bool = True
    Sat: bool = False
    Sun: bool = True
    start: time = "12:00:00"
    stop: time = "13:30:00"

class AddSensorShift(ShiftSensorBase):
    system_id: int

class AddTimerShift(ShiftTimerBase):
    system_id: int
    
class UpdateShift(BaseModel):
    mode: Optional[str] 
    sensors_settings: Optional[str]
    turn_on: Optional[float]
    turn_off: Optional[float]
    Mon: Optional[bool]
    Tue: Optional[bool]
    Wed: Optional[bool]
    Thu: Optional[bool]
    Fri: Optional[bool]
    Sat: Optional[bool]
    Sun: Optional[bool]
    start: Optional[time] 
    stop: Optional[time]
    updated_at: datetime = datetime.now()

class Shifts(BaseModel):
    id: int
    system_id: int
    mode: str 
    sensors_settings: Union[str, None] = None
    turn_on: Union[float, None] = None
    turn_off: Union[float, None] = None
    Mon: Union[bool, None] = None
    Tue: Union[bool, None] = None
    Wed: Union[bool, None] = None
    Thu: Union[bool, None] = None
    Fri: Union[bool, None] = None
    Sat: Union[bool, None] = None
    Sun: Union[bool, None] = None
    start: Union[time, None] = None
    stop: Union[time, None] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
    
        
class SystemBase(BaseModel):
    name: str
    location: str
        
class SystemCreate(SystemBase):
    owner: str
    
class SystemUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    updated_at: datetime = datetime.now()
    
class System(SystemBase):
    id: int
    owner: str
    created_at: datetime
    updated_at: datetime
    system_pumps: list[Pump] = []
    system_valves: list[Valve] = []
    system_sensors: list[Sensor]= []
    system_shifts: list[Shifts]= []
 
    class Config:
        orm_mode = True
        
class LogCreate(BaseModel):
    dev_id: str 
    message: str
    disable: bool = False
    
class Logs(LogCreate):
    date: datetime
    
    class Config:
        orm_mode = True
        
class UpdateLog(BaseModel):
    disable: bool = True