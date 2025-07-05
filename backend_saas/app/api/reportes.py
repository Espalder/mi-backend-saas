from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.venta import Venta
from app.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter()

@router.get("/general")
async def get_reporte_general(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener reporte general de la empresa"""
    try:
        # Contar productos
        total_productos = db.query(func.count(Producto.id)).filter(
            Producto.empresa_id == current_user.empresa_id,
            Producto.activo == True
        ).scalar()
        
        # Contar clientes
        total_clientes = db.query(func.count(Cliente.id)).filter(
            Cliente.empresa_id == current_user.empresa_id,
            Cliente.activo == True
        ).scalar()
        
        # Contar ventas
        total_ventas = db.query(func.count(Venta.id)).filter(
            Venta.empresa_id == current_user.empresa_id
        ).scalar()
        
        # Sumar total de ventas
        total_ventas_monto = db.query(func.sum(Venta.total)).filter(
            Venta.empresa_id == current_user.empresa_id
        ).scalar() or 0
        
        # Ventas del mes actual (simplificado)
        from datetime import datetime, timedelta
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        ventas_mes = db.query(func.count(Venta.id)).filter(
            Venta.empresa_id == current_user.empresa_id,
            Venta.fecha >= inicio_mes
        ).scalar()
        
        monto_mes = db.query(func.sum(Venta.total)).filter(
            Venta.empresa_id == current_user.empresa_id,
            Venta.fecha >= inicio_mes
        ).scalar() or 0
        
        return {
            "total_productos": total_productos,
            "total_clientes": total_clientes,
            "total_ventas": total_ventas,
            "total_ventas_monto": float(total_ventas_monto),
            "ventas_mes": ventas_mes,
            "monto_mes": float(monto_mes)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte: {str(e)}"
        ) 