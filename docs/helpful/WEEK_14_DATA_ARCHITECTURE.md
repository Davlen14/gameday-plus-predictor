# 🏈 Week 14 Data Architecture - Complete File Map

## 🎯 CRITICAL: Week 14 Prediction System Architecture

This document maps **EVERY file** that powers Week 14 predictions and how they connect to the prediction engine.

---

## 📂 THE POWER SOURCE: `weekly_updates/week_14/` (35+ MB)

**THIS FOLDER IS THE BRAIN OF WEEK 14 PREDICTIONS!** Without these files, predictions cannot run.

### 🔴 CORE PREDICTION ENGINE FILES

#### **1. Main Engine**
- **`graphqlpredictor.py`** (3,549 lines)
  - `LightningPredictor` class
  - Reads from: `fbs.json`, `Coaches.json`, `fbs_top_players_2025.json`
  - Makes GraphQL calls to College Football Data API
  - **Connects to Week 14 folder for:** Team stats, power rankings, QB analysis

#### **2. API Wrapper**
- **`app.py`** (Flask server)
  - `/predict` endpoint
  - Imports: `graphqlpredictor.py`, `prediction_validator.py`
  - Serves JSON to React frontend
  - Port: 5002

#### **3. Validation Layer**
- **`prediction_validator.py`**
  - `PredictionValidator` class
  - Validates prediction outputs
  - Fixes data inconsistencies

---

## 📊 WEEK 14 DATA FILES - FILE-BY-FILE BREAKDOWN

### 🔵 **TEAM STATISTICS (Core Data)**

#### **`react_power5_teams.json`** (20.4 MB) ⭐ MOST IMPORTANT
**Connected to:**
- `frontend/src/services/teamService.js` - Loads team data for UI
- `graphqlpredictor.py` - Cross-references with GraphQL data
- All React components that display team info

**Contains:**
- Complete team profiles for all Power 5 teams
- Season statistics, schedules, results
- Used by: Team selectors, stat displays, rankings

---

#### **`fbs_team_stats_complete.json`** (745 KB)
**Connected to:**
- `graphqlpredictor.py` - EPA calculations
- `EPAComparison.tsx` - Offensive/defensive EPA display
- `OffensiveMetrics.tsx`, `DefensiveMetrics.tsx`

**Contains:**
- Complete offensive & defensive stats
- Success rates, explosiveness metrics
- EPA per play, per drive data

---

#### **`fbs_offensive_stats.json`** (438 KB)
**Connected to:**
- `OffensiveMetrics.tsx` - Display component
- `graphqlpredictor.py` - Offensive analysis section

**Contains:**
- Yards per play, per game
- Scoring offense, red zone efficiency
- Third/fourth down conversions

---

#### **`fbs_defensive_stats.json`** (384 KB)
**Connected to:**
- `DefensiveMetrics.tsx` - Display component
- `ExtendedDefensiveAnalytics.tsx` - Advanced metrics
- `graphqlpredictor.py` - Defensive analysis

**Contains:**
- Yards allowed, points allowed
- Sacks, TFLs, turnovers forced
- Red zone defense, third down stops

---

#### **`fbs_teams_stats_only.json`** (702 KB)
**Connected to:**
- Backup data source for stats
- Used when complete stats unavailable

---

### 🟢 **POWER RANKINGS (Multiple Systems)**

#### **`comprehensive_power_rankings_*.json`** (831 KB)
**Connected to:**
- `graphqlpredictor.py` - Overall team strength assessment
- `PredictionCards.tsx` - Rankings display
- `FinalPredictionSummary.tsx` - Confidence calculations

**Contains:**
- Combined rankings from ELO, FPI, SP+, SRS
- Composite scores
- Strength of schedule adjustments

---

#### **`enhanced_power_rankings_detailed_*.json`** (306 KB)
**Connected to:**
- `frontend/src/data/` - Frontend rankings data
- `APPollRankings.tsx` - Detailed rankings view
- Used in confidence breakdown calculations

**Contains:**
- Detailed power rating breakdowns
- Offensive/defensive components
- Special teams ratings

---

#### **Individual Ranking Systems:**
- **`fbs_elo_rankings_*.json`** - ELO ratings
- **`fbs_fpi_rankings_*.json`** - ESPN FPI
- **`fbs_sp_overall_rankings_*.json`** - SP+ ratings
- **`fbs_srs_rankings_*.json`** - Simple Rating System

