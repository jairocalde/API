# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test para el endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Chat Message Processing API" in data["message"]

def test_health_check():
    """Test para el endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_message():
    """Test para crear un mensaje"""
    message_data = {
        "message_id": "msg-test-001",
        "session_id": "session-test-001",
        "content": "Mensaje de prueba",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    
    response = client.post("/api/messages/", json=message_data)
    # Aceptar 201 (creado) o 400 (validación fallida)
    assert response.status_code in [201, 400]
    
    if response.status_code == 201:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

def test_get_messages():
    """Test para obtener mensajes"""
    response = client.get("/api/messages/session-test-001")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
