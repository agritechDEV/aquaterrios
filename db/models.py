from sqlalchemy import Boolean, Column, Integer, String, Text, Time, ForeignKey, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from db.database import Base


class User(Base):
    __tablename__= "users"
    
    username = Column(String(50), primary_key=True, unique=True)
    email = Column(String(50), nullable=False,unique=True)
    hashed_password = Column(String(250))
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    address = Column(Text(), nullable=False)
    admin = Column(Boolean, nullable=False)
    premium = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    delisted = Column(Boolean, nullable=False)
    secret = Column(String(50),unique=True)
    
    systems = relationship("System", back_populates="system_owner")
    alerts = relationship("Notification", back_populates="notes")

class System(Base):
    __tablename__= "systems"
    
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(50), ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(100),nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    system_owner = relationship("User", back_populates="systems")
    system_pumps = relationship("Pump", back_populates="pumps")
    system_valves = relationship("Valve", back_populates="valves")
    system_sensors = relationship("Sensor", back_populates="sensors")
    system_shifts = relationship("Shift", back_populates="shifts")

class Pump(Base):
    __tablename__= "pumps"
    
    pump_id = Column(String(25), primary_key=True, unique=True)
    system_id = Column(Integer, ForeignKey("systems.id", ondelete="CASCADE"), nullable=False)
    capacity = Column(Float)
    available = Column(Float)
    current = Column(Float)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    pumps = relationship("System", back_populates="system_pumps")
    
class Valve(Base):
    __tablename__= "valves"
    
    valve_id = Column(String(25), primary_key=True, unique=True)
    system_id = Column(Integer, ForeignKey("systems.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(Integer)
    status = Column(Boolean)
    mode = Column(String(25), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    valves = relationship("System", back_populates="system_valves")
    
class Sensor(Base):
    __tablename__= "sensors"
    
    sensor_id = Column(String(25), primary_key=True, unique=True)
    system_id = Column(Integer, ForeignKey("systems.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(Integer)
    readings = Column(Float)
    set_lvl_1 = Column(Boolean, nullable=False)
    set_lvl_2 = Column(Boolean, nullable=False)
    set_lvl_3 = Column(Boolean, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    sensors = relationship("System", back_populates="system_sensors")
    
class Shift(Base):
    __tablename__= "shifts"
    
    id = Column(Integer, primary_key=True)
    system_id = Column(Integer, ForeignKey("systems.id", ondelete="CASCADE"), nullable=False)
    mode = Column(String(25), nullable=False)
    sensors_settings = Column(String(25))
    turn_on = Column(Float)
    turn_off = Column(Float)
    Mon = Column(Boolean)
    Tue = Column(Boolean)
    Wed = Column(Boolean)
    Thu = Column(Boolean)
    Fri = Column(Boolean)
    Sat = Column(Boolean)
    Sun = Column(Boolean)
    start = Column(Time)
    stop = Column(Time)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    shifts = relationship("System", back_populates="system_shifts")

class FlowData(Base):
    __tablename__= "flow_data"
    
    id = Column(Integer, primary_key=True)
    pump_id = Column(String(25), ForeignKey("pumps.pump_id"), nullable=False)
    flow_rate = Column(Float)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class SensorData(Base):
    __tablename__="sensor_data"
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String(25), ForeignKey("sensors.sensor_id"), nullable=False)
    level_1 = Column(Float)
    level_2 = Column(Float)
    level_3 = Column(Float)
    temperature = Column(Float)
    moisture = Column(Float)
    bat_level = Column(Float)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Logs(Base):
    __tablename__="logs"
    
    id = Column(Integer, primary_key=True)
    dev_id = Column(String(25))
    message = Column(Text)
    disable = Column(Boolean)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Notification(Base):
    __tablename__="notifications"
    
    id = Column(Integer, primary_key=True)
    user = Column(String(25), ForeignKey("users.username"), nullable=False)
    message = Column(Text)
    read = Column(Boolean)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    notes = relationship("User", back_populates="alerts")
    
class Subscription(Base):
    __tablename__="subscriptions"
    
    id = Column(Integer, primary_key=True)
    mail = Column(String(50), unique=True)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    