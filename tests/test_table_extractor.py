import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_valid():
    """Test that extract_tables successfully parses a valid HTML table."""
    html_content = """
    <html>
        <body>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Age</th>
                        <th>City</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Alice</td>
                        <td>30</td>
                        <td>New York</td>
                    </tr>
                    <tr>
                        <td>Bob</td>
                        <td>25</td>
                        <td>Los Angeles</td>
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
    assert len(result["tables"]) == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 3
    assert table["column_names"] == ["Name", "Age", "City"]
    assert table["data"][0]["Name"] == "Alice"
    assert table["data"][0]["Age"] == 30
    assert table["data"][0]["City"] == "New York"
    assert table["data"][1]["Name"] == "Bob"
    assert table["data"][1]["Age"] == 25
    assert table["data"][1]["City"] == "Los Angeles"

def test_extract_tables_no_tables():
    """Test that extract_tables handles HTML with no tables correctly."""
    html_content = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")
    result = extract_tables(soup, html_content)

    assert result["count"] == 0
    assert result["tables"] == []
