from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.configuracion import Configuracion
from app.schemas.configuracion import ConfiguracionResponse

router = APIRouter(prefix="/api/configuracion", tags=["configuracion"])

@router.get("/", response_model=list[ConfiguracionResponse])
def listar_configuracion(db: Session = Depends(get_db)):
    return db.query(Configuracion).all() 