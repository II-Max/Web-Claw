# Web-Claw V6 — Advanced Web Data Scraper

<p align="center">
  <strong>Công cụ cào dữ liệu web chuyên nghiệp cho Windows & Linux</strong><br>
  <em>Trích xuất 18+ loại dữ liệu · Hỗ trợ JavaScript rendering · Anti-detection · Multi-format export</em>
</p>

---

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 🔄 Smart Scraping | Tự động phát hiện website JS-rendered, fallback sang headless browser |
| 🛡️ Anti-Detection | Random User-Agent (16 UA), realistic headers, configurable delay |
| 🔐 Auth & Cookies | Hỗ trợ cookie, HTTP Basic Auth, custom headers, cookie file JSON |
| 🌐 Proxy | HTTP / HTTPS / SOCKS5 proxy |
| 🕷️ Multi-page Crawl | Crawl sâu nhiều cấp, same-domain filter, URL dedup |
| 📦 4 Output Formats | Markdown · JSON · CSV · Excel (.xlsx) |
| 📋 Batch Mode | Cào hàng loạt từ `targets.txt` |
| 🔒 SSL Flexible | Hỗ trợ `--no-verify` cho self-signed certificates |

### 18+ loại dữ liệu được trích xuất

- **Metadata** — Title, Description, Keywords, Author, Canonical URL, Favicon, Charset, Language, Viewport, Generator
- **Open Graph & Twitter Cards** — Toàn bộ thẻ OG và Twitter Card
- **Structured Data** — JSON-LD (Schema.org)
- **Text** — Headings (H1-H6), Paragraphs, Lists (UL/OL/DL), Blockquotes, Code Blocks
- **Links** — Internal, External, Social Media, Download Files, Anchors
- **Media** — Images (src, alt, srcset, dimensions), Videos (HTML5 + YouTube/Vimeo/Dailymotion), Audio
- **Contacts** — Emails (mailto + regex), Phone (tel + regex), Social Profiles, Addresses
- **Tables** — Trích xuất, validate, scoring và ranking
- **Forms** — Action, Method, tất cả fields (input/select/textarea/button)
- **Navigation** — Nav menus, Breadcrumbs, Stylesheets, Scripts

---

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.10 trở lên
- Git (tùy chọn, để clone)

### Bước 1 — Clone & thiết lập môi trường

```bash
git clone https://github.com/yourusername/Web-Claw.git
cd Web-Claw
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

### Bước 2 — Cài dependencies

```bash
pip install -r requirements.txt
```

### Bước 3 — Cài headless browser (tùy chọn, cho website JS-rendered)

```bash
playwright install chromium
```

> **Lưu ý:** Bước này chỉ cần thiết nếu bạn muốn cào website render bằng JavaScript (SPA). Nếu chỉ cào website tĩnh, bước này không bắt buộc — tool sẽ tự động dùng `requests`.

---

## 🛠 Hướng dẫn sử dụng

### Chế độ 1 — Cào 1 trang (tương tác)
```bash
python main.py
```
Tool sẽ hiện prompt hỏi URL. Nhập URL và nhấn Enter.

### Chế độ 2 — Cào 1 trang (trực tiếp)
```bash
python main.py --url https://example.com
```

### Chế độ 3 — Headless mode (non-interactive)
```bash
python main.py --url https://example.com --no-prompt
```
Hữu ích khi tích hợp vào script/pipeline khác.

### Chế độ 4 — Force JavaScript rendering
```bash
python main.py --url https://example.com --js
```
Bắt buộc dùng Playwright headless browser. Phù hợp cho các website React, Vue, Angular, Next.js...

### Chế độ 5 — Crawl nhiều trang
```bash
python main.py --url https://example.com --depth 3 --max-pages 20
```
Crawl từ URL gốc, follow link đến depth=3, tối đa 20 trang.

### Chế độ 6 — Batch mode (hàng loạt)
```bash
python main.py --batch
```
Cào tất cả URL trong file `targets.txt` (mỗi URL một dòng, dùng `#` để comment).

### Proxy, Cookie & Authentication

```bash
# Proxy
python main.py --url https://example.com --proxy http://127.0.0.1:8080
python main.py --url https://example.com --proxy socks5://127.0.0.1:1080

# Cookie
python main.py --url https://example.com --cookie "session=abc123" --cookie "token=xyz"
python main.py --url https://example.com --cookie-file cookies.json

# HTTP Basic Auth
python main.py --url https://example.com --auth admin:password

# Custom headers
python main.py --url https://example.com --header "Authorization: Bearer token123"
```

### SSL & Output

```bash
# Bỏ qua SSL verification (self-signed cert)
python main.py --url https://internal.local --no-verify

# Chọn format xuất
python main.py --url https://example.com --format md           # Chỉ Markdown
python main.py --url https://example.com --format json,csv     # JSON + CSV
python main.py --url https://example.com --format all          # Tất cả (mặc định)
```

---

## 📋 Tham chiếu CLI

