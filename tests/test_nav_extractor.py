from bs4 import BeautifulSoup
from web_miner.core.extractors.nav_extractor import _get_nav_menus, _get_breadcrumbs

def test_get_nav_menus_empty_class():
    html = '<nav class=""><a href="/x">X</a></nav>'
    soup = BeautifulSoup(html, "html.parser")
    menus = _get_nav_menus(soup, "http://ex.com")
    assert len(menus) == 1
    assert menus[0]["label"] == ""

def test_get_breadcrumbs_lambda():
    html = '<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/x">X</a></li></ol></nav>'
    soup = BeautifulSoup(html, "html.parser")
    bc = _get_breadcrumbs(soup, "http://ex.com")
    assert len(bc) > 0
    assert bc[0]["url"] == "http://ex.com/x"
