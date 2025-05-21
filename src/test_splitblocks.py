# Tests for splitmarkdown logic
# python imports
import unittest


# application imports
from splitblocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from splitblocks import BlockType


class TestSplitMarkdown(unittest.TestCase):
    # <------ Test cases for the markdown_to_blocks function ------>
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_lines(self):
        md = """
This is a paragraph with some text


- This is a list item


This is another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with some text",
                "- This is a list item",
                "This is another paragraph",
            ],
        )

    def test_markdown_to_blocks_with_leading_trailing_whitespace(self):
        md = """
    This is a paragraph with leading and trailing whitespace   
    This is another paragraph   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with leading and trailing whitespace   \n    This is another paragraph",
            ],
        )

    # <------ Test cases for the block_to_block_type function ------>
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello, World!')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list item\n- This is another unordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list item\n2. This is another ordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote
> that is in blockquote form

I'm a paragraph
> and I am a paragraph, not really
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that is in blockquote form</blockquote>"
            "<p>I'm a paragraph > and I am a paragraph, not really</p></div>",
        )
