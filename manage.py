from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection

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
