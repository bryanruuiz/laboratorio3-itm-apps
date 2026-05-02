from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.crud.usuarios import get_usuario_by_correo
from app.security.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, ROLES_SCOPES
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscar al usuario por correo (form_data.username mapea al correo)
    usuario = get_usuario_by_correo(db, correo=form_data.username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Verificar que la contraseña coincida
    if not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Verificar si el usuario está activo
    if not usuario.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # 4. Construir el Token JWT
    rol_usuario = usuario.rol.value if hasattr(usuario.rol, "value") else usuario.rol
    if rol_usuario not in ROLES_SCOPES:
        raise HTTPException(status_code=403, detail="El usuario tiene un rol invalido. Contacta al administrador.")

    scopes_del_rol = ROLES_SCOPES.get(rol_usuario, [])
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={
            "sub": usuario.correo,
            "id_usuario": usuario.id_usuario,
            "rol": rol_usuario,
            "scopes": scopes_del_rol # ¡Aquí inyectamos los scopes de la tabla!
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}