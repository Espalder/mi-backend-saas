from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.config import settings
from app.models.database import engine, SessionLocal
from app.models import Base
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.services.auth_service import AuthService
from app.api import auth, empresas, usuarios, productos, clientes, ventas, reportes, categorias, compras, proveedores, historial, configuracion
from app.dependencies import get_current_user

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de inicialización al arrancar
    db = SessionLocal()
    try:
        # Verificar si hay empresas
        if db.query(Empresa).count() == 0:
            print("🌱 Sembrando base de datos...")
            empresa = Empresa(
                nombre="Empresa Administradora",
                codigo_empresa="ADMIN001",
                descripcion="Sede principal del sistema",
                plan_suscripcion="enterprise"
            )
            db.add(empresa)
            db.commit()
            db.refresh(empresa)
            
            # Crear usuario admin
            hashed_password = AuthService.get_password_hash("admin123")
            user = Usuario(
                username="admin",
                password=hashed_password,
                nombre="Administrador",
                rol="admin",
                empresa_id=empresa.id,
                activo=True
            )
            db.add(user)
            db.commit()
            print("✅ Base de datos sembrada con éxito.")
    except Exception as e:
        print(f"❌ Error durante el sembrado: {e}")
    finally:
        db.close()
    yield

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de Gestión Empresarial SaaS - API REST",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(empresas.router, prefix="/api/empresas", tags=["Empresas"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(ventas.router, prefix="/api/ventas", tags=["Ventas"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])
app.include_router(categorias.router)
app.include_router(compras.router)
app.include_router(proveedores.router)
app.include_router(historial.router)
app.include_router(configuracion.router)

@app.get("/")
async def root():
    return {
        "message": "Sistema de Gestión Empresarial SaaS API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "healthy"}

@app.get("/usuarios/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
