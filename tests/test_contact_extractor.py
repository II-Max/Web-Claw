import pytest
from bs4 import BeautifulSoup
from web_miner.core.extractors.contact_extractor import extract_contacts

def test_extract_valid_contacts():
    html_content = """
    <html>
        <body>
            <a href="mailto:contact@myrealcompany.net">Email Us</a>
            <a href="tel:+1234567890">Call Us</a>
            <a href="https://twitter.com/test">Twitter</a>
            <p>You can also reach us at hello@myrealcompany.net or call +098-765-4321.</p>
            <address>123 Main St, Anytown, USA</address>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")

    contacts = extract_contacts(soup, html_content)

    # emails: contact@myrealcompany.net (mailto), hello@myrealcompany.net (regex)
    assert len(contacts["emails"]) == 2
    emails = [e["email"] for e in contacts["emails"]]
    assert "contact@myrealcompany.net" in emails
    assert "hello@myrealcompany.net" in emails

    # phones: +1234567890 (tel), +098-765-4321 (regex)
    assert len(contacts["phones"]) == 2
    phones = [p["normalized"] for p in contacts["phones"]]
    assert "+1234567890" in phones
    assert "+0987654321" in phones

    # social: twitter.com
    assert len(contacts["social_profiles"]) == 1
    assert contacts["social_profiles"][0]["platform"] == "twitter"
    assert contacts["social_profiles"][0]["url"] == "https://twitter.com/test"

    # addresses
    assert len(contacts["addresses"]) == 1
    assert contacts["addresses"][0] == "123 Main St, Anytown, USA"
