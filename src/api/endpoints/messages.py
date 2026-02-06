# src/api/endpoints/messages.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database.database import get_db
from src.domain.schemas import MessageCreate, SuccessResponse, ErrorResponse, MessageListResponse
from src.services.message_service import MessageService
from src.repositories.message_repository import MessageRepository

# REQUERIMIENTO: 1. Endpoint de Mensajes - Router principal para endpoints de mensajes

router = APIRouter(prefix="/api/messages", tags=["messages"])

# REQUERIMIENTO: 1.1. Endpoint POST /api/messages que acepte cargas JSON
# REQUERIMIENTO: 1.2. El endpoint debe validar los mensajes entrantes
# REQUERIMIENTO: 1.3. Procesar mensajes válidos y almacenarlos en la base de datos
# REQUERIMIENTO: 1.4. Devolver códigos de estado HTTP y respuestas apropiadas
# REQUERIMIENTO: 1.5. Manejo de Errores - Formato de mensaje inválido, campos requeridos faltantes

@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Mensaje creado exitosamente"},
        400: {"model": ErrorResponse, "description": "Error de validación"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo mensaje de chat.
    
    - **message_id**: ID único del mensaje (debe comenzar con "msg-" o "message-")
    - **session_id**: ID de la sesión
    - **content**: Contenido del mensaje (máx. 1000 caracteres)
    - **timestamp**: Fecha y hora en formato ISO 8601 con timezone
    - **sender**: Remitente ("user" o "system")

        Funcionalidades implementadas:
    1. Acepta cargas JSON (validado por FastAPI con MessageCreate)
    2. Valida mensajes entrantes (esquema Pydantic + servicios de validación)
    3. Procesa mensajes válidos (pipeline de procesamiento)
    4. Almacena en base de datos (repositorio SQLAlchemy)
    5. Devuelve códigos HTTP apropiados (201, 400, 500)
    6. Manejo de errores completo (validación, DB, servidor)

    """
    try:
        repository = MessageRepository(db)
        service = MessageService(repository)
        
        # Convertir a dict para validación
        message_dict = message.dict()
        
        # REQUERIMIENTO: 1.2. Validación de mensaje (implementada en MessageService)
        # Procesar y guardar mensaje
        result = service.create_message(message_dict)
        
        # REQUERIMIENTO: 1.4. Respuesta exitosa con código 201
        return SuccessResponse(
            status="success",
            data=result
        )
    
    except ValueError as e:
         # REQUERIMIENTO: 5. Manejo de errores - Formato de mensaje inválido / campos faltantes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                    "details": str(e)
                }
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno del servidor",
                    "details": str(e)
                }
            }
        )
# REQUERIMIENTO: 4. Recuperación de Mensajes
# 4.1. Endpoint GET /api/messages/{session_id} para sesión dada
# 4.2. Soporte para paginación (limit/offset)
# 4.3. Permitir filtrado por remitente

@router.get(
    "/{session_id}",
    response_model=MessageListResponse,
    responses={
        200: {"description": "Lista de mensajes recuperada exitosamente"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def get_messages(
    session_id: str,
    skip: int = Query(0, ge=0, description="Número de mensajes a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de mensajes"),
    sender: Optional[str] = Query(None, description="Filtrar por remitente"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los mensajes para una sesión específica.
    
    - **session_id**: ID de la sesión a consultar
    - **skip**: Número de mensajes a omitir (paginación)
    - **limit**: Número máximo de mensajes a retornar (1-1000)
    - **sender**: Filtrar por remitente (opcional)
    """
    try:
        # Validar parámetro sender si se proporciona
        if sender and sender not in ["user", "system"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "error": {
                        "code": "INVALID_PARAMETER",
                        "message": "El parámetro 'sender' debe ser 'user' o 'system'",
                        "details": f"Valor recibido: '{sender}'"
                    }
                }
            )
        
        repository = MessageRepository(db)
        service = MessageService(repository)
        
        result = service.get_messages_by_session(
            session_id=session_id,
            skip=skip,
            limit=limit,
            sender=sender
        )
        
        return MessageListResponse(
            status="success",
            data=result
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error al recuperar mensajes",
                    "details": str(e)
                }
            }
        )