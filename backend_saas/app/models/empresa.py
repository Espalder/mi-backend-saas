from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo_empresa = Column(String(20), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    plan_suscripcion = Column(String(20), default="basic")  # basic, premium, enterprise
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    activo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Empresa(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo_empresa}')>" 