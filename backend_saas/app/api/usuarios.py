from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter()

def require_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden realizar esta acción"
        )
    return current_user

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
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario para la empresa del usuario actual (solo admin)"""
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

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar un usuario existente (solo admin)"""
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id,
        Usuario.empresa_id == current_user.empresa_id
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario_update.nombre is not None:
        usuario.nombre = usuario_update.nombre
    if usuario_update.email is not None:
        usuario.email = usuario_update.email
    if usuario_update.rol is not None:
        usuario.rol = usuario_update.rol
    if usuario_update.activo is not None:
        usuario.activo = usuario_update.activo
    if usuario_update.password is not None:
        usuario.password = AuthService.get_password_hash(usuario_update.password)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}", status_code=204)
async def delete_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Eliminar un usuario existente (solo admin)"""
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id,
        Usuario.empresa_id == current_user.empresa_id
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return None

@router.get("/me", response_model=UsuarioResponse)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user 