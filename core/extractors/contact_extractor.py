"""
Contact Extractor — Extract emails, phone numbers,
and social media profile links.
"""

import re
from typing import Any, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from core.config import EMAIL_REGEX, PHONE_REGEX, SOCIAL_DOMAINS
from core.cleaner import extract_clean_text
from core.logger import logger


def extract_contacts(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Extract all contact information from the page."""
    logger.info("Extracting contacts...")
    data = {
        "emails": _get_emails(soup, html),
        "phones": _get_phones(soup, html),
        "social_profiles": _get_social_profiles(soup),
        "addresses": _get_addresses(soup),
    }
    logger.info(
        f"Contacts extracted: {len(data['emails'])} emails, "
        f"{len(data['phones'])} phones, "
        f"{len(data['social_profiles'])} social profiles"
    )
    return data


def _get_emails(soup, html):
    emails_set = set()
    email_list = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "")
        if href.startswith("mailto:"):
            email = href.replace("mailto:", "").split("?")[0].strip()
            if email and email not in emails_set:
                emails_set.add(email)
                email_list.append({"email": email, "source": "mailto_link", "context": a_tag.get_text(strip=True)})
    clean_text = extract_clean_text(html)
    for email in re.findall(EMAIL_REGEX, clean_text):
        email = email.strip().lower()
        if email not in emails_set and not _is_fake_email(email):
            emails_set.add(email)
            email_list.append({"email": email, "source": "text_regex", "context": ""})
    return email_list


def _is_fake_email(email):
    fake = ["example.com", "example.org", "test.com", "domain.com", "email.com", "your", "name@", "user@", "info@example"]
    return any(p in email.lower() for p in fake)


def _get_phones(soup, html):
    phones_set = set()
    phone_list = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "")
        if href.startswith("tel:"):
            phone = href.replace("tel:", "").strip()
            normalized = re.sub(r'[^\d+]', '', phone)
            if normalized and normalized not in phones_set:
                phones_set.add(normalized)
                phone_list.append({"phone": phone, "normalized": normalized, "source": "tel_link", "context": a_tag.get_text(strip=True)})
    clean_text = extract_clean_text(html)
    for phone in re.findall(PHONE_REGEX, clean_text):
        phone = phone.strip()
        normalized = re.sub(r'[^\d+]', '', phone)
        digits = re.sub(r'[^\d]', '', normalized)
        if len(digits) < 8:
            continue
        if normalized not in phones_set:
            phones_set.add(normalized)
            phone_list.append({"phone": phone, "normalized": normalized, "source": "text_regex", "context": ""})
    return phone_list


def _get_social_profiles(soup):
    profiles = []
    seen_urls = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()
        if not href:
            continue
        parsed = urlparse(href)
        domain = parsed.netloc.replace("www.", "").lower()
        for platform, domains in SOCIAL_DOMAINS.items():
            if any(d in domain for d in domains):
                if href not in seen_urls:
                    seen_urls.add(href)
                    profiles.append({"platform": platform, "url": href, "text": a_tag.get_text(strip=True)})
                break
    return profiles


def _get_addresses(soup):
    return [addr.get_text(strip=True) for addr in soup.find_all("address") if addr.get_text(strip=True)]
