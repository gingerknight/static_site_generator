#! /usr/bin/python3
from textnode import TextNode, TextType


def main():
    my_node = TextNode("Sample Text", TextType.LINK, "https://www.google.com")  # noqa: F841


main()
