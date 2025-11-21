from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

router = APIRouter(prefix='/services', tags=['services'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[schemas.Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_services(db, skip=skip, limit=limit)

@router.get('/{service_id}', response_model=schemas.Service)
def read_service(service_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_service(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Service not found')
    return db_obj

@router.post('/', response_model=schemas.Service, status_code=201)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, service)

@router.put('/{service_id}', response_model=schemas.Service)
def update_service(service_id: int, service: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    db_obj = crud.update_service(db, service_id, service)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Service not found')
    return db_obj

@router.delete('/{service_id}', response_model=schemas.Service)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_service(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Service not found')
    return db_obj
