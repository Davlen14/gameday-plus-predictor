# UI Data Issues - Showing Zeros/50-50 Splits

**Date:** December 14, 2025  
**Priority:** HIGH - Multiple components showing placeholder data

---

## 🔴 Critical Issues

### 1. Game Control Metrics - Shows "AA leads 0, NN leads 0"
**Component:** `ComprehensiveStats.tsx` - `parseGameControl()`  
**Status:** ❌ BROKEN (just fixed but still not working)

**Symptoms:**
- Team abbreviations show as "AA" and "NN" instead of actual team names
- All values show 0:00 or 0
- All percentages show 50.0% / 50.0%

**Expected Data:**
```
Possession Time: 402:05 vs 398:03
Turnover Margin: -1 vs +8  
Penalty Yards: 491 vs 535
Games Played: 12 vs 12
Drives Per Game: 10.2 vs 10.1
```

**Root Cause:**
- `predictionData.team_statistics.away` or `.home` is **undefined/null**
- Function falls back to default values
- Need to verify backend is sending `team_statistics` object in API response

**Fix Location:** [ComprehensiveStats.tsx](frontend/src/components/figma/ComprehensiveStats.tsx#L580-L630)

---

### 2. Advanced Offensive Metrics - All Zeros
**Component:** `ComprehensiveStats.tsx` - `parseAdvancedOffensive()`  
**Status:** ❌ BROKEN

**Symptoms:**
```
Offense PPA:          BS 0    vs WASH 0
Success Rate:         BS 0%   vs WASH 0%
Explosiveness:        BS 0    vs WASH 0
Power Success:        BS 0%   vs WASH 0%
Stuff Rate:           BS 0%   vs WASH 0%
Line Yards:           BS 0    vs WASH 0
Second Level Yards:   BS 0    vs WASH 0
Open Field Yards:     BS 0    vs WASH 0
```

**Expected Data:**
- Should show actual PPA values (e.g., 0.161 vs 0.247)
- Success rates (e.g., 48.0% vs 96.1%)
- Real yardage metrics

**Root Cause:**
- Same as #1 - `team_statistics` object missing/undefined
- Updated function to use structured data but data source is empty

**Fix Location:** [ComprehensiveStats.tsx](frontend/src/components/figma/ComprehensiveStats.tsx#L393-L467)

---

### 3. Defensive Details - All Zeros
**Component:** `ComprehensiveStats.tsx` - `parseDefensiveData()`  
**Status:** ❌ BROKEN

**Symptoms:**
```
Sacks:                BS 0.0  vs WASH 0.0
Interceptions:        BS 0.0  vs WASH 0.0
Tackles for Loss:     BS 0.0  vs WASH 0.0
Fumbles Recovered:    BS 0.0  vs WASH 0.0
Defense PPA:          BS 0.0  vs WASH 0.0
Defense Success Rate: BS 0.0  vs WASH 0.0
Defense Explosiveness:BS 0.0  vs WASH 0.0
Defense Havoc Total:  BS 0.0  vs WASH 0.0
```

**Expected Data:**
- Real defensive stats from team_statistics
- Sacks, INTs, TFLs should be actual numbers

**Root Cause:**
- Same as #1 & #2 - `team_statistics` object missing

**Fix Location:** [ComprehensiveStats.tsx](frontend/src/components/figma/ComprehensiveStats.tsx#L472-L550)

---

## 🟡 Medium Priority Issues

### 4. Situational Performance - Identical Values
**Component:** `ComprehensiveStats.tsx` - Situational charts  
**Status:** ⚠️ SUSPICIOUS

**Symptoms:**
- Both teams show exact same percentages:
  - Success Rate: 42.9%
  - Explosiveness: 120%
  - Passing Downs: 30.8%
  - Standard Downs: 48.6%

**Expected:** Different values per team based on actual performance

---

### 5. Field Position Metrics - Near-Identical Values
**Component:** `ComprehensiveStats.tsx`  
**Status:** ⚠️ SUSPICIOUS

**Symptoms:**
```
Army vs Navy:
  Line Yards:         2.915 vs 3.295
  Second Level:       2.915 vs 3.295  
  Open Field:         2.915 vs 3.295
  Highlight Yards:    2.915 vs 3.295

Boise State vs Washington:
  All zones:          2.937 vs 2.951
```

**Expected:** More variance between teams

---

## 🔍 Investigation Plan

### Step 1: Verify Backend API Response
**File:** `app.py` - `/predict` endpoint

Check if `team_statistics` object is being sent:
```python
"team_statistics": {
    "home": convert_comprehensive_stats_to_dict(getattr(prediction, 'home_team_stats', None)),
    "away": convert_comprehensive_stats_to_dict(getattr(prediction, 'away_team_stats', None))
}
```

**Test:**
```bash
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Washington", "away_team": "Boise State"}' \
  | jq '.team_statistics'
```

**Expected Output:**
```json
{
  "home": {
    "possession_time": 24123,
    "turnover_margin": 8,
    "penalty_yards": 535,
    "games_played": 12,
    "offense_drives": 121,
    "offense_ppa": 0.247,
    "offense_success_rate": 0.961,
    ...
  },
  "away": { ... }
}
```

---

### Step 2: Verify GraphQL Data Fetch
**File:** `graphqlpredictor.py`

Check if `prediction.home_team_stats` and `prediction.away_team_stats` are being populated:

**Lines to check:**
- Where `ComprehensiveTeamStats` dataclass is populated
- GraphQL queries for team statistics
- Data transformation from API → dataclass

---

### Step 3: Check React Data Flow
**File:** `frontend/src/App.tsx`

Verify prediction data structure:
```typescript
console.log('predictionData:', predictionData);
console.log('team_statistics:', predictionData?.team_statistics);
console.log('away:', predictionData?.team_statistics?.away);
console.log('home:', predictionData?.team_statistics?.home);
```

---

## 📋 Checklist for Tomorrow

- [ ] **Test backend API** - Verify `team_statistics` in response
- [ ] **Check graphqlpredictor.py** - Confirm stats dataclass population
- [ ] **Add console.logs** - Debug React data flow
- [ ] **Fix null checks** - Ensure graceful fallback handling
- [ ] **Test with real games** - Army/Navy, Boise State/Washington
- [ ] **Verify other components** - Check if any other components affected

---

## 🎯 Expected Behavior After Fix

### Game Control Metrics
```
NAVY leads 1
ARMY leads 3

Possession Time:     ARM 402:05 (50.3%) vs NAV 398:03 (49.7%)
Turnover Margin:     ARM -1 (14.3%) vs NAV +8 (114.3%)
Penalty Yards:       ARM 491 (47.9%) vs NAV 535 (52.1%)
Games Played:        ARM 12 (50%) vs NAV 12 (50%)
Drives Per Game:     ARM 10.2 (50.2%) vs NAV 10.1 (49.8%)
```

### Advanced Offensive Metrics
```
Offense PPA:         BOIS 0.161 vs WASH 0.247
Success Rate:        BOIS 48.0% vs WASH 96.1%
Explosiveness:       BOIS 0.404 vs WASH 0.480
Power Success:       [real data]
Stuff Rate:          [real data]
Line Yards:          [real data]
Second Level Yards:  [real data]
Open Field Yards:    [real data]
```

### Defensive Details
```
Sacks:               [real data]
Interceptions:       [real data]
Tackles for Loss:    [real data]
Defense PPA:         BOIS 0.100 vs WASH 0.080
Defense Success Rate:[real data]
...
```

---

## 🛠️ Quick Fix Commands

```bash
# 1. Check backend response structure
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Washington", "away_team": "Boise State"}' \
  > /tmp/prediction_response.json

# 2. Inspect team_statistics
cat /tmp/prediction_response.json | jq '.team_statistics'

# 3. Check if fields exist
cat /tmp/prediction_response.json | jq '.team_statistics.home | keys'
cat /tmp/prediction_response.json | jq '.team_statistics.away | keys'

# 4. Verify specific fields
cat /tmp/prediction_response.json | jq '.team_statistics.home | {
  possession_time,
  turnover_margin,
  penalty_yards,
  games_played,
  offense_drives,
  offense_ppa,
  offense_success_rate
}'
```

---

## 📝 Notes

- All three components (`parseGameControl`, `parseAdvancedOffensive`, `parseDefensiveData`) were updated to use `team_statistics` structured data
- The updates are correct in the React code
- The issue is likely **upstream** in the backend not sending `team_statistics` or sending it as null/undefined
- Need to trace data flow: GraphQL API → graphqlpredictor.py → app.py → React frontend
