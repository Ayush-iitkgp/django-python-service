import logging
from typing import Any, Union

import bs4
from argostranslate.tags import Tag
from bs4 import BeautifulSoup

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
    def translate_html(cls, html: str) -> Any:
        soup = BeautifulSoup(html, "html.parser")
        tag = cls.tag_of_soup(soup=soup)
        translated_tag = cls.translate_tags(tag=tag)
        translated_soup = cls.soup_of_tag(translated_tag)
        return translated_soup

    @classmethod
    def tag_of_soup(cls, soup: Any) -> Union[Tag, str]:
        """Returns an argostranslate.tags.ITag tree from a BeautifulSoup object.

        Args:
            soup (bs4.element.Navigablestring or bs4.element.Tag): Beautiful Soup object

        Returns:
            argostranslate.tags.ITag: Argos Translate ITag tree
        """
        if isinstance(soup, bs4.element.NavigableString):
            return str(soup)
        translateable = soup.name not in NON_TRANSLATEABLE_TAGS and soup.get("translate") != "no"
        to_return = Tag([cls.tag_of_soup(content) for content in soup.contents], translateable)
        to_return.soup = soup
        return to_return

    @classmethod
    def translate_tags(cls, tag: Union[Tag, str]) -> Union[Tag, str]:
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
        elif cls.depth(tag) == 2:
            tag_injection = cls.inject_tags_inference(tag)
            if tag_injection is not None:
                logger.info("translate_tags", "tag injection successful")
                return tag_injection
        else:
            tag.children = [cls.translate_tags(child) for child in tag.children]

        return tag

    @classmethod
    def soup_of_tag(cls, tag: Any) -> Any:
        """Returns a BeautifulSoup object from an Argos Translate ITag.

        Args:
            tag (argostranslate.tags.ITag): ITag object to convert to Soup

        Returns:
            bs4.elements.BeautifulSoup: BeautifulSoup object
        """
        if isinstance(tag, str):
            logger.info(f"soup_of_tag: tag is {tag}")
            return bs4.element.NavigableString(tag)
        soup = tag.soup
        soup.contents = [cls.soup_of_tag(child) for child in tag.children]
        return soup

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

    @classmethod
    def inject_tags_inference(cls, tag: Tag) -> Tag | None:
        """Returns translated tag tree with injection tags, None if not possible

        tag is only modified in place if tag injection is successful.

        Args:
            underlying_translation: The translation to apply to the tags.
            tag: A depth=2 tag tree to attempt injection on.

        Returns:
            A translated version of tag, None if not possible to tag inject
        """
        MAX_SEQUENCE_LENGTH = 200

        text = tag.text()
        if len(text) > MAX_SEQUENCE_LENGTH:
            return None

        translated_text = cls.translate_preserve_formatting(text)

        class InjectionTag:
            """

            Attributes:
                text: The text of the tag
                tag: The depth 1 ITag it represents
                injection_index: The index in the outer translated string that
                        this tag can be injected into.
            """

            def __init__(self, text: str, tag: Tag):
                self.text = text
                self.tag = tag
                self.injection_index = None

        injection_tags = []
        for child in tag.children:
            if cls.depth(child) == 1:
                translated = cls.translate_preserve_formatting(child.text())
                injection_tags.append(InjectionTag(translated, child))
            elif type(child) is not str:
                logger.info("inject_tags_inference", "can't inject depth 0 ITag")
                return None

        for injection_tag in injection_tags:
            injection_index = translated_text.find(injection_tag.text)
            if injection_index != -1:
                injection_tag.injection_index = injection_index
            else:
                logger.info(
                    "inject_tags_inference",
                    "injection text not found in translated text",
                    translated_text,
                    injection_tag.text,
                )
                return None

        # Check for overlap
        injection_tags.sort(key=lambda x: x.injection_index)
        for i in range(len(injection_tags) - 1):
            injection_tag = injection_tags[i]
            next_injection_tag = injection_tags[i + 1]
            if injection_tag.injection_index + len(injection_tag.text) >= next_injection_tag.injection_index:
                logger.info(
                    "inject_tags_inference",
                    "injection tags overlap",
                    injection_tag,
                    next_injection_tag,
                )
                return None

        to_return = []
        i = 0
        for injection_tag in injection_tags:
            if i < injection_tag.injection_index:
                to_return.append(translated_text[i:injection_tag.injection_index])
            to_return.append(injection_tag.tag)
            i = injection_tag.injection_index + len(injection_tag.text)
        if i < len(translated_text):
            to_return.append(translated_text[i:])

        tag.children = to_return

        return tag
