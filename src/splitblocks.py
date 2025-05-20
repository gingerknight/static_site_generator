# python imports
import re
from enum import Enum

# application imports


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
    # regex for quote block
    quote_regex = re.compile(r"^>\s+")
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
