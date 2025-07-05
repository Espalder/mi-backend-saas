# 🚀 Sistema de Gestión Empresarial SaaS - Backend API

## 📋 Descripción

Backend API REST para el sistema de gestión empresarial SaaS, construido con FastAPI y soporte multi-tenant.

## 🏗️ Arquitectura

### Multi-Tenant (Multi-Empresa)
- Cada empresa tiene su propio `tenant_id` en todas las tablas
- Aislamiento completo de datos entre empresas
- Usuarios solo pueden acceder a datos de su empresa

### Tecnologías
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **MySQL**: Base de datos principal (Railway)
- **JWT**: Autenticación segura
- **Pydantic**: Validación de datos

## 🚀 Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Crear archivo `.env` con:
```env
DB_HOST=hopper.proxy.rlwy.net
DB_USER=root
DB_PASSWORD=bLFNXiHRbOvKNRHbMPwZXJPeCmjGTAtK
DB_NAME=railway
DB_PORT=57218
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion
```

### 3. Migrar datos existentes
```bash
python migrate_data.py
```

### 4. Ejecutar el servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Endpoints de la API

### Autenticación
- `POST /api/auth/login` - Login con form data
- `POST /api/auth/login-json` - Login con JSON

### Empresas
- `GET /api/empresas/` - Listar empresas (solo admin)
- `GET /api/empresas/{id}` - Obtener empresa
- `POST /api/empresas/` - Crear empresa (solo admin)

### Usuarios
- `GET /api/usuarios/` - Listar usuarios de la empresa
- `GET /api/usuarios/{id}` - Obtener usuario
- `POST /api/usuarios/` - Crear usuario

### Productos
- `GET /api/productos/` - Listar productos de la empresa
- `GET /api/productos/{id}` - Obtener producto
- `POST /api/productos/` - Crear producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto

### Clientes
- `GET /api/clientes/` - Listar clientes de la empresa
- `GET /api/clientes/{id}` - Obtener cliente
- `POST /api/clientes/` - Crear cliente
- `PUT /api/clientes/{id}` - Actualizar cliente

### Ventas
- `GET /api/ventas/` - Listar ventas de la empresa
- `GET /api/ventas/{id}` - Obtener venta
- `POST /api/ventas/` - Crear venta

## 🔐 Autenticación

### Obtener Token
```bash
curl -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Usar Token
```bash
curl -X GET "http://localhost:8000/api/productos/" \
  -H "Authorization: Bearer tu_token_aqui"
```

## 📊 Documentación Automática

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏢 Estructura Multi-Tenant

### Tablas con tenant_id:
- `empresas` - Información de empresas
- `usuarios` - Usuarios por empresa
- `productos` - Productos por empresa
- `clientes` - Clientes por empresa
- `ventas` - Ventas por empresa
- `detalle_ventas` - Detalles de ventas

### Ejemplo de aislamiento:
```sql
-- Empresa A
SELECT * FROM productos WHERE empresa_id = 1;

-- Empresa B  
SELECT * FROM productos WHERE empresa_id = 2;
```

## 🔧 Desarrollo

### Estructura del proyecto:
```
backend_saas/
├── app/
│   ├── api/           # Endpoints de la API
│   ├── models/        # Modelos de base de datos
│   ├── schemas/       # Esquemas Pydantic
│   ├── services/      # Lógica de negocio
│   └── utils/         # Utilidades
├── config.py          # Configuración
├── main.py           # Aplicación principal
├── migrate_data.py   # Script de migración
└── requirements.txt  # Dependencias
```

## 🚀 Próximos pasos

1. **Frontend Web**: Crear interfaz web con React/Vue.js
2. **Sistema de Suscripciones**: Implementar planes y pagos
3. **Notificaciones**: WebSockets para tiempo real
4. **Reportes**: Endpoints para reportes avanzados
5. **Backup**: Sistema de respaldo automático

## 📞 Soporte

Para dudas o problemas, revisar:
1. Logs del servidor
2. Documentación en `/docs`
3. Estado de la base de datos
4. Configuración de variables de entorno 