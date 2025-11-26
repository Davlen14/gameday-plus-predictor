# 🗓️ Weekly Update Checklist - Week 12 (College Football Season)

Use this every Monday (or when new week data becomes available) to roll the system forward cleanly.

**📍 CURRENT WEEK:** Week 12 (November 11-16, 2025)  
**🎯 DATA SOURCES:** GraphQL API + Static JSON Files + Manual AP Poll Updates  
**⚙️ CRITICAL SYSTEMS:** Backend (Flask/app.py), Frontend (React/Vite), Predictor Engine (graphqlpredictor.py)

---

## 🚀 QUICK START CHECKLIST FOR WEEK 12

### Pre-Update Preparation
- [ ] Verify current environment is activated: `source .venv/bin/activate`
- [ ] Backup current `Currentweekgames.json`: `cp Currentweekgames.json Currentweekgames_week11_backup.json`
- [ ] Check for any active processes on ports: `lsof -ti:5002,5173`

### Core Updates (Required)
- [x] **Update predictor week constants** (predictor/core/lightning_predictor.py lines 319, 933) ✅ COMPLETED Nov 13
- [x] **Generate Week 12 betting data** (week11_graphql_fetcher.py modified to Week 12) ✅ COMPLETED Nov 13 - 58 FBS games
- [x] **Update AP Poll rankings** (add week_12 node to frontend/src/data/ap.json) ✅ COMPLETED Nov 13
- [x] **Update player analysis files** (copy from ABCNEW to backtesting 2/) ✅ COMPLETED Nov 13
- [x] **Update frontend components** (TeamSelector, Header with Texas @ Georgia) ✅ COMPLETED Nov 13

### Verification Steps
- [ ] Test prediction for featured Week 12 game
- [ ] Verify rankings display correctly in header
- [ ] Check weekly progression shows Weeks 1-12
- [ ] Confirm network/media data populated
- [ ] Validate all game times in ET timezone

---

## 🎯 WEEK 12 KEY MATCHUPS (November 16, 2025)

**Top Games to Feature:**
1. **#1 Ohio State @ Northwestern** - Big Ten Championship implications
2. **#2 Indiana @ Ohio State** (if scheduled) - Top 5 showdown
3. **#3 Texas A&M @ Auburn** - SEC battle
4. **#4 Alabama vs Mercer** (tune-up game)
5. **#5 Georgia @ Tennessee** - SEC East rivalry
6. **#6 Oregon vs Washington** - Pac-12 matchup
7. **#8 BYU @ Arizona State** - Big 12 race continues
8. **#10 Notre Dame vs Army** - Ranked showdown

---

## 1. Core Predictor Week Constants  
<sup><strong>Status:</strong> RUNNABLE (local Python edit only)</sup>

**📁 Files to Update:**
- `graphqlpredictor.py`

**✏️ Exact Changes Required:**
1. **Line 319**: Update `self.current_week = 11` → `self.current_week = 12`
2. **Line 933**: Update `$currentWeek: smallint = 11` → `$currentWeek: smallint = 12`

**🔍 How to Verify:** 
```bash
# Search for current_week references
grep -n "current_week" graphqlpredictor.py | head -5

# Should show:
# 319:        self.current_week = 12
# 933:        $currentWeek: smallint = 12
```

**⚠️ Common Mistakes:**
- Forgetting to update BOTH the class variable AND the GraphQL query parameter
- Using string "12" instead of integer 12

- [x] Update `self.current_week = 12` in predictor/core/lightning_predictor.py line 319 ✅
- [x] Update GraphQL query `$currentWeek: smallint = 12` in line 933 ✅
- [x] Update player_files dict with Nov 13 timestamps (lines 425-431) ✅
- [x] Verify both changes with grep command above ✅

---

## 2. Betting Data / Lines  
<sup><strong>Status:</strong> RUNNABLE – Create new Week 12 fetcher script</sup>

**🎯 PRIMARY DATA SOURCE:** College Football Data GraphQL API  
**📁 Output Files:** `Currentweekgames.json` (primary)  
**🔧 Script to Create:** `week12_graphql_fetcher.py`

