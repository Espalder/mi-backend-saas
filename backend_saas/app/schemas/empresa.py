from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmpresaBase(BaseModel):
    nombre: str
    codigo_empresa: str
    descripcion: Optional[str] = None
    plan_suscripcion: str = "basic"

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    plan_suscripcion: Optional[str] = None
    activo: Optional[bool] = None

class EmpresaResponse(EmpresaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    activo: bool
    
    class Config:
        from_attributes = True 