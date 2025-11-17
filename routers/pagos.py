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
    try:
        payload = dict(payload)

        # Default solo si no viene nada
        metodo = payload.get("metodo_pago", "Efectivo")

        METODOS_VALIDOS = {"Efectivo", "Debito", "Transferencia"}
        if metodo not in METODOS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Metodo de pago inválido: {metodo}. Debe ser uno de: {', '.join(METODOS_VALIDOS)}"
            )

        payload["metodo_pago"] = metodo  # ya validado

        payload.setdefault("fecha_hora", datetime.utcnow().isoformat())
        payload.setdefault("total", 0)
        payload.setdefault("productos", [])

        res = pagos_collection.insert_one(payload)
        return {
            "ok": True,
            "message": "Pago guardado en Mongo",
            "id": str(res.inserted_id),
        }

    except HTTPException:
        # re-lanzamos las de validación
        raise
    except Exception as e:
        print("Error en crear_pago:", e)
        raise HTTPException(status_code=500, detail=f"Error al guardar el pago: {e}")


@router.get("")
@router.get("/")
def listar_pagos():
    docs = list(pagos_collection.find({}, {"_id": 0}))
    return docs

# ... (otras funciones como GET, POST) ...

# ===============================
# 🔹 Borrar TODOS los pagos/ventas
# Corresponde a DELETE /api/pagos
# ===============================
@router.delete("/")
def borrar_todos_los_pagos(db = Depends(get_mongodb_connection)):
    try:
        # Aquí 'pagos' es el nombre de tu colección
        resultado = db.pagos.delete_many({}) 
        
        if resultado.deleted_count == 0:
            # Aunque no haya pagos, se considera éxito en la limpieza
            return {"ok": True, "message": "No había pagos/ventas que eliminar. Limpieza exitosa.", "count": 0}

        return {
            "ok": True, 
            "message": f"{resultado.deleted_count} pagos/ventas eliminados correctamente.",
            "count": resultado.deleted_count
        }
    except Exception as e:
        print("❌ Error al borrar todos los pagos:", e)
        # 500 para error de servidor/DB
        raise HTTPException(status_code=500, detail=f"Error al vaciar la colección de pagos: {e}")
