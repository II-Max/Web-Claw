"""
Form Extractor — Extract HTML forms, their actions,
methods, and all input/select/textarea fields.
"""

from typing import Any, Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from core.logger import logger


def extract_forms(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    """Extract all forms and their fields from the page."""

    logger.info("Extracting forms...")

    forms = []

    for form in soup.find_all("form"):
        action = form.get("action", "")
        if action:
            action = urljoin(base_url, action)

        form_data = {
            "action": action,
            "method": form.get("method", "GET").upper(),
            "id": form.get("id", ""),
            "name": form.get("name", ""),
            "class": " ".join(form.get("class", [])),
            "enctype": form.get("enctype", ""),
            "fields": _get_fields(form),
        }

        forms.append(form_data)

    logger.info(f"Forms extracted: {len(forms)}")

    return {
        "count": len(forms),
        "forms": forms,
    }


def _get_fields(form) -> List[Dict[str, str]]:
    """Extract all input, select, and textarea fields from a form."""

    fields = []

    # Input fields
    for inp in form.find_all("input"):
        field = {
            "tag": "input",
            "type": inp.get("type", "text"),
            "name": inp.get("name", ""),
            "id": inp.get("id", ""),
            "placeholder": inp.get("placeholder", ""),
            "value": inp.get("value", ""),
            "required": inp.has_attr("required"),
        }
        fields.append(field)

    # Select fields
    for sel in form.find_all("select"):
        options = []
        for opt in sel.find_all("option"):
            options.append({
                "value": opt.get("value", ""),
                "text": opt.get_text(strip=True),
                "selected": opt.has_attr("selected"),
            })

        field = {
            "tag": "select",
            "type": "select",
            "name": sel.get("name", ""),
            "id": sel.get("id", ""),
            "placeholder": "",
            "value": "",
            "required": sel.has_attr("required"),
            "options": options,
        }
        fields.append(field)

    # Textarea fields
    for ta in form.find_all("textarea"):
        field = {
            "tag": "textarea",
            "type": "textarea",
            "name": ta.get("name", ""),
            "id": ta.get("id", ""),
            "placeholder": ta.get("placeholder", ""),
            "value": ta.get_text(strip=True),
            "required": ta.has_attr("required"),
        }
        fields.append(field)

    # Buttons
    for btn in form.find_all("button"):
        field = {
            "tag": "button",
            "type": btn.get("type", "submit"),
            "name": btn.get("name", ""),
            "id": btn.get("id", ""),
            "placeholder": "",
            "value": btn.get_text(strip=True),
            "required": False,
        }
        fields.append(field)

    return fields
