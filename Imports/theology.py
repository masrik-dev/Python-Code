"""Theology overview with historical place and time.

Scrapes Wikipedia (summaries) and Wikidata (origin place + inception date)
for major theologies / religious systems, then prints a readable report.
"""

from __future__ import annotations

import re
import sys
import time
from typing import Any

import requests

# Avoid Windows cp1252 crashes on Wikipedia text (macrons, etc.).
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def safe_print(text: str = "") -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))

WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKIDATA_URL = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "User-Agent": (
        "AtestTheologyBot/1.0 "
        "(educational student project; contact: local)"
    ),
    "Accept": "application/json",
}
DEFAULT_TIMEOUT = 20

# Curated catalog: Wikipedia title + Wikidata QID + fallback place/time.
# Scraped live data is preferred; fallbacks are used if a request fails.
THEOLOGIES: list[dict[str, str]] = [
    {
        "name": "Judaism",
        "wiki": "Judaism",
        "qid": "Q9268",
        "fallback_place": "Ancient Near East (Levant / Israel)",
        "fallback_time": "c. 1200-500 BCE (Second Temple period solidification)",
    },
    {
        "name": "Zoroastrianism",
        "wiki": "Zoroastrianism",
        "qid": "Q9601",
        "fallback_place": "Ancient Iran (Persia)",
        "fallback_time": "c. 1500-1000 BCE (traditional dating of Zarathustra)",
    },
    {
        "name": "Hinduism",
        "wiki": "Hinduism",
        "qid": "Q9089",
        "fallback_place": "Indian subcontinent",
        "fallback_time": "c. 1500 BCE onward (Vedic roots; classical form later)",
    },
    {
        "name": "Buddhism",
        "wiki": "Buddhism",
        "qid": "Q748",
        "fallback_place": "Northern India / Nepal (Gangetic plain)",
        "fallback_time": "c. 5th-4th century BCE (life of the Buddha)",
    },
    {
        "name": "Confucianism",
        "wiki": "Confucianism",
        "qid": "Q9581",
        "fallback_place": "China (Lu state, East Asia)",
        "fallback_time": "c. 6th-5th century BCE (Confucius)",
    },
    {
        "name": "Taoism",
        "wiki": "Taoism",
        "qid": "Q9598",
        "fallback_place": "China",
        "fallback_time": "c. 4th-3rd century BCE (early Daoist texts)",
    },
    {
        "name": "Christianity",
        "wiki": "Christianity",
        "qid": "Q5043",
        "fallback_place": "Roman Judea / Eastern Mediterranean",
        "fallback_time": "1st century CE (Jesus movement; apostolic era)",
    },
    {
        "name": "Islam",
        "wiki": "Islam",
        "qid": "Q432",
        "fallback_place": "Arabian Peninsula (Mecca and Medina)",
        "fallback_time": "7th century CE (Prophet Muhammad, from 610 CE)",
    },
    {
        "name": "Sikhism",
        "wiki": "Sikhism",
        "qid": "Q9316",
        "fallback_place": "Punjab (Indian subcontinent)",
        "fallback_time": "15th-16th century CE (Guru Nanak, from 1469)",
    },
    {
        "name": "Shinto",
        "wiki": "Shinto",
        "qid": "Q812767",
        "fallback_place": "Japan",
        "fallback_time": "Prehistoric Japan; recorded from 8th century CE",
    },
]


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def fetch_wikipedia_summary(session: requests.Session, title: str) -> dict[str, Any]:
    url = WIKI_SUMMARY_URL.format(title=requests.utils.quote(title))
    response = session.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    return {
        "title": data.get("title") or title,
        "extract": (data.get("extract") or "").strip(),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        "description": data.get("description") or "",
    }


def _claim_values(entity: dict[str, Any], prop: str) -> list[dict[str, Any]]:
    claims = entity.get("claims", {}).get(prop, [])
    values = []
    for claim in claims:
        mainsnak = claim.get("mainsnak", {})
        if mainsnak.get("snaktype") != "value":
            continue
        values.append(mainsnak.get("datavalue", {}).get("value", {}))
    return values


