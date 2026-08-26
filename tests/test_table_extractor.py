import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

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
            <tr><td>Invalid</td></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 2

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Name", "Age"]
    assert table["data"] == [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]
