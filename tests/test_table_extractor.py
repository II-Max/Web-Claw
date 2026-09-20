import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = """
    <html>
      <head><title>Test Table</title></head>
      <body>
        <table>
          <thead>
            <tr><th>Name</th><th>Age</th></tr>
          </thead>
          <tbody>
            <tr><td>Alice</td><td>30</td></tr>
            <tr><td>Bob</td><td>25</td></tr>
          </tbody>
        </table>

        <!-- Invalid table, should not be extracted due to size < MIN_ROWS/MIN_COLS -->
        <table>
          <tr><td>Single Item</td></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 2 # Found 2, but 1 is invalid

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Name", "Age"]
    assert table["data"][0]["Name"] == "Alice"
    assert table["data"][0]["Age"] == 30
    assert table["data"][1]["Name"] == "Bob"
    assert table["data"][1]["Age"] == 25
