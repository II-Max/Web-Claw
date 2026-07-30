import pytest
from bs4 import BeautifulSoup
from web_miner.core.cleaner import extract_main_content, extract_clean_text

def test_extract_clean_text():
    html = "<html><body><script>alert('xss');</script><p>Hello</p><style>.hidden { display: none; }</style><span>World</span></body></html>"
    text = extract_clean_text(html)
    assert "Hello World" in text
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
    assert "Menu" not in content
    assert "Ads" not in content
    assert "Copyright" not in content
