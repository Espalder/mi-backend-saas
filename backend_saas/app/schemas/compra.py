from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompraResponse(BaseModel):
    id: int
    proveedor_id: int
    fecha: datetime
    total: float
    class Config:
        from_attributes = True 