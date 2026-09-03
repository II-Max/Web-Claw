"""
Scraper V6 — Advanced web page fetcher with:
- Requests (fast, lightweight) as primary method
- Playwright (headless browser) as fallback for JS-rendered pages
- Anti-detection: random UA, realistic headers, random delays
- Proxy support (HTTP/HTTPS/SOCKS5)
- Cookie & authentication support
- SSL/TLS flexibility
"""

import time
import random
import json
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

from core.config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF,
)
from core.user_agents import get_random_headers
from core.logger import logger


# ===== SCRAPER OPTIONS =====

@dataclass
class ScrapeOptions:
    """Configuration options for the scraper."""
    use_js: bool = False              # Force headless browser
    verify_ssl: bool = True           # SSL certificate verification
    proxy: str = ""                   # Proxy URL (http/https/socks5)
    cookies: Dict[str, str] = field(default_factory=dict)
    cookie_file: str = ""             # Path to cookies.json
    headers: Dict[str, str] = field(default_factory=dict)
    auth: str = ""                    # "user:pass" for HTTP Basic Auth
    delay_min: float = 0.5            # Min delay between requests (seconds)
    delay_max: float = 2.0            # Max delay between requests (seconds)
    timeout: int = REQUEST_TIMEOUT
    max_retries: int = MAX_RETRIES


# ===== SESSION FACTORY =====

def _build_session(options: ScrapeOptions) -> requests.Session:
    """Build a requests.Session with all configured options."""
    session = requests.Session()

    # Set headers (random UA + realistic browser headers)
    headers = get_random_headers()
    headers.update(options.headers)
    session.headers.update(headers)

    # Proxy
    if options.proxy:
        session.proxies = {
            "http": options.proxy,
            "https": options.proxy,
        }
        logger.info(f"Using proxy: {options.proxy}")

    # Cookies
    cookies = dict(options.cookies)
    if options.cookie_file:
        cookies.update(_load_cookies(options.cookie_file))
    if cookies:
        session.cookies.update(cookies)
        logger.info(f"Loaded {len(cookies)} cookies")

    # HTTP Basic Auth
    if options.auth:
        parts = options.auth.split(":", 1)
        if len(parts) == 2:
            session.auth = (parts[0], parts[1])
            logger.info("HTTP Basic Auth configured")

    return session


def _load_cookies(cookie_file: str) -> Dict[str, str]:
    """Load cookies from a JSON file."""
    try:
        path = Path(cookie_file)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Support both {name: value} and [{name, value}] formats
            if isinstance(data, list):
                return {c["name"]: c["value"] for c in data if "name" in c and "value" in c}
            elif isinstance(data, dict):
                return data
    except Exception as e:
        logger.warning(f"Failed to load cookies from {cookie_file}: {e}")
    return {}


# ===== REQUESTS-BASED FETCHER =====

def _fetch_with_requests(
    url: str,
    options: ScrapeOptions,
) -> Tuple[Optional[str], Optional[BeautifulSoup]]:
    """Fetch a page using requests library (fast, no JS)."""

    session = _build_session(options)

    for attempt in range(1, options.max_retries + 1):
        try:
            logger.info(
                f"[Requests] Connecting to: {url} (attempt {attempt}/{options.max_retries})"
            )

            response = session.get(
                url,
                timeout=options.timeout,
                allow_redirects=True,
                verify=options.verify_ssl,
            )
            response.raise_for_status()

            # Fix encoding
            if response.encoding is None or response.encoding == "ISO-8859-1":
                response.encoding = response.apparent_encoding

            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            logger.info(f"[Requests] Success: {url} ({len(html)} bytes)")
            return html, soup

        except requests.exceptions.SSLError as e:
            logger.warning(f"SSL Error for {url}: {e}")
            if options.verify_ssl:
                logger.info("Tip: Use --no-verify to skip SSL verification")
            if attempt < options.max_retries:
                _wait_retry(attempt)
            else:
                logger.error(f"All {options.max_retries} attempts failed (SSL) for {url}")

        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt}/{options.max_retries} failed for {url}: {e}"
            )
            if attempt < options.max_retries:
                _wait_retry(attempt)
            else:
                logger.error(f"All {options.max_retries} attempts failed for {url}")

    return None, None


# ===== PLAYWRIGHT-BASED FETCHER =====

