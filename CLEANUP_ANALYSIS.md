# 🧹 Gameday+ Project Cleanup Analysis

## 📊 Current State

**Project Size:** 2.8GB  
**JSON Files:** 489 files  
**CSV Files:** 267 files  

### Largest Data Directories:
- `weekly_updates/`: **130MB** (duplicates + old weekly snapshots)
- `data_generators/`: **84MB** (build artifacts, duplicates)
- `data/`: **28MB** (old data files)
- `frontend/src/data/`: **26MB** (React app data)

### Largest Individual Files:
- `react_power5_teams.json`: **21MB** (6 duplicate copies!)
- `power5_drives_complete.json`: **9.6MB** (5 duplicate copies!)
- `comprehensive_team_game_stats.json`: **8.7MB** (duplicates)
- `defensive_leaders_2025.json`: **15MB**

---

## 🗄️ Database Migration Status

**All data is now in `predictions.db`:**
- ✅ `drives_complete` table (replaces drive JSON/CSV files)
- ✅ `player_metrics_data` table (replaces player JSON files)
- ✅ `team_offensive_stats` & `team_defensive_stats` (replaces team JSON files)
- ✅ `comprehensive_power_rankings` (replaces rankings JSON)
- ✅ `upcoming_games` + `sportsbook_lines` (replaces betting JSON)
- ✅ `historical_game_results` (replaces historical data)

---

## 🎯 Cleanup Targets

### 🔴 HIGH PRIORITY - Safe to Delete (240MB+ savings)

#### Duplicate JSON Files (Most Critical)
```
weekly_updates/week_15/react_power5_teams.json (21MB)
weekly_updates/week_15/react_power5_teams 2.json (21MB)
data_generators/team_stats/react_power5_teams.json (21MB)
data_generators/team_stats/react_power5_teams 2.json (21MB)
frontend/src/data/react_power5_teams.json (16MB) - KEEP ONE COPY ONLY IF USED BY REACT
data/react_power5_teams.json (16MB)
```

#### Drive Data (Already in DB)
```
data_generators/team_stats/power5_drives_complete.json (9.6MB)
data_generators/team_stats/power5_drives_complete 2.json (9.6MB)
weekly_updates/week_15/power5_drives_only.json (8.8MB)
weekly_updates/week_15/power5_drives_only 2.json (8.8MB)
data/power5_drives_only.json (8.8MB)
data_generators/team_stats/power5_drives_only.json (8.8MB)
data_generators/team_stats/power5_drives_only 2.json (8.8MB)
frontend/src/data/power5_drives_only.json (6.6MB)
```

#### Team Stats (Already in DB)
```
weekly_updates/week_15/comprehensive_team_game_stats.json (8.7MB)
weekly_updates/week_15/comprehensive_team_game_stats 2.json (8.7MB)
weekly_updates/week_15/clean_team_game_stats.json (4.1MB)
weekly_updates/week_15/clean_team_game_stats 2.json (4.1MB)
weekly_updates/week_15/team_season_stats_2025.json (1.4MB)
weekly_updates/week_15/fbs_team_stats_complete.json (728K)
weekly_updates/week_15/fbs_team_stats_complete 2.json (728K)
```

#### Player Stats (Already in DB)
```
weekly_updates/week_15/defensive_leaders_2025.json (15MB)
weekly_updates/week_15/receiving_leaders_2025.json (5.5MB)
weekly_updates/week_15/rushing_leaders_2025.json (4.3MB)
weekly_updates/week_15/passing_leaders_2025.json (1.9MB)
```

#### Old Player Metrics Directory
```
player_metrics/ - All comprehensive analysis JSON files (already in player_metrics_data table)
```

### 🟡 MEDIUM PRIORITY - Review First

#### CSV Files (267 files)
```
drives/*.csv (260+ empty files - 0B each)
game_analysis/*.csv (old game analysis)
json_data/*.csv (old predictions)
```

