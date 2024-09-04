import os
from typing import Generator

import django
import pytest


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()


pytest_configure()

from rest_framework.test import APIClient  # noqa: E402

from translation.models import Translation  # noqa: E402


@pytest.fixture
def translation() -> Generator[Translation]:
    yield Translation.objects.create(name="Test Team")


# @pytest.fixture
# def api_key() -> API:
#     project_api_key, key = ProjectAPIKey.objects.create_key(name="Test API Key")
#     project_api_key.projects.add(project)
#     yield key


@pytest.fixture
def client_api_token(api_key: str) -> Generator[APIClient]:
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=api_key)
    yield client
