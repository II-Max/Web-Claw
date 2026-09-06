import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = """
    <html>
        <body>
            <table>
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>Alice</td><td>30</td></tr>
                <tr><td>Bob</td><td>25</td></tr>
            </table>
            <table>
                <tr><th>Item</th></tr>
                <tr><td>A</td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1 # Only one valid table due to size limits
    assert result["total_found"] == 2
    assert result["tables"][0]["rows"] == 2
    assert result["tables"][0]["columns"] == 2
    assert result["tables"][0]["column_names"] == ["Name", "Age"]
