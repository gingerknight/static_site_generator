# python imports

# application imports
from textnode import TextNode, TextType


SYMBOL_TO_TEXTTYPE = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def _split_node(node, delimiter, text_type):
    nodes_list = []
    # dealing with italics, bold, etc
    if delimiter not in SYMBOL_TO_TEXTTYPE:
        raise Exception(f"Not a valid markdown for text formating: {delimiter}")

    split_node = node.text.split(delimiter)
    # In [8]: node3 = TextNode("Bad Markdown _formatting here", TextType.NORMAL)
    # In [9]: node3.text.split("_")
    # Out[9]: ['Bad Markdown ', 'formatting here']
    if len(split_node) % 2 == 0:
        raise Exception(f"Invalid Markdown syntax, missing closing {delimiter}")
    for i, text_part in enumerate(split_node):
        # Split logic: Even if it starts with formatting, split leads with empty
        # node2 = TextNode("**Starting with bold** then normal", TextType.NORMAL)
        # In [6]: node2.text.split("**")
        # Out[6]: ['', 'Starting with bold', ' then normal']
        if text_part == "":
            continue
        if i % 2 == 0:
            nodes_list.append(TextNode(text_part, TextType.NORMAL))
        else:
            nodes_list.append(TextNode(text_part, SYMBOL_TO_TEXTTYPE.get(delimiter, text_type)))
    return nodes_list


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    """Use:
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    new_nodes = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ]
    """
    new_nodes = []
    for node in old_nodes:
        # If already not a text node, just add it (link, img)
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            new_nodes.extend(_split_node(node, delimiter, text_type))

    return new_nodes
