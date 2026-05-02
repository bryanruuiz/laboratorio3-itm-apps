from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.servicios import ServicioCreate, ServicioResponse
from app.crud import servicios as crud_servicios
from app.security.auth import get_current_user

router = APIRouter(prefix="/servicios", tags=["Servicios"])

@router.post("/", response_model=ServicioResponse)
def crear_servicio(
    servicio: ServicioCreate,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user, scopes=["usuarios:gestionar"])
):
    return crud_servicios.create_servicio(db=db, servicio=servicio)

@router.get("/", response_model=List[ServicioResponse])
def listar_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user)
):
    return crud_servicios.get_servicios(db, skip=skip, limit=limit)

@router.get("/{id_servicio}", response_model=ServicioResponse)
def obtener_servicio(
    id_servicio: int,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user)
):
    db_servicio = crud_servicios.get_servicio(db, id_servicio=id_servicio)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return db_servicio