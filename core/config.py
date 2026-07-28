from pathlib import Path

# ===== ROOT DIRECTORY =====

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== OUTPUT DIRECTORIES =====

OUTPUT_DIR = BASE_DIR / "outputs"
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
JSON_DIR = OUTPUT_DIR / "json"

# ===== LOG DIRECTORY =====

LOG_DIR = BASE_DIR / "logs"

# ===== TARGET FILE =====

TARGET_FILE = BASE_DIR / "targets.txt"

# ===== AUTO CREATE FOLDERS =====

OUTPUT_DIR.mkdir(exist_ok=True)
MARKDOWN_DIR.mkdir(exist_ok=True)
JSON_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

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
    r'(?:\d{2,4}[\s.-]?){2}'
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
}

# ===== DOWNLOADABLE FILE EXTENSIONS =====

DOWNLOAD_EXTENSIONS = {
    "documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".odt", ".ods", ".odp", ".rtf", ".txt"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".bmp", ".tiff"],
    "media": [".mp3", ".mp4", ".avi", ".mkv", ".mov", ".wav", ".flac", ".ogg", ".webm"],
    "data": [".csv", ".json", ".xml", ".sql", ".db", ".sqlite"],
    "executables": [".exe", ".msi", ".dmg", ".apk", ".deb", ".rpm"],
}

ALL_DOWNLOAD_EXTENSIONS = []
for exts in DOWNLOAD_EXTENSIONS.values():
    ALL_DOWNLOAD_EXTENSIONS.extend(exts)

# ===== HTTP CONFIG =====

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)