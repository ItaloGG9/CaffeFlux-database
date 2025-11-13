from fastapi import APIRouter, HTTPException, Request
from core.database import get_db_connection
from core.mongo import db

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

# Colecciones Mongo usadas aquí
pagos_collection = db["pagos"]
turnos_collection = db["turnos"]

# GET /api/pagos/ — (tu versión original contra PostgreSQL)
@router.get("/")
def ver_pagos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos

# ✅ POST /api/pagos — guarda lo que envía el front en MongoDB
# Evita problemas de Pydantic: leemos el JSON “tal cual”
@router.post("")
@router.post("/")
async def crear_pago(request: Request):
    try:
        payload = await request.json()
        # (Opcional) calculamos total por si no viene
        if "total" not in payload and "productos" in payload:
            payload["total"] = sum(
                (p.get("precio_unitario", 0) * p.get("cantidad", 0))
                for p in payload["productos"]
            )
        res = pagos_collection.insert_one(payload)
        return {"message": "Pago guardado en MongoDB", "id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el pago: {e}")

# DELETE /api/pagos — borra todos los pagos en Mongo
@router.delete("/")
def borrar_todos_los_pagos():
    pagos_collection.delete_many({})
    return {"message": "Pagos eliminados"}

# DELETE /api/pagos/cerrados — borra turnos cerrados en Mongo
@router.delete("/cerrados")
def borrar_turnos_cerrados():
    turnos_collection.delete_many({"estado": "cerrado"})
    return {"message": "Turnos cerrados eliminados"}
