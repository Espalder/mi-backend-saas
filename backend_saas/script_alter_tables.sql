-- Script para agregar columnas faltantes a las tablas

-- Agregar columna activo a la tabla clientes
ALTER TABLE clientes ADD COLUMN activo BOOLEAN DEFAULT TRUE;

-- Agregar columna numero_factura a la tabla ventas
ALTER TABLE ventas ADD COLUMN numero_factura VARCHAR(50) NULL;

-- Actualizar registros existentes
UPDATE clientes SET activo = TRUE WHERE activo IS NULL;
UPDATE ventas SET numero_factura = CONCAT('FAC-', LPAD(id, 6, '0')) WHERE numero_factura IS NULL; 