from fastapi import FastAPI
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers import services, technicians, agendas, users

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
def on_startup():
    init_db()

@app.get('/ping')
def ping():
    return {'ping': 'pong'}
