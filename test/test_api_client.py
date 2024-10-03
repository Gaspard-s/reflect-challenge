import pytest
import os
from unittest.mock import patch
from src.api_client import LuccaAPIClient
from dotenv import load_dotenv


# Charger les variables d'environnement pour les tests
load_dotenv(dotenv_path='tests/.env.test')

@pytest.fixture
def api_client():
    return LuccaAPIClient()

@patch('src.api_client.requests.get')
def test_get_users_success(mock_get, api_client):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "items": [
                {"id": 1, "name": "John Doe", "department": {"name": "Engineering"}, "rolePrincipal": {"name": "Developer"}, "legalEntity": {"name": "Company A"}, "applicationData": {"theoreticalRemuneration": {"value": 50000}}}
            ]
        }
    }

    users = api_client.get_users()
    assert len(users) == 1
    assert users[0]['name'] == "John Doe"

@patch('src.api_client.requests.get')
def test_get_users_rate_limit(mock_get, api_client):
    # Simuler une réponse de limite de taux
    mock_response = mock_get.return_value
    mock_response.status_code = 429
    mock_response.headers = {'Retry-After': '1'}
    mock_response.json.return_value = {"message": "rate limit exceeded"}

    users = api_client.get_users()
    assert users == []

@patch('src.api_client.requests.get')
def test_get_departments_success(mock_get, api_client):
    # Simuler une réponse API réussie pour les départements
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "items": [
                {"id": 1, "name": "Engineering", "hierarchy": "/engineering/", "parentId": None, "headID": 10, "users": [], "currentUsers": [], "currentUsersCount": 0}
            ]
        }
    }

    departments = api_client.get_departments()
    assert len(departments) == 1
    assert departments[0]['name'] == "Engineering"

@patch('src.api_client.requests.get')
def test_get_departments_rate_limit(mock_get, api_client):
    # Simuler une réponse de limite de taux pour les départements
    mock_response = mock_get.return_value
    mock_response.status_code = 429
    mock_response.headers = {'Retry-After': '1'}
    mock_response.json.return_value = {"message": "rate limit exceeded"}

    departments = api_client.get_departments()
    assert departments == []

def test_api_client_initialization_missing_token(monkeypatch):
    # Supprimer la variable d'environnement LUCCA_API_TOKEN
    monkeypatch.delenv("LUCCA_API_TOKEN", raising=False)

    with pytest.raises(ValueError) as excinfo:
        LuccaAPIClient()
    assert "Le token API est manquant." in str(excinfo.value)
