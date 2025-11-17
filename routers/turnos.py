from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.database import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/api/turnos", tags=["Turnos"])


# ===============================
# 🔹 Modelo de datos Turno
# ===============================
class Turno(BaseModel):
    usuario_responsable: str
    fondo_inicial: float | None = 0.0
    hora_apertura: datetime | None = None


# ===============================
# 🔹 Obtener todos los turnos (MODIFICADO: Ordenado por más reciente)
# ===============================
@router.get("/")
def ver_turnos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 🟢 CAMBIO APLICADO AQUÍ: Ordenar por 'hora_apertura' o 'id_turno' de forma descendente (DESC)
        cur.execute("SELECT * FROM turnos ORDER BY hora_apertura DESC;")
        
        columnas = [desc[0] for desc in cur.description]
        datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
        cur.close()
        conn.close()
        return datos
    except Exception as e:
        print("❌ Error al consultar turnos:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 🔹 Obtener turno activo
# ===============================
@router.get("/active")
def turno_activo():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM turnos 
        WHERE hora_cierre IS NULL
        ORDER BY hora_apertura DESC LIMIT 1;
        """
    )
    fila = cur.fetchone()
    cur.close()
    conn.close()
    if not fila:
        return None
    columnas = [desc[0] for desc in cur.description]
    return dict(zip(columnas, fila))


# ===============================
# 🔹 Abrir turno
# ===============================
@router.post("/open")
def abrir_turno(turno: Turno):
    conn = get_db_connection()
    cur = conn.cursor()
    hora_apertura = turno.hora_apertura or datetime.now()
    try:
        cur.execute(
            """
            INSERT INTO turnos (usuario_responsable, hora_apertura, fondo_inicial)
            VALUES (%s, %s, %s)
            RETURNING id_turno, usuario_responsable, hora_apertura, fondo_inicial;
            """,
            (turno.usuario_responsable, hora_apertura, turno.fondo_inicial),
        )
        nuevo = cur.fetchone()
        conn.commit()
        columnas = [desc[0] for desc in cur.description]
        return dict(zip(columnas, nuevo))
    except Exception as e:
        conn.rollback()
        print("❌ Error al abrir turno:", e)
        raise HTTPException(status_code=500, detail=f"Error al abrir turno: {e}")
    finally:
        cur.close()
        conn.close()


# ===============================
# 🔹 Cerrar turno
# ===============================
@router.post("/close")
def cerrar_turno(data: dict):
    id_turno = data.get("id_turno")
    usuario_cierre = data.get("usuario_cierre", "Desconocido")

    if not id_turno:
        raise HTTPException(status_code=400, detail="id_turno es requerido")

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM turnos WHERE id_turno = %s;", (id_turno,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Turno no encontrado")

        cur.execute(
            """
            UPDATE turnos 
            SET hora_cierre = %s, usuario_cierre = %s
            WHERE id_turno = %s
            RETURNING *;
            """,
            (datetime.now(), usuario_cierre, id_turno),
        )
        fila = cur.fetchone()
        conn.commit()
        columnas = [desc[0] for desc in cur.description]
        return dict(zip(columnas, fila))
    except Exception as e:
        conn.rollback()
        print("❌ Error al cerrar turno:", e)
        raise HTTPException(status_code=500, detail=f"Error al cerrar turno: {e}")
    finally:
        cur.close()
        conn.close()


# ===============================
# 🔹 Eliminar turno por ID
# ===============================
@router.delete("/{id_turno}")
def eliminar_turno(id_turno: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM turnos WHERE id_turno = %s RETURNING id_turno;",
            (id_turno,)
        )
        eliminado = cur.fetchone()
        conn.commit()

        if not eliminado:
            raise HTTPException(status_code=404, detail=f"Turno con ID {id_turno} no encontrado.")

        return {"ok": True, "message": f"Turno {id_turno} eliminado correctamente."}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print("❌ Error al eliminar turno:", e)
        raise HTTPException(status_code=500, detail=f"Error al eliminar turno: {e}")
    finally:
        cur.close()
        conn.close()
    
# ===============================
# 🔹 Borrar todos los turnos CERRADOS
# Corresponde a DELETE /api/turnos/cerrados
# ===============================
@router.delete("/cerrados")
def borrar_turnos_cerrados():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Borra todos los turnos que tienen hora_cierre (es decir, están cerrados)
        cur.execute(
            "DELETE FROM turnos WHERE hora_cierre IS NOT NULL RETURNING id_turno;"
        )
        count = cur.rowcount
        conn.commit()
        return {
            "ok": True, 
            "count": count, 
            "message": f"{count} turno(s) cerrado(s) eliminado(s) correctamente."
        }
    except Exception as e:
        conn.rollback()
        print("❌ Error al borrar turnos cerrados:", e)
        raise HTTPException(status_code=500, detail=f"Error al borrar turnos cerrados: {e}")
    finally:
        cur.close()
        conn.close()


# ===============================
# 🔹 Borrar todos los turnos ACTIVOS
# Corresponde a DELETE /api/turnos/activos
# ===============================
@router.delete("/activos")
def borrar_turnos_activos():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Borra todos los turnos donde hora_cierre es NULL (es decir, están activos)
        cur.execute(
            "DELETE FROM turnos WHERE hora_cierre IS NULL RETURNING id_turno;"
        )
        count = cur.rowcount
        conn.commit()
        return {
            "ok": True, 
            "count": count, 
            "message": f"{count} turno(s) activo(s) eliminado(s) correctamente."
        }
    except Exception as e:
        conn.rollback()
        print("❌ Error al borrar turnos activos:", e)
        raise HTTPException(status_code=500, detail=f"Error al borrar turnos activos: {e}")
    finally:
        cur.close()
        conn.close()
