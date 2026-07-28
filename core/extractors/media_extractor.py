"""
Media Extractor — Extract images, videos (including
embedded YouTube/Vimeo), and audio tags.
"""

import re
from typing import Any, Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from core.logger import logger


def extract_media(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    """Extract all media elements from the page."""

    logger.info("Extracting media...")

    data = {
        "images": _get_images(soup, base_url),
        "videos": _get_videos(soup, base_url),
        "audio": _get_audio(soup, base_url),
    }

    logger.info(
        f"Media extracted: {len(data['images'])} images, "
        f"{len(data['videos'])} videos, "
        f"{len(data['audio'])} audio"
    )

    return data


def _get_images(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """Extract all images with attributes."""

    images = []

    for img in soup.find_all("img"):
        src = (
            img.get("src", "")
            or img.get("data-src", "")
            or img.get("data-lazy-src", "")
            or img.get("data-original", "")
            or img.get("loading", "")
        )

        if not src or src.startswith("data:"):
            continue

        full_src = urljoin(base_url, src)

        image_data = {
            "src": full_src,
            "alt": img.get("alt", ""),
            "title": img.get("title", ""),
            "width": img.get("width", ""),
            "height": img.get("height", ""),
            "loading": img.get("loading", ""),
        }

        # Check for srcset
        srcset = img.get("srcset", "")
        if srcset:
            image_data["srcset"] = srcset

        images.append(image_data)

    # Also check <picture> sources
    for picture in soup.find_all("picture"):
        for source in picture.find_all("source"):
            srcset = source.get("srcset", "")
            if srcset:
                first_src = srcset.split(",")[0].strip().split(" ")[0]
                images.append({
                    "src": urljoin(base_url, first_src),
                    "alt": "",
                    "title": "",
                    "width": "",
                    "height": "",
                    "loading": "",
                    "type": source.get("type", ""),
                    "media": source.get("media", ""),
                })

    return images


def _get_videos(soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
    """Extract video elements and embedded videos."""

    videos = []

    # <video> tags
    for video in soup.find_all("video"):
        sources = []
        for source in video.find_all("source"):
            sources.append({
                "src": urljoin(base_url, source.get("src", "")),
                "type": source.get("type", ""),
            })

        video_src = video.get("src", "")
        if video_src:
            sources.append({
                "src": urljoin(base_url, video_src),
                "type": "",
            })

        if sources:
            videos.append({
                "type": "html5_video",
                "sources": sources,
                "poster": urljoin(base_url, video.get("poster", "")) if video.get("poster") else "",
                "controls": video.has_attr("controls"),
                "autoplay": video.has_attr("autoplay"),
            })

    # Embedded iframes (YouTube, Vimeo, etc.)
    for iframe in soup.find_all("iframe", src=True):
        src = iframe.get("src", "")

        platform = None
        video_id = ""

        # YouTube
        yt_match = re.search(
            r'(?:youtube\.com/embed/|youtube-nocookie\.com/embed/)([a-zA-Z0-9_-]+)',
            src
        )
        if yt_match:
            platform = "youtube"
            video_id = yt_match.group(1)

        # Vimeo
        vm_match = re.search(r'player\.vimeo\.com/video/(\d+)', src)
        if vm_match:
            platform = "vimeo"
            video_id = vm_match.group(1)

        # Dailymotion
        dm_match = re.search(r'dailymotion\.com/embed/video/([a-zA-Z0-9]+)', src)
        if dm_match:
            platform = "dailymotion"
            video_id = dm_match.group(1)

        if platform:
            videos.append({
                "type": "embedded",
                "platform": platform,
                "video_id": video_id,
                "embed_url": src,
                "width": iframe.get("width", ""),
                "height": iframe.get("height", ""),
            })

    return videos


def _get_audio(soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
    """Extract audio elements."""

    audio_list = []

    for audio in soup.find_all("audio"):
        sources = []
        for source in audio.find_all("source"):
            sources.append({
                "src": urljoin(base_url, source.get("src", "")),
                "type": source.get("type", ""),
            })

        audio_src = audio.get("src", "")
        if audio_src:
            sources.append({
                "src": urljoin(base_url, audio_src),
                "type": "",
            })

        if sources:
            audio_list.append({
                "sources": sources,
                "controls": audio.has_attr("controls"),
            })

    return audio_list
