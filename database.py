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
    # El primer nivel de código dentro de la función debe estar indentado 4 espacios.
    
    # ----------------------------------------------------
    # 1. CONEXIÓN DE PRODUCCIÓN (RENDER/POSTGRESQL)
    # ----------------------------------------------------
    if DATABASE_URL: 
        # Asegúrate que el bloque try/except esté indentado 8 espacios (4 + 4)
        try:
            # ... tu lógica de psycopg2.connect ...
            # y el sslmode='require'
        except psycopg2.Error as e:
            # ... manejo del error
            pass # Asegúrate que el pass/raise esté correctamente indentado
    # ----------------------------------------------------
    # 2. CONEXIÓN DE DESARROLLO (LOCAL/SQLITE)
    # ----------------------------------------------------
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        # Mantener la configuración que tenías para facilitar la transición
        conn.row_factory = sqlite3.Row 
        return conn
