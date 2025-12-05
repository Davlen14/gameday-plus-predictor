# 📊 GraphQL Migration Guide - Gameday+ Data Architecture

**Last Updated**: December 2, 2025  
**Current API**: College Football Data GraphQL API (`https://graphql.collegefootballdata.com/v1/graphql`)

---

## 🎯 Overview

The Gameday+ prediction system has progressively moved from static JSON files to live GraphQL API calls. This document tracks:
- What data is now fetched from GraphQL
- What still uses cached JSON files
- How to handle both data formats
- Migration patterns for future updates

---

## 📡 Data Sources Migrated to GraphQL

### **PRIMARY QUERY: `GamePredictorEnhanced`**
Location: `graphqlpredictor.py` (lines 2670-2840)

This single massive query fetches **18 different data points** in one API call:

#### 1. **Team Performance Metrics** (`adjustedTeamMetrics`)
```graphql
homeTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $homeTeamId}})
awayTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $awayTeamId}})
```
**Fields Fetched**:
- `epa`, `epaAllowed` - Expected Points Added
- `explosiveness`, `explosivenessAllowed` - Big play metrics
- `success`, `successAllowed` - Play success rates
- `passingEpa`, `passingEpaAllowed` - Pass-specific EPA
- `rushingEpa`, `rushingEpaAllowed` - Rush-specific EPA
- `passingDownsSuccess`, `passingDownsSuccessAllowed` - 3rd down passing
- `standardDownsSuccess`, `standardDownsSuccessAllowed` - 1st/2nd down
- `lineYards`, `lineYardsAllowed` - Yards at line of scrimmage
- `secondLevelYards`, `secondLevelYardsAllowed` - 5-10 yards downfield
- `openFieldYards`, `openFieldYardsAllowed` - 10+ yards downfield
- `highlightYards`, `highlightYardsAllowed` - Explosive plays (50+ yards)

**JSON Equivalent**: Previously in `team_stats.json`, `epa_data.json`

---

#### 2. **Player Metrics** (`adjustedPlayerMetrics`)
```graphql
allPlayers: adjustedPlayerMetrics(
    where: {year: {_eq: $currentYear}},
    orderBy: {metricValue: DESC},
    limit: 100
)
```
**Fields Fetched**:
- `athleteId` - Player unique identifier
- `metricType` - Type of stat (passing, rushing, receiving, defense)
- `metricValue` - Statistical value

**Used For**:
- QB efficiency scores
- WR/RB impact analysis
- Defensive player ratings
- Individual matchup advantages

**JSON Equivalent**: `fbs_top_players_2025.json`, `comprehensive_qb_analysis_2025.json`

---

#### 3. **Talent Ratings** (`teamTalent`)
```graphql
homeTeamTalent: teamTalent(where: {team: {teamId: {_eq: $homeTeamId}}})
awayTeamTalent: teamTalent(where: {team: {teamId: {_eq: $awayTeamId}}})
```
**Fields Fetched**:
- `talent` - Composite recruiting/roster talent score

**Used For**: 
- Talent gap calculations
- Recruiting advantage analysis
- Roster strength comparison

**JSON Equivalent**: `talent_ratings.json` (deprecated)

---

#### 4. **Season Game Results** (`game`)
```graphql
homeSeasonGames: game(
    where: {
        _or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}],
        season: {_eq: $currentYear}
    },
    orderBy: {week: ASC}
)
```
**Fields Fetched**:
- `id`, `season`, `week`, `seasonType`
- `homeTeam`, `awayTeam`
- `homePoints`, `awayPoints`
- `homeWinProb`, `awayWinProb`
- `startDate`

**Used For**:
- Win/loss records
- Scoring trends
- Opponent strength analysis
- Recent form calculations

**JSON Equivalent**: `all_fbs_teams_schedules_2025.json`

---

