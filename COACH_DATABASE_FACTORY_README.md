# 🏗️ COACH DATABASE FACTORY - Production System

## 📋 Overview

This is a **universal coach database system** that scales the Matt Campbell prototype to all 134 FBS head coaches.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    COACH DATABASE FACTORY                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1️⃣  setup_master_db.py     → Creates coaches_master.db     │
│  2️⃣  ingest_coach.py         → CoachIngestor class          │
│  3️⃣  batch_ingest.py         → Batch processing script      │
│  4️⃣  app_master.py           → Universal Flask API          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### Step 1: Create Master Database

```bash
python setup_master_db.py
```

**Output**: `instance/coaches_master.db` with 11 tables

### Step 2: Set API Key

```bash
export CFBD_API_KEY="your_api_key_here"
```

Get your key from: https://collegefootballdata.com/key

### Step 3: Ingest Coaches (Conference-by-Conference)

⚠️ **IMPORTANT**: Do NOT ingest all coaches at once! Use conference filtering.

```bash
# Test with a small conference first
python batch_ingest.py --conference MAC --dry-run

# Actually ingest MAC coaches
python batch_ingest.py --conference MAC

# Ingest SEC coaches
python batch_ingest.py --conference SEC

# Ingest Big Ten coaches
python batch_ingest.py --conference "Big Ten"
```

### Step 4: Start Flask API

```bash
python app_master.py
```

Visit: http://localhost:5555/api/stats

---

## 📊 Database Schema

### 11 Tables (Identical to Campbell Prototype)

| Table                | Purpose                          | Rows per Coach |
|---------------------|----------------------------------|----------------|
| `coaches`           | Core metadata + headshot         | 1              |
| `stints`            | Coaching history by school       | 1-4            |
| `games`             | Game-by-game results             | 50-200         |
| `rankings`          | AP Poll appearances              | 0-100          |
| `draft_picks`       | NFL talent produced              | 0-50           |
| `situational_stats` | Home/away, blowouts, vs ranked   | 1-4            |
| `vs_coaches`        | Head-to-head records             | 10-50          |
| `season_analytics`  | Offensive/defensive metrics      | 5-20           |
| `recruiting_classes`| 247Sports class rankings         | 5-20           |
| `talent_composite`  | Team talent ratings              | 5-20           |
| `transfer_portal`   | Portal activity (2018+)          | 0-8            |

---

## 🤖 CoachIngestor Class API

### Basic Usage

```python
from ingest_coach import CoachIngestor

# Initialize with API key
ingestor = CoachIngestor(api_key="YOUR_KEY")

# Ingest single coach
success = ingestor.ingest("Kirby Smart")

# Check API call count
print(f"API calls used: {ingestor.call_count}")
```

### What It Does Automatically

1. ✅ Fetches coach metadata + headshot from CFBD
2. ✅ Retrieves full game history with opponent metrics
3. ✅ **Auto-fixes 0.0 values** for FPI/SP+ (fetches real data)
4. ✅ Calculates situational stats (home/away, blowouts, vs ranked)
5. ✅ Computes season analytics (PPG, YPP, advanced metrics)
6. ✅ Ingests recruiting classes, talent composite, portal data
7. ✅ Rate-limited to 1 API call/second (respects CFBD limits)

### Estimated API Calls per Coach

| Data Type          | API Calls |
|-------------------|-----------|
| Coach metadata    | 1         |
| Game history      | 2-3       |
| Opponent metrics  | 1-2       |
| Season stats      | 1         |
| Recruiting        | 1         |
| Talent composite  | 1         |
| **TOTAL**         | **7-9**   |

---

## ⚠️ API Limit Management

### The Problem

**CollegeFootballData.com** free tier = **1,000 calls/month**

- **134 coaches** × **7 calls each** = **~940 calls**
- Running all at once uses **94% of monthly quota!**

### The Solution: Conference Batching

| Conference    | Teams | Est. API Calls |
|--------------|-------|----------------|
| SEC          | 16    | ~112           |
| Big Ten      | 18    | ~126           |
| ACC          | 17    | ~119           |
| Big 12       | 16    | ~112           |
| AAC          | 14    | ~98            |
| Mountain West| 12    | ~84            |
| Sun Belt     | 14    | ~98            |
| C-USA        | 9     | ~63            |
| MAC          | 12    | ~84            |
| Independent  | 3     | ~21            |

**Strategy**: Ingest 1-2 conferences per day to spread API usage across month.

---

## 🌐 Flask API Endpoints

### List Coaches

```bash
GET /api/coaches
```

**Response**:
```json
{
  "coaches": [
    {
      "id": 1,
      "name": "Matt Campbell",
      "current_school": "Iowa State",
      "career_record": "122-79",
      "career_win_pct": 0.607
    }
  ],
  "count": 134
}
```

### Get Coach Details

```bash
GET /api/coach/1
```

### Get Game History

```bash
GET /api/coach/1/games
GET /api/coach/1/games?season=2024
GET /api/coach/1/games?school=Iowa%20State&limit=50
```

### All Endpoints

