# Week 12 Data Update Status - November 13, 2025

## ✅ **COMPLETED UPDATES**

### **Core Team Data Files (Updated from week_12 folder)**
All updated with **Nov 13, 2024** timestamps:

**Frontend & Data Directories:**
- ✅ `fbs_teams_stats_only.json` (685K) - 123 FBS teams
- ✅ `fbs_offensive_stats.json` (427K) 
- ✅ `fbs_defensive_stats.json` (374K)
- ✅ `react_power5_efficiency.json` (46K)
- ✅ `react_power5_teams.json` (16M)
- ✅ `power5_drives_only.json` (6.6M)
- ✅ `react_fbs_conferences.json` (3.3K)
- ✅ `react_fbs_team_rankings.json` (36K)

**Backtesting 2 Directory:**
- ✅ `all_fbs_ratings_comprehensive_2025_20251113_042801.json` (106K)
- ✅ `all_fbs_teams_schedules_2025_20251113_042858.json` (1.9M)
- ✅ `comprehensive_power_rankings_20251113_040210.json` (812K)
- ✅ `enhanced_power_rankings_detailed_20251113_045028.json` (277K)
- ✅ `fbs_elo_rankings_2025_20251113_042801.json` (18K)
- ✅ `fbs_fpi_rankings_2025_20251113_042801.json` (18K)
- ✅ `fbs_sp_overall_rankings_2025_20251113_042801.json` (18K)
- ✅ `fbs_srs_rankings_2025_20251113_042801.json` (18K)
- ✅ `fbs_team_stats_complete.json` (726K)

### **Player Analysis Files (Updated Nov 13, 2025)**
All in `backtesting 2/` directory:
- ✅ `comprehensive_qb_analysis_2025_20251113_034352.json` (213K)
- ✅ `comprehensive_rb_analysis_2025_20251113_034902.json` (476K)
- ✅ `comprehensive_wr_analysis_2025_20251113_034912.json` (455K)
- ✅ `comprehensive_te_analysis_2025_20251113_034910.json` (204K)
- ✅ `comprehensive_db_analysis_2025_20251113_034921.json` (1.1M)
- ✅ `comprehensive_lb_analysis_2025_20251113_034919.json` (584K)
- ✅ `comprehensive_dl_analysis_2025_20251113_034920.json` (825K)

### **Coaching Data Files (Updated Nov 3, 2025)**
- ✅ `coaches_simplified_ranked.json` (96K) - Nov 3 02:48
- ✅ `coaches_with_vsranked_stats.json` (124K) - Nov 3 04:22

### **Code Updates**
- ✅ `graphqlpredictor.py` - Updated player file paths to Nov 13 timestamps (lines 3866-3872)

---

## ⚠️ **NEEDS UPDATE - Old Data Still in Use**

### **1. complete_win_probabilities.json**
- **Current Date:** Oct 12, 2025 (5+ weeks old)
- **Location:** `frontend/src/data/complete_win_probabilities.json`
- **Size:** 279K
- **Used By:** `graphqlpredictor.py` line 1023
- **Purpose:** Historical win probability calibration
- **Action Needed:** Regenerate from GraphQL API or find Week 12 version

### **2. team_season_summaries_clean.json**
- **Current Date:** Oct 12, 2025 (5+ weeks old)
- **Location:** `frontend/src/data/team_season_summaries_clean.json`
- **Size:** 196K
- **Used By:** `graphqlpredictor.py` line 1041
- **Purpose:** Team season records, rankings, scoring averages
- **Action Needed:** Regenerate from GraphQL API or find Week 12 version

### **3. ap.json**
- **Current Date:** Nov 13, 2025 ✅
- **Status:** Has week_12 node added manually
- **Location:** `frontend/src/data/ap.json`
- **Note:** Updated manually per WEEKLY_UPDATE_CHECKLIST

---

## 📋 **TODO FOR TOMORROW**

### **Priority 1: Find or Generate Missing Files**

#### **Option A: Search for Existing Week 12 Versions**
```bash
# Search Work Computer for these files
cd "/Users/davlenswain/Desktop/Desktop - Work Computer/GameDay_Plus_Model"
find . -name "complete_win_probabilities.json" -o -name "team_season_summaries_clean.json"
```

#### **Option B: Regenerate from GraphQL API**
Need to create/find Python scripts that:

1. **complete_win_probabilities.json**
   - Query: `teamRecords` + `games` with win probability data
   - Calculate pregame/postgame win percentages
   - Historical upset detection
   
2. **team_season_summaries_clean.json**
   - Query: `teamRecords` endpoint
   - Team records, rankings, statistics
   - Season summary data

### **Priority 2: Document Generation Scripts**

**Find the Python scripts that originally created these files:**
```bash
# Search for scripts that write these JSON files
grep -r "complete_win_probabilities" --include="*.py" .
grep -r "team_season_summaries_clean" --include="*.py" .
```

**Likely script locations:**
- `/weekly_update_scripts/`
- Root directory data generation scripts
- Check `ABCNEW/` directory on Work Computer

### **Priority 3: Update Workflow Documentation**

Add to `WEEKLY_UPDATE_CHECKLIST.md`:
- Scripts that generate `complete_win_probabilities.json`
- Scripts that generate `team_season_summaries_clean.json`
- Proper sequence for regenerating all data files

---

## 🔍 **DATA FILE INVENTORY**

### **Files Updated in This Session:**
| File | Old Date | New Date | Status |
|------|----------|----------|--------|
| All player analysis (7 files) | Oct 15 | Nov 13 | ✅ Updated |
| All team stats (8 files) | Oct 12/Nov 3 | Nov 13 | ✅ Updated |
| All rankings (4 files) | Oct 31 | Nov 13 | ✅ Updated |
| Coaches files (2 files) | Oct 12 | Nov 3 | ✅ Updated |
| `complete_win_probabilities.json` | Oct 12 | Oct 12 | ❌ OLD |
| `team_season_summaries_clean.json` | Oct 12 | Oct 12 | ❌ OLD |

### **Source Locations:**
- Week 12 data: `/Users/davlenswain/Desktop/Desktop - Work Computer/GameDay_Plus_Model/ABCNEW/week_12/`
- Coaches data: `/Users/davlenswain/Desktop/Desktop - Work Computer/GameDay_Plus_Model/ABCNEW/`
- Player data: Generated by scripts in `weekly_update_scripts/` (Nov 13)

---

## ✅ **VERIFICATION COMMANDS**

```bash
# Check all file dates in data directory
ls -lh ~/Desktop/Gameday_Graphql_Model/data/*.json

# Check frontend data files
ls -lh ~/Desktop/Gameday_Graphql_Model/frontend/src/data/*.json

# Check backtesting 2 files
ls -lh ~/Desktop/Gameday_Graphql_Model/backtesting\ 2/*.json

# Test graphqlpredictor loads correctly
cd ~/Desktop/Gameday_Graphql_Model
python -c "import json; data = json.load(open('data/fbs_teams_stats_only.json')); print(f'{len(data)} teams loaded')"
```

---

## 📝 **NOTES**

- Model is currently using **Oct 12 data** for win probabilities and season summaries
- This should not significantly impact Week 12 predictions since:
  - Core team stats are current (Nov 13)
  - Player data is current (Nov 13)
  - Rankings are current (Nov 13)
- **Recommendation:** Update these 2 files before Week 13 predictions

**Created:** November 13, 2025, 4:58 AM
**Last Updated:** November 13, 2025, 4:58 AM
