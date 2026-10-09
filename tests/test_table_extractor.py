import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables, _is_valid_table, _score_table
import pandas as pd

def test_extract_tables_valid():
    html = """
    <html>
      <body>
        <table>
          <thead>
            <tr><th>Name</th><th>Age</th><th>City</th></tr>
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
    assert result.get("total_found", 0) == 1
    table = result["tables"][0]
    assert table["rows"] == 2
    assert table["columns"] == 3
    assert "Name" in table["column_names"]
    assert table["data"][0]["Name"] == "Alice"

def test_extract_tables_no_tables():
    html = "<html><body><p>No tables here.</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    result = extract_tables(soup, html)
    assert result["count"] == 0
    assert result.get("total_found", 0) == 0
    assert result["tables"] == []

def test_is_valid_table():
    df_valid = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    assert _is_valid_table(df_valid) == True

    df_too_small = pd.DataFrame({'A': [1]})
    assert _is_valid_table(df_too_small) == False

    df_mostly_empty = pd.DataFrame({'A': [None, None, 1], 'B': [None, None, None]})
    assert _is_valid_table(df_mostly_empty) == False

def test_score_table():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    score1 = _score_table(df1)

    df2 = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 4, 5], 'C': [1, 2, 3]})
    score2 = _score_table(df2)

    assert score2 > score1
