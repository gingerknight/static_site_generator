#! /usr/bin/python3

import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    # Text String and Text Type test cases
    def test_text_and_type_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is different node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_equal_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # Test url parameter default
    def test_url_is_none(self):
        node = TextNode("Url is missing", TextType.ITALIC)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
