"""
Batch Processor V5 — Process multiple websites
from targets.txt using the WebMiner pipeline.
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from web_miner.core.config import TARGET_FILE
from web_miner.miner import WebMiner

console = Console()


def process_single_site(url: str) -> dict:
    """Process a single website and return results."""

    console.print(f"\n[cyan]🔍 Scanning:[/cyan] {url}")

    miner = WebMiner(url)
    data = miner.run()

    if not data:
        console.print(f"[red]❌ Failed:[/red] {url}")
        return {}

    meta = data.get("metadata", {})
    text = data.get("text", {})
    links = data.get("links", {})
    contacts = data.get("contacts", {})
    tables = data.get("tables", {})

    h_count = sum(len(v) for v in text.get("headings", {}).values())

    console.print(f"[green]✅ Completed:[/green] {miner.site_name}")
    console.print(f"   Headings: {h_count} | Tables: {tables.get('count', 0)} | Links: {links.get('total_count', 0)}")
    console.print(f"   Emails: {len(contacts.get('emails', []))} | Phones: {len(contacts.get('phones', []))}")

    return data


def process_multiple_sites(file_path=None) -> None:
    """Process all websites listed in targets.txt."""

    target = file_path or TARGET_FILE

    with open(target, "r", encoding="utf-8") as f:
        urls = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    if not urls:
        console.print("[bold red]❌ No URLs found in targets.txt[/bold red]")
        return

    console.print(f"\n[bold yellow]📦 Loaded {len(urls)} target websites[/bold yellow]")

    success = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        console.print(f"\n{'='*60}")
        console.print(f"[bold]Website {i}/{len(urls)}[/bold]")

        # Ensure URL has scheme
        if not url.startswith("http"):
            url = "https://" + url

        result = process_single_site(url)
        if result:
            success += 1
        else:
            failed += 1

    console.print(f"\n{'='*60}")
    console.print(f"[bold green]📊 Batch complete: {success} success, {failed} failed[/bold green]")