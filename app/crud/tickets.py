from sqlalchemy.orm import Session
from app.models.tickets import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdateEstado

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket(db: Session, id_ticket: int):
    return db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()

def create_ticket(db: Session, ticket: TicketCreate, id_solicitante: int):
    db_ticket = Ticket(
        titulo=ticket.titulo,
        descripcion=ticket.descripcion,
        prioridad=ticket.prioridad,
        id_laboratorio=ticket.id_laboratorio,
        id_servicio=ticket.id_servicio,
        # Inyectamos el solicitante manualmente por ahora
        id_solicitante=id_solicitante 
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_estado(db: Session, id_ticket: int, datos: TicketUpdateEstado, id_asignado: int = None, id_responsable: int = None):
    db_ticket = get_ticket(db, id_ticket)
    if not db_ticket:
        return None
    
    # Actualizar estado
    db_ticket.estado = datos.estado
    
    # Actualizar observaciones si las envían
    if datos.observacion_responsable:
        db_ticket.observacion_responsable = datos.observacion_responsable
    if datos.observacion_tecnico:
        db_ticket.observacion_tecnico = datos.observacion_tecnico
        
    # Asignaciones (se usarán en la máquina de estados)
    if id_asignado:
        db_ticket.id_asignado = id_asignado
    if id_responsable:
        db_ticket.id_responsable = id_responsable
        
    db.commit()
    db.refresh(db_ticket)
    return db_ticket