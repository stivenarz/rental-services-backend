from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

# router = APIRouter()
router = APIRouter(prefix='/agendas', tags=['agendas'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[schemas.Agenda])
def read_agendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_agendas(db, skip=skip, limit=limit)

@router.get('/{agenda_id}', response_model=schemas.Agenda)
def read_agenda(agenda_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_agenda(db, agenda_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Agenda not found')
    return db_obj

@router.post('/', response_model=schemas.Agenda, status_code=201)
def create_agenda(agenda: schemas.AgendaCreate, db: Session = Depends(get_db)):
    return crud.create_agenda(db, agenda)

@router.put('/{agenda_id}', response_model=schemas.Agenda)
def update_agenda(agenda_id: int, agenda: schemas.AgendaUpdate, db: Session = Depends(get_db)):
    db_obj = crud.update_agenda(db, agenda_id, agenda)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Agenda not found')
    return db_obj

@router.delete('/{agenda_id}', response_model=schemas.Agenda)
def delete_agenda(agenda_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_agenda(db, agenda_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Agenda not found')
    return db_obj
