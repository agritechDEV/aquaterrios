from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from db.database import get_db
from schema.devices import AddFlowData, AddSensorData, GetFlowData, SensorData, LogCreate, Logs, UpdateValveStatus, CurrentTime
from crud import devices


api_router = APIRouter()

""" Flow date routes """


@api_router.post("/flowdata")
def flow_data(flow: AddFlowData, db: Session = Depends(get_db)):
    try:
        db_flow = devices.create_flow_data(db=db, flow=flow)
        db_pump = devices.get_pump(db=db, pump_id=db_flow.pump_id)
        new_volume = db_pump.current - db_flow.flow_rate
        devices.update_pump_data(
            db=db, pump_id=db_flow.pump_id, current=new_volume)
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


@api_router.get("/lastflowdata/{pump_id}", response_model=GetFlowData)
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
        data = {"level_1": new_data.level_1,
                "level_2": new_data.level_2, "level_3": new_data.level_3}
        settings = {"level_1": sensor.set_lvl_1,
                    "level_2": sensor.set_lvl_2, "level_3": sensor.set_lvl_3}
        x = [1, 2, 3]
        user_setup = []
        user_setup = [f"level_{i}" for i in x if settings[f"level_{i}"]]
        y = len(user_setup)
        new_readings = 0
        for x in user_setup:
            new_readings += data[x]/y
        devices.update_sensor_data(
            db=db, sensor_id=new_data.sensor_id, readings=new_readings)
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


@api_router.get("/lastsensordata/{sensor_id}", response_model=SensorData)
def last_sensor_data(sensor_id: str, db: Session = Depends(get_db)):
    try:
        last_data = devices.get_sensor_data(db=db, sensor_id=sensor_id)
        if not last_data:
            return {"detail": "There is no available data"}
        return last_data
    except:
        return {"detail": "There is problems with database"}


""" Valve routes """


@api_router.get("/valvestatus/{system_id}")
def get_valve_status(system_id: int, db: Session = Depends(get_db)):
    try:
        valves = devices.get_system_valves(db=db, system_id=system_id)
        valve_status = []
        for valve in valves:
            valve_status.append({valve.valve_id: valve.status})
        return valve_status
    except:
        return {"detail": "There is problems with database"}


@api_router.patch("/valve/{valve_id}")
def change_valve_status(valve_id: str, valve: UpdateValveStatus, db: Session = Depends(get_db)):
    existing_valve = devices.get_valve(db=db, valve_id=valve_id)
    if not existing_valve:
        return {"detail": "Could not found valve in database"}
    try:
        devices.update_valve_status(db=db, valve=valve, valve_id=valve_id)
        return {"detail": "Successfully updated database"}
    except:
        return {"detail": "Something went wrong with database"}


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


@api_router.get("/system_shifts/{system_id}")
def get_systems_shifts(system_id: int, db: Session = Depends(get_db)):
    shifts = devices.get_system_shifts(db=db, system_id=system_id)
    system_shifts = []
    for shift in shifts:
        system_shifts.append({"shift ID": shift.id, "shift mode": shift.mode})
    return system_shifts


@api_router.get("/shift_setting/{shift_id}")
def get_shift_setting(shift_id: int, db: Session = Depends(get_db)):
    shift = devices.get_shift(db=db, shift_id=shift_id)
    if not shift:
        return {"detail": "Couldn't find shift in database."}
    shift_sections = devices.get_shift_sections(db=db, shift_id=shift_id)

    shift_api = {"ShiftID": shift.id, "Shift Mode": shift.mode}
    # if shift.mode == "SENSOR":
    section_data = shift_api["sensor_selections"] = []

    for section in shift_sections:
        sensor_settings = []
        controlers = devices.get_sensor_controlers(
            db=db, section_id=section.id)
        section_data.append(
            {
                "sectionID": section.id,
                "Valve": section.valve_id,
                "mode": shift.sensors_settings,
                "sensor_settings": sensor_settings})

        for sensor in controlers:
            if sensor.section_id == section.id:
                sensor_settings.append(
                    {"sensor": sensor.sensor_id, "starts": sensor.starts_at, "stops": sensor.stops_at})
    # else:
    timer_data = shift_api["timer_selections"] = []
    for section in shift_sections:
        timer_settings = []
        controlers = devices.get_timer_controlers(db=db, shift_id=shift_id)
        timer_data.append(
            {
                "sectionID": section.id,
                "Valve": section.valve_id,
                "timer_settings": timer_settings
            }
        )
        days = []
        starts = []
        stops = []
        for timer in controlers:
            if timer.shift_id == section.shift_id:
                if timer.day not in days:
                    days.append(timer.day)
                if timer.starts not in starts:
                    starts.append(timer.starts)
                if timer.stops not in stops:
                    stops.append(timer.stops)

        timer_settings.append(
            {
                "Days": days,
                "Starts": starts,
                "Stops": stops
            }
        )

    return shift_api


""" Get current time """


@api_router.get("/timestamp", response_model=CurrentTime)
def return_current_time():
    return datetime.now().timestamp()
