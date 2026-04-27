"""
Script para configurar la base de datos local y crear las tablas necesarias
"""
import mysql.connector
from mysql.connector import Error
import os
from config_bd import DB_CONFIG_LOCAL

def crear_tablas_mysql():
    """Crear todas las tablas necesarias en MySQL local"""
    
    # Script SQL para crear todas las tablas
    sql_script = """
    -- Crear base de datos si no existe
    CREATE DATABASE IF NOT EXISTS gestion_empresas;
    USE gestion_empresas;

    -- Tabla de usuarios
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        rol ENUM('admin', 'vendedor', 'inventario') NOT NULL,
        activo TINYINT(1) DEFAULT 1,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Tabla de productos
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo VARCHAR(50) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        precio DECIMAL(10,2) NOT NULL,
        stock INT NOT NULL DEFAULT 0,
        stock_minimo INT DEFAULT 5,
        categoria VARCHAR(50) DEFAULT 'General',
        activo TINYINT(1) DEFAULT 1,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Tabla de clientes
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        telefono VARCHAR(20),
        direccion TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Tabla de ventas
    CREATE TABLE IF NOT EXISTS ventas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cliente_id INT,
        usuario_id INT,
        subtotal DECIMAL(10,2) DEFAULT 0,
        descuento DECIMAL(10,2) DEFAULT 0,
        total DECIMAL(10,2) DEFAULT 0,
        estado ENUM('pendiente', 'completada', 'cancelada') DEFAULT 'completada',
        sincronizado TINYINT(1) DEFAULT 0,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );

    -- Tabla de detalle de ventas
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        venta_id INT,
        producto_id INT,
        cantidad INT NOT NULL,
        precio_unitario DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        sincronizado TINYINT(1) DEFAULT 0,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );

    -- Tabla de auditoría
    CREATE TABLE IF NOT EXISTS auditoria (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tabla VARCHAR(50) NOT NULL,
        accion VARCHAR(20) NOT NULL,
        registro_id INT,
        datos_anteriores JSON,
        datos_nuevos JSON,
        usuario VARCHAR(50) NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Tabla de configuración del sistema
    CREATE TABLE IF NOT EXISTS configuracion_sistema (
        id INT AUTO_INCREMENT PRIMARY KEY,
        clave VARCHAR(100) UNIQUE NOT NULL,
        valor TEXT NOT NULL,
        descripcion TEXT,
        fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Tabla de notificaciones
    CREATE TABLE IF NOT EXISTS notificaciones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        mensaje TEXT NOT NULL,
        tipo ENUM('info', 'warning', 'error') DEFAULT 'info',
        leida TINYINT(1) DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sincronizado TINYINT(1) DEFAULT 0
    );

    -- Insertar configuración por defecto
    INSERT IGNORE INTO configuracion_sistema (clave, valor, descripcion) VALUES 
    ('alerta_stock_minimo', '5', 'Nivel mínimo de stock para alertas'),
    ('tema_aplicacion', 'claro', 'Tema visual de la aplicación'),
    ('auto_sync_interval', '300', 'Intervalo de sincronización automática en segundos'),
    ('backup_automatico', '1', 'Habilitar respaldo automático');

    -- Insertar usuario administrador por defecto
    INSERT IGNORE INTO usuarios (username, password, nombre, rol) VALUES 
    ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2O', 'Administrador', 'admin');
    """
    
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host=DB_CONFIG_LOCAL['host'],
            user=DB_CONFIG_LOCAL['user'],
            password=DB_CONFIG_LOCAL['password'],
            port=DB_CONFIG_LOCAL['port']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Ejecutar el script SQL
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            connection.commit()
            print("✅ Tablas creadas exitosamente en la base de datos local")
            
            # Verificar que las tablas se crearon
            cursor.execute("USE gestion_empresas")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tablas creadas: {[table[0] for table in tables]}")
            
    except Error as e:
        print(f"❌ Error al crear las tablas: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

def verificar_conexion():
    """Verificar conexión a la base de datos local"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG_LOCAL)
        if connection.is_connected():
            print("✅ Conexión a base de datos local exitosa")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"📊 Base de datos actual: {db_name}")
            return True
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("🔧 Configurando base de datos local...")
    print("=" * 50)
    
    # Verificar conexión
    if verificar_conexion():
        # Crear tablas
        if crear_tablas_mysql():
            print("\n🎉 ¡Base de datos configurada correctamente!")
            print("Ahora puedes ejecutar el sistema con la base de datos local.")
        else:
            print("\n❌ Error al configurar la base de datos")
    else:
        print("\n❌ No se pudo conectar a MySQL local")
        print("Verifica que:")
        print("1. MySQL esté ejecutándose")
        print("2. Las credenciales en DB_CONFIG_LOCAL sean correctas")
        print("3. El usuario tenga permisos para crear bases de datos")
