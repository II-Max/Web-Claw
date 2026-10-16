import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.form_extractor import extract_forms

def test_extract_forms_string_class():
    html = """
    <html>
        <body>
            <form action="/submit" class="search-form">
                <input type="text" name="q" />
            </form>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Simulate string for 'class' attribute
    soup.form["class"] = "search-form"

    result = extract_forms(soup, "https://example.com")
    assert result["count"] == 1
    assert result["forms"][0]["class"] == "search-form"
