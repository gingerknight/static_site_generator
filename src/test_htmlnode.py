# python imports
import unittest

# application imports
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    # HTMLNode init all params case
    def test_htmlnode_tag_value_params(self):
        # self, tag, value, children, props
        node = HTMLNode("h1", "Title Home Page", None, None)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title Home Page")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html(self):
        """
        return a string that represents the HTML of attributes of the node

        {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        returns (leading space before key):
         href="https://www.google.com" target="_blank"
         """
        node = HTMLNode("p", "google link here", None, {"href":"https://www.google.com", "target":"_blank"})
        props_to_html_return = node.props_to_html()
        self.assertEqual(props_to_html_return, ' href="https://www.google.com" target="_blank"')

    def test_to_html_error(self):
        """
        test that to_html raises the NotImplementedError
        """
        node = HTMLNode("p", "google link here", None, {"href":"https://www.google.com", "target":"_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
class TestLeafNode(unittest.TestCase):
    # LeafNode tests
    def test_leafnode_params(self):
        leaf_node = LeafNode("p", "I'm a paragraph")
        self.assertEqual(leaf_node.tag, "p")
        self.assertEqual(leaf_node.value, "I'm a paragraph")
        self.assertEqual(leaf_node.children, [])

    def test_leafnode_to_html_p(self):
        leaf_node = LeafNode("p", "I'm a paragraph")
        self.assertEqual(leaf_node.to_html(), "<p>I'm a paragraph</p>")

    def test_leafnode_to_html_a(self):
        prop_dict = {"href":"https://www.google.com", "target":"_blank"}
        leaf_node = LeafNode("a", "Click Me Damnit!", None, prop_dict)
        self.assertEqual(leaf_node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Click Me Damnit!</a>")

    def test_leafnode_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None, None, None)

    def test_leaf_to_html_no_tag(self):
        leaf_node = LeafNode(None, "Hello, world!")
        self.assertEqual(leaf_node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()