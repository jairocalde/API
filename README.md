
#  API Para Nequi

## Descripción General del Proyecto

**API Para Nequi** es una API RESTful desarrollada en Python con FastAPI como parte de la prueba técnica para backend. La API permite procesar, validar, almacenar y recuperar mensajes de chat con un enfoque en arquitectura limpia y buenas prácticas de desarrollo.

### 🎯 Objetivos Cumplidos
-  **Diseñar e implementar una API limpia y mantenible**
-  **Trabajar con Python y frameworks backend comunes** (FastAPI, SQLAlchemy)
-  **Implementar manejo de errores y validación adecuados**
-  **Escribir pruebas unitarias con cobertura > 80%**
-  **Documentar código y API de forma completa**

### ✨ Características Principales
- **Validación robusta** de mensajes con Pydantic
- **Procesamiento pipeline** (conteo palabras/caracteres, filtrado contenido)
- **Base de datos SQLite** con SQLAlchemy ORM
- **Arquitectura limpia** (separación de responsabilidades)
- **Documentación automática** Swagger UI y ReDoc
- **Manejo de errores** con respuestas HTTP apropiadas
- **Paginación y filtrado** en consultas de mensajes

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web async |
| SQLAlchemy | 2.0.25 | ORM para base de datos |
| Pydantic | 1.10.13 | Validación de datos |
| SQLite | 3.x | Base de datos embebida |
| Pytest | 7.4.3 | Framework de pruebas |
| Uvicorn | 0.24.0 | Servidor ASGI |

## Estructura del Proyecto

api/
├── src/ # Código fuente principal
│ ├── api/ # Capa de presentación (endpoints)
│ │ ├── endpoints/
│ │ │ ├── messages.py # Endpoints de mensajes
│ │ │ └── health.py # Endpoints de monitoreo
│ │ └── init.py
│ ├── core/ # Configuración y utilidades
│ │ ├── config.py # Configuración de la aplicación
│ │ └── init.py
│ ├── database/ # Capa de datos
│ │ ├── database.py # Configuración de DB y sesiones
│ │ ├── models.py # Modelos SQLAlchemy
│ │ └── init.py
│ ├── domain/ # Modelos de dominio
│ │ ├── schemas.py # Esquemas Pydantic (DTOs)
│ │ └── init.py
│ ├── repositories/ # Patrón repositorio
│ │ ├── message_repository.py # Operaciones CRUD
│ │ └── init.py
│ ├── services/ # Lógica de negocio
│ │ ├── message_service.py # Servicio principal
│ │ ├── validation_service.py # Validación de mensajes
│ │ ├── processing_pipeline.py # Procesamiento de contenido
│ │ └── init.py
│ └── main.py # Aplicación principal FastAPI
├── tests/ # Pruebas unitarias e integración
│ ├── test_api.py # Pruebas de endpoints
│ ├── test_services.py # Pruebas de servicios
│ └── init.py
├── requirements.txt # Dependencias del proyecto
├── Dockerfile # Configuración Docker
├── docker-compose.yml # Orquestación Docker
├── .env.example # Variables de entorno ejemplo
├── .gitignore # Archivos ignorados por Git
└── README.md # Este archivo

##  Instalación y Configuración

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Paso 1: Clonar el Repositorio

# Clonar desde GitHub
git clone https://github.com/jairocalde/API
cd API

### Paso 2: Configurar Entorno Virtual
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Si hay error de permisos, ejecutar como administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# En Windows (CMD):
venv\Scripts\activate.bat

# Verificar que está activado (deberías ver (venv) al principio)
(venv) $

### Paso 3: Instalar Dependencias
# Instalar desde requirements.txt
pip install -r requirements.txt

# Verificar instalación
pip list | findstr fastapi  # Windows

### Paso 4: Configurar Variables de Entorno

# Copiar archivo de ejemplo
copy .env.example .env  # Windows

# Los valores por defecto funcionarán para desarrollo

## Ejecución de la Aplicación

# Desde la raíz del proyecto
uvicorn src.main:app --reload

# Verificar que la aplicación está corriendo

# o en PowerShell:
Invoke-RestMethod -Uri "http://localhost:8000/"

# Salida esperada:

{
  "message": "Chat Message Processing API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "redoc": "/redoc"
}

# Documentación de la API

## Endpoints Disponibles
 
### POST /api/messages - Crear Mensaje
Crea un nuevo mensaje de chat con validación y procesamiento.

Request Body tipo JSON:

{
  "message_id": "msg-123456", //string
  "session_id": "session-abcdef", //string
  "content": "Hola, ¿cómo puedo ayudarte hoy?", //string
  "timestamp": "2023-06-15T14:30:00Z", //datatime
  "sender": "system" //string
}

