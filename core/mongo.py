from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()


# Obtiene la URL desde las variables de entorno
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://italogrossi9_db_user:italogrossi9_db_user@caffeflux.yqiwvy6.mongodb.net/?appName=Caffeflux")

# Crea la conexión con MongoDB Atlas
try:
    client = MongoClient(MONGO_URL)
    db = client["caffeflux"]  # nombre de tu base de datos en Atlas
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print(f"❌ Error conectando con MongoDB: {e}")

# Colecciones
ventas_collection = db["ventas"]
logs_collection = db["logs"]
