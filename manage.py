# main.py
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from base import get_db
from models import Producto

app = FastAPI()

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
