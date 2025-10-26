from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection
from pydantic import BaseModel

class Producto(BaseModel):
    nombre_producto: str
    precio_venta: float
    precio_costo: float
    jerarquia: str
    estado_producto: bool
    id_jerarquia: int



app = FastAPI(
    title="CaffeFlux API ☕",
    description="API del sistema de pedidos, productos y mesas del proyecto CaffeFlux.",
    version="1.0.0"
)

# =====================================================
# 🌐 CORS (para permitir conexión con el frontend React)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://localhost:3000", "https://tu-frontend-en-render.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# 🏠 Raíz
# =====================================================
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de CaffeFlux conectada a PostgreSQL ✅"}

# =====================================================
# 📦 PRODUCTOS
# =====================================================
@app.get("/api/productos")
def ver_productos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

@app.post("/api/productos")
def agregar_producto(producto: Producto):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO productos 
            (nombre_producto, precio_venta, precio_costo, jerarquia, estado_producto, id_jerarquia)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_producto;
            """,
            (
                producto.nombre_producto,
                producto.precio_venta,
                producto.precio_costo,
                producto.jerarquia,
                producto.estado_producto,
                producto.id_jerarquia
            )
        )
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        return {"id_producto": nuevo_id, **producto.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar producto: {e}")
    finally:
        cur.close()
        conn.close()


@app.put("/api/productos/{producto_id}")
def editar_producto(producto_id: int, producto: Producto):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s;", (producto_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    cur.execute(
        "UPDATE productos SET nombre=%s, precio=%s, descripcion=%s WHERE id=%s;",
        (producto.nombre, producto.precio, producto.descripcion, producto_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"id": producto_id, **producto.dict()}

@app.delete("/api/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s;", (producto_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    cur.execute("DELETE FROM productos WHERE id=%s;", (producto_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Producto eliminado", "id": producto_id}

# =====================================================
# 🍽️ MESAS
# =====================================================
@app.get("/api/mesas")
def ver_mesas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mesas;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# =====================================================
# 🧾 PEDIDOS
# =====================================================
@app.get("/api/pedidos")
def ver_pedidos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pedidos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# =====================================================
# 📋 LÍNEAS DE PEDIDO
# =====================================================
@app.get("/api/lineas_pedido")
def ver_lineas_pedido():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lineaspedido;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# =====================================================
# 💰 PAGOS
# =====================================================
@app.get("/api/pagos")
def ver_pagos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# =====================================================
# 👨‍🍳 TURNOS
# =====================================================
@app.get("/api/turnos")
def ver_turnos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turnos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# =====================================================
# 🧭 JERARQUÍA DE PRODUCTOS
# =====================================================
@app.get("/api/jerarquia")
def ver_jerarquia():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jerarquiaproductos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos
