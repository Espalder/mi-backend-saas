from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Venta(Base):
    __tablename__ = "ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    numero_factura = Column(String(50), nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    subtotal = Column(Numeric(10, 2), default=0)
    descuento = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    estado = Column(String(20), default="completada")  # completada, cancelada, pendiente
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    empresa = relationship("Empresa", backref="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario", backref="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Venta(id={self.id}, total={self.total}, estado='{self.estado}')>"

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")
    
    def __repr__(self):
        return f"<DetalleVenta(id={self.id}, cantidad={self.cantidad}, subtotal={self.subtotal})>" 