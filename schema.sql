```sql
-- =====================
-- TABLA: JerarquiaProductos
-- =====================
CREATE TABLE JerarquiaProductos (
    id_jerarquia SERIAL PRIMARY KEY,
    nombre_jerarquia VARCHAR(255) NOT NULL,
    id_categoria INT,
    id_subcategoria INT,
    estado BOOLEAN
);

-- =====================
-- TABLA: Productos
-- =====================
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(255) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    precio_costo DECIMAL(10,2) NOT NULL,
    jerarquia VARCHAR(50),
    estado_producto BOOLEAN,
    id_jerarquia INT,
    CONSTRAINT fk_productos_jerarquia
        FOREIGN KEY (id_jerarquia) REFERENCES JerarquiaProductos(id_jerarquia)
);

-- =====================
-- TABLA: Mesas
-- =====================
CREATE TABLE Mesas (
    id_mesa SERIAL PRIMARY KEY,
    estado_mesa VARCHAR(50) NOT NULL,
    hora_apertura TIMESTAMP,
    hora_cierre TIMESTAMP,
    observaciones TEXT
);

-- =====================
-- TABLA: Pedidos
-- =====================
CREATE TABLE Pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_mesa INT NOT NULL,
    hora_creacion TIMESTAMP NOT NULL,
    metodo_pago VARCHAR(50),
    propina DECIMAL(10,2),
    descuento DECIMAL(10,2),
    total DECIMAL(10,2),
    CONSTRAINT fk_pedidos_mesa
        FOREIGN KEY (id_mesa) REFERENCES Mesas(id_mesa)
);

-- =====================
-- TABLA: LineasPedido
-- =====================
CREATE TABLE LineasPedido (
    id_linea SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    CONSTRAINT fk_lineas_pedido
        FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido),
    CONSTRAINT fk_lineas_producto
        FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- =====================
-- TABLA: Turnos
-- =====================
CREATE TABLE Turnos (
    id_turno SERIAL PRIMARY KEY,
    usuario_responsable VARCHAR(255) NOT NULL,
    hora_apertura TIMESTAMP NOT NULL,
    fondo_inicial DECIMAL(10,2) NOT NULL,
    hora_cierre TIMESTAMP,
    usuario_cierre VARCHAR(50)
);

-- =====================
-- TABLA: Pagos
-- =====================
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    metodo_pago VARCHAR(50),
    monto DECIMAL(10,2) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pagos_pedido
        FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido)
);
```
