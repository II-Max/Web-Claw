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
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Test 1</td>
              <td>100</td>
            </tr>
            <tr>
              <td>2</td>
              <td>Test 2</td>
              <td>200</td>
            </tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 1
    assert len(result["tables"]) == 1

    table_data = result["tables"][0]
    assert table_data["rows"] == 2
    assert table_data["columns"] == 3
    assert table_data["column_names"] == ["ID", "Name", "Value"]
    assert table_data["data"][0]["ID"] == 1
    assert table_data["data"][0]["Name"] == "Test 1"
    assert table_data["data"][0]["Value"] == 100
