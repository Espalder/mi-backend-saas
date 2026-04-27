"""
Script de instalación del Sistema de Gestión Empresarial
"""
import os
import sys
import subprocess

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    dependencias = [
        'mysql-connector-python',
        'Pillow',
        'tkinter'  # Ya viene con Python
    ]
    
    for dep in dependencias:
        try:
            if dep == 'tkinter':
                print(f"✅ {dep} ya está incluido con Python")
                continue
                
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")

def configurar_base_datos():
    """Configurar base de datos"""
    print("\n🗄️ Configurando base de datos...")
    
    # Importar y ejecutar configuración de BD
    try:
        from configuracion_bd_local import crear_tablas_mysql, verificar_conexion
        
        if verificar_conexion():
            if crear_tablas_mysql():
                print("✅ Base de datos configurada correctamente")
                return True
            else:
                print("❌ Error al crear las tablas")
                return False
        else:
            print("❌ No se pudo conectar a MySQL")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")
        return False

def verificar_configuracion():
    """Verificar configuración del sistema"""
    print("\n🔍 Verificando configuración...")
    
    # Verificar archivos necesarios
    archivos_necesarios = [
        'main_offline.py',
        'modulo_autenticacion.py',
        'modulo_inventario.py',
        'modulo_ventas.py',
        'modulo_reportes.py',
        'modulo_configuracion.py',
        'estilos.py',
        'config_bd.py'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"❌ Archivos faltantes: {archivos_faltantes}")
        return False
    else:
        print("✅ Todos los archivos necesarios están presentes")
        return True

def mostrar_instrucciones():
    """Mostrar instrucciones de uso"""
    print("\n" + "="*60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("="*60)
    print("\n📋 INSTRUCCIONES DE USO:")
    print("\n1. 🔧 CONFIGURAR BASE DE DATOS:")
    print("   - Edita el archivo 'config_bd.py'")
    print("   - Cambia 'USAR_BD_LOCAL = True' para usar BD local")
    print("   - Ajusta las credenciales de MySQL si es necesario")
    
    print("\n2. 🚀 EJECUTAR EL SISTEMA:")
    print("   - Ejecuta: python main_offline.py")
    print("   - Usuario por defecto: admin")
    print("   - Contraseña por defecto: admin123")
    
    print("\n3. 🗄️ BASE DE DATOS:")
    print("   - Local: gestion_empresas (MySQL)")
    print("   - Remota: railway (Railway)")
    print("   - Respaldo: offline_backup.db (SQLite)")
    
    print("\n4. 🔑 USUARIOS POR DEFECTO:")
    print("   - admin / admin123 (Administrador)")
    print("   - Puedes crear más usuarios desde Configuración")
    
    print("\n5. 📁 ARCHIVOS IMPORTANTES:")
    print("   - configuracion.json: Configuración del sistema")
    print("   - offline_backup.db: Respaldo local")
    print("   - backup_sistema_*.json.gz: Respaldos comprimidos")
    
    print("\n" + "="*60)
    print("¡El sistema está listo para usar! 🎊")
    print("="*60)

def main():
    """Función principal de instalación"""
    print("🚀 INSTALADOR DEL SISTEMA DE GESTIÓN EMPRESARIAL")
    print("="*60)
    
    # Verificar configuración
    if not verificar_configuracion():
        print("\n❌ Error en la configuración. Verifica los archivos.")
        return
    
    # Instalar dependencias
    instalar_dependencias()
    
    # Configurar base de datos
    if configurar_base_datos():
        mostrar_instrucciones()
    else:
        print("\n❌ Error configurando la base de datos.")
        print("Verifica que MySQL esté ejecutándose y las credenciales sean correctas.")

if __name__ == "__main__":
    main()
