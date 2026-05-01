from pydantic import BaseModel, EmailStr
from typing import Optional

# Base: Atributos comunes
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr # Pydantic valida que sea un correo real
    rol: str
    activo: bool = True

# Para Crear: Requiere la contraseña en texto plano
class UsuarioCreate(UsuarioBase):
    password: str

# Para Devolver (Response), no incluye el password pero si el ID
class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True # Esto permite a Pydantic leer modelos de SQLAlchemy