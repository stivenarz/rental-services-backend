from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

router = APIRouter(prefix='/users', tags=['users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get('/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_user(db, user_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='User not found')
    return db_obj

@router.post('/', response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.put('/{user_id}', response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_obj = crud.update_user(db, user_id, user)
    if not db_obj:
        raise HTTPException(status_code=404, detail='User not found')
    return db_obj

@router.delete('/{user_id}', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_user(db, user_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='User not found')
    return db_obj

@router.post("/login", response_model=schemas.UserPublic)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, credentials.email)

    if not user:
        raise HTTPException(status_code=404, detail="El email no está registrado")

    # Comparar contraseña (sin hashing por ahora)
    if user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return user