**All Connected to:**
- `graphqlpredictor.py` - Multi-system ranking validation
- Confidence calculations weighted across systems

---

### 🟡 **DRIVE-BY-DRIVE DATA**

#### **`power5_drives_only.json`** (8.5 MB) ⭐ CRITICAL
**Connected to:**
- `DriveEfficiency.tsx` - Drive success metrics
- `FieldPositionAnalysis.tsx` - Starting field position
- `graphqlpredictor.py` - EPA per drive calculations

**Contains:**
- Every drive from Power 5 games 2025
- Start/end field position
- Points scored, time of possession
- Drive success/failure outcomes

---

### 🟠 **QUARTERBACK ANALYSIS**

#### **`comprehensive_qb_analysis_*.json`** (232 KB)
**Connected to:**
- `PlayerImpactAnalysis.tsx` - QB efficiency display
- `graphqlpredictor.py` - QB impact section
- Player props generation

**Contains:**
- 155 QB profiles with complete stats
- Passing efficiency, completion %
- Yards per attempt, TD/INT ratio
- Rushing stats for dual-threat QBs

---

#### **QB Ranking Files:**
- **`qb_passer_rating_rankings_*.json`**
- **`qb_total_yards_rankings_*.json`**
- **`qb_dual_threat_efficiency_rankings_*.json`**
- **`qb_ball_security_score_rankings_*.json`**
- **`qb_comprehensive_efficiency_score_rankings_*.json`**

**All Connected to:**
- `PlayerImpactAnalysis.tsx` - Individual QB metrics
- Player comparison logic in predictions
- Player props recommendations

---

### 🟣 **COACHING DATA**

#### **`coaches_with_vsranked_stats.json`** (127 KB)
**Connected to:**
- `CoachingComparison.tsx` - Coach vs ranked display
- `graphqlpredictor.py` - Coaching analysis section
- Confidence adjustments for ranked matchups

**Contains:**
- Coach records vs Top 25 teams
- Win percentages by ranking tier
- Historical performance patterns

---

#### **`coaches_simplified_ranked.json`** (99 KB)
**Connected to:**
- Simplified coaching display
- Quick coach comparison metrics

---

### 🔵 **WIN PROBABILITY & PREDICTIONS**

#### **`complete_win_probabilities.json`** (285 KB)
**Connected to:**
- `FinalPredictionSummary.tsx` - Win % display
- `graphqlpredictor.py` - Historical probability models
- Confidence calculations

**Contains:**
- Win probability models by rating differential
- Historical accuracy data
- Point spread to win % conversions

---

#### **`team_season_summaries_clean.json`** (200 KB)
**Connected to:**
- `HistoricalPerformance.tsx` - Season summary display
- `GameSummaryRationale.tsx` - Context for predictions
- Trend analysis in predictions

**Contains:**
- Season record, key wins/losses
- Strength of schedule
- Performance trends by month
- Notable game results

---

### 🟢 **REACT UI DATA FILES**

#### **`react_fbs_team_rankings.json`** (37 KB)
**Connected to:**
- `frontend/src/components/figma/PredictionCards.tsx`
- Team ranking displays throughout UI

---

#### **`react_power5_efficiency.json`** (49 KB)
**Connected to:**
- `ComprehensiveMetricsDashboard.tsx`
- Efficiency metric displays

---

#### **`react_fbs_conferences.json`** (3 KB)
**Connected to:**
- `TeamSelector.tsx` - Conference filtering
- Conference-based analysis

---

### 🔴 **SCHEDULES & MATCHUPS**

#### **`all_fbs_teams_schedules_2025_*.json`** (2 MB)
**Connected to:**
- `CommonOpponents.tsx` - Common opponent analysis
- `HistoricalPerformance.tsx` - H2H history
- `graphqlpredictor.py` - Strength of schedule calculations

**Contains:**
- Full 2025 season schedules for all FBS teams
- Game results, scores, locations
- Home/away/neutral site data

---

### 🟠 **RANKINGS & POLLS**

#### **`ap.json`** (40 KB)
**Connected to:**
- `APPollRankings.tsx` - AP Poll display
- `graphqlpredictor.py` - Ranking context
- Confidence boost for ranked teams

**Contains:**
- Current AP Top 25 rankings
- First-place votes
- Points received

---

### 🔵 **COMPOSITE RATINGS**

#### **`all_fbs_ratings_comprehensive_*.json`** (80 KB)
**Connected to:**
- `graphqlpredictor.py` - Multi-system validation
- Confidence calculations across rating systems

