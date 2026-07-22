# Anime Recommender

This folder contains an automated anime recommendation script that fetches:

- Top 10 anime of all time
- Top 10 anime from the last 12 months

## Files

- `main.py` — main script that fetches recommendation data from the Jikan API and prints results.
- `requirements.txt` — required Python dependency for the script.

## Setup

1. Open a terminal in this folder:
   ```powershell
   cd c:\Users\User\OneDrive\Documents\GitHub\Atest\anime_recommender
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run

```powershell
python main.py
```

The script runs automatically and prints both recommendation lists.

## Notes

- The script uses the Jikan API, which may occasionally return rate-limit or temporary errors.
- If the last-year list cannot be built, the script will still print the all-time top 10 list.
