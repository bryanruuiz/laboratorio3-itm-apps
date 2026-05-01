from sqlalchemy.orm import Session
from app.models.servicios import Servicio
from app.schemas.servicios import ServicioCreate

def get_servicios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Servicio).offset(skip).limit(limit).all()

def get_servicio(db: Session, id_servicio: int):
    return db.query(Servicio).filter(Servicio.id_servicio == id_servicio).first()

def create_servicio(db: Session, servicio: ServicioCreate):
    db_servicio = Servicio(**servicio.model_dump())
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio