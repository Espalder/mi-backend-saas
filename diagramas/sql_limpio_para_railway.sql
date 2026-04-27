-- Script limpio para importar en Railway

-- Elimina las vistas si existen
DROP VIEW IF EXISTS vista_productos_mas_vendidos;
DROP VIEW IF EXISTS vista_stock_bajo;
DROP VIEW IF EXISTS vista_ventas_diarias;

-- Elimina las tablas si existen
DROP TABLE IF EXISTS detalle_ventas;
DROP TABLE IF EXISTS detalle_compras;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS historial;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS proveedores;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS configuracion;

-- 1. categorias
CREATE TABLE categorias (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion text COLLATE utf8mb4_unicode_ci,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO categorias VALUES
(1,'Electrónicos','Productos electrónicos y dispositivos','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(2,'Alimentos','Comestibles y bebidas','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(3,'Papelería','Artículos de oficina y papelería','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(4,'Limpieza','Productos de limpieza y hogar','2025-06-21 23:07:25','2025-06-21 23:07:25');

-- 2. clientes
CREATE TABLE clientes (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  nit varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  telefono varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  direccion text COLLATE utf8mb4_unicode_ci,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO clientes VALUES
(1,'Consumidor Final','CF',NULL,NULL,NULL,'2025-06-21 23:07:25','2025-06-21 23:07:25'),
(2,'Empresa ABC SA','123456-7','2222-3333','compras@empresaabc.com','123 Calle Comercial, Zona 1','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(3,'Tienda XYZ','987654-3','4444-5555','pedidos@tiendaxyz.com','456 Avenida Norte, Zona 2','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(4,'Jose',NULL,NULL,NULL,NULL,'2025-06-22 02:36:52','2025-06-22 02:36:52'),
(5,'Daniel',NULL,NULL,NULL,NULL,'2025-06-22 03:46:53','2025-06-22 03:46:53'),
(6,'Carlos',NULL,NULL,NULL,NULL,'2025-06-24 06:34:48','2025-06-24 06:34:48'),
(7,'Cris',NULL,NULL,NULL,NULL,'2025-06-24 06:39:25','2025-06-24 06:39:25'),
(8,'Doris',NULL,NULL,NULL,NULL,'2025-06-24 06:50:29','2025-06-24 06:50:29'),
(9,'Juaquin',NULL,NULL,NULL,NULL,'2025-06-24 06:51:50','2025-06-24 06:51:50');

-- 3. proveedores
CREATE TABLE proveedores (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  contacto varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  telefono varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  direccion text COLLATE utf8mb4_unicode_ci,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO proveedores VALUES
(1,'Distribuidora Electrónica SA','Juan Pérez','5555-1234','ventas@electronicasa.com','456 Avenida Norte, Ciudad','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(2,'Alimentos del Valle','María Gómez','5555-5678','pedidos@alimentosvalle.com','789 Calle Oriente, Ciudad','2025-06-21 23:07:25','2025-06-21 23:07:25'),
(3,'Suministros de Oficina','Carlos Rodríguez','5555-9012','info@suministros.com','321 Boulevard Sur, Ciudad','2025-06-21 23:07:25','2025-06-21 23:07:25');

-- 4. configuracion
CREATE TABLE configuracion (
  id int NOT NULL AUTO_INCREMENT,
  nombre_empresa varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  direccion text COLLATE utf8mb4_unicode_ci,
  telefono varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  moneda varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'Q',
  logo varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  iva decimal(5,2) DEFAULT '12.00',
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO configuracion VALUES
(1,'Mi Pequeña Empresa','123 Calle Principal, Ciudad','1234-5678','contacto@miempresa.com','Q',NULL,12.00,'2025-06-21 23:07:25','2025-06-21 23:07:25');

-- 5. usuarios
CREATE TABLE usuarios (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  password varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  email varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  rol enum('admin','vendedor','inventario') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'vendedor',
  activo tinyint(1) DEFAULT '1',
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO usuarios VALUES
(1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','Administrador','admin@miempresa.com','admin',1,'2025-06-21 23:07:25','2025-06-21 23:07:25'),
(2,'vendedor1','8ef6624812728dec98e81a11d1ffd3c19d21f95ccc8103a858b8e2de147a788a','Juan Vendedor','juan@miempresa.com','vendedor',1,'2025-06-21 23:07:25','2025-06-21 23:07:25'),
(3,'inventario1','35de1a09ec425493170e5b83380e4fd5fba692fc2e6b48f2b9c042644bcfef74','María Inventario','maria@miempresa.com','inventario',1,'2025-06-21 23:07:25','2025-06-21 23:07:25');

-- 6. productos
CREATE TABLE productos (
  id int NOT NULL AUTO_INCREMENT,
  codigo varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion text COLLATE utf8mb4_unicode_ci,
  precio decimal(10,2) NOT NULL,
  precio_compra decimal(10,2) NOT NULL,
  precio_venta decimal(10,2) NOT NULL,
  stock int NOT NULL DEFAULT '0',
  stock_minimo int NOT NULL DEFAULT '5',
  categoria_id int DEFAULT NULL,
  proveedor_id int DEFAULT NULL,
  activo tinyint(1) DEFAULT '1',
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY codigo (codigo),
  KEY categoria_id (categoria_id),
  KEY proveedor_id (proveedor_id),
  CONSTRAINT productos_ibfk_1 FOREIGN KEY (categoria_id) REFERENCES categorias (id),
  CONSTRAINT productos_ibfk_2 FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO productos VALUES
(1,'PROD-001','Teclado USB','Teclado ergonómico con conexión USB',75.00,50.00,75.00,49,5,1,1,1,'2025-06-21 23:07:25','2025-06-24 06:39:25'),
(2,'PROD-002','Mouse Inalámbrico','Mouse óptico sin cables',63.00,40.00,60.00,49,5,1,1,1,'2025-06-21 23:07:25','2025-06-24 06:39:25'),
(3,'PROD-003','Arroz 1kg','Arroz blanco grano largo',7.50,5.00,7.50,78,20,2,2,1,'2025-06-21 23:07:25','2025-06-24 06:50:29'),
(4,'PROD-004','Frijol 1kg','Frijol negro',9.00,6.00,9.00,78,15,2,2,1,'2025-06-21 23:07:25','2025-06-24 06:34:48'),
(5,'PROD-005','Cuaderno Profesional','Cuaderno de 100 hojas rayado',22.50,15.00,22.50,10,10,3,3,1,'2025-06-21 23:07:25','2025-06-24 06:50:29'),
(6,'PROD-006','Bolígrafos x12','Paquete de 12 bolígrafos azules',12.00,8.00,12.00,59,15,3,3,1,'2025-06-21 23:07:25','2025-06-22 03:22:13'),
(7,'PROD-007','Detergente 1L','Detergente líquido para ropa',18.00,12.00,18.00,49,10,4,3,1,'2025-06-21 23:07:25','2025-06-24 06:50:29'),
(8,'PROD-008','Cloro 1L','Cloro para desinfección',9.00,6.00,9.00,79,8,4,3,1,'2025-06-21 23:07:25','2025-06-24 06:39:25'),
(9,'PROD-009','Arroz 15kg','Arroz blanco grano largo',50.00,50.00,50.00,100,50,2,2,1,'2025-06-22 02:36:32','2025-06-23 15:13:41'),
(10,'PROD-010','Arroz 49kg','Arroz blanco grano largo',150.00,150.00,150.00,74,50,2,2,1,'2025-06-22 02:38:25','2025-06-24 06:51:50'),
(11,'PROD-011','Papa 1kg','Papa blanca',4.50,4.50,4.50,78,80,2,2,1,'2025-06-22 03:21:26','2025-06-23 15:13:48'),
(12,'PROD-012','Papa 10kg','Papa Yungay',40.00,40.00,40.00,50,50,NULL,NULL,1,'2025-06-24 06:10:59','2025-06-24 06:10:59'),
(13,'PROD-013','Cloro 2L','Cloro para desinfección',17.00,17.00,17.00,49,50,NULL,NULL,1,'2025-06-24 06:18:28','2025-06-24 06:34:48');

-- 7. ventas
CREATE TABLE ventas (
  id int NOT NULL AUTO_INCREMENT,
  fecha datetime NOT NULL,
  cliente_id int DEFAULT NULL,
  usuario_id int NOT NULL,
  subtotal decimal(10,2) NOT NULL,
  descuento decimal(10,2) DEFAULT '0.00',
  total decimal(10,2) NOT NULL,
  estado enum('pendiente','completada','cancelada') COLLATE utf8mb4_unicode_ci DEFAULT 'completada',
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY cliente_id (cliente_id),
  KEY usuario_id (usuario_id),
  CONSTRAINT ventas_ibfk_1 FOREIGN KEY (cliente_id) REFERENCES clientes (id),
  CONSTRAINT ventas_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO ventas VALUES
(1,'2025-06-21 21:36:52',4,1,59.00,0.00,59.00,'completada','2025-06-22 02:36:52','2025-06-22 02:36:52'),
(2,'2025-06-21 22:22:13',4,1,189.00,0.00,189.00,'completada','2025-06-22 03:22:13','2025-06-22 03:22:13'),
(3,'2025-06-21 22:46:53',5,1,168.00,0.00,168.00,'completada','2025-06-22 03:46:53','2025-06-22 03:46:53'),
(4,'2025-06-24 01:34:48',6,1,176.00,0.00,176.00,'completada','2025-06-24 06:34:48','2025-06-24 06:34:48'),
(5,'2025-06-24 01:39:25',7,1,294.00,0.00,294.00,'completada','2025-06-24 06:39:25','2025-06-24 06:39:25'),
(6,'2025-06-24 01:50:29',8,1,55.50,0.00,55.50,'completada','2025-06-24 06:50:29','2025-06-24 06:50:29'),
(7,'2025-06-24 01:51:50',9,1,300.00,0.00,300.00,'completada','2025-06-24 06:51:50','2025-06-24 06:51:50');

-- 8. compras
CREATE TABLE compras (
  id int NOT NULL AUTO_INCREMENT,
  fecha datetime NOT NULL,
  proveedor_id int DEFAULT NULL,
  usuario_id int NOT NULL,
  total decimal(10,2) NOT NULL,
  observaciones text COLLATE utf8mb4_unicode_ci,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY proveedor_id (proveedor_id),
  KEY usuario_id (usuario_id),
  CONSTRAINT compras_ibfk_1 FOREIGN KEY (proveedor_id) REFERENCES proveedores (id),
  CONSTRAINT compras_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. historial
CREATE TABLE historial (
  id int NOT NULL AUTO_INCREMENT,
  usuario_id int DEFAULT NULL,
  accion varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  tabla_afectada varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  registro_id int DEFAULT NULL,
  detalles text COLLATE utf8mb4_unicode_ci,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY usuario_id (usuario_id),
  CONSTRAINT historial_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. detalle_compras
CREATE TABLE detalle_compras (
  id int NOT NULL AUTO_INCREMENT,
  compra_id int NOT NULL,
  producto_id int NOT NULL,
  cantidad int NOT NULL,
  precio_unitario decimal(10,2) NOT NULL,
  subtotal decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY compra_id (compra_id),
  KEY producto_id (producto_id),
  CONSTRAINT detalle_compras_ibfk_1 FOREIGN KEY (compra_id) REFERENCES compras (id),
  CONSTRAINT detalle_compras_ibfk_2 FOREIGN KEY (producto_id) REFERENCES productos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. detalle_ventas
CREATE TABLE detalle_ventas (
  id int NOT NULL AUTO_INCREMENT,
  venta_id int NOT NULL,
  producto_id int NOT NULL,
  cantidad int NOT NULL,
  precio_unitario decimal(10,2) NOT NULL,
  subtotal decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY venta_id (venta_id),
  KEY producto_id (producto_id),
  CONSTRAINT detalle_ventas_ibfk_1 FOREIGN KEY (venta_id) REFERENCES ventas (id),
  CONSTRAINT detalle_ventas_ibfk_2 FOREIGN KEY (producto_id) REFERENCES productos (id)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vistas
DROP VIEW IF EXISTS vista_productos_mas_vendidos;
CREATE ALGORITHM=UNDEFINED VIEW vista_productos_mas_vendidos AS
SELECT
    p.id AS id,
    p.codigo AS codigo,
    p.nombre AS nombre,
    SUM(dv.cantidad) AS total_vendido,
    SUM(dv.subtotal) AS monto_total
FROM
    detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    JOIN ventas v ON dv.venta_id = v.id
WHERE
    v.estado = 'completada'
GROUP BY
    p.id, p.codigo, p.nombre
ORDER BY
    total_vendido DESC;

DROP VIEW IF EXISTS vista_stock_bajo;
CREATE ALGORITHM=UNDEFINED VIEW vista_stock_bajo AS
SELECT
    p.id AS id,
    p.codigo AS codigo,
    p.nombre AS nombre,
    p.stock AS stock,
    p.stock_minimo AS stock_minimo,
    c.nombre AS categoria,
    pr.nombre AS proveedor
FROM
    productos p
    LEFT JOIN categorias c ON p.categoria_id = c.id
    LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
WHERE
    p.stock <= p.stock_minimo
    AND p.activo = TRUE;

DROP VIEW IF EXISTS vista_ventas_diarias;
CREATE ALGORITHM=UNDEFINED VIEW vista_ventas_diarias AS
SELECT
    CAST(v.fecha AS DATE) AS fecha,
    COUNT(0) AS total_ventas,
    SUM(v.total) AS monto_total,
    AVG(v.total) AS promedio_venta
FROM
    ventas v
WHERE
    v.estado = 'completada'
GROUP BY
    CAST(v.fecha AS DATE); 