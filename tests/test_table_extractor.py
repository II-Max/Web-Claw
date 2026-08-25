import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_valid():
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
    assert "Name" in table["column_names"]
    assert "Age" in table["column_names"]
    assert table["data"][0]["Name"] == "Alice"
    assert table["data"][0]["Age"] == 30
    assert table["data"][1]["Name"] == "Bob"
    assert table["data"][1]["Age"] == 25

def test_extract_tables_no_tables():
    html = """
    <html>
        <body>
            <p>No tables here.</p>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result["tables"] == []

def test_extract_tables_invalid_size():
    html = """
    <html>
        <body>
            <table>
                <tr><td>Only one cell</td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert result["total_found"] == 1
    assert result["tables"] == []
