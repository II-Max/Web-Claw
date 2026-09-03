"""
Markdown Exporter — Export all extracted data as beautifully formatted Markdown files.
"""

import json
import datetime
from pathlib import Path
from typing import Any, Dict

from core.config import MARKDOWN_DIR
from core.logger import logger


def export_markdown(data: Dict[str, Any], site_name: str) -> Path:
    """Export all extracted data to Markdown files. Returns the output directory path."""
    out_dir = MARKDOWN_DIR / site_name
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Exporting Markdown to: {out_dir}")

    _write_full_content(data, out_dir)
    _write_metadata(data, out_dir)
    _write_tables(data, out_dir)
    _write_links(data, out_dir)
    _write_media(data, out_dir)
    _write_contacts(data, out_dir)
    _write_forms_and_code(data, out_dir)

    logger.info(f"Markdown export complete: {out_dir}")
    return out_dir


def _write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write_full_content(data, out_dir):
    md = []
    meta = data.get("metadata", {})
    text = data.get("text", {})
    links = data.get("links", {})
    media = data.get("media", {})
    contacts = data.get("contacts", {})
    tables = data.get("tables", {})
    forms = data.get("forms", {})
    nav = data.get("navigation", {})

    md.append(f"# {meta.get('title', 'Untitled Page')}\n")
    md.append(f"> 🔗 URL: {meta.get('url', 'N/A')}")
    md.append(f"> 📅 Scraped: {_timestamp()}\n")

    md.append("## 📊 Tóm tắt dữ liệu\n")
    md.append("| Loại dữ liệu | Số lượng |")
    md.append("|---|---|")

    h_count = sum(len(v) for v in text.get("headings", {}).values())
    stats = [
        ("Headings", h_count), ("Paragraphs", len(text.get("paragraphs", []))),
        ("Lists", len(text.get("lists", []))), ("Tables", tables.get("count", 0)),
        ("Links (tổng)", links.get("total_count", 0)), ("Images", len(media.get("images", []))),
        ("Videos", len(media.get("videos", []))), ("Emails", len(contacts.get("emails", []))),
        ("Phones", len(contacts.get("phones", []))), ("Social Profiles", len(contacts.get("social_profiles", []))),
        ("Forms", forms.get("count", 0)), ("Code Blocks", len(text.get("code_blocks", []))),
        ("Stylesheets", len(nav.get("stylesheets", []))), ("Scripts", len(nav.get("scripts", []))),
    ]
    for name, count in stats:
        md.append(f"| {name} | {count} |")
    md.append("")

    main_content = text.get("main_content", "")
    if main_content:
        md.append("## 📝 Nội dung chính\n")
        md.append(main_content[:5000])
        if len(main_content) > 5000:
            md.append(f"\n\n*... (đã cắt, tổng {len(main_content)} ký tự)*")
        md.append("")

    headings = text.get("headings", {})
    if headings:
        md.append("## 📑 Cấu trúc Headings\n")
        for level, items in sorted(headings.items()):
            for item in items:
                indent = "  " * (int(level[1]) - 1)
                md.append(f"{indent}- **{level.upper()}**: {item}")
        md.append("")

    _write_file(out_dir / "full_content.md", "\n".join(md))


def _write_metadata(data, out_dir):
    meta = data.get("metadata", {})
    md = ["# 🏷️ Metadata\n", "| Thuộc tính | Giá trị |", "|---|---|"]
    for key in ["title", "description", "keywords", "author", "canonical", "language", "charset", "favicon", "robots", "viewport", "generator"]:
        md.append(f"| {key.title()} | {meta.get(key, '')} |")
    md.append("")

    og = meta.get("og", {})
    if og:
        md.append("## Open Graph Tags\n")
        md.append("| Property | Content |")
        md.append("|---|---|")
        for prop, content in og.items():
            md.append(f"| {prop} | {content} |")
        md.append("")

    tc = meta.get("twitter", {})
    if tc:
        md.append("## Twitter Cards\n")
        md.append("| Name | Content |")
        md.append("|---|---|")
        for name, content in tc.items():
            md.append(f"| {name} | {content} |")
        md.append("")

    json_ld = meta.get("json_ld", [])
    if json_ld:
        md.append("## Structured Data (JSON-LD)\n")
        for i, schema in enumerate(json_ld, 1):
            md.append(f"### Schema {i}\n")
            md.append("```json")
            md.append(json.dumps(schema, indent=2, ensure_ascii=False))
            md.append("```\n")

    _write_file(out_dir / "metadata.md", "\n".join(md))


