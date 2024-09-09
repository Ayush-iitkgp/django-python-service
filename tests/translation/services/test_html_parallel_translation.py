import pytest
from bs4 import BeautifulSoup
from rest_framework.test import APIClient
from translatehtml import itag_of_soup, soup_of_itag

from app.helper import compare_html_structure, format_html
from translation.services.html_translation_service import HTMLTranslationService

pytestmark = pytest.mark.django_db


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
def test_parallel_translation_success(
    filename: str,
    client_api_token: APIClient,
    request_html_payload: dict,
) -> None:
    prefix = "tests/translation/api/data"
    file_name = f"{prefix}/en/{filename}.html"
    content = open(file_name, "r").read()
    content = format_html(content)
    soup = BeautifulSoup(content, "html.parser")
    tag = itag_of_soup(soup)
    german_translation = HTMLTranslationService.parallel_translate_tags(tag)
    german_translation = soup_of_itag(german_translation)
    expected_german_html = open(f"{prefix}/de/{filename}.html", "r").read()
    expected_german_html = format_html(expected_german_html)
    assert compare_html_structure(expected_german_html, str(german_translation))
