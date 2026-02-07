from fastapi import APIRouter, HTTPException, status # Importa APIRouter para crear rutas, HTTPException para errores HTTP, status para códigos HTTP
from src.domain.schemas import MessageSchema # Importa el esquema Pydantic para validación y serialización
from src.services.message_service import MessageService # Importa el servicio que contiene la lógica de negocio
from src.repositories.message_repository import MessageRepository # Importa el repositorio para acceso a base de datos
from src.database.database import SessionLocal # Importa la sesión de base de datos

router = APIRouter() # Crea un router para agrupar endpoints relacionados

db = SessionLocal() # Crear sesión de base de datos

# Inyectar dependencias
repository = MessageRepository(db) # Repositorio con la sesión global
service = MessageService(repository) # Servicio con el repositorio global

# Define endpoint POST para crear mensajes
# status_code=201: Código HTTP "Created" para éxito
@router.post("/api/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: MessageSchema): # message ya validado por Pydantic
    try:
        data = service.process_message(message)   # Procesa el mensaje a través de toda la cadena de servicios
        return {  # Retorna respuesta exitosa con formato consistente
            "status": "success",
            "data": data
        }
    except ValueError as e:
        raise HTTPException(  # Error de validación del negocio (ej: ID duplicado)
            status_code=400, # Bad Request
            detail={
                "status": "error",
                "error": {
                    "code": "VALIDATION_ERROR",  # Código de error para cliente
                    "message": str(e)
                }
            }
        )
    except Exception as e:
        print("ERROR REAL DEL SERVIDOR", e)
        raise

