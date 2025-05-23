#! /usr/bin/python3
from textnode import TextNode, TextType
import os
import shutil
from pathlib import Path
import logging
import time

# application imports
from log_config import setup_logging
from extractor import generate_pages_recursively


setup_logging()
logger = logging.getLogger(__name__)


def copy_recursively(static_dir: str, public_dir: str) -> None:
    """
    Write a recursive function that copies all the contents from a source directory to a destination directory
    and creates the destination directory if it does not exist.

    Args:
        static_dir (str): The source directory to copy from.
        public_dir (str): The destination directory to copy to.
    Returns:
        None
    """
    src_path = Path(static_dir).resolve()
    logger.info(f"Source Path: {src_path}")
    dest_path = Path(public_dir).resolve()
    logger.info(f"Destination Path: {dest_path}")

    if src_path.is_file():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src_path, dest_path)
        logger.info(f"Copied file {src_path} to {dest_path}")

    elif src_path.is_dir():
        # Recursively copy each item in the source directory
        for item in src_path.iterdir():
            copy_recursively(item, dest_path / item.name)


def clean_up_public_dir(public_dir: str) -> None:
    """
    Write a function that cleans up the public directory by removing all files and directories in it.
    Args:
        public_dir (str): The directory to clean up.
    Returns:
        None
    """
    # Check if the destination path exists
    dest_path = Path(public_dir).resolve()
    logger.info(f"Cleaning up all files in: {dest_path}")
    # Remove all files and directories in the destination path
    if dest_path.exists():
        for item in dest_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
                logger.info(f"Removed directory {item}")
            else:
                item.unlink()
                logger.info(f"Removed file {item}")


def main():
    my_node = TextNode("Sample Text", TextType.LINK, "https://www.google.com")  # noqa: F841
    # Clean up the public directory
    public_dir = Path("public").resolve()
    if len(os.listdir(public_dir)) > 0:
        clean_up_public_dir(public_dir)
    # Copy the static directory to the public directory
    static_dir = Path("static").resolve()
    copy_recursively(static_dir, public_dir)
    
    content_dir = Path("content")
    template_path = Path("template.html")
    output_dir = Path("public")

    # Generate pages from markdown files
    generate_pages_recursively(content_dir, template_path, output_dir)


main()
