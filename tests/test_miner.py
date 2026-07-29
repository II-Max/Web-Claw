import pytest
from miner import WebMiner

def test_webminer_make_site_name():
    # Test typical URL
    name1 = WebMiner._make_site_name("https://www.example.com/path/to/page")
    assert name1 == "example_com_path_to_page"

    # Test URL with port and query params (though query params might not be handled perfectly by original, we test current logic)
    name2 = WebMiner._make_site_name("http://localhost:8080/api/v1")
    assert name2 == "localhost_8080_api_v1"

    # Test empty path
    name3 = WebMiner._make_site_name("https://test.com")
    assert name3 == "test_com"
