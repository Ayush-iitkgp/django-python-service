import time

import pytest
from bs4 import BeautifulSoup
from translatehtml import itag_of_soup

from translation.services.html_translation_service import HTMLTranslationService


def generate_large_html(num_sections: int, num_paragraphs: int) -> str:
    """
    Generate a large HTML string with a nested structure.

    Args:
        num_sections (int): Number of sections to include.
        num_paragraphs (int): Number of paragraphs per section.

    Returns:
        str: The generated large HTML string.
    """
    html_content = []

    for i in range(num_sections):
        html_content.append(f"<section>\n    <h2>Section {i + 1}</h2>")
        for j in range(num_paragraphs):
            html_content.append(
                f"    <p>This is paragraph {j + 1} in section {i + 1}. It contains a "
                f"lot of text to simulate a large HTML document. " * 10 + "</p>"
            )
        html_content.append("</section>")

    return "\n".join(html_content)


@pytest.mark.parametrize(
    "num_sections, num_paragraphs",
    [
        (1, 2),
        (2, 4),
    ],
)
def test_translation_performance(num_sections: int, num_paragraphs: int) -> None:
    large_html = generate_large_html(num_sections, num_paragraphs)

    soup = BeautifulSoup(large_html, "html.parser")
    tag = itag_of_soup(soup)
    start_time = time.time()
    _ = HTMLTranslationService.snyc_translate_tags(tag)
    end_time = time.time()
    sync_duration = end_time - start_time

    start_time = time.time()
    _ = HTMLTranslationService.translate_html(large_html)
    end_time = time.time()
    parallel_duration = end_time - start_time

    assert sync_duration > parallel_duration, "Parallel translation should be faster than sync translation."


# Notes: Turns out multi-processing solution is not always fast compared to multi-threaded solution
# @pytest.mark.parametrize(
#     "num_sections, num_paragraphs",
#     [
#         (1, 2),
#         (2, 4),
#     ],
# )
# def test_translation_performance_thread_vs_pool(num_sections: int, num_paragraphs: int) -> None:
#     large_html = generate_large_html(num_sections, num_paragraphs)
#
#     soup = BeautifulSoup(large_html, "html.parser")
#     tag = itag_of_soup(soup)
#     start_time = time.time()
#     _ = HTMLTranslationService.parallel_thread_translate_tags(tag)
#     end_time = time.time()
#     thread_duration = end_time - start_time
#
#     start_time = time.time()
#     _ = HTMLTranslationService.parallel_process_translate_tags(large_html)
#     end_time = time.time()
#     process_duration = end_time - start_time
#
#     assert (
#         thread_duration > process_duration
#     ), "Parallel process translation should be faster than parallel thread translation."
