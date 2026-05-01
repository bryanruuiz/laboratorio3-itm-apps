from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Servicio(Base):
    __tablename__ = "servicios"
    __table_args__ = {'schema': 'jwt_grupo_10'}

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    # Relación con tickets
    tickets = relationship("Ticket", back_populates="servicio")