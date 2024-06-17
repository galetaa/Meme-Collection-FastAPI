import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import Meme

client = TestClient(app)

# Создаем таблицы до начала тестов
Base.metadata.create_all(bind=engine)


# Удаляем таблицы после завершения тестов
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_meme():
    response = client.post(
        "/memes/",
        json={"title": "Test Meme", "description": "This is a test meme", "image_url": "http://example.com/test.jpg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Meme"
    assert data["description"] == "This is a test meme"
    assert data["image_url"] == "http://example.com/test.jpg"
    assert "id" in data


def test_get_memes():
    response = client.get("/memes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_get_meme():
    response = client.post(
        "/memes/",
        json={"title": "Test Meme 2", "description": "This is another test meme",
              "image_url": "http://example.com/test2.jpg"}
    )
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Meme 2"
    assert data["description"] == "This is another test meme"
    assert data["image_url"] == "http://example.com/test2.jpg"


def test_update_meme():
    response = client.post(
        "/memes/",
        json={"title": "Test Meme 3", "description": "This is a test meme to update",
              "image_url": "http://example.com/test3.jpg"}
    )
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = client.put(
        f"/memes/{meme_id}",
        json={"title": "Updated Meme", "description": "This is an updated test meme",
              "image_url": "http://example.com/updated.jpg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Meme"
    assert data["description"] == "This is an updated test meme"
    assert data["image_url"] == "http://example.com/updated.jpg"


def test_delete_meme():
    response = client.post(
        "/memes/",
        json={"title": "Test Meme 4", "description": "This is a test meme to delete",
              "image_url": "http://example.com/test4.jpg"}
    )
    assert response.status_code == 200
    meme_id = response.json()["id"]

    response = client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Meme 4"

    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 404
