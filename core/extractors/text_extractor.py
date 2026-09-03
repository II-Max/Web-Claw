"""
Text Extractor — Extract headings, paragraphs, lists,
code blocks, blockquotes from page content.
"""

from typing import Any, Dict, List
from bs4 import BeautifulSoup, Tag

from core.cleaner import extract_main_content
from core.logger import logger


def extract_text_content(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract all text-based content from the page."""

    logger.info("Extracting text content...")

    data = {
        "headings": _get_headings(soup),
        "paragraphs": _get_paragraphs(soup),
        "lists": _get_lists(soup),
        "code_blocks": _get_code_blocks(soup),
        "blockquotes": _get_blockquotes(soup),
        "main_content": extract_main_content(soup),
    }

    h_count = sum(len(v) for v in data["headings"].values())
    logger.info(
        f"Text extracted: {h_count} headings, "
        f"{len(data['paragraphs'])} paragraphs, "
        f"{len(data['lists'])} lists, "
        f"{len(data['code_blocks'])} code blocks"
    )

    return data


def _get_headings(soup: BeautifulSoup) -> Dict[str, List[str]]:
    """Extract all headings H1-H6 organized by level."""

    headings = {}
    for level in range(1, 7):
        tag_name = f"h{level}"
        found = soup.find_all(tag_name)
        texts = [h.get_text(strip=True) for h in found if h.get_text(strip=True)]
        if texts:
            headings[tag_name] = texts

    return headings


def _get_paragraphs(soup: BeautifulSoup) -> List[str]:
    """Extract meaningful paragraph text."""

    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        # Skip very short or empty paragraphs
        if text and len(text) > 10:
            paragraphs.append(text)

    return paragraphs


def _get_lists(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract ordered, unordered, and definition lists."""

    lists = []

    # Unordered lists
    for ul in soup.find_all("ul"):
        items = []
        for li in ul.find_all("li", recursive=False):
            text = li.get_text(strip=True)
            if text:
                items.append(text)
        if items:
            lists.append({"type": "unordered", "items": items})

    # Ordered lists
    for ol in soup.find_all("ol"):
        items = []
        for li in ol.find_all("li", recursive=False):
            text = li.get_text(strip=True)
            if text:
                items.append(text)
        if items:
            lists.append({"type": "ordered", "items": items})

    # Definition lists
    for dl in soup.find_all("dl"):
        items = []
        current_term = None
        for child in dl.children:
            if not isinstance(child, Tag):
                continue
            if child.name == "dt":
                current_term = child.get_text(strip=True)
            elif child.name == "dd" and current_term:
                items.append({
                    "term": current_term,
                    "definition": child.get_text(strip=True),
                })
                current_term = None
        if items:
            lists.append({"type": "definition", "items": items})

    return lists


def _get_code_blocks(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """Extract code blocks from <pre> and standalone <code> tags."""

    blocks = []

    # <pre> blocks (may contain <code>)
    for pre in soup.find_all("pre"):
        code_tag = pre.find("code")
        code_text = code_tag.get_text() if code_tag else pre.get_text()

        # Try to detect language from class
        lang = ""
        target = code_tag if code_tag else pre
        classes = target.get("class", [])
        for cls in classes:
            if cls.startswith("language-") or cls.startswith("lang-"):
                lang = cls.split("-", 1)[1]
                break
            elif cls.startswith("highlight-"):
                lang = cls.split("-", 1)[1]
                break

        if code_text.strip():
            blocks.append({
                "language": lang,
                "code": code_text.strip(),
            })

    # Standalone <code> not inside <pre> (inline code)
    for code in soup.find_all("code"):
        if code.find_parent("pre"):
            continue
        text = code.get_text(strip=True)
        if text and len(text) > 5:
            blocks.append({
                "language": "",
                "code": text,
            })

    return blocks


def _get_blockquotes(soup: BeautifulSoup) -> List[str]:
    """Extract blockquote text."""

    quotes = []
    for bq in soup.find_all("blockquote"):
        text = bq.get_text(strip=True)
        if text:
            quotes.append(text)

    return quotes
