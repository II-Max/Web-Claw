"""
Navigation Extractor — Extract navigation menus,
breadcrumbs, and CSS/JS resource URLs.
"""

from typing import Any, Dict, List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from core.logger import logger


def extract_navigation(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    """Extract navigation elements and page resources."""
    logger.info("Extracting navigation & resources...")
    data = {
        "nav_menus": _get_nav_menus(soup, base_url),
        "breadcrumbs": _get_breadcrumbs(soup, base_url),
        "stylesheets": _get_stylesheets(soup, base_url),
        "scripts": _get_scripts(soup, base_url),
    }
    logger.info(
        f"Navigation extracted: {len(data['nav_menus'])} menus, "
        f"{len(data['breadcrumbs'])} breadcrumbs, "
        f"{len(data['stylesheets'])} CSS, {len(data['scripts'])} JS"
    )
    return data


def _get_nav_menus(soup, base_url):
    menus = []
    for nav in soup.find_all("nav"):
        menu_items = []
        nav_label = nav.get("aria-label", "") or nav.get("id", "") or (nav.get("class", [""])[0] if nav.get("class") else "")
        for a_tag in nav.find_all("a", href=True):
            href = a_tag.get("href", "").strip()
            if not href or href.startswith("javascript:"):
                continue
            menu_items.append({"text": a_tag.get_text(strip=True), "url": urljoin(base_url, href)})
        if menu_items:
            menus.append({"label": nav_label, "items": menu_items})
    return menus


def _get_breadcrumbs(soup, base_url):
    breadcrumbs = []
    bc_containers = (
        soup.find_all("nav", attrs={"aria-label": lambda x: x and "breadcrumb" in x.lower() if x else False})
        + soup.find_all(class_=lambda x: x and "breadcrumb" in " ".join(x).lower() if x else False)
        + soup.find_all("ol", class_=lambda x: x and "breadcrumb" in " ".join(x).lower() if x else False)
    )
    for container in bc_containers:
        for item in container.find_all(["a", "li", "span"]):
            text = item.get_text(strip=True)
            if not text:
                continue
            href = ""
            if item.name == "a":
                href = urljoin(base_url, item.get("href", ""))
            else:
                a_child = item.find("a")
                if a_child:
                    href = urljoin(base_url, a_child.get("href", ""))
            breadcrumbs.append({"text": text, "url": href})
        if breadcrumbs:
            break
    return breadcrumbs


def _get_stylesheets(soup, base_url):
    stylesheets = []
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if href:
            stylesheets.append({"url": urljoin(base_url, href), "media": link.get("media", "all")})
    return stylesheets


def _get_scripts(soup, base_url):
    scripts = []
    for script in soup.find_all("script", src=True):
        src = script.get("src", "")
        if src:
            scripts.append({
                "url": urljoin(base_url, src),
                "async": script.has_attr("async"),
                "defer": script.has_attr("defer"),
                "type": script.get("type", ""),
            })
    return scripts
