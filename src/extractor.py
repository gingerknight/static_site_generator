import os
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


def generate_pages_recursively(from_path, template_path, dest_root_path):

    logger.info(f"Generating from {from_path} to {dest_root_path} using {template_path}")

    if from_path.is_file() and from_path.suffix == ".md":
        # Get relative path and change suffix
        relative_path = from_path.relative_to(Path("content")).with_suffix(".html")
        dest_path = dest_root_path / relative_path

        logger.info(f"Generating file {dest_path} from markdown {from_path}")
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        generate_page(from_path, template_path, dest_path)

    elif from_path.is_dir():
        for item in from_path.iterdir():
            generate_pages_recursively(item, template_path, dest_root_path)


def generate_page(from_file_path, template_path, dest_file_path):
    """
    Generate a single HTML page from a markdown file using a template.
    Args:
        from_file_path (str): The source markdown file to generate the HTML page from.
        template_path (str): The path to the HTML template file.
        dest_file_path (str): The destination path to save the generated HTML file.
    Returns:
        None
    """
    logger.info(f"Generating page from {from_file_path} to {dest_file_path} using {template_path}")
    # Read the template file
    template_path = Path(template_path).resolve()
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()
    
    # Generate the page
    with open(from_file_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    # Convert the markdown to HTML
    html = markdown_to_html_node(markdown).to_html()
    # Extract the title
    title = extract_title(markdown)
    # Replace the placeholders in the template
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    # Write the HTML to the destination file
    with open(dest_file_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Generated page at {dest_file_path}")
            
