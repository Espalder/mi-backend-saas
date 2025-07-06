from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaResponse

router = APIRouter(prefix="/api/categorias", tags=["categorias"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all() 