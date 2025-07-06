from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Historial(Base):
    __tablename__ = "historial"
    id = Column(Integer, primary_key=True, index=True)
    accion = Column(String(255), nullable=False)
    usuario_id = Column(Integer)
    fecha = Column(DateTime(timezone=True), server_default=func.now()) 