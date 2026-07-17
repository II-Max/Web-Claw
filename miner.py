"""
WebMiner V5 — Orchestrator that runs all extractors
and exports data to Markdown + JSON.
"""

from typing import Any, Dict, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from web_miner.core.scraper import fetch_page
from web_miner.core.logger import logger

# Extractors
from web_miner.core.extractors.metadata_extractor import extract_metadata
from web_miner.core.extractors.text_extractor import extract_text_content
from web_miner.core.extractors.link_extractor import extract_links
from web_miner.core.extractors.media_extractor import extract_media
from web_miner.core.extractors.contact_extractor import extract_contacts
from web_miner.core.extractors.table_extractor import extract_tables
from web_miner.core.extractors.form_extractor import extract_forms
from web_miner.core.extractors.nav_extractor import extract_navigation

# Exporters
from web_miner.core.exporters.markdown_exporter import export_markdown
from web_miner.core.exporters.json_exporter import export_json


class WebMiner:
    """
    Main orchestrator for DataMine V5.
    Fetches a page, runs all extractors, exports to MD + JSON.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.html: Optional[str] = None
        self.soup: Optional[BeautifulSoup] = None
        self.data: Dict[str, Any] = {}
        self.site_name = self._make_site_name(url)

    @staticmethod
    def _make_site_name(url: str) -> str:
        """Generate a safe folder name from URL."""
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        path = parsed.path.strip("/").replace("/", "_")
        name = domain.replace(".", "_").replace(":", "_")
        if path:
            name += f"_{path}"
        # Keep it reasonable length
        return name[:80]

    def fetch(self) -> bool:
        """Fetch the webpage. Returns True if successful."""
        self.html, self.soup = fetch_page(self.url)
        return self.html is not None and self.soup is not None

    def mine_all(self) -> Dict[str, Any]:
        """
        Run ALL extractors and collect data.
        Returns the complete extracted data dict.
        """

        if not self.html or not self.soup:
            logger.error("Cannot mine: page not fetched yet")
            return {}

        logger.info(f"Starting full mining of: {self.url}")

        self.data = {
            "metadata": extract_metadata(self.soup, self.url),
            "text": extract_text_content(self.soup),
            "links": extract_links(self.soup, self.url),
            "media": extract_media(self.soup, self.url),
            "contacts": extract_contacts(self.soup, self.html),
            "tables": extract_tables(self.soup, self.html),
            "forms": extract_forms(self.soup, self.url),
            "navigation": extract_navigation(self.soup, self.url),
        }

        logger.info("Full mining complete")
        return self.data

    def export_all(self) -> Dict[str, str]:
        """
        Export all data to Markdown + JSON.
        Returns dict with paths to output directories.
        """

        if not self.data:
            logger.warning("No data to export. Run mine_all() first.")
            return {}

        md_dir = export_markdown(self.data, self.site_name)
        json_dir = export_json(self.data, self.site_name)

        return {
            "markdown": str(md_dir),
            "json": str(json_dir),
        }

    def run(self) -> Dict[str, Any]:
        """
        Complete pipeline: fetch → mine → export.
        Returns the extracted data dict.
        """

        if not self.fetch():
            logger.error(f"Failed to fetch: {self.url}")
            return {}

        self.mine_all()
        paths = self.export_all()

        logger.info(
            f"Pipeline complete for {self.url} → "
            f"MD: {paths.get('markdown', 'N/A')}, "
            f"JSON: {paths.get('json', 'N/A')}"
        )

        return self.data
