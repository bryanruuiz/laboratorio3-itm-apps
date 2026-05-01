import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Configuraciones de JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 # El token durará 2 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Diccionario maestro de Scopes según el Rol (Basado en la Actividad 2 de la guía)
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
    
    # Crea el token firmado con la clave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt