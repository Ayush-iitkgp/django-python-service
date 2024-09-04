import os
from typing import Generator
from uuid import UUID, uuid4

import django
import pytest


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()


pytest_configure()

from rest_framework.test import APIClient  # noqa: E402
from rest_framework_api_key.models import APIKey  # noqa: E402

from translation.models import Translation  # noqa: E402


@pytest.fixture
def user_id() -> Generator[UUID, None, None]:
    yield uuid4()


@pytest.fixture
def original_content() -> Generator[str, None, None]:
    yield "Hello World!"


@pytest.fixture
def translated_content() -> Generator[str, None, None]:
    yield "Hallo Welt!"


@pytest.fixture
def translation(user_id: UUID, original_content: str, translated_content: str) -> Generator[Translation, None, None]:
    yield Translation.objects.create(
        user_id=user_id,
        original_content=original_content,
        translated_content=translated_content,
    )


@pytest.fixture
def api_key() -> Generator[str, None, None]:
    project_api_key, key = APIKey.objects.create_key(name="Test API Key")
    yield key


@pytest.fixture
def client_api_token(api_key: str) -> Generator[APIClient, None, None]:
    client = APIClient()
    client.credentials(API_KEY=api_key)
    yield client
