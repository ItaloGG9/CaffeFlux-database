```sql
-- =====================
-- SEED: JerarquiaProductos
-- =====================
INSERT INTO JerarquiaProductos (nombre_jerarquia, id_categoria, id_subcategoria, estado)
VALUES 
('Bebidas', 1, NULL, TRUE),
('Comida Rápida', 2, NULL, TRUE),
('Postres', 3, NULL, TRUE);

-- =====================
-- SEED: Productos
-- =====================
INSERT INTO Productos (nombre_producto, precio_venta, precio_costo, jerarquia, estado_producto, id_jerarquia)
VALUES
('Coca Cola 350ml', 1200, 600, 'Bebidas', TRUE, 1),
('Hamburguesa Clásica', 3500, 2000, 'Comida Rápida', TRUE, 2),
('Helado Vainilla', 2000, 800, 'Postres', TRUE, 3);

-- =====================
-- SEED: Mesas
-- =====================
INSERT INTO Mesas (estado_mesa, hora_apertura, observaciones)
VALUES
('Disponible', NOW(), 'Mesa cerca de la ventana'),
('Ocupada', NOW(), 'Mesa en terraza');

-- =====================
-- SEED: Pedidos
-- =====================
INSERT INTO Pedidos (id_mesa, hora_creacion, metodo_pago, propina, descuento, total)
VALUES
(1, NOW(), 'Efectivo', 500, 0, 1700),
(2, NOW(), 'Tarjeta', 0, 200, 3300);

-- =====================
-- SEED: LineasPedido
-- =====================
INSERT INTO LineasPedido (id_pedido, id_producto)
VALUES
(1, 1), -- Coca Cola
(2, 2), -- Hamburguesa
(2, 3); -- Helado

-- =====================
-- SEED: Turnos
-- =====================
INSERT INTO Turnos (usuario_responsable, hora_apertura, fondo_inicial)
VALUES
('Juan Pérez', NOW(), 50000);

-- =====================
-- SEED: Pagos
-- =====================
INSERT INTO Pagos (id_pedido, metodo_pago, monto)
VALUES
(1, 'Efectivo', 1700),
(2, 'Tarjeta', 3300);
```
