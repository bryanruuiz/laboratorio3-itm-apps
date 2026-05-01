from pydantic import BaseModel
from typing import Optional

class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    activo: bool = True

class ServicioCreate(ServicioBase):
    pass

class ServicioResponse(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True