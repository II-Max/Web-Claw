import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_valid():
    html = """
    <html>
      <body>
        <table>
          <tr><th>Header1</th><th>Header2</th></tr>
          <tr><td>Data1</td><td>Data2</td></tr>
          <tr><td>Data3</td><td>Data4</td></tr>
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
    assert table_data["column_names"] == ["Header1", "Header2"]
    assert table_data["data"][0]["Header1"] == "Data1"
    assert table_data["data"][0]["Header2"] == "Data2"
    assert table_data["data"][1]["Header1"] == "Data3"
    assert table_data["data"][1]["Header2"] == "Data4"


def test_extract_tables_invalid_no_table():
    html = "<html><body><p>No table here</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result.get("total_found", 0) == 0
    assert result["tables"] == []

def test_extract_tables_invalid_small_table():
    # Table with only 1 row (fails MIN_ROWS)
    html = """
    <html>
      <body>
        <table>
          <tr><th>Header1</th><th>Header2</th></tr>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result["total_found"] == 1
    assert result["tables"] == []
