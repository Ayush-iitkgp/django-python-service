import logging
import time

from bs4 import BeautifulSoup
from translatehtml import itag_of_soup, soup_of_itag

from app.helper import format_html
from translation.services.html_translation_service import HTMLTranslationService

logger = logging.getLogger()


def test_munich_stadt_homepage_translation() -> None:
    filename = "tests/translation/api/data/munich_stadt.html"
    content = open(filename, "r").read()
    content = format_html(content)
    soup = BeautifulSoup(content, "html.parser")
    tag = itag_of_soup(soup)

    start_time = time.time()
    translated_tag = HTMLTranslationService.parallel_thread_translate_tags(tag)
    translated_soup = soup_of_itag(translated_tag)
    logger.debug(translated_soup)
    end_time = time.time()
    parallel_duration = end_time - start_time
    logger.debug(f"parallel duration: {parallel_duration}")
