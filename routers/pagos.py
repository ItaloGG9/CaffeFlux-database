from fastapi import APIRouter, HTTPException, Request, Depends # 🟢 CORRECCIÓN 1: AGREGADO Depends
from datetime import datetime
from typing import Any, Dict
from core.mongo import db  # usa tu conexión ya inicializada

# ⚠️ NOTA: Necesitas también importar get_mongodb_connection si lo usas en otros archivos,
# pero para este endpoint de DELETE, usaremos la colección global.
# from core.database import get_mongodb_connection 

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])
pagos_collection = db["pagos"] # Colección global que usaremos


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
    # Incluimos _id si el Frontend lo necesita, sino lo quitamos como antes
    docs = list(pagos_collection.find({}, {"_id": 0})) 
    return docs

# ... (otras funciones como GET, POST) ...

# ===============================
# 🔹 Borrar TODOS los pagos/ventas (CORREGIDO: Usa la colección global 'pagos_collection')
# Corresponde a DELETE /api/pagos
# ===============================
@router.delete("/")
# 🟢 CORRECCIÓN 2: Eliminado Depends y el argumento de dependencia innecesario
def borrar_todos_los_pagos(): 
    try:
        # Usamos la variable global de colección
        resultado = pagos_collection.delete_many({})  
        
        if resultado.deleted_count == 0:
            return {"ok": True, "message": "No había pagos/ventas que eliminar. Limpieza exitosa.", "count": 0}

        return {
            "ok": True, 
            "message": f"{resultado.deleted_count} pagos/ventas eliminados correctamente.",
            "count": resultado.deleted_count
        }
    except Exception as e:
        print("❌ Error al borrar todos los pagos:", e)
        raise HTTPException(status_code=500, detail=f"Error al vaciar la colección de pagos: {e}")s
