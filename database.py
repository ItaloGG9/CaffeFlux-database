import os
import sqlite3
from urllib.parse import urlparse
# Necesitas instalar esta librería: pip install psycopg2-binary
import psycopg2 

# Obtiene la URL de PostgreSQL desde la variable de entorno de Render
DATABASE_URL = os.environ.get('DATABASE_URL')

# Ruta local para SQLite (solo se usa si no hay DATABASE_URL)
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "local_database.db")


def get_db_connection():
    # ----------------------------------------------------
    # 1. CONEXIÓN DE PRODUCCIÓN (RENDER/POSTGRESQL)
    # ----------------------------------------------------
   # Modificación en database.py (parte de PRODUCCIÓN)
# ...
if os.environ.get('DB_HOST'): # Verificar si las variables separadas existen
    try:
        conn = psycopg2.connect(
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            host=os.environ.get('DB_HOST'),
            port='5432', # Puerto por defecto
            sslmode='require' # Aún necesaria para la conexión externa
        )
        return conn
# ...
    # ----------------------------------------------------
    # 2. CONEXIÓN DE DESARROLLO (LOCAL/SQLITE)
    # ----------------------------------------------------
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        # Mantener la configuración que tenías para facilitar la transición
        conn.row_factory = sqlite3.Row 
        return conn
