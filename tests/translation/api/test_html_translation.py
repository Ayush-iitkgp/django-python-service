import pytest
from rest_framework import status
from rest_framework.test import APIClient

from app.helper import compare_html_structure

pytestmark = pytest.mark.django_db


def test_translate_html_success(
    client_api_token: APIClient, request_html_payload: dict, translated_html_content: str
) -> None:
    response = client_api_token.post(path="/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert "translated_content" in body
    german_translation = body["translated_content"]
    compare_html_structure(translated_html_content, german_translation)
    # assert german_translation == translated_html_content


def test_translate_html_403_error(client_api_token: APIClient, request_html_payload: dict) -> None:
    client_api_token.credentials(HTTP_AUTHORIZATION="Api-Key random key")
    response = client_api_token.post("/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_translate_html_400_error(client_api_token: APIClient, request_html_payload: dict) -> None:
    request_html_payload.pop("format")
    response = client_api_token.post("/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "filename",
    [
        "canvas_example",
        "datetime_example",
        "details_and_summary_example",
        "embed_example",
        "iframe_and_script_example",
        "input_example",
        "no_script_example",
        "object_example",
        "problem_statement_example",
        "select_and_option_example",
        "svg_example",
        "template_example",
    ],
)
def test_translate_multiple_html_success(
    filename: str,
    client_api_token: APIClient,
    request_html_payload: dict,
) -> None:
    prefix = "tests/translation/api/data"
    file_name = f"{prefix}/en/{filename}.html"
    content = open(file_name, "r").read()
    content = content.replace("\n", "").replace("\t", "").replace("  ", "")
    request_html_payload["original_content"] = content
    response = client_api_token.post(path="/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    german_html = open(f"{prefix}/de/{filename}.html", "r").read()
    german_html = german_html.replace("\n", "").replace("\t", "").replace("  ", "")
    german_translation = body["translated_content"]
    compare_html_structure(german_html, german_translation)
