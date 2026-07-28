import pytest
import requests
from unittest.mock import patch, Mock
from core.scraper import fetch_page, MAX_RETRIES

@patch("core.scraper.session.get")
def test_fetch_page_success(mock_get):
    mock_resp = Mock()
    mock_resp.text = "<html><body><p>Test</p></body></html>"
    mock_resp.apparent_encoding = "utf-8"
    mock_get.return_value = mock_resp

    html, soup = fetch_page("http://example.com")

    assert html == "<html><body><p>Test</p></body></html>"
    assert soup is not None
    mock_get.assert_called_once_with(
        "http://example.com",
        timeout=30,
        verify=True,
        allow_redirects=True,
    )

@patch("core.scraper.session.get")
@patch("core.scraper.time.sleep")
def test_fetch_page_retries_and_fails(mock_sleep, mock_get):
    # Make get always raise RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Timeout")

    html, soup = fetch_page("http://example.com")

    assert html is None
    assert soup is None
    assert mock_get.call_count == MAX_RETRIES
