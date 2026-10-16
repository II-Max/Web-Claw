import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.link_extractor import extract_links

def test_extract_links_string_rel():
    # 'rel' is normally a list in html.parser, but testing robust handling
    # just in case the parser behaves differently or we pass it artificially
    html = """
    <html>
        <body>
            <a href="https://example.com" rel="nofollow">Link</a>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Simulate a parser returning a string for 'rel'
    soup.a["rel"] = "nofollow"

    result = extract_links(soup, "https://example.com")
    assert result["total_count"] == 1
    assert result["all_links"][0]["rel"] == "nofollow"
