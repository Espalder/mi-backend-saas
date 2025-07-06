from sqlalchemy import Column, Integer, String
from .database import Base

class Configuracion(Base):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), nullable=False)
    valor = Column(String(255), nullable=False) 