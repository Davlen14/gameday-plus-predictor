# TODO: Add Coach & NIL API Routes to app.py

## Problem
The gamedaylive.html template has navigation links to `/coaches`, `/teams`, `/nil`, and `/master-dashboard`, but app.py (deployed to Railway) is missing the API endpoints that these templates need to fetch data.

Currently:
- ✅ Template routes exist in app.py (`/coaches`, `/nil`, etc.)
- ❌ API routes missing from app.py (they're only in app_master.py)
- Result: Pages load but show no data

## Required Database Setup

### Add Database Connection Helper (from app_master.py)
Add to top of app.py after imports:

```python
# Database path for coaches/NIL data
COACHES_DB_PATH = 'instance/coaches_master.db'

def get_coaches_db_connection():
    """Get database connection for coaches_master.db with row factory"""
    conn = sqlite3.connect(COACHES_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    """Convert sqlite Row to dict"""
    return dict(row) if row else None

def rows_to_list(rows):
    """Convert list of rows to list of dicts"""
    return [dict(row) for row in rows]
```

**Important**: Use `get_coaches_db_connection()` for these routes to avoid conflicts with existing `predictions.db` connections in app.py.

## API Routes to Copy from app_master.py

### Core Coach APIs (lines 220-700 in app_master.py)
Copy these routes and update database calls to use `get_coaches_db_connection()`:

1. **`GET /api/coaches`** - List all coaches with rankings count
2. **`GET /api/coach/<int:coach_id>`** - Coach details with stint/game counts
3. **`GET /api/coach/<int:coach_id>/stints`** - Coaching history
4. **`GET /api/coach/<int:coach_id>/games`** - Game-by-game history
5. **`GET /api/coach/<int:coach_id>/rankings`** - AP Poll rankings
6. **`GET /api/coach/<int:coach_id>/draft_picks`** - NFL draft picks
7. **`GET /api/coach/<int:coach_id>/situational_stats`** - Situational statistics
8. **`GET /api/coach/<int:coach_id>/vs_coaches`** - Head-to-head records
9. **`GET /api/coach/<int:coach_id>/season_analytics`** - Season analytics
10. **`GET /api/coach/<int:coach_id>/recruiting_classes`** - Recruiting data
11. **`GET /api/coach/<int:coach_id>/talent_composite`** - Talent ratings
12. **`GET /api/coach/<int:coach_id>/transfer_portal`** - Portal data
13. **`GET /api/coach/<int:coach_id>/timeline`** - Career timeline (Highcharts data)
14. **`GET /api/search?q=<query>`** - Search coaches by name/school

### Teams API (already exists, verify compatibility)
- **`GET /api/teams`** - app.py has this at line 2312, but verify it returns correct format
- **`GET /api/team/<int:team_id>`** - Add if missing (lines 286-330 in app_master.py)
- **`GET /api/team/<int:team_id>/roster`** - Add roster endpoint (lines 332-383)

### NIL APIs (lines 731-900 in app_master.py)
1. **`GET /api/nil/teams`** - All teams with NIL valuations
2. **`GET /api/nil/team/<int:team_id>`** - Single team NIL summary
3. **`GET /api/nil/team/<int:team_id>/players`** - Team's NIL players
4. **`GET /api/nil/team/<int:team_id>/positions`** - Position group analytics

### Additional Utility Routes
- **`GET /fbs.json`** - FBS teams data (line 213 in app_master.py)
- **`GET /api/stats`** - General statistics (line 905)

## Implementation Steps

### Step 1: Add Database Helpers
Add helper functions to app.py right after the Flask app initialization (around line 20).

### Step 2: Copy API Routes
Insert routes before the `/predictor` routes (around line 3240 in app.py) in this order:
1. Helper routes (`/fbs.json`, `/api/stats`)
2. Coach APIs
3. Team APIs (verify/enhance existing)
4. NIL APIs

### Step 3: Update Database Calls
**Critical**: In each copied function, change:
```python
# OLD (app_master.py):
conn = get_db_connection()

# NEW (app.py):
conn = get_coaches_db_connection()
```

This prevents conflicts with predictions database connections.

### Step 4: Verify Imports
Ensure these are imported at top of app.py:
```python
import sqlite3
from pathlib import Path
```

### Step 5: Test Endpoints
After deployment, verify each endpoint:
```bash
curl https://graphqlmodel-production.up.railway.app/api/coaches
curl https://graphqlmodel-production.up.railway.app/api/nil/teams
curl https://graphqlmodel-production.up.railway.app/api/search?q=saban
```

## Files Involved
- **Source**: `app_master.py` (lines 40-900) - Copy from here
- **Target**: `app.py` (insert around line 3240) - Add to here
- **Database**: `instance/coaches_master.db` - Must exist in Docker container

## Docker Consideration
Verify `Dockerfile` includes:
```dockerfile
COPY . .
```
This ensures `instance/coaches_master.db` is copied to the container.

## Estimated Scope
- ~700 lines of code to copy
- ~30 API routes total
- 3 helper functions
- Minimal modifications needed (just database connection function names)

## Success Criteria
1. All gamedaylive navigation links work
2. `/coaches` page loads coach list with data
3. `/coach/<id>` pages display full profile with charts
4. `/nil` page shows NIL team rankings
5. `/master-dashboard` displays comprehensive data
6. No 404 or 500 errors on any template page

## Priority
**HIGH** - Templates are deployed but non-functional without these APIs.

---

**Note**: Do NOT merge app_master.py into app.py entirely. Only copy the API routes and helpers. Keep template-serving routes separate as they already exist in app.py.
