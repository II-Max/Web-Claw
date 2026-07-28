"""
JSON Exporter — Export all extracted data as
structured JSON files.
"""

import json
import datetime
from pathlib import Path
from typing import Any, Dict

from core.config import JSON_DIR
from core.logger import logger


def export_json(data: Dict[str, Any], site_name: str) -> Path:
    """
    Export all extracted data to JSON files.
    Returns the output directory path.
    """

    out_dir = JSON_DIR / site_name
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Exporting JSON to: {out_dir}")

    # Add export metadata
    export_meta = {
        "exported_at": datetime.datetime.now().isoformat(),
        "site_name": site_name,
        "url": data.get("metadata", {}).get("url", ""),
    }

    # Full data (everything in one file)
    full_data = {
        "_export": export_meta,
        **data,
    }
    _write_json(out_dir / "full_data.json", full_data)

    # Individual category files
    _write_json(
        out_dir / "metadata.json",
        {"_export": export_meta, "metadata": data.get("metadata", {})}
    )

    _write_json(
        out_dir / "tables.json",
        {"_export": export_meta, "tables": data.get("tables", {})}
    )

    _write_json(
        out_dir / "links.json",
        {"_export": export_meta, "links": data.get("links", {})}
    )

    _write_json(
        out_dir / "media.json",
        {"_export": export_meta, "media": data.get("media", {})}
    )

    _write_json(
        out_dir / "contacts.json",
        {"_export": export_meta, "contacts": data.get("contacts", {})}
    )

    _write_json(
        out_dir / "text_content.json",
        {"_export": export_meta, "text": data.get("text", {})}
    )

    _write_json(
        out_dir / "forms_and_code.json",
        {
            "_export": export_meta,
            "forms": data.get("forms", {}),
            "navigation": data.get("navigation", {}),
        }
    )

    logger.info(f"JSON export complete: {out_dir}")
    return out_dir


def _write_json(path: Path, data: Dict) -> None:
    """Write data to a JSON file with pretty printing."""

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            default=str,  # Handle non-serializable types
        )
