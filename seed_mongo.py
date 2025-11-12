from core.mongo import db
from datetime import datetime

# Jerarquías
db["JerarquiaProductos"].insert_many([
    {"nombre_jerarquia": "Bebidas", "id_categoria": 1, "estado": True},
    {"nombre_jerarquia": "Comida Rápida", "id_categoria": 2, "estado": True},
    {"nombre_jerarquia": "Postres", "id_categoria": 3, "estado": True}
])

# Productos
db["Productos"].insert_many([
    {"nombre_producto": "Coca Cola 350ml", "precio_venta": 1200, "precio_costo": 600, "jerarquia": "Bebidas", "estado_producto": True},
    {"nombre_producto": "Hamburguesa Clásica", "precio_venta": 3500, "precio_costo": 2000, "jerarquia": "Comida Rápida", "estado_producto": True},
    {"nombre_producto": "Helado Vainilla", "precio_venta": 2000, "precio_costo": 800, "jerarquia": "Postres", "estado_producto": True}
])

# Mesas
db["Mesas"].insert_many([
    {"estado_mesa": "Disponible", "hora_apertura": datetime.now(), "observaciones": "Mesa cerca de la ventana"},
    {"estado_mesa": "Ocupada", "hora_apertura": datetime.now(), "observaciones": "Mesa en terraza"}
])

# Turnos
db["Turnos"].insert_one({
    "usuario_responsable": "Juan Pérez",
    "hora_apertura": datetime.now(),
    "fondo_inicial": 50000
})

# Pagos (ejemplo)
db["Pagos"].insert_many([
    {"id_pedido": 1, "metodo_pago": "Efectivo", "monto": 1700, "fecha_hora": datetime.now()},
    {"id_pedido": 2, "metodo_pago": "Tarjeta", "monto": 3300, "fecha_hora": datetime.now()}
])

print("✅ Datos insertados correctamente en MongoDB")
