import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔹 fuerza la carga de la conexión a Mongo al iniciar
from core import mongo  # noqa: F401

# Agregar el directorio actual al sys.path para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar routers
from routers.productos import router as productos_router
from routers.mesas import router as mesas_router
from routers.pedidos import router as pedidos_router
from routers.lineas_pedido import router as lineas_pedido_router
from routers.pagos import router as pagos_router
from routers.turnos import router as turnos_router
from routers.jerarquia import router as jerarquia_router
from routers.nosql import router as nosql

app = FastAPI(
    title="CaffeFlux API ☕",
    description="API del sistema de pedidos, productos y mesas del proyecto CaffeFlux.",
    version="1.0.0",
)

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://caffeflux-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧩 Routers
app.include_router(productos_router)
app.include_router(mesas_router)
app.include_router(pedidos_router)
app.include_router(lineas_pedido_router)
app.include_router(pagos_router)
app.include_router(turnos_router)
app.include_router(jerarquia_router)
app.include_router(nosql)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de CaffeFlux conectada a PostgreSQL ✅"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Imprime rutas al iniciar (útil para verificar /api/pagos)
@app.on_event("startup")
async def show_routes():
    for r in app.routes:
        try:
            print("ROUTE:", r.path, list(getattr(r, "methods", [])))
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("manage:app", host="0.0.0.0", port=port)