**Contains:**
- All major rating systems combined
- ELO, FPI, SP+, SRS in one file
- Used for cross-validation

---

## 🔗 HOW FILES CONNECT TO PREDICTION FLOW

### **Prediction Request Flow:**
```
User selects teams in React UI
    ↓
TeamSelector.tsx → reads from react_power5_teams.json
    ↓
Sends POST request to Flask API (app.py)
    ↓
app.py calls graphqlpredictor.py
    ↓
LightningPredictor.predict_game() executes:
    ├─ Loads fbs.json, Coaches.json
    ├─ Makes GraphQL API calls
    ├─ Reads weekly_updates/week_14/*.json files:
    │   ├─ react_power5_teams.json (team data)
    │   ├─ fbs_team_stats_complete.json (stats)
    │   ├─ comprehensive_power_rankings_*.json (rankings)
    │   ├─ power5_drives_only.json (drive data)
    │   ├─ comprehensive_qb_analysis_*.json (QB stats)
    │   ├─ coaches_with_vsranked_stats.json (coaching)
    │   └─ complete_win_probabilities.json (models)
    ↓
Returns 18 analysis sections as JSON
    ↓
app.py formats and returns to frontend
    ↓
React components display data:
    ├─ PredictionCards.tsx
    ├─ FinalPredictionSummary.tsx
    ├─ EPAComparison.tsx
    ├─ CoachingComparison.tsx
    ├─ PlayerImpactAnalysis.tsx
    └─ (22 other components)
```

---

## ⚠️ CRITICAL DEPENDENCIES

### **Without These Files, Predictions FAIL:**
1. ✅ `fbs.json` - Team IDs/names
2. ✅ `Coaches.json` - Coaching data
3. ✅ `fbs_top_players_2025.json` - Player database
4. ✅ `weekly_updates/week_14/react_power5_teams.json` - MOST CRITICAL (20MB)
5. ✅ `weekly_updates/week_14/fbs_team_stats_complete.json` - Team stats
6. ✅ `weekly_updates/week_14/power5_drives_only.json` - Drive data
7. ✅ `weekly_updates/week_14/comprehensive_power_rankings_*.json` - Rankings
8. ✅ `weekly_updates/week_14/comprehensive_qb_analysis_*.json` - QB data
9. ✅ `weekly_updates/week_14/coaches_with_vsranked_stats.json` - Coach stats

### **Frontend Dependencies:**
- All 24 Figma components in `frontend/src/components/figma/`
- `frontend/src/services/teamService.js` - Team data loader
- `frontend/src/store.js` - State management

---

## 📝 DEPLOYMENT CHECKLIST

**For Genspark or any deployment, MUST include:**

### Backend:
- [ ] `graphqlpredictor.py`
- [ ] `app.py`
- [ ] `prediction_validator.py`
- [ ] `fbs.json`
- [ ] `Coaches.json`
- [ ] `fbs_top_players_2025.json`
- [ ] **ENTIRE `weekly_updates/week_14/` folder** (35MB)
- [ ] `requirements.txt`
- [ ] `runtime.txt`

### Frontend:
- [ ] `frontend/src/App.tsx`
- [ ] `frontend/src/main.tsx`
- [ ] `frontend/src/store.js`
- [ ] `frontend/src/services/teamService.js`
- [ ] **All 24 components** in `frontend/src/components/figma/`
- [ ] `frontend/package.json`
- [ ] `frontend/vite.config.js`
- [ ] `frontend/tailwind.config.js`

---

## 🚀 WHY WEEK 14 FOLDER IS CRITICAL

**Size:** 35+ MB of data
**Files:** 29 comprehensive data files
**Purpose:** Powers ALL Week 14 predictions

**Without this folder:**
- ❌ No team statistics
- ❌ No power rankings
- ❌ No QB analysis
- ❌ No drive efficiency data
- ❌ No coaching performance data
- ❌ Predictions will be incomplete or fail

**THIS FOLDER MUST BE INCLUDED IN ANY DEPLOYMENT!**

---

## 📊 Data Flow Summary

```
Week 14 Folder (35MB) 
    ↓
graphqlpredictor.py (3,549 lines)
    ↓
app.py (Flask API)
    ↓
React Frontend (24 components)
    ↓
User sees comprehensive prediction
```

**Every prediction uses 27+ data sources from Week 14 folder!**

---

*Last Updated: December 1, 2025*
*Architecture: Gameday+ College Football Prediction Platform*
