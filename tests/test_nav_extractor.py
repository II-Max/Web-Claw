import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.nav_extractor import extract_navigation

def test_extract_navigation_string_class():
    html = """
    <html>
        <body>
            <div class="breadcrumb-container">
                <ol class="breadcrumb">
                    <li><a href="/">Home</a></li>
                    <li><a href="/category">Category</a></li>
                </ol>
            </div>
            <nav class="breadcrumb-nav">
                <a href="/">Home</a>
            </nav>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Simulate string for 'class' attribute
    soup.ol["class"] = "breadcrumb"
    soup.find("div")["class"] = "breadcrumb-container"
    soup.find("nav")["class"] = "breadcrumb-nav"

    result = extract_navigation(soup, "https://example.com")
    assert len(result["breadcrumbs"]) > 0
    assert result["breadcrumbs"][0]["url"] == "https://example.com/"
