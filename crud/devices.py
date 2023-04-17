from sqlalchemy.orm import Session
import pandas as pd
import plotly.express as px

from db import models
from schema import devices
from db.database import engine

# Handle system
def get_systems(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.System).offset(skip).limit(limit).all()

def get_system(db: Session, system_id: int):
    return db.query(models.System).filter(models.System.id == system_id).first()

def create_system(db: Session, system: devices.SystemCreate):
    db_system = models.System(**system.dict())
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system

def update_system(db: Session, system: devices.SystemUpdate, system_id: int):
    system_query = db.query(models.System).filter(models.System.id == system_id)
    if not system_query.first():
        return False
    system_query.update(system.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_system(system_id: int, db: Session):
    existing_system = db.query(models.System).filter(models.System.id == system_id)
    if not existing_system.first():
        return False
    existing_system.delete(synchronize_session=False)
    db.commit()
    return True

# Handle pumps
def get_pumps(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Pump).offset(skip).limit(limit).all()

def get_pump(db: Session, pump_id: str):
    return db.query(models.Pump).filter(models.Pump.pump_id == pump_id).first()

def get_system_pumps(db: Session, system_id: int):
    return db.query(models.Pump).filter(models.Pump.system_id == system_id).all()

def create_pump(db: Session, pump: devices.AddPump):
    db_pump = models.Pump(**pump.dict())
    db.add(db_pump)
    db.commit()
    db.refresh(db_pump)
    return db_pump

def update_pump(db: Session, pump: devices.UpdatePump, pump_id: str):
    pump_query = db.query(models.Pump).filter(models.Pump.pump_id == pump_id)
    if not pump_query.first():
        return False
    pump_query.update(pump.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_pump(pump_id: str, db: Session):
    existing_pump = db.query(models.Pump).filter(models.Pump.pump_id == pump_id)
    if not existing_pump.first():
        return False
    existing_pump.delete(synchronize_session=False)
    db.commit()
    return True

# Handle Valves
def get_valves(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Valve).offset(skip).limit(limit).all()

def get_valve(db: Session, valve_id: str):
    return db.query(models.Valve).filter(models.Valve.valve_id == valve_id).first()

def get_valve_shift(db: Session, shift_id: int):
    return db.query(models.Valve).filter(models.Valve.shift_id == shift_id).all()

def get_system_valves(db: Session, system_id: int):
    return db.query(models.Valve).filter(models.Valve.system_id == system_id).all()

def create_valve(db: Session, valve: devices.AddValve):
    db_valve = models.Valve(**valve.dict())
    db.add(db_valve)
    db.commit()
    db.refresh(db_valve)
    return db_valve

def update_valve(db: Session, valve: devices.UpdateValve, valve_id: str):
    valve_query = db.query(models.Valve).filter(models.Valve.valve_id == valve_id)
    if not valve_query.first():
        return False
    valve_query.update(valve.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_valve(valve_id: str, db: Session):
    existing_valve = db.query(models.Valve).filter(models.Valve.valve_id == valve_id)
    if not existing_valve.first():
        return False
    existing_valve.delete(synchronize_session=False)
    db.commit()
    return True


# Handle sensors
def get_sensors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_sensor(db: Session, sensor_id: str):
    return db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()

def get_sensor_shift(db: Session, shift_id: int):
    return db.query(models.Sensor).filter(models.Sensor.shift_id == shift_id).all()

def get_system_sensors(db: Session, system_id: int):
    return db.query(models.Sensor).filter(models.Sensor.system_id == system_id).all()

def create_sensor(db: Session, sensor: devices.AddSensor):
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def update_sensor(db: Session, sensor: devices.UpdateSensor, sensor_id: str):
    sensor_query = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id)
    if not sensor_query.first():
        return False
    sensor_query.update(sensor.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_sensor(sensor_id: str, db: Session):
    existing_sensor = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id)
    if not existing_sensor.first():
        return False
    existing_sensor.delete(synchronize_session=False)
    db.commit()
    return True

# Handle shifts
def get_shifts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Shift).offset(skip).limit(limit).all()

def get_shift(db: Session, shift_id: int):
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()

def get_active_timer_shifts(day: str, db: Session):
    active_shifts = []
    if day.capitalize() == "Mon":
        shifts = db.query(models.Shift).filter(models.Shift.Mon == True).all()  
    elif day.capitalize() == "Tue":
        shifts = db.query(models.Shift).filter(models.Shift.Tue == True).all()
    elif day.capitalize() == "Wed":
        shifts = db.query(models.Shift).filter(models.Shift.Wed == True).all()
    elif day.capitalize() == "Thu":
        shifts = db.query(models.Shift).filter(models.Shift.Thu == True).all()
    elif day.capitalize() == "Fri":
        shifts = db.query(models.Shift).filter(models.Shift.Fri == True).all()
    elif day.capitalize() == "Sat":
        shifts = db.query(models.Shift).filter(models.Shift.Sat == True).all()
    elif day.capitalize() == "Sun":
        shifts = db.query(models.Shift).filter(models.Shift.Sun == True).all()
    for shift in shifts:
        active_shifts.append(shift.id)
    return active_shifts
   

def delete_shift(shift_id: int, db: Session):
    existing_shift = db.query(models.Shift).filter(models.Shift.id == shift_id)
    if not existing_shift.first():
        return False
    existing_shift.delete(synchronize_session=False)
    db.commit()
    return True

def create_sensor_shift(db: Session, sensor_shift: devices.AddSensorShift):
    db_s_shift = models.Shift(**sensor_shift.dict())
    db.add(db_s_shift)
    db.commit()
    db.refresh(db_s_shift)
    return db_s_shift

def create_timer_shift(db: Session, timer_shift: devices.AddTimerShift):
    db_t_shift = models.Shift(**timer_shift.dict())
    db.add(db_t_shift)
    db.commit()
    db.refresh(db_t_shift)
    return db_t_shift

def update_shift(db: Session, shift: devices.UpdateShift, shift_id: int):
    shift_query = db.query(models.Shift).filter(models.Shift.id == shift_id)
    if not shift_query.first():
        return False
    shift_query.update(shift.dict(), synchronize_session=False)
    db.commit()
    return True

# Handle logs
def get_logs(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Logs).offset(skip).limit(limit).all()

def get_dev_logs(db: Session, dev_id: str):
    return db.query(models.Logs).filter(models.Logs.dev_id == dev_id).all()

def get_log(db: Session, log_id: int):
    return db.query(models.Logs).filter(models.Logs.id == log_id).first()

def create_log(db: Session, log: devices.LogCreate):
    db_log = models.Logs(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update_log(db: Session, log: devices.UpdateLog, log_id: int):
    log_query = db.query(models.Logs).filter(models.Logs.id == log_id)
    if not log_query.first():
        return False
    log_query.update(log.dict(), synchronize_session=False)
    db.commit()
    return True

def delete_log(log_id: int, db: Session):
    existing_log = db.query(models.Logs).filter(models.Logs.id == log_id)
    if not existing_log.first():
        return False
    existing_log.delete(synchronize_session=False)
    db.commit()
    return True

# Handle flow data
def get_flow_data(db: Session, pump_id: str):
    return db.query(models.FlowData).order_by(models.FlowData.pump_id, models.FlowData.date.desc()).filter(
        models.FlowData.pump_id == pump_id).first()

def get_all_flow_data(db: Session, pump_id: str):
    return db.query(models.FlowData).filter(models.FlowData.pump_id == pump_id)

def create_flow_data(db: Session, flow: devices.AddFlowData):
    db_data = models.FlowData(**flow.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
    
def update_pump_data(db: Session, pump_id: str, current: float):
    query_pump = db.query(models.Pump).filter(models.Pump.pump_id == pump_id)
    if not query_pump.first():
        return False
    query_pump.update({models.Pump.current: current}, synchronize_session=False)
    db.commit()
    return True

# Handle sensor data
def get_sensor_data(db: Session, sensor_id: str):
    return db.query(models.SensorData).order_by(models.SensorData.sensor_id, models.SensorData.date.desc()).filter(
        models.SensorData.sensor_id == sensor_id).first()

def get_all_sensor_data(db: Session, sensor_id: str):
    return db.query(models.SensorData).filter(models.SensorData.sensor_id == sensor_id)

def create_sensor_data(db: Session, sensor: devices.AddSensorData):
    db_data = models.SensorData(**sensor.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def update_sensor_data(db: Session, sensor_id: str, readings: float):
    query_readings = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id)
    if not query_readings.first():
        return False
    query_readings.update({models.Sensor.readings: readings}, synchronize_session=False)
    db.commit()
    return True
    
""" Images and figures """
def create_flow_image(pump_id: str, db: Session):
    pump_data = get_all_flow_data(db=db, pump_id=pump_id)
    flow_df = pd.read_sql(sql=pump_data.statement, con=engine)
    fig = px.bar(flow_df, x="date", y="flow_rate", title="Daily Consumption")
    fig.write_image(f"static/images/flowimg/{pump_id}.png")

def show_flow_fig(id: str, db: Session):
    pump_data = get_all_flow_data(db=db, pump_id=id)
    flow_df = pd.read_sql(sql=pump_data.statement, con=engine)
    fig = px.bar(flow_df, x="date", y="flow_rate", title="Daily Consumption")
    return fig

def show_sensor_fig(id: str, db: Session):
    sensor_data = get_all_sensor_data(db=db, sensor_id=id)
    sensor_df = pd.read_sql(sql=sensor_data.statement, con=engine)
    fig = px.line(sensor_df, x="date", y=["level_1", "level_2", "level_3"], labels={
                     "value": "Moisture (%)",
                     "date": "Measurement date",
                     "variable": "Measurement"
                 }, title="Sensor Readings")
    return fig