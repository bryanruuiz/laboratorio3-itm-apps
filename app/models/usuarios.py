from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'jwt_grupo_10'} 

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False) # solicitante, responsable_tecnico, auxiliar, tecnico_especializado, admin
    activo = Column(Boolean, default=True)

    # Relaciones (Se conectarán con la tabla tickets más adelante)
    tickets_solicitados = relationship("Ticket", foreign_keys="[Ticket.id_solicitante]", back_populates="solicitante")
    tickets_responsable = relationship("Ticket", foreign_keys="[Ticket.id_responsable]", back_populates="responsable")
    tickets_asignados = relationship("Ticket", foreign_keys="[Ticket.id_asignado]", back_populates="asignado")