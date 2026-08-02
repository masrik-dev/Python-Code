"""Web frontend for Chinese short drama recommendations."""

from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, jsonify, render_template, request

from core import TOP_LIMIT, get_top_drama_recommendations

app = Flask(__name__)

_cache: dict[str, Any] = {
    "items": [],
    "source": "",
    "is_fallback": False,
    "fetched_at": None,
}
CACHE_SECONDS = 300


def _cache_valid() -> bool:
    fetched_at = _cache.get("fetched_at")
    if not fetched_at or not _cache.get("items"):
        return False
    age = (datetime.datetime.utcnow() - fetched_at).total_seconds()
    return age < CACHE_SECONDS


def warm_cache(items: list[dict[str, Any]], source: str, is_fallback: bool) -> None:
    """Store results so the web UI loads instantly after CLI fetch."""
    _cache["items"] = items
    _cache["source"] = source
    _cache["is_fallback"] = is_fallback
    _cache["fetched_at"] = datetime.datetime.utcnow()


def _fetch_recommendations(force: bool = False) -> dict[str, Any]:
    if not force and _cache_valid():
        return {
            "items": _cache["items"],
            "source": _cache["source"],
            "is_fallback": _cache["is_fallback"],
            "fetched_at": _cache["fetched_at"].isoformat() + "Z",
            "cached": True,
        }

    items, source, is_fallback = get_top_drama_recommendations(TOP_LIMIT)
    fetched_at = datetime.datetime.utcnow()

    _cache["items"] = items
    _cache["source"] = source
    _cache["is_fallback"] = is_fallback
    _cache["fetched_at"] = fetched_at

    return {
        "items": items,
        "source": source,
        "is_fallback": is_fallback,
        "fetched_at": fetched_at.isoformat() + "Z",
        "cached": False,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recommendations")
def api_recommendations():
    force = request.args.get("refresh", "0") == "1"
    data = _fetch_recommendations(force=force)
    return jsonify(data)


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
