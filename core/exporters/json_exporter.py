"""
JSON Exporter — Export all extracted data as structured JSON files.
"""

import json
import datetime
from pathlib import Path
from typing import Any, Dict

from core.config import JSON_DIR
from core.logger import logger


def export_json(data: Dict[str, Any], site_name: str) -> Path:
    """Export all extracted data to JSON files. Returns the output directory path."""
    out_dir = JSON_DIR / site_name
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Exporting JSON to: {out_dir}")

    export_meta = {
        "exported_at": datetime.datetime.now().isoformat(),
        "site_name": site_name,
        "url": data.get("metadata", {}).get("url", ""),
    }

    full_data = {"_export": export_meta, **data}
    _write_json(out_dir / "full_data.json", full_data)

    categories = [
        ("metadata.json", {"metadata": data.get("metadata", {})}),
        ("tables.json", {"tables": data.get("tables", {})}),
        ("links.json", {"links": data.get("links", {})}),
        ("media.json", {"media": data.get("media", {})}),
        ("contacts.json", {"contacts": data.get("contacts", {})}),
        ("text_content.json", {"text": data.get("text", {})}),
        ("forms_and_code.json", {"forms": data.get("forms", {}), "navigation": data.get("navigation", {})}),
    ]
    for filename, content in categories:
        _write_json(out_dir / filename, {"_export": export_meta, **content})

    logger.info(f"JSON export complete: {out_dir}")
    return out_dir


def _write_json(path: Path, data: Dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
