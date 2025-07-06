from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    precio_compra: Decimal
    stock: int = 0
    stock_minimo: int = 0
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    empresa_id: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    precio_compra: Optional[Decimal] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int
    empresa_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    activo: bool
    categoria_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True 