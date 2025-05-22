# python imports
import re
from enum import Enum

# application imports
from textnode import TextNode, TextType, text_node_to_html_node
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
    block = block.strip()  # remove leading and trailing whitespace
    # regex for heading block
    heading_regex = re.compile(r"^#{1,6}\s+?")
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
    The function should:
    - Split the markdown into blocks using the markdown_to_blocks function.
    - Create a list of HTMLNode objects for each block.
        - For each block, determine the type of block using the block_to_block_type function.
        - Based on the type of block, create a new HTMLNode with the proper data.
        - Assign the proper child HTMLNode objects to the block node.
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
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return blockquote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
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
    # Convert the TextNode objects to HTMLNode objects
    for text_node in text_nodes:
        html_nodes = text_node_to_html_node(text_node)
        children.append(html_nodes)
    return children


# Helper functions to convert blocks of code to various HTML nodes #
## ============================================================== ##
def heading_to_html_node(block: str) -> HTMLNode:
    """
    Takes a block string of markdown text as input. Determines the level of the heading
    (h1, h2, h3, etc) based on the number of '#' characters at the start of the string.
    Returns a ParentNode object with the tag "h1", "h2", etc. and the text as its children.
    Args:
        block (str): A block of text to be converted to a heading HTMLNode.
    Returns:
        ParentNode: A ParentNode object with the tag "h1", "h2", etc. and the text as its children.
    Raises:
        We dont raise value error because we regex look for # to determine block type
        TODO: Raise error if count > 6
    Note: We treat multiple lines of headings as a single heading within the same block.
    """
    heading_lines = block.split("\n")
    # Get the level of the heading based on the number of '#' characters
    for line in block.splitlines():
        if line.startswith("#"):
            i = 0
            while i < len(line) and line[i] == "#":
                i += 1
            level = i
            break
    # Remove leading '#' from each line
    heading_lines = [line.lstrip("#").strip() for line in heading_lines if line.startswith("#")]
    # Join the lines back together
    text = " ".join(heading_lines)
    # get all the children nodes back from text_to_children
    children = text_to_children(text)
    # Create a new ParentNode for the heading
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> HTMLNode:
    """
    Takes a block of code as input and returns a ParentNode object
    with the tag "pre" and the code as its children.
    Args:
        block (str): A block of code to be converted to a code HTMLNode.
    Returns:
        ParentNode: A ParentNode object with the tag "pre" and the code as its children.
    Raises:
        ValueError: If the block is not a valid code block (does not start and end with "```").
    Note: We assume that the code block is a single line of code.
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.NORMAL)
    child = text_node_to_html_node(text_node)
    # Create a new ParentNode for the code block
    code = ParentNode("code", [child])
    # Wrap the code in a <pre> tag
    return ParentNode("pre", [code])


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
    Converts markdown unordered lists to HTMLNodes.
    Unordered list blocks should be surrounded by a <ul> tag,
    and each list item should be surrounded by a <li> tag.
    """
    ul_html_nodes = []
    # This can be multiple lines of '- ' text, so we need to split it up
    list_items = block.split("\n")
    # Remove leading '- ' from each line
    list_items = [item[2:] for item in list_items if item.startswith("- ")]
    for item in list_items:
        # Create a new HTMLNode for each list item
        children = text_to_children(item)
        ul_html_nodes.append(ParentNode("li", children))

    return ParentNode("ul", ul_html_nodes)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    """
    Converts markdown ordered (numbered) lists to HTMLNodes.
    Ordered list blocks should be surrounded by a <ol> tag,
    and each list item should be surrounded by a <li> tag.
    """
    ol_html_nodes = []
    # This can be multiple lines of '1. ' text, so we need to split it up
    list_items = block.split("\n")
    # Remove leading '1. ' from each line
    list_items = [item[3:] for item in list_items if re.match(r"^\d+\.\s+", item)]
    for item in list_items:
        # Create a new HTMLNode for each list item
        children = text_to_children(item)
        ol_html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", ol_html_nodes)


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
