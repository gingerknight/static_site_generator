#! /usr/bin/python3
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
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
    pass


def main():
    my_node = TextNode("Sample Text", TextType.LINK, "https://www.google.com")
    print(my_node)


main()
