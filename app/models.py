from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class Technician(Base):
    __tablename__ = 'technicians'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    specialties = Column(JSON, nullable=True)  # array of strings

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")

class Agenda(Base):
    __tablename__ = 'agendas'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="agendas")
    userName = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)
    date = Column(String(100), nullable=True)  # ISO datetime as string (can be changed to DateTime)
    observation = Column(Text, nullable=True)
    technician_id = Column(Integer, ForeignKey('technicians.id'), nullable=True)
    technician = relationship('Technician', backref='agendas')
    technicianObservation = Column(Text, nullable=True)
    status = Column(String(100), nullable=True)
    service = Column(String(200), nullable=True)
