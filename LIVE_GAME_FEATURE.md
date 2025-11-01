# Live Game Integration Guide
**GameDay+ Model - Real-Time Game Data Integration**

---

## Overview
This guide explains the backend architecture and data fetching logic for integrating live game data (play-by-play, win probability, field visualization) into the existing GameDay+ prediction UI.

---

## System Architecture

### 1. Core Components

#### **A. Data Fetching Scripts**
Located in: `/GameDay_Plus_Model/`

1. **`week9_current_games_graphql.py`** - Main game discovery
   - Fetches all current week games
   - Filters to FBS games only (53 from 307 total)
   - Gets live scores, rankings, betting lines
   - Output: JSON with game status (in_progress/completed/scheduled)

2. **`live_game_detail_graphql.py`** - Individual game details
   - Fetches detailed single-game data
   - Gets win probability, scores, plays
   - Supports lookup by game ID or team names
   - Output: JSON + formatted console display

3. **`generate_live_game_html.py`** - HTML visualization generator
   - Creates ESPN-style HTML reports
   - Fetches team logos/colors from CFBD API
   - Generates responsive UI with field visualization
   - Output: Standalone HTML file

4. **`live_game_monitor.py`** - Background monitoring service
   - Continuously fetches game data (30-second intervals)
   - Auto-regenerates HTML
   - Runs until manually stopped

---

## Data Sources & APIs

### Primary APIs Used

#### **1. GraphQL API** 
```
Endpoint: https://graphql.collegefootballdata.com/v1/graphql
Auth: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p
```

**What it provides:**
- Game metadata (teams, date, venue)
- Rankings (AP Poll)
- Betting lines (spread, O/U, moneyline)
- Team information (conference, colors)

**Key Queries:**
- `game(where: {season: {_eq: $year}, week: {_eq: $week}})`
- `betting_line(where: {gameId: {_eq: $id}})`
- `team_ranking(where: {season: {_eq: $year}, week: {_eq: $week}})`

#### **2. REST API - Scoreboard**
```
Endpoint: https://api.collegefootballdata.com/scoreboard
Parameters: ?year=2025&week=9&classification=fbs
```

**What it provides:**
- Live scores (real-time points)
- Game status (in_progress/completed/scheduled)
- Current period and clock
- Win probability (live updates)
- Last play description
- Current situation (down, distance, field position)
- Possession indicator

**Response Structure:**
```json
{
  "id": 401754571,
  "status": "in_progress",
  "period": 4,
  "clock": "02:22",
  "situation": "4th & 2 at SYR 33",
  "possession": "away",
  "lastPlay": "(03:05) No Huddle-Shotgun #10 R.Collins...",
  "homeTeam": {
    "points": 41,
    "lineScores": [3, 17, 14, 7],
    "winProbability": 0.925
  },
  "awayTeam": {
    "points": 16,
    "lineScores": [3, 0, 7, 6],
    "winProbability": 0.075
  }
}
```

#### **3. REST API - Live Plays**
```
Endpoint: https://api.collegefootballdata.com/live/plays
Parameters: ?gameId=401754571
```

**What it provides:**
- Play-by-play data (all drives)
- Team statistics (EPA, success rate, etc.)
- Individual play details:
  - Quarter, clock, down/distance
  - Team possession
  - Yard line, yards gained
  - Play type, play text
  - Score at time of play
  - EPA, success indicator

**Response Structure:**
```json
{
  "id": 401754571,
  "drives": [
    {
      "offense": "Georgia Tech",
      "plays": [
        {
          "id": "4017545713",
          "period": 1,
          "clock": "15:00",
          "team": "Syracuse",
          "teamId": 183,
          "down": 1,
          "distance": 10,
          "yardsToGoal": 65,
          "yardsGained": 0,
          "playType": "Kickoff",
          "playText": "(15:00) #98 J.Oh kickoff...",
          "homeScore": 0,
          "awayScore": 0
        }
      ]
    }
  ]
}
```

#### **4. REST API - Team Data**
```
Endpoint: https://api.collegefootballdata.com/teams/fbs
Parameters: ?year=2025
```

**What it provides:**
- Official team colors (primary, alternate)
- Team logos (ESPN CDN URLs)
- Team abbreviations
- Conference affiliation

---

## Critical Schema Discoveries

### Fields NOT Available (Removed from queries):
- `completed` - Not in GraphQL game schema
- `status` - Not in GraphQL game schema  
- `color`, `altColor`, `mascot` - Not in GraphQL team schema

