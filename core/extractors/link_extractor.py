"""
Link Extractor — Extract and categorize all links:
internal, external, download files, social media.
"""

from typing import Any, Dict, List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from core.config import (
    SOCIAL_DOMAINS,
    ALL_DOWNLOAD_EXTENSIONS,
    DOWNLOAD_EXTENSIONS,
)
from core.logger import logger


def extract_links(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    """Extract and categorize all links from the page."""

    logger.info("Extracting links...")

    base_domain = urlparse(base_url).netloc.replace("www.", "")

    all_links = []
    internal = []
    external = []
    downloads = []
    social = []
    anchors = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            if href.startswith("#"):
                anchors.append({
                    "anchor": href,
                    "text": a_tag.get_text(strip=True),
                })
            continue

        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        link_data = {
            "url": full_url,
            "text": a_tag.get_text(strip=True),
            "title": a_tag.get("title", ""),
            "rel": " ".join(a_tag.get("rel", [])),
            "target": a_tag.get("target", ""),
        }

        all_links.append(link_data)

        # Classify: social media
        link_domain = parsed.netloc.replace("www.", "").lower()
        is_social = False
        for platform, domains in SOCIAL_DOMAINS.items():
            if any(d in link_domain for d in domains):
                social.append({
                    **link_data,
                    "platform": platform,
                })
                is_social = True
                break

        # Classify: download file
        path_lower = parsed.path.lower()
        is_download = False
        if any(path_lower.endswith(ext) for ext in ALL_DOWNLOAD_EXTENSIONS):
            file_type = "other"
            for category, exts in DOWNLOAD_EXTENSIONS.items():
                if any(path_lower.endswith(ext) for ext in exts):
                    file_type = category
                    break
            downloads.append({
                **link_data,
                "file_type": file_type,
                "filename": parsed.path.split("/")[-1] if "/" in parsed.path else parsed.path,
            })
            is_download = True

        # Classify: internal vs external
        if not is_social and not is_download:
            if base_domain in link_domain or not parsed.netloc:
                internal.append(link_data)
            else:
                external.append(link_data)

    data = {
        "total_count": len(all_links),
        "internal": internal,
        "external": external,
        "social_media": social,
        "downloads": downloads,
        "anchors": anchors,
        "all_links": all_links,
    }

    logger.info(
        f"Links extracted: {len(internal)} internal, "
        f"{len(external)} external, {len(social)} social, "
        f"{len(downloads)} downloads"
    )

    return data
