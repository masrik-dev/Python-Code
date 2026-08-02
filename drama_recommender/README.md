# Drama Recommender

This folder contains an automated Chinese short drama recommendation script that fetches:

- Top 10 popular Chinese short dramas with English dub from YouTube

## Files

- `main.py` - main script that scrapes YouTube search results and prints recommendations.
- `requirements.txt` - required Python dependency for the script.

## Setup

1. Open a terminal in this folder:
   ```powershell
   cd c:\Users\User\OneDrive\Documents\GitHub\Atest\drama_recommender
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run

```powershell
python main.py
```

The script runs automatically and prints the top 10 recommendations.

You can also run the wrapper in Imports:

```powershell
python Imports/drama_recommendation.py
```

## Notes

- The script shows progress while fetching so it does not look frozen.
- It retries on slow network or temporary YouTube errors.
- If YouTube is unreachable, it prints an offline fallback recommendation list.
