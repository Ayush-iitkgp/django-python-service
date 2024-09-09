from argostranslate.tags import Tag
from bs4 import BeautifulSoup


def print_tag(tag: Tag, level: int = 0) -> None:
    indent = "  " * level  # Indentation for nested tags

    # Print the tag if it's an instance of the Tag class
    if isinstance(tag, Tag):
        print(f"{indent}Tag(translateable={tag.translateable}, children=[")
        for child in tag.children:
            print_tag(child, level + 1)
        print(f"{indent}])")
    # If it's a string, just print the string
    elif isinstance(tag, str):
        print(f"{indent}'{tag}'")


def get_soup(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def compare_html_structure(expected_html: str, translated_html: str) -> bool:
    expected_soup = get_soup(expected_html)
    translated_soup = get_soup(translated_html)

    return str(expected_soup.prettify()) == str(translated_soup.prettify())
