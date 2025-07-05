from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los usuarios de la empresa del usuario actual"""
    usuarios = db.query(Usuario).filter(
        Usuario.empresa_id == current_user.empresa_id,
        Usuario.activo == True
    ).offset(skip).limit(limit).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un usuario específico de la empresa del usuario actual"""
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id,
        Usuario.empresa_id == current_user.empresa_id,
        Usuario.activo == True
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.post("/", response_model=UsuarioResponse)
async def create_usuario(
    usuario: UsuarioCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario para la empresa del usuario actual"""
    # Verificar que el username no exista
    existing_usuario = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()
    
    if existing_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese username"
        )
    
    # Hash de la contraseña
    hashed_password = AuthService.get_password_hash(usuario.password)
    
    db_usuario = Usuario(
        username=usuario.username,
        password=hashed_password,
        nombre=usuario.nombre,
        email=usuario.email,
        rol=usuario.rol,
        empresa_id=current_user.empresa_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario 