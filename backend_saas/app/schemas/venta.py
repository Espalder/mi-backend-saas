from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id: int
    venta_id: int
    
    class Config:
        from_attributes = True

class VentaBase(BaseModel):
    cliente_id: Optional[int] = None
    numero_factura: Optional[str] = None
    subtotal: Decimal = 0
    descuento: Decimal = 0
    total: Decimal = 0
    estado: str = "completada"
    notas: Optional[str] = None

class VentaCreate(VentaBase):
    empresa_id: int
    usuario_id: int
    detalles: List[DetalleVentaCreate]

class VentaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    numero_factura: Optional[str] = None
    subtotal: Optional[Decimal] = None
    descuento: Optional[Decimal] = None
    total: Optional[Decimal] = None
    estado: Optional[str] = None
    notas: Optional[str] = None

class VentaResponse(VentaBase):
    id: int
    empresa_id: int
    usuario_id: int
    fecha: datetime
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    detalles: List[DetalleVentaResponse] = []
    
    class Config:
        from_attributes = True 