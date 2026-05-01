from pydantic import BaseModel
from typing import Optional

class LaboratorioBase(BaseModel):
    nombre: str
    ubicacion: str
    activo: bool = True

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioResponse(LaboratorioBase):
    id_laboratorio: int

    class Config:
        from_attributes = True