from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ServiceBase(BaseModel):
    icon: Optional[str] = None
    title: str
    description: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    class Config:
        orm_mode = True

class TechnicianBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialties: Optional[List[str]] = []

class TechnicianCreate(TechnicianBase):
    pass

class TechnicianUpdate(TechnicianBase):
    pass

class Technician(TechnicianBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = 'user'

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class AgendaBase(BaseModel):
    userId: int
    userName: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date: Optional[str] = None
    observation: Optional[str] = None
    technician_id: Optional[int] = None
    technicianObservation: Optional[str] = None
    status: Optional[str] = None
    service: Optional[str] = None

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(AgendaBase):
    pass

class Agenda(AgendaBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: str
    password: str

class UserPublic(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    email: str
    role: str | None = None

    class Config:
        orm_mode = True
