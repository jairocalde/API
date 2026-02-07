from sqlalchemy import create_engine # Importa create_engine para crear conexión a base de datos
from sqlalchemy.orm import sessionmaker, declarative_base # Importa sessionmaker para crear fábrica de sesiones, declarative_base para crear clase base de modelos

DATABASE_URL = "sqlite:///./messages.db" # URL de conexión a SQLite. "sqlite:///./messages.db" significa: # - sqlite: motor de base de datos
# - ///: ruta relativa
# - ./messages.db: archivo en directorio actual

engine = create_engine( # Crea el motor (engine) de SQLAlchemy
    DATABASE_URL,
    connect_args={"check_same_thread": False} # Necesario para SQLite con FastAPI
)

SessionLocal = sessionmaker( # Crea una fábrica de sesiones (SessionLocal)
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() # Crea la clase base para todos los modelos SQLAlchemy, Todos los modelos heredarán de esta clase

def get_db(): # Función de dependencia para FastAPI
    db = SessionLocal() # Crea una nueva sesión
    try:   # Entrega la sesión al endpoint
        yield db
    finally:
        db.close() # Cierra la sesión siempre, incluso si hay error
