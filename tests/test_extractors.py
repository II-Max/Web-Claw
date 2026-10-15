from bs4 import BeautifulSoup
from web_miner.core.cleaner import extract_main_content
from web_miner.core.extractors.link_extractor import extract_links
from web_miner.core.extractors.form_extractor import extract_forms
from web_miner.core.extractors.nav_extractor import extract_navigation

def test_extract_main_content_string_attrs():
    html = """
    <html><body>
    <div id="main content">Main text</div>
    <div class="breadcrumb">breadcrumb</div>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Forcing string attributes to simulate non-standard parser behaviors
    soup.find("div", id="main content")["id"] = "main content"
    soup.find("div", class_="breadcrumb")["class"] = "breadcrumb"

    content = extract_main_content(soup)
    assert "Main text" in content

def test_extract_links_string_rel():
    html = """<a href="http://example.com" rel="nofollow noopener">Link</a>"""
    soup = BeautifulSoup(html, "html.parser")
    soup.a["rel"] = "nofollow noopener" # Force string
    links = extract_links(soup, "http://example.com")
    assert links["all_links"][0]["rel"] == "nofollow noopener"

def test_extract_forms_string_class():
    html = """<form class="my-form test-form"></form>"""
    soup = BeautifulSoup(html, "html.parser")
    soup.form["class"] = "my-form test-form" # Force string
    forms = extract_forms(soup, "http://example.com")
    assert forms["forms"][0]["class"] == "my-form test-form"

def test_extract_navigation_string_class():
    html = """
    <nav class="main-nav">
      <a href="http://example.com">Link</a>
    </nav>
    <div class="breadcrumb">
      <a href="http://example.com/home">Home</a>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    soup.nav["class"] = "main-nav" # Force string
    soup.find("div", class_="breadcrumb")["class"] = "breadcrumb" # Force string
    navs = extract_navigation(soup, "http://example.com")
    assert navs["nav_menus"][0]["label"] == "main-nav"
    assert navs["breadcrumbs"][0]["text"] == "Home"
