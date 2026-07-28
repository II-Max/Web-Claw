"""
DataMine V5 — Main entry point.
Usage:
    python -m web_miner.main --url https://example.com
    python -m web_miner.main --batch
"""

import sys
import argparse
from typing import Optional, List
from pathlib import Path

# Thêm thư mục cha vào sys.path để hỗ trợ import tuyệt đối 'web_miner'
current_file = Path(__file__).resolve()
project_root = current_file.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.batch_processor import process_multiple_sites
from miner import WebMiner

console = Console()


def main(args_list: Optional[List[str]] = None) -> None:

    parser = argparse.ArgumentParser(
        description="DataMine V5 — Web Data Miner (Full Extraction)"
    )
    parser.add_argument(
        '--url', type=str,
        help="URL website to mine"
    )
    parser.add_argument(
        '--batch', action='store_true',
        help="Run in batch mode using targets.txt"
    )
    parser.add_argument(
        '--no_prompt', action='store_true',
        help="Run without interactive prompts (requires --url)"
    )

    args = parser.parse_args(args_list)

    # Print banner
    console.print(Panel.fit(
        "[bold cyan]DataMine V5[/bold cyan]\n"
        "[dim]Web Data Mining Framework — Full Extraction[/dim]\n"
        "[green]Output: markdown/ + json/[/green]",
        border_style="cyan",
    ))

    # ===== BATCH MODE =====

    if args.batch:
        console.print("\n[bold yellow]📦 Batch Mode — Processing targets.txt[/bold yellow]")
        try:
            process_multiple_sites()
            console.print("\n[bold green]✅ All websites processed successfully[/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ ERROR:[/bold red] {e}")
        return

    # ===== SINGLE URL MODE =====

    if args.no_prompt:
        if not args.url:
            console.print("[bold red]❌ LỖI: Khi dùng --no_prompt phải cung cấp --url[/bold red]")
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

    miner = WebMiner(url)

    # Fetch
    console.print("\n[yellow]⏳ Đang tải trang web...[/yellow]")
    if not miner.fetch():
        console.print("[bold red]❌ Không thể kết nối tới website[/bold red]")
        return

    console.print("[green]✅ Tải trang thành công[/green]")

    # Mine all data
    console.print("\n[yellow]⛏️  Đang cào dữ liệu...[/yellow]")
    data = miner.mine_all()

    if not data:
        console.print("[bold red]❌ Không thể trích xuất dữ liệu[/bold red]")
        return

    # Export
    console.print("\n[yellow]💾 Đang xuất dữ liệu...[/yellow]")
    paths = miner.export_all()

    # Print summary
    _print_summary(data, paths)


def _print_summary(data: dict, paths: dict) -> None:
    """Print a beautiful summary table of extracted data."""

    console.print("\n")

    # Results table
    table = Table(
        title="📊 Kết quả cào dữ liệu",
        border_style="cyan",
        show_lines=True,
    )
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

    table.add_row("Title", meta.get("title", "N/A")[:60])
    table.add_row("Headings (H1-H6)", str(h_count))
    table.add_row("Paragraphs", str(len(text.get("paragraphs", []))))
    table.add_row("Lists", str(len(text.get("lists", []))))
    table.add_row("Tables", str(tables.get("count", 0)))
    table.add_row("Links (tổng)", str(links.get("total_count", 0)))
    table.add_row("  ↳ Internal", str(len(links.get("internal", []))))
    table.add_row("  ↳ External", str(len(links.get("external", []))))
    table.add_row("  ↳ Social", str(len(links.get("social_media", []))))
    table.add_row("  ↳ Downloads", str(len(links.get("downloads", []))))
    table.add_row("Images", str(len(media.get("images", []))))
    table.add_row("Videos", str(len(media.get("videos", []))))
    table.add_row("Audio", str(len(media.get("audio", []))))
    table.add_row("Emails", str(len(contacts.get("emails", []))))
    table.add_row("Phone Numbers", str(len(contacts.get("phones", []))))
    table.add_row("Social Profiles", str(len(contacts.get("social_profiles", []))))
    table.add_row("Forms", str(forms.get("count", 0)))
    table.add_row("Code Blocks", str(len(text.get("code_blocks", []))))
    table.add_row("Nav Menus", str(len(nav.get("nav_menus", []))))
    table.add_row("Stylesheets", str(len(nav.get("stylesheets", []))))
    table.add_row("Scripts", str(len(nav.get("scripts", []))))

    console.print(table)

    # Output paths
    console.print(f"\n[bold green]📂 Output:[/bold green]")
    console.print(f"  📝 Markdown: [cyan]{paths.get('markdown', 'N/A')}[/cyan]")
    console.print(f"  📊 JSON:     [cyan]{paths.get('json', 'N/A')}[/cyan]")
    console.print()


if __name__ == "__main__":
    main()
