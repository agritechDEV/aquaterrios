from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schema.devices import AddFlowData, AddSensorData, GetFlowData, SensorData, LogCreate, Logs
from crud import devices


api_router = APIRouter()

""" Flow date routes """
@api_router.post("/flowdata")
def flow_data(flow: AddFlowData, db: Session = Depends(get_db)):
    try:
        db_flow = devices.create_flow_data(db=db, flow=flow)
        db_pump = devices.get_pump(db=db, pump_id=db_flow.pump_id)
        new_volume = db_pump.current - db_flow.flow_rate
        devices.update_pump_data(db=db, pump_id=db_flow.pump_id, current=new_volume)
        devices.create_flow_image(db=db, pump_id=db_pump.pump_id)
        return {"detail": "Successfully updated pump volume"}
    except:
        return {"detail": "Couldn't find pump in database"}


@api_router.get("/flowdata/{pump_id}", response_model=List[GetFlowData])
def all_flow_data(pump_id: str, db: Session = Depends(get_db)):
    try:
        db_data = devices.get_all_flow_data(db=db, pump_id=pump_id)
        if not db_data:
            return {"detail": "There is no available data"}
        return db_data.all()
    except:
        return {"detail": "There is problems with database"}

@api_router.get("/lastflowdata/{pump_id}")
def last_flow_data(pump_id: str, db: Session = Depends(get_db)):
    try:
        last_data = devices.get_flow_data(db=db, pump_id=pump_id)
        if not last_data:
            return {"detail": "There is no available data"}
        return last_data
    except:
        return {"detail": "There is problems with database"}

""" Sensor data routes """
@api_router.post("/sensordata")
def sensor_data(sensor_data: AddSensorData, db: Session = Depends(get_db)):
    try:
        new_data = devices.create_sensor_data(db=db, sensor=sensor_data)
        sensor = devices.get_sensor(db=db, sensor_id=new_data.sensor_id)
        data = {"level_1": new_data.level_1, "level_2": new_data.level_2, "level_3": new_data.level_3}
        settings = {"level_1": sensor.set_lvl_1, "level_2": sensor.set_lvl_2, "level_3": sensor.set_lvl_3}
        x = [1,2,3]
        user_setup = []
        user_setup = [f"level_{i}" for i in x if settings[f"level_{i}"]]
        y = len(user_setup)
        new_readings = 0
        for x in user_setup:
            new_readings += data[x]/y
        devices.update_sensor_data(db=db, sensor_id=new_data.sensor_id, readings=new_readings)
        return {"detail": "Successfully updated sensor readings"}
    except:
        return {"detail": "Couldn't find sensor in database"}


@api_router.get("/sensordata/{sensor_id}", response_model=List[SensorData])
def all_sensor_data(sensor_id: str, db: Session = Depends(get_db)):
    try:
        db_data = devices.get_all_sensor_data(db=db, sensor_id=sensor_id)
        if not db_data:
            return {"detail": "There is no available data"}
        return db_data.all()
    except:
        return {"detail": "There is problems with database"}

@api_router.get("/lastsensordata/{sensor_id}")
def last_sensor_data(sensor_id: str, db: Session = Depends(get_db)):
    try:
        last_data = devices.get_sensor_data(db=db, sensor_id=sensor_id)
        if not last_data:
            return {"detail": "There is no available data"}
        return last_data
    except:
        return {"detail": "There is problems with database"}

""" Logs of devices events """
@api_router.post("/log/{id}")
def create_log(log: LogCreate, id: str, db: Session = Depends(get_db)):
    pump = devices.get_pump(db=db, pump_id=id)
    valve = devices.get_valve(db=db, valve_id=id)
    sensor = devices.get_sensor(db=db, sensor_id=id)
    if not pump and not valve and not sensor:
        return {"detail": "Couldn't find device in database. Check if input is valid!"}
    else:
        devices.create_log(db=db, log=log)
        return {"detail": "Successfully updated log"}

@api_router.get("/systemlogs", response_model=List[List[Logs]])
def get_system_logs(system_id: int, db: Session = Depends(get_db)):
  
    pumps = devices.get_system_pumps(db=db, system_id=system_id)
    valves = devices.get_system_valves(db=db, system_id=system_id)
    sensors = devices.get_system_sensors(db=db, system_id=system_id)
    for pump in pumps:
        pump_logs = devices.get_dev_logs(db=db, dev_id=pump.pump_id)
    for valve in valves:
        valve_logs = devices.get_dev_logs(db=db, dev_id=valve.valve_id)
    for sensor in sensors:
        sensor_logs = devices.get_dev_logs(db=db, dev_id=sensor.sensor_id)
    return [pump_logs, valve_logs, sensor_logs]

""" API routes for getting setting """
@api_router.get("/shift_setting/{shift_id}")
def get_shift_setting(shift_id: int, db: Session = Depends(get_db)):
    shift = devices.get_shift(db=db, shift_id=shift_id)
    if not shift:
        return {"detail": "There is no available data"}
    if shift.mode == "SENSOR":
        settings = shift.sensors_settings
        shift_sensors = []
        shift_valves = []
        shift_settings = {"START": shift.turn_on, "STOP": shift.turn_off}
        sensors = devices.get_sensor_shift(db=db, shift_id=shift_id)
        valves = devices.get_valve_shift(db=db, shift_id=shift_id)
        for sensor in sensors:
             shift_sensors.append(sensor.sensor_id)
        for valve in valves:
            shift_valves.append(valve.valve_id)
    if shift.mode == "TIMER":
        shift_sensors = None
        shift_valves = []
        settings = []
        shift_settings = {"START": shift.start, "STOP": shift.stop }
        if shift.Mon:
            settings.append("Mon")
        if shift.Tue:
            settings.append("Tue")
        if shift.Wed:
            settings.append("Wed")
        if shift.Thu:
            settings.append("Thu")
        if shift.Fri:
            settings.append("Fri")
        if shift.Sat:
            settings.append("Sat")
        if shift.Sun:
            settings.append("Sun")
        valves = devices.get_valve_shift(db=db, shift_id=shift_id)
        for valve in valves:
            shift_valves.append(valve.valve_id)
    return {"Mode": shift.mode, "Setting": settings, "Limits": shift_settings, "Shift Sensors": shift_sensors,
            "Shift Valves": shift_valves}


@api_router.get("/timershift/{day}")
def get_timer_shift(day: str, db: Session = Depends(get_db)):
    try:
        active_valves = []
        shift_timers = []
        active_shifts = devices.get_active_timer_shifts(day=day, db=db)
        if not active_shifts:
            return {"detail": "No data abailable"}
        for num in active_shifts:
            valves = devices.get_valve_shift(db=db, shift_id=num)
            for valve in valves:
                active_valves.append({f"Shift {num}": valve.valve_id})
        for num in active_shifts:
            shift = devices.get_shift(db=db, shift_id=num)
            timer = {"START": shift.start, "STOP": shift.stop}
            shift_timers.append({f"Shift {num}": timer})
        return {"Active Shifts": active_shifts, "Active Valves": active_valves, "Timers": shift_timers}
    except:
        return {"detail": "Incorrect entry. Please enter English three letter abrrv of the days."}


