#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación de dependencias para el Sistema de Gestión Empresarial
Instala automáticamente todos los paquetes necesarios
"""

import subprocess
import sys
import os
import importlib.util

def verificar_python():
    """Verifica que se esté ejecutando con Python 3.6+"""
    if sys.version_info < (3, 6):
        print("❌ Error: Se requiere Python 3.6 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def verificar_pip():
    """Verifica que pip esté disponible"""
    try:
        import pip
        print("✅ pip disponible")
        return True
    except ImportError:
        print("❌ Error: pip no está instalado")
        print("   Instala pip desde: https://pip.pypa.io/en/stable/installation/")
        return False

def instalar_paquete(paquete):
    """Instala un paquete usando pip"""
    try:
        # Verificar si ya está instalado
        if paquete.split('==')[0] in sys.modules or importlib.util.find_spec(paquete.split('==')[0]):
            print(f"✅ {paquete.split('==')[0]} ya está instalado")
            return True
        
        print(f"📦 Instalando {paquete}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {paquete} instalado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar {paquete}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al instalar {paquete}: {e}")
        return False

def verificar_paquete(nombre_paquete):
    """Verifica si un paquete está instalado"""
    try:
        importlib.util.find_spec(nombre_paquete)
        return True
    except ImportError:
        return False

def main():
    print("🚀 Instalador de dependencias - Sistema de Gestión Empresarial")
    print("=" * 60)
    
    # Verificar Python
    if not verificar_python():
        return False
    
    # Verificar pip
    if not verificar_pip():
        return False
    
    print("\n📋 Instalando dependencias necesarias...")
    
    # Lista de paquetes principales
    paquetes = [
        "mysql-connector-python==8.2.0",
        "reportlab==4.0.4",
        "matplotlib==3.8.2",
        "numpy==1.26.2",
        "Pillow==10.1.0",
        "python-dateutil==2.8.2"
    ]
    
    # Paquetes opcionales para desarrollo
    paquetes_dev = [
        "pytest==7.4.3",
        "pytest-cov==4.1.0"
    ]
    
    errores = []
    
    # Instalar paquetes principales
    for paquete in paquetes:
        if not instalar_paquete(paquete):
            errores.append(paquete)
    
    print("\n🔧 Instalando paquetes de desarrollo (opcionales)...")
    
    # Instalar paquetes de desarrollo
    for paquete in paquetes_dev:
        instalar_paquete(paquete)  # No añadir a errores si falla
    
    # Verificar instalaciones críticas
    print("\n🔍 Verificando instalaciones críticas...")
    
    verificaciones = {
        "mysql.connector": "mysql-connector-python",
        "reportlab": "reportlab", 
        "matplotlib": "matplotlib",
        "numpy": "numpy",
        "PIL": "Pillow"
    }
    
    for modulo, paquete in verificaciones.items():
        if verificar_paquete(modulo):
            print(f"✅ {paquete} funcionando correctamente")
        else:
            print(f"❌ {paquete} no se pudo verificar")
            errores.append(paquete)
    
    # Resumen final
    print("\n" + "=" * 60)
    
    if errores:
        print("⚠️  Instalación completada con errores:")
        for error in errores:
            print(f"   - {error}")
        print("\n💡 Consejos:")
        print("   - Ejecuta este script como administrador")
        print("   - Actualiza pip: python -m pip install --upgrade pip")
        print("   - Verifica tu conexión a internet")
        return False
    else:
        print("🎉 ¡Todas las dependencias instaladas exitosamente!")
        print("\n🚀 Puedes ejecutar el sistema con:")
        print("   python main_offline.py")
        return True

def crear_archivo_bat():
    """Crea un archivo batch para Windows"""
    contenido_bat = '''@echo off
echo Instalando dependencias del Sistema de Gestion Empresarial...
python instalar_dependencias.py
pause
'''
    
    try:
        with open('instalar_dependencias.bat', 'w', encoding='utf-8') as f:
            f.write(contenido_bat)
        print("✅ Archivo instalar_dependencias.bat creado para Windows")
    except Exception as e:
        print(f"❌ Error al crear archivo .bat: {e}")

def crear_archivo_sh():
    """Crea un archivo shell script para Linux/Mac"""
    contenido_sh = '''#!/bin/bash
echo "Instalando dependencias del Sistema de Gestión Empresarial..."
python3 instalar_dependencias.py
read -p "Presiona Enter para continuar..."
'''
    
    try:
        with open('instalar_dependencias.sh', 'w', encoding='utf-8') as f:
            f.write(contenido_sh)
        os.chmod('instalar_dependencias.sh', 0o755)
        print("✅ Archivo instalar_dependencias.sh creado para Linux/Mac")
    except Exception as e:
        print(f"❌ Error al crear archivo .sh: {e}")

if __name__ == "__main__":
    try:
        exito = main()
        
        # Crear archivos de conveniencia
        if os.name == 'nt':  # Windows
            crear_archivo_bat()
        else:  # Linux/Mac
            crear_archivo_sh()
            
        if exito:
            print("\n🎯 Sistema listo para usar!")
        else:
            print("\n⚠️  Revisa los errores e intenta nuevamente")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("   Contacta al soporte técnico")
