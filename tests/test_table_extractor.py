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
              <td>Test A</td>
              <td>100</td>
            </tr>
            <tr>
              <td>2</td>
              <td>Test B</td>
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
    assert result["total_found"] == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 3
    assert table["column_names"] == ["ID", "Name", "Value"]

    data = table["data"]
    assert len(data) == 2
    assert data[0]["ID"] == 1
    assert data[0]["Name"] == "Test A"
    assert data[0]["Value"] == 100
    assert data[1]["ID"] == 2
    assert data[1]["Name"] == "Test B"
    assert data[1]["Value"] == 200
