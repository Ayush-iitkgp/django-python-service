import pytest
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_translate_html_success(
    client_api_token: APIClient, request_html_payload: dict, translated_html_content: str
) -> None:
    response = client_api_token.post(path="/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert "translated_content" in body
    assert body["translated_content"] == translated_html_content


def test_translate_html_403_error(client_api_token: APIClient, request_html_payload: dict) -> None:
    client_api_token.credentials(HTTP_AUTHORIZATION="Api-Key random key")
    response = client_api_token.post("/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_translate_html_400_error(client_api_token: APIClient, request_html_payload: dict) -> None:
    request_html_payload.pop("format")
    response = client_api_token.post("/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
