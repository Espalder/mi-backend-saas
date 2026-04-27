"""
Script para actualizar la estructura de la base de datos existente
"""
import mysql.connector
from mysql.connector import Error
from config_bd import DB_CONFIG

def actualizar_estructura_bd():
    """Actualizar la estructura de la base de datos existente"""
    
    # Script SQL para actualizar la estructura
    sql_updates = [
        # Agregar columna categoria a productos si no existe
        "ALTER TABLE productos ADD COLUMN IF NOT EXISTS categoria VARCHAR(50) DEFAULT 'General'",
        
        # Agregar columna stock_minimo a productos si no existe
        "ALTER TABLE productos ADD COLUMN IF NOT EXISTS stock_minimo INT DEFAULT 5",
        
        # Agregar columna fecha_modificacion a productos si no existe
        "ALTER TABLE productos ADD COLUMN IF NOT EXISTS fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        
        # Actualizar la tabla usuarios para asegurar que tenga el rol correcto
        "ALTER TABLE usuarios MODIFY COLUMN rol ENUM('admin', 'vendedor', 'inventario') NOT NULL",
        
        # Insertar usuario admin si no existe
        """
        INSERT IGNORE INTO usuarios (username, password, nombre, rol) VALUES 
        ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2O', 'Administrador', 'admin')
        """,
        
        # Insertar configuración por defecto si no existe
        """
        INSERT IGNORE INTO configuracion_sistema (clave, valor, descripcion) VALUES 
        ('alerta_stock_minimo', '5', 'Nivel mínimo de stock para alertas'),
        ('tema_aplicacion', 'claro', 'Tema visual de la aplicación'),
        ('auto_sync_interval', '300', 'Intervalo de sincronización automática en segundos'),
        ('backup_automatico', '1', 'Habilitar respaldo automático')
        """
    ]
    
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔧 Actualizando estructura de la base de datos...")
            
            # Ejecutar cada actualización
            for i, sql in enumerate(sql_updates, 1):
                try:
                    if sql.strip():
                        cursor.execute(sql)
                        print(f"✅ Actualización {i} ejecutada correctamente")
                except Error as e:
                    if "Duplicate column name" in str(e) or "already exists" in str(e):
                        print(f"ℹ️ Actualización {i} omitida (ya existe): {e}")
                    else:
                        print(f"⚠️ Error en actualización {i}: {e}")
            
            connection.commit()
            
            # Verificar estructura actualizada
            print("\n📋 Verificando estructura actualizada...")
            
            # Verificar tabla productos
            cursor.execute("DESCRIBE productos")
            columnas_productos = cursor.fetchall()
            print("📦 Columnas de productos:")
            for columna in columnas_productos:
                print(f"   - {columna[0]} ({columna[1]})")
            
            # Verificar usuarios
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total_usuarios = cursor.fetchone()[0]
            print(f"👥 Total de usuarios: {total_usuarios}")
            
            # Verificar configuración
            cursor.execute("SELECT COUNT(*) FROM configuracion_sistema")
            total_config = cursor.fetchone()[0]
            print(f"⚙️ Configuraciones: {total_config}")
            
            print("\n🎉 ¡Base de datos actualizada correctamente!")
            
    except Error as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    print("🔧 Actualizando estructura de base de datos...")
    print("=" * 50)
    
    if actualizar_estructura_bd():
        print("\n✅ ¡Actualización completada!")
        print("Ahora puedes ejecutar el sistema sin errores.")
    else:
        print("\n❌ Error en la actualización")
