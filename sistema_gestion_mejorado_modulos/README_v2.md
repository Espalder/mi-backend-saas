# Sistema de Gestión Empresarial Mejorado v2.0 🚀

Sistema completo de gestión empresarial con módulos independientes, gráficos avanzados y funcionalidades modernas.

## ✨ Nuevas Características v2.0

### 🎨 **Cambio de Tema sin Reinicio**
- Cambio instantáneo entre temas claro y oscuro
- Aplicación inmediata sin necesidad de reiniciar
- Persistencia automática de preferencias

### 📊 **Gráficos Estadísticos Avanzados**
- Gráficos de barras para análisis de ventas por fecha
- Gráficos de torta para productos más vendidos
- Visualización interactiva con matplotlib
- Múltiples pestañas de visualización

### 📄 **Generación de PDFs Profesionales**
- Reportes de ventas en formato PDF
- Diseño profesional con encabezados y pie de página
- Tablas estructuradas con datos detallados
- Apertura automática del PDF generado

### ⚡ **Optimizaciones de Rendimiento**
- Actualización asíncrona del dashboard
- Sincronización silenciosa en segundo plano
- Monitor de conexión optimizado (30s en lugar de 10s)
- Mejor manejo de errores y excepciones

### 🔄 **Modo Híbrido Online/Offline Mejorado**
- Sincronización bidireccional automática
- Notificaciones discretas de estado
- Compatibilidad completa SQLite/MySQL
- Recuperación automática de conexión

## 📋 Características Principales

- **Arquitectura Modular**: Módulos independientes para inventario, ventas, reportes y configuración
- **Autenticación Robusta**: Sistema de login con roles y permisos granulares
- **Dual Database**: Compatible con MySQL (online) y SQLite (offline)
- **Interfaz Moderna**: Diseño responsive con temas personalizables
- **Reportes Avanzados**: Generación de reportes con gráficos y exportación PDF
- **Configuración Flexible**: Configuración centralizada con persistencia

## 🗂️ Estructura del Proyecto

```
sistema_gestion_mejorado_modulos/
├── main.py                     # Punto de entrada estándar
├── main_offline.py            # Versión híbrida online/offline
├── estilos.py                 # Sistema de temas y estilos
├── generador_pdf.py           # ✨ Generación de PDFs profesionales
├── graficos_estadisticas.py   # ✨ Gráficos interactivos
├── instalar_dependencias.py   # ✨ Instalador automático
├── modulo_autenticacion.py    # Sistema de autenticación
├── modulo_inventario.py       # Gestión de productos e inventario
├── modulo_ventas.py           # Procesamiento de ventas
├── modulo_reportes.py         # ✨ Reportes con gráficos y PDF
├── modulo_configuracion.py    # ✨ Configuración con cambio dinámico
├── requirements.txt           # ✨ Dependencias del proyecto
├── configuracion.json         # Archivo de configuración
└── README.md                  # Documentación completa
```

## ⚙️ Requisitos del Sistema

- **Python**: 3.6 o superior
- **Sistema Operativo**: Windows, Linux, macOS
- **RAM**: 512MB mínimo (1GB recomendado)
- **Disco**: 100MB de espacio libre

### 📦 Dependencias

```
mysql-connector-python==8.2.0  # Conexión MySQL
reportlab==4.0.4               # Generación de PDFs
matplotlib==3.8.2              # Gráficos estadísticos
numpy==1.26.2                  # Cálculos matemáticos
Pillow==10.1.0                 # Procesamiento de imágenes
python-dateutil==2.8.2         # Manejo de fechas
```

## 🚀 Instalación Rápida

### Opción 1: Instalador Automático (Recomendado)
```bash
# Ejecutar el instalador automático
python instalar_dependencias.py

# En Windows también puedes usar:
# instalar_dependencias.bat

# En Linux/Mac también puedes usar:
# ./instalar_dependencias.sh
```

