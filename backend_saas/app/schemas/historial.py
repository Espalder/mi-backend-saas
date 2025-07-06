from pydantic import BaseModel
from datetime import datetime

class HistorialResponse(BaseModel):
    id: int
    accion: str
    usuario_id: int
    fecha: datetime
    class Config:
        from_attributes = True 