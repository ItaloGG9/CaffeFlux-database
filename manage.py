# main.py
from fastapi import FastAPI
import sqlite3
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Producto

app = FastAPI()
DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/local_database.db')

# Ejemplo de ruta principal
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI en Render!"}

# Opcional: más rutas
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/api/debug/productos")
def ver_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
