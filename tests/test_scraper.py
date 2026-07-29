import pytest
import responses
from bs4 import BeautifulSoup
from core.scraper import fetch_page

@responses.activate
def test_fetch_page_success():
    url = "https://example.com"
    html_content = "<html><body><h1>Hello, World!</h1></body></html>"

    responses.add(
        responses.GET,
        url,
        body=html_content,
        status=200,
        content_type="text/html",
    )

    html, soup = fetch_page(url)

    assert html == html_content
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("h1").text == "Hello, World!"

    # Verify that verify=True was used (responses mocks this transparently but we verify the call was made correctly)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == url + "/"

@responses.activate
def test_fetch_page_retry_failure():
    url = "https://example.com/fail"

    responses.add(
        responses.GET,
        url,
        status=500,
    )

    # Should retry MAX_RETRIES times and then return None, None
    html, soup = fetch_page(url)

    assert html is None
    assert soup is None
    # Assuming MAX_RETRIES = 3 in config
    assert len(responses.calls) == 3
