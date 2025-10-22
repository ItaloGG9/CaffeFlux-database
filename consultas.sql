```sql
-- =====================
-- CONSULTAS DE EJEMPLO
-- =====================

-- 1. Listar todos los productos disponibles
SELECT * FROM Productos WHERE estado_producto = TRUE;

-- 2. Ver los pedidos con detalle de mesa y productos
SELECT p.id_pedido, m.estado_mesa, pr.nombre_producto, lp.id_linea, p.total
FROM Pedidos p
JOIN Mesas m ON p.id_mesa = m.id_mesa
JOIN LineasPedido lp ON p.id_pedido = lp.id_pedido
JOIN Productos pr ON lp.id_producto = pr.id_producto;

-- 3. Calcular ventas totales del día
SELECT DATE(p.hora_creacion) AS fecha, SUM(pa.monto) AS total_ventas
FROM Pedidos p
JOIN Pagos pa ON p.id_pedido = pa.id_pedido
GROUP BY fecha;

-- 4. Ver pedidos con propina mayor a 0
SELECT id_pedido, total, propina
FROM Pedidos
WHERE propina > 0;

-- 5. Listar turnos abiertos (sin hora de cierre)
SELECT * FROM Turnos WHERE hora_cierre IS NULL;

-- 6. Productos más vendidos
SELECT pr.nombre_producto, COUNT(lp.id_producto) AS veces_vendido
FROM LineasPedido lp
JOIN Productos pr ON lp.id_producto = pr.id_producto
GROUP BY pr.nombre_producto
ORDER BY veces_vendido DESC;

-- 7. Mesas más utilizadas
SELECT m.id_mesa, COUNT(p.id_pedido) AS cantidad_pedidos
FROM Mesas m
JOIN Pedidos p ON m.id_mesa = p.id_mesa
GROUP BY m.id_mesa
ORDER BY cantidad_pedidos DESC;
```
