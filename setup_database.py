import sqlite3
import os

# --- Configuración ---
# Railway nos dará una ruta persistente en la variable 'DATABASE_PATH'
# Si no existe (para pruebas locales), usará 'local_database.db'
DB_FILE_PATH = os.environ.get('DATABASE_PATH', 'local_database.db')
SCHEMA_FILE = 'schema.sql'
DATA_FILE = 'base.sql'
# ---------------------

def initialize_database():
    """
    Revisa si la base de datos existe. Si no, la crea
    y ejecuta los scripts schema.sql y base.sql.
    """
    
    # Revisamos si el archivo .db ya existe
    db_exists = os.path.exists(DB_FILE_PATH)
    
    if not db_exists:
        print(f"No se encontró la base de datos en '{DB_FILE_PATH}'. Creando una nueva...")
        
        try:
            # 1. Conectar (esto crea el archivo .db vacío)
            conn = sqlite3.connect(DB_FILE_PATH)
            cursor = conn.cursor()
            
            # 2. Leer y ejecutar el schema.sql (crear tablas)
            print(f"Ejecutando {SCHEMA_FILE}...")
            with open(SCHEMA_FILE, 'r') as f:
                cursor.executescript(f.read())
            
            # 3. Leer y ejecutar el base.sql (insertar datos iniciales)
            print(f"Ejecutando {DATA_FILE}...")
            with open(DATA_FILE, 'r') as f:
                cursor.executescript(f.read())

            # Guardar cambios y cerrar
            conn.commit()
            conn.close()
            
            print("¡Base de datos inicializada con éxito!")
            
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            # Si falla, borramos el archivo para reintentar en el próximo inicio
            if os.path.exists(DB_FILE_PATH):
                os.remove(DB_FILE_PATH)
    else:
        print(f"La base de datos en '{DB_FILE_PATH}' ya existe. Omitiendo creación.")

if __name__ == "__main__":
    initialize_database()