### Step 1: Create week12_graphql_fetcher.py
Copy the Week 11 fetcher and modify:

```bash
# Copy Week 11 fetcher as template
cp week11_graphql_fetcher.py week12_graphql_fetcher.py
```

**Key Changes Required in week12_graphql_fetcher.py:**
1. **Line 24**: Update comment from "GetWeek11Games" to "GetWeek12Games"
2. **Line 30**: Change `week: {_eq: 11}` to `week: {_eq: 12}`
3. **Line 89**: Change `'week': 11` to `'week': 12`
4. **Line 1** (docstring): Update title to "Week 12 College Football Data Fetcher"

### Step 2: Run the Week 12 Fetcher
```bash
python week12_graphql_fetcher.py
```

**Expected Output:**
```
🏈 Week 12 College Football Data Fetcher (GraphQL)
==================================================
📡 Fetching Week 12 games via GraphQL...
✅ Found ~300+ total games for Week 12
📊 Filtered to 50-60 FBS games
📊 Fetching AP Poll rankings...
✅ Found 25 ranked teams
🔄 Processing games...

✅ Week 12 data saved to Currentweekgames.json
   Total games: 52 (approximate)
   Ranked matchups: 12-18
   Games with media info: 45-50
```

### Step 3: Validate Network/Media Data
```bash
# Check games have network information
jq -r '.games.all[] | select(.media.network != "TBD") | "\(.awayTeam.name) @ \(.homeTeam.name) - \(.media.network)"' Currentweekgames.json | head -10

# Expected: ABC, ESPN, FOX, NBC, etc.
```

### Step 4: Verify Timezone Conversion
```bash
# Check first game's datetime
jq '.games.all[0].datetime' Currentweekgames.json

# Should show:
# - "timeZone": "ET"
# - "formatted": contains "ET" not "UTC"
```

### Step 5: Validate Rankings Integration
```bash
# Show all ranked teams in games
jq -r '.games.all[] | select(.homeTeam.rank != null or .awayTeam.rank != null) | "[\(.awayTeam.rank // "NR")] \(.awayTeam.name) @ [\(.homeTeam.rank // "NR")] \(.homeTeam.name)"' Currentweekgames.json

# Expected: Should show ranked teams from Week 12 AP Poll
```

### Step 6: Verify Game Week Fields
All individual games should have week=12:
```bash
jq '.games.all[].gameInfo.week' Currentweekgames.json | sort -u

# Should output: 12
```

**Checklist:**
- [x] Created week12_graphql_fetcher.py from week11 template (modified in place) ✅
- [x] Updated week numbers in lines 24, 30, 89 ✅
- [x] Ran fetcher script successfully ✅
- [x] Verified 58 FBS games generated ✅
- [x] Confirmed network data populated (57/58 games = 98% coverage) ✅
- [x] Validated all times in ET timezone ✅
- [x] Checked rankings embedded in game objects (21 ranked matchups) ✅
- [x] Verified all games have week=12 in gameInfo ✅

---

## 3. AP Poll Rankings (Week 12)
<sup><strong>Status:</strong> MANUAL ENTRY - ESPN/AP Official Source</sup>

**📁 Primary File:** `frontend/src/data/ap.json`  
**🎯 Data Source:** https://www.espn.com/college-football/rankings  
**⏱️ Update Timing:** Monday ~12pm ET (November 11, 2025)

### Step 1: Get Week 12 AP Poll Rankings
Navigate to ESPN AP Poll page. Week 12 poll will be released Monday, November 11, 2025.

### Step 2: Add week_12 Node to ap.json
Open `frontend/src/data/ap.json` and add new week node:

```json
{
  "week_12": {
    "poll": "AP Top 25",
    "season": 2025,
    "seasonType": "regular",
    "week": 12,
    "ranks": [
      {
        "rank": 1,
        "school": "Ohio State",
        "conference": "Big Ten",
        "firstPlaceVotes": 60,
        "points": 1650
      },
      {
        "rank": 2,
        "school": "Indiana",
        "conference": "Big Ten",
        "firstPlaceVotes": 2,
        "points": 1598
      }
      // ... continue with all 25 teams
    ]
  }
}
```