### Opción 2: Instalación Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el sistema
python main_offline.py  # Versión recomendada con modo híbrido
```

## 🎯 Guía de Uso

### 1. **Primer Inicio**
- Ejecuta `python main_offline.py`
- Usa las credenciales por defecto (ver tabla abajo)
- El sistema creará automáticamente la base de datos local

### 2. **Gestión de Inventario**
- Añadir, editar y eliminar productos
- Control de stock con alertas automáticas
- Búsqueda avanzada y filtros

### 3. **Procesamiento de Ventas**
- Selección de productos con búsqueda rápida
- Cálculo automático de totales y descuentos
- Gestión de clientes integrada

### 4. **Reportes y Analytics** ✨
- Dashboard en tiempo real con métricas clave
- Gráficos de barras para análisis temporal
- Gráficos de torta para productos top
- Exportación a PDF con un clic

### 5. **Configuración del Sistema**
- Cambio de tema instantáneo (claro/oscuro)
- Configuración de datos de empresa
- Respaldo y restauración de datos

## 👥 Usuarios Predeterminados

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| admin | admin123 | Administrador | Acceso completo |
| vendedor | venta123 | Vendedor | Ventas y reportes |
| inventario | stock123 | Inventario | Inventario y reportes |

## 🎨 Temas Disponibles

### Tema Claro (Por Defecto)
- Colores claros y profesionales
- Alto contraste para mejor legibilidad
- Ideal para uso durante el día

### Tema Oscuro
- Colores oscuros que reducen fatiga visual
- Perfecto para trabajo nocturno
- Cambio instantáneo sin reinicio ✨

## 📊 Nuevos Tipos de Reportes

### 1. **Reporte de Texto Tradicional**
- Formato de texto estructurado
- Ideal para revisión rápida
- Exportable a PDF

### 2. **Gráfico de Barras de Ventas** ✨
- Visualización de ventas por fecha
- Análisis de tendencias temporales
- Interactivo con matplotlib

### 3. **Gráfico de Torta de Productos** ✨
- Distribución de productos más vendidos
- Porcentajes automáticos
- Colores distintivos por categoría

### 4. **Exportación PDF Profesional** ✨
- Diseño corporativo con encabezados
- Tablas estructuradas con datos
- Apertura automática del archivo

## ⚡ Optimizaciones de Rendimiento

### Mejoras Implementadas:
- **Dashboard Asíncrono**: Actualización sin bloqueos
- **Consultas Optimizadas**: Mejor rendimiento de base de datos
- **Sincronización Inteligente**: Solo cuando hay cambios
- **Monitor de Conexión Eficiente**: Menor frecuencia de chequeos
- **Notificaciones Discretas**: No interrumpen el flujo de trabajo

## 🔧 Configuración Avanzada

### Archivo `configuracion.json`:
```json
{
  "nombre_empresa": "Tu Empresa S.A.",
  "direccion_empresa": "Av. Principal 123, Ciudad",
  "telefono_empresa": "+51 123 456 789",
  "alerta_stock_config": 5,
  "tema": "claro"
}
```

### Base de Datos:
- **MySQL**: Para modo online (configurar credenciales en código)
- **SQLite**: Para modo offline (automático)
- **Sincronización**: Bidireccional automática

## 🐛 Solución de Problemas

### Error: Módulo no encontrado
```bash
# Ejecutar el instalador de dependencias
python instalar_dependencias.py
```

### Error: Base de datos
- Verifica las credenciales de MySQL
- El sistema creará SQLite automáticamente

### Error: Permisos
```bash
# En Linux/Mac, dar permisos:
chmod +x instalar_dependencias.sh
```

## 🤝 Contribución

1. **Fork** del proyecto
2. **Crear rama** para tu característica (`git checkout -b feature/NuevaCaracteristica`)
3. **Commit** cambios (`git commit -m 'Añadir nueva característica'`)
4. **Push** a la rama (`git push origin feature/NuevaCaracteristica`)
5. **Crear Pull Request**

## 📄 Changelog v2.0

### ✨ Añadido
- Gráficos estadísticos interactivos
- Generación de PDFs profesionales
- Cambio de tema sin reinicio
- Instalador automático de dependencias
- Sincronización silenciosa
- Notificaciones discretas

### 🔧 Mejorado
- Rendimiento general del sistema
- Compatibilidad SQLite/MySQL
- Manejo de errores robusto
- Interfaz de usuario más fluida
- Monitor de conexión optimizado

### 🐛 Corregido
- Errores de sincronización
- Problemas de tema dinámico
- Bloqueos en dashboard
- Compatibilidad de consultas SQL

## 📞 Soporte

- **Issues**: Para reportar bugs o solicitar características
- **Documentación**: README completo con ejemplos
- **Instalador**: Script automático para dependencias

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT** - ver archivo `LICENSE` para detalles.

---

### 🎉 ¡Disfruta del Sistema de Gestión Empresarial v2.0!

**Desarrollado con ❤️ para mejorar tu productividad empresarial**