# 🚀 Sistema de Gestión Empresarial - Guía de Instalación

## 📋 PROBLEMA SOLUCIONADO

**Error:** `"No se pudo conectar a ninguna base de datos: no such table: usuarios"`

**Causa:** La base de datos local no tiene las tablas necesarias creadas.

**Solución:** Scripts de configuración automática incluidos.

---

## 🛠️ INSTALACIÓN RÁPIDA

### 1. Ejecutar Instalador Automático
```bash
python instalar_sistema.py
```

### 2. Configurar Base de Datos
```bash
python configuracion_bd_local.py
```

### 3. Ejecutar Sistema
```bash
python main_offline.py
```

---

## ⚙️ CONFIGURACIÓN MANUAL

### 1. Configurar Base de Datos Local

Edita el archivo `config_bd.py`:

```python
# Configuración para base de datos LOCAL
DB_CONFIG_LOCAL = {
    'host': 'localhost',
    'user': 'root',                    # Tu usuario de MySQL
    'password': 'tu_contraseña',       # Tu contraseña de MySQL
    'database': 'gestion_empresas',    # Nombre de tu BD
    'port': 3306
}

# Cambiar a True para usar BD local
USAR_BD_LOCAL = True
```

### 2. Crear Base de Datos en MySQL

```sql
CREATE DATABASE gestion_empresas;
USE gestion_empresas;
```

### 3. Ejecutar Script de Creación de Tablas

```bash
python configuracion_bd_local.py
```

---

## 🔑 USUARIOS POR DEFECTO

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin   | admin123   | Administrador |

---

## 📊 ESTRUCTURA DE BASE DE DATOS

### Tablas Creadas:
- ✅ `usuarios` - Usuarios del sistema
- ✅ `productos` - Catálogo de productos
- ✅ `clientes` - Base de clientes
- ✅ `ventas` - Registro de ventas
- ✅ `detalle_ventas` - Detalle de productos vendidos
- ✅ `auditoria` - Historial de cambios
- ✅ `configuracion_sistema` - Configuración
- ✅ `notificaciones` - Sistema de notificaciones

---

## 🔄 MODOS DE FUNCIONAMIENTO

### Modo Local (Recomendado)
- ✅ Base de datos: `gestion_empresas` (MySQL local)
- ✅ Respaldo automático: `offline_backup.db` (SQLite)
- ✅ Sincronización: Manual con Railway

### Modo Remoto
- ✅ Base de datos: `railway` (Railway)
- ✅ Sincronización: Automática
- ✅ Respaldo: En la nube

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "No se pudo conectar a MySQL"
1. Verifica que MySQL esté ejecutándose
2. Revisa las credenciales en `config_bd.py`
3. Asegúrate de que el usuario tenga permisos

### Error: "no such table: usuarios"
1. Ejecuta: `python configuracion_bd_local.py`
2. Verifica que la base de datos `gestion_empresas` exista
3. Confirma que las tablas se crearon correctamente

### Error: "ModuleNotFoundError"
1. Instala dependencias: `pip install mysql-connector-python Pillow`
2. Verifica que Python 3.7+ esté instalado

---

## 📁 ARCHIVOS IMPORTANTES

| Archivo | Descripción |
|---------|-------------|
| `main_offline.py` | Archivo principal del sistema |
| `config_bd.py` | Configuración de base de datos |
| `configuracion_bd_local.py` | Script de creación de tablas |
| `instalar_sistema.py` | Instalador automático |
| `configuracion.json` | Configuración del sistema |
| `offline_backup.db` | Respaldo local SQLite |

---

## 🎯 FUNCIONALIDADES

### ✅ Implementadas:
- 🏠 Dashboard con estadísticas
- 📦 Gestión de inventario con búsqueda avanzada
- 💰 Sistema de ventas completo
- 📊 Reportes y exportación
- 🔔 Sistema de notificaciones
- 🔄 Sincronización offline/online
- 🎨 Temas claro/oscuro
- 💾 Respaldos automáticos
- 🔍 Búsqueda avanzada
- 📤 Exportación a CSV/JSON

---

## 🚀 EJECUCIÓN

```bash
# Instalación completa
python instalar_sistema.py

# Solo configuración de BD
python configuracion_bd_local.py

# Ejecutar sistema
python main_offline.py
```

---

## 📞 SOPORTE

Si tienes problemas:

1. **Verifica MySQL:** Asegúrate de que esté ejecutándose
2. **Revisa credenciales:** En `config_bd.py`
3. **Ejecuta instalador:** `python instalar_sistema.py`
4. **Verifica tablas:** Ejecuta `python configuracion_bd_local.py`

---

## 🎉 ¡LISTO!

Una vez completada la instalación, el sistema estará listo para usar con:
- ✅ Base de datos local configurada
- ✅ Todas las tablas creadas
- ✅ Usuario administrador listo
- ✅ Sistema completamente funcional

**¡Disfruta tu nuevo sistema de gestión empresarial!** 🎊
