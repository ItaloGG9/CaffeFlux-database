from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from typing import Any, Dict
from core.mongo import db  # usa tu conexión ya inicializada

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])
pagos_collection = db["pagos"]

# Acepta con y sin slash
@router.post("")
@router.post("/")
async def crear_pago(payload: Dict[str, Any]):
    """
    Guarda la venta tal cual llega desde el front en MongoDB.
    Evita Pydantic para no chocar con versiones y validadores.
    """
    try:
        # Normaliza algunos campos opcionales
        payload = dict(payload)
        payload.setdefault("fecha_hora", datetime.utcnow().isoformat())
        payload.setdefault("metodo_pago", "Efectivo")
        payload.setdefault("total", 0)
        payload.setdefault("productos", [])

        res = pagos_collection.insert_one(payload)
        return {"ok": True, "message": "Pago guardado en Mongo", "id": str(res.inserted_id)}
    except Exception as e:
        # imprime en logs de Render
        print("Error en crear_pago:", e)
        raise HTTPException(status_code=500, detail=f"Error al guardar el pago: {e}")

@router.get("")
@router.get("/")
def listar_pagos():
    docs = list(pagos_collection.find({}, {"_id": 0}))
    return docs
