import sys
from pathlib import Path

# Add project root to sys.path for tests
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from bs4 import BeautifulSoup
from core.cleaner import extract_main_content, extract_clean_text


def test_extract_clean_text():
    html = "<html><body><script>alert('xss');</script><p>Hello</p><style>.hidden { display: none; }</style><span>World</span></body></html>"
    text = extract_clean_text(html)
    assert "Hello" in text
    assert "World" in text
    assert "alert" not in text
    assert ".hidden" not in text


def test_extract_main_content():
    html = """
    <html>
      <head><title>Test</title></head>
      <body>
        <nav class="navbar"><a href="#">Menu</a></nav>
        <div class="sidebar">Ads</div>
        <main>
          <h1>Main Title</h1>
          <p>This is the main content.</p>
        </main>
        <footer>Copyright</footer>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    content = extract_main_content(soup)
    assert "Main Title" in content
    assert "This is the main content." in content


def test_extract_clean_text_empty():
    text = extract_clean_text("")
    assert text == ""


def test_extract_main_content_no_main():
    html = "<html><body><p>Just a paragraph</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    content = extract_main_content(soup)
    assert "Just a paragraph" in content
