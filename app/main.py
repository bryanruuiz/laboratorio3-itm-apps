from fastapi import FastAPI
from app.db import engine, Base

# Más adelante importaremos los modelos aquí para que SQLAlchemy los reconozca y cree las tablas
# from app.models import usuarios, laboratorios, servicios, tickets

app = FastAPI(
    title="API Mesa de Servicios - Laboratorios ITM",
    description="API para gestionar solicitudes de servicios en laboratorios con JWT y Scopes.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensaje": "API de Mesa de Servicios activa. Taller 3 en línea."}