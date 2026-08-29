import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables():
    html_content = """
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
    soup = BeautifulSoup(html_content, "html.parser")
    result = extract_tables(soup, html_content)

    assert result["count"] == 1
    assert result["total_found"] == 1

    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert "Header1" in table["column_names"]
    assert "Header2" in table["column_names"]
    assert table["data"][0]["Header1"] == "Data1"
    assert table["data"][0]["Header2"] == "Data2"
    assert table["data"][1]["Header1"] == "Data3"
    assert table["data"][1]["Header2"] == "Data4"

def test_extract_tables_no_tables():
    html_content = """
    <html>
        <body>
            <p>No tables here.</p>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = extract_tables(soup, html_content)

    assert result["count"] == 0
    assert result.get("total_found", 0) == 0
    assert result["tables"] == []
