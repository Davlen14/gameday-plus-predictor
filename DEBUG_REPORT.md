# Game Preview Stats Debug Report
**Game ID:** 401778309 (Toledo @ Louisville)  
**Date:** 2025-12-15

---

## ✅ BACKEND VERIFICATION - ALL WORKING

### Database Check
Both coaches have complete season analytics data for 2025:

**Jason Candle (Toledo) - ID 283:**
- ✅ points_per_game: 31.58
- ✅ yards_per_game: 422.4
- ✅ third_down_pct: 41.0%
- ❌ red_zone_pct: NULL (expected to show "-")
- ✅ points_allowed_pg: 12.17
- ✅ sacks_per_game: 2.9
- ✅ turnovers_gained_pg: 1.7
- ✅ sp_overall: 8.4
- ✅ sp_offense: 26.8
- ✅ sp_defense: 17.9
- ✅ fpi: 4.148

**Jeff Brohm (Louisville) - ID 342:**
- ✅ points_per_game: 30.17
- ✅ yards_per_game: 388.9
- ✅ third_down_pct: 36.7%
- ❌ red_zone_pct: NULL (expected to show "-")
- ✅ points_allowed_pg: 21.08
- ✅ sacks_per_game: 2.2
- ✅ turnovers_gained_pg: 1.6
- ✅ sp_overall: 11.7
- ✅ sp_offense: 31.9
- ✅ sp_defense: 20.6
- ✅ fpi: 9.894

### Backend Function Check
`get_game_preview_data(401778309)` returns:
- ✅ Correct structure with all keys
- ✅ `season_analytics.primary` (Toledo/Away) populated
- ✅ `season_analytics.opponent` (Louisville/Home) populated
- ✅ JSON serialization successful (8,729 bytes)
- ✅ All field names match database columns

---

## 🔍 FRONTEND INVESTIGATION

### Data Flow
1. Server route `/game-preview/401778309` calls `get_game_preview_data()`
2. Data passed to template as `game_data`
3. Template embeds as `SERVER_GAME_DATA` via Jinja2 `tojson` filter
4. JavaScript sets `gameData = SERVER_GAME_DATA`
5. `transformServerData()` creates team objects (preserves season_analytics)
6. `updateUI()` calls `populateSeasonAnalytics()`

### Template Analysis
**File:** `templates/game_detail_upcoming.html`

**JavaScript Function:** `populateSeasonAnalytics()` (lines 1260-1320)
- Correctly accesses `gameData.season_analytics.primary` and `.opponent`
- Has proper null checks
- Field name mapping is correct:
  - `points_per_game` → `away-ppg`, `home-ppg`
  - `yards_per_game` → `away-ypg`, `home-ypg`
  - `third_down_pct` → `away-3rd`, `home-3rd`
  - `red_zone_pct` → `away-rz`, `home-rz`
  - `points_allowed_pg` → `away-ppg-allowed`, `home-ppg-allowed`
  - `sacks_per_game` → `away-sacks`, `home-sacks`
  - `turnovers_gained_pg` → `away-to`, `home-to`
  - `sp_overall`, `sp_offense`, `sp_defense` → corresponding elements

**HTML Elements:** All `id` attributes exist in template (verified lines 700-800)

---

## 🐛 POTENTIAL ISSUES

### Hypothesis 1: Early Return from Function
If `!gameData.season_analytics` or `!awayAnalytics` or `!homeAnalytics`, function returns early and ALL stats show "-".

**Fix:** Added comprehensive debug logging to identify where function exits.

### Hypothesis 2: Timing Issue
`populateSeasonAnalytics()` might be called before data is fully loaded.

**Fix:** Function is called from `updateUI()` which is called after data is confirmed loaded.

### Hypothesis 3: Data Structure Mismatch
The `transformServerData()` function might accidentally overwrite or break the season_analytics structure.

**Fix:** Reviewed code - function only adds `gameData.home` and `gameData.away`, doesn't touch `season_analytics`.

### Hypothesis 4: Element IDs Don't Match
HTML element IDs might not match JavaScript `getElementById()` calls.

**Fix:** Verified all element IDs exist in template.

---

## 🔧 DEBUGGING CHANGES MADE

### Enhanced Logging in `populateSeasonAnalytics()`
Added extensive console.log statements to trace:
1. Whether function is called
2. Whether gameData exists
3. Whether season_analytics exists  
4. What keys are in gameData
5. What fields are in awayAnalytics and homeAnalytics
6. Specific values for key fields like yards_per_game

### Test Instructions
1. Start server: `python app_master.py`
2. Open: http://localhost:5555/game-preview/401778309
3. Open browser console (F12)
4. Look for debug messages starting with "🔍 DEBUG:"
5. Check if function is being called
6. Check if data exists
7. Check actual field values

---

## ✅ VERIFICATION STEPS

To verify the fix works:

```bash
# 1. Start server
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
source .venv/bin/activate
python app_master.py

# 2. Test API endpoint directly
python test_api.py

# 3. Open browser to:
http://localhost:5555/game-preview/401778309

# 4. Check browser console for debug output
# Look for "🔍 DEBUG:" messages
```

---

## 📊 EXPECTED RESULTS

After fix, the page should display:

**Toledo (Away):**
- Points/Game: 31.6 ✅
- Yards/Game: 422 ✅  
- 3rd Down: 41.0% ✅
- Red Zone: - (NULL in DB) ✅
- Points Allowed: 12.2 ✅
- Sacks/Game: 2.9 ✅
- Turnovers/Game: 1.7 ✅
- SP+ Overall: 8.4 ✅
- SP+ Offense: 26.8 ✅
- SP+ Defense: 17.9 ✅
- FPI: 4.1 ✅

**Louisville (Home):**
- Points/Game: 30.2 ✅
- Yards/Game: 389 ✅
- 3rd Down: 36.7% ✅
- Red Zone: - (NULL in DB) ✅
- Points Allowed: 21.1 ✅
- Sacks/Game: 2.2 ✅
- Turnovers/Game: 1.6 ✅
- SP+ Overall: 11.7 ✅
- SP+ Offense: 31.9 ✅
- SP+ Defense: 20.6 ✅
- FPI: 9.9 ✅

---

## 🎯 CONCLUSION

**Backend:** ✅ Working perfectly - all data present and correctly formatted

**Frontend:** ⚠️ Needs verification - added debug logging to identify issue

**Most Likely Root Cause:** The populateSeasonAnalytics() function may be returning early due to a falsy check, OR there's a timing issue where it's called before data loads.

**Next Steps:** 
1. Open page in browser with console open
2. Review debug output
3. If data exists but still shows "-", check if elements are being updated
4. If data doesn't exist, trace back to see where it's lost

**Files Modified:**
- `templates/game_detail_upcoming.html` - Added debug logging to populateSeasonAnalytics()
- `test_api.py` - Created new test script for API verification