def _time_to_text(time_value: dict[str, Any]) -> str:
    """Convert Wikidata time like '+0700-01-01T00:00:00Z' into readable text."""
    raw = time_value.get("time", "")
    precision = time_value.get("precision", 11)  # 9=year, 10=month, 11=day
    match = re.match(r"^([+-])(\d+)-(\d{2})-(\d{2})", raw)
    if not match:
        return raw or "Unknown"

    sign, year_s, month, day = match.groups()
    year = int(year_s)
    era = "BCE" if sign == "-" else "CE"
    display_year = year if sign == "+" else year  # Wikidata uses year 0 oddly; keep simple

    if precision <= 7:  # century or broader
        century = (display_year - 1) // 100 + 1 if sign == "+" else (display_year - 1) // 100 + 1
        return f"{century}th century {era} (approx.)"
    if precision == 8:  # decade
        decade = (display_year // 10) * 10
        return f"c. {decade}s {era}"
    if precision == 9:
        return f"c. {display_year} {era}"
    if precision == 10:
        return f"{month}/{display_year} {era}"
    return f"{day}/{month}/{display_year} {era}"


def fetch_entity_labels(
    session: requests.Session, qids: list[str]
) -> dict[str, str]:
    if not qids:
        return {}
    params = {
        "action": "wbgetentities",
        "ids": "|".join(sorted(set(qids))),
        "props": "labels",
        "languages": "en",
        "format": "json",
    }
    response = session.get(WIKIDATA_URL, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    entities = response.json().get("entities", {})
    labels = {}
    for qid, entity in entities.items():
        label = entity.get("labels", {}).get("en", {}).get("value")
        if label:
            labels[qid] = label
    return labels


def fetch_wikidata_place_and_time(
    session: requests.Session, qid: str
) -> dict[str, str]:
    """Pull inception (P571) and origin/location claims from Wikidata."""
    params = {
        "action": "wbgetentities",
        "ids": qid,
        "props": "claims|descriptions",
        "languages": "en",
        "format": "json",
    }
    response = session.get(WIKIDATA_URL, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    entity = response.json().get("entities", {}).get(qid, {})

    # Time: inception date
    time_text = ""
    for value in _claim_values(entity, "P571"):
        if isinstance(value, dict) and "time" in value:
            time_text = _time_to_text(value)
            break

    # Prefer formation / origin only (skip P17 "country" = modern presence).
    place_props = [
        "P740",  # location of formation
        "P495",  # country of origin
        "P276",  # location
    ]
    place_qids: list[str] = []
    for prop in place_props:
        for value in _claim_values(entity, prop):
            if isinstance(value, dict) and value.get("id"):
                place_qids.append(value["id"])
        if place_qids:
            break

    labels = fetch_entity_labels(session, place_qids[:3])
    places = [labels[q] for q in place_qids[:3] if q in labels]
    unique_places = list(dict.fromkeys(places))[:2]

    description = (
        entity.get("descriptions", {}).get("en", {}).get("value") or ""
    )

    return {
        "time": time_text,
        "place": ", ".join(unique_places),
        "wikidata_description": description,
    }


def build_theology_profile(
    session: requests.Session, entry: dict[str, str]
) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "name": entry["name"],
        "place": entry["fallback_place"],
        "time": entry["fallback_time"],
        "summary": "",
        "wiki_url": "",
        "source_notes": [],
    }

    try:
        wiki = fetch_wikipedia_summary(session, entry["wiki"])
        profile["summary"] = wiki["extract"]
        profile["wiki_url"] = wiki["url"]
        if wiki["description"]:
            profile["source_notes"].append(f"Wikipedia: {wiki['description']}")
    except requests.RequestException as exc:
        profile["summary"] = (
            f"(Could not fetch Wikipedia summary: {exc.__class__.__name__})"
        )
        profile["source_notes"].append("Wikipedia fetch failed; using fallbacks only")

    try:
        wiki_data = fetch_wikidata_place_and_time(session, entry["qid"])
        scraped_place = wiki_data["place"]
        # Use scrape when it looks like an origin, not a long modern list.
        if scraped_place and scraped_place.count(",") < 2:
            profile["place"] = scraped_place
            profile["source_notes"].append("Place from Wikidata")
        else:
            profile["source_notes"].append("Place from curated fallback")
        if wiki_data["time"]:
            # Prefer richer curated period when Wikidata only has a vague century.
            if "century" in wiki_data["time"] and "approx" in wiki_data["time"]:
                profile["source_notes"].append(
                    f"Wikidata time hint: {wiki_data['time']} (kept curated period)"
                )
            else:
                profile["time"] = wiki_data["time"]
                profile["source_notes"].append("Time from Wikidata inception (P571)")
        else:
            profile["source_notes"].append("Time from curated fallback")
        if wiki_data["wikidata_description"]:
            profile["source_notes"].append(
                f"Wikidata: {wiki_data['wikidata_description']}"
            )
    except requests.RequestException:
        profile["source_notes"].append(
            "Wikidata fetch failed; place/time from curated fallback"
        )

    return profile


def print_profile(profile: dict[str, Any], index: int) -> None:
    safe_print(f"\n{'=' * 72}")
    safe_print(f"{index}. {profile['name']}")
    safe_print(f"{'=' * 72}")
    safe_print(f"Circulated / origin place : {profile['place']}")
    safe_print(f"Historical time           : {profile['time']}")
    if profile["wiki_url"]:
        safe_print(f"Source                    : {profile['wiki_url']}")
    safe_print("-" * 72)
    summary = profile["summary"] or "No summary available."
    if len(summary) > 700:
        summary = summary[:697].rstrip() + "..."
    safe_print(summary)
    if profile["source_notes"]:
        safe_print("-" * 72)
        safe_print("Data notes: " + "; ".join(profile["source_notes"]))


def lookup_by_name(
    session: requests.Session, query: str
) -> dict[str, Any] | None:
    query_lower = query.strip().lower()
    for entry in THEOLOGIES:
        if entry["name"].lower() == query_lower:
            return build_theology_profile(session, entry)
    return None


def main() -> None:
    safe_print("Theology Atlas")
    safe_print("Live data from Wikipedia + Wikidata (with local fallbacks)")
    safe_print(f"Entries: {len(THEOLOGIES)}")

    session = create_session()
    profiles = []
    for i, entry in enumerate(THEOLOGIES):
        if i > 0:
            time.sleep(0.6)  # be polite to Wikipedia / Wikidata
        safe_print(f"\nFetching: {entry['name']} ...")
        profiles.append(build_theology_profile(session, entry))

    safe_print("\n" + "#" * 72)
    safe_print("THEOLOGIES BY PLACE AND TIME IN HISTORY")
    safe_print("#" * 72)

    for i, profile in enumerate(profiles, start=1):
        print_profile(profile, i)

    safe_print("\n" + "#" * 72)
    safe_print("QUICK REFERENCE TABLE")
    safe_print("#" * 72)
    safe_print(f"{'Theology':<16} {'Time':<40} {'Place'}")
    safe_print("-" * 72)
    for profile in profiles:
        time_short = profile["time"][:38]
        place_short = profile["place"][:40]
        safe_print(f"{profile['name']:<16} {time_short:<40} {place_short}")

    safe_print("\nTip: use lookup_by_name(session, 'Islam') for a single theology.")


if __name__ == "__main__":
    main()
