import pytest
from bs4 import BeautifulSoup
from core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html = """
    <html>
        <body>
            <table>
                <tr><th>Header1</th><th>Header2</th></tr>
                <tr><td>Row1Col1</td><td>Row1Col2</td></tr>
                <tr><td>Row2Col1</td><td>Row2Col2</td></tr>
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
    assert table_data["data"][0]["Header1"] == "Row1Col1"
    assert table_data["data"][1]["Header2"] == "Row2Col2"

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert len(result["tables"]) == 0
