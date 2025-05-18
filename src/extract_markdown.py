# python imports
import re

# application imports


def extract_markdown_images(text):
    """
    takes raw markdown text and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images

    Example:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    :param text: markdown text
    :return __: list of tuples [(alt_text, url)]
    """

    alt_uri_regex = re.compile(r"\!\[(.*?)\]\((htt.*?)\)")
    matches = re.findall(alt_uri_regex, text)
    return matches


def extract_markdown_links(text):
    """
    extracts markdown links instead of images. It should return tuples of anchor text and URLs.
    Example:
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    :param text: markdown text
    :return __: list of tuples
    """

    alt_uri_link_regex = re.compile(r"(?<!\!)\[(.*?)\]\((https?:\/\/[^\s)]+)\)")
    matches = re.findall(alt_uri_link_regex, text)
    return matches