**⚠️ CRITICAL RULES:**
1. **Team Name Matching:** Must EXACTLY match names in `fbs.json`
   - ✅ "Miami" not "Miami (FL)"
   - ✅ "USC" not "Southern California"  
   - ✅ "Ole Miss" not "Mississippi"
2. **Week Key Format:** Must be `week_12` (underscore, lowercase)
3. **All 25 Teams:** Include complete Top 25
4. **Sort Order:** Rank 1-25 in order

### Step 3: Verify Rankings in Currentweekgames.json
Rankings should auto-populate during fetch, but verify:

```bash
# Check ranked teams in games
jq '.games.all[] | select(.homeTeam.rank != null or .awayTeam.rank != null) | {home: .homeTeam.name, homeRank: .homeTeam.rank, away: .awayTeam.name, awayRank: .awayTeam.rank}' Currentweekgames.json | head -10
```

If rankings missing, run this Python script:
```python
import json

# Load files
with open('frontend/src/data/ap.json', 'r') as f:
    ap_data = json.load(f)
    
with open('Currentweekgames.json', 'r') as f:
    games_data = json.load(f)

# Get Week 12 rankings
week_12_ranks = {team['school']: team['rank'] for team in ap_data['week_12']['ranks']}

# Update games
for game in games_data['games']['all']:
    game['homeTeam']['rank'] = week_12_ranks.get(game['homeTeam']['name'])
    game['awayTeam']['rank'] = week_12_ranks.get(game['awayTeam']['name'])

# Save
with open('Currentweekgames.json', 'w') as f:
    json.dump(games_data, f, indent=2)
    
print("✅ Added Week 12 rankings to all games")
```

### Step 4: Test Rankings Display
```bash
# Show Week 12 Top 10
jq '.week_12.ranks[] | select(.rank <= 10) | {rank: .rank, school: .school}' frontend/src/data/ap.json
```

**Checklist:**
- [x] Week 12 AP Poll released (Monday Nov 11) ✅
- [x] Added week_12 node to ap.json with all 25 teams ✅
- [x] Verified team names match fbs.json exactly ✅
- [ ] Confirmed rankings in Currentweekgames.json (after fetcher runs)
- [x] Tested jq command shows correct Top 10 ✅

---

## 4. Player Analysis Files Update
<sup><strong>Status:</strong> EXTERNAL COPY - From ABCNEW folder</sup>

**📁 Source:** ABCNEW folder (latest exports)  
**📁 Destination:** `backtesting 2/` folder  
**⏱️ Update Timing:** Weekly after games complete (~Monday)

### Step 1: Verify New Files in ABCNEW
Check for files with current week timestamps:

```bash
# Navigate to ABCNEW folder
cd ~/path/to/ABCNEW

# List all comprehensive analysis files
ls -lh comprehensive_*_analysis_*.json

# Should see 7 files with recent dates (Nov 10-11, 2025)
```

### Step 2: Copy Files to backtesting 2/
```bash
# Copy all 7 position files
cp comprehensive_qb_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_rb_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_wr_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_te_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_db_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_lb_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/
cp comprehensive_dl_analysis_*.json ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/

echo "✅ Copied all 7 player analysis files for Week 12"
```

### Step 3: Update File References in graphqlpredictor.py
Open `graphqlpredictor.py` and update lines 425-431:

```python
player_files = {
    'qb': 'backtesting 2/comprehensive_qb_analysis_2025_Nov_10_2025_01_17_46.json',
    'rb': 'backtesting 2/comprehensive_rb_analysis_2025_Nov_10_2025_01_22_01.json',
    'wr': 'backtesting 2/comprehensive_wr_analysis_2025_Nov_10_2025_01_24_19.json',
    'te': 'backtesting 2/comprehensive_te_analysis_2025_Nov_10_2025_01_26_30.json',
    'db': 'backtesting 2/comprehensive_db_analysis_2025_Nov_10_2025_01_28_41.json',
    'lb': 'backtesting 2/comprehensive_lb_analysis_2025_Nov_10_2025_01_30_52.json',
    'dl': 'backtesting 2/comprehensive_dl_analysis_2025_Nov_10_2025_01_33_03.json'
}
```

