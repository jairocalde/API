from fastapi import FastAPI
from src.api.endpoints import messages, health
from src.database.database import engine, Base
from src.database import models

app = FastAPI(title="Message Processing API")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Rutas
app.include_router(messages.router)
app.include_router(health.router)
