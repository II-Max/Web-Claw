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
        <table>
          <tbody>
            <tr><td>Empty</td></tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 2 # it found 2 raw tables, but only 1 valid

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Name", "Age"]
    assert table["data"][0]["Name"] == "Alice"
    assert str(table["data"][0]["Age"]) == "30"

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert len(result.get("tables", [])) == 0
