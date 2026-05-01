from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.tickets import TicketCreate, TicketResponse, TicketUpdateEstado
from app.crud import tickets as crud_tickets

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse)
def crear_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # TEMPORAL: Asumimos que el usuario con ID 1 está creando el ticket
    # En la Actividad 5, esto se sacará del token del usuario logueado
    id_usuario_simulado = 1 
    return crud_tickets.create_ticket(db=db, ticket=ticket, id_solicitante=id_usuario_simulado)

@router.get("/", response_model=List[TicketResponse])
def listar_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tickets.get_tickets(db, skip=skip, limit=limit)

@router.get("/{id_ticket}", response_model=TicketResponse)
def obtener_ticket(id_ticket: int, db: Session = Depends(get_db)):
    db_ticket = crud_tickets.get_ticket(db, id_ticket=id_ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return db_ticket

@router.patch("/{id_ticket}/estado", response_model=TicketResponse)
def actualizar_estado(id_ticket: int, actualizacion: TicketUpdateEstado, db: Session = Depends(get_db)):
    db_ticket = crud_tickets.update_estado(db, id_ticket=id_ticket, datos=actualizacion)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return db_ticket