**⚠️ Update filenames with EXACT timestamps from your new files!**

### Step 4: Verify File Loading
```bash
# Check files exist
ls -lh backtesting\ 2/comprehensive_*_analysis_*.json

# Test loading QB data
python -c "import json; f=open('backtesting 2/comprehensive_qb_analysis_2025_Nov_10_2025_01_17_46.json'); data=json.load(f); print(f'✅ Loaded {len(data)} QBs')"
```

**Expected:** Should load 150-160 QBs without errors

**Checklist:**
- [x] Verified 7 new files exist in ABCNEW folder ✅
- [x] Copied all files to backtesting 2/ ✅
- [ ] Updated player_files dict in graphqlpredictor.py (lines 425-431)
- [x] Verified QB file loads successfully ✅
- [x] Confirmed WR file has 600+ players ✅

**✅ FILES GENERATED & COPIED (Nov 13, 2025):**
- comprehensive_qb_analysis_2025_20251113_034352.json (213K - 385 QBs)
- comprehensive_rb_analysis_2025_20251113_034902.json (476K)
- comprehensive_wr_analysis_2025_20251113_034912.json (455K - 706 WRs)
- comprehensive_te_analysis_2025_20251113_034910.json (204K)
- comprehensive_db_analysis_2025_20251113_034921.json (1.1M)
- comprehensive_lb_analysis_2025_20251113_034919.json (584K)
- comprehensive_dl_analysis_2025_20251113_034920.json (825K)

---

## 5. Frontend Component Updates
<sup><strong>Status:</strong> RUNNABLE - Direct TypeScript edits</sup>

### Update 1: TeamSelector Quick Games
**File:** `frontend/src/components/figma/TeamSelector.tsx`  
**Lines to Update:** 203-211, 74-76, 291

#### A. Update Quick Games Array (lines 203-211)
```typescript
const week12Games = [  // Renamed from week9Games
  { away: 'Indiana', home: 'Ohio State', label: '#2 Indiana @ #1 Ohio State' },
  { away: 'Texas A&M', home: 'Auburn', label: '#3 Texas A&M @ Auburn' },
  { away: 'Georgia', home: 'Tennessee', label: '#5 Georgia @ Tennessee' },
  { away: 'BYU', home: 'Arizona State', label: '#8 BYU @ Arizona State' },
  { away: 'Army', home: 'Notre Dame', label: 'Army @ #10 Notre Dame' },
  { away: 'Oregon', home: 'Washington', label: '#6 Oregon @ Washington' },
  { away: 'Alabama', home: 'Mercer', label: '#4 Alabama vs Mercer' },
  { away: 'LSU', home: 'Florida', label: 'LSU @ Florida' }
];
```

#### B. Update Default Team Selection (lines 74-76)
Choose the featured game of the week:
```typescript
const [homeTeam, setHomeTeam] = useState<Team | null>(
  teams.find(t => t.school === 'Ohio State') || null  // Featured home team
);
const [awayTeam, setAwayTeam] = useState<Team | null>(
  teams.find(t => t.school === 'Indiana') || null  // Featured away team
);
```

#### C. Update Section Header (line 291)
```typescript
<h3 className="text-lg font-semibold text-white mb-3">Week 12 Key Games - Quick Select</h3>
```

### Update 2: Header Demo Data
**File:** `frontend/src/components/figma/Header.tsx`  
**Lines:** 46-65

Update to show Week 12 featured matchup:
```typescript
const demoData = {
  game_info: {
    date: "November 16, 2025",
    time: "12:00 PM ET",
    network: "FOX",  // Update when known
    excitement_index: 9.5
  },
  teams: {
    away: {
      name: "Indiana",
      record: "10-0",
      logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/84.png",
      rank: 2
    },
    home: {
      name: "Ohio State",
      record: "9-1",
      logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png",
      rank: 1
    }
  }
};
```

