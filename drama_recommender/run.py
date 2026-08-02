"""One-click runner for the Drama Recommender project.

Does everything in order:
1. Installs required packages (if missing)
2. Fetches top 10 dramas and prints results in the terminal
3. Starts the web UI and opens your browser
"""

from __future__ import annotations

import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HOST = "127.0.0.1"
PORT = 5000
APP_URL = f"http://{HOST}:{PORT}"


def safe_print(text: str = "") -> None:
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), flush=True)


def install_dependencies() -> None:
    safe_print("Step 1/3: Checking dependencies...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
    )
    safe_print("Dependencies ready.\n")


def print_cli_results() -> None:
    from core import TOP_LIMIT, get_top_drama_recommendations

    safe_print("Step 2/3: Fetching top 10 Chinese short dramas (English dub)...")
    safe_print("This may take 10-30 seconds on slow networks.\n")

    items, source, is_fallback = get_top_drama_recommendations(
        TOP_LIMIT,
        log=safe_print,
    )

    safe_print("\nTop 10 Chinese Short Drama Recommendations (English Dub)")
    safe_print(f"Source: {source}")
    safe_print("=" * 60)

    for index, item in enumerate(items, start=1):
        safe_print(f"\n{index}. {item['title']}")
        safe_print(f"   Channel : {item['channel']}")
        safe_print(f"   Views   : {item['views']}")
        safe_print(f"   Link    : {item['url']}")

    from app import warm_cache

    warm_cache(items, source, is_fallback)
    safe_print("\nCLI results ready.\n")
    return None


def open_browser_later() -> None:
    time.sleep(1.5)
    webbrowser.open(APP_URL)


def start_web_app() -> None:
    from app import app

    safe_print("Step 3/3: Starting web UI...")
    safe_print(f"Open in browser: {APP_URL}")
    safe_print("Press Ctrl+C to stop the server.\n")

    threading.Thread(target=open_browser_later, daemon=True).start()
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    safe_print("=" * 60)
    safe_print("Drama Recommender - Full Run")
    safe_print("=" * 60 + "\n")

    install_dependencies()
    print_cli_results()
    start_web_app()


if __name__ == "__main__":
    main()