### Correct Field Names:
- Live scores: `scoreboard_entry['homeTeam']['points']` (nested, not flat)
- Plays: `play.get('team')` not `play.get('offense')`
- Yards: `play.get('yardsGained')` not `play.get('yards')`
- Yard line: `play.get('yardsToGoal')` not `play.get('yardLine')`

### Type Safety:
- Betting line spreads: Must convert to float with try/except
- Win probability: Can be `None` for completed games (default to 50%)

---

## Integration Logic for GameDay+ UI

### Step 1: Detect Live Game
**When user selects a matchup in your UI:**

```python
# Check if game is currently live
def is_game_live(home_team, away_team, week=9, year=2025):
    """
    Query scoreboard API to check game status
    """
    url = f"https://api.collegefootballdata.com/scoreboard?year={year}&week={week}&classification=fbs"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        games = response.json()
        for game in games:
            home_match = home_team in game['homeTeam']['name']
            away_match = away_team in game['awayTeam']['name']
            
            if home_match and away_match:
                return {
                    'is_live': game['status'] == 'in_progress',
                    'game_id': game['id'],
                    'status': game['status']
                }
    
    return {'is_live': False}
```

### Step 2: Fetch Live Data
**If game is live, fetch real-time data:**

```python
def get_live_game_data(game_id):
    """
    Fetch live scoreboard + plays data
    """
    # Get scoreboard (win prob, scores, status)
    scoreboard_url = f"https://api.collegefootballdata.com/scoreboard"
    params = {'year': 2025, 'week': 9, 'classification': 'fbs'}
    scoreboard_data = requests.get(scoreboard_url, headers=headers, params=params).json()
    
    game = next((g for g in scoreboard_data if g['id'] == game_id), None)
    
    # Get play-by-play
    plays_url = f"https://api.collegefootballdata.com/live/plays?gameId={game_id}"
    plays_data = requests.get(plays_url, headers=headers).json()
    
    return {
        'win_probability': {
            'home': game['homeTeam']['winProbability'],
            'away': game['awayTeam']['winProbability']
        },
        'score': {
            'home': game['homeTeam']['points'],
            'away': game['awayTeam']['points']
        },
        'status': {
            'period': game['period'],
            'clock': game['clock'],
            'situation': game['situation'],
            'possession': game['possession']
        },
        'plays': plays_data['drives'],  # All drives with plays
        'team_stats': plays_data['teams']  # Live team statistics
    }
```

### Step 3: Process Plays Data
**Extract recent plays for UI display:**

```python
def process_plays(plays_data, limit=100):
    """
    Process drives into flat play list, sorted by recency
    """
    all_plays = []
    
    for drive in plays_data.get('drives', []):
        for play in drive.get('plays', []):
            all_plays.append({
                'quarter': play.get('period'),
                'clock': play.get('clock'),
                'team': play.get('team'),  # Not 'offense'!
                'down': play.get('down'),
                'distance': play.get('distance'),
                'yardLine': play.get('yardsToGoal'),  # Not 'yardLine'!
                'yards': play.get('yardsGained'),  # Not 'yards'!
                'playType': play.get('playType'),
                'playText': play.get('playText'),
                'homeScore': play.get('homeScore'),
                'awayScore': play.get('awayScore'),
                'epa': play.get('epa'),
                'success': play.get('success')
            })
    
    # Sort by timestamp (most recent first)
    all_plays.sort(key=lambda p: p.get('wallClock', ''), reverse=True)
    
    return all_plays[:limit]
```

### Step 4: Calculate Field Position
**For field visualization:**

```python
def calculate_field_position(situation, possession):
    """
    Parse situation string to get ball position
    Example: "1st & 10 at SYR 25" -> 25 yards from SYR endzone
    """
    import re
    match = re.search(r'at (\w+) (\d+)', situation)
    
    if match:
        team_abbr = match.group(1)
        yard_line = int(match.group(2))
        
        # Convert to 0-100 field position
        if possession == 'away':
            field_position = yard_line
        else:
            field_position = 100 - yard_line
        
        return {
            'position': field_position,
            'yard_line': yard_line,
            'team': team_abbr
        }
    
    return None
```

---

## UI Integration Points

### Where to Add Live Data in Your UI

#### **1. Win Probability Chart**
**Location:** Below "Win Probability" section (currently shows static model prediction)

**Data to display:**
```javascript
{
  live_win_prob: {
    home: 0.515,  // 51.5%
    away: 0.485,  // 48.5%
    updated_at: "Q1 - 12:13"
  }
}
```

