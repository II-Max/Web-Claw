import pytest
import pandas as pd
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_with_bs4_flavor():
    html = """
    <html>
        <body>
            <table>
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>Alice</td><td>30</td></tr>
                <tr><td>Bob</td><td>25</td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 1

    table_data = result["tables"][0]
    assert table_data["rows"] == 2
    assert table_data["columns"] == 2
    assert table_data["column_names"] == ["Name", "Age"]

    # Check that data is properly extracted
    assert table_data["data"][0]["Name"] == "Alice"
    assert table_data["data"][0]["Age"] == 30

def test_extract_tables_invalid():
    html = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result["total_found"] == 0
    assert len(result["tables"]) == 0
