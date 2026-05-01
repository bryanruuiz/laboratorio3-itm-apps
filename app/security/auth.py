import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ROLES_SCOPES = {
    "solicitante": ["tickets:crear", "tickets:ver_propios"],
    "responsable_tecnico": ["tickets:ver_propios", "tickets:recibir", "tickets:asignar", "tickets:finalizar"],
    "auxiliar": ["tickets:ver_propios", "tickets:atender"],
    "tecnico_especializado": ["tickets:ver_propios", "tickets:atender"],
    "admin": [
        "tickets:crear", "tickets:ver_propios", "tickets:recibir", 
        "tickets:asignar", "tickets:atender", "tickets:finalizar", 
        "tickets:ver_todos", "usuarios:gestionar"
    ]
}

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- EL GUARDIÁN DE SEGURIDAD Y LOS SCOPES ---

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "tickets:crear": "Crear nuevos tickets",
        "tickets:ver_propios": "Ver los tickets propios",
        "tickets:recibir": "Cambiar estado a recibido",
        "tickets:asignar": "Asignar ticket a tecnico",
        "tickets:atender": "Atender ticket (en proceso/revision)",
        "tickets:finalizar": "Finalizar ticket",
        "tickets:ver_todos": "Ver todos los tickets",
        "usuarios:gestionar": "Gestionar usuarios"
    }
)

def get_current_user(security_scopes: SecurityScopes, token: str = Security(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
    except JWTError:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado. Requiere el scope: {scope}",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return payload