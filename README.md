# CafféFlux - Backend Django + PostgreSQL)

API REST para la cafetería CafféFlux. Conectable a frontend en React.

## Instrucciones locales
1. Crear entorno virtual e instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar migraciones y cargar datos de ejemplo:
   ```bash
   python manage.py migrate
   python manage.py loaddata core/fixtures/initial_data.json
   ```
3. Crear usuario admin:
   ```bash
   python manage.py createsuperuser
   ```
4. Correr servidor:
   ```bash
   python manage.py runserver
   ```

## Despliegue en Railway
1. Subir este repositorio a GitHub.
2. Crear un nuevo proyecto en Railway y conectar el repo.
3. Railway ejecutará automáticamente `pip install -r requirements.txt`.
4. Ejecutar migraciones con:
   ```bash
   python manage.py migrate
   python manage.py loaddata core/fixtures/initial_data.json
   ```

Frontend React puede consumir esta API en `/api/...`.
