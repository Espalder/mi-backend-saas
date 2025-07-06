from sqlalchemy import Column, Integer, String
from .database import Base

class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False) 