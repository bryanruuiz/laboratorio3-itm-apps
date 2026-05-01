from fastapi import FastAPI
from app.db import engine, Base
from app.models.usuarios import Usuario
from app.models.laboratorios import Laboratorio
from app.models.servicios import Servicio
from app.models.tickets import Ticket

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Mesa de Servicios - Laboratorios ITM",
    description="API para gestionar solicitudes de servicios en laboratorios con JWT y Scopes.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensaje": "API de Mesa de Servicios activa. Tablas sincronizadas."}