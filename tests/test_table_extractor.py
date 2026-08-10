import pytest
from bs4 import BeautifulSoup
from core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = """
    <html>
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
            <tr><td>Only one row</td><td>1</td></tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert "count" in result
    assert "tables" in result
    assert result["count"] >= 1

    # Check the valid table
    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert "Name" in table["column_names"]
    assert "Age" in table["column_names"]

def test_extract_tables_no_table():
    html = "<html><body><p>No tables here!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert len(result["tables"]) == 0
