from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class RolUsuario(str, Enum):
    solicitante = "solicitante"
    responsable_tecnico = "responsable_tecnico"
    auxiliar = "auxiliar"
    tecnico_especializado = "tecnico_especializado"
    admin = "admin"

# Base: Atributos comunes
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr # Pydantic valida que sea un correo real
    activo: bool = True

# Para Crear: Requiere la contraseña en texto plano
class UsuarioCreate(UsuarioBase):
    rol: RolUsuario
    password: str = Field(min_length=8, max_length=128)

# Para Devolver (Response), no incluye el password pero si el ID
class UsuarioResponse(UsuarioBase):
    id_usuario: int
    # Se deja como str para no romper el listado con datos legacy en BD.
    rol: str

    class Config:
        from_attributes = True # Esto permite a Pydantic leer modelos de SQLAlchemy