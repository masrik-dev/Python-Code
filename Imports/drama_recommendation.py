"""Wrapper for drama_recommender project.

Run this file or: python drama_recommender/main.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "drama_recommender" / "main.py"


def _load_main():
    spec = importlib.util.spec_from_file_location("drama_recommender_main", MAIN_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {MAIN_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    drama_main = _load_main()
    drama_main.main()