#### 5. **Recent Game Performance** (`game` with limit)
```graphql
homeRecentGames: game(
    where: {...},
    orderBy: {startDate: DESC},
    limit: 4
)
```
**Fields**: Same as season games, but only last 4 games

**Used For**:
- Hot/cold streak detection
- Recent form weighting (Dixon-Coles temporal)
- Momentum calculations

---

#### 6. **Team Information** (`currentTeams`)
```graphql
homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}})
awayTeam: currentTeams(where: {teamId: {_eq: $awayTeamId}})
```
**Fields Fetched**:
- `id`, `school` - Team identifiers
- `mascot`, `abbreviation` - Display names
- `conference`, `division` - Conference info
- `color`, `altColor` - Team colors for UI
- `logos` - Array of logo URLs

**JSON Equivalent**: `fbs.json` (still used for team selection in frontend)

---

#### 7. **ELO & FPI Ratings** (`ratings`)
```graphql
homeRatings: ratings(
    where: {
        teamId: {_eq: $homeTeamId},
        year: {_eq: $currentYear}
    },
    orderBy: {week: DESC},
    limit: 1
)
```
**Fields Fetched**:
- `elo` - ELO rating
- `fpi` - Football Power Index
- `year`, `week` - When rating was calculated

**Used For**:
- Composite rating calculations
- Historical strength comparison
- Win probability baselines

**JSON Equivalent**: `all_fbs_ratings_comprehensive_2025.json` (still loaded for offline mode)

---

#### 8. **Current Game Metadata** (`game` - specific matchup)
```graphql
currentGame: game(
    where: {
        homeTeamId: {_eq: $homeTeamId},
        awayTeamId: {_eq: $awayTeamId},
        season: {_eq: $currentYear},
        week: {_eq: $currentWeek}
    }
)
```
**Fields Fetched**:
- `id` - Game ID for subsequent queries
- `startDate` - Kickoff time
- `homePoints`, `awayPoints` - Final score (if played)
- `excitementIndex` - Game excitement rating

**Used For**:
- Getting game ID for lines/media queries
- Checking if game already played
- Scheduling information

---

#### 9. **Weather Data** (`gameWeather`)
```graphql
gameWeather: gameWeather(
    where: {
        gameId: {_eq: $gameId}
    }
)
```
**Fields Fetched**:
- `temperature` - Degrees Fahrenheit
- `windSpeed` - MPH
- `precipitation` - Inches
- `humidity` - Percentage

**Used For**:
- Weather impact on total score
- Passing game penalties
- Field condition adjustments

**JSON Equivalent**: `Currentweekgames.json` (has weather data for Week 14)

**⚠️ CURRENT ISSUE**: GraphQL weather data shows static values in some cases (fallback to 67.3°F, 3.4 mph)

---

#### 10. **AP Poll Rankings** (`pollRank`)
```graphql
currentPolls: pollRank(
    where: {
        season: {_eq: $currentYear},
        week: {_eq: $currentWeek}
    },
    orderBy: {rank: ASC}
)
```
**Fields Fetched**:
- `rank` - AP Poll position
- `school` - Team name
- `points` - Poll points
- `firstPlaceVotes` - #1 votes received

**Used For**:
- Ranked matchup detection
- Poll momentum calculations
- Public perception metrics

**JSON Equivalent**: `week15_polls_raw.json`

---

#### 11. **Calendar/Bye Weeks** (`calendar`)
```graphql
weeklyCalendar: calendar(
    where: {
        season: {_eq: $currentYear}
    }
)
```
**Fields Fetched**:
- `season`, `week`
- `seasonType` (regular, postseason)
- `firstGameStart`, `lastGameStart`

**Used For**:
- Bye week tracking
- Rest advantage calculations
- Season progression context

---

### **SECONDARY QUERIES**

#### 12. **Betting Lines** (`gameLines`)
Location: `graphqlpredictor.py` `_fetch_game_lines()` method

