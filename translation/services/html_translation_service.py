import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from argostranslate.tags import Tag
from bs4 import BeautifulSoup
from translatehtml import itag_of_soup, soup_of_itag

from translation.services.translation_service import TranslationService

logger = logging.getLogger(__name__)

NON_TRANSLATEABLE_TAGS = [
    "address",
    "applet",
    "audio",
    "canvas",
    "code",
    "embed",
    "script",
    "style",
    "time",
    "video",
]


class HTMLTranslationService:
    @classmethod
    def translate_html(cls, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        tag = itag_of_soup(soup)
        translated_tag = cls.parallel_translate_tags(tag=tag)
        translated_soup = soup_of_itag(translated_tag)
        logger.debug(f"Translated tag: {translated_soup}")
        return str(translated_soup)

    @classmethod
    def snyc_translate_tags(cls, tag: Union[Tag, str]) -> Union[Tag, str]:
        """Translate an ITag or str

        Recursively takes either an ITag or a str, modifies it in place, and returns the translated tag tree

        Args:
            tag: The tag tree to translate

        Returns:
            The translated tag tree
        """
        if type(tag) is str:
            return cls.translate_preserve_formatting(tag)
        elif tag.translateable is False:
            return tag
        else:
            tag.children = [cls.snyc_translate_tags(child) for child in tag.children]

        return tag

    @classmethod
    def parallel_translate_tags(cls, tag: Union[Tag, str]) -> Union[Tag, str]:
        """Translate an ITag or str in parallel.

        Recursively takes either an ITag or a str, modifies it in place,
        and returns the translated tag tree, utilizing parallel translation
        for child tags.

        Args:
            tag: The tag tree to translate.

        Returns:
            The translated tag tree.
        """
        # Base case: if it's a string, translate it
        if isinstance(tag, str):
            # Only translate the text content, leave tags intact
            return cls.translate_preserve_formatting(tag)

        if not tag.translateable:
            # If the tag is not translateable (e.g., <code> or other), return it as is
            return tag

            # Use ThreadPoolExecutor for parallel translation of child text nodes
        children = tag.children

        with ThreadPoolExecutor() as executor:
            future_to_child = {executor.submit(cls.parallel_translate_tags, child): child for child in children}
            translated_children = [future.result() for future in future_to_child]

        tag.children = translated_children
        return tag

    @classmethod
    def translate_preserve_formatting(cls, input_text: str) -> str:
        """Translates but preserves a space if it exists on either end of translation.
        Args:
            input_text: The text to translate
        Returns:
            The translated text
        """
        translated_text = TranslationService.translate_text(input_text)
        if len(input_text) > 0:
            if input_text[0] == " " and not (len(translated_text) > 0 and translated_text[0] == " "):
                translated_text = " " + translated_text
            if input_text[-1] == " " and not (len(translated_text) > 0 and translated_text[-1] == " "):
                translated_text = translated_text + " "
        return translated_text

    @classmethod
    def depth(cls, tag: Tag | str) -> int:
        """Returns the depth of an ITag or str.

        A str has depth 0, ITag([]) has depth 0, ITag(['str']) has depth 1.

        Args:
            tag: The ITag or string to get the depth of.
        """
        if type(tag) is str:
            return 0
        if len(tag.children) == 0:
            return 0
        return max([cls.depth(t) for t in tag.children])