def _fetch_with_playwright(
    url: str,
    options: ScrapeOptions,
) -> Tuple[Optional[str], Optional[BeautifulSoup]]:
    """Fetch a page using Playwright headless browser (supports JS rendering)."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error(
            "Playwright is not installed. Install with:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
        return None, None

    for attempt in range(1, options.max_retries + 1):
        try:
            logger.info(
                f"[Playwright] Launching headless browser for: {url} "
                f"(attempt {attempt}/{options.max_retries})"
            )

            with sync_playwright() as p:
                # Browser launch options
                launch_args = {
                    "headless": True,
                }
                if options.proxy:
                    launch_args["proxy"] = {"server": options.proxy}

                # Try Chromium first, then Firefox
                try:
                    browser = p.chromium.launch(**launch_args)
                except Exception:
                    logger.info("Chromium not available, trying Firefox...")
                    try:
                        browser = p.firefox.launch(**launch_args)
                    except Exception as e:
                        logger.error(
                            f"No browser available. Run: playwright install chromium\n"
                            f"Error: {e}"
                        )
                        return None, None

                context_opts = {
                    "ignore_https_errors": not options.verify_ssl,
                    "user_agent": get_random_headers()["User-Agent"],
                }
                context = browser.new_context(**context_opts)

                # Load cookies
                cookies_to_set = dict(options.cookies)
                if options.cookie_file:
                    cookies_to_set.update(_load_cookies(options.cookie_file))
                if cookies_to_set:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    cookie_list = [
                        {
                            "name": k,
                            "value": v,
                            "domain": parsed.netloc,
                            "path": "/",
                        }
                        for k, v in cookies_to_set.items()
                    ]
                    context.add_cookies(cookie_list)

                # Set custom headers
                if options.headers:
                    context.set_extra_http_headers(options.headers)

                page = context.new_page()

                # Navigate with timeout
                page.goto(url, wait_until="networkidle", timeout=options.timeout * 1000)

                # Wait a bit for dynamic content
                page.wait_for_timeout(2000)

                html = page.content()
                browser.close()

            soup = BeautifulSoup(html, "html.parser")
            logger.info(f"[Playwright] Success: {url} ({len(html)} bytes)")
            return html, soup

        except Exception as e:
            logger.warning(
                f"[Playwright] Attempt {attempt}/{options.max_retries} failed for {url}: {e}"
            )
            if attempt < options.max_retries:
                _wait_retry(attempt)
            else:
                logger.error(f"[Playwright] All {options.max_retries} attempts failed for {url}")

    return None, None


# ===== SMART FETCH (AUTO-FALLBACK) =====

def _is_content_likely_js_rendered(html: str, soup: BeautifulSoup) -> bool:
    """Heuristic: check if the page likely needs JS rendering."""
    if not html or not soup:
        return False

    body = soup.find("body")
    if not body:
        return True

    body_text = body.get_text(strip=True)

    # Very little visible text but has JS
    scripts = soup.find_all("script")
    if len(body_text) < 100 and len(scripts) > 3:
        return True

    # Common SPA framework markers
    spa_markers = [
        'id="__next"',       # Next.js
        'id="__nuxt"',       # Nuxt.js
        'id="app"',          # Vue.js
        'id="root"',         # React
        'ng-app',            # Angular
        'data-reactroot',    # React
    ]
    html_lower = html[:5000].lower()
    for marker in spa_markers:
        if marker.lower() in html_lower:
            if len(body_text) < 200:
                return True

    return False


def fetch_page(
    url: str,
    options: Optional[ScrapeOptions] = None,
) -> Tuple[Optional[str], Optional[BeautifulSoup]]:
    """
    Smart page fetcher with automatic fallback.

    Strategy:
    1. If --js flag is set → use Playwright directly
    2. Otherwise → try requests first
    3. If requests returns near-empty content → auto-fallback to Playwright

    Returns (html_text, soup) tuple. Both None on failure.
    """

    if options is None:
        options = ScrapeOptions()

    # Random delay for anti-detection
    if options.delay_min > 0:
        delay = random.uniform(options.delay_min, options.delay_max)
        logger.debug(f"Anti-detection delay: {delay:.1f}s")
        time.sleep(delay)

    # Force JS mode
    if options.use_js:
        logger.info("JS mode enabled — using headless browser")
        return _fetch_with_playwright(url, options)

    # Try requests first (fast)
    html, soup = _fetch_with_requests(url, options)

    if html and soup:
        # Check if content might need JS rendering
        if _is_content_likely_js_rendered(html, soup):
            logger.info(
                "Page appears to be JS-rendered (little content found). "
                "Auto-falling back to headless browser..."
            )
            js_html, js_soup = _fetch_with_playwright(url, options)
            if js_html and js_soup:
                return js_html, js_soup
            # If Playwright fails, return what we got from requests
            logger.warning("Playwright fallback failed, using requests result")

    return html, soup


def _wait_retry(attempt: int) -> None:
    """Wait with exponential backoff before retrying."""
    wait = RETRY_BACKOFF ** attempt
    logger.info(f"Retrying in {wait}s...")
    time.sleep(wait)