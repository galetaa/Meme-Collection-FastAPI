import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_file():
    file_path = "test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(b"test data")

    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": f})

    assert response.status_code == 200
    data = response.json()
    assert "file_url" in data

    import os
    os.remove(file_path)
