from fastapi import FastAPI
import os
import sqlite3
from database import get_db_connection  # ✅ importamos nuestra función nueva

app = FastAPI()

DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/local_database.db')

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI en Render!"}

# Ejemplo simple: listar productos desde SQLite
@app.get("/productos")
def ver_productos():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return [dict(row) for row in productos]
