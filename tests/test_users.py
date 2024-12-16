import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from app.database import get_db
    from app.main import app
    from app.models import Base
except ImportError:
    from database import get_db
    from main import app
    from models import Base

# Test database setup
TEST_DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup and teardown the database for testing
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Override dependency
@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Test cases
def test_get_users(client):
    response = client.get("/user/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user(client):
    new_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = client.post("/user/signup", json=new_user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_login_invalid_credentials(client):
    login_data = {
        "username_or_email": "nonexistentuser",
        "password": "wrongpassword"
    }
    response = client.post("/user/login", json=login_data)
    assert response.status_code == 401  # Unauthorized

def test_login_user(client):
    login_data = {
        "username_or_email": "testuser",
        "password": "password123"
    }
    response = client.post("/user/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_user_missing_field(client):
    new_user = {
        "username": "testuser",
        "password": "password123"
    }
    response = client.post("/user/signup", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_delete_user(client):
    # Ensure user exists before deleting
    client.post(
        "/user/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    response = client.delete("/user/delete-user/1")
    assert response.status_code == 204

def test_delete_nonexistent_user(client):
    response = client.delete("/user/delete-user/9999")  # Non-existent ID
    assert response.status_code == 404  # Not Found
