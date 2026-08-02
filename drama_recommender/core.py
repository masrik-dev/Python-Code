"""Core logic for Chinese short drama YouTube recommendations."""

from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable

import requests

SEARCH_QUERIES = [
    "chinese short drama english dub",
    "cdrama short series english dubbed",
    "mini chinese drama english dub full",
]
YOUTUBE_SEARCH_URL = "https://www.youtube.com/results"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 35
MAX_RETRIES = 3
TOP_LIMIT = 10

FALLBACK_DRAMAS = [
    {
        "title": "Flash Marriage CEO - English Dub (Short Drama)",
        "channel": "Short Drama Channel",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=flash+marriage+ceo+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Reborn Revenge Queen - English Dub CDrama",
        "channel": "Chinese Drama Dubbed",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=reborn+revenge+queen+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "My Secret Billionaire Husband - Short Drama English Dub",
        "channel": "Mini Drama Hub",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=secret+billionaire+husband+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Love After Marriage - Chinese Short Drama English Dub",
        "channel": "CDrama Shorts",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=love+after+marriage+chinese+drama+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "The Hidden Heiress - English Dub Mini Series",
        "channel": "Drama Shorts EN",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=hidden+heiress+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "CEO Falls For Me - Chinese Short Drama English Dub",
        "channel": "Short CDrama EN",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=ceo+falls+for+me+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Return of the Dragon King - English Dub Short Drama",
        "channel": "Chinese Mini Drama",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=return+dragon+king+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Contract Marriage With The CEO - English Dub",
        "channel": "Drama Dub Studio",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=contract+marriage+ceo+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Revenge of the Abandoned Wife - English Dub CDrama",
        "channel": "Short Drama World",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=revenge+abandoned+wife+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
    {
        "title": "Billionaire's Hidden Love - Chinese Short Drama English Dub",
        "channel": "Mini Series EN",
        "views": "Popular pick",
        "view_count": 0,
        "url": "https://www.youtube.com/results?search_query=billionaire+hidden+love+english+dub",
        "video_id": "",
        "thumbnail": "",
    },
]


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def parse_view_count(text: str) -> int:
    if not text:
        return 0
    cleaned = text.lower().replace(" views", "").replace(",", "").strip()
    match = re.match(r"^([\d.]+)\s*([kmb])?$", cleaned)
    if not match:
        digits = re.sub(r"[^\d]", "", cleaned)
        return int(digits) if digits else 0

    number = float(match.group(1))
    suffix = match.group(2) or ""
    multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}
    return int(number * multipliers.get(suffix, 1))


def extract_yt_initial_data(html: str) -> dict[str, Any] | None:
    marker = "var ytInitialData = "
    start = html.find(marker)
    if start == -1:
        return None

    start += len(marker)
    if start >= len(html) or html[start] != "{":
        return None

    depth = 0
    for index in range(start, len(html)):
        char = html[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(html[start : index + 1])
                except json.JSONDecodeError:
                    return None
    return None


def thumbnail_url(video_id: str) -> str:
    if not video_id:
        return ""
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"


def extract_search_videos(html: str) -> list[dict[str, Any]]:
    data = extract_yt_initial_data(html)
    if not data:
        return []

    sections = (
        data.get("contents", {})
        .get("twoColumnSearchResultsRenderer", {})
        .get("primaryContents", {})
        .get("sectionListRenderer", {})
        .get("contents", [])
    )

    videos: list[dict[str, Any]] = []
    for section in sections:
        items = section.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            renderer = item.get("videoRenderer")
            if not renderer:
                continue

            title_runs = renderer.get("title", {}).get("runs", [])
            title = title_runs[0]["text"] if title_runs else "Unknown title"

            channel_runs = (
                renderer.get("ownerText", {}).get("runs")
                or renderer.get("longBylineText", {}).get("runs")
                or []
            )
            channel = channel_runs[0]["text"] if channel_runs else "Unknown channel"

            view_text = (
                renderer.get("viewCountText", {}).get("simpleText")
                or renderer.get("shortViewCountText", {}).get("simpleText")
                or ""
            )

            video_id = renderer.get("videoId", "")
            videos.append(
                {
                    "title": title,
                    "channel": channel,
                    "views": view_text or "N/A",
                    "view_count": parse_view_count(view_text),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "video_id": video_id,
                    "thumbnail": thumbnail_url(video_id),
                }
            )
    return videos


def is_relevant_drama(video: dict[str, Any]) -> bool:
    text = f"{video['title']} {video['channel']}".lower()
    drama_words = ("drama", "cdrama", "series", "episode", "mini", "short")
    english_words = ("english", "dub", "dubbed", "eng sub", "eng dub")
    chinese_words = ("chinese", "china", "cdrama", "c-drama", "mandarin")

    has_drama = any(word in text for word in drama_words)
    has_english = any(word in text for word in english_words)
    has_chinese = any(word in text for word in chinese_words)
    return has_drama and (has_english or has_chinese)


def fetch_youtube_search(
    session: requests.Session,
    query: str,
    log: Callable[[str], None] | None = None,
) -> list[dict[str, Any]]:
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if log:
                log(f"Search attempt {attempt}/{MAX_RETRIES}: {query}")
            response = session.get(
                YOUTUBE_SEARCH_URL,
                params={"search_query": query},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if response.status_code in {429, 502, 503, 504} and attempt < MAX_RETRIES:
                wait = attempt * 2
                if log:
                    log(f"YouTube returned {response.status_code}. Retrying in {wait}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            videos = extract_search_videos(response.text)
            if log:
                log(f"Found {len(videos)} videos for: {query}")
            return videos
        except requests.RequestException as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                wait = attempt * 2
                if log:
                    log(f"Network error ({exc.__class__.__name__}). Retrying in {wait}s...")
                time.sleep(wait)

    if last_error:
        raise last_error
    return []


def fetch_query_worker(
    query: str,
    log: Callable[[str], None] | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    session = create_session()
    try:
        return query, fetch_youtube_search(session, query, log=log)
    except requests.RequestException:
        return query, []


def get_top_drama_recommendations(
    limit: int = TOP_LIMIT,
    log: Callable[[str], None] | None = None,
) -> tuple[list[dict[str, Any]], str, bool]:
    seen_ids: set[str] = set()
    candidates: list[dict[str, Any]] = []
    source = "YouTube search (ranked by popularity)"
    is_fallback = False

    if log:
        log("Fetching drama recommendations from YouTube...")
        log("This may take 10-30 seconds on slow networks.")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(fetch_query_worker, query, log)
            for query in SEARCH_QUERIES
        ]

        for future in as_completed(futures):
            query, results = future.result()
            added = 0
            for video in results:
                video_id = video.get("video_id")
                if not video_id or video_id in seen_ids:
                    continue
                if not is_relevant_drama(video):
                    continue
                seen_ids.add(video_id)
                candidates.append(video)
                added += 1

            if log:
                log(f"Added {added} relevant videos from: {query}")

    if not candidates:
        source = "Offline fallback list (YouTube was slow or unreachable)"
        is_fallback = True
        return FALLBACK_DRAMAS[:limit], source, is_fallback

    candidates.sort(
        key=lambda item: (-item.get("view_count", 0), item.get("title", ""))
    )
    return candidates[:limit], source, is_fallback
