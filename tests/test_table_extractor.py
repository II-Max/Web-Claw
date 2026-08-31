import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_with_bs4_flavor():
    """
    Verify that table extraction works correctly with the bs4 flavor
    and that tables are extracted as expected.
    """
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

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 3
    assert table["column_names"] == ["Name", "Age", "City"]

    data = table["data"]
    assert len(data) == 2
    assert data[0]["Name"] == "Alice"
    assert data[0]["Age"] == 30
    assert data[0]["City"] == "New York"

    assert data[1]["Name"] == "Bob"
    assert data[1]["Age"] == 25
    assert data[1]["City"] == "Los Angeles"
