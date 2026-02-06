# src/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# URL de conexión a la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat_messages.db"

# Crear el motor de base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    poolclass=StaticPool,  # Para SQLite en desarrollo
    echo=True  # Muestra las consultas SQL en consola (útil para debug)
)


# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base para los modelos
Base = declarative_base()

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()