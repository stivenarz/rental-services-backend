from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
import app.models as models
from app.database import SessionLocal

router = APIRouter(prefix='/technicians', tags=['technicians'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[schemas.Technician])
def read_techs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_technicians(db, skip=skip, limit=limit)

@router.get('/{tech_id}', response_model=schemas.Technician)
def read_tech(tech_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_technician(db, tech_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Technician not found')
    return db_obj

@router.post('/', response_model=schemas.Technician, status_code=201)
def create_tech(tech: schemas.TechnicianCreate, db: Session = Depends(get_db)):
    return crud.create_technician(db, tech)

@router.put('/{tech_id}', response_model=schemas.Technician)
def update_tech(tech_id: int, tech: schemas.TechnicianUpdate, db: Session = Depends(get_db)):
    db_obj = crud.update_technician(db, tech_id, tech)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Technician not found')
    return db_obj

@router.delete('/{tech_id}', response_model=schemas.Technician)
def delete_tech(tech_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_technician(db, tech_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Technician not found')
    return db_obj
