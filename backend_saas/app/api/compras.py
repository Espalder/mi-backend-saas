from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.compra import Compra
from app.schemas.compra import CompraResponse

router = APIRouter(prefix="/api/compras", tags=["compras"])

@router.get("/", response_model=list[CompraResponse])
def listar_compras(db: Session = Depends(get_db)):
    return db.query(Compra).all() 