# Gameday+ Development Guide

## Project Overview
Gameday+ is a full-stack college football prediction platform with ML-powered analytics, betting line analysis, and rivalry game tracking.

---

## Application Architecture

### Two Main Server Applications

#### 1. **start-fullstack.sh** - Full Production Stack
**Purpose**: Launches your complete **full stack** (backend + frontend)

**Servers it starts**:
- 🐍 **Flask backend** (`app.py`) on **port 5002** - Your prediction engine with complex ML
- 🎨 **React frontend** (`npm run dev`) on **port 5173** - The UI

**What it does**: 
- Opens TWO separate Terminal tabs (one for each server)
- Runs health checks to verify both are running
- Pipes logs to `logs/backend.log` and `logs/frontend.log`

**Target**: Full production-ready app with UI

**How to run**:
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
./start-fullstack.sh
```

---

#### 2. **app_master.py** - Coach Database API
**Purpose**: A **standalone coach database API** for exploring coaching data

**Server it starts**:
- Single Flask app on **port 5555** (different from 5002!)
- Only serves coach/team/recruiting data from `coaches_master.db`
- NO React frontend needed
- NO prediction engine (`graphqlpredictor.py`)
- Much simpler imports (just Flask, sqlite3, pathlib)

**What it does**: 
- Serves database endpoints like `/api/coaches`, `/api/coach/<id>`, etc.
- Renders HTML templates for exploration dashboards

**Target**: Database explorer/API for coaching data only

**How to run**:
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
source .venv/bin/activate
python app_master.py
```

**Available URLs** (access at `http://localhost:5555`):

**General**
- `http://localhost:5555/` - API documentation homepage
- `http://localhost:5555/fbs.json` - FBS teams JSON data

**UI Pages**
- `http://localhost:5555/gamedaylive` - **🏈 Main landing page with game cards slider**
- `http://localhost:5555/coaches` - Coaches list page
- `http://localhost:5555/coach/<id>` - Coach detail page
- `http://localhost:5555/teams` - Teams list page
- `http://localhost:5555/team/<id>` - Team detail page
- `http://localhost:5555/nil` - NIL overview page
- `http://localhost:5555/nil/team/<id>` - NIL team page
- `http://localhost:5555/drives-explorer` - Drives explorer dashboard
- `http://localhost:5555/predictions` - Predictions page

**⚠️ IMPORTANT: When working on templates (HTML/CSS), ALWAYS use `app_master.py` on port 5555**

**API Endpoints - Coaches**
- `http://localhost:5555/api/coaches` - List all coaches
- `http://localhost:5555/api/coach/<id>` - Coach details
- `http://localhost:5555/api/coach/<id>/stints` - Coaching history
- `http://localhost:5555/api/coach/<id>/games` - Game history
- `http://localhost:5555/api/coach/<id>/rankings` - AP Poll history
- `http://localhost:5555/api/coach/<id>/draft_picks` - NFL draft picks
- `http://localhost:5555/api/coach/<id>/situational` - Situational stats
- `http://localhost:5555/api/coach/<id>/situational_stats` - Situational stats (alt)
- `http://localhost:5555/api/coach/<id>/vs_coaches` - Head-to-head records
- `http://localhost:5555/api/coach/<id>/season_analytics` - Season analytics
- `http://localhost:5555/api/coach/<id>/recruiting` - Recruiting classes
- `http://localhost:5555/api/coach/<id>/recruiting_classes` - Recruiting classes (alt)
- `http://localhost:5555/api/coach/<id>/talent` - Talent composite
- `http://localhost:5555/api/coach/<id>/talent_composite` - Talent composite (alt)
- `http://localhost:5555/api/coach/<id>/portal` - Transfer portal
- `http://localhost:5555/api/coach/<id>/transfer_portal` - Transfer portal (alt)

**API Endpoints - Teams**
- `http://localhost:5555/api/teams` - List all teams
- `http://localhost:5555/api/team/<id>` - Team details
- `http://localhost:5555/api/team/<id>/roster` - Team roster

**API Endpoints - Search & Stats**
- `http://localhost:5555/api/search?q=<query>` - Search coaches/teams
- `http://localhost:5555/api/stats` - General stats
- `http://localhost:5555/api/predictions/table/<table_name>` - Prediction table data
- `http://localhost:5555/api/upcoming-games` - Upcoming games

**API Endpoints - NIL**
- `http://localhost:5555/api/nil/teams` - NIL teams list
- `http://localhost:5555/api/nil/team/<id>` - NIL team data
- `http://localhost:5555/api/nil/team/<id>/players` - NIL team players
- `http://localhost:5555/api/nil/team/<id>/positions` - NIL team positions

**API Endpoints - Drives**
- `http://localhost:5555/api/drives/teams` - All teams with drives
- `http://localhost:5555/api/drives/team/<team_name>/drives` - Team drives
- `http://localhost:5555/api/drives/team/<team_name>/stats` - Team drive stats
- `http://localhost:5555/api/drives/drive/<id>/plays` - Drive plays