| Endpoint                               | Description               |
|---------------------------------------|---------------------------|
| `GET /api/coaches`                    | List all coaches          |
| `GET /api/coach/<id>`                 | Coach details             |
| `GET /api/coach/<id>/stints`          | Coaching history          |
| `GET /api/coach/<id>/games`           | Game history              |
| `GET /api/coach/<id>/rankings`        | AP Poll history           |
| `GET /api/coach/<id>/draft_picks`     | NFL draft picks           |
| `GET /api/coach/<id>/situational`     | Situational stats         |
| `GET /api/coach/<id>/vs_coaches`      | Head-to-head records      |
| `GET /api/coach/<id>/season_analytics`| Season analytics          |
| `GET /api/coach/<id>/recruiting`      | Recruiting classes        |
| `GET /api/coach/<id>/talent`          | Talent composite          |
| `GET /api/coach/<id>/portal`          | Transfer portal           |
| `GET /api/search?q=<query>`           | Search coaches            |
| `GET /api/stats`                      | Database statistics       |

---

## 📈 Monitoring Progress

### Check Database Stats

```bash
curl http://localhost:5555/api/stats
```

**Example Output**:
```json
{
  "coaches": 24,
  "games": 3847,
  "stints": 52,
  "recruiting_classes": 312,
  "talent_composite": 268
}
```

### Check Single Coach

```bash
# Search for coach
curl "http://localhost:5555/api/search?q=Kirby"

# Get their ID from response
curl http://localhost:5555/api/coach/12

# Get their games
curl http://localhost:5555/api/coach/12/games
```

---

## 🔧 Maintenance Scripts

### Re-fix Metrics for Specific Coach

```python
from ingest_coach import CoachIngestor

ingestor = CoachIngestor(api_key="YOUR_KEY")
ingestor._fix_fbs_metrics(coach_id=5)
```

### Re-calculate Analytics

```python
import sqlite3

conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()

# Delete old analytics for a coach
cursor.execute("DELETE FROM season_analytics WHERE coach_id = ?", (5,))

# Re-run ingestion for just analytics
ingestor._calculate_season_analytics(coach_id=5)
```

---

## 🎯 Example Workflow: Full System Setup

```bash
# 1. Create database
python setup_master_db.py

# 2. Set API key
export CFBD_API_KEY="abc123..."

# 3. Test with smallest conference (Independent = 3 coaches)
python batch_ingest.py --conference Independent --dry-run
python batch_ingest.py --conference Independent

# 4. Check results
python app_master.py &
curl http://localhost:5555/api/stats

# 5. Ingest MAC (12 coaches, ~84 API calls)
python batch_ingest.py --conference MAC

# 6. Continue with other conferences over several days
python batch_ingest.py --conference SEC      # Day 1
python batch_ingest.py --conference "Big Ten" # Day 2
python batch_ingest.py --conference ACC      # Day 3
# ... etc
```

---

## 📝 Available Conferences

Use these exact names with `--conference` flag:

- `SEC`
- `Big Ten` (use quotes!)
- `ACC`
- `Big 12` (use quotes!)
- `AAC`
- `Mountain West` (use quotes!)
- `Sun Belt` (use quotes!)
- `C-USA`
- `MAC`
- `Independent`

---

## 🐛 Troubleshooting

### "Coach not found" error

**Cause**: API returned no data for that coach name

**Fix**: Check exact spelling, try different name format

### "429 Too Many Requests"

**Cause**: Hit API rate limit (1000 calls/month)

**Fix**: Wait until next month, or use conference batching more carefully

### Missing opponent metrics (0.0 values)

**Cause**: CFBD doesn't have metrics for FCS opponents or some seasons

**Fix**: This is expected! The system auto-estimates where possible.

### Database locked error

**Cause**: Another process is using the database

**Fix**: Close other connections, restart Flask app

---

## 📊 Success Metrics

After ingesting all 134 coaches, you should see:

| Metric              | Expected Value  |
|--------------------|-----------------|
| Total coaches      | 134             |
| Total games        | ~18,000-20,000  |
| Total stints       | ~200-250        |
| Recruiting classes | ~1,500-2,000    |
| Talent records     | ~1,200-1,500    |
| API calls used     | ~900-1,000      |

---

## 🎉 What You Built

### Before
- ❌ One coach (Matt Campbell) in `campbell_test.db`
- ❌ Manual fixes in separate scripts
- ❌ Hardcoded Flask routes for ID=1

### After
- ✅ Universal `coaches_master.db` for all 134 coaches
- ✅ Automated ingestion with smart data cleaning
- ✅ Dynamic Flask API that scales to any coach
- ✅ Production-ready architecture

---

## 📚 File Reference

| File                      | Purpose                          | Lines |
|--------------------------|----------------------------------|-------|
| `setup_master_db.py`     | Create universal database        | 320   |
| `ingest_coach.py`        | Coach ingestion engine           | 650   |
| `batch_ingest.py`        | Batch processing script          | 380   |
| `app_master.py`          | Universal Flask API              | 420   |
| **TOTAL**                | **Production system**            | 1,770 |

---

## 🔐 Security Notes

- ⚠️ Never commit `CFBD_API_KEY` to git
- ⚠️ Use `.env` file for production
- ⚠️ Add rate limiting to Flask API in production
- ⚠️ Use PostgreSQL instead of SQLite for scale

---

## 🎯 Next Steps

1. **Test with small conference**: Start with Independent (3 coaches)
2. **Validate data quality**: Check Campbell vs prototype
3. **Build frontend**: Create React UI to consume API
4. **Deploy**: Move to Railway/Heroku with PostgreSQL
5. **Enhance**: Add real-time updates, more analytics

---

**Built with ❤️ for Gameday+ Prediction Engine**
