from fastapi import APIRouter
from core.database import get_db_connection

router = APIRouter(prefix="/api/jerarquia", tags=["Jerarquía"])

@router.get("/")
def ver_jerarquia():
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM jerarquiaproductos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close(); conn.close()
    return datos
