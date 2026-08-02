"""CLI entry point for drama recommendations."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import TOP_LIMIT, get_top_drama_recommendations


def safe_print(text: str = "") -> None:
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), flush=True)


def print_recommendations(items: list, source: str) -> None:
    safe_print("\nTop 10 Chinese Short Drama Recommendations (English Dub)")
    safe_print(f"Source: {source}")
    safe_print("=" * 60)

    for index, item in enumerate(items, start=1):
        safe_print(f"\n{index}. {item['title']}")
        safe_print(f"   Channel : {item['channel']}")
        safe_print(f"   Views   : {item['views']}")
        safe_print(f"   Link    : {item['url']}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    recommendations, source, _ = get_top_drama_recommendations(
        TOP_LIMIT,
        log=safe_print,
    )
    print_recommendations(recommendations, source)


if __name__ == "__main__":
    main()
