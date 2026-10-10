import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables, _is_valid_table, _score_table
import pandas as pd

def test_extract_tables_valid():
    html = """
    <html>
        <body>
            <table>
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>Alice</td><td>30</td></tr>
                <tr><td>Bob</td><td>25</td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 1
    assert result["total_found"] == 1
    assert len(result["tables"]) == 1
    table_data = result["tables"][0]
    assert table_data["rows"] == 2
    assert table_data["columns"] == 2
    assert table_data["column_names"] == ["Name", "Age"]
    assert table_data["data"][0]["Name"] == "Alice"
    assert table_data["data"][0]["Age"] == 30

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 0
    assert result["tables"] == []

def test_is_valid_table_too_small():
    df = pd.DataFrame({"A": [1]}) # 1 row, 1 col
    assert not _is_valid_table(df)

def test_is_valid_table_mostly_empty():
    df = pd.DataFrame({"A": [None, None, None, 1], "B": [None, None, None, 2]}) # 4 rows, 2 cols, 75% empty
    # threshold is 0.8 so this is valid
    assert _is_valid_table(df)

    df = pd.DataFrame({"A": [None, None, None, None, 1], "B": [None, None, None, None, 2]}) # 5 rows, 2 cols, 80% empty. mean=0.8
    assert _is_valid_table(df)

    df = pd.DataFrame({"A": [None, None, None, None, None, 1], "B": [None, None, None, None, None, 2]}) # 6 rows, 2 cols, 83% empty.
    assert not _is_valid_table(df)

def test_score_table():
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
    # rows=2, cols=2 -> score = 4
    # missing_ratio = 0 -> score = 4
    # named_cols = 2 -> score = 4 + 10 = 14
    score = _score_table(df)
    assert score == 14
