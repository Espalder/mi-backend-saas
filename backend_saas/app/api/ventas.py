from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from app.models.database import get_db
from app.models.usuario import Usuario
from app.models.venta import Venta, DetalleVenta
from app.models.producto import Producto
from app.schemas.venta import VentaCreate, VentaUpdate, VentaResponse, DetalleVentaCreate
from app.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[VentaResponse])
async def get_ventas(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las ventas de la empresa del usuario actual"""
    ventas = db.query(Venta).filter(
        Venta.empresa_id == current_user.empresa_id
    ).offset(skip).limit(limit).all()
    return ventas

@router.get("/{venta_id}", response_model=VentaResponse)
async def get_venta(
    venta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una venta específica de la empresa del usuario actual"""
    venta = db.query(Venta).filter(
        Venta.id == venta_id,
        Venta.empresa_id == current_user.empresa_id
    ).first()
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta

@router.post("/", response_model=VentaResponse)
async def create_venta(
    venta: VentaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva venta para la empresa del usuario actual"""
    # Crear la venta
    db_venta = Venta(
        empresa_id=current_user.empresa_id,
        usuario_id=current_user.id,
        cliente_id=venta.cliente_id,
        numero_factura=venta.numero_factura,
        subtotal=venta.subtotal,
        descuento=venta.descuento,
        total=venta.total,
        estado=venta.estado,
        notas=venta.notas,
        fecha=datetime.utcnow()
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    
    # Crear los detalles de venta
    for detalle in venta.detalles:
        # Verificar que el producto existe y pertenece a la empresa
        producto = db.query(Producto).filter(
            Producto.id == detalle.producto_id,
            Producto.empresa_id == current_user.empresa_id,
            Producto.activo == True
        ).first()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto con ID {detalle.producto_id} no encontrado"
            )
        
        # Verificar stock
        if producto.stock < detalle.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {producto.nombre}"
            )
        
        # Crear detalle de venta
        db_detalle = DetalleVenta(
            venta_id=db_venta.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.subtotal
        )
        db.add(db_detalle)
        
        # Actualizar stock del producto
        producto.stock -= detalle.cantidad
    
    db.commit()
    db.refresh(db_venta)
    return db_venta 