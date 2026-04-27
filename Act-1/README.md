# Sistema de Gestión Empresarial Modular

## ¿Qué es?
Un sistema de gestión empresarial con control de inventario, ventas, reportes y configuración, separado en módulos según el rol del usuario (admin, vendedor, inventario), con soporte de modo claro y oscuro.

---

## ¿Cómo se usa?

### 1. **Ejecución**
- Abre una terminal en la carpeta del proyecto.
- Ejecuta:
  ```bash
  python sistema_gestion_mejorado_modulos/main.py
  ```

### 2. **Inicio de sesión**
- Ingresa tu usuario y contraseña (según la tabla `usuarios` de la base de datos).
- El sistema detecta tu rol y muestra solo las pestañas y funciones permitidas.

### 3. **Módulos disponibles según el rol**
- **admin**: Acceso total (Inventario, Ventas, Reportes, Configuración)
- **vendedor**: Ventas y Reportes
- **inventario**: Inventario y Reportes

### 4. **Modo claro/oscuro**
- Por defecto, el sistema inicia en modo claro.
- Si eres admin, puedes cambiar el tema desde la pestaña "Configuración".
- El cambio de tema es inmediato y afecta a toda la interfaz.

### 5. **Gestión de productos (Inventario)**
- Agrega, actualiza, elimina y consulta productos.
- Visualiza alertas de stock bajo.

### 6. **Gestión de ventas**
- Registra ventas, selecciona productos y clientes.
- Consulta ventas recientes y detalles.

### 7. **Reportes**
- Genera reportes de ventas y productos vendidos por periodo.
- Visualiza dashboard con métricas clave.

### 8. **Configuración**
- Cambia datos de la empresa, nivel de alerta de stock y tema visual (solo admin).
- Realiza respaldos y restauraciones simuladas.

---

## **Estructura de carpetas y archivos**

- `main.py`: Punto de entrada del sistema.
- `modulo_autenticacion.py`: Login y gestión de roles.
- `modulo_inventario.py`: Inventario y productos.
- `modulo_ventas.py`: Ventas y detalle de ventas.
- `modulo_reportes.py`: Reportes y dashboard.
- `modulo_configuracion.py`: Configuración y modo claro/oscuro.
- `estilos.py`: Estilos visuales y gestión de temas.
- `__init__.py`: Inicializa el paquete.

---

## **Requisitos**
- Python 3.x
- Paquetes: `tkinter`, `mysql-connector-python`, `Pillow`
- Base de datos MySQL con la estructura y usuarios definidos en el script de instalación.

---

## **Notas**
- El sistema es modular y fácil de ampliar.
- Si tienes dudas o necesitas soporte, consulta este documento o contacta al administrador del sistema. 