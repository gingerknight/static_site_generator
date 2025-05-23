# Tests for Extractor Logic
# python imports
import unittest


# application imports
from extractor import extract_title


class TestMarkdownExtractor(unittest.TestCase):
    # <------ Test cases for the extract_title function ------>
    def test_title_as_expected(self):
        md = "# Main Title"
        title = extract_title(md)
        self.assertEqual(title, "Main Title")

    def test_title_with_leading_whitespace(self):
        md = "   # Main Title"
        title = extract_title(md)
        self.assertEqual(title, "Main Title")

    def test_title_no_hash(self):
        md = "Main Title"
        with self.assertRaises(ValueError) as context:
            extract_title(md)
            self.assertEqual(str(context.exception), "Title symbol not found in markdown string.")

    def test_title_empty_string(self):
        md = ""
        with self.assertRaises(ValueError) as context:
            extract_title(md)
            self.assertEqual(str(context.exception), "Markdown is empty. Expecting a title '# Title'")

    def test_title_with_hash_and_no_text(self):
        md = "#"
        with self.assertRaises(ValueError) as context:
            extract_title(md)
            self.assertEqual(str(context.exception), "Title text not found in markdown string.")
