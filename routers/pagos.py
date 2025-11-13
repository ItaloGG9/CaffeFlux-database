# routers/pagos.py
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from core.database import get_db_connection
from core.mongo import db  # 👈 conexión a MongoDB

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

# --- Colecciones Mongo
pagos_collection = db["pagos"]
turnos_collection = db["turnos"]  # por si usas el delete de abajo

# --------- MODELOS (compatibles con Pydantic v1) ---------
class ProductoPago(BaseModel):
    id_producto: int
    nombre: str
    cantidad: int
    precio_unitario: float

class PagoIn(BaseModel):
    id_mesa: int
    propina: float
    descuento: float
    total: float
    metodo_pago: str
    fecha_hora: str
    productos: List[ProductoPago]

# --------- ENDPOINTS ---------

# 1) POST (lo que llama tu botón) → guarda en MongoDB
@router.post("")     # /api/pagos
@router.post("/")    # /api/pagos/
def crear_pago(pago: PagoIn):
    try:
        doc = pago.dict()
        pagos_collection.insert_one(doc)
        return {"message": "✅ Pago registrado en MongoDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el pago: {e}")

# 2) GET (tu endpoint original que lee desde PostgreSQL)
@router.get("/")
def ver_pagos():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM pagos;")
        columnas = [desc[0] for desc in cur.description]
        datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
        return datos
    finally:
        cur.close()
        conn.close()

# 3) DELETE pagos en Mongo
@router.delete("/")
def borrar_todos_los_pagos():
    pagos_collection.delete_many({})
    return {"message": "Pagos eliminados"}

# 4) DELETE turnos cerrados en Mongo
@router.delete("/cerrados")
def borrar_turnos_cerrados():
    turnos_collection.delete_many({"estado": "cerrado"})
    return {"message": "Turnos cerrados eliminados"}
