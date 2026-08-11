import pytest
from bs4 import BeautifulSoup
from core.extractors.table_extractor import extract_tables

def test_extract_tables_success():
    """Test extracting a valid HTML table."""
    html_content = """
    <html>
      <body>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Age</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Alice</td>
              <td>30</td>
            </tr>
            <tr>
              <td>Bob</td>
              <td>25</td>
            </tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = extract_tables(soup, html_content)

    assert result["count"] == 1
    assert result["total_found"] == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert "Name" in table["column_names"]
    assert "Age" in table["column_names"]

    # Check data
    data = table["data"]
    assert len(data) == 2
    assert data[0]["Name"] == "Alice"
    assert data[0]["Age"] == 30
    assert data[1]["Name"] == "Bob"
    assert data[1]["Age"] == 25

def test_extract_tables_no_tables():
    """Test extracting from HTML with no tables."""
    html_content = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")
    result = extract_tables(soup, html_content)

    assert result["count"] == 0
    assert len(result["tables"]) == 0
