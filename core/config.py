"""
Config V6 — Central configuration for Web-Claw.
All paths, regex patterns, and default settings.
"""

from pathlib import Path

# ===== ROOT DIRECTORY =====

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== OUTPUT DIRECTORIES =====

OUTPUT_DIR = BASE_DIR / "outputs"
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
JSON_DIR = OUTPUT_DIR / "json"
CSV_DIR = OUTPUT_DIR / "csv"
EXCEL_DIR = OUTPUT_DIR / "excel"

# ===== LOG DIRECTORY =====

LOG_DIR = BASE_DIR / "logs"

# ===== TARGET FILE =====

TARGET_FILE = BASE_DIR / "targets.txt"

# ===== AUTO CREATE FOLDERS =====

for _dir in [OUTPUT_DIR, MARKDOWN_DIR, JSON_DIR, CSV_DIR, EXCEL_DIR, LOG_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ===== AUTO CREATE TARGET FILE =====

if not TARGET_FILE.exists():
    TARGET_FILE.write_text(
        "https://example.com\n",
        encoding="utf-8"
    )

# ===== REGEX PATTERNS =====

EMAIL_REGEX = (
    r'\b[A-Za-z0-9._%+-]+'
    r'@[A-Za-z0-9.-]+'
    r'\.[A-Za-z]{2,}\b'
)

PHONE_REGEX = (
    r'(?:\+?\d{1,4}[\s.-]?)?'
    r'(?:\(?\d{1,5}\)?[\s.-]?)?'
    r'\d{2,4}[\s.-]?'
    r'\d{2,4}[\s.-]?'
    r'\d{2,4}'
)

# ===== SOCIAL MEDIA DOMAINS =====

SOCIAL_DOMAINS = {
    "facebook": ["facebook.com", "fb.com", "fb.me"],
    "twitter": ["twitter.com", "x.com", "t.co"],
    "youtube": ["youtube.com", "youtu.be"],
    "linkedin": ["linkedin.com"],
    "instagram": ["instagram.com"],
    "tiktok": ["tiktok.com"],
    "github": ["github.com"],
    "pinterest": ["pinterest.com"],
    "reddit": ["reddit.com"],
    "telegram": ["t.me", "telegram.me"],
    "zalo": ["zalo.me"],
    "threads": ["threads.net"],
    "discord": ["discord.gg", "discord.com"],
    "whatsapp": ["wa.me", "whatsapp.com"],
}

# ===== DOWNLOADABLE FILE EXTENSIONS =====

DOWNLOAD_EXTENSIONS = {
    "documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".odt", ".ods", ".odp", ".rtf", ".txt"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".bmp", ".tiff", ".avif"],
    "media": [".mp3", ".mp4", ".avi", ".mkv", ".mov", ".wav", ".flac", ".ogg", ".webm", ".m4a"],
    "data": [".csv", ".json", ".xml", ".sql", ".db", ".sqlite", ".parquet"],
    "executables": [".exe", ".msi", ".dmg", ".apk", ".deb", ".rpm", ".appimage"],
}

ALL_DOWNLOAD_EXTENSIONS = []
for exts in DOWNLOAD_EXTENSIONS.values():
    ALL_DOWNLOAD_EXTENSIONS.extend(exts)

# ===== HTTP CONFIG =====

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds base for exponential backoff

# ===== CRAWLER DEFAULTS =====

DEFAULT_CRAWL_DEPTH = 1        # Only scrape the given URL
MAX_CRAWL_DEPTH = 10           # Safety limit
DEFAULT_MAX_PAGES = 50         # Max pages per crawl
MAX_PAGES_LIMIT = 500          # Hard safety limit
DEFAULT_DELAY_MIN = 0.5        # seconds
DEFAULT_DELAY_MAX = 2.0        # seconds

# ===== EXPORT FORMATS =====

VALID_FORMATS = {"md", "json", "csv", "xlsx", "all"}
DEFAULT_FORMAT = "all"