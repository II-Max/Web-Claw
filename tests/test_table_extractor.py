from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_with_bs4_flavor():
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
    result = extract_tables(soup, html_content)
    assert result["count"] == 1
    assert result["tables"][0]["rows"] == 2
    assert result["tables"][0]["columns"] == 2
