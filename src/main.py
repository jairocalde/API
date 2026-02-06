# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.database.database import engine, Base
from src.api.endpoints import messages, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager para manejar eventos de inicio y cierre de la aplicación.
    """
    print("🚀 Iniciando la API...")
    
    try:
        # Crear tablas de base de datos
        Base.metadata.create_all(bind=engine)
        print(" Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar base de datos: {e}")
    
    yield
    
    print("Apagando aplicación...")

# PRIMERO definir 'app' antes de usarlo
app = FastAPI(
    title="API para Nequi",
    description="""
    API RESTful para procesamiento de mensajes de chat.
    
    Características
    
    - Crear mensajes con validación y procesamiento
    - Recuperar mensajes por sesión con paginación
    - Filtrar contenido inapropiado
    - Conteo de palabras y caracteres
    - Manejo robusto de errores
    
    Endpoints
    
    - `POST /api/messages` - Crear un nuevo mensaje
    - `GET /api/messages/{session_id}` - Obtener mensajes por sesión
    - `GET /health` - Verificar salud de la API
    - `GET /ready` - Verificar preparación de la API
    """,
    version="1.0.0",
    contact={
        "name": "Jairo Calderon ",
        "email": "developer@example.com",
    },
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# AHORA SÍ incluir routers (después de definir 'app')
app.include_router(messages.router)
app.include_router(health.router)

@app.get("/", include_in_schema=False)
async def root():
    """Página de inicio de la API"""
    return {
        "message": "Chat Message Processing API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "create_message": "POST /api/messages",
            "get_messages": "GET /api/messages/{session_id}",
            "health": "GET /health",
            "readiness": "GET /ready"
        }
    }

@app.get("/info", include_in_schema=False)
async def api_info():
    """Información detallada de la API"""
    return {
        "name": "API",
        "version": "1.0.0",
        "description": "API para procesamiento de mensajes de chat - Prueba Técnica",
        "author": "Jairo Calderon",
        "repository": "https://github.com/jairocalde/API"
    }