import time
from typing import Optional, Tuple

import requests
from bs4 import BeautifulSoup

from web_miner.core.config import (
    USER_AGENT,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF,
)
from web_miner.core.logger import logger

# ===== SESSION SETUP =====

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})


def fetch_page(url: str) -> Tuple[Optional[str], Optional[BeautifulSoup]]:
    """
    Fetch a webpage with retry logic.
    Returns (html_text, soup) tuple. Both None on failure.
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Connecting to: {url} (attempt {attempt}/{MAX_RETRIES})")

            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
            )
            response.raise_for_status()

            # Fix encoding
            response.encoding = response.apparent_encoding

            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            logger.info(f"Success: {url}")
            return html, soup

        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}"
            )

            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF ** attempt
                logger.info(f"Retrying in {wait}s...")
                time.sleep(wait)
            else:
                logger.error(f"All {MAX_RETRIES} attempts failed for {url}")

    return None, None
