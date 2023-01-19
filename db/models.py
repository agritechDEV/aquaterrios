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
    delisted = Column(Boolean, nullable=False, server_default='FALSE')
    
    systems = relationship("System", back_populates="system_owner")