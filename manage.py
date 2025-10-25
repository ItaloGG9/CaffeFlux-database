from fastapi import FastAPI
from database import get_db_connection

app = FastAPI()

@app.get("/productos")
def ver_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    columnas = [desc[0] for desc in cursor.description]
    productos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    return productos

@app.get("/debug-db")
def debug_db():
    conn = get_db_connection()
    return {"tipo_conexion": str(type(conn))}
