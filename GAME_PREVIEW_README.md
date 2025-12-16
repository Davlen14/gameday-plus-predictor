# Game Preview Feature - Setup & Usage Guide

## Overview
Full game preview experience with comprehensive data from coaches_master.db including matchup analysis, coaching profiles, form, head-to-head records, season analytics, rankings, talent pipeline, and more.

---

## ✅ Setup Complete

### Data Backfill ✓
- **Opponent logos**: 100% populated (12,950/12,951 games)
- **Head-to-head records**: 3,777 coach matchups populated in `vs_coaches` table

### API Endpoints ✓
- **`GET /api/game-preview/<game_id>`** - Full JSON payload with all preview data
- **`GET /game-preview/<game_id>`** - Rendered HTML page
- Supports both internal game IDs and ESPN game IDs

### Template Updates ✓
- Server-side data injection via `game_data` context variable
- JavaScript receives data as `SERVER_GAME_DATA` constant

---

## 🚀 Quick Start

### 1. Run Data Backfill (One-Time Setup)
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
source .venv/bin/activate
python backfill_game_data.py
```

**What it does:**
- Populates missing `opponent_logo` in games table (from teams table)
- Derives head-to-head coaching records from game history
- Creates `vs_coaches` entries for all coach matchups

**Output:**
```
📊 Current games table statistics:
   Total games:       12,951
   Has opponent_logo: 12,950 (100.0%)
   
📊 vs_coaches table: 3,777 records
✅ All done!
```

### 2. Start the Server
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
source .venv/bin/activate
python app_master.py
```

**Server runs on:** `http://localhost:5555`

### 3. Access Game Previews

**Via Web UI:**
- Navigate to: `http://localhost:5555/game-preview/<game_id>`
- Example: `http://localhost:5555/game-preview/401628455`

**Via API:**
```bash
# Get full JSON payload
curl http://localhost:5555/api/game-preview/401628455 | python -m json.tool
```

---

## 📊 Data Payload Structure

The `/api/game-preview/<game_id>` endpoint returns:

```json
{
  "success": true,
  "data": {
    "game": { /* Base game data */ },
    "opponent_game": { /* Opponent's perspective */ },
    "matchup": {
      "home_team": "Ohio State",
      "away_team": "Akron",
      "is_neutral": false,
      "is_conference": false,
      "is_signature": false,
      "excitement_index": 4.2,
      "season": 2024,
      "week": 1
    },
    "teams": {
      "home": { "school", "logo", "color", "alt_color", "mascot" },
      "away": { "school", "logo", "color", "alt_color", "mascot" }
    },
    "coaches": {
      "home_coach": {
        "name": "Ryan Day",
        "current_stint": { "record", "win_pct", "games_coached" },
        "last_10_games": [ /* Recent results */ ]
      },
      "away_coach": { /* Same structure */ }
    },
    "head_to_head": {
      "wins": 3,
      "losses": 1,
      "record": "3-1",
      "avg_point_differential": 18.5,
      "biggest_win_margin": 42,
      "last_meeting_year": 2023
    },
    "form": {
      "last_5_overall": [ /* Recent games */ ],
      "last_5_vs_opponent": [ /* H2H games */ ]
    },
    "season_analytics": {
      "primary": { /* Offensive/defensive stats */ },
      "opponent": { /* Same structure */ }
    },
    "situational_stats": {
      "primary": { /* Red zone, 3rd down, vs ranked, etc. */ },
      "opponent": { /* Same structure */ }
    },
    "rankings": {
      "primary_trend": [ /* Last 4 weeks AP/Coaches */ ],
      "opponent_trend": [ /* Same structure */ ]
    },
    "talent": {
      "primary": { "talent_rating", "talent_rank", "year" },
      "opponent": { /* Same structure */ }
    },
    "recruiting": {
      "primary": [ /* Last 2 recruiting classes */ ],
      "opponent": [ /* Same structure */ ]
    },
    "portal": {
      "primary": { "transfers_in", "transfers_out", "net_transfers" },
      "opponent": { /* Same structure */ }
    },
    "signature_wins": [ /* Notable wins this season */ ]
  }
}
```

---

## 🎨 Frontend Integration

