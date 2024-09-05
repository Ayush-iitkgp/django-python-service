import uuid
from uuid import UUID

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from translation.models import Translation

pytestmark = pytest.mark.django_db


def test_get_translation_success(client_api_token: APIClient, user_id: UUID, translation: Translation) -> None:
    response = client_api_token.get(f"/v1/translation/{user_id}?limit=10&offset=0")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    result = body["results"][0]
    assert result["user_id"] == str(user_id)
    assert "count" in body


def test_get_translation_403_error(client_api_token: APIClient, user_id: UUID, translation: Translation) -> None:
    client_api_token.credentials(HTTP_AUTHORIZATION="Api-Key random key")
    response = client_api_token.get(f"/v1/translation/{user_id}?limit=10&offset=0")
    # TODO: Investigate why wrong Api-Key returning 403 instead of 401 error
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_translation_404_error(client_api_token: APIClient, translation: Translation) -> None:
    user_id = uuid.uuid4()
    response = client_api_token.get(f"/v1/translation/{user_id}?limit=10&offset=0")
    assert response.status_code == status.HTTP_404_NOT_FOUND
