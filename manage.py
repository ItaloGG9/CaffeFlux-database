from fastapi import FastAPI
from database import get_db_connection

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API de CaffeFlux conectada a PostgreSQL ✅"}

@app.get("/productos")
def ver_productos():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM productos;")
        columnas = [desc[0] for desc in cur.description]
        productos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
        cur.close()
        return productos
    finally:
        conn.close()

@app.get("/debug-db")
def debug_db():
    conn = get_db_connection()
    return {"tipo_conexion": str(type(conn))}
