from pydantic import BaseModel

class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True 