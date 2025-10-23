import sqlite3
import os

# --- Configuración ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Render NO tiene persistencia de archivos, por eso se crea dentro de /tmp/
DB_FILE_PATH = os.environ.get('DATABASE_PATH', os.path.join('/tmp', 'local_database.db'))

SCHEMA_FILE = os.path.join(BASE_DIR, 'schema.sql')
DATA_FILE = os.path.join(BASE_DIR, 'base.sql')
# ---------------------

def initialize_database():
    """
    Revisa si la base de datos existe. Si no, la crea
    y ejecuta los scripts schema.sql y base.sql.
    """

    db_exists = os.path.exists(DB_FILE_PATH)

    if not db_exists:
        print(f"⚙️  Creando base de datos en '{DB_FILE_PATH}'...")
        try:
            conn = sqlite3.connect(DB_FILE_PATH)
            cursor = conn.cursor()

            print(f"🏗️  Ejecutando {SCHEMA_FILE}...")
            with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())

            print(f"📦  Ejecutando {DATA_FILE}...")
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())

            conn.commit()
            conn.close()
            print("✅ Base de datos inicializada correctamente.")

        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            if os.path.exists(DB_FILE_PATH):
                os.remove(DB_FILE_PATH)
    else:
        print(f"ℹ️  Base de datos ya existente en '{DB_FILE_PATH}'. Omitiendo creación.")

if __name__ == "__main__":
    initialize_database()
