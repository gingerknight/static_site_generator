# imports here
import os
import shutil
from pathlib import Path
import logging

# application imports
from log_config import setup_logging
from splitblocks import markdown_to_html_node


setup_logging()
logger = logging.getLogger(__name__)

def extract_title(markdown: str) -> str:
    """
    Extract the title from the markdown string.
    If there is no title, raise exception
    Args:
        markdown (str): The markdown string to extract the title from.
    Returns:
        str: The extracted title.
    Raises:
        ValueError: If the title is not found in the markdown string.

    Example:
        markdown = "# Main Title"
        extract_titel("# Main Title")
        # returns "Main Title"
    """
    if len(markdown) == 0:
        raise ValueError("Markdown is empty. Expecting a title '# Title'")
    # Split the markdown string into lines
    lines = markdown.splitlines()
    # Get the first line and strip any leading/trailing whitespace
    title = lines[0].strip()
    # Check if the first line starts with a '#' character
    if not title.startswith("#"):
        raise ValueError("Title symbol not found in markdown string.")
    # Remove the '#' character and any leading/trailing whitespace
    title = title[1:].strip()
    # Check if the title is empty
    if not title:
        raise ValueError("Title text not found in markdown string.")
    # Return the extracted title
    return title

def generate_page(from_path, template_path, dest_path):
    """
    Print a message like "Generating page from from_path to dest_path using template_path".
    Read the markdown file at from_path and store the contents in a variable.
    Read the template file at template_path and store the contents in a variable.
    Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    Use the extract_title function to grab the title of the page.
    Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    """
    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    # Convert the markdown to HTML
    html = markdown_to_html_node(markdown).to_html()
    # Extract the title
    title = extract_title(markdown)
    # Replace the placeholders in the template
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write the HTML to the destination file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Generated page at {dest_path}")

