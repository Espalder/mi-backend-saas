from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.historial import Historial
from app.schemas.historial import HistorialResponse

router = APIRouter(prefix="/api/historial", tags=["historial"])

@router.get("/", response_model=list[HistorialResponse])
def listar_historial(db: Session = Depends(get_db)):
    return db.query(Historial).all() 