### Update 3: AP Poll Week Fallback
**File:** `frontend/src/components/figma/APPollRankings.tsx`  
**Line:** 27

```typescript
const dynamicWeek = predictionData?.contextual_analysis?.current_week || 12;
```

**⚠️ CRITICAL:** This controls weekly progression display (Week 1-12)

**Checklist:**
- [ ] Updated TeamSelector quick games to Week 12 matchups (8 games)
- [ ] Changed default team selection to featured game
- [ ] Updated quick games section header to "Week 12"
- [ ] Modified Header demo data to Indiana @ Ohio State
- [ ] Changed APPollRankings week fallback from 11 to 12
- [ ] Updated demo data records and logos

---

## 6. System Restart & Testing
<sup><strong>Status:</strong> RUNNABLE - Full stack validation</sup>

### Step 1: Kill Existing Processes
```bash
# Kill backend and frontend
lsof -ti:5002 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Verify ports are free
lsof -i:5002,5173
# Should return empty
```

### Step 2: Start Full Stack
```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Start both servers
./start-fullstack.sh
```

**Expected Output:**
- Terminal Tab 1: Flask server running on port 5002
- Terminal Tab 2: Vite dev server running on port 5173
- Browser auto-opens to http://localhost:5173

### Step 3: Frontend Validation Checklist
Open browser to http://localhost:5173 and verify:

**Initial Load:**
- [ ] Default teams show Indiana @ Ohio State (or your featured game)
- [ ] Team logos display correctly
- [ ] Quick Games section shows "Week 12 Key Games"
- [ ] 8 quick game buttons display with correct matchups

**After Running Prediction:**
- [ ] Header shows correct rankings (e.g., "#2 Indiana @ #1 Ohio State")
- [ ] Network displays (ABC, ESPN, FOX, etc. - not "TBD")
- [ ] Game time shows in ET timezone
- [ ] Date shows November 16, 2025 (Week 12 Saturday)

**Rankings Section:**
- [ ] Weekly Rankings Progression shows Weeks 1-12 (not stopping at 11)
- [ ] Current week highlighted as Week 12
- [ ] Both teams show correct rank progression

**Season Records:**
- [ ] Each team shows ALL games (10-11 games, not just 6)
- [ ] Games include opponent, score, result (W/L)
- [ ] Recent games appear at bottom

**Player Impact:**
- [ ] Individual players listed with efficiency scores
- [ ] Team differentials calculated correctly
- [ ] No "Player data unavailable" errors

**Market Analysis:**
- [ ] Multiple sportsbooks displayed (DraftKings, FanDuel, etc.)
- [ ] Consensus spread and total shown
- [ ] Line comparison with recommendations

### Step 4: Backend API Testing
Test the prediction endpoint directly:

```bash
# Test with featured game
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Ohio State", "away_team": "Indiana"}' \
  | jq '.ui_components.header.teams'

# Should return:
# {
#   "home": { "name": "Ohio State", "rank": 1, ... },
#   "away": { "name": "Indiana", "rank": 2, ... }
# }
```

### Step 5: Verify Data Files
```bash
# Check Currentweekgames.json updated
jq '.summary.week' Currentweekgames.json
# Should return: 12

# Count total games
jq '.summary.totalGames' Currentweekgames.json
# Should be: 50-60

# Check ranked matchups
jq '.summary.rankedMatchups' Currentweekgames.json
# Should be: 12-18
```

### Step 6: Browser Cache Clear (If Needed)
If old data persists:

**Mac:** Command + Shift + R (hard refresh)  
**Windows:** Ctrl + Shift + R

Or clear cache completely in browser settings.

**Checklist:**
- [ ] Backend running on port 5002
- [ ] Frontend running on port 5173
- [ ] Default game loads correctly
- [ ] Predictions return Week 12 data
- [ ] Rankings show correctly in header
- [ ] Weekly progression shows 1-12
- [ ] Season records show all games
- [ ] Network data populated
- [ ] No console errors in browser
- [ ] API endpoint test successful