def _write_tables(data, out_dir):
    tables_data = data.get("tables", {})
    tables = tables_data.get("tables", [])
    md = [f"# 📊 Tables ({tables_data.get('count', 0)} valid / {tables_data.get('total_found', 0)} found)\n"]

    if not tables:
        md.append("*Không tìm thấy bảng nào trên trang này.*")
    else:
        for table in tables:
            md.append(f"## Table {table['index']} (Score: {table['score']}, {table['rows']} rows × {table['columns']} cols)\n")
            cols = table["column_names"]
            md.append("| " + " | ".join(cols) + " |")
            md.append("| " + " | ".join(["---"] * len(cols)) + " |")
            for row in table["data"]:
                values = [str(row.get(c, "")).replace("|", "\\|").replace("\n", " ")[:100] for c in cols]
                md.append("| " + " | ".join(values) + " |")
            md.append("")
    _write_file(out_dir / "tables.md", "\n".join(md))


def _write_links(data, out_dir):
    links = data.get("links", {})
    md = [f"# 🔗 Links (Tổng: {links.get('total_count', 0)})\n"]

    for section, key, emoji in [("Internal Links", "internal", ""), ("External Links", "external", ""), ("Social Media Links", "social_media", ""), ("Download Links", "downloads", "📥 ")]:
        items = links.get(key, [])
        if items:
            md.append(f"## {section} ({len(items)})\n")
            for link in items:
                text = link.get("text", "") or link.get("url", "")
                if key == "social_media":
                    md.append(f"- **{link.get('platform', '').title()}**: [{text}]({link['url']})")
                elif key == "downloads":
                    md.append(f"- {emoji}[{link.get('filename', '')}]({link['url']}) ({link.get('file_type', '')})")
                else:
                    md.append(f"- [{text}]({link['url']})")
            md.append("")
    _write_file(out_dir / "links.md", "\n".join(md))


def _write_media(data, out_dir):
    media = data.get("media", {})
    md = ["# 🖼️ Media\n"]

    images = media.get("images", [])
    if images:
        md.append(f"## Images ({len(images)})\n")
        md.append("| # | URL | Alt Text | Dimensions |")
        md.append("|---|---|---|---|")
        for i, img in enumerate(images, 1):
            dims = f"{img.get('width', '?')}×{img.get('height', '?')}"
            alt = img.get("alt", "").replace("|", "\\|")[:80]
            md.append(f"| {i} | {img.get('src', '')} | {alt} | {dims} |")
        md.append("")

    videos = media.get("videos", [])
    if videos:
        md.append(f"## Videos ({len(videos)})\n")
        for video in videos:
            if video.get("type") == "embedded":
                md.append(f"- 🎬 **{video.get('platform', '').title()}** — ID: `{video.get('video_id', '')}` — [Embed]({video.get('embed_url', '')})")
            else:
                for src in video.get("sources", []):
                    md.append(f"- 🎬 HTML5 Video: {src.get('src', '')}")
        md.append("")

    audio = media.get("audio", [])
    if audio:
        md.append(f"## Audio ({len(audio)})\n")
        for a in audio:
            for src in a.get("sources", []):
                md.append(f"- 🔊 Audio: {src.get('src', '')}")
        md.append("")

    if not images and not videos and not audio:
        md.append("*Không tìm thấy media nào trên trang này.*")
    _write_file(out_dir / "media.md", "\n".join(md))