```graphql
query GameLines($gameId: Int!) {
    gameLines(where: {gameId: {_eq: $gameId}}) {
        gameId
        spread
        spreadOpen
        overUnder
        overUnderOpen
        moneylineHome
        moneylineAway
        provider { name }
    }
}
```

**⚠️ CRITICAL FINDING**: This query exists but **returns no data** for Week 15 games!

**Alternative Source**: `betting_lines_manager.py` uses a different query:
```graphql
query {
  game(where: {season: {_eq: 2025}, week: {_eq: 15}}) {
    id
    homeTeam
    awayTeam
    lines {
      provider { name }
      spread
      overUnder
    }
  }
}
```

**Data Returned**:
- ✅ `spread` - Point spread (e.g., 2.5)
- ✅ `overUnder` - Total points line (e.g., 47.5)
- ✅ `provider.name` - Sportsbook name
- ❌ `moneylineHome` - NOT INCLUDED (shows N/A)
- ❌ `moneylineAway` - NOT INCLUDED (shows N/A)
- ❌ `spreadOpen` - NOT INCLUDED
- ❌ `overUnderOpen` - NOT INCLUDED

**JSON Fallback**: `Currentweekgames.json` has complete betting data including moneylines

---

#### 13. **Game Media/Network** (`game.mediaInfo`)
Location: `graphqlpredictor.py` `_fetch_game_media()` method

```graphql
query GameMedia($gameId: Int!) {
    game(where: {id: {_eq: $gameId}}) {
        id
        homeTeam
        awayTeam
        startDate
        mediaInfo {
            mediaType
            name
        }
    }
}
```

**Fields Fetched**:
- `mediaType` - "TV", "radio", "web", etc.
- `name` - Network name (ESPN, FOX, CBS, etc.)

**Used For**:
- Displaying broadcast network
- Prime time detection
- Media exposure metrics

**JSON Equivalent**: `Currentweekgames.json` has `media.network` field

---

## 🔄 Hybrid Data Sources (GraphQL + JSON)

### **What Still Uses JSON Files**

#### 1. **Team Selection** (`fbs.json`)
```json
{
  "id": 127,
  "school": "Alabama",
  "mascot": "Crimson Tide",
  "abbreviation": "ALA",
  "alt_name_1": "Bama",
  "alt_name_2": "UA",
  "conference": "SEC",
  "division": "West",
  "color": "#9E1B32",
  "alt_color": "#FFFFFF",
  "logo_url": "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png",
  "logos": ["https://..."]
}
```

**Why**: Frontend needs this immediately on load, before any API calls. Used in:
- `frontend/src/services/teamService.js`
- `frontend/src/components/figma/TeamSelector.tsx`

**GraphQL Alternative**: `currentTeams` table, but requires loading all 130+ teams

---

#### 2. **Coaching Data** (`data/coaches_with_vsranked_stats.json`)
```json
{
  "Alabama": {
    "name": "Kalen DeBoer",
    "school": "Alabama",
    "year": 2024,
    "games": 12,
    "wins": 10,
    "losses": 2,
    "win_pct": 0.833,
    "vsranked_record": "3-2",
    "vsranked_win_pct": 0.6
  }
}
```

**Why**: GraphQL API doesn't have coaching-specific metrics. This is custom-curated data.

**Location**: Loaded in `app.py` startup, used in `format_prediction_for_api()`

---

#### 3. **Historical Ratings** (`all_fbs_ratings_comprehensive_2025.json`)
Backup data loaded when GraphQL `ratings` query fails or is incomplete.

---

#### 4. **Week 14 Games** (`Currentweekgames.json`)
- **Complete betting lines** with moneylines
- **Weather data** for all Week 14 games
- **Media/network** information
- **Team rankings** embedded in game data

**Status**: Used as fallback when `betting_lines_manager` GraphQL query returns incomplete data

---

## 🎯 Data Format Handling Patterns