## Comparison Table

| Feature | start-fullstack.sh | app_master.py |
|---------|---|---|
| **Purpose** | Full prediction platform | Coach database explorer |
| **Backend Port** | 5002 | 5555 |
| **Complexity** | Complex (ML predictor) | Simple (database queries) |
| **Includes Frontend?** | ✅ Yes (React) | ❌ No |
| **Imports heavy modules?** | ✅ Yes (graphqlpredictor, betting_lines_manager) | ❌ No (just sqlite3) |
| **Database Used** | `predictions.db` | `coaches_master.db` |
| **Startup Speed** | Slower (complex imports) | Faster (minimal dependencies) |

---

## Key Modules

### Heavy Import Modules (used in app.py)
- **graphqlpredictor.py** - ML prediction engine
- **betting_lines_manager.py** - Now uses **lazy loading** to avoid network calls on startup
- **game_media_service.py** - Game broadcast information
- **batch_rivalry_analyzer.py** - Rivalry game analysis

### Light Import Modules (used in app_master.py)
- **sqlite3** - Database queries only
- **pathlib** - File path handling
- **Flask** - Web framework

---

## Important Implementation Notes

### Lazy Loading Pattern (betting_lines_manager.py)
The `betting_lines_manager.py` module uses **lazy initialization** to prevent blocking on startup:

```python
def __init__(self):
    self.games_data = None
    self.current_week_data = None
    self._initialized = False

def _ensure_initialized(self):
    """Lazy load data on first access"""
    if not self._initialized:
        self.games_data = self._load_games_data()
        self.current_week_data = self._load_current_week_data()
        self._initialized = True
```

This prevents the app from hanging when the GraphQL API is slow or unreachable during startup. Data is only fetched when first needed.

---

## Betting Lines & Database Updates

### Updating Betting Lines
The application stores betting lines from multiple sportsbooks in the `sportsbook_lines` table. Lines should be refreshed regularly as they change frequently.

**Database Structure**:
- `upcoming_games` - Main game data with basic consensus lines
- `sportsbook_lines` - Multiple sportsbook lines per game (DraftKings, Bovada, etc.)

**Update betting lines from GraphQL API**:
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
python update_betting_lines.py
```

**What it does**:
- Fetches latest spreads and over/unders from GraphQL API
- Stores lines from multiple sportsbooks (DraftKings, Bovada, etc.)
- Updates existing lines or inserts new ones
- Shows coverage summary by provider

**Sample output**:
```
✅ Fetched 45 games
✅ Updated 0 lines, inserted 80 new lines
📊 Sportsbook Coverage:
  DraftKings: 39 games
  Bovada: 39 games
```

**When to update**:
- Before making predictions for games
- Daily during bowl season / playoffs
- When lines move significantly (injury news, weather, etc.)

**View current lines**:
```bash
python -c "import sqlite3; conn = sqlite3.connect('instance/predictions.db'); cursor = conn.cursor(); cursor.execute('SELECT home_team, away_team, provider, spread, over_under FROM sportsbook_lines LIMIT 10'); [print(f\"{row[1]} @ {row[0]}: {row[2]} - Spread {row[3]}, O/U {row[4]}\") for row in cursor.fetchall()]"
```

**How it works**:
1. `betting_lines_manager.py` queries `sportsbook_lines` table first
2. Falls back to `upcoming_games` table if multi-sportsbook data unavailable
3. Finally falls back to GraphQL API or JSON files
4. All sportsbook lines display in Market Analysis section of predictions

---

## Troubleshooting

### App won't start / hangs on startup
1. Check if `betting_lines_manager` is properly using lazy loading (no network calls in `__init__`)
2. Try `app_master.py` instead - it has minimal dependencies
3. Verify database files exist in `instance/` directory
4. Check for stuck processes: `pkill -9 python`

### Ports already in use
```bash
# Kill process on port 5002
lsof -ti :5002 | xargs kill -9

# Kill process on port 5173
lsof -ti :5173 | xargs kill -9

# Kill process on port 5555
lsof -ti :5555 | xargs kill -9
```

### Database connection issues
```bash
# Test database integrity
python -c "import sqlite3; conn = sqlite3.connect('instance/coaches_master.db'); print(f'Tables: {len(conn.execute(\"SELECT name FROM sqlite_master WHERE type=\\\"table\\\"\").fetchall())}')"
```

---

## Startup Sequence

### app.py startup flow:
1. Import Flask & extensions
2. Import `graphqlpredictor` (database helper loads)
3. Import `betting_lines_manager` (lazy init - no network calls)
4. Import `game_media_service`, `batch_rivalry_analyzer`, `espn_player_service`
5. Define routes
6. Wait for requests → data loads on first prediction request

### app_master.py startup flow:
1. Import Flask & extensions
2. Import sqlite3 & templates
3. Define routes
4. Start server immediately
5. Database queries on-demand per request
