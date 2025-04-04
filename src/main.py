#! /usr/bin/python3
from textnode import TextNode, TextType

def main():
    my_node = TextNode("Sample Text", TextType.LINK, "https://www.google.com")
    print(my_node)

main()
