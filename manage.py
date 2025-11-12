import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core import mongo  # 👈 Importa la conexión a MongoDB



# Agregar el directorio actual al sys.path para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar los routers de las diferentes funcionalidades
from routers.productos import router as productos_router
from routers.mesas import router as mesas_router
from routers.pedidos import router as pedidos_router
from routers.lineas_pedido import router as lineas_pedido_router
from routers.pagos import router as pagos_router
from routers.turnos import router as turnos_router
from routers.jerarquia import router as jerarquia_router
from routers.nosql import router as nosql


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="CaffeFlux API ☕",
    description="API del sistema de pedidos, productos y mesas del proyecto CaffeFlux.",
    version="1.0.0"
)

# =====================================================
# 🧩 Incluir los Routers
# =====================================================
app.include_router(productos_router)
app.include_router(mesas_router)
app.include_router(pedidos_router)
app.include_router(lineas_pedido_router)
app.include_router(pagos_router)
app.include_router(turnos_router)
app.include_router(jerarquia_router)
app.include_router(nosql)

# =====================================================
# 🌐 Configuración CORS (para permitir conexión con el frontend React)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://caffeflux-frontend.onrender.com"],  # Agregar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# =====================================================
# 🏠 Ruta principal
# =====================================================
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de CaffeFlux conectada a PostgreSQL ✅"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("manage:app", host="0.0.0.0", port=port)
