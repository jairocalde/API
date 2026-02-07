from sqlalchemy.exc import IntegrityError # Importa IntegrityError para capturar errores de restricciones de BD
from src.database.models import MessageModel # Importa el modelo SQLAlchemy para la tabla messages


class MessageRepository: # Clase repositorio - maneja todas las operaciones de base de datos

    def __init__(self, db): # Constructor recibe una sesión de base de datos
        self.db = db # Sesión de SQLAlchemy

    def save_message(self, data: dict): # Guarda un mensaje en la base de datos
        try:
            message = MessageModel(**data)
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message

        except IntegrityError:
            self.db.rollback()
            raise ValueError("El message_id ya existe")

        except Exception:
            self.db.rollback()
            raise
