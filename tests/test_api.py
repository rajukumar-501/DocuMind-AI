from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "DocuMind AI" in response.json()["message"]


def test_upload_rejects_non_pdf():
    response = client.post(
        "/upload/",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_rejects_invalid_pdf_content():
    response = client.post(
        "/upload/",
        files={"file": ("notes.pdf", b"not actually a pdf", "application/pdf")},
    )
    assert response.status_code == 400


def test_query_rejects_short_question():
    response = client.post(
        "/query/",
        json={"document_id": "12345678-1234-1234-1234-123456789012", "question": "?"}
    )
    assert response.status_code == 422
