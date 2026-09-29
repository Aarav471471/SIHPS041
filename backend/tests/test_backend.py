from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.main import app
from app.db import Base, engine, SessionLocal
from app.models.all import User, RoleEnum
from app.security import get_password_hash

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
