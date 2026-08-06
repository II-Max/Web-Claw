import pytest
from bs4 import BeautifulSoup
from core.extractors.table_extractor import extract_tables

def test_extract_tables_with_bs4_flavor():
    html = """
    <html>
      <body>
        <table>
          <tr><th>Name</th><th>Age</th><th>Location</th></tr>
          <tr><td>Alice</td><td>30</td><td>New York</td></tr>
          <tr><td>Bob</td><td>25</td><td>London</td></tr>
          <tr><td>Charlie</td><td>35</td><td>Paris</td></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 1

    table_data = result["tables"][0]
    assert table_data["rows"] == 3
    assert table_data["columns"] == 3
    assert table_data["column_names"] == ["Name", "Age", "Location"]
    assert table_data["data"][0]["Name"] == "Alice"
    assert table_data["data"][1]["Name"] == "Bob"

def test_extract_tables_invalid():
    # Only 1 row (header) + no data, should be rejected by _is_valid_table
    html = """
    <html>
      <body>
        <table>
          <tr><th>Name</th><th>Age</th></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 0
