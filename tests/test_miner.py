import pytest
from miner import WebMiner

def test_make_site_name_safe():
    # Regular valid URL
    name = WebMiner._make_site_name("http://example.com/some/path")
    assert name == "example_com_some_path"

    # Path traversal attempt
    name2 = WebMiner._make_site_name("http://example.com/../../../etc/passwd")
    assert ".." not in name2
    assert "/" not in name2
    assert name2 == "example_com__________etc_passwd"

    # Windows style traversal attempt
    name3 = WebMiner._make_site_name(r"http://example.com/..\..\..\\")
    assert ".." not in name3
    assert "\\" not in name3
