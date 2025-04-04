from fastapi.testclient import TestClient
from parsecv.app.main import app
from pathlib import Path
from argon2 import PasswordHasher
from parsecv.app.services.auth_config import hashed_password
import requests
import responses

test_client = TestClient(app)

RESOURCE_PATH = f"{Path(__file__).parent.parent}/resources"

ph = PasswordHasher()

@responses.activate
def test_parse_endpoint():
    extractor_response = responses.Response(
        method="POST",
        url="http://localhost:9090/extract",
        status=200,
        json={"Example text" : "example"}
    )

    responses.add(extractor_response)

    with open(f"{RESOURCE_PATH}/test_resume.pdf", "rb") as f:
        files = {"resume": ("file.pdf", f, "application/pdf")}
        response = test_client.post("/api/parse", headers={"apiKey" : "test-api-key"}, files=files)
    
    assert response.status_code == 200
    assert response.json()["info"] is not None

@responses.activate
def test_parse_text():
    with open(f"{RESOURCE_PATH}/test_resume_text.txt", "r") as f:
        extractor_text = f.read()
    
    extractor_response = responses.Response(
        method="POST",
        url="http://localhost:9090/extract",
        status=200,
        body=extractor_text
    )

    responses.add(extractor_response)

    with open(f"{RESOURCE_PATH}/test_resume.pdf", "rb") as f:
        files = {"resume": ("file.pdf", f, "application/pdf")}
        response = test_client.post("/api/parse", headers={"apiKey" : "test-api-key"}, files=files)
    
    assert response.status_code == 200
    assert response.json()["info"]["phone"] == "(123) 456-7890"


def test_non_pdf():
    with open(f"{RESOURCE_PATH}/text_file.txt", "rb") as f:
        files = {"resume": ("test_file.txt", f)}
        response = test_client.post("/api/parse",headers={"apiKey" : "test-api-key"}, files=files)
    
    assert response.status_code == 400
    assert response.json()["message"] == "File must be a PDF"

def test_incorrect_api_key():
    with open(f"{RESOURCE_PATH}/text_file.txt", "rb") as f:
        files = {"resume": ("test_file.txt", f)}
        response = test_client.post("/api/parse",headers={"apiKey" : "incorrect-key"}, files=files)
    
    assert response.status_code == 401
    assert response.json()["message"] == "Invalid auth credentials"

def test_extractor_unavailable():
    with open(f"{RESOURCE_PATH}/test_resume.pdf", "rb") as f:
        files = {"resume": ("file.pdf", f, "application/pdf")}
        response = test_client.post("/api/parse", headers={"apiKey" : "test-api-key"}, files=files)
    
    assert response.status_code == 500
    assert response.json()["detail"] == "There was an error calling the backend text extractor service"
        
