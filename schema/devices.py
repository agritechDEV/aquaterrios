from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, Union, List


# Pump's schemas
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
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


# Valve's schemas
class ValveBase(BaseModel):
    valve_id: str
    status: Union[bool, None] = None


class AddValve(ValveBase):
    system_id: int


class UpdateValve(BaseModel):
    status: Optional[bool]
    updated_at: datetime = datetime.now()


class UpdateValveStatus(BaseModel):
    status: Optional[bool]
    updated_at: datetime = datetime.now()


class Valve(ValveBase):
    system_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# Sensor's schemas


class SensorBase(BaseModel):
    sensor_id: str
    readings: Optional[float] = 50
    set_lvl_1: bool = False
    set_lvl_2: bool = True
    set_lvl_3: bool = False


class AddSensor(SensorBase):
    system_id: int


class UpdateSensor(BaseModel):
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
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class SectionCreate(BaseModel):
    shift_id: int
    valve_id: str
    updated_at: datetime = datetime.now()


class Section(SectionCreate):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class SensorControler(BaseModel):
    section_id: int
    sensor_id: Optional[str]
    starts_at: Optional[float]
    stops_at: Optional[float]
    updated_at: datetime = datetime.now()


class SControl(BaseModel):
    id: int
    section_id: int
    sensor_id: Union[str, None] = None
    starts_at: Union[float, None] = None
    stops_at: Union[float, None] = None
    updated_at: datetime

    class Config:
        orm_mode = True


class TimerControl(BaseModel):
    shift_id: int
    day: Optional[str]
    starts: Optional[time]
    stops: Optional[time]
    updated_at: datetime = datetime.now()


class TControl(BaseModel):
    id: int
    shift_id: Union[int, None] = None
    day: Union[str, None] = None
    starts: Union[time, None] = None
    stops: Union[time, None] = None
    updated_at: datetime

    class Config:
        orm_mode = True


class ShiftBase(BaseModel):
    mode: Optional[str] = "TIMER"
    sensors_settings: Optional[str] = "N/A"


class AddShift(ShiftBase):
    system_id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UpdateShift(BaseModel):
    mode: Optional[str]
    sensors_settings: Optional[str]
    updated_at: datetime = datetime.now()


class Shifts(ShiftBase):
    id: int
    system_id: int
    created_at: datetime
    updated_at: datetime
    shifts_sections: List[Section] = []

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
    system_pumps: List[Pump] = []
    system_valves: List[Valve] = []
    system_sensors: List[Sensor] = []
    system_shifts: List[Shifts] = []

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
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class UpdateLog(BaseModel):
    disable: bool = True


class CurrentTime(BaseModel):
    current_time: datetime = datetime.now()

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
