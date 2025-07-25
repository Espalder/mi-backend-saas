-- Agregar columnas de fechas a las tablas principales para compatibilidad con el backend SaaS

-- USUARIOS
ALTER TABLE usuarios
ADD COLUMN fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN fecha_actualizacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- PRODUCTOS
ALTER TABLE productos
ADD COLUMN fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN fecha_actualizacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- CLIENTES
ALTER TABLE clientes
ADD COLUMN fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN fecha_actualizacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- VENTAS
ALTER TABLE ventas
ADD COLUMN fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN fecha_actualizacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- DETALLE_VENTAS
ALTER TABLE detalle_ventas
ADD COLUMN fecha_creacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN fecha_actualizacion TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP; 