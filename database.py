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
    if DATABASE_URL:
        try:
            url = urlparse(DATABASE_URL)
            
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port,
                # Forzar SSL es NECESARIO para Render
                sslmode='require' 
            )
            # En PostgreSQL, usamos un cursor para obtener las filas, 
            # no sqlite3.Row. Tu código de consulta deberá adaptarse.
            return conn
        
        except psycopg2.Error as e:
            print(f"ERROR: Fallo al conectar con PostgreSQL en Render. {e}")
            raise ConnectionError("No se pudo conectar a la base de datos de Render.")

    # ----------------------------------------------------
    # 2. CONEXIÓN DE DESARROLLO (LOCAL/SQLITE)
    # ----------------------------------------------------
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        # Mantener la configuración que tenías para facilitar la transición
        conn.row_factory = sqlite3.Row 
        return conn
