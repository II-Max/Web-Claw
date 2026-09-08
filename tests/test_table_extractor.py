import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables, _is_valid_table, _score_table
import pandas as pd

def test_extract_tables_success():
    html = """
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
                    <td>25</td>
                </tr>
                <tr>
                    <td>Bob</td>
                    <td>30</td>
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
    assert len(result["tables"]) == 1
    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 2
    assert table["column_names"] == ["Name", "Age"]
    assert table["data"] == [{"Name": "Alice", "Age": 25}, {"Name": "Bob", "Age": 30}]

def test_extract_tables_no_tables():
    html = """
    <html>
    <body>
        <p>There are no tables here.</p>
    </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)

    assert result["count"] == 0
    assert "tables" in result
    assert len(result["tables"]) == 0

def test_is_valid_table():
    # Valid table
    df_valid = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    assert _is_valid_table(df_valid) == True

    # Too small
    df_small = pd.DataFrame({'A': [1]})
    assert _is_valid_table(df_small) == False

    # Mostly empty
    df_empty = pd.DataFrame({'A': [None, None, None, None, None], 'B': [None, None, None, None, 4]})
    assert _is_valid_table(df_empty) == False

    # Bad headers
    df_bad_headers = pd.DataFrame({'unnamed: 0': [1, 2], 'unnamed: 1': [3, 4]})
    assert _is_valid_table(df_bad_headers) == False

def test_score_table():
    df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
    # score = 2 * 2 = 4
    # missing = 0
    # named_cols = 2 * 5 = 10
    # total = 14
    assert _score_table(df) == 14
