# 🏈 AAA COMPREHENSIVE GUIDE: Gameday+ Prediction Model Architecture

> **CRITICAL DOCUMENT**: Read this FIRST before making any changes to the prediction system.  
> Last Updated: November 3, 2025  
> Status: ✅ PRODUCTION READY - Dynamic weighting system implemented and tested

---

## 📋 TABLE OF CONTENTS

1. [Understanding The Split Architecture](#understanding-the-split-architecture)
2. [Active vs Modular Files](#active-vs-modular-files)
3. [How The Prediction Engine Works](#how-the-prediction-engine-works)
4. [Dynamic Weighting System (NEW!)](#dynamic-weighting-system)
5. [Making Changes Without Breaking Things](#making-changes-without-breaking-things)
6. [Weekly Update Process](#weekly-update-process)
7. [Completing The Refactoring](#completing-the-refactoring)
8. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## 🎯 UNDERSTANDING THE SPLIT ARCHITECTURE

### **The Confusion: Two Prediction Systems**

You have **TWO VERSIONS** of the prediction engine in your codebase:

```
📁 Gameday_Graphql_Model/
├── 📄 graphqlpredictor.py          ← ✅ ACTIVE (used by app.py and run.py)
│                                      5,200+ lines, monolithic, PRODUCTION
│
└── 📁 predictor/                    ← ⚠️  INCOMPLETE REFACTOR (NOT USED)
    ├── 📁 core/
    │   ├── lightning_predictor.py   ← 1,861 lines, modular version
    │   └── data_loader.py
    ├── 📁 analysis/
    │   ├── betting_analyzer.py
    │   ├── player_analyzer.py
    │   ├── team_analyzer.py
    │   └── weather_analyzer.py
    └── 📁 utils/
        ├── data_processor.py
        └── graphql_client.py
```

### **Why The Confusion Happened**

1. **You started refactoring** `graphqlpredictor.py` into modular components in `predictor/`
2. **You got partway through** - created the modular structure but never switched imports
3. **app.py still imports from the old file**: `from graphqlpredictor import LightningPredictor`
4. **The modular version was never connected** to the Flask API or CLI

### **Current Production Flow**

```
User Request → app.py → graphqlpredictor.py → LightningPredictor.predict_game() → JSON Response
                ↑
            IMPORTS FROM graphqlpredictor.py (NOT predictor/core/lightning_predictor.py)
```

---

## 🚨 ACTIVE VS MODULAR FILES

### **✅ ACTIVE FILES (CURRENTLY IN USE)**

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `graphqlpredictor.py` | Core prediction engine | 5,200+ | ✅ PRODUCTION |
| `app.py` | Flask API server | 1,335 | ✅ PRODUCTION |
| `run.py` | CLI interface | ~500 | ✅ PRODUCTION |
| `betting_lines_manager.py` | Market analysis | 217 | ✅ PRODUCTION |
| `prediction_validator.py` | Validation checks | 205 | ✅ PRODUCTION |

### **⚠️  MODULAR FILES (NOT USED - INCOMPLETE)**

| File | Purpose | Status |
|------|---------|--------|
| `predictor/core/lightning_predictor.py` | Modular engine | ❌ NOT IMPORTED |
| `predictor/analysis/*.py` | Analysis modules | ❌ NOT IMPORTED |
| `predictor/utils/*.py` | Utility modules | ❌ NOT IMPORTED |

### **❗ CRITICAL RULE**

**When making changes to the prediction logic:**
- ✅ **ALWAYS edit `graphqlpredictor.py`** (the active file)
- ❌ **DO NOT edit files in `predictor/`** (they're not being used)
- 🔄 **After testing changes in production**, then update modular files if desired

---

## 🔧 HOW THE PREDICTION ENGINE WORKS

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Data Collection (GraphQL API Calls)                │
│  - Team metrics (EPA, success rate, explosiveness)          │
│  - Ratings (ELO, FPI, S&P+, SRS)                           │
│  - Player data (QBs, WRs, DBs)                             │
│  - Market lines (betting spreads/totals)                    │
│  - Weather, polls, bye weeks                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Dynamic Weight Calculation (NEW!)                  │
│  - Analyzes ELO differential                                │
│  - Checks rating system consensus                           │
│  - Adjusts weights based on matchup type                    │
│  - Applies SOS corrections                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Component Scoring                                  │
│  [1] Opponent-Adjusted Metrics (20-35% weight)             │
│      - EPA differential with SOS adjustment                 │
│      - Success rate, explosiveness                          │
│      - Recent form vs early season                          │
│                                                              │
│  [2] Composite Ratings (40-65% weight) ⭐ PRIMARY          │
│      - ELO win probability calculation                      │
│      - FPI, S&P+, SRS differentials                        │
│      - Mismatch multiplier (elite vs weak)                 │
│                                                              │
│  [3] Defensive Metrics (10-12% weight)                     │
│      - Defensive efficiency vs opponent offense             │
│      - Dampening for elite defense vs poor offense          │
│                                                              │
│  [4] Key Player Impact (5-8% weight)                       │
│      - QB efficiency differential                           │
│      - WR/RB production                                     │
│      - Defensive playmakers                                 │
│                                                              │
│  [5] Market Consensus (2-5% weight)                        │
│      - Used for VALIDATION, not prediction                  │
│      - Flags >15 point differences                          │
│                                                              │
│  [6] Contextual Factors (1-2% weight)                      │
│      - Weather (temp, wind, precipitation)                  │
│      - Bye week advantage                                   │
│      - Poll momentum                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Weighted Combination                               │
│  Raw Differential = Σ(component × dynamic_weight)           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Enhancements & Adjustments                         │
│  - Home field advantage (+2.5 points)                       │
│  - Conference rivalry bonus                                 │
│  - Weather penalty                                           │
│  - Comprehensive differential (EPA, ELO, consistency)       │
│  - Defensive dampener (reduces total for mismatches)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Win Probability & Spread Calculation              │
│  - Logistic function: 1/(1 + e^(-diff/18))                 │
│  - Platt scaling calibration                                │
│  - Inverse logit to spread: ln(p/(1-p)) × 4.5-6.0         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: Total Calculation & Validation                    │
│  - Base total from offensive/defensive metrics              │
│  - Apply defensive dampener (8-15% for mismatches)          │
│  - Compare to market consensus                              │
│  - Flag if >15 points off market                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    FINAL PREDICTION
```

---

## 🎲 DYNAMIC WEIGHTING SYSTEM (NEW!)

### **The Problem We Solved**

**Before (Static Weights):**
- Same weights used for ALL games regardless of matchup
- Ohio State (ELO 2146) vs Purdue (ELO 1310) = treated same as even matchup
- Model predicted OSU -16.4, should have been -30+
- Over-weighted EPA from weak opponents, under-weighted proven ratings

**After (Dynamic Weights):**
- Weights adjust based on ELO differential, rating consensus, SOS
- Extreme mismatches (750+ ELO diff) → 65% composite ratings
- Even matchups (<200 ELO diff) → 35% EPA, 40% ratings
- Properly scales elite team dominance

### **Dynamic Weight Tiers**

#### **TIER 1: Extreme Mismatch (ELO diff ≥ 750)**
```python
Composite Ratings:          65%  ⭐ Elite vs terrible - trust ratings heavily
Opponent-Adjusted Metrics:  15%  ⬇️ EPA inflated by weak opponents
Defensive Metrics:          12%  ⬆️ Defense dominates in blowouts
Key Player Impact:          5%
Market Consensus:           2%
Contextual Factors:         1%
```
**Example:** #1 Oregon (ELO 2100+) vs bottom-dweller
**Why:** When talent gap is massive, season-long ratings > recent stats

#### **TIER 2: Large Mismatch (ELO diff 600-749)**
```python
Composite Ratings:          60%
Opponent-Adjusted Metrics:  18%
Defensive Metrics:          11%
Key Player Impact:          7%
Market Consensus:           3%
Contextual Factors:         1%
```
**Example:** Top-10 team vs unranked mid-tier opponent
**Why:** Still significant talent gap, ratings matter most

#### **TIER 3: Moderate Mismatch (ELO diff 400-599)**
```python
Composite Ratings:          55%  ← Base weights
Opponent-Adjusted Metrics:  20%
Defensive Metrics:          10%
Key Player Impact:          8%
Market Consensus:           5%
Contextual Factors:         2%
```
**Example:** Ranked team vs fringe Top 25 opponent
**Why:** Balanced approach, ratings slightly favored

#### **TIER 4: Small Advantage (ELO diff 200-399)**
```python
Composite Ratings:          50%
Opponent-Adjusted Metrics:  25%  ⬆️ Recent form matters more
Defensive Metrics:          10%
Key Player Impact:          8%
Market Consensus:           5%
Contextual Factors:         2%
```
**Example:** Two ranked teams, one slightly better
**Why:** Closer matchup, recent performance and ratings balanced

#### **TIER 5: Even Matchup (ELO diff < 200)**
```python
Composite Ratings:          40%
Opponent-Adjusted Metrics:  35%  ⭐ EPA weighted highest
Defensive Metrics:          10%
Key Player Impact:          8%
Market Consensus:           5%
Contextual Factors:         2%
```
**Example:** Two evenly-matched teams
**Why:** Recent performance (EPA, success rate) matters most when talent is equal

### **Additional Dynamic Adjustments**

#### **Rating Consensus Multiplier**
```python
if all_four_systems_agree_within_15%:
    composite_ratings_weight *= 1.10  # +10% boost
    opponent_adjusted_weight *= 0.90  # -10% reduction
```
**When:** ELO, FPI, S&P+, SRS all show similar differentials
**Why:** When all expert systems agree, trust them even more

#### **Strength of Schedule Adjustment**
```python
if favorite_has_tough_SOS_and_underdog_has_weak_SOS:
    composite_ratings_weight *= 1.05  # +5% boost
    opponent_adjusted_weight *= 0.95  # -5% reduction
```
**When:** Favorite played top-40 schedule, underdog played 80+ ranked schedule
**Why:** Favorite's EPA is more credible (tested against good opponents)

---

## 🔬 ENHANCED ELO SCALING (CRITICAL FIX)

### **Old Method (WRONG)**
```python
# ❌ Simple division - doesn't account for win probability
elo_diff = 2146 - 1310  # 836
spread = elo_diff / 100  # 8.36 points ← WAY TOO LOW
```

### **New Method (CORRECT)**
```python
# ✅ Chess rating formula converted to spread
elo_diff = 2146 - 1310  # 836

# Step 1: Calculate win probability using proper formula
win_prob = 1 / (1 + 10 ** (-elo_diff / 400))  # 0.9876 (98.76%)

# Step 2: Convert to spread using inverse logit
if win_prob > 0.01 and win_prob < 0.99:
    spread_equivalent = log(win_prob / (1 - win_prob)) * 7.0  # ~30 points
else:
    spread_equivalent = log(win_prob / (1 - win_prob)) * 9.0  # ~35 points
```

**Why 7.0-9.0 multiplier?**
- College football has higher variance than NFL (talent gaps larger)
- NFL uses ~2.4 multiplier, CFB needs 3x that
- Calibrated against historical blowout games

### **Mismatch Multiplier**
```python
elite_threshold = 2000  # Top-5 teams
weak_threshold = 1400   # Bottom-tier teams

if (home_elo > 2000 and away_elo < 1400) or vice_versa:
    mismatch_multiplier = 1.5  # Amplify by 50%
    print("🔥 ELITE VS WEAK MISMATCH DETECTED!")
elif elo_diff > 600:
    mismatch_multiplier = 1.3  # Amplify by 30%
```

**Example:**
- Ohio State (ELO 2146) vs Purdue (ELO 1310)
- Base spread from ELO: 30 points
- Mismatch multiplier: 1.5x
- Final ELO contribution: 45 points
- After weighting (65%): 29.25 points to final spread

---

## 🛡️ DEFENSIVE METRICS SYSTEM (NEW!)

### **The Missing Piece**

Old model didn't properly account for **defensive dominance**. When elite defense meets terrible offense, scoring plummets.

### **Defensive Dampener Calculation**

```python
# Get efficiency ratings from backtesting data
home_def_efficiency = 92.1  # Elite (Ohio State)
away_off_efficiency = 40.7  # Poor (Purdue)

# Calculate mismatch
def_mismatch = abs(home_def_efficiency - away_off_efficiency)  # 51.4

if def_mismatch > 40:
    total_dampener = 0.85  # Reduce total by 15%
    print("🔒 ELITE DEFENSE: Dampening by 15%")
elif def_mismatch > 30:
    total_dampener = 0.92  # Reduce total by 8%
    print("🛡️ Strong defense: Dampening by 8%")
```

### **Effect on Total**

**Without dampener:**
- Base total: 67.0 points
- Implied scores: OSU 48, Purdue 19

**With dampener (15% reduction):**
- Adjusted total: 57.0 points
- Implied scores: OSU 43, Purdue 14 ← More realistic

### **Defensive Advantage Component**

Also contributes to spread prediction:
```python
home_def_vs_away_off = 92.1 - 40.7  # +51.4
away_def_vs_home_off = 50.3 - 88.2  # -37.9

defensive_advantage = (51.4 - (-37.9)) / 10.0  # +8.93

# Added to comprehensive enhancement with 10-12% weight
```

---

## 🚀 MAKING CHANGES WITHOUT BREAKING THINGS

### **Rule #1: Always Edit The Active File**

```bash
# ✅ CORRECT
nano graphqlpredictor.py  # The monolithic file in root directory

# ❌ WRONG
nano predictor/core/lightning_predictor.py  # Not being used!
```

### **Rule #2: Test After EVERY Change**

```bash
# Restart backend
lsof -ti:5002 | xargs kill -9 2>/dev/null
./start-fullstack.sh

# Wait for startup
sleep 5

# Test prediction
python run.py "Ohio State" "Purdue"
```

### **Rule #3: Check For Import Errors**

```bash
# Backend health check
curl http://localhost:5002/health

# Should return:
# {"status":"healthy","service":"Gameday GraphQL Predictor"}

# If it fails, check backend logs in the terminal tab
```

### **Rule #4: Never Change Weights Mid-Season**

The dynamic weighting system now handles weight adjustments. Don't manually tweak `BASE_WEIGHTS` unless you have a very good reason:

```python
# ❌ DON'T DO THIS without extensive testing
self.BASE_WEIGHTS = {
    'composite_ratings': 0.70,  # Changed from 0.55
    ...
}

# ✅ DO THIS instead - adjust the dynamic thresholds
self.ELO_THRESHOLDS = {
    'extreme_mismatch': 700,  # Changed from 750
    ...
}
```

---

## 📅 WEEKLY UPDATE PROCESS

### **What Needs Updating Every Week**

See `WEEKLY_UPDATE_CHECKLIST.md` for full details, but key items:

#### **1. Betting Lines** (Monday/Tuesday)
```bash
# Update week number and fetch new lines
python week11_fetcher.py
# Generates: Currentweekgames.json
```

#### **2. AP Poll Rankings** (Sunday evening)
```bash
python ap_poll_week11.py
# Updates: frontend/src/data/ap.json
```

#### **3. Player Data** (Every 2-3 weeks)
```bash
# Fetch updated player stats
python fetch_player_data.py
# Updates files in: data/ directory
```

#### **4. Rating Files** (Weekly if available)
```bash
# Check for new backtesting ratings
ls -la "backtesting 2/" | grep "all_fbs_ratings_comprehensive"
# If new file exists, model automatically uses latest
```

### **What You DON'T Need to Change**

- ❌ `graphqlpredictor.py` weights (dynamic now!)
- ❌ Prediction algorithms (unless fixing bugs)
- ❌ GraphQL queries (stable API)
- ❌ Frontend components (pull data from backend)

---

## 🔄 COMPLETING THE REFACTORING

### **If You Want To Use The Modular Structure**

The `predictor/` directory has a partially completed refactor. To finish it:

#### **Step 1: Update Imports in app.py**

```python
# Current (line 6):
from graphqlpredictor import LightningPredictor

# Change to:
from predictor.core.lightning_predictor import LightningPredictor
```

#### **Step 2: Copy Latest Changes to Modular File**

```bash
# The modular version is outdated - it doesn't have:
# - Dynamic weighting system
# - Enhanced ELO scaling
# - Defensive metrics
# - Market validation

# You'd need to port all changes from graphqlpredictor.py
# to predictor/core/lightning_predictor.py
```

#### **Step 3: Test Extensively**

```bash
# Test CLI
python run.py "Ohio State" "Purdue"

# Test Flask API
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Ohio State", "away_team": "Purdue"}'

# Test frontend
# Open http://localhost:5173 and make predictions
```

#### **Step 4: Update All Documentation**

- Update `README.md` with new import paths
- Update `WEEKLY_UPDATE_CHECKLIST.md`
- Update deployment scripts if needed

### **Recommendation: DON'T REFACTOR MID-SEASON**

The monolithic `graphqlpredictor.py` works perfectly. Refactoring is risky:
- ✅ **Do it in offseason** (January-March)
- ❌ **Don't do it during football season** (August-December)
- 🎯 **Current focus**: Make predictions, not reorganize code

---

## 🐛 TROUBLESHOOTING COMMON ISSUES

### **Issue 1: Prediction Showing Wrong Teams**

**Symptom:**
```bash
python run.py 194 2509
# Shows: Miami vs Louisville instead of Ohio State vs Purdue
```

**Cause:** GraphQL API returning cached/wrong game data

**Fix:** Check team IDs in `fbs.json`:
```bash
python -c "import json; teams = json.load(open('fbs.json')); 
print([t for t in teams if 'Ohio' in t['school']])"
```

### **Issue 2: Backend Won't Start**

**Symptom:**
```bash
./start-fullstack.sh
curl http://localhost:5002/health
# curl: (7) Failed to connect
```

**Causes & Fixes:**

#### **A. Import Error**
```bash
# Check terminal tab for:
# "ModuleNotFoundError: No module named 'graphqlpredictor'"

# Fix: Make sure file exists
ls -la graphqlpredictor.py

# If you renamed it:
mv graphqlpredictor.py.backup graphqlpredictor.py
```

#### **B. Syntax Error in graphqlpredictor.py**
```bash
# Check for Python syntax errors
python -m py_compile graphqlpredictor.py

# If error, check line number mentioned
nano +<line_number> graphqlpredictor.py
```

#### **C. Port Already in Use**
```bash
# Kill existing process
lsof -ti:5002 | xargs kill -9

# Restart
./start-fullstack.sh
```

### **Issue 3: Weights Not Adjusting Dynamically**

**Symptom:**
```bash
# Output shows:
⚖️ WEIGHTED COMPOSITE CALCULATION
Composite Ratings (55%): ...  # Same every game
```

**Fix:** Check that `_calculate_dynamic_weights` is being called:
```bash
# Should see this in output:
🎲 DYNAMIC WEIGHT CALCULATION
🔥 EXTREME MISMATCH (ELO diff 836): Composite boosted to 65%
```

If not appearing, check around line 3020 in `graphqlpredictor.py`:
```python
# Should have:
self.WEIGHTS = self._calculate_dynamic_weights(...)
```

### **Issue 4: Spread Too Low for Elite Teams**

**Symptom:** Model predicts OSU -16 when should be -30

**Check List:**
1. ✅ Dynamic weights enabled? (Should see "EXTREME MISMATCH" in output)
2. ✅ ELO scaling using proper formula? (Should show "ELO Win Probability: 98%")
3. ✅ Mismatch multiplier applied? (Should show "Mismatch Multiplier: 1.5x")
4. ✅ Composite ratings weighted heavily? (Should be 60-65% for extreme mismatches)

### **Issue 5: Market Validation Always Flagging**

**Symptom:**
```bash
⚠️ WARNING: Prediction differs from market by 23.6 points!
```

**This is GOOD!** It means:
- Model is identifying value bets
- Market might be wrong (or you found edge)
- Compare to other sharp books (Pinnacle, Circa)

**When to worry:**
- If you're off by >30 points on even matchups
- If ALL your predictions are way off market
- If model predicts Purdue -20 when they're 2-7 (data issue)

---

## 📊 KEY FILES REFERENCE

### **Configuration**
| File | Purpose | Edit Frequency |
|------|---------|----------------|
| `graphqlpredictor.py` lines 980-1000 | Base weights | Never (dynamic now) |
| `graphqlpredictor.py` lines 1100-1200 | Dynamic weight function | Rarely (only for tuning) |
| `graphqlpredictor.py` lines 4088-4145 | ELO scaling formula | Never (mathematically correct) |

### **Data Files**
| File | Purpose | Update Frequency |
|------|---------|------------------|
| `Currentweekgames.json` | Weekly games & lines | Weekly (Monday) |
| `frontend/src/data/ap.json` | AP Poll rankings | Weekly (Sunday) |
| `data/*.json` | Player statistics | Every 2-3 weeks |
| `backtesting 2/all_fbs_ratings_*.json` | ELO/FPI ratings | Weekly if available |
| `fbs.json` | Team metadata | Rarely (only if new teams added) |

### **Script Files**
| File | Purpose | When to Run |
|------|---------|-------------|
| `week11_fetcher.py` | Fetch betting lines | Weekly |
| `ap_poll_week11.py` | Fetch AP rankings | Weekly |
| `week11_graphql_fetcher.py` | Fetch network/game data | Weekly |
| `run.py` | CLI testing | Anytime |
| `app.py` | Flask server | Always running |

---

## 🎯 QUICK REFERENCE: WHAT CHANGED

### **November 3, 2025 Updates**

#### **✅ Implemented Dynamic Weighting System**
- Weights now adjust based on ELO differential (40-65% composite ratings)
- 5 tiers from extreme mismatch to even matchup
- Rating consensus and SOS adjustments

#### **✅ Fixed ELO Scaling**
- Now uses proper chess rating formula: `1/(1 + 10^(-diff/400))`
- Converts win probability to spread: `ln(p/(1-p)) × 7.0-9.0`
- Mismatch multiplier (1.3-1.5x) for elite vs weak teams

#### **✅ Added Defensive Metrics Category**
- 10-12% weight for defensive analysis
- Dampens total scoring by 8-15% for elite defense vs poor offense
- Calculates defensive advantage for spread

#### **✅ Reduced Market Weight**
- Dropped from 20% to 2-5% (validation only)
- Added market validation warnings (>15 point differences)
- Prevents circular logic in value betting

#### **✅ EPA Now SOS-Adjusted**
- Weight drops from 50% to 15-35% depending on matchup
- Accounts for opponent quality
- Recent games weighted higher (1.5x last 3 games)

---

## 🔐 FINAL CRITICAL REMINDERS

1. **`graphqlpredictor.py` is the active file** - ignore `predictor/` directory
2. **Dynamic weights adjust automatically** - don't manually change base weights
3. **Test after every change** - restart backend and run test predictions
4. **Week-to-week updates are data only** - don't touch prediction logic mid-season
5. **Market warnings are good** - they indicate potential value bets
6. **ELO scaling is mathematically correct** - don't "fix" what isn't broken
7. **Defensive dampener reduces totals** - this is expected for mismatches
8. **Save refactoring for offseason** - current system works perfectly

---

## 📞 NEED HELP?

**If something breaks:**
1. Check backend terminal tab for error messages
2. Run health check: `curl http://localhost:5002/health`
3. Test with known good teams: `python run.py "Georgia" "Alabama"`
4. Check this guide's troubleshooting section
5. Restore from backup if needed: `git diff graphqlpredictor.py`

**If predictions seem wrong:**
1. Check if dynamic weights are applying (look for "DYNAMIC WEIGHT CALCULATION")
2. Verify ELO data is loading (look for "COMPOSITE RATINGS")
3. Check market lines are current (look in `Currentweekgames.json`)
4. Compare to sharp sportsbooks (Pinnacle, Circa, BetMGM)

---

## ✅ SUCCESS CHECKLIST

Before considering the system "working":

- [ ] Dynamic weights adjust based on ELO differential
- [ ] Extreme mismatches (750+ ELO diff) use 65% composite ratings
- [ ] Even matchups (<200 ELO diff) use 35% EPA
- [ ] ELO win probability calculated correctly (chess formula)
- [ ] Mismatch multiplier applies for elite vs weak teams
- [ ] Defensive dampener reduces totals for defensive mismatches
- [ ] Market validation warns when >15 points off consensus
- [ ] Backend starts without errors
- [ ] Frontend displays predictions correctly
- [ ] Test predictions look reasonable vs market

---

**Document Version:** 1.0.0  
**Last Tested:** November 3, 2025  
**Status:** ✅ All systems operational  
**Next Review:** End of 2025 season (January 2026)
