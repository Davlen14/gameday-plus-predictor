# Quick Database Reference - Gameday+ Predictor

## 🎯 Quick Access Guide

### Main Databases (3 Active)

```
📁 instance/
├── 📊 coaches_master.db (18 MB) ⭐ Primary Coach Database
│   └── 24 tables: coaches, teams, players, games, recruiting, NIL, etc.
│
├── 🎲 predictions.db (7.5 MB) ⭐ Prediction Engine Database  
│   └── 20 tables: upcoming_games, betting_lines, team_stats, rankings
│
└── 🧪 campbell_test.db (100 KB)
    └── Test database

📁 / (root)
└── 📈 gameday_analytics.db (31 MB) ⭐ Live Game Analytics
    └── 4 tables: teams, games, drives, plays
```

---

## 🚀 Which Database to Use?

| Need | Use This Database | Key Tables |
|------|-------------------|------------|
| Coach info & history | `coaches_master.db` | coaches, stints, games |
| Game predictions | `predictions.db` | upcoming_games, sportsbook_lines |
| Betting lines | `predictions.db` | sportsbook_lines, sportsbook_lines_history |
| Team stats | `predictions.db` | team_offensive_stats, team_defensive_stats |
| Player rosters | `coaches_master.db` | players, player_stats |
| Live game data | `gameday_analytics.db` | drives, plays |
| Recruiting data | `coaches_master.db` | recruiting_classes, talent_composite |
| NIL data | `coaches_master.db` | nil_players, nil_team_summary |

---

## 🔌 Quick Connection Examples

### Python
```python
import sqlite3

# Connect to coach database
conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()
cursor.execute('SELECT name, school FROM coaches LIMIT 5')
print(cursor.fetchall())
conn.close()

# Connect to predictions database
conn = sqlite3.connect('instance/predictions.db')
cursor = conn.cursor()
cursor.execute('SELECT home_team, away_team, spread FROM upcoming_games LIMIT 5')
print(cursor.fetchall())
conn.close()
```

### Command Line
```bash
# Browse coaches database
sqlite3 instance/coaches_master.db

# Browse predictions database
sqlite3 instance/predictions.db

# Quick table count
sqlite3 instance/coaches_master.db ".tables"
```

---

## 📊 Table Counts by Database

| Database | Tables | Primary Content |
|----------|--------|-----------------|
| coaches_master.db | 24 | Coaches, teams, players, recruiting, NIL |
| predictions.db | 20 | Games, betting, analytics, rankings |
| gameday_analytics.db | 4 | Live drives and plays |
| campbell_test.db | ? | Test data |

---

## 🛠️ Application Usage

### Flask Backend (port 5002) - app.py
- Uses: `predictions.db` + `coaches_master.db`
- For: ML predictions, betting analysis

### Coach Database API (port 5555) - app_master.py  
- Uses: `coaches_master.db` only
- For: Coach/team exploration, NIL data

---

## 📋 Most Used Tables

### From coaches_master.db:
1. **coaches** - Coach biographical data
2. **teams** - FBS team information  
3. **stints** - Coaching position history
4. **games** - Game results
5. **recruiting_classes** - Recruiting data
6. **players** - Player rosters

### From predictions.db:
1. **upcoming_games** - Future matchups with lines
2. **sportsbook_lines** - Multi-book betting odds
3. **team_offensive_stats** - Offensive metrics
4. **team_defensive_stats** - Defensive metrics
5. **historical_game_results** - Past game data

### From gameday_analytics.db:
1. **drives** - Drive-by-drive data
2. **plays** - Play-by-play details

---

## 🔄 Update Commands

```bash
# Update betting lines
python update_betting_lines.py

# Import upcoming games  
python import_upcoming_games.py

# Track line movements
python track_line_movements.py

# Import rankings
python import_comprehensive_rankings.py
```

---

## 📍 File Locations

```bash
# Primary databases
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/instance/coaches_master.db
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/instance/predictions.db
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/gameday_analytics.db

# Schema files
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/create_espn_tables.sql
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/add_missing_columns.sql

# Backups
/home/runner/work/gameday-plus-predictor/gameday-plus-predictor/backups/cleanup_20251214_103010/
```

---

## 🎓 Tips

- Always use `instance/coaches_master.db`, not root `coaches_master.db` (empty)
- Betting lines in `predictions.db` need regular updates
- Use `app_master.py` for coach/team queries (faster, simpler)
- Full prediction engine in `app.py` includes ML models

---

**For detailed documentation, see:** `DATABASE_INVENTORY.md`
