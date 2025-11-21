from fastapi import FastAPI
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers import services, technicians, agendas, users
from .db_init import init_database
from app.database import Base, engine
from database import Base, engine
import models
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import uuid

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


# LLAMAR AL INICIO
create_default_admin()

print("Creando tablas si no existen...")
Base.metadata.create_all(bind=engine)

app = FastAPI(title='rental-services-python', redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agendas.router)
app.include_router(services.router)
app.include_router(technicians.router)
app.include_router(users.router)


# Initialize DB (creates tables)
@app.on_event('startup')
def startup_event():
    init_database()

@app.get('/ping')
def ping():
    return {'ping': 'pong'}