| Option | Mô tả | Mặc định |
|--------|--------|----------|
| `--url URL` | URL website cần cào | _(prompt khi chạy)_ |
| `--batch` | Batch mode từ `targets.txt` | — |
| `--no-prompt` | Không hỏi tương tác (cần `--url`) | — |
| `--js` | Bắt buộc headless browser | — |
| `--depth N` | Crawl sâu N cấp | `1` |
| `--max-pages N` | Tối đa trang crawl | `50` |
| `--same-domain` | Chỉ follow link cùng domain | `True` |
| `--no-verify` | Bỏ qua SSL certificate | — |
| `--timeout N` | Timeout mỗi request (giây) | `30` |
| `--delay N` | Delay cố định giữa requests (giây) | _random 0.5–2s_ |
| `--retries N` | Số lần retry khi thất bại | `3` |
| `--proxy URL` | Proxy server (`http://`, `socks5://`) | — |
| `--cookie K=V` | Cookie (sử dụng nhiều lần) | — |
| `--cookie-file PATH` | Load cookie từ file JSON | — |
| `--header K:V` | Custom header (sử dụng nhiều lần) | — |
| `--auth user:pass` | HTTP Basic Authentication | — |
| `--format FMT` | `md`, `json`, `csv`, `xlsx`, `all` | `all` |
| `--quiet` | Ẩn bảng kết quả chi tiết | — |

---

## 📂 Cấu trúc Output

Dữ liệu xuất ra được tổ chức trong `outputs/`, phân theo format và tên miền:

```
outputs/
├── markdown/<domain>/
│   ├── full_content.md          # Tổng hợp: stats, nội dung chính, headings
│   ├── metadata.md              # Title, OG, Twitter Cards, JSON-LD
│   ├── tables.md                # Bảng HTML → Markdown table
│   ├── links.md                 # Internal, External, Social, Downloads
│   ├── media.md                 # Images, Videos, Audio
│   ├── contacts.md              # Emails, Phones, Social profiles, Addresses
│   └── forms_and_code.md        # Forms, Code blocks, CSS/JS, Navigation
│
├── json/<domain>/
│   ├── full_data.json           # TẤT CẢ dữ liệu trong 1 file
│   ├── metadata.json            # Metadata riêng
│   ├── links.json               # Links riêng
│   ├── media.json               # Media riêng
│   ├── contacts.json            # Contacts riêng
│   ├── text_content.json        # Text content riêng
│   ├── tables.json              # Tables riêng
│   └── forms_and_code.json      # Forms + Navigation riêng
│
├── csv/<domain>/
│   ├── links.csv                # Tất cả links
│   ├── social_links.csv         # Social media links
│   ├── emails.csv               # Emails
│   ├── phones.csv               # Phone numbers
│   ├── images.csv               # Images
│   ├── headings.csv             # Headings (H1-H6)
│   ├── paragraphs.csv           # Paragraphs
│   └── table_N.csv              # Từng bảng HTML
│
└── excel/<domain>/
    └── data.xlsx                # Multi-sheet workbook (tất cả dữ liệu)
```

---

## 🏗 Kiến trúc dự án

```
Web-Claw/
├── main.py                      # CLI entry point
├── miner.py                     # WebMiner orchestrator
├── core/
│   ├── config.py                # Cấu hình tập trung
│   ├── scraper.py               # Smart fetcher (requests + Playwright)
│   ├── cleaner.py               # HTML cleaning & content extraction
│   ├── crawler.py               # Multi-page BFS crawler
│   ├── logger.py                # Logging (file + Rich console)
│   ├── user_agents.py           # User-Agent pool & header generator
│   ├── batch_processor.py       # Batch processing từ targets.txt
│   ├── extractors/              # 8 data extractors
│   │   ├── metadata_extractor.py
│   │   ├── text_extractor.py
│   │   ├── link_extractor.py
│   │   ├── media_extractor.py
│   │   ├── contact_extractor.py
│   │   ├── table_extractor.py
│   │   ├── form_extractor.py
│   │   └── nav_extractor.py
│   └── exporters/               # 4 data exporters
│       ├── markdown_exporter.py
│       ├── json_exporter.py
│       ├── csv_exporter.py
│       └── excel_exporter.py
├── tests/
│   └── test_cleaner.py          # Unit tests
├── targets.txt                  # Danh sách URL cho batch mode
├── requirements.txt             # Python dependencies
└── logs/
    └── datamine.log             # Log file
```

---

## ⚙️ Cách hoạt động (Pipeline)

```
URL Input
    │
    ▼
┌─────────────────┐
│   Smart Fetch    │  requests → (auto-detect JS?) → Playwright fallback
│   + Anti-detect  │  random UA, headers, delay, proxy, cookies
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   8 Extractors   │  metadata, text, links, media, contacts, tables, forms, nav
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   4 Exporters    │  Markdown, JSON, CSV, Excel
└─────────────────┘
```

---

## 📌 Khắc phục sự cố

| Vấn đề | Giải pháp |
|--------|-----------|
| Lỗi encoding Unicode trên Windows | Đặt `$env:PYTHONUTF8="1"` trước khi chạy |
| Website chặn bot (Cloudflare, CAPTCHA) | Dùng `--js` để render qua headless browser |
| SSL Error / Self-signed certificate | Dùng `--no-verify` |
| Website yêu cầu đăng nhập | Dùng `--cookie`, `--cookie-file` hoặc `--auth` |
| Playwright chưa cài browser | Chạy `playwright install chromium` |
| Rate limiting / bị block IP | Dùng `--proxy` và `--delay` |
| Không thấy dữ liệu (website JS) | Thêm flag `--js` để render JavaScript |

---

## 📄 License

MIT License — Sử dụng tự do cho mục đích cá nhân và thương mại.

---

<p align="center">
  <strong>Web-Claw V6</strong> · Chúc bạn khai thác dữ liệu hiệu quả! 🕷️
</p>