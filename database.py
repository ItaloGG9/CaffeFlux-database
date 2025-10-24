import os
import sqlite3
from urllib.parse import urlparse
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
            # Parsear la URL de Render
            url = urlparse(DATABASE_URL)
            
            # Conexión a PostgreSQL (con SSL)
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port,
                sslmode='require'  # OBLIGATORIO para Render
            )
            return conn
        
        except psycopg2.Error as e:
            # Si falla la conexión (ej. credenciales malas), se imprime el error 
            # y se levanta una excepción.
            print(f"ERROR: Fallo al conectar con PostgreSQL en Render. {e}")
            # Es mejor levantar el error para que FastAPI sepa que falló.
            raise ConnectionError(f"No se pudo conectar a la base de datos de Render: {e}")

    # ----------------------------------------------------
    # 2. CONEXIÓN DE DESARROLLO (LOCAL/SQLITE)
    # ----------------------------------------------------
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  
        return conn
