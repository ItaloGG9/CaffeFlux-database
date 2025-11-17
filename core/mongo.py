# core/mongo.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://caffeflux:igg1812@caffeflux.f393nnt.mongodb.net/?retryWrites=true&w=majority&appName=Caffeflux")  # sin default, así te obliga a configurarla bien

if not MONGO_URL:
    raise RuntimeError("❌ Falta la variable de entorno MONGO_URL")

try:
    client = MongoClient(MONGO_URL)
    db = client["caffeflux"]  # nombre de tu base en Atlas
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print(f"❌ Error conectando con MongoDB: {e}")
    raise
