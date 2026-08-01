import copy

from bs4 import BeautifulSoup, Tag


from typing import Union

def extract_clean_text(html_or_soup: Union[str, BeautifulSoup]) -> str:
    """Extract all visible text, removing scripts/styles/noscript."""
    if isinstance(html_or_soup, str):
        soup = BeautifulSoup(html_or_soup, "html.parser")
    else:
        soup = html_or_soup

    texts = []
    for text in soup.strings:
        text_strip = text.strip()
        if not text_strip:
            continue
        parent = text.parent
        is_hidden = False
        while parent is not None and parent.name != '[document]':
            if parent.name in ['script', 'style', 'noscript']:
                is_hidden = True
                break
            parent = parent.parent
        if not is_hidden:
            texts.append(text_strip)

    return " ".join(texts)


def get_soup(html: str) -> BeautifulSoup:
    """Parse HTML into a BeautifulSoup object."""

    return BeautifulSoup(html, "html.parser")


def extract_main_content(soup: BeautifulSoup) -> str:
    """
    Extract the main text content, attempting to
    skip navigation, sidebars, footers, and ads.
    Returns cleaned plain text of the main content area.
    """

    # Try to find a <main>, <article>, or role="main" element
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(attrs={"role": "main"})
        or soup.find("div", id=lambda x: x and "content" in x.lower() if x else False)
        or soup.find("div", class_=lambda x: x and "content" in " ".join(x).lower() if x else False)
    )

    target = main if main else soup.body if soup.body else soup

    # Clone to avoid mutating original
    clone = copy.copy(target)

    # Remove unwanted elements
    unwanted_tags = [
        "script", "style", "noscript", "nav",
        "footer", "header", "aside", "iframe",
    ]
    for tag_name in unwanted_tags:
        for tag in clone.find_all(tag_name):
            tag.decompose()

    # Remove elements with common ad/nav class/id patterns
    ad_patterns = [
        "sidebar", "menu", "nav", "footer",
        "header", "advertisement", "ad-", "ads-",
        "banner", "popup", "modal", "cookie",
    ]

    for element in list(clone.find_all(True)):
        if not isinstance(element, Tag):
            continue
        try:
            cls = element.attrs.get("class", []) if element.attrs else []
            eid = element.attrs.get("id", "") if element.attrs else ""
            attrs_text = " ".join([
                " ".join(cls) if isinstance(cls, list) else str(cls),
                str(eid),
            ]).lower()

            if any(p in attrs_text for p in ad_patterns):
                element.decompose()
        except (AttributeError, TypeError):
            continue

    return clone.get_text(separator="\n", strip=True)