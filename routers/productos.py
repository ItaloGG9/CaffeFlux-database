from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.database import get_db_connection

class Producto(BaseModel):
    nombre_producto: str
    precio_venta: float
    precio_costo: float
    jerarquia: str
    estado_producto: bool
    id_jerarquia: int
    
router = APIRouter(prefix="/api/productos", tags=["Productos"])



@router.get("/")
def ver_productos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos;")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return datos


@router.post("/")
def agregar_producto(producto: Producto):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO productos 
            (nombre_producto, precio_venta, precio_costo, jerarquia, estado_producto, id_jerarquia)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_producto;
            """,
            (
                producto.nombre_producto,
                producto.precio_venta,
                producto.precio_costo,
                producto.jerarquia,
                producto.estado_producto,
                producto.id_jerarquia
            )
        )
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        return {"id_producto": nuevo_id, **producto.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar producto: {e}")
    finally:
        cur.close()
        conn.close()


@router.put("/{producto_id}")
def editar_producto(producto_id: int, producto: Producto):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id_producto = %s;", (producto_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cur.execute(
        """
        UPDATE productos
        SET nombre_producto=%s, precio_venta=%s, precio_costo=%s, jerarquia=%s, estado_producto=%s, id_jerarquia=%s
        WHERE id_producto=%s;
        """,
        (
            producto.nombre_producto,
            producto.precio_venta,
            producto.precio_costo,
            producto.jerarquia,
            producto.estado_producto,
            producto.id_jerarquia,
            producto_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"id_producto": producto_id, **producto.dict()}


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Verificar existencia (Esto ya lo tienes)
    cur.execute("SELECT 1 FROM productos WHERE id_producto = %s;", (producto_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        # 2. Intentar la eliminación
        cur.execute("DELETE FROM productos WHERE id_producto = %s;", (producto_id,))
        conn.commit()
        return {"mensaje": "Producto eliminado", "id_producto": producto_id}
        
    except Exception as e:
        # 3. Manejo de errores
        conn.rollback() # ¡Importante!
        # Si el error es de clave foránea, podemos devolver un 409 Conflict
        # En PostgreSQL, el error 23503 es el de Foreign Key Violation
        if '23503' in str(e): 
            raise HTTPException(
                status_code=409, 
                detail="No se puede eliminar el producto porque está siendo referenciado por otras tablas (ej. órdenes o inventario)."
            )
        # Para cualquier otro error, devolvemos el 500 general
        raise HTTPException(status_code=500, detail=f"Error inesperado al eliminar producto: {e}")
        
    finally:
        # 4. Cerrar recursos
        cur.close()
        conn.close()
