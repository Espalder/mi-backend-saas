from pydantic import BaseModel

class ConfiguracionResponse(BaseModel):
    id: int
    clave: str
    valor: str
    class Config:
        from_attributes = True 