#!/usr/bin/env python3
"""
Script para migrar datos existentes a la nueva estructura multi-tenant
"""
import mysql.connector
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models import Base, Empresa, Usuario, Producto, Cliente, Venta, DetalleVenta
from app.services.auth_service import AuthService
from config import settings

def migrate_data():
    """Migrar datos existentes a la nueva estructura multi-tenant"""
    
    # Crear las tablas nuevas
    Base.metadata.create_all(bind=engine)
    
    # Conectar a la base de datos existente
    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        port=settings.DB_PORT
    )
    cursor = conn.cursor()
    
    # Crear empresa por defecto
    db = SessionLocal()
    try:
        # Crear empresa por defecto
        empresa_default = Empresa(
            nombre="Empresa por Defecto",
            codigo_empresa="EMPRESA001",
            descripcion="Empresa creada durante la migración",
            plan_suscripcion="basic"
        )
        db.add(empresa_default)
        db.commit()
        db.refresh(empresa_default)
        
        print(f"✅ Empresa creada: {empresa_default.nombre} (ID: {empresa_default.id})")
        
        # Migrar usuarios
        cursor.execute("SELECT username, password, nombre, rol, activo FROM usuarios")
        usuarios_existentes = cursor.fetchall()
        
        for user_data in usuarios_existentes:
            username, password, nombre, rol, activo = user_data
            
            # Verificar si el usuario ya existe
            existing_user = db.query(Usuario).filter(Usuario.username == username).first()
            if not existing_user:
                # Hash de la contraseña si no está hasheada
                if not password.startswith('$2b$'):
                    password = AuthService.get_password_hash(password)
                
                nuevo_usuario = Usuario(
                    username=username,
                    password=password,
                    nombre=nombre,
                    rol=rol,
                    empresa_id=empresa_default.id,
                    activo=bool(activo)
                )
                db.add(nuevo_usuario)
                print(f"✅ Usuario migrado: {username}")
        
        # Migrar productos
        cursor.execute("SELECT codigo, nombre, descripcion, precio, stock, activo FROM productos")
        productos_existentes = cursor.fetchall()
        
        for prod_data in productos_existentes:
            codigo, nombre, descripcion, precio, stock, activo = prod_data
            
            # Verificar si el producto ya existe
            existing_producto = db.query(Producto).filter(
                Producto.codigo == codigo,
                Producto.empresa_id == empresa_default.id
            ).first()
            
            if not existing_producto:
                nuevo_producto = Producto(
                    codigo=codigo,
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    empresa_id=empresa_default.id,
                    activo=bool(activo)
                )
                db.add(nuevo_producto)
                print(f"✅ Producto migrado: {codigo} - {nombre}")
        
        # Migrar clientes
        cursor.execute("SELECT nombre FROM clientes")
        clientes_existentes = cursor.fetchall()
        
        for cli_data in clientes_existentes:
            nombre = cli_data[0]
            
            # Verificar si el cliente ya existe
            existing_cliente = db.query(Cliente).filter(
                Cliente.nombre == nombre,
                Cliente.empresa_id == empresa_default.id
            ).first()
            
            if not existing_cliente:
                nuevo_cliente = Cliente(
                    nombre=nombre,
                    empresa_id=empresa_default.id
                )
                db.add(nuevo_cliente)
                print(f"✅ Cliente migrado: {nombre}")
        
        db.commit()
        print("✅ Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
    finally:
        db.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando migración de datos...")
    migrate_data() 