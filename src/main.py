from fastapi import FastAPI # Importa FastAPI para crear la aplicación web
from src.api.endpoints import messages, health # Importa los routers (conjuntos de endpoints) de mensajes y salud
from src.database.database import engine, Base # Importa engine (conexión a DB) y Base (base para modelos SQLAlchemy)
from src.database import models # Importa modelos para que SQLAlchemy los registre (aunque no se usan directamente)

app = FastAPI(title="API PARA NEQUI", debug=True) # Crea la aplicación FastAPI principal, title: Nombre de la API en documentación, debug: True solo para desarrollo, muestra errores detallados

Base.metadata.create_all(bind=engine) # Crea todas las tablas en la base de datos basadas en los modelos definidos, Se ejecuta al iniciar la aplicación. En producción usar migraciones (Alembic)

app.include_router(messages.router) # Registra los grupos de endpoints en la aplicación, Todas las rutas de messages.py estarán bajo /api/messages
app.include_router(health.router) # Rutas de health para monitoreo
