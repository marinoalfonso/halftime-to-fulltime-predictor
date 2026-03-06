# Data

The raw CSV files are **not included in this repository** due to their size (~1 GB for the event file).

## How to download

```bash
python data/download_data.py
```

This script uses the official [`statsbombpy`](https://github.com/statsbomb/statsbomb-py) library to download the data directly from StatsBomb's open-data GitHub repository and saves two files:

| File | Description | Rows | Size (approx.) |
|---|---|---|---|
| `seriea1516.csv` | Event-level data — every on-ball action | ~1,353,739 | ~950 MB |
| `aggregate_ita.csv` | Match-level data — scores, dates, teams | 380 | < 1 MB |

## Data structure

### `seriea1516.csv` (key columns)

| Column | Description |
|---|---|
| `match_id` | Unique match identifier |
| `type.name` | Event type (Pass, Shot, Pressure, …) |
| `team.name` | Team that performed the action |
| `player.name` | Player that performed the action |
| `period` | 1 = first half, 2 = second half |
| `location.x / .y` | Pitch coordinates (0–120 × 0–80) |
| `shot.statsbomb_xg` | Expected goal value (shots only) |
| `pass.outcome.name` | Pass outcome (null = completed) |

### `aggregate_ita.csv` (key columns)

| Column | Description |
|---|---|
| `match_id` | Unique match identifier |
| `home_team.home_team_name` | Home team name |
| `away_team.away_team_name` | Away team name |
| `home_score` | Full-time home goals |
| `away_score` | Full-time away goals |
| `match_date` | Date of the match |
| `match_week` | Matchday number |

## Source & License

- **Provider:** [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- **Competition:** Serie A, season 2015/16 (`competition_id=12`, `season_id=27`)
- **License:** [StatsBomb Open Data License](https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf)

The data is free for non-commercial use. If you use it in your own work, please include the following attribution:

> Data provided by StatsBomb via [statsbomb/open-data](https://github.com/statsbomb/open-data)