### **Pattern 1: GraphQL with JSON Fallback**
```python
# Example from betting_lines_manager.py

# Try GraphQL first
live_data = self._fetch_live_betting_lines()
if live_data:
    print(f"✅ Using live data from GraphQL API")
    return live_data

# Fallback to cached JSON
try:
    if os.path.exists(self.lines_file):
        with open(self.lines_file, 'r') as f:
            data = json.load(f)
            print(f"⚠️ Using cached data from {self.lines_file}")
            return data
except Exception as e:
    print(f"❌ Error loading betting lines: {e}")
    return {'games': []}
```

---

### **Pattern 2: Dual Format Parsing**
```python
# Handle both GraphQL 'lines' format and JSON 'bettingLines' format

if 'lines' in game:
    # GraphQL format
    lines_data = game['lines']
    providers_data = lines_data
    
elif 'bettingLines' in game:
    # JSON format  
    betting_lines = game['bettingLines']
    providers_data = betting_lines.get('allProviders', [])
```

**Files Using This Pattern**:
- `betting_lines_manager.py` (lines 362-390)

---

### **Pattern 3: Field Name Mapping**
```python
# GraphQL returns nested provider object, JSON returns string

# Handle both formats
provider_name = (
    provider.get('provider', {}).get('name')  # GraphQL nested
    if isinstance(provider.get('provider'), dict)
    else provider.get('provider', 'Unknown')  # JSON string
)
```

**Files Using This Pattern**:
- `betting_lines_manager.py` (lines 155-157)

---

## ⚠️ Known GraphQL API Limitations

### 1. **Betting Lines Missing Moneylines**
- **Expected**: `moneylineHome`, `moneylineAway` fields
- **Actual**: Only `spread` and `overUnder` in `game.lines` query
- **Workaround**: Use `Currentweekgames.json` for moneyline data

### 2. **Weather Data Incomplete**
- **Issue**: Some games return static fallback values (67.3°F, 3.4 mph)
- **Expected**: Real-time weather from `gameWeather` table
- **Status**: Working for most games, fallback for others

### 3. **Opening Lines Not Available**
- **Expected**: `spreadOpen`, `overUnderOpen` fields
- **Actual**: `lines` query doesn't include opening lines
- **Impact**: Can't calculate line movement

### 4. **Historical Games Limit**
- **Limit**: `limit: 100` on player metrics query
- **Impact**: Only top 100 players analyzed
- **Consideration**: May miss impact players on weaker teams

---

## 🔍 How to Identify Data Source

### **In Code**
```python
# Check for GraphQL data structure
if 'lines' in game:
    print("✅ Using GraphQL live data")
elif 'bettingLines' in game:
    print("⚠️ Using cached JSON data")
```

### **In Logs**
Look for these messages:
```
✅ Fetched 32 games with live betting lines from GraphQL
✅ Using live data from GraphQL API
```
or
```
⚠️ Using cached data from Currentweekgames.json
```

### **In Browser DevTools**
Check API response structure:
```json
// GraphQL format
{
  "lines": [
    {"provider": "ESPN Bet", "spread": 2.5}
  ]
}

// JSON format
{
  "bettingLines": {
    "allProviders": [
      {"provider": "ESPN Bet", "spread": 2.5, "moneylineHome": -185}
    ]
  }
}
```

---

## 🚀 Migration Checklist for New Data

When adding new data sources, follow this pattern:

### 1. **Check if GraphQL API Has It**
- Browse schema: https://api.collegefootballdata.com/api/docs/?url=/api-docs.json
- Test query in GraphQL playground
- Verify field names match expectations

### 2. **Add Query to `graphqlpredictor.py`**
```python
# Add to main query or create new async method
newData: tableName(where: {teamId: {_eq: $homeTeamId}}) {
    field1
    field2
}
```

### 3. **Handle Both Formats**
```python
# GraphQL format
if 'newField' in data:
    value = data['newField']
    
# JSON fallback format
elif 'old_field_name' in cached_data:
    value = cached_data['old_field_name']
```

