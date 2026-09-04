"""
Basic tests for ROSE backend
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "🌹 ROSE is ready for research"

def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_status():
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "components" in data

def test_create_session():
    """Test creating chat session"""
    response = client.post("/api/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "created_at" in data

def test_create_experiment():
    """Test creating experiment"""
    response = client.post("/api/experiments", json={
        "name": "Test Experiment",
        "description": "Test description",
        "config": {"model": "test"}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Experiment"
    assert data["status"] == "created"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
