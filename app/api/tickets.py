from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.tickets import TicketCreate, TicketResponse, TicketUpdateEstado
from app.crud import tickets as crud_tickets
from app.crud import usuarios as crud_usuarios
from app.security.auth import get_current_user

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def puede_ver_ticket(usuario_actual: dict, ticket) -> bool:
    rol = usuario_actual["rol"]
    mi_id = usuario_actual["id_usuario"]
    mis_scopes = usuario_actual.get("scopes", [])

    if rol == "admin":
        return "tickets:ver_todos" in mis_scopes
    if rol == "solicitante":
        return ticket.id_solicitante == mi_id

    return (
        ticket.id_solicitante == mi_id
        or ticket.id_responsable == mi_id
        or ticket.id_asignado == mi_id
    )

@router.post("/", response_model=TicketResponse)
def crear_ticket(
    ticket: TicketCreate, 
    db: Session = Depends(get_db),
    # Bloqueado: Solo quien tenga "tickets:crear" puede entrar
    usuario_actual: dict = Security(get_current_user, scopes=["tickets:crear"]) 
):
    # Ya no simulamos. Sacamos el ID real de quien inició sesión
    id_usuario_real = usuario_actual["id_usuario"] 
    return crud_tickets.create_ticket(db=db, ticket=ticket, id_solicitante=id_usuario_real)

@router.get("/", response_model=List[TicketResponse])
def listar_tickets(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["tickets:ver_propios"])
):
    todos_los_tickets = crud_tickets.get_tickets(db, skip=skip, limit=limit)
    rol = usuario_actual["rol"]

    # Filtro de visibilidad exigido por la guía
    if rol == "admin":
        if "tickets:ver_todos" not in usuario_actual.get("scopes", []):
            raise HTTPException(status_code=403, detail="No tienes permisos para ver todos los tickets.")
        return todos_los_tickets

    return [t for t in todos_los_tickets if puede_ver_ticket(usuario_actual, t)]

@router.get("/{id_ticket}", response_model=TicketResponse)
def obtener_ticket(
    id_ticket: int, db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["tickets:ver_propios"])
):
    db_ticket = crud_tickets.get_ticket(db, id_ticket=id_ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if not puede_ver_ticket(usuario_actual, db_ticket):
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este ticket.")

    return db_ticket

@router.patch("/{id_ticket}/estado", response_model=TicketResponse)
def actualizar_estado(
    id_ticket: int, 
    actualizacion: TicketUpdateEstado, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Security(get_current_user, scopes=["tickets:ver_propios"])
):
    db_ticket = crud_tickets.get_ticket(db, id_ticket=id_ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
    estado_actual = db_ticket.estado
    nuevo_estado = actualizacion.estado.value if hasattr(actualizacion.estado, "value") else actualizacion.estado
    mi_id = usuario_actual["id_usuario"]
    mis_scopes = usuario_actual.get("scopes", [])
    mi_rol = usuario_actual["rol"]

    # LA MÁQUINA DE ESTADOS
    
    
    if estado_actual == "solicitado" and nuevo_estado == "recibido":
        if "tickets:recibir" not in mis_scopes or mi_rol not in ["responsable_tecnico", "admin"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para recibir tickets.")
        # Al recibirlo, el usuario actual se convierte automáticamente en el responsable
        return crud_tickets.update_estado(db, id_ticket, actualizacion, id_responsable=mi_id)

    elif estado_actual == "recibido" and nuevo_estado == "asignado":
        if "tickets:asignar" not in mis_scopes or mi_rol not in ["responsable_tecnico", "admin"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para asignar tickets.")

        if mi_rol != "admin" and db_ticket.id_responsable != mi_id:
            raise HTTPException(status_code=403, detail="Solo el responsable del ticket puede asignarlo.")

        if not actualizacion.id_asignado:
            raise HTTPException(status_code=422, detail="Para pasar a estado 'asignado', debes enviar el id_asignado.")

        usuario_asignado = crud_usuarios.get_usuario(db, id_usuario=actualizacion.id_asignado)
        if not usuario_asignado:
            raise HTTPException(status_code=422, detail="El id_asignado no corresponde a un usuario valido.")
        if not usuario_asignado.activo:
            raise HTTPException(status_code=422, detail="El usuario asignado esta inactivo.")
        if usuario_asignado.rol not in ["auxiliar", "tecnico_especializado"]:
            raise HTTPException(status_code=422, detail="Solo se puede asignar a un auxiliar o tecnico especializado.")

        return crud_tickets.update_estado(db, id_ticket, actualizacion, id_asignado=actualizacion.id_asignado)

    elif estado_actual == "asignado" and nuevo_estado == "en_proceso":
        if "tickets:atender" not in mis_scopes or mi_rol not in ["auxiliar", "tecnico_especializado", "admin"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para atender tickets.")
        # Regla crítica: Solo el asignado puede pasarlo a en_proceso
        if db_ticket.id_asignado != mi_id and mi_rol != "admin":
            raise HTTPException(status_code=403, detail="Solo el técnico asignado a este ticket puede atenderlo.")
        return crud_tickets.update_estado(db, id_ticket, actualizacion)

    elif estado_actual == "en_proceso" and nuevo_estado == "en_revision":
        if "tickets:atender" not in mis_scopes or mi_rol not in ["auxiliar", "tecnico_especializado", "admin"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para modificar atenciones.")
        if db_ticket.id_asignado != mi_id and mi_rol != "admin":
            raise HTTPException(status_code=403, detail="Solo el técnico asignado puede enviar el ticket a revisión.")
        return crud_tickets.update_estado(db, id_ticket, actualizacion)

    elif estado_actual == "en_revision" and nuevo_estado == "terminado":
        if "tickets:finalizar" not in mis_scopes or mi_rol not in ["responsable_tecnico", "admin"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para finalizar tickets.")

        if mi_rol != "admin" and db_ticket.id_responsable != mi_id:
            raise HTTPException(status_code=403, detail="Solo el responsable del ticket puede finalizarlo.")

        return crud_tickets.update_estado(db, id_ticket, actualizacion)

    else:
        # Si intentan hacer una transición inventada (ej: de solicitado directo a terminado)
        raise HTTPException(
            status_code=422, 
            detail=f"Transición de estado no permitida: No puedes pasar de '{estado_actual}' a '{nuevo_estado}'."
        )