import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = """
    <html>
      <body>
        <table>
          <thead>
            <tr><th>Header1</th><th>Header2</th></tr>
          </thead>
          <tbody>
            <tr><td>Data1</td><td>Data2</td></tr>
            <tr><td>Data3</td><td>Data4</td></tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert result["total_found"] == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Header1", "Header2"]

    # Assert data using the correct dictionary keys based on columns
    assert table["data"][0]["Header1"] == "Data1"
    assert table["data"][0]["Header2"] == "Data2"
