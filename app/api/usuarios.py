from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse, RolUsuario
from app.crud import usuarios as crud_usuarios
from app.security.auth import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/bootstrap-admin", response_model=UsuarioResponse)
def bootstrap_admin(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if crud_usuarios.count_usuarios(db) > 0:
        raise HTTPException(status_code=403, detail="El bootstrap inicial ya fue ejecutado.")

    if usuario.rol != RolUsuario.admin:
        raise HTTPException(status_code=422, detail="El primer usuario debe ser de rol admin.")

    db_user = crud_usuarios.get_usuario_by_correo(db, correo=usuario.correo)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    return crud_usuarios.create_usuario(db=db, usuario=usuario)

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["usuarios:gestionar"])
):
    db_user = crud_usuarios.get_usuario_by_correo(db, correo=usuario.correo)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return crud_usuarios.create_usuario(db=db, usuario=usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["usuarios:gestionar"])
):
    return crud_usuarios.get_usuarios(db, skip=skip, limit=limit)

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(
    id_usuario: int, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["usuarios:gestionar"]) 
):
    db_usuario = crud_usuarios.get_usuario(db, id_usuario=id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario