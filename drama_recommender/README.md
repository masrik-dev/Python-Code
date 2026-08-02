# Drama Recommender

This folder contains an automated Chinese short drama recommendation project that fetches:

- Top 10 popular Chinese short dramas with English dub from YouTube
- A web UI for browsing recommendations in a card layout

## Files

- `core.py` - scraping and ranking logic
- `main.py` - CLI script (terminal output)
- `app.py` - web frontend server (Flask)
- `templates/index.html` - main UI page
- `static/css/style.css` - UI styling
- `static/js/app.js` - frontend logic
- `requirements.txt` - Python dependencies

## Setup

1. Open a terminal in this folder:
   ```powershell
   cd c:\Users\User\OneDrive\Documents\GitHub\Atest\drama_recommender
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run everything (recommended)

One command does install + terminal results + web UI + browser:

```powershell
python run.py
```

On Windows you can also double-click:

```
run.bat
```

## Run CLI only

```powershell
python main.py
```

## Run Web UI

```powershell
python app.py
```

Then open in your browser:

```
http://127.0.0.1:5000
```

You can also run the wrapper in Imports:

```powershell
python Imports/drama_recommendation.py
```

## Web UI features

- Card layout with rank, thumbnail, channel, and views
- Live refresh button
- Loading panel while YouTube is fetched
- 5-minute cache to reduce repeated scraping
- Offline fallback list if YouTube is unreachable

## Notes

- The script shows progress in CLI mode while fetching.
- It retries on slow network or temporary YouTube errors.
- Links open directly on YouTube.
