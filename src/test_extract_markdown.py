# Tests for extracting markdown images and links logic
# python imports
import unittest

# application imports
from splitnode import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "Here is one ![alt1](https://img1.com/image.png) and here is another ![alt2](https://img2.com/pic.jpg)"
        expected = [
            ("alt1", "https://img1.com/image.png"),
            ("alt2", "https://img2.com/pic.jpg"),
        ]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_extract_no_images(self):
        self.assertEqual(extract_markdown_images("Nothing here!"), [])

    def test_extract_images_with_special_chars(self):
        text = "Check this ![an image: cat & dog](https://img.com/catdog.png)"
        expected = [("an image: cat & dog", "https://img.com/catdog.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_malformed_image_syntax(self):
        text = "Bad image ![alt](https://img.com/image.png"
        self.assertEqual(extract_markdown_images(text), [])

    ## -------------------------- Markdown Link Tests -------------------------- ##
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://test_your_might.com/@ricketyrickety_wrecked)"
        )
        self.assertListEqual(
            [("link", "https://test_your_might.com/@ricketyrickety_wrecked")], matches
        )

    def test_extract_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_link_with_formatting_in_text(self):
        text = "A [**bold link**](https://bold.com)"
        expected = [("**bold link**", "https://bold.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_malformed_link(self):
        text = "Bad link [link](missing_paren"
        self.assertEqual(extract_markdown_links(text), [])
