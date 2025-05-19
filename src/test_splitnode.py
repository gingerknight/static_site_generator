# Tests for splitnode logic
# python imports
import unittest

from splitnode import (split_nodes_delimiter, split_nodes_image,
                       split_nodes_link, text_to_textnodes)
# application imports
from textnode import TextNode, TextType


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

    # ========================= Tests for split_nodes_images =========================
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertIsNotNone(new_nodes)
        self.assertEqual(new_nodes, [node])

    def test_split_images_with_bold(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some **bold text**",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some **bold text**", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_no_leading_text(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and some text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_with_special_chars(self):
        node = TextNode(
            "Check this ![an image: cat & dog](https://img.com/catdog.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.NORMAL),
                TextNode("an image: cat & dog", TextType.IMAGE, "https://img.com/catdog.png"),
            ],
            new_nodes,
        )

    def test_split_images_malformed(self):
        node = TextNode("Bad image ![alt](https://img.com/image.png", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Bad image ![alt](https://img.com/image.png", TextType.NORMAL)],
            new_nodes,
        )

    def test_split_images_adjacent(self):
        node = TextNode("![img1](http://url1)![img2](https://url2)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "http://url1"),
                TextNode("img2", TextType.IMAGE, "https://url2"),
            ],
            new_nodes,
        )

    def test_split_images_with_newlines(self):
        node = TextNode("Some text\n![alt](https://url)\nmore text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text\n", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, "https://url"),
                TextNode("\nmore text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_same_image_repeated(self):
        node = TextNode("![cat](https://cat_link) and again ![cat](https://cat_link)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://cat_link"),
                TextNode(" and again ", TextType.NORMAL),
                TextNode("cat", TextType.IMAGE, "https://cat_link"),
            ],
            new_nodes,
        )

    def test_split_images_inside_sentence_punctuation(self):
        node = TextNode("This is ![img](https://inside_the_mindhive_url), and this too.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("img", TextType.IMAGE, "https://inside_the_mindhive_url"),
                TextNode(", and this too.", TextType.NORMAL),
            ],
            new_nodes,
        )

    # TODO: Add more test cases for split_images:
    # """
    # Image with unusual alt text
    #    Alt text with punctuation, numbers, or parentheses: ![img #1](url)
    # Image markdown with missing parts (broken syntax)
    #     Missing closing ), or missing ![, etc. These shouldn’t match or should be ignored gracefully.
    # """

    # TODO: Add test cases for split_nodes_link
    # ========================= Tests for split_nodes_links =========================
    def test_split_links(self):
        node = TextNode(
            "This is text with an [good_link](https://the_mighty_googles.com/) and another [second link](https://the_mighty_youtubes.com/)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("good_link", TextType.LINK, "https://the_mighty_googles.com/"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second link", TextType.LINK, "https://the_mighty_youtubes.com/"),
            ],
            new_nodes,
        )

    def test_split_images_no_links(self):
        node = TextNode("This is text with no links", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertIsNotNone(new_nodes)
        self.assertEqual(new_nodes, [node])

    def test_split_links_with_bold(self):
        node = TextNode(
            "This is text with an [link here](https://amazon_buyers_club.org) and some **bold text**",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link here", TextType.LINK, "https://amazon_buyers_club.org"),
                TextNode(" and some **bold text**", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_no_leading_text(self):
        node = TextNode("[golf_links](https://denison_county_golfclub.net) and some text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("golf_links", TextType.LINK, "https://denison_county_golfclub.net"),
                TextNode(" and some text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_with_special_chars(self):
        node = TextNode(
            "Check this [a link for: cats & dogs](https://the_bestest_friends_clubs.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.NORMAL),
                TextNode("a link for: cats & dogs", TextType.LINK, "https://the_bestest_friends_clubs.com"),
            ],
            new_nodes,
        )

    def test_split_link_malformed(self):
        node = TextNode("Bad image [url_link](https://missing_Parens.com/image.png", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Bad image [url_link](https://missing_Parens.com/image.png", TextType.NORMAL)],
            new_nodes,
        )

    def test_split_links_adjacent(self):
        node = TextNode("[uri1](http://url1)[url2](https://url2)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("uri1", TextType.LINK, "http://url1"),
                TextNode("url2", TextType.LINK, "https://url2"),
            ],
            new_nodes,
        )

    def test_split_links_with_newlines(self):
        node = TextNode("Some text\n[newline](https://gottem)\nmore text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text\n", TextType.NORMAL),
                TextNode("newline", TextType.LINK, "https://gottem"),
                TextNode("\nmore text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_same_image_repeated(self):
        node = TextNode("[cat](https://cat_link) and again [cat](https://cat_link)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.LINK, "https://cat_link"),
                TextNode(" and again ", TextType.NORMAL),
                TextNode("cat", TextType.LINK, "https://cat_link"),
            ],
            new_nodes,
        )

    def test_split_links_inside_sentence_punctuation(self):
        node = TextNode("This is [mindhive link](https://inside_the_mindhive_url), and this too.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("mindhive link", TextType.LINK, "https://inside_the_mindhive_url"),
                TextNode(", and this too.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        nodes = [
            TextNode("This is ", TextType.NORMAL, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.NORMAL, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.NORMAL, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.NORMAL, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
