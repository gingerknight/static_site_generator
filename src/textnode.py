# python imports
from enum import Enum

# application imports
from htmlnode import LeafNode


class TextType(Enum):
    NORMAL = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    # convert TextNode to HTMLNode --> LeafNode
    """
    It should handle each type of the TextType enum.
    If it gets a TextNode that is none of those types, it should raise an exception.
    Otherwise, it should return a new LeafNode object.

    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    TextType.ITALIC: "i" tag, text
    TextType.CODE: "code" tag, text
    TextType.LINK: "a" tag, anchor text, and "href" prop
    TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    """
    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type.value == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type.value == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type.value == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type.value == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type.value == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