def _write_contacts(data, out_dir):
    contacts = data.get("contacts", {})
    md = ["# 📇 Contacts\n"]

    emails = contacts.get("emails", [])
    if emails:
        md.append(f"## 📧 Emails ({len(emails)})\n")
        md.append("| # | Email | Nguồn | Ngữ cảnh |")
        md.append("|---|---|---|---|")
        for i, e in enumerate(emails, 1):
            md.append(f"| {i} | {e['email']} | {e.get('source', '')} | {e.get('context', '')} |")
        md.append("")

    phones = contacts.get("phones", [])
    if phones:
        md.append(f"## 📞 Phone Numbers ({len(phones)})\n")
        md.append("| # | Số điện thoại | Chuẩn hóa | Nguồn |")
        md.append("|---|---|---|---|")
        for i, p in enumerate(phones, 1):
            md.append(f"| {i} | {p['phone']} | {p.get('normalized', '')} | {p.get('source', '')} |")
        md.append("")

    social = contacts.get("social_profiles", [])
    if social:
        md.append(f"## 🌐 Social Media Profiles ({len(social)})\n")
        for p in social:
            md.append(f"- **{p.get('platform', '').title()}**: [{p.get('text', '')}]({p['url']})")
        md.append("")

    addresses = contacts.get("addresses", [])
    if addresses:
        md.append(f"## 📍 Addresses ({len(addresses)})\n")
        for addr in addresses:
            md.append(f"- {addr}")
        md.append("")

    if not emails and not phones and not social and not addresses:
        md.append("*Không tìm thấy thông tin liên hệ nào.*")
    _write_file(out_dir / "contacts.md", "\n".join(md))


def _write_forms_and_code(data, out_dir):
    forms_data = data.get("forms", {})
    text = data.get("text", {})
    nav = data.get("navigation", {})
    md = ["# 📋 Forms, Code & Resources\n"]

    forms = forms_data.get("forms", [])
    if forms:
        md.append(f"## 📝 Forms ({len(forms)})\n")
        for i, form in enumerate(forms, 1):
            md.append(f"### Form {i}")
            md.append(f"- **Action**: `{form.get('action', 'N/A')}`")
            md.append(f"- **Method**: `{form.get('method', 'GET')}`")
            if form.get("id"):
                md.append(f"- **ID**: `{form['id']}`")
            md.append(f"- **Fields**: {len(form.get('fields', []))}\n")
            fields = form.get("fields", [])
            if fields:
                md.append("| Tag | Type | Name | Placeholder | Required |")
                md.append("|---|---|---|---|---|")
                for f in fields:
                    md.append(f"| {f.get('tag', '')} | {f.get('type', '')} | {f.get('name', '')} | {f.get('placeholder', '')} | {'✅' if f.get('required') else ''} |")
            md.append("")

    code_blocks = text.get("code_blocks", [])
    if code_blocks:
        md.append(f"## 💻 Code Blocks ({len(code_blocks)})\n")
        for i, block in enumerate(code_blocks, 1):
            lang = block.get("language", "") or ""
            md.append(f"### Block {i}" + (f" ({lang})" if lang else ""))
            md.append(f"```{lang}")
            md.append(block.get("code", "")[:2000])
            md.append("```\n")

    stylesheets = nav.get("stylesheets", [])
    if stylesheets:
        md.append(f"## 🎨 Stylesheets ({len(stylesheets)})\n")
        for css in stylesheets:
            md.append(f"- `{css.get('url', '')}` (media: {css.get('media', 'all')})")
        md.append("")

    scripts = nav.get("scripts", [])
    if scripts:
        md.append(f"## ⚙️ Scripts ({len(scripts)})\n")
        for js in scripts:
            flags = []
            if js.get("async"):
                flags.append("async")
            if js.get("defer"):
                flags.append("defer")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            md.append(f"- `{js.get('url', '')}`{flag_str}")
        md.append("")

    nav_menus = nav.get("nav_menus", [])
    if nav_menus:
        md.append(f"## 🧭 Navigation Menus ({len(nav_menus)})\n")
        for menu in nav_menus:
            md.append(f"### {menu.get('label', 'Unnamed')}\n")
            for item in menu.get("items", []):
                md.append(f"- [{item.get('text', '')}]({item.get('url', '')})")
            md.append("")

    breadcrumbs = nav.get("breadcrumbs", [])
    if breadcrumbs:
        md.append("## 🍞 Breadcrumbs\n")
        parts = [f"[{bc.get('text', '')}]({bc['url']})" if bc.get("url") else bc.get("text", "") for bc in breadcrumbs]
        md.append(" > ".join(parts))
        md.append("")

    _write_file(out_dir / "forms_and_code.md", "\n".join(md))