#### Miscellaneous
```
army_navy_matchup.json
washington_boise_q*.json
Coaches.json (if data in coaches_master.db)
```

### 🟢 KEEP - Still Required

```
fbs.json - ✅ Used by frontend (team metadata)
package.json - ✅ npm dependencies
package-lock.json - ✅ npm lock
railway.json - ✅ deployment config
n8n_gameday_workflow.json - ✅ automation
tsconfig.json - ✅ TypeScript config
```

---

## 📈 Expected Impact

### Space Savings:
- **JSON cleanup**: ~200MB
- **CSV cleanup**: ~250KB (mostly empty files)
- **Duplicate removal**: ~100MB
- **Total savings**: ~300MB (11% reduction)

### Performance Improvements:
- ✅ Faster git operations
- ✅ Reduced deployment size
- ✅ Cleaner codebase
- ✅ No JSON file dependencies in graphqlpredictor.py

---

## ⚠️ Pre-Cleanup Checklist

Before deleting files, verify:
1. ✅ All data tables populated in predictions.db
2. ✅ graphqlpredictor.py uses database only (no JSON imports)
3. ✅ betting_lines_manager.py prioritizes database
4. ✅ Frontend uses fbs.json (keep this)
5. ✅ Backup database files before cleanup
6. ⚠️ Check if react_power5_teams.json used by React app

---

## 🔍 Code References Found

**react_power5_teams / power5_drives references in Python:** 82 occurrences  
**CSV file references in Python:** 434 occurrences

**Action Required:** Verify these references are using database tables, not JSON/CSV files.

---

## 📝 Recommended Cleanup Commands

```bash
# Backup first!
cp -r instance instance_backup_$(date +%Y%m%d)

# Remove duplicate JSON files
rm -f weekly_updates/week_15/*" 2.json"
rm -f data_generators/team_stats/*" 2.json"

# Remove old data directories (data now in DB)
rm -rf weekly_updates/week_15/defensive_leaders_2025.json
rm -rf weekly_updates/week_15/receiving_leaders_2025.json
rm -rf weekly_updates/week_15/rushing_leaders_2025.json
rm -rf weekly_updates/week_15/passing_leaders_2025.json
rm -rf weekly_updates/week_15/comprehensive_team_game_stats*.json
rm -rf weekly_updates/week_15/power5_drives*.json

# Remove empty CSV files
find drives/ -name "*.csv" -size 0 -delete

# Remove old analysis CSVs
rm -rf game_analysis/*.csv json_data/*.csv

# Remove unused JSON files
rm -f army_navy_matchup.json washington_boise*.json

# Verify frontend still works after cleanup!
```

---

---

## 🎨 React Component JSON Audit

### ✅ KEEP - Essential Frontend Files

**1. fbs.json (45KB)** - **MUST KEEP**
- Used by: `App.tsx`, `teamUtils.ts`, `TeamSelector.tsx`, `CoachTimeline.tsx`, `MetricsHeatMap.tsx`, `EVBettingDashboard.tsx`, `teamService.js`
- Purpose: Team metadata (logos, colors, mascots, abbreviations)
- Status: ✅ **ACTIVE** - Core dependency for team display

### 🔴 DELETE - Coach Data (Should Use API Instead)

**frontend/src/data/coach files (280KB total):**
- ❌ `lane_kiffin_master.json` (93KB) - Used by `CoachAnalysisPage.tsx`
- ❌ `james_franklin_master.json` (96KB) - Used by `CoachAnalysisPage.tsx`  
- ❌ `coaches_advanced_rankings.json` (233KB) - Used by `CoachAnalysisPage.tsx`
- ❌ `coach_timelines/kiffin_ole_miss_FULL_timeline.json` - Used by `CoachAnalysisPage.tsx`
- ❌ `coach_timelines/franklin_penn_state_timeline.json` - Used by `CoachAnalysisPage.tsx`

