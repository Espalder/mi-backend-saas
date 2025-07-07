from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from pydantic import ValidationError
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[EmpresaResponse])
async def get_empresas(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las empresas (solo para administradores)"""
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver todas las empresas"
        )
    
    empresas = db.query(Empresa).filter(Empresa.activo == True).offset(skip).limit(limit).all()
    return empresas

@router.get("/{empresa_id}", response_model=EmpresaResponse)
async def get_empresa(
    empresa_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una empresa específica"""
    if current_user.rol != "admin" and current_user.empresa_id != empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta empresa"
        )
    
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id,
        Empresa.activo == True
    ).first()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return empresa

@router.post("/", response_model=EmpresaResponse)
async def create_empresa(
    empresa: EmpresaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva empresa (solo para administradores)"""
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear empresas"
        )
    
    # Verificar que el código de empresa no exista
    existing_empresa = db.query(Empresa).filter(
        Empresa.codigo_empresa == empresa.codigo_empresa
    ).first()
    
    if existing_empresa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una empresa con ese código"
        )
    
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa 

@router.get("/me")
async def get_empresa_actual(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == current_user.empresa_id,
        Empresa.activo == True
    ).first()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    try:
        return EmpresaResponse.from_orm(empresa)
    except ValidationError as e:
        raise HTTPException(
            status_code=418,
            detail=e.errors()
        )

@router.put("/me", response_model=EmpresaResponse)
async def update_empresa_actual(
    empresa_update: EmpresaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar la empresa del usuario autenticado"""
    empresa = db.query(Empresa).filter(
        Empresa.id == current_user.empresa_id,
        Empresa.activo == True
    ).first()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    
    for field, value in empresa_update.dict(exclude_unset=True).items():
        setattr(empresa, field, value)
    
    db.commit()
    db.refresh(empresa)
    return empresa 