Response (201 Created):

{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 32,
      "processed_at": "2023-06-15T14:30:01Z",
      "is_filtered": false
    }
  }
}

Response (400 Bad Request - Ejemplo de error):

{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Formato de mensaje inválido",
    "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}

### GET /api/messages/{session_id} - Obtener Mensajes
Recupera todos los mensajes de una sesión específica con paginación.

Parámetros de consulta:

Parámetro	Tipo	
skip,	integer	// Número de mensajes a omitir
limit,	integer	//	Máximo de mensajes a retornar (1-1000)
sender,	string	//	Filtrar por remitente ("user" o "system")

Ejemplo de request:

GET /api/messages/session-abcdef?skip=0&limit=10&sender=user

Response (200 OK):

{
  "status": "success",
  "data": {
    "session_id": "session-abcdef",
    "messages": [
      {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo estás?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
        "metadata": {
          "word_count": 3,
          "character_count": 14,
          "processed_at": "2023-06-15T14:30:01Z",
          "is_filtered": false
        }
      }
    ],
    "pagination": {
      "skip": 0,
      "limit": 10,
      "total": 1,
      "has_more": false
    }
  }
}

### GET /health - Health Check
Verifica que la API está funcionando correctamente.

response:

{
  "status": "healthy",
  "service": "chat-message-api"
}

### GET /ready - Readiness Check
Verifica que la API y sus dependencias (base de datos) están listas.

Response:

{
  "status": "ready",
  "service": "chat-message-api",
  "database": "connected"
}

Códigos de Estado HTTP

Código	                  Significado	              Uso
200                       OK	Solicitud exitosa	    GET, respuestas exitosas
201Created	              Recurso creado	          POST exitoso
400Bad Request	          Error de validación	      Datos inválidos
404Not Found	            Recurso no encontrado	    Sesión no existente
500Internal Server Error	Error del servidor	      Errores inesperados

# Instrucciones para Pruebas

Configuración del Entorno de Pruebas

## Asegúrate de tener el entorno virtual activado
venv\Scripts\activate  # Windows

## Instalar dependencias de desarrollo si no están
pip install pytest pytest-cov

Ejecutar Todas las Pruebas
## Desde la raíz del proyecto
pytest

## Con información detallada
pytest -v

## Ejecutar pruebas específicas
pytest tests/test_api.py -v
pytest tests/test_services.py -v

Ejecutar con Cobertura de Código

## Reporte en terminal
pytest --cov=src --cov-report=term-missing

## Reporte HTML (se crea carpeta htmlcov/)
pytest --cov=src --cov-report=html

## Abrir reporte HTML en navegador
Windows:
start htmlcov/index.html

Pruebas de Integración Manuales
Usando cURL

1. Health check
curl -X GET "http://localhost:8000/health"

2. Crear mensaje
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test-curl-001",
    "session_id": "session-curl-001",
    "content": "Prueba desde cURL",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "user"
  }'

3. Obtener mensajes
curl -X GET "http://localhost:8000/api/messages/session-curl-001"

Usando Python

import requests
import json

4. Crear mensaje
response = requests.post(
    "http://localhost:8000/api/messages/",
    json={
        "message_id": "test-python-001",
        "session_id": "session-python-001",
        "content": "Prueba desde Python",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system"
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

Pruebas Automatizadas con Script

5. Ejecutar script de pruebas completo
python test_api_complete.py

# Solución de Problemas Comunes

1. No se puede activar entorno virtual en Windows

## Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

2.  Error "Address already in use"
## Cambiar puerto
uvicorn src.main:app --reload --port 8001

## O matar proceso en puerto 8000
Windows:
netstat -ano | findstr :8000
taskkill /PID [PID] /F

3. Error de importación de módulos

## Verificar estructura de carpetas
ls -la src/

## Asegurarse de que existen archivos __init__.py
find src -name "__init__.py" | wc -l  # Debería ser al menos 6

4. Base de datos no se crea

## Borrar archivo existente y reiniciar
rm chat_messages.db  # Linux/Mac
del chat_messages.db  # Windows

## Reiniciar aplicación
uvicorn src.main:app --reload

5. Criterios de Evaluación Implementados

Criterio	           Estado	          Evidencia
Funcionalidad	       Completado	      Endpoints POST/GET funcionando con validación
Calidad del Código	 Completado	      Arquitectura limpia, SOLID, código legible
Pruebas	             Completado	      Pruebas unitarias con cobertura >80%
Manejo de Errores	   Completado	      Respuestas HTTP apropiadas, mensajes claros
Documentación	       Completado	      Swagger UI, ReDoc, README completo

