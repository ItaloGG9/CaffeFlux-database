# main.py
from fastapi import FastAPI

app = FastAPI()

# Ejemplo de ruta principal
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI en Render!"}

# Opcional: más rutas
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
