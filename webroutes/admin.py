from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import plotly



from schema.users import User
from crud import devices
from crud.login import get_current_user
from crud.users import  get_users, alerts, get_subscribers
from db.database import get_db



web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@web_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@web_router.get("/reset", response_class=HTMLResponse)
def reset_password(request: Request):
    return templates.TemplateResponse("reset.html", {"request": request})

@web_router.get("/get_key", response_class=HTMLResponse)
def reset_password(request: Request):
    return templates.TemplateResponse("get_key.html", {"request": request})
        

@web_router.get("/profile", response_model=User)
def current_user(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user, "alerts": alerts, "users": users})


@web_router.get("/flow/{id}")
def get_flow_figures(id: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    data = devices.show_flow_fig(id=id, db=db)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return templates.TemplateResponse("fig.html", {"request": request, "graphJSON": graphJSON, "current_user": user, 
                                                   "alerts": alerts, "users": users})

@web_router.get("/sensor/{id}")
def get_flow_figures(id: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    data = devices.show_sensor_fig(id=id, db=db)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return templates.TemplateResponse("fig.html", {"request": request, "graphJSON": graphJSON, "current_user": user,
                                                   "alerts": alerts, "users": users})

@web_router.get("/systems") 
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}  
    systems = devices.get_systems(db=db)
    return templates.TemplateResponse("systems.html", {"request": request, "systems": systems, "current_user": current_user,
                                "users": users})
    
@web_router.get("/pumps") 
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}  
    systems = devices.get_systems(db=db)
    pumps = devices.get_pumps(db=db)
    return templates.TemplateResponse("pumps.html", {"request": request, "systems": systems, "pumps": pumps, "current_user": current_user,
                                "users": users})

@web_router.get("/valves") 
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}  
    systems = devices.get_systems(db=db)
    valve_mode_options = ["SENSOR", "TIMER"]
    valves = devices.get_valves(db=db)
    return templates.TemplateResponse("valves.html", {"request": request, "systems": systems, "modes": valve_mode_options, 
                                "valves": valves, "current_user": current_user, "users": users})

@web_router.get("/sensors") 
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}  
    systems = devices.get_systems(db=db)
    sensors = devices.get_sensors(db=db)
    return templates.TemplateResponse("sensors.html", {"request": request, "systems": systems,"sensors": sensors, 
                                    "current_user": current_user, "users": users})

@web_router.get("/logs") 
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}  
    logs = devices.get_logs(db=db)
    notifications = alerts(db=db)
    subsctiptions = get_subscribers(db=db)
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs, "alerts": notifications, 
                                                "subscriptions": subsctiptions, "current_user": current_user, "users": users})

@web_router.get("/system/{id}")
def system(id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    pump_logs = []
    valve_logs = []
    sensor_logs = []
    red_sensors = []
    green_sensors = []
    blue_sensors = []
    sensor_data = []
    active_days = []
    valve_mode_options = ["SENSOR", "TIMER"]
    if not current_user:
        return {"detail": "You are not logged in"}
    system = devices.get_system(db=db, system_id=id)
    for sensor in system.system_sensors:
        if sensor.readings < 50:
            red_sensors.append(sensor)
        elif sensor.readings > 50 and sensor.readings < 80:
            green_sensors.append(sensor)
        else:
            blue_sensors.append(sensor)
    if current_user.username != system.owner and not current_user.admin:
        return {"detail": "You are not authorized"}
    for pump in system.system_pumps:
        pump_logs = devices.get_dev_logs(db=db, dev_id=pump.pump_id)
    for valve in system.system_valves:
        valve_logs = devices.get_dev_logs(db=db, dev_id=valve.valve_id)
    for sensor in system.system_sensors:
        sensor_logs = devices.get_dev_logs(db=db, dev_id=sensor.sensor_id)
    for sensor in system.system_sensors:
        data = devices.get_sensor_data(db=db,sensor_id=sensor.sensor_id)
        sensor_data.append(data)
    for shift in system.system_shifts:
        if shift.mode == "TIMER":
            if shift.Mon:
                active_days.append("Mon")
            if shift.Tue:
                active_days.append("Tue")
            if shift.Wed:
                active_days.append("Wed")
            if shift.Thu:
                active_days.append("Thu")
            if shift.Fri:
                active_days.append("Fri")
            if shift.Sat:
                active_days.append("Sat")
            if shift.Sun:
                active_days.append("Sun")
    return templates.TemplateResponse("system.html", {"request": request, "system": system, "pump_logs": pump_logs, 
                    "valve_logs": valve_logs, "sensor_logs": sensor_logs, "current_user": current_user, "alerts": alerts,
                    "red_sensors": red_sensors, "green_sensors": green_sensors, "blue_sensors": blue_sensors, "sensor_data": sensor_data,
                    "active_days": active_days, "users": users, "options": valve_mode_options})
    