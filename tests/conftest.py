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
def original_html_content() -> Generator[str, None, None]:
    yield (
        "<div><h2 class='editor-heading-h2' dir='ltr'>"
        "<span>hallo1 as headline</span></h2><p class='editor-paragraph' dir='ltr'>"
        "<br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph</span></p>"
        "<p class='editor-paragraph' dir='ltr'><span>hallo3 as paragraph with </span><b>"
        "<strong class='editor-text-bold'>bold</strong></b><span> inline</span></p></div>"
    )


@pytest.fixture
def translated_html_content() -> Generator[str, None, None]:
    yield (
        '<div><h2 class="editor-heading-h2" dir="ltr">'
        '<span>hallo1 als Überschrift</span></h2><p class="editor-paragraph" dir="ltr"><br/></p>'
        '<p class="editor-paragraph" dir="ltr"><span>hallo2 als Absatz</span></p>'
        '<p class="editor-paragraph" dir="ltr"><span>hallo3 als Absatz mit'
        ' </span><b><strong class="editor-text-bold">fett</strong></b><span> Inline</span></p></div>'
    )


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
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    yield client


@pytest.fixture
def request_payload(user_id: UUID, original_content: str) -> Generator[dict, None, None]:
    yield {"user_id": user_id, "original_content": original_content, "format": "text"}


@pytest.fixture
def request_html_payload(user_id: UUID, original_html_content: str) -> Generator[dict, None, None]:
    yield {"user_id": user_id, "original_content": original_html_content, "format": "html"}
