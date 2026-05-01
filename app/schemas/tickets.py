from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    # Solo pedimos estos dos, el id_solicitante se sacará del Token JWT por seguridad
    id_laboratorio: int
    id_servicio: int

# Para Crear: El usuario solo envía los datos básicos
class TicketCreate(TicketBase):
    pass

# Para Actualizar Estado (usado en el PATCH del Taller)
class TicketUpdateEstado(BaseModel):
    estado: str
    id_asignado: Optional[int] = None
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None

# Para Devolver: Incluye todo lo generado por el sistema (IDs y Fechas)
class TicketResponse(TicketBase):
    id_ticket: int
    id_solicitante: int
    id_responsable: Optional[int] = None
    id_asignado: Optional[int] = None
    estado: str
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    fecha_finalizacion: Optional[datetime] = None

    class Config:
        from_attributes = True