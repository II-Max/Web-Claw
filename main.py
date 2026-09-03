"""
Web-Claw V6 — Main entry point.
Advanced web scraping tool for Windows & Linux.

Usage:
    python main.py                                    # Interactive mode
    python main.py --url https://example.com          # Single URL
    python main.py --url https://example.com --js     # Force headless browser (JS)
    python main.py --batch                            # Batch mode from targets.txt
    python main.py --url https://example.com --depth 3  # Crawl 3 levels deep
"""

import sys
import argparse
from typing import Optional, List
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.scraper import ScrapeOptions
from core.batch_processor import process_multiple_sites
from core.crawler import crawl_urls
from miner import WebMiner

console = Console()

VERSION = "6.0"


def main(args_list: Optional[List[str]] = None) -> None:

    parser = argparse.ArgumentParser(
        description="Web-Claw V6 — Advanced Web Data Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python main.py --url https://example.com
  python main.py --url https://example.com --js --format all
  python main.py --url https://example.com --depth 3 --max-pages 20
  python main.py --batch --proxy http://127.0.0.1:8080
  python main.py --url https://example.com --cookie "session=abc123"
  python main.py --url https://example.com --no-verify
"""
    )

    # === Target ===
    target_group = parser.add_argument_group("Target")
    target_group.add_argument('--url', type=str, help="URL of the website to scrape")
    target_group.add_argument('--batch', action='store_true', help="Batch mode: scrape all URLs in targets.txt")
    target_group.add_argument('--no-prompt', action='store_true', help="Non-interactive mode (requires --url)")

    # === Crawling ===
    crawl_group = parser.add_argument_group("Crawling")
    crawl_group.add_argument('--depth', type=int, default=1, help="Crawl depth (1 = single page, 2+ = follow links). Default: 1")
    crawl_group.add_argument('--max-pages', type=int, default=50, help="Maximum pages to crawl. Default: 50")
    crawl_group.add_argument('--same-domain', action='store_true', default=True, help="Only follow links on the same domain (default: True)")

    # === Scraping ===
    scrape_group = parser.add_argument_group("Scraping")
    scrape_group.add_argument('--js', action='store_true', help="Force headless browser for JavaScript-rendered pages")
    scrape_group.add_argument('--no-verify', action='store_true', help="Skip SSL certificate verification")
    scrape_group.add_argument('--timeout', type=int, default=30, help="Request timeout in seconds. Default: 30")
    scrape_group.add_argument('--delay', type=float, default=None, help="Fixed delay between requests (seconds). Overrides random delay.")
    scrape_group.add_argument('--retries', type=int, default=3, help="Max retry attempts. Default: 3")

    # === Authentication ===
    auth_group = parser.add_argument_group("Authentication")
    auth_group.add_argument('--proxy', type=str, default="", help="Proxy URL (http://host:port or socks5://host:port)")
    auth_group.add_argument('--cookie', type=str, action='append', default=[], help="Cookie in 'name=value' format. Can be used multiple times.")
    auth_group.add_argument('--cookie-file', type=str, default="", help="Path to cookies JSON file")
    auth_group.add_argument('--header', type=str, action='append', default=[], help="Custom header 'Name: Value'. Can be used multiple times.")
    auth_group.add_argument('--auth', type=str, default="", help="HTTP Basic Auth as 'user:password'")

    # === Output ===
    output_group = parser.add_argument_group("Output")
    output_group.add_argument('--format', type=str, default="all", help="Output format: md, json, csv, xlsx, all. Default: all")
    output_group.add_argument('--quiet', action='store_true', help="Suppress detailed console output")

    args = parser.parse_args(args_list)

    # Print banner
    console.print(Panel.fit(
        f"[bold cyan]Web-Claw V{VERSION}[/bold cyan]\n"
        "[dim]Advanced Web Data Scraper — Win/Linux[/dim]\n"
        "[green]Formats: Markdown · JSON · CSV · Excel[/green]",
        border_style="cyan",
    ))

    # Build ScrapeOptions
    options = _build_options(args)
    formats = _parse_formats(args.format)

    # ===== BATCH MODE =====
    if args.batch:
        console.print("\n[bold yellow]📦 Batch Mode — Processing targets.txt[/bold yellow]")
        try:
            process_multiple_sites(options=options, formats=formats)
            console.print("\n[bold green]✅ All websites processed successfully[/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ ERROR:[/bold red] {e}")
        return

    # ===== SINGLE URL MODE =====
    if args.no_prompt:
        if not args.url:
            console.print("[bold red]❌ LỖI: Khi dùng --no-prompt phải cung cấp --url[/bold red]")
            return
        url = args.url
    else:
        url = args.url
        if not url:
            url = console.input("\n[bold]🌐 Nhập URL website cần cào: [/bold]").strip()

    if not url:
        console.print("[bold red]❌ LỖI: Vui lòng cung cấp URL.[/bold red]")
        return

    # Ensure URL has scheme
    if not url.startswith("http"):
        url = "https://" + url

    console.print(f"\n[cyan]🔍 Target:[/cyan] {url}")

    # ===== CRAWL MODE (depth > 1) =====
    if args.depth > 1:
        console.print(f"\n[yellow]🕷️  Crawling (depth={args.depth}, max={args.max_pages})...[/yellow]")
        urls = crawl_urls(
            url, depth=args.depth, max_pages=args.max_pages,
            same_domain=args.same_domain, options=options,
        )
        console.print(f"[green]✅ Discovered {len(urls)} pages[/green]")

        success = 0
        for i, page_url in enumerate(urls, 1):
            console.print(f"\n{'='*60}")
            console.print(f"[bold]Page {i}/{len(urls)}:[/bold] {page_url}")
            miner = WebMiner(page_url, options=options, formats=formats)
            if _scrape_single(miner, args):
                success += 1
        console.print(f"\n[bold green]📊 Crawl complete: {success}/{len(urls)} pages scraped[/bold green]")
        return

    # ===== SINGLE PAGE MODE =====
    miner = WebMiner(url, options=options, formats=formats)
    _scrape_single(miner, args)


def _scrape_single(miner: WebMiner, args) -> bool:
    """Scrape a single page. Returns True on success."""
    console.print("\n[yellow]⏳ Đang tải trang web...[/yellow]")
    if not miner.fetch():
        console.print("[bold red]❌ Không thể kết nối tới website[/bold red]")
        return False

    console.print("[green]✅ Tải trang thành công[/green]")

    console.print("\n[yellow]⛏️  Đang cào dữ liệu...[/yellow]")
    data = miner.mine_all()

    if not data:
        console.print("[bold red]❌ Không thể trích xuất dữ liệu[/bold red]")
        return False

    console.print("\n[yellow]💾 Đang xuất dữ liệu...[/yellow]")
    paths = miner.export_all()

    if not args.quiet:
        _print_summary(data, paths)

    return True


def _build_options(args) -> ScrapeOptions:
    """Build ScrapeOptions from CLI arguments."""
    cookies = {}
    for c in args.cookie:
        if "=" in c:
            key, val = c.split("=", 1)
            cookies[key.strip()] = val.strip()

    headers = {}
    for h in args.header:
        if ":" in h:
            key, val = h.split(":", 1)
            headers[key.strip()] = val.strip()

    delay_min = 0.5
    delay_max = 2.0
    if args.delay is not None:
        delay_min = args.delay
        delay_max = args.delay

    return ScrapeOptions(
        use_js=args.js,
        verify_ssl=not args.no_verify,
        proxy=args.proxy,
        cookies=cookies,
        cookie_file=args.cookie_file,
        headers=headers,
        auth=args.auth,
        delay_min=delay_min,
        delay_max=delay_max,
        timeout=args.timeout,
        max_retries=args.retries,
    )


def _parse_formats(format_str: str) -> set:
    """Parse format string into a set of formats."""
    if format_str.lower() == "all":
        return {"all"}
    return {f.strip().lower() for f in format_str.split(",")}


def _print_summary(data: dict, paths: dict) -> None:
    """Print a summary table of extracted data."""

    console.print("\n")

    table = Table(title="📊 Kết quả cào dữ liệu", border_style="cyan", show_lines=True)
    table.add_column("Loại dữ liệu", style="bold")
    table.add_column("Số lượng", justify="center", style="green")

    meta = data.get("metadata", {})
    text = data.get("text", {})
    links = data.get("links", {})
    media = data.get("media", {})
    contacts = data.get("contacts", {})
    tables = data.get("tables", {})
    forms = data.get("forms", {})
    nav = data.get("navigation", {})

    h_count = sum(len(v) for v in text.get("headings", {}).values())

    rows = [
        ("Title", meta.get("title", "N/A")[:60]),
        ("Headings (H1-H6)", str(h_count)),
        ("Paragraphs", str(len(text.get("paragraphs", [])))),
        ("Lists", str(len(text.get("lists", [])))),
        ("Tables", str(tables.get("count", 0))),
        ("Links (tổng)", str(links.get("total_count", 0))),
        ("  ↳ Internal", str(len(links.get("internal", [])))),
        ("  ↳ External", str(len(links.get("external", [])))),
        ("  ↳ Social", str(len(links.get("social_media", [])))),
        ("  ↳ Downloads", str(len(links.get("downloads", [])))),
        ("Images", str(len(media.get("images", [])))),
        ("Videos", str(len(media.get("videos", [])))),
        ("Audio", str(len(media.get("audio", [])))),
        ("Emails", str(len(contacts.get("emails", [])))),
        ("Phone Numbers", str(len(contacts.get("phones", [])))),
        ("Social Profiles", str(len(contacts.get("social_profiles", [])))),
        ("Forms", str(forms.get("count", 0))),
        ("Code Blocks", str(len(text.get("code_blocks", [])))),
    ]

    for name, value in rows:
        table.add_row(name, value)

    console.print(table)

    console.print(f"\n[bold green]📂 Output:[/bold green]")
    for key, path in paths.items():
        emoji = {"markdown": "📝", "json": "📊", "csv": "📋", "excel": "📈"}.get(key, "📁")
        console.print(f"  {emoji} {key.title()}: [cyan]{path}[/cyan]")
    console.print()


if __name__ == "__main__":
    main()
