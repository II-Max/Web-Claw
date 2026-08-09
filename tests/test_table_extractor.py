import pytest
from bs4 import BeautifulSoup
import pandas as pd
from core.extractors.table_extractor import extract_tables, _is_valid_table, _score_table

def test_extract_tables_valid():
    html = """
    <html>
      <body>
        <table>
          <thead>
            <tr><th>Name</th><th>Age</th><th>Location</th></tr>
          </thead>
          <tbody>
            <tr><td>Alice</td><td>30</td><td>New York</td></tr>
            <tr><td>Bob</td><td>25</td><td>London</td></tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 1
    assert result["total_found"] == 1
    assert result["tables"][0]["rows"] == 2
    assert result["tables"][0]["columns"] == 3
    assert result["tables"][0]["column_names"] == ["Name", "Age", "Location"]

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 0
    assert result["total_found"] == 0
    assert result["tables"] == []

def test_is_valid_table():
    # Valid table
    df_valid = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    assert _is_valid_table(df_valid) == True

    # Too small (1 row)
    df_small = pd.DataFrame({'A': [1], 'B': [2]})
    assert _is_valid_table(df_small) == False

    # Too small (1 col)
    df_small2 = pd.DataFrame({'A': [1, 2]})
    assert _is_valid_table(df_small2) == False

    # Mostly empty
    df_empty = pd.DataFrame({'A': [1, None, None, None], 'B': [None, None, None, None]})
    assert _is_valid_table(df_empty) == False

    # Bad headers (all unnamed)
    df_bad_headers = pd.DataFrame({'Unnamed: 0': [1, 2], 'Unnamed: 1': [3, 4]})
    assert _is_valid_table(df_bad_headers) == False

def test_score_table():
    df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [30, 25]})
    score = _score_table(df)
    # rows * cols = 2 * 2 = 4
    # no missing = 0
    # named cols = 2 * 5 = 10
    # 4 - 0 + 10 = 14
    assert score == 14
