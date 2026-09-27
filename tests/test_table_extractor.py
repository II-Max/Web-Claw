import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables


def test_extract_tables_with_bs4_flavor():
    """
    Test that extract_tables can successfully parse an HTML table
    using the 'bs4' flavor without errors.
    """
    html_content = """
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
    soup = BeautifulSoup(html_content, "html.parser")

    # Should not raise any ValueError about no tables found or parsing errors
    result = extract_tables(soup, html_content)

    assert result["count"] == 1
    assert result["total_found"] == 1
    assert len(result["tables"]) == 1

    table_data = result["tables"][0]
    assert table_data["rows"] == 2 # Data rows only
    assert table_data["columns"] == 2
    assert "Name" in table_data["column_names"]
    assert "Age" in table_data["column_names"]
