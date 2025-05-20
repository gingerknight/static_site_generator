## Static Site Generator Project

### Assignment

Create a static site generator from scratch. Translating Markdown text to HTML for webpage rendering.

### Background

A static site generator takes raw content files (like [Markdown](https://www.markdownguide.org/) and images) and turns them into a static website (a mix of [HTML](https://en.wikipedia.org/wiki/HTML) and [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) files).

### Features

- **Markdown Parsing**:
  - Converts Markdown text into structured blocks (e.g., paragraphs, headings, lists, and code blocks).
  - Supports inline formatting such as bold, italic, code, links, and images.

- **HTML Node Generation**:
  - Converts parsed Markdown into HTML nodes using `HTMLNode`, `LeafNode`, and `ParentNode` classes.
  - Supports attributes like `href` for links and `src`/`alt` for images.

- **Text Node Splitting**:
  - Splits text into `TextNode` objects based on Markdown syntax.
  - Handles nested formatting (e.g., bold and italic within the same text).

- **Image and Link Extraction**:
  - Extracts images and links from Markdown text using regex-based utilities.

- **Testing**:
  - Comprehensive unit tests for all major components:
    - Markdown block splitting (`splitblocks.py`).
    - Text node splitting and formatting (`splitnode.py`).
    - HTML node generation (`htmlnode.py`).
    - Markdown image and link extraction (`extract_markdown.py`).
  - Tests ensure proper handling of edge cases, malformed Markdown, and nested structures.

### Running the Project

To execute the main script:

```sh
main.sh
```

### Running Tests
To run all unit tests:

```sh
test.sh
```

#### Linting and Formatting
- Lint check with Ruff: Run `ruff check src/` to check lint the code.
> Reference: [ruff linter](https://docs.astral.sh/ruff/linter/)
- Formatting with Ruff: Run `ruff format src/` or `ruff check src/ --fix` to run code formatting.
> Reference: [ruff formatter](https://docs.astral.sh/ruff/formatter/)
  - Note: pyproject.toml is a legacy file that defines the rules for linting and formatting inside src/ for black, isort, and some initial ruff configuration
  - The ruff.toml is mostly the default settings except for the linelength is adjusted 120. 

### Continuous Integration
The project uses GitHub Actions to:

- Run tests with pytest.
- Perform linting with Ruff.
- Check code formatting with Black.