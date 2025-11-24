from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from fastapi import HTTPException
from sqlalchemy import func

# Services
def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_obj = models.Service(icon=service.icon, title=service.title, description=service.description)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_service(db: Session, service_id: int, service: schemas.ServiceUpdate):
    db_obj = get_service(db, service_id)
    if not db_obj:
        return None
    for field, value in service.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_service(db: Session, service_id: int):
    db_obj = get_service(db, service_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# Technicians
def get_technicians(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Technician).offset(skip).limit(limit).all()

def get_technician(db: Session, tech_id: int):
    return db.query(models.Technician).filter(models.Technician.id == tech_id).first()

def create_technician(db: Session, tech: schemas.TechnicianCreate):
    db_obj = models.Technician(name=tech.name, phone=tech.phone, email=tech.email, specialties=tech.specialties)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_technician(db: Session, tech_id: int, tech: schemas.TechnicianUpdate):
    db_obj = get_technician(db, tech_id)
    if not db_obj:
        return None
    for field, value in tech.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_technician(db: Session, tech_id: int):
    db_obj = get_technician(db, tech_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# Users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_obj = models.User(name=user.name, email=user.email, phone=user.phone, address=user.address, password=user.password, role=user.role )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_obj = get_user(db, user_id)
    if not db_obj:
        return None
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_user(db: Session, user_id: int):
    db_obj = get_user(db, user_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# Agendas
def get_agendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Agenda).offset(skip).limit(limit).all()

def get_agenda(db: Session, agenda_id: int):
    return db.query(models.Agenda).filter(models.Agenda.id == agenda_id).first()

# CREAR AGENDA BUSCANDO TÉCNICOS DISPONIBLES POR FECHA
def create_agenda(db: Session, agenda: schemas.AgendaCreate):

    # 1. Obtener técnicos cuya especialidad coincida
    technicians = db.query(models.Technician).filter(
        models.Technician.specialties.contains([agenda.service])
    ).all()

    if not technicians:
        raise HTTPException(status_code=404, detail="No hay técnicos con esa especialidad.")

    # 2. Buscar técnicos con disponibilidad (máx 2 agenda por fecha)
    available_technician = None

    for tech in technicians:
        agendas_count = db.query(models.Agenda).filter(
            models.Agenda.technician_id == tech.id,
            models.Agenda.date == agenda.date
        ).count()

        if agendas_count <= 1:
            available_technician = tech
            break

    if not available_technician:
        raise HTTPException(status_code=409, detail="No hay técnicos disponibles para esa fecha.")

    # 3. Crear agenda asignando el técnico encontrado
    db_obj = models.Agenda(
        userId=agenda.userId,
        userName=agenda.userName,
        email=agenda.email,
        phone=agenda.phone,
        address=agenda.address,
        date=agenda.date,
        observation=agenda.observation,
        technician_id=available_technician.id,
        technicianObservation='',
        status='Pendiente',
        service=agenda.service
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def update_agenda(db: Session, agenda_id: int, agenda: schemas.AgendaUpdate):
    db_obj = get_agenda(db, agenda_id)
    if not db_obj:
        return None
    for field, value in agenda.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_agenda(db: Session, agenda_id: int):
    db_obj = get_agenda(db, agenda_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
