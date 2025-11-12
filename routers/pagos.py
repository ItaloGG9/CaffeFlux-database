from fastapi import APIRouter
from core.database import get_db_connection

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

@router.get("/")
def ver_pagos():
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM pagos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close(); conn.close()
    return datos

# routers/pagos.py
@router.delete("/")
def borrar_todos_los_pagos():
    pagos_collection.delete_many({})
    return {"message": "Pagos eliminados"}

# routers/turnos.py
@router.delete("/cerrados")
def borrar_turnos_cerrados():
    turnos_collection.delete_many({"estado": "cerrado"})
    return {"message": "Turnos cerrados eliminados"}
