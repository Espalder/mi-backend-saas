from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str
    nombre: str
    email: Optional[str] = None
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str
    empresa_id: int

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    empresa_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    activo: bool
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    username: str
    password: str 