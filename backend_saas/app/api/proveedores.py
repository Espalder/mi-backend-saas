from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorResponse

router = APIRouter(prefix="/api/proveedores", tags=["proveedores"])

@router.get("/", response_model=list[ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all() 