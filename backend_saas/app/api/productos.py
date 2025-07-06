from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductoResponse])
async def get_productos(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los productos de la empresa del usuario actual"""
    productos = db.query(Producto).filter(
        Producto.empresa_id == current_user.empresa_id,
        Producto.activo == True
    ).offset(skip).limit(limit).all()
    # Agregar el nombre de la categoría a cada producto
    productos_response = []
    for prod in productos:
        categoria_nombre = None
        if prod.categoria:
            categoria_nombre = prod.categoria.nombre
        prod_dict = prod.__dict__.copy()
        prod_dict["categoria_nombre"] = categoria_nombre
        prod_dict["precio_compra"] = getattr(prod, "precio_compra", 0)
        productos_response.append(ProductoResponse(**prod_dict))
    return productos_response

@router.get("/{producto_id}", response_model=ProductoResponse)
async def get_producto(
    producto_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un producto específico de la empresa del usuario actual"""
    producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.empresa_id == current_user.empresa_id,
        Producto.activo == True
    ).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto

@router.post("/", response_model=ProductoResponse)
async def create_producto(
    producto: ProductoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo producto para la empresa del usuario actual"""
    # Verificar que el código no exista en la misma empresa
    existing_producto = db.query(Producto).filter(
        Producto.codigo == producto.codigo,
        Producto.empresa_id == current_user.empresa_id
    ).first()
    
    if existing_producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con ese código en esta empresa"
        )
    
    data = producto.dict()
    data["empresa_id"] = current_user.empresa_id
    db_producto = Producto(**data)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar un producto de la empresa del usuario actual"""
    db_producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.empresa_id == current_user.empresa_id
    ).first()
    
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = producto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{producto_id}")
async def delete_producto(
    producto_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar (desactivar) un producto de la empresa del usuario actual"""
    db_producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.empresa_id == current_user.empresa_id
    ).first()
    
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Soft delete - solo desactivar
    db_producto.activo = False
    db.commit()
    
    return {"message": "Producto eliminado correctamente"} 