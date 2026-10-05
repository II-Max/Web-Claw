import pytest
import pandas as pd
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = "<html><body><table><tr><th>Header 1</th><th>Header 2</th></tr><tr><td>Data 1</td><td>Data 2</td></tr><tr><td>Data 3</td><td>Data 4</td></tr></table></body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    result = extract_tables(soup, html)
    assert result['count'] == 1
    assert result['tables'][0]['rows'] == 2
    assert result['tables'][0]['columns'] == 2
