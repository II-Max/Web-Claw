"""
CSV Exporter — Export extracted data as CSV files.
UTF-8 BOM encoding for Excel compatibility.
"""

import csv
from pathlib import Path
from typing import Any, Dict

from core.config import CSV_DIR
from core.logger import logger


def export_csv(data: Dict[str, Any], site_name: str) -> Path:
    """Export extracted data to CSV files. Returns the output directory path."""
    out_dir = CSV_DIR / site_name
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Exporting CSV to: {out_dir}")

    _export_links_csv(data.get("links", {}), out_dir)
    _export_contacts_csv(data.get("contacts", {}), out_dir)
    _export_media_csv(data.get("media", {}), out_dir)
    _export_tables_csv(data.get("tables", {}), out_dir)
    _export_text_csv(data.get("text", {}), out_dir)

    logger.info(f"CSV export complete: {out_dir}")
    return out_dir


def _write_csv(path: Path, headers: list, rows: list) -> None:
    """Write CSV with UTF-8 BOM for Excel compatibility."""
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def _export_links_csv(links, out_dir):
    all_links = links.get("all_links", [])
    if all_links:
        headers = ["URL", "Text", "Title", "Rel", "Target"]
        rows = [[l.get("url", ""), l.get("text", ""), l.get("title", ""), l.get("rel", ""), l.get("target", "")] for l in all_links]
        _write_csv(out_dir / "links.csv", headers, rows)

    social = links.get("social_media", [])
    if social:
        headers = ["Platform", "URL", "Text"]
        rows = [[s.get("platform", ""), s.get("url", ""), s.get("text", "")] for s in social]
        _write_csv(out_dir / "social_links.csv", headers, rows)


def _export_contacts_csv(contacts, out_dir):
    emails = contacts.get("emails", [])
    if emails:
        headers = ["Email", "Source", "Context"]
        rows = [[e.get("email", ""), e.get("source", ""), e.get("context", "")] for e in emails]
        _write_csv(out_dir / "emails.csv", headers, rows)

    phones = contacts.get("phones", [])
    if phones:
        headers = ["Phone", "Normalized", "Source", "Context"]
        rows = [[p.get("phone", ""), p.get("normalized", ""), p.get("source", ""), p.get("context", "")] for p in phones]
        _write_csv(out_dir / "phones.csv", headers, rows)


def _export_media_csv(media, out_dir):
    images = media.get("images", [])
    if images:
        headers = ["Source URL", "Alt Text", "Title", "Width", "Height"]
        rows = [[i.get("src", ""), i.get("alt", ""), i.get("title", ""), i.get("width", ""), i.get("height", "")] for i in images]
        _write_csv(out_dir / "images.csv", headers, rows)


def _export_tables_csv(tables_data, out_dir):
    tables = tables_data.get("tables", [])
    for table in tables:
        idx = table.get("index", 0)
        cols = table.get("column_names", [])
        data_rows = table.get("data", [])
        if cols and data_rows:
            rows = [[str(row.get(c, "")) for c in cols] for row in data_rows]
            _write_csv(out_dir / f"table_{idx}.csv", cols, rows)


def _export_text_csv(text, out_dir):
    paragraphs = text.get("paragraphs", [])
    if paragraphs:
        headers = ["#", "Paragraph"]
        rows = [[i, p] for i, p in enumerate(paragraphs, 1)]
        _write_csv(out_dir / "paragraphs.csv", headers, rows)

    headings = text.get("headings", {})
    if headings:
        headers = ["Level", "Heading"]
        rows = []
        for level, items in sorted(headings.items()):
            for item in items:
                rows.append([level.upper(), item])
        _write_csv(out_dir / "headings.csv", headers, rows)
