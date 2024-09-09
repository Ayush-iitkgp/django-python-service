from argostranslate.tags import Tag


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
