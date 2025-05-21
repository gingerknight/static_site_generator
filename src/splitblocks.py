# python imports
import re
from enum import Enum

# application imports
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode
from splitnode import text_to_textnodes


# block type Enum
class BlockType(Enum):
    """Enum for block types"""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """
    Takes a single block of markdown text as input and returns the BlockType representing the type of block it is

        - Headings start with 1-6 # characters, followed by a space and then the heading text.
        - Code blocks must start with 3 backticks and end with 3 backticks.
        - Quote block must start with a > character.
        - Unordered list block must start with a - character, followed by a space.
        - Ordered list block must start with a number followed by a . character and a space.
            - The number must start at 1 and increment by 1 for each line.
        - If none of the above conditions are met, the block is a normal paragraph.

    Args:
        block (str): A single block of markdown text.
    Returns:
        BlockType: The type of block represented by the input string.
    """
    # regex for heading
    heading_regex = re.compile(r"^(#{1,6})\s+")
    if re.match(heading_regex, block):
        return BlockType.HEADING
    # regex for code block
    code_regex = re.compile(r"```\n(.*?)\n```", re.DOTALL)
    if re.match(code_regex, block):
        return BlockType.CODE
    # regex for quote block, space is optional
    quote_regex = re.compile(r"^>\s+?")
    if re.match(quote_regex, block):
        return BlockType.QUOTE
    # regex for unordered list block
    unordered_list_regex = re.compile(r"^-\s+")
    if re.match(unordered_list_regex, block):
        return BlockType.UNORDERED_LIST
    # regex for ordered list block
    ordered_list_regex = re.compile(r"^\d+\.\s+")
    if re.match(ordered_list_regex, block):
        return BlockType.ORDERED_LIST
    # if none of the above, return paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Takes raw markdown string (representing a full document)
    as input and returns a list of "block" strings.

    ```
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
    ```

    [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
    ]
    """
    blocks = markdown.split("\n\n")
    # Remove leading and trailing whitespace from each block
    blocks = [block.strip() for block in blocks]
    # Remove empty blocks
    blocks = [block for block in blocks if block]
    return blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Converts a full markdown document into a single parent HTML node.
    The one parent should contain many child HTMLNode objects representing nested elements.

    - Split the markdown into blocks (using the markdown_to_blocks function)
    - Loop over each block:
        - Determine the type of block (you already have a function for this)
        - Based on the type of block, create a new HTMLNode with the proper data
        - Assign the proper child HTMLNode objects to the block node.
            I created a shared text_to_children(text) function that works for all block types.
            It takes a string of text and returns a list of HTMLNodes that represent the inline
            markdown using previously created functions (think TextNode -> HTMLNode).
        - The "code" block is a bit of a special case: it should not do any inline markdown
        parsing of its children. I didn't use my text_to_children function for this block type,
        I manually made a TextNode and used text_node_to_html_node.

    - Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    children_nodes = []
    for block in blocks:
        # create helper for creating block nodes
        html_block_node = block_to_html_node(block)
        children_nodes.append(html_block_node)
    return ParentNode("div", children_nodes)


def block_to_html_node(block: str) -> HTMLNode:
    """
    Takes a single block of markdown text as input and returns an HTMLNode representing the block.
    """
    # Determine the type of block
    block_type = block_to_block_type(block)
    # based on the type of block, create a new HTMLNode with matching properties
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            # level = block.count("#")
            pass
        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            return blockquote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            pass
        case BlockType.ORDERED_LIST:
            pass
        case _:
            raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Takes a string of text, converts to TextNode objects
    then for each TextNode, converts to HTMLNode objects
    and returns a list of HTMLNode objects.
    """
    # local children list of nodes
    children = []
    # Convert the text to TextNode objects
    text_nodes = text_to_textnodes(text)
    print(f"text_nodes: {text_nodes}")
    # Convert the TextNode objects to HTMLNode objects
    for text_node in text_nodes:
        html_nodes = text_node_to_html_node(text_node)
        children.append(html_nodes)
    return children


# Helper functions to convert blocks of code to various HTML nodes #
## ============================================================== ##
def heading_to_html_node(block: str) -> HTMLNode:
    """
    Takes a single block of markdown text as input and returns an HTMLNode representing the block.
    """
    # Create a new HTMLNode for the heading
    # level = block.count("#")
    pass


def code_to_html_node(block: str) -> HTMLNode:
    """
    Takes a single block of markdown text as input and returns an HTMLNode representing the block.
    """
    pass


def blockquote_to_html_node(block: str) -> HTMLNode:
    """
    # WARNING: WE DO NOT CORRECTLY CAPTURE BLOCK QUOTES WITHOUT A SPACE
    Takes a blockquote of markdown text as input and returns a ParentNode object
    with the tag "blockquote".
    Args:
        block (str): A block of text to be converted to a blockquote HTMLNode.
    Returns:
        ParentNode: A ParentNode object with the tag "blockquote" and the text as its children.
    """
    children = []
    # This can be multiple lines of '> ' text, so we need to split it up
    quote_lines = block.split("\n")
    stripped_lines = [line[2:] for line in quote_lines if line.startswith("> ")]
    # Join the lines back together
    text = " ".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    """
    Takes a single block of markdown text as input and returns an HTMLNode representing the block.
    """
    pass


def ordered_list_to_html_node(block: str) -> HTMLNode:
    """
    Takes a single block of markdown text as input and returns an HTMLNode representing the block.
    """
    pass


def paragraph_to_html_node(block: str) -> HTMLNode:
    """
    Converts a block of text into a paragraph HTMLNode.
    It takes a string of text and returns a ParentNode object with the tag "p".
    The text is split into paragraphs, and each paragraph is converted to a TextNode.
    The TextNode is then converted to a LeafNode, which is added to the ParentNode.
    Args:
        block (str): A block of text to be converted to a paragraph HTMLNode.
    Returns:
        ParentNode: A ParentNode object with the tag "p" and the text as its children.
    """
    # This could be multiple lines of text, so we need to split it into paragraphs
    paragraphs = block.split("\n")
    paragraph = " ".join(paragraphs)
    # get all the children nodes back from text_to_children
    children = text_to_children(paragraph)
    return ParentNode("p", children)
