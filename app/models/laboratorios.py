from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Laboratorio(Base):
    __tablename__ = "laboratorios"
    __table_args__ = {'schema': 'jwt_grupo_10'}

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    # Relación con tickets
    tickets = relationship("Ticket", back_populates="laboratorio")