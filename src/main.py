#! /usr/bin/python3
from textnode import TextNode, TextType


def main():
    my_node = TextNode(  # noqa: F841
        "Sample Text", TextType.LINK, "https://www.google.com"
    )


main()
