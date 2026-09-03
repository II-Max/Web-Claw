"""
Crawler V6 — Multi-page web crawler that follows links
within the same domain, collecting URLs for batch scraping.
"""

from typing import Set, List, Optional
from urllib.parse import urljoin, urlparse
from collections import deque

from bs4 import BeautifulSoup

from core.scraper import fetch_page, ScrapeOptions
from core.config import DEFAULT_CRAWL_DEPTH, DEFAULT_MAX_PAGES, MAX_CRAWL_DEPTH, MAX_PAGES_LIMIT
from core.logger import logger


def crawl_urls(
    start_url: str,
    depth: int = DEFAULT_CRAWL_DEPTH,
    max_pages: int = DEFAULT_MAX_PAGES,
    same_domain: bool = True,
    options: Optional[ScrapeOptions] = None,
) -> List[str]:
    """
    Crawl starting from start_url, discover linked pages up to the given depth.
    Returns a list of unique URLs to scrape.
    """

    # Safety clamps
    depth = min(max(depth, 1), MAX_CRAWL_DEPTH)
    max_pages = min(max(max_pages, 1), MAX_PAGES_LIMIT)

    if depth <= 1:
        return [start_url]

    if options is None:
        options = ScrapeOptions()

    base_parsed = urlparse(start_url)
    base_domain = base_parsed.netloc.replace("www.", "").lower()

    visited: Set[str] = set()
    to_visit: deque = deque()
    to_visit.append((start_url, 0))
    discovered_urls: List[str] = []

    logger.info(f"Starting crawl from: {start_url} (depth={depth}, max_pages={max_pages})")

    while to_visit and len(discovered_urls) < max_pages:
        current_url, current_depth = to_visit.popleft()

        # Normalize URL
        normalized = _normalize_url(current_url)
        if normalized in visited:
            continue
        visited.add(normalized)
        discovered_urls.append(current_url)

        logger.info(f"Crawled [{len(discovered_urls)}/{max_pages}] depth={current_depth}: {current_url}")

        # Don't follow links beyond max depth
        if current_depth >= depth - 1:
            continue

        # Fetch page to find links
        html, soup = fetch_page(current_url, options)
        if not html or not soup:
            continue

        # Extract links
        for link_url in _extract_page_links(soup, current_url, base_domain, same_domain):
            link_normalized = _normalize_url(link_url)
            if link_normalized not in visited and len(discovered_urls) + len(to_visit) < max_pages * 2:
                to_visit.append((link_url, current_depth + 1))

    logger.info(f"Crawl complete: {len(discovered_urls)} URLs discovered")
    return discovered_urls


def _normalize_url(url: str) -> str:
    """Normalize URL for deduplication."""
    parsed = urlparse(url)
    # Remove fragment, trailing slash, normalize domain
    normalized = f"{parsed.scheme}://{parsed.netloc.replace('www.', '').lower()}{parsed.path.rstrip('/')}"
    if parsed.query:
        normalized += f"?{parsed.query}"
    return normalized


def _extract_page_links(soup: BeautifulSoup, base_url: str, base_domain: str, same_domain: bool) -> List[str]:
    """Extract followable links from a page."""
    links = []

    skip_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar',
        '.mp3', '.mp4', '.avi', '.mkv', '.mov', '.wav',
        '.css', '.js', '.xml', '.json',
    }

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()

        # Skip non-HTTP links
        if not href or href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("tel:"):
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Only HTTP(S)
        if parsed.scheme not in ("http", "https"):
            continue

        # Skip file downloads
        path_lower = parsed.path.lower()
        if any(path_lower.endswith(ext) for ext in skip_extensions):
            continue

        # Same domain check
        if same_domain:
            link_domain = parsed.netloc.replace("www.", "").lower()
            if base_domain not in link_domain:
                continue

        links.append(full_url)

    return links
