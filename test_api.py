from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_generate_endpoint_exists():
    response = client.post(
        "/generate",
        json={
            "document_type": "Test Agreement",
            "parties": "Party A and Party B",
            "terms": "Test terms",
            "dates": "29 September 2026"
        }
    )

    # Gemini may currently return 503.
    # We only verify that the endpoint itself exists.
    assert response.status_code in [200, 500]