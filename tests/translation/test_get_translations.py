from uuid import UUID

import pytest
from rest_framework.test import APIClient

from translation.models import Translation

pytestmark = pytest.mark.django_db


def test_get_translation_success(client_api_token: APIClient, user_id: UUID, translation: Translation) -> None:
    response = client_api_token.get(f"/v1/translation/{user_id}/?limit=10&offset=0")
    print(response)
    assert response.status_code == 200
    result = response.data["results"][0]
    assert result["user_id"] == str(user_id)
    # assert result["project"] == project_id
    # assert "label" in result
