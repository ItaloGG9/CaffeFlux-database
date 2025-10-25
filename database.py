import psycopg2
from urllib.parse import urlparse

# URL directa de tu base en Render (puedes moverla a variable de entorno si quieres)
DATABASE_URL = "postgresql://base_de_datos_postgresql_00kp_user:AvAJSH6iC1aEj34OGhjQ7dHrBCimpFbW@dpg-d3tctauuk2gs73d1da5g-a.oregon-postgres.render.com/base_de_datos_postgresql_00kp"

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
