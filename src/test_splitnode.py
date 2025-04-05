# Tests for splitnode logic
# python imports
import unittest

# application imports
from textnode import TextNode, TextType
from splitnode import split_nodes_delimiter


class TestSplitNode(unittest.TestCase):
    # Check expected length, text, and type
    # Test with known good input
    def test_splitnode_single_formatting_node(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]

        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # split into 3 TextNodes
        # self.assertEqual(len(new_nodes), 3)
        for result_node, expected_node in zip(new_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)

    # Test that if we have plain text, it simply appends to the result
    def test_splitnode_nothing_to_do(self):
        node = TextNode("Plain text here bud.", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    # Test handling code formatting at the front resulting in "" empty node
    def test_splitnode_upfront_formatting(self):
        expected_nodes = [
            TextNode("Bold Start", TextType.BOLD),
            TextNode(" to the day.", TextType.NORMAL),
        ]
        node = TextNode("**Bold Start** to the day.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        for result, expected in zip(new_nodes, expected_nodes):
            self.assertEqual(result.text, expected.text)
            self.assertEqual(result.text_type, expected.text_type)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
