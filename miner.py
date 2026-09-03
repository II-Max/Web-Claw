"""
WebMiner V6 — Orchestrator that runs all extractors
and exports data to multiple formats (Markdown, JSON, CSV, Excel).
"""

from typing import Any, Dict, Optional, Set
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from core.scraper import fetch_page, ScrapeOptions
from core.logger import logger

# Extractors
from core.extractors.metadata_extractor import extract_metadata
from core.extractors.text_extractor import extract_text_content
from core.extractors.link_extractor import extract_links
from core.extractors.media_extractor import extract_media
from core.extractors.contact_extractor import extract_contacts
from core.extractors.table_extractor import extract_tables
from core.extractors.form_extractor import extract_forms
from core.extractors.nav_extractor import extract_navigation

# Exporters
from core.exporters.markdown_exporter import export_markdown
from core.exporters.json_exporter import export_json
from core.exporters.csv_exporter import export_csv
from core.exporters.excel_exporter import export_excel


class WebMiner:
    """
    Main orchestrator for Web-Claw V6.
    Fetches a page, runs all extractors, exports to multiple formats.
    """

    def __init__(self, url: str, options: Optional[ScrapeOptions] = None, formats: Optional[Set[str]] = None) -> None:
        self.url = url
        self.options = options or ScrapeOptions()
        self.formats = formats or {"md", "json", "csv", "xlsx"}
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
        return name[:80]

    def fetch(self) -> bool:
        """Fetch the webpage. Returns True if successful."""
        self.html, self.soup = fetch_page(self.url, self.options)
        return self.html is not None and self.soup is not None

    def mine_all(self) -> Dict[str, Any]:
        """Run ALL extractors and collect data."""
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
        """Export all data to requested formats."""
        if not self.data:
            logger.warning("No data to export. Run mine_all() first.")
            return {}

        paths = {}
        fmts = self.formats

        if "md" in fmts or "all" in fmts:
            paths["markdown"] = str(export_markdown(self.data, self.site_name))

        if "json" in fmts or "all" in fmts:
            paths["json"] = str(export_json(self.data, self.site_name))

        if "csv" in fmts or "all" in fmts:
            paths["csv"] = str(export_csv(self.data, self.site_name))

        if "xlsx" in fmts or "all" in fmts:
            paths["excel"] = str(export_excel(self.data, self.site_name))

        return paths

    def run(self) -> Dict[str, Any]:
        """Complete pipeline: fetch -> mine -> export."""
        if not self.fetch():
            logger.error(f"Failed to fetch: {self.url}")
            return {}

        self.mine_all()
        paths = self.export_all()

        logger.info(
            f"Pipeline complete for {self.url} -> "
            + ", ".join(f"{k}: {v}" for k, v in paths.items())
        )

        return self.data
