import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

HTML_WITH_TABLES = """
<html>
<body>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Age</th>
        </tr>
        <tr>
            <td>John Doe</td>
            <td>30</td>
        </tr>
        <tr>
            <td>Jane Smith</td>
            <td>25</td>
        </tr>
    </table>

    <!-- Invalid table (less than 2 rows) -->
    <table>
        <tr><th>Invalid</th></tr>
    </table>
</body>
</html>
"""

def test_extract_tables():
    soup = BeautifulSoup(HTML_WITH_TABLES, "html.parser")
    result = extract_tables(soup, HTML_WITH_TABLES)

    assert result["total_found"] == 2
    assert result["count"] == 1

    tables = result["tables"]
    assert len(tables) == 1

    table = tables[0]
    assert table["rows"] == 2 # 2 data rows
    assert table["columns"] == 2
    assert "Name" in table["column_names"]
    assert "Age" in table["column_names"]

    assert table["data"][0]["Name"] == "John Doe"
    assert table["data"][0]["Age"] == 30

HTML_WITHOUT_TABLES = """
<html>
<body>
    <p>No tables here.</p>
</body>
</html>
"""

def test_extract_no_tables():
    soup = BeautifulSoup(HTML_WITHOUT_TABLES, "html.parser")
    result = extract_tables(soup, HTML_WITHOUT_TABLES)

    assert result["count"] == 0
    assert result["tables"] == []
