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
    assert result["tables"][0]["rows"] == 2
    assert result["tables"][0]["columns"] == 2
    assert "Name" in result["tables"][0]["column_names"]

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 0
    assert result["tables"] == []
