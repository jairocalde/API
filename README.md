#  API Para Nequi

## Descripción General del Proyecto
Este proyecto consiste en el desarrollo de una API RESTful construida con Python y FastAPI, cuyo objetivo es procesar mensajes de chat de manera estructurada y segura.

La API permite:

Recibir mensajes de chat en formato JSON
Validar el formato y contenido de los mensajes
Procesar el contenido (filtrado básico y generación de metadatos)
Almacenar los mensajes en una base de datos SQLite
Recuperar mensajes por sesión con soporte de paginación y filtrado
Manejar errores de forma clara y consistente

El proyecto fue desarrollado siguiendo principios de arquitectura limpia, separando responsabilidades entre capas de presentación, dominio, lógica de negocio y acceso a datos, facilitando la mantenibilidad, escalabilidad y pruebas.

## Instrucciones de configuración

- Requisitos previos

Python 3.10 o superior
Git

### Instalación local

1. Clonar el repositorio
   git clone https://github.com/jairocalde/API.git
   cd API

2. Crea y activa un entorno virtual
   En Windows iniciar:
   
   python -m venv venv
   venv\Scripts\activate

3. Instala las dependencias
   pip install -r requirements.txt

### Ejecuta la aplicación
   uvicorn src.main:app --reload

   La API estará disponible en: http://127.0.0.1:8000
   La documentación interactiva (Swagger): http://127.0.0.1:8000/docs

## Documentación de la API

### Crear un mensaje
Endpoint
POST /api/messages

Descripción
Recibe un mensaje de chat, valida su estructura, procesa su contenido y lo almacena en la base de datos.

Ejemplo de request:
{
  "message_id": "msg-123456",  ## Se debe de variar el id del mensaje
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}

Ejemplo de respuesta exitosa
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
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}

### Obtener mensajes por sesión
Endpoint
GET /api/messages/{session_id}
Descripción
Devuelve todos los mensajes asociados a una sesión específica.

Parámetros de consulta opcionales
| Parámetro | Descripción                               |
| --------- | ----------------------------------------- |
| limit     | Número máximo de mensajes                 |
| offset    | Desplazamiento para paginación            |
| sender    | Filtrar por remitente (`user` o `system`) |

## Instrucciones para pruebas
Las pruebas fueron implementadas utilizando pytest, incluyendo pruebas unitarias y de integración para los endpoints y la lógica de negocio.

Ejecutar las pruebas
Desde la raíz del proyecto:
pytest

Cobertura de pruebas
Las pruebas cubren:
- Endpoints de la API
- Validaciones de datos
- Procesamiento de mensajes
- Manejo de errores
  
El objetivo es mantener una cobertura mínima del 80%, conforme a los requisitos de la prueba técnica.

Notas finales:

La base de datos utilizada es SQLite, elegida por su simplicidad y portabilidad.
La API sigue estándares REST y buenas prácticas de desarrollo backend.
FastAPI proporciona documentación automática accesible desde /docs.

## Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web async |
| SQLAlchemy | 2.0.25 | ORM para base de datos |
| Pydantic | 1.10.13 | Validación de datos |
| SQLite | 3.x | Base de datos embebida |
| Pytest | 7.4.3 | Framework de pruebas |
| Uvicorn | 0.24.0 | Servidor ASGI |
