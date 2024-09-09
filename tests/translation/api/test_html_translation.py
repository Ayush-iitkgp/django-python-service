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
    request_html_payload["original_content"] = content
    response = client_api_token.post(path="/v1/translation/translate", data=request_html_payload)
    assert response.status_code == status.HTTP_201_CREATED
    # body = response.json()
    # german_html = open(f"{prefix}/de/{filename}.html", "r").read()
    # assert body["translated_content"] == german_html
