from fastapi import APIRouter, HTTPException
from core.database import get_db_connection
from pydantic import BaseModel

router = APIRouter(prefix="/api/mesas", tags=["Mesas"])

class Mesa(BaseModel):
    numero_mesa: int
    estado: str

@router.get("/")
def ver_mesas():
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM mesas;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close(); conn.close()
    return datos

@router.post("/")
def agregar_mesa(mesa: Mesa):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO mesas (numero_mesa, estado) VALUES (%s, %s) RETURNING id_mesa;", 
                (mesa.numero_mesa, mesa.estado))
    nuevo_id = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return {"id_mesa": nuevo_id, **mesa.dict()}

@router.put("/{id_mesa}")
def editar_mesa(id_mesa: int, mesa: Mesa):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("UPDATE mesas SET numero_mesa=%s, estado=%s WHERE id_mesa=%s;",
                (mesa.numero_mesa, mesa.estado, id_mesa))
    conn.commit(); cur.close(); conn.close()
    return {"mensaje": "Mesa actualizada", "id_mesa": id_mesa}

@router.delete("/{id_mesa}")
def eliminar_mesa(id_mesa: int):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM mesas WHERE id_mesa=%s;", (id_mesa,))
    conn.commit(); cur.close(); conn.close()
    return {"mensaje": "Mesa eliminada", "id_mesa": id_mesa}
