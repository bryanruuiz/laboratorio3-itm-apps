from sqlalchemy.orm import Session
from app.models.laboratorios import Laboratorio
from app.schemas.laboratorios import LaboratorioCreate

# Buscar todos los laboratorios
def get_laboratorios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Laboratorio).offset(skip).limit(limit).all()

# Buscar un laboratorio por ID
def get_laboratorio(db: Session, id_laboratorio: int):
    return db.query(Laboratorio).filter(Laboratorio.id_laboratorio == id_laboratorio).first()

# Crear un nuevo laboratorio
def create_laboratorio(db: Session, laboratorio: LaboratorioCreate):
    # Convertimos el esquema Pydantic en un modelo SQLAlchemy
    db_laboratorio = Laboratorio(**laboratorio.model_dump())
    db.add(db_laboratorio)
    db.commit()
    db.refresh(db_laboratorio) # Refresca para obtener el ID generado
    return db_laboratorio