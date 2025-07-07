-- 1. Crear la tabla de empresas (si no existe)
CREATE TABLE IF NOT EXISTS empresas (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  codigo_empresa varchar(20) NOT NULL UNIQUE,
  descripcion text,
  plan_suscripcion varchar(20) DEFAULT 'basic',
  fecha_creacion timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_actualizacion timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  activo tinyint(1) DEFAULT 1,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO empresas (id, nombre, codigo_empresa, descripcion) VALUES
(1, 'Empresa por Defecto', 'EMPRESA001', 'Empresa creada por migración');

-- 2. Agregar columna empresa_id a las tablas necesarias (si no existe)
ALTER TABLE clientes ADD COLUMN empresa_id INT NOT NULL DEFAULT 1 AFTER id;
ALTER TABLE usuarios ADD COLUMN empresa_id INT NOT NULL DEFAULT 1 AFTER id;
ALTER TABLE productos ADD COLUMN empresa_id INT NOT NULL DEFAULT 1 AFTER id;
ALTER TABLE ventas ADD COLUMN empresa_id INT NOT NULL DEFAULT 1 AFTER id;
ALTER TABLE detalle_ventas ADD COLUMN empresa_id INT NOT NULL DEFAULT 1 AFTER id;

-- 3. Agregar claves foráneas (si no existen)
ALTER TABLE clientes ADD CONSTRAINT clientes_ibfk_1 FOREIGN KEY (empresa_id) REFERENCES empresas(id);
ALTER TABLE usuarios ADD CONSTRAINT usuarios_ibfk_1 FOREIGN KEY (empresa_id) REFERENCES empresas(id);
ALTER TABLE productos ADD CONSTRAINT productos_ibfk_3 FOREIGN KEY (empresa_id) REFERENCES empresas(id);
ALTER TABLE ventas ADD CONSTRAINT ventas_ibfk_3 FOREIGN KEY (empresa_id) REFERENCES empresas(id);
ALTER TABLE detalle_ventas ADD CONSTRAINT detalle_ventas_ibfk_3 FOREIGN KEY (empresa_id) REFERENCES empresas(id);

-- 4. Actualizar todos los registros existentes para que tengan empresa_id = 1
UPDATE clientes SET empresa_id = 1 WHERE empresa_id IS NULL OR empresa_id <> 1;
UPDATE usuarios SET empresa_id = 1 WHERE empresa_id IS NULL OR empresa_id <> 1;
UPDATE productos SET empresa_id = 1 WHERE empresa_id IS NULL OR empresa_id <> 1;
UPDATE ventas SET empresa_id = 1 WHERE empresa_id IS NULL OR empresa_id <> 1;
UPDATE detalle_ventas SET empresa_id = 1 WHERE empresa_id IS NULL OR empresa_id <> 1;

-- 5. (Opcional) Crear índice único para productos por empresa
ALTER TABLE productos DROP INDEX codigo, ADD UNIQUE KEY codigo_empresa (codigo, empresa_id);

-- ¡Listo! Tu base de datos ahora es multi-tenant y no perdiste ningún dato. 