---

## 7. Data Verification Commands

### Quick Health Check
```bash
# Verify all core files exist and are recent
ls -lh Currentweekgames.json  # Should be Nov 11+ 2025
ls -lh frontend/src/data/ap.json  # Should have week_12 node
ls -lh backtesting\ 2/comprehensive_qb_analysis_*.json  # Should be Nov 10+ 2025

# Check predictor week
grep "self.current_week = " graphqlpredictor.py
# Should show: self.current_week = 12

# Verify game week in data
jq '.games.all[0].gameInfo.week' Currentweekgames.json
# Should return: 12
```

### Comprehensive Data Validation
```bash
# Show Week 12 summary
jq '.summary' Currentweekgames.json

# List all ranked teams in Week 12 games
jq -r '.games.all[] | select(.homeTeam.rank != null or .awayTeam.rank != null) | "[\(.awayTeam.rank // "NR")] \(.awayTeam.name) @ [\(.homeTeam.rank // "NR")] \(.homeTeam.name) - \(.media.network)"' Currentweekgames.json

# Show Top 10 from Week 12 AP Poll
jq '.week_12.ranks[] | select(.rank <= 10) | {rank: .rank, school: .school, points: .points}' frontend/src/data/ap.json

# Verify player file loading
python -c "
import json
positions = ['qb', 'rb', 'wr', 'te', 'db', 'lb', 'dl']
for pos in positions:
    try:
        # Update with actual filenames
        files = !ls backtesting\ 2/comprehensive_{pos}_analysis_*.json 2>/dev/null
        if files:
            with open(files[0]) as f:
                data = json.load(f)
                print(f'✅ {pos.upper()}: {len(data)} players loaded')
    except Exception as e:
        print(f'❌ {pos.upper()}: Error - {e}')
"
```

### Network Data Coverage
```bash
# Count games with network data
jq '[.games.all[] | select(.media.network != "TBD")] | length' Currentweekgames.json

# Show network distribution
jq -r '.games.all[].media.network' Currentweekgames.json | sort | uniq -c | sort -rn
```

**Checklist:**
- [ ] All data files have correct Week 12 timestamps
- [ ] predictor week = 12
- [ ] Game week fields = 12
- [ ] Week 12 AP Poll in ap.json (25 teams)
- [ ] Ranked matchups identified correctly
- [ ] Network coverage 85%+ (45+ games with networks)
- [ ] Player files load without errors

---

## 8. Week 12 Documentation

### Files Modified This Week
Create a record of all changes:

```markdown
## Week 12 Update Summary (November 11-13, 2025)

### Files Modified:
1. graphqlpredictor.py - Lines 319, 933, 425-431
2. week12_graphql_fetcher.py - Created new
3. Currentweekgames.json - Regenerated with 52 games
4. frontend/src/data/ap.json - Added week_12 node
5. frontend/src/components/figma/TeamSelector.tsx - Lines 203-211, 74-76, 291
6. frontend/src/components/figma/Header.tsx - Lines 46-65
7. frontend/src/components/figma/APPollRankings.tsx - Line 27
8. backtesting 2/ - All 7 player analysis files updated

### Data Changes:
- Total Games: 52 FBS games
- Ranked Matchups: 14 games with ranked teams
- Top Game: #2 Indiana @ #1 Ohio State
- New Features: [List any new enhancements]

### Issues Encountered:
[Document any problems and solutions]

### Testing Results:
- Backend predictions: ✅ Working
- Frontend display: ✅ Working
- Rankings integration: ✅ Working
- Player data: ✅ Working
```

**Checklist:**
- [ ] Created Week 12 update summary
- [ ] Documented all file changes
- [ ] Recorded any issues and solutions
- [ ] Backed up previous week's data

---

## 🎯 WEEK 12 COMPLETION CHECKLIST

System is fully updated for Week 12 when ALL of these are true:

### Core Functionality
- [ ] Predictor runs with week=12 in all queries
- [ ] Predictions return Week 12 game data
- [ ] Multiple sportsbooks integrated (8+ providers)
- [ ] Player analysis uses latest Week 12 data

