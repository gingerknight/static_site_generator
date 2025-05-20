# python imports
import re

# application imports
from textnode import TextNode, TextType

SYMBOL_TO_TEXTTYPE = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
    "[": TextType.LINK,
    "![": TextType.IMAGE,
    # Add more symbols and their corresponding TextType if needed
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


def extract_markdown_images(text):
    """
    takes raw markdown text and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images

    Example:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    :param text: markdown text
    :return __: list of tuples [(alt_text, url)]
    """

    alt_uri_regex = re.compile(r"\!\[(.*?)\]\((htt.*?)\)")
    matches = re.findall(alt_uri_regex, text)
    return matches


def extract_markdown_links(text):
    """
    extracts markdown links instead of images. It should return tuples of anchor text and URLs.
    Example:
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    :param text: markdown text
    :return __: list of tuples
    """

    alt_uri_link_regex = re.compile(r"(?<!\!)\[(.*?)\]\((https?:\/\/[^\s)]+)\)")
    matches = re.findall(alt_uri_link_regex, text)
    return matches


def split_nodes_image(old_nodes):
    """
    Takes a list of TextNode objects and splits them into separate nodes for images.
    It should return a list of TextNode objects, where each image is represented as a separate node.

    Example:
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        # [
        #     TextNode("This is text with an ", TextType.TEXT),
        #     TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        #     TextNode(" and another ", TextType.TEXT),
        #     TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        # ]
    """
    new_nodes = []
    for node in old_nodes:
        # if not text.normal, pass through
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        # Extaract the image links from the text
        matches = extract_markdown_images(node.text)
        # If there are no image links, return list with original TextNode
        if not matches:
            new_nodes.append(node)
            continue
        # If there are image links, split the text into sections
        # and create new TextNode objects for each image
        remaining_text = node.text
        for match in matches:
            image_alt, image_link = match
            parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            # Create a new TextNode for the image
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = parts[1] if len(parts) > 1 else ""
        # If there's any remaining text after the last image, add it as a normal TextNode
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Takes a list of TextNode objects and splits them into separate nodes for links.
    It should return a list of TextNode objects, where each link is represented as a separate node.

    Example:
        node = TextNode(
            "This is text with an [link](https://the_mighty_googles.com) and another [second link](https://the_mighty_youtubes.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        # [
        #     TextNode("This is text with an ", TextType.TEXT),
        #     TextNode("link", TextType.LINK, "https://the_mighty_googles.comg"),
        #     TextNode(" and another ", TextType.TEXT),
        #     TextNode("second image", TextType.LINK, "https://the_mighty_youtubes.com"),
        # ]
    """
    new_nodes = []
    for node in old_nodes:
        # if not text.normal, pass through
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        # Extaract the image links from the text
        matches = extract_markdown_links(node.text)
        # If there are no valid markdown url links, return list with original TextNode
        if not matches:
            new_nodes.append(node)
            continue
        # If there are valid markdown url links, split the text into sections
        # and create new TextNode objects for each link
        remaining_text = node.text
        for match in matches:
            uri_alt, uri_link = match
            print(f"uri_alt: {uri_alt}, uri_link: {uri_link}")
            parts = remaining_text.split(f"[{uri_alt}]({uri_link})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            # Create a new TextNode for the image
            new_nodes.append(TextNode(uri_alt, TextType.LINK, uri_link))
            remaining_text = parts[1] if len(parts) > 1 else ""
        # If there's any remaining text after the last image, add it as a normal TextNode
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Takes a string and returns a list of TextNode objects.
    The function should handle different text types (normal, bold, italic, etc.) based on the delimiters.

    Example:
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        [
            TextNode(This is , text, None)
            TextNode(text, bold, None)
            TextNode( with an , text, None)
            TextNode(italic, italic, None)
            TextNode( word and a , text, None)
            TextNode(code block, code, None)
            TextNode( and an , text, None)
            TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg)
            TextNode( and a , text, None)
            TextNode(link, link, https://boot.dev)
        ]

    """
    nodes = [TextNode(text, TextType.NORMAL)]

    # Order matters: images and links should be split before emphasis
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
