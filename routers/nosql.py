# routers/nosql.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
from core.mongo import ventas_collection  # conexión ya configurada

router = APIRouter(prefix="/api/ventas", tags=["Ventas NoSQL"])

@router.post("/")
def registrar_venta(venta: dict):
    try:
        venta["fecha"] = datetime.now()
        result = ventas_collection.insert_one(venta)
        return {"id": str(result.inserted_id), "message": "✅ Venta registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar venta: {e}")