### Data Accuracy
- [ ] 50-60 FBS games in Currentweekgames.json
- [ ] AP Poll Week 12 rankings (all 25 teams)
- [ ] Rankings embedded in game objects
- [ ] Network/TV data populated (85%+ coverage)
- [ ] All game times in ET timezone

### Frontend Display
- [ ] Header shows correct Week 12 rankings
- [ ] Weekly progression displays Weeks 1-12
- [ ] Season records show all games (not truncated)
- [ ] Quick games show 8 Week 12 matchups
- [ ] Default game is Week 12 featured matchup
- [ ] Network information displays correctly

### Testing
- [ ] Test prediction for 3+ different Week 12 games
- [ ] Verify rankings match AP Poll exactly
- [ ] Confirm no console errors in browser
- [ ] Check mobile responsiveness (optional)
- [ ] Validate betting lines from multiple books

### Documentation
- [ ] Update summary created
- [ ] Previous week data backed up
- [ ] Any issues documented with solutions
- [ ] Version incremented (if applicable)

---

## 🚨 TROUBLESHOOTING GUIDE (Week 12 Specific)

### Issue: Week still shows 11 instead of 12
**Locations to check:**
1. graphqlpredictor.py line 319: `self.current_week = 12`
2. graphqlpredictor.py line 933: `$currentWeek: smallint = 12`
3. week12_graphql_fetcher.py line 30: `week: {_eq: 12}`
4. APPollRankings.tsx line 27: `|| 12`
5. Currentweekgames.json: `"week": 12` in summary
6. Individual games: `gameInfo.week = 12`

**Fix command:**
```bash
# Find all week 11 references that should be 12
grep -rn "week.*11" graphqlpredictor.py week12_graphql_fetcher.py frontend/src/components/figma/APPollRankings.tsx
```

### Issue: Rankings not displaying
**Check:**
1. ap.json has week_12 node with 25 teams
2. Team names match exactly (Miami not Miami (FL))
3. Currentweekgames.json has rank fields populated
4. Backend restarted after data update

**Fix:**
```bash
# Verify rankings in games
jq '[.games.all[] | select(.homeTeam.rank != null or .awayTeam.rank != null)] | length' Currentweekgames.json

# If 0, rankings not embedded - run ranking sync script from Section 3 Step 3
```

### Issue: Player data errors
**Check:**
1. Files exist in backtesting 2/ folder
2. Filenames in player_files dict match exactly (lines 425-431)
3. Files are valid JSON (not corrupted)
4. Timestamps are from Nov 10+ 2025

**Fix:**
```bash
# Validate all player files
for pos in qb rb wr te db lb dl; do
  file=$(ls backtesting\ 2/comprehensive_${pos}_analysis_*.json 2>/dev/null | head -1)
  if [ -f "$file" ]; then
    python -c "import json; data=json.load(open('$file')); print(f'✅ $pos: {len(data)} players')"
  else
    echo "❌ $pos: File not found"
  fi
done
```

### Issue: Frontend not updating
**Try these in order:**
1. Hard refresh browser (Cmd+Shift+R on Mac)
2. Clear browser cache completely
3. Restart backend: `lsof -ti:5002 | xargs kill -9 && ./start-fullstack.sh`
4. Check for JavaScript errors in browser console (F12)
5. Verify API endpoint returns Week 12 data: `curl http://localhost:5002/health`

### Issue: Network data missing
**Check:**
1. week12_graphql_fetcher.py includes mediaInfo in query
2. Network extraction logic present (lines ~90-110)
3. Games with "TBD" network expected for some games
4. Major networks (ABC, ESPN, FOX) should be present

**Verify:**
```bash
# Count games with networks
jq '[.games.all[] | select(.media.network != "TBD")] | length' Currentweekgames.json

# Show network breakdown
jq -r '.games.all[].media.network' Currentweekgames.json | sort | uniq -c
```

---

## 📋 QUICK COMMAND REFERENCE

