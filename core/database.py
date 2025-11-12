# database.py (en la raíz)
import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()  # 🔹 carga las variables del archivo .env

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            sslmode='require'  # obligatorio en Render
        )
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error al conectar con PostgreSQL: {e}")
        raise