**Implementation:**
- Add live indicator badge next to static prediction
- Show "LIVE: 51.5%" vs "Model: 60.6%"
- Update every 30 seconds via polling or WebSocket

#### **2. Field Visualization**
**Location:** New section between "Win Probability" and "Predicted Spread"

**Data needed:**
```javascript
{
  field: {
    possession_team: "BYU",
    possession_logo: "http://a.espncdn.com/i/teamlogos/ncaa/500/252.png",
    yard_line: 33,
    down: "2nd",
    distance: 9,
    quarter: "Q1",
    clock: "12:13"
  }
}
```

**Visual elements:**
- Green striped field (280px height)
- Team logos in endzones with team colors
- Animated ball position with team logo
- Drive stats below (down/distance, ball position, possession)

#### **3. Play-by-Play Feed**
**Location:** Expandable section or sidebar panel

**Data structure:**
```javascript
{
  plays: [
    {
      quarter: "Q1",
      clock: "14:38",
      team: "BYU",
      situation: "1 & 10 at 68",
      description: "Shotgun #4 L.Martin rush middle for 1 yard",
      yards: 1,
      score: "0-7"
    }
    // ... up to 100 plays
  ]
}
```

**UI features:**
- Scrollable list with latest plays at top
- Color-coded by team
- Hover effects
- Score indicators
- EPA/success badges (optional)

#### **4. Live Score Updates**
**Location:** Header matchup display

**Data to replace:**
```javascript
// Instead of predicted scores:
{
  home_score: 7,  // Live actual score
  away_score: 7,  // Live actual score
  status: "Q1 - 12:13",
  is_live: true
}
```

---

## Auto-Refresh Strategy

### Option 1: Polling (Recommended)
**Simple, reliable, works everywhere**

```javascript
// In your React/Vue component
let liveDataInterval = null;

function startLiveUpdates(gameId) {
  liveDataInterval = setInterval(async () => {
    const data = await fetchLiveGameData(gameId);
    updateUI(data);
  }, 30000);  // 30 seconds
}

function stopLiveUpdates() {
  if (liveDataInterval) {
    clearInterval(liveDataInterval);
  }
}
```

### Option 2: Meta Refresh (Simplest)
**Already implemented in HTML generator**

```html
<meta http-equiv="refresh" content="30">
```

### Option 3: WebSocket (Advanced)
**Real-time, efficient, complex setup**

---

## Backend Service Architecture

### Recommended Flow:

```
1. User selects matchup in UI
   ↓
2. Check if game is live (scoreboard API)
   ↓
3a. If NOT live:
    → Show static model predictions only
   
3b. If LIVE:
    → Fetch live data (scoreboard + plays)
    → Start auto-refresh interval
    → Display live UI components
   ↓
4. Every 30 seconds:
   → Re-fetch scoreboard data
   → Re-fetch plays data (incremental)
   → Update UI components
   ↓
5. When game completes:
   → Stop auto-refresh
   → Show final score
   → Keep play-by-play history
```

---

## Key Implementation Notes

### 1. **Team Name Matching**
**Problem:** API uses full names like "Iowa State Cyclones", UI might use "Iowa State"

**Solution:**
```python
def match_team(ui_team_name, api_teams):
    """
    Fuzzy match team names with length-based scoring
    Prioritizes longer matches to avoid "Iowa" matching "Iowa State"
    """
    best_match = None
    best_score = 0
    
    for team in api_teams:
        school = team['school'].lower()
        ui_name = ui_team_name.lower()
        
        # Exact match
        if school == ui_name:
            return team
        
        # Substring match with length scoring
        if school in ui_name:
            score = len(school)
        elif ui_name in school:
            score = len(ui_name)
        else:
            score = 0
        
        if score > best_score:
            best_score = score
            best_match = team
    
    return best_match
```

### 2. **Error Handling**
**Always handle None values:**

```python
# Win probability can be None for completed games
wp = game['homeTeam'].get('winProbability')
win_prob = (wp * 100) if wp is not None else 50.0

# Yards can be None
yards = play.get('yardsGained')
yards_str = f"({'+' if yards > 0 else ''}{yards})" if yards is not None else ""
```

### 3. **Rate Limiting**
**CFBD API limits:**
- 30 seconds minimum between requests
- Use caching for team data (colors/logos)
- Batch requests when possible

### 4. **Data Caching**
**Cache static data to reduce API calls:**