### Essential Updates (Copy & Paste Order)
```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Backup current data
cp Currentweekgames.json Currentweekgames_week11_backup.json

# 3. Create Week 12 fetcher
cp week11_graphql_fetcher.py week12_graphql_fetcher.py
# (Then manually edit week numbers: lines 24, 30, 89)

# 4. Run Week 12 fetcher
python week12_graphql_fetcher.py

# 5. Update predictor constants
# Manually edit graphqlpredictor.py lines 319, 933 to use 12

# 6. Copy player files (if available)
cp ~/path/to/ABCNEW/comprehensive_*_analysis_*.json backtesting\ 2/

# 7. Update player file references
# Manually edit graphqlpredictor.py lines 425-431

# 8. Update AP Poll
# Manually add week_12 node to frontend/src/data/ap.json

# 9. Update frontend components
# Manually edit TeamSelector.tsx, Header.tsx, APPollRankings.tsx

# 10. Restart servers
lsof -ti:5002,5173 | xargs kill -9 2>/dev/null
./start-fullstack.sh

# 11. Test in browser
open http://localhost:5173
```

### Verification Commands
```bash
# Check week in all locations
echo "Predictor week:" && grep "self.current_week = " graphqlpredictor.py
echo "Game data week:" && jq '.summary.week' Currentweekgames.json
echo "AP Poll week:" && jq 'keys | .[-1]' frontend/src/data/ap.json

# Verify game count
jq '.summary.totalGames' Currentweekgames.json

# Show featured games
jq -r '.games.all[] | select(.homeTeam.rank <= 10 or .awayTeam.rank <= 10) | "[\(.awayTeam.rank // "NR")] \(.awayTeam.name) @ [\(.homeTeam.rank // "NR")] \(.homeTeam.name)"' Currentweekgames.json | head -10

# Test API
curl -s http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Ohio State", "away_team": "Indiana"}' \
  | jq '.ui_components.header.teams.home.rank'
# Should return: 1
```

---

## 📊 WEEK 12 DATA EXPECTATIONS

### Game Schedule
- **Week 12 Dates:** November 11-16, 2025 (mostly Saturday Nov 16)
- **Total FBS Games:** 50-60 games
- **Ranked Teams Playing:** 18-22 teams
- **Ranked Matchups:** 12-18 games
- **Ranked vs Ranked:** 3-5 games

### Key Conferences
- **Big Ten:** Championship race continues (Ohio State, Indiana, Oregon)
- **SEC:** Crucial matchups (Georgia @ Tennessee, A&M @ Auburn)
- **Big 12:** BYU still in race (@ Arizona State)
- **ACC:** Miami potentially playing for ACC Championship spot
- **Playoff Implications:** Every ranked game matters for CFP selection

### Media Coverage
- **Major Networks:** ABC (2-3 games), ESPN (5-8 games), FOX (3-4 games)
- **Conference Networks:** SEC Network, Big Ten Network, ESPN2
- **Prime Time:** Saturday 7:30 PM ET slots likely on ABC/ESPN

---

## 🎯 SUCCESS METRICS FOR WEEK 12

### Data Quality
- ✅ 90%+ games have network information
- ✅ 100% ranked teams identified correctly
- ✅ All game times in ET timezone
- ✅ Player data covers 150+ QBs, 600+ WRs
- ✅ 8+ sportsbooks integrated per game

### System Performance
- ✅ Predictions complete in < 10 seconds
- ✅ Frontend loads in < 2 seconds
- ✅ No console errors in browser
- ✅ API responses properly formatted
- ✅ All 24 UI components render correctly

### User Experience
- ✅ Quick games show relevant Week 12 matchups
- ✅ Rankings display accurately
- ✅ Season records comprehensive
- ✅ Player impact analysis detailed
- ✅ Market comparison actionable

---

**🏈 READY FOR WEEK 12 PREDICTIONS!**

Once all items checked, system is fully operational for Week 12 college football analysis.

Last Updated: November 13, 2025
Prepared For: Week 12 (November 16, 2025 games)
Next Update: Week 13 Checklist (due November 18, 2025)