### 4. **Add Field Name Mapping**
```python
# Map GraphQL field names to internal structure
{
    'graphqlFieldName': data.get('fieldFromAPI'),
    'internalName': data.get('differentAPIName', 'default')
}
```

### 5. **Test with Both Sources**
- Test with GraphQL API live
- Test with cached JSON (disconnect internet or modify query to fail)
- Verify fallback works correctly

### 6. **Update This Document**
- Add new data source to list
- Document field mappings
- Note any limitations or gotchas

---

## 📊 Current Data Flow Diagram

```
User Request (Georgia @ Alabama)
        ↓
Frontend (TeamSelector.tsx)
        ↓
Flask API (/predict endpoint)
        ↓
LightningPredictor.predict_game()
        ↓
┌─────────────────────────────────────────┐
│  GRAPHQL API (Primary)                  │
│  • Team metrics (EPA, success rates)   │
│  • Player stats (top 100)              │
│  • Talent ratings                      │
│  • Game results (season + recent)      │
│  • ELO/FPI ratings                     │
│  • Weather data                        │
│  • AP Poll rankings                    │
│  • Calendar/bye weeks                  │
│  • Betting lines (spread/total only)   │
│  • Media/network info                  │
└─────────────────────────────────────────┘
        ↓ (if incomplete)
┌─────────────────────────────────────────┐
│  JSON FILES (Fallback)                  │
│  • Currentweekgames.json (Week 14)     │
│    - Complete betting lines            │
│    - Moneylines                       │
│    - Team rankings                     │
│  • fbs.json (team selection)           │
│  • coaches_with_vsranked_stats.json    │
│  • all_fbs_ratings_comprehensive.json  │
└─────────────────────────────────────────┘
        ↓
Prediction Engine Processing
        ↓
format_prediction_for_api()
        ↓
JSON Response to Frontend
        ↓
React Components Display
```

---

## 🎯 Summary Statistics

| Data Type | GraphQL Tables | Total Fields | JSON Fallback |
|-----------|----------------|--------------|---------------|
| Team Metrics | 2 | 24 | ✅ |
| Player Stats | 1 | 3 | ✅ |
| Game Results | 5 queries | 15+ | ✅ |
| Ratings | 1 | 3 | ✅ |
| Talent | 1 | 1 | ❌ |
| Weather | 1 | 4 | ✅ |
| Betting Lines | 1* | 3* | ✅ (complete) |
| Poll Rankings | 1 | 4 | ✅ |
| Calendar | 1 | 4 | ❌ |
| Team Info | 1 | 8 | ✅ |
| Media | 1 | 2 | ✅ |

**Total**: 9 unique GraphQL tables, 18+ data queries per prediction

*Betting lines query returns incomplete data (no moneylines)

---

## 🔧 Troubleshooting Common Issues

### **Issue**: Sportsbook lines show "N/A"
**Cause**: Field name mismatch or using wrong data source  
**Fix**: Check if using GraphQL `lines` format vs JSON `bettingLines` format

### **Issue**: Weather shows static values (67.3°F)
**Cause**: GraphQL `gameWeather` returns null, fallback data used  
**Fix**: Verify game has weather data in API, use JSON fallback if needed

### **Issue**: Moneylines missing
**Cause**: GraphQL `game.lines` doesn't include moneyline fields  
**Fix**: Use `Currentweekgames.json` which has complete betting data

### **Issue**: Python using old code after changes
**Cause**: Python bytecode cache (`__pycache__`)  
**Fix**: 
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

---

## 📝 Next Migration Candidates

Data still in JSON files that could move to GraphQL:

1. **Coaching Stats** - No GraphQL equivalent yet
2. **Player Props** - Custom data not in API
3. **Rivalry Data** - Custom analysis
4. **Historical Backtesting** - Large dataset, better in files

---

**Document Version**: 1.0  
**Author**: AI Assistant (Claude Sonnet 4.5)  
**Last Migration**: Betting Lines (December 2, 2025)
