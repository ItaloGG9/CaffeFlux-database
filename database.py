import os
import sqlite3
from urllib.parse import urlparse
import psycopg2 

# 🚨 ADVERTENCIA: Esta URL contiene credenciales y solo debe usarse para pruebas.
# En producción, usa variables de entorno (os.environ.get).
DATABASE_URL_DIRECTO = "postgresql://base_de_datos_postgresql_00kp_user:AvAJSH6iC1aEj34OGhjQ7dHrBCimpFbW@dpg-d3tctauuk2gs73d1da5g-a.oregon-postgres.render.com/base_de_datos_postgresql_00kp"

def get_db_connection():
    # ----------------------------------------------------
    # 1. CONEXIÓN DE PRODUCCIÓN (RENDER/POSTGRESQL)
    # ----------------------------------------------------
    if DATABASE_URL_DIRECTO: # Usamos la URL incrustada
        try:
            # Parsear la URL (ahora la incrustada)
            url = urlparse(DATABASE_URL_DIRECTO)
            
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
            # Si falla la conexión, se levanta una excepción.
            print(f"ERROR: Fallo al conectar con PostgreSQL en Render. {e}")
            raise ConnectionError(f"No se pudo conectar a la base de datos de Render: {e}")

    # ----------------------------------------------------
    # 2. CONEXIÓN DE DESARROLLO (LOCAL/SQLITE)
    # ----------------------------------------------------
    else:
        # Esta sección nunca se ejecutará mientras DATABASE_URL_DIRECTO no esté vacío.
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  
        return conn
