"""
download_data.py
----------------
Downloads StatsBomb open data for Serie A 2015/16 and saves the two CSV
files expected by the main notebook:

    data/seriea1516.csv      — event-level data  (~1.35M rows)
    data/aggregate_ita.csv   — match-level data  (380 rows)

Requirements:
    pip install statsbombpy

StatsBomb Open Data License:
    https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf
    Free for non-commercial use with attribution.
"""

import os
import sys

try:
    from statsbombpy import sb
except ImportError:
    sys.exit(
        "statsbombpy is not installed.\n"
        "Run:  pip install statsbombpy\n"
        "then retry."
    )

import pandas as pd

# ── Config ────────────────────────────────────────────────────────────────────
COMPETITION_ID = 12   # Serie A
SEASON_ID      = 27   # 2015/16
OUT_DIR        = os.path.dirname(os.path.abspath(__file__))

EVENTS_PATH = os.path.join(OUT_DIR, "seriea1516.csv")
AGG_PATH    = os.path.join(OUT_DIR, "aggregate_ita.csv")


def download_matches() -> pd.DataFrame:
    print("Downloading match list...")
    matches = sb.matches(competition_id=COMPETITION_ID, season_id=SEASON_ID)
    print(f"  {len(matches)} matches found.")
    return matches


def download_events(match_ids: list) -> pd.DataFrame:
    print(f"Downloading events for {len(match_ids)} matches — this may take several minutes...")
    frames = []
    for i, mid in enumerate(match_ids, 1):
        if i % 50 == 0 or i == len(match_ids):
            print(f"  {i}/{len(match_ids)} matches processed...")
        try:
            events = sb.events(match_id=mid)
            events["match_id"] = mid
            frames.append(events)
        except Exception as e:
            print(f"  Warning: could not download events for match {mid}: {e}")
    return pd.concat(frames, ignore_index=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── Matches ───────────────────────────────────────────────────────────────
    if os.path.exists(AGG_PATH):
        print(f"aggregate_ita.csv already exists — skipping download.")
        matches = pd.read_csv(AGG_PATH)
    else:
        matches = download_matches()
        matches.to_csv(AGG_PATH, index=False)
        print(f"  Saved → {AGG_PATH}")

    # ── Events ────────────────────────────────────────────────────────────────
    if os.path.exists(EVENTS_PATH):
        print(f"seriea1516.csv already exists — skipping download.")
    else:
        match_ids = matches["match_id"].tolist()
        events = download_events(match_ids)
        events.to_csv(EVENTS_PATH, index=False)
        print(f"  Saved → {EVENTS_PATH}  ({len(events):,} rows)")

    print("\nDone. You can now open the notebook.")


if __name__ == "__main__":
    main()
