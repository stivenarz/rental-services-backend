import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import User
from app.routers import services, technicians, agendas, users

# Crear tablas al iniciar
def init_database():
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)

def create_default_admin():
    db: Session = SessionLocal()

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("ADMIN_EMAIL o ADMIN_PASSWORD no configurados.")
        return

    admin = db.query(User).filter(User.email == admin_email).first()

    if not admin:
        print("Creando usuario admin por defecto...")
        new_admin = User(
            id=str(uuid.uuid4()),
            name="Admin",
            email=admin_email,
            password=admin_password,
            role="admin"
        )
        db.add(new_admin)
        db.commit()
    else:
        print("Admin ya existe.")

    db.close()

# FastAPI
app = FastAPI(title='rental-services-python', redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(agendas.router)
app.include_router(services.router)
app.include_router(technicians.router)
app.include_router(users.router)

# Evento startup
@app.on_event("startup")
def startup_event():
    init_database()
    create_default_admin()

@app.get('/ping')
def ping():
    return {'ping': 'pong'}
