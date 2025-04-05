# python imports
import unittest

# application imports
from htmlnode import HTMLNode

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
    

if __name__ == "__main__":
    unittest.main()