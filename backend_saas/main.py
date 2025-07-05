from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config import settings
from app.models.database import get_db, engine
from app.models import Base
from app.services.auth_service import AuthService
from app.api import auth, empresas, usuarios, productos, clientes, ventas, reportes
from app.dependencies import get_current_user

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de Gestión Empresarial SaaS - API REST"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el esquema de autenticación
security = HTTPBearer()

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(empresas.router, prefix="/api/empresas", tags=["Empresas"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(ventas.router, prefix="/api/ventas", tags=["Ventas"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])

@app.get("/")
async def root():
    return {
        "message": "Sistema de Gestión Empresarial SaaS API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 