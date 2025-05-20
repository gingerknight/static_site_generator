# python imports
import unittest

# application imports
from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_textnode_to_htmlnode(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_to_htmlnode_bold(self):
        node = TextNode("Bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text node")

    def test_textnode_to_htmlnode_italics(self):
        node = TextNode("Italics text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italics text node")

    def test_textnode_to_htmlnode_link(self):
        node = TextNode("Click here phishing link!", TextType.LINK, "https://hackerwebs.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here phishing link!")
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://hackerwebs.com/">Click here phishing link!</a>',
        )

    def test_textnode_to_htmlnode_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


if __name__ == "__main__":
    unittest.main()
