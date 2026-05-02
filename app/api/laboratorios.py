from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.laboratorios import LaboratorioCreate, LaboratorioResponse
from app.crud import laboratorios as crud_laboratorios
from app.security.auth import get_current_user

# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/laboratorios",
    tags=["Laboratorios"] 
)

@router.post("/", response_model=LaboratorioResponse)
def crear_laboratorio(
    laboratorio: LaboratorioCreate,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user, scopes=["usuarios:gestionar"])
):
    return crud_laboratorios.create_laboratorio(db=db, laboratorio=laboratorio)

@router.get("/", response_model=List[LaboratorioResponse])
def listar_laboratorios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user)
):
    return crud_laboratorios.get_laboratorios(db, skip=skip, limit=limit)

@router.get("/{id_laboratorio}", response_model=LaboratorioResponse)
def obtener_laboratorio(
    id_laboratorio: int,
    db: Session = Depends(get_db),
    _usuario_actual: dict = Security(get_current_user)
):
    db_laboratorio = crud_laboratorios.get_laboratorio(db, id_laboratorio=id_laboratorio)
    if db_laboratorio is None:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return db_laboratorio