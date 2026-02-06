from fastapi import APIRouter, HTTPException, status
from src.domain.schemas import MessageSchema
from src.services.message_service import MessageService
from src.repositories.message_repository import MessageRepository
from src.database.database import SessionLocal

router = APIRouter()

# Crear sesión de base de datos
db = SessionLocal()

# Inyectar dependencias
repository = MessageRepository(db)
service = MessageService(repository)

@router.post("/api/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: MessageSchema):
    try:
        data = service.process_message(message)
        return {
            "status": "success",
            "data": data
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e)
                }
            }
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno del servidor"
                }
            }
        )