**Why delete:**
- ✅ **API exists:** `app_master.py` has `/api/coach/<id>` endpoints (port 5555)
- ✅ Hardcoded coach data becomes stale
- ✅ Database has fresh coach data in `coaches_master.db`

**Migration Required:**
- Update `CoachAnalysisPage.tsx` to fetch from API instead of importing JSON
- Remove hardcoded Lane Kiffin / James Franklin data

### 🔴 DELETE - Team Stats (Duplicates Database)

**frontend/src/data/stats files (2.6MB total):**
- ❌ `fbs_defensive_stats.json` (374KB)
- ❌ `fbs_offensive_stats.json` (427KB)
- ❌ `fbs_team_stats_complete.json` (726KB)
- ❌ `fbs_teams_stats_only.json` (685KB)
- ❌ `react_fbs_team_rankings.json` (36KB)
- ❌ `react_power5_efficiency.json` (46KB)
- ❌ `team_season_summaries_clean.json` (196KB)
- ❌ `complete_win_probabilities.json` (279KB)

**Why delete:**
- Database tables: `team_offensive_stats`, `team_defensive_stats`, `comprehensive_power_rankings`
- No React components actively using these (checked all imports)

### 🔴 DELETE - Drives Data (22MB!)

**frontend/src/data/power5_drives_only.json (6.6MB)**
- Status: ❌ **NOT USED** in any React component
- Database equivalent: `drives_complete` table (11,507 rows)
- **Immediate deletion candidate**

### 🔴 DELETE - Massive Team File (16MB!)

**frontend/src/data/react_power5_teams.json (16MB)**
- Status: ❌ **NOT USED** in any React component (uses `fbs.json` instead)
- This is a **duplicate** of the 21MB files in other directories
- **High priority deletion** - saves 16MB instantly

### 🟡 NEEDS REVIEW - Coach Headshots

**power5_coaches_headshots.json (34KB)**
- Used by: `coachService.ts` for `getCoachHeadshot()` function
- Contains: Coach headshot URLs by conference
- Decision: Keep for now OR migrate to database `coaches_master.db`

### 🟡 NEEDS REVIEW - Small Config Files

**frontend/src/data/misc files (150KB):**
- `ap.json` (51KB) - AP Poll data
- `coaches_enhanced_stats.json` (65KB)
- `coaches_simplified_ranked.json` (96KB)
- `coaches_with_vsranked_stats.json` (124KB)
- `react_fbs_conferences.json` (3.3KB)

Status: No active imports found, likely safe to delete

---

## 📊 React Component Cleanup Summary

| Category | Files | Size | Action |
|----------|-------|------|--------|
| **Essential (Keep)** | fbs.json | 45KB | ✅ Keep |
| **Coach JSON (Delete)** | 5+ files | 280KB | 🔴 Migrate to API |
| **Team Stats (Delete)** | 8 files | 2.6MB | 🔴 Delete |
| **Drives Data (Delete)** | 1 file | 6.6MB | 🔴 Delete |
| **Massive Duplicate (Delete)** | 1 file | 16MB | 🔴 Delete NOW |
| **Coach Headshots (Review)** | 1 file | 34KB | 🟡 Keep/Migrate |
| **Small Configs (Review)** | 5 files | 150KB | 🟡 Probably Delete |

**Total frontend/src/data/ savings: ~25MB (96% of directory)**

---

## 🚨 Action Required: CoachAnalysisPage.tsx Migration

**Current (hardcoded JSON):**
```tsx
import laneKiffinData from '../../data/lane_kiffin_master.json';
import jamesFranklinData from '../../data/james_franklin_master.json';
```

**Should be (dynamic API):**
```tsx
const [coachData, setCoachData] = useState(null);

useEffect(() => {
  fetch(`http://localhost:5555/api/coach/${coachId}`)
    .then(res => res.json())
    .then(data => setCoachData(data));
}, [coachId]);
```

---

## 🎯 COPY THIS PROMPT FOR AI CLEANUP

