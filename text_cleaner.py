import re


def clean_speak_text(text):
    """
    removes apostrophe (') and quotation marks (") from a given text
    :param text: a string of text
    :type text: str
    """
    search_pattern = r"['\"]"
    print(search_pattern)
    new_text = re.sub(search_pattern, "", text)
    return new_text
