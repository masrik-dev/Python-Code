"""Automated anime recommendation using Jikan API.

This module fetches the top 10 anime of all time and the top 10 anime from the last 12 months.
The code runs automatically when executed and does not require user input.
"""

from __future__ import annotations

import datetime
import requests
from typing import Any

JIKAN_TOP_URL = "https://api.jikan.moe/v4/top/anime"
JIKAN_SEASON_URL = "https://api.jikan.moe/v4/seasons/{year}/{season}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
DEFAULT_TIMEOUT = 20
TOP_LIMIT = 10


def parse_iso_datetime(value: str | None) -> datetime.datetime | None:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": item.get("title"),
        "score": item.get("score"),
        "type": item.get("type"),
        "url": item.get("url"),
        "start_date": item.get("aired", {}).get("from"),
    }


def fetch_top_all_time(limit: int = TOP_LIMIT) -> list[dict[str, Any]]:
    params = {"limit": limit}
    response = requests.get(JIKAN_TOP_URL, params=params, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json().get("data", [])
    return [extract_item(item) for item in data[:limit]]


def season_name_from_month(month: int) -> str:
    if month in (1, 2, 3):
        return "winter"
    if month in (4, 5, 6):
        return "spring"
    if month in (7, 8, 9):
        return "summer"
    return "fall"


def previous_season(year: int, season: str) -> tuple[int, str]:
    order = ["winter", "spring", "summer", "fall"]
    index = order.index(season) - 1
    if index < 0:
        return year - 1, order[-1]
    return year, order[index]


def seasons_for_last_year(today: datetime.date | None = None) -> list[tuple[int, str]]:
    today = today or datetime.date.today()
    season = season_name_from_month(today.month)
    year = today.year
    seasons: list[tuple[int, str]] = []
    # Use five seasons to cover a full year and include the current season.
    for _ in range(5):
        seasons.append((year, season))
        year, season = previous_season(year, season)
    return seasons


def fetch_season_anime(year: int, season: str) -> list[dict[str, Any]]:
    url = JIKAN_SEASON_URL.format(year=year, season=season)
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json().get("data", [])
    return [extract_item(item) for item in data]


def top_anime_from_last_year(limit: int = TOP_LIMIT) -> list[dict[str, Any]]:
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=365)
    seen_titles: set[str] = set()
    candidates: list[dict[str, Any]] = []

    for year, season in seasons_for_last_year():
        try:
            season_items = fetch_season_anime(year, season)
        except requests.RequestException:
            continue
        for item in season_items:
            title = item.get("title")
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)
            start_date = parse_iso_datetime(item.get("start_date"))
            if start_date is None or start_date < cutoff_date:
                continue
            if item.get("score") is None:
                continue
            candidates.append(item)

    candidates.sort(key=lambda x: (-float(x["score"]), x["title"] or ""))
    return candidates[:limit]


def format_recommendations(title: str, items: list[dict[str, Any]]) -> str:
    lines = [f"{title}"]
    for index, item in enumerate(items, start=1):
        score = item.get("score")
        lines.append(f"{index}. {item.get('title')} ({item.get('type')}) - score: {score}")
    return "\n".join(lines)


def get_recommendations() -> dict[str, list[dict[str, Any]]]:
    return {
        "all_time_top_10": fetch_top_all_time(TOP_LIMIT),
        "last_year_top_10": top_anime_from_last_year(TOP_LIMIT),
    }


def print_recommendations() -> None:
    recommendations = get_recommendations()
    print(format_recommendations("Top 10 Anime of All Time:", recommendations["all_time_top_10"]))
    print()
    if recommendations["last_year_top_10"]:
        print(format_recommendations("Top 10 Anime from the Last 12 Months:", recommendations["last_year_top_10"]))
    else:
        print("Top 10 Anime from the Last 12 Months: No data could be retrieved.")


if __name__ == "__main__":
    print_recommendations()
