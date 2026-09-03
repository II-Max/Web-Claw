"""
Excel Exporter — Export all extracted data into a single .xlsx file
with multiple sheets for easy viewing in Excel/LibreOffice.
"""

from pathlib import Path
from typing import Any, Dict

import pandas as pd

from core.config import EXCEL_DIR
from core.logger import logger


def export_excel(data: Dict[str, Any], site_name: str) -> Path:
    """Export all extracted data to a single Excel file with multiple sheets."""
    out_dir = EXCEL_DIR / site_name
    out_dir.mkdir(parents=True, exist_ok=True)
    xlsx_path = out_dir / "data.xlsx"

    logger.info(f"Exporting Excel to: {xlsx_path}")

    try:
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            _write_metadata_sheet(data, writer)
            _write_links_sheet(data, writer)
            _write_contacts_sheet(data, writer)
            _write_media_sheet(data, writer)
            _write_tables_sheet(data, writer)
            _write_headings_sheet(data, writer)
            _write_paragraphs_sheet(data, writer)
    except Exception as e:
        logger.error(f"Excel export failed: {e}")
        return out_dir

    logger.info(f"Excel export complete: {xlsx_path}")
    return out_dir


def _safe_df(data_list, columns=None):
    """Create a DataFrame safely, returning empty DF on failure."""
    try:
        if not data_list:
            return pd.DataFrame(columns=columns or [])
        return pd.DataFrame(data_list, columns=columns)
    except Exception:
        return pd.DataFrame(columns=columns or [])


def _write_metadata_sheet(data, writer):
    meta = data.get("metadata", {})
    rows = []
    for key in ["url", "title", "description", "keywords", "author", "canonical", "language", "charset", "favicon", "robots", "viewport", "generator"]:
        rows.append({"Property": key.title(), "Value": str(meta.get(key, ""))})
    og = meta.get("og", {})
    for k, v in og.items():
        rows.append({"Property": f"OG: {k}", "Value": str(v)})
    tc = meta.get("twitter", {})
    for k, v in tc.items():
        rows.append({"Property": f"Twitter: {k}", "Value": str(v)})
    df = _safe_df(rows)
    if not df.empty:
        df.to_excel(writer, sheet_name="Metadata", index=False)


def _write_links_sheet(data, writer):
    links = data.get("links", {})
    all_links = links.get("all_links", [])
    if all_links:
        rows = [{"URL": l.get("url", ""), "Text": l.get("text", ""), "Title": l.get("title", ""), "Rel": l.get("rel", ""), "Target": l.get("target", "")} for l in all_links]
        _safe_df(rows).to_excel(writer, sheet_name="Links", index=False)

    social = links.get("social_media", [])
    if social:
        rows = [{"Platform": s.get("platform", ""), "URL": s.get("url", ""), "Text": s.get("text", "")} for s in social]
        _safe_df(rows).to_excel(writer, sheet_name="Social Links", index=False)


def _write_contacts_sheet(data, writer):
    contacts = data.get("contacts", {})
    emails = contacts.get("emails", [])
    if emails:
        rows = [{"Email": e.get("email", ""), "Source": e.get("source", ""), "Context": e.get("context", "")} for e in emails]
        _safe_df(rows).to_excel(writer, sheet_name="Emails", index=False)

    phones = contacts.get("phones", [])
    if phones:
        rows = [{"Phone": p.get("phone", ""), "Normalized": p.get("normalized", ""), "Source": p.get("source", "")} for p in phones]
        _safe_df(rows).to_excel(writer, sheet_name="Phones", index=False)


def _write_media_sheet(data, writer):
    media = data.get("media", {})
    images = media.get("images", [])
    if images:
        rows = [{"Source": i.get("src", ""), "Alt": i.get("alt", ""), "Width": i.get("width", ""), "Height": i.get("height", "")} for i in images]
        _safe_df(rows).to_excel(writer, sheet_name="Images", index=False)


def _write_tables_sheet(data, writer):
    tables_data = data.get("tables", {})
    tables = tables_data.get("tables", [])
    for table in tables[:10]:  # Limit to 10 tables
        idx = table.get("index", 0)
        cols = table.get("column_names", [])
        rows = table.get("data", [])
        if cols and rows:
            sheet_name = f"Table {idx}"[:31]  # Excel sheet name limit
            _safe_df(rows).to_excel(writer, sheet_name=sheet_name, index=False)


def _write_headings_sheet(data, writer):
    text = data.get("text", {})
    headings = text.get("headings", {})
    if headings:
        rows = []
        for level, items in sorted(headings.items()):
            for item in items:
                rows.append({"Level": level.upper(), "Heading": item})
        _safe_df(rows).to_excel(writer, sheet_name="Headings", index=False)


def _write_paragraphs_sheet(data, writer):
    text = data.get("text", {})
    paragraphs = text.get("paragraphs", [])
    if paragraphs:
        rows = [{"#": i, "Paragraph": p} for i, p in enumerate(paragraphs, 1)]
        _safe_df(rows).to_excel(writer, sheet_name="Paragraphs", index=False)
