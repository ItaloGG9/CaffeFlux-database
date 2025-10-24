# settings.py (Ejemplo de lógica para Django)
import os
import dj_database_url
from pathlib import Path

# ... (otras configuraciones)

# Obtener la URL de la variable de entorno que configuraste en Render
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # USO DE POSTGRESQL (PRODUCCIÓN EN RENDER)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            # Esto es VITAL para Render
            ssl_require=True 
        )
    }
else:
    # USO DE SQLITE (DESARROLLO LOCAL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'local_database.db',
        }
    }