### Server-Side Data Injection
The template receives data via Flask context:

```python
# app_master.py
@app.route('/game-preview/<int:game_id>')
def game_preview_by_id(game_id):
    preview_data = get_game_preview_data(game_id)
    return render_template('game_detail_upcoming.html', 
                         game_data=preview_data,
                         game_id=game_id)
```

### JavaScript Access
```javascript
// templates/game_detail_upcoming.html
const SERVER_GAME_DATA = {{ game_data | tojson | safe }};
let gameData = SERVER_GAME_DATA;

// Now use gameData throughout the script
console.log('Home team:', gameData.teams.home.school);
console.log('Coaches:', gameData.coaches);
```

---

## 🔧 Troubleshooting

### Game Not Found Error
```json
{"error": "Game not found", "success": false}
```

**Solution:** The API supports both internal IDs and ESPN game IDs. Make sure the game exists in the database:

```bash
# Check if game exists
sqlite3 instance/coaches_master.db "SELECT id, espn_game_id, school, opponent FROM games WHERE espn_game_id = '401628455'"
```

### Missing Opponent Data
If opponent logos or analytics are missing:
```bash
# Re-run backfill
python backfill_game_data.py
```

### Server Not Starting
```bash
# Check for port conflicts
lsof -ti :5555 | xargs kill -9

# Restart
python app_master.py
```

---

## 📝 UI Sections to Implement

The template now has access to all this data. Implement these sections:

1. **Matchup Snapshot** - Records, points for/against, excitement index
2. **Form Cards** - Last 5 games overall and vs opponent
3. **Head-to-Head** - Coaching record, margins, last meeting
4. **Coaching Profiles** - Career record, current stint, last 10 games
5. **Situational Edges** - Red zone %, 3rd down, 2-minute drill
6. **Season Analytics** - Offensive/defensive efficiency comparison
7. **Rankings Momentum** - Last 4 weeks AP trend
8. **Talent Pipeline** - Talent composite, recruiting classes, portal
9. **Signature Wins** - Best wins this season
10. **Model Lean** - Projected spread from SP+/FPI

---

## 🗄️ Database Tables Used

- `games` - Main game records with opponent data
- `coaches` - Coach biographical info
- `teams` - Team logos, colors, mascots
- `stints` - Coaching tenure records
- `vs_coaches` - Head-to-head coaching records (derived)
- `season_analytics` - Offensive/defensive season stats
- `situational_stats` - Situational performance (red zone, vs ranked, etc.)
- `rankings` - AP/Coaches poll history
- `talent_composite` - Team talent ratings by year
- `recruiting_classes` - Recruiting class rankings
- `transfer_portal` - Transfer portal activity

---

## 🎯 Game ID Sources

### From Game Slider
The game slider uses **ESPN game IDs** (e.g., `401778303`, `401628455`). These are automatically handled by the API.

### Finding Game IDs
```bash
# Recent games with ESPN IDs
sqlite3 instance/coaches_master.db "SELECT id, espn_game_id, school, opponent, season, week FROM games WHERE espn_game_id IS NOT NULL LIMIT 10"

# Games by team
sqlite3 instance/coaches_master.db "SELECT id, espn_game_id, school, opponent FROM games WHERE school = 'Ohio State' AND season = 2024 LIMIT 5"
```

---

## ✨ Next Steps

1. **Wire up template sections** - Use `gameData` object to populate UI components
2. **Add loading states** - Show skeleton loaders while data loads
3. **Implement comparisons** - Side-by-side stat bars, radar charts
4. **Add SP+/FPI data** - Extend backfill script to fetch from CFBD API
5. **Style team colors** - Use `teams.home.color` and `teams.away.color` for dynamic theming

---

## 📞 Support

- **Backfill script**: `backfill_game_data.py`
- **API endpoint**: Line 1397 in `app_master.py`
- **Template**: `templates/game_detail_upcoming.html`
- **Server**: Runs on port 5555 (see `.github/copilot-instructions.md`)

**Test endpoint:**
```bash
curl http://localhost:5555/api/game-preview/401628455 | python -m json.tool | head -50
```

✅ **Feature is complete and ready for frontend implementation!**
