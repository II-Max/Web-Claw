import pytest
from bs4 import BeautifulSoup
from core.extractors.table_extractor import extract_tables

def test_extract_tables_valid():
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
    assert len(result["tables"]) == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Name", "Age"]
    assert table["data"][0]["Name"] == "Alice"
    assert table["data"][0]["Age"] == 30
    assert table["data"][1]["Name"] == "Bob"
    assert table["data"][1]["Age"] == 25

def test_extract_tables_invalid():
    # Table without headers, not enough rows/cols or empty should be skipped
    html = """
    <html>
      <body>
        <table>
          <tr><td>1</td></tr>
        </table>
        <table>
          <tr><th>Unnamed: 0</th><th>Unnamed: 1</th></tr>
          <tr><td>1</td><td>2</td></tr>
          <tr><td>3</td><td>4</td></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result["tables"] == []
