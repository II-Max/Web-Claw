from bs4 import BeautifulSoup
from web_miner.core.extractors.table_extractor import extract_tables

def test_extract_tables_valid_html():
    html_content = '''
    <html>
        <body>
            <table border="1">
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>Alice</td><td>30</td></tr>
                <tr><td>Bob</td><td>25</td></tr>
            </table>
        </body>
    </html>
    '''
    soup = BeautifulSoup(html_content, 'html.parser')

    result = extract_tables(soup, html_content)

    assert result['count'] == 1
    assert result['total_found'] == 1

    table_data = result['tables'][0]
    assert table_data['rows'] == 2
    assert table_data['columns'] == 2

    # Check data matches
    assert table_data['data'][0]['Name'] == 'Alice'
    assert table_data['data'][0]['Age'] == 30
    assert table_data['data'][1]['Name'] == 'Bob'
    assert table_data['data'][1]['Age'] == 25