```python
class LiveGameFetcher:
    def __init__(self):
        self.team_data_cache = {}  # Cache team logos/colors
        self.last_fetch = None
        self.min_interval = 30  # seconds
    
    def should_fetch(self):
        if not self.last_fetch:
            return True
        elapsed = time.time() - self.last_fetch
        return elapsed >= self.min_interval
```

---

## Files to Reference

### Core Implementation Files:
1. `live_game_detail_graphql.py` - Lines 220-300 (process_game function)
2. `generate_live_game_html.py` - Lines 30-70 (get_team_data function)
3. `week9_current_games_graphql.py` - Lines 140-200 (get_live_scores function)
4. `live_game_monitor.py` - Lines 15-90 (monitor_game function)

### Key Functions to Extract:

```python
# From live_game_detail_graphql.py
- get_scoreboard_data(game_id)  # Win prob, scores
- get_live_plays(game_id)       # Play-by-play
- process_game(game_id)          # Combines all data

# From generate_live_game_html.py
- get_team_data(team_name)       # Logos, colors
- _calculate_field_position()    # Field viz math
- _generate_plays_html()         # Play formatting
```

---

## Testing & Validation

### Test Live Integration:
```bash
# 1. Find a live game
python week9_current_games_graphql.py | grep "in_progress"

# 2. Get game details
python live_game_detail_graphql.py --game-id 401756931

# 3. Generate HTML (for UI reference)
python generate_live_game_html.py live_game_401756931_*.json

# 4. Start monitor (test auto-refresh)
python live_game_monitor.py --game-id 401756931
```

### Validation Checklist:
- [ ] Game status detection works (in_progress vs scheduled)
- [ ] Win probability updates every 30s
- [ ] Plays appear in correct order (most recent first)
- [ ] Team logos/colors match correctly
- [ ] Field position calculates accurately
- [ ] Scores update in real-time
- [ ] Auto-refresh doesn't cause memory leaks
- [ ] Error handling for completed games
- [ ] Graceful degradation when API unavailable

---

## Performance Considerations

### Optimization Tips:

1. **Debounce UI updates** - Don't re-render on every data fetch
2. **Virtualize play list** - Only render visible plays (use react-window)
3. **Lazy load team logos** - Use CDN caching
4. **Compress API responses** - Enable gzip
5. **Use service worker** - Cache team data offline
6. **Batch state updates** - Single React state update per fetch
7. **Memoize calculations** - Cache field position math

---

## Security Notes

### API Key Management:
```python
# DO NOT hardcode in frontend
API_KEY = os.getenv('CFBD_API_KEY')

# Use backend proxy
# Frontend → Your Server → CFBD API
```

### Rate Limit Protection:
```python
import time
from functools import wraps

def rate_limit(min_interval=30):
    def decorator(func):
        last_called = [0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator
```

---

## Summary Checklist for AI Agent

**To integrate live game data into GameDay+ UI:**

✅ **Data Fetching:**
- [ ] Implement `is_game_live()` check on matchup selection
- [ ] Fetch scoreboard data for win prob + scores
- [ ] Fetch plays data for play-by-play
- [ ] Handle team name matching with fuzzy logic
- [ ] Cache team logos/colors to reduce API calls

✅ **UI Components:**
- [ ] Add "LIVE" indicator to win probability section
- [ ] Create field visualization component (280px height)
- [ ] Build play-by-play feed (scrollable, 100 plays)
- [ ] Update score displays with live data
- [ ] Add quarter/clock status indicator

✅ **Auto-Refresh:**
- [ ] Implement 30-second polling interval
- [ ] Stop updates when game completes
- [ ] Show loading states during fetches
- [ ] Handle API errors gracefully

✅ **Data Processing:**
- [ ] Parse plays into UI-friendly format
- [ ] Calculate field position from situation string
- [ ] Handle None values (win prob, yards, etc.)
- [ ] Sort plays by recency (most recent first)

✅ **Performance:**
- [ ] Debounce UI updates
- [ ] Virtualize long play lists
- [ ] Use React.memo/useMemo for expensive calculations
- [ ] Lazy load team logos

✅ **Testing:**
- [ ] Test with live game during actual gameplay
- [ ] Verify data accuracy against ESPN
- [ ] Check auto-refresh memory usage
- [ ] Test completed game handling

---

**Next Steps:**
1. Extract backend logic from reference files
2. Create API service layer in your app
3. Build UI components for live sections
4. Implement polling/refresh strategy
5. Test during live game week
6. Add error boundaries and fallbacks

**Reference Implementation:** All working code is in `/GameDay_Plus_Model/` directory with fully functional examples.