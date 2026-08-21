import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_with_bs4_flavor():
    # Simple table to test extraction works correctly
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
