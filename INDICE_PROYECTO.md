# ÍNDICE DEL PROYECTO - SISTEMA DE GESTIÓN EMPRESARIAL

## Estructura Organizada del Proyecto

Este documento explica la organización de carpetas y archivos del proyecto para facilitar la navegación y mantenimiento.

---

## 📁 CARPETAS PRINCIPALES

### 🏠 **Raíz del Proyecto**
- `README.md` - Documentación principal del proyecto
- `configuracion.json` - Configuración general del sistema
- `requirements.txt` - Dependencias principales

### 📚 **documentacion/**
Contiene toda la documentación del proyecto:
- `DOCUMENTACION_COMPLETA_SISTEMA_SAAS.md` - Documentación técnica completa
- `DOCUMENTACION_COMPLETA_SISTEMA_SAAS.pdf` - Versión PDF de la documentación
- `INFORME_PROYECTO_SISTEMA_SAAS.md` - Informe final del proyecto
- `INFORME_PROYECTO_SISTEMA_SAAS.pdf` - Versión PDF del informe
- `README_OFFLINE_ONLINE.md` - Documentación del sistema offline
- `custom_pdf_style.css` - Estilos para generación de PDFs

### 🔧 **scripts_utiles/**
Scripts y herramientas de utilidad:
- `keep_alive.py` - Script para mantener el backend activo
- `generar_hashes_bcrypt.py` - Generador de hashes para contraseñas
- `sistema_gestion.py` - Sistema de gestión básico
- `sistema_gestion_mejorado.py` - Sistema de gestión mejorado
- `script_alter_fechas.sql` - Script para modificar fechas en BD
- `script_migracion_multitenant.sql` - Script de migración multiempresa
- `historial_reportes.json` - Historial de reportes generados
- `requirements_keep_alive.txt` - Dependencias para keep_alive

### 📊 **diagramas/**
Diagramas y archivos de diseño:
- `diagrama_despliegue_mermaid.md` - Diagrama de despliegue básico
- `diagrama_despliegue_mermaid_extendido.md` - Diagrama de despliegue extendido
- `diagrama_despliegue_mermaid_super_extenso.md` - Diagrama de despliegue completo
- `sql_limpio_para_railway.sql` - Script SQL limpio para Railway

### 📦 **archivos_compresos/**
Archivos comprimidos del proyecto:
- `proyecto_completo_funcional.zip` - Proyecto completo comprimido
- `sistema_gestion_mejorado_modulos.rar` - Sistema offline comprimido
- `sistema_gestion_mejorado_modulos_OFFLINE_ONLINE.zip` - Sistema offline/online

### 🖼️ **images/**
Recursos gráficos del proyecto:
- `banner_bg.png` - Imagen de fondo del banner
- `caja_registradora.png` - Icono de caja registradora
- `logo_empresa.png` - Logo de la empresa

### 🗄️ **SQL/**
Scripts de base de datos:
- `respaldo_railway.sql` - Respaldo de la base de datos de Railway

---

## 🚀 CARPETAS DE DESARROLLO

### ⚙️ **backend_saas/**
Backend del sistema SaaS (FastAPI):
- API RESTful completa
- Autenticación JWT
- Gestión multiempresa
- Endpoints para todas las entidades

### 🎨 **frontend_saas/**
Frontend del sistema SaaS (React):
- Interfaz moderna con Material UI
- Sistema de roles y permisos
- Reportes con gráficos
- Gestión completa de entidades

### 💻 **sistema_gestion_mejorado_modulos/**
Sistema offline (Tkinter):
- Aplicación de escritorio
- Sincronización con la nube
- Gestión local de datos

### 🔄 **backup_sistema_actual/**
Respaldos y versiones previas:
- Versiones anteriores del sistema
- Respaldos de configuración
- Archivos de respaldo

---

## 📋 ARCHIVOS IMPORTANTES

### Documentación Principal
- **README.md** - Punto de entrada principal del proyecto
- **INDICE_PROYECTO.md** - Este archivo de índice

### Configuración
- **configuracion.json** - Configuración general del sistema
- **requirements.txt** - Dependencias de Python

---

## 🔍 CÓMO NAVEGAR EL PROYECTO

### Para Desarrolladores:
1. **README.md** - Información general y setup
2. **documentacion/** - Documentación técnica completa
3. **backend_saas/** - Código del backend
4. **frontend_saas/** - Código del frontend
5. **scripts_utiles/** - Herramientas de desarrollo

### Para Usuarios:
1. **README.md** - Guía de instalación y uso
2. **documentacion/** - Manuales y documentación
3. **archivos_compresos/** - Descargas del sistema

### Para Despliegue:
1. **diagramas/** - Diagramas de arquitectura
2. **SQL/** - Scripts de base de datos
3. **scripts_utiles/** - Scripts de mantenimiento

---

## 📝 NOTAS IMPORTANTES

- **Git:** Todos los archivos están bajo control de versiones
- **Compatibilidad:** La organización mantiene la funcionalidad completa
- **Mantenimiento:** Los archivos están organizados por tipo y función
- **Escalabilidad:** La estructura permite agregar nuevos módulos fácilmente

---

**Última actualización:** 13/07/2025  
**Versión del proyecto:** 2.0.0  
**Organización:** Completada 