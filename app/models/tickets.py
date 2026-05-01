from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {'schema': 'jwt_grupo_10'}

    id_ticket = Column(Integer, primary_key=True, index=True)
    
    # Claves foráneas 
    id_solicitante = Column(Integer, ForeignKey("jwt_grupo_10.usuarios.id_usuario"), nullable=False)
    id_laboratorio = Column(Integer, ForeignKey("jwt_grupo_10.laboratorios.id_laboratorio"), nullable=False)
    id_servicio = Column(Integer, ForeignKey("jwt_grupo_10.servicios.id_servicio"), nullable=False)
    id_responsable = Column(Integer, ForeignKey("jwt_grupo_10.usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey("jwt_grupo_10.usuarios.id_usuario"), nullable=True)
    
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    estado = Column(String, default="solicitado", nullable=False) # solicitado, recibido, asignado, en_proceso, en_revision, terminado
    prioridad = Column(String, nullable=False) # baja, media, alta
    
    observacion_responsable = Column(String, nullable=True)
    observacion_tecnico = Column(String, nullable=True)
    
    # Manejo de fechas automático
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_finalizacion = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante], back_populates="tickets_solicitados")
    responsable = relationship("Usuario", foreign_keys=[id_responsable], back_populates="tickets_responsable")
    asignado = relationship("Usuario", foreign_keys=[id_asignado], back_populates="tickets_asignados")
    
    laboratorio = relationship("Laboratorio", back_populates="tickets")
    servicio = relationship("Servicio", back_populates="tickets")