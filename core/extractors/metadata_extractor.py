"""
Metadata Extractor — Extract meta tags, OG, Twitter cards,
structured data (JSON-LD), canonical URL, favicon, etc.
"""

import json
from typing import Any, Dict, List
from bs4 import BeautifulSoup

from core.logger import logger


def extract_metadata(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Extract all metadata from the page."""

    logger.info("Extracting metadata...")

    data = {
        "url": url,
        "title": _get_title(soup),
        "description": _get_meta(soup, "description"),
        "keywords": _get_meta(soup, "keywords"),
        "author": _get_meta(soup, "author"),
        "robots": _get_meta(soup, "robots"),
        "canonical": _get_canonical(soup),
        "favicon": _get_favicon(soup),
        "charset": _get_charset(soup),
        "language": _get_language(soup),
        "viewport": _get_meta(soup, "viewport"),
        "generator": _get_meta(soup, "generator"),
        "og": _get_og_tags(soup),
        "twitter": _get_twitter_cards(soup),
        "json_ld": _get_json_ld(soup),
        "other_meta": _get_other_meta(soup),
    }

    logger.info(
        f"Metadata extracted: title='{data['title'][:50]}...'"
        if data['title'] and len(data['title']) > 50
        else f"Metadata extracted: title='{data['title']}'"
    )

    return data


def _get_title(soup: BeautifulSoup) -> str:
    """Get page title."""
    tag = soup.find("title")
    return tag.get_text(strip=True) if tag else ""


def _get_meta(soup: BeautifulSoup, name: str) -> str:
    """Get a meta tag content by name."""
    tag = soup.find("meta", attrs={"name": name})
    if not tag:
        tag = soup.find("meta", attrs={"name": name.capitalize()})
    return tag.get("content", "") if tag else ""


def _get_canonical(soup: BeautifulSoup) -> str:
    """Get canonical URL."""
    tag = soup.find("link", rel="canonical")
    return tag.get("href", "") if tag else ""


def _get_favicon(soup: BeautifulSoup) -> str:
    """Get favicon URL."""
    for rel in [["icon"], ["shortcut", "icon"], ["apple-touch-icon"]]:
        tag = soup.find("link", rel=rel)
        if tag:
            return tag.get("href", "")
    return ""


def _get_charset(soup: BeautifulSoup) -> str:
    """Get charset."""
    tag = soup.find("meta", charset=True)
    if tag:
        return tag.get("charset", "")
    tag = soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if tag:
        content = tag.get("content", "")
        if "charset=" in content:
            return content.split("charset=")[-1].strip()
    return ""


def _get_language(soup: BeautifulSoup) -> str:
    """Get page language."""
    html_tag = soup.find("html")
    if html_tag:
        return html_tag.get("lang", "")
    return ""


def _get_og_tags(soup: BeautifulSoup) -> Dict[str, str]:
    """Get all Open Graph tags."""
    og = {}
    for tag in soup.find_all("meta", property=True):
        prop = tag.get("property", "")
        if prop.startswith("og:"):
            og[prop] = tag.get("content", "")
    return og


def _get_twitter_cards(soup: BeautifulSoup) -> Dict[str, str]:
    """Get Twitter card tags."""
    tc = {}
    for tag in soup.find_all("meta", attrs={"name": True}):
        name = tag.get("name", "")
        if name.startswith("twitter:"):
            tc[name] = tag.get("content", "")
    return tc


def _get_json_ld(soup: BeautifulSoup) -> List[Dict]:
    """Extract JSON-LD structured data."""
    scripts = soup.find_all("script", type="application/ld+json")
    results = []

    for script in scripts:
        try:
            text = script.string
            if text:
                data = json.loads(text)
                results.append(data)
        except (json.JSONDecodeError, TypeError):
            continue

    return results


def _get_other_meta(soup: BeautifulSoup) -> Dict[str, str]:
    """Get all other meta tags not covered above."""
    skip_names = {
        "description", "keywords", "author", "robots",
        "viewport", "generator",
    }
    other = {}

    for tag in soup.find_all("meta"):
        name = tag.get("name", "")
        prop = tag.get("property", "")

        if name and name.lower() not in skip_names:
            if not name.startswith("twitter:"):
                other[name] = tag.get("content", "")
        elif prop and not prop.startswith("og:"):
            other[prop] = tag.get("content", "")

    return other
