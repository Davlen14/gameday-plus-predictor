# 📋 COACH DATABASE FACTORY - QUICK REFERENCE

## 🚀 Essential Commands

### Setup (One-Time)
```bash
python setup_master_db.py              # Create database
export CFBD_API_KEY="your_key"         # Set API key
./test_system.sh                       # Validate system
```

### Ingestion (Conference-by-Conference)
```bash
# Dry run first
python batch_ingest.py --conference SEC --dry-run

# Actual ingest
python batch_ingest.py --conference SEC

# Available conferences:
# SEC, "Big Ten", ACC, "Big 12", AAC, 
# "Mountain West", "Sun Belt", C-USA, MAC, Independent
```

### API Server
```bash
python app_master.py                   # Start on port 5555
```

### Testing
```bash
# Database stats
curl http://localhost:5555/api/stats

# List coaches
curl http://localhost:5555/api/coaches

# Search
curl "http://localhost:5555/api/search?q=Campbell"

# Get coach games
curl http://localhost:5555/api/coach/1/games
```

---

## 📁 File Reference

| File | Use Case |
|------|----------|
| `setup_master_db.py` | Create empty database |
| `ingest_coach.py` | Import from Python: `from ingest_coach import CoachIngestor` |
| `batch_ingest.py` | Batch ingest coaches |
| `app_master.py` | Run Flask API server |
| `test_system.sh` | Validate full system |

---

## 🗄️ Database Tables

```
coaches              # 1 row per coach
stints               # 1-4 rows per coach
games                # 50-200 rows per coach
rankings             # 0-100 rows per coach
draft_picks          # 0-50 rows per coach
situational_stats    # 1-4 rows per coach
vs_coaches           # 10-50 rows per coach
season_analytics     # 5-20 rows per coach
recruiting_classes   # 5-20 rows per coach
talent_composite     # 5-20 rows per coach
transfer_portal      # 0-8 rows per coach
```

---

## 📡 API Endpoints

### Discovery
- `GET /api/coaches` - All coaches
- `GET /api/search?q=<name>` - Search
- `GET /api/stats` - DB statistics

### Coach Data (`<id>` = coach ID)
- `GET /api/coach/<id>` - Details
- `GET /api/coach/<id>/stints` - Coaching history
- `GET /api/coach/<id>/games` - Games
- `GET /api/coach/<id>/rankings` - AP Polls
- `GET /api/coach/<id>/draft_picks` - NFL picks
- `GET /api/coach/<id>/situational` - Situational stats
- `GET /api/coach/<id>/vs_coaches` - Head-to-head
- `GET /api/coach/<id>/season_analytics` - Analytics
- `GET /api/coach/<id>/recruiting` - Recruiting
- `GET /api/coach/<id>/talent` - Talent ratings
- `GET /api/coach/<id>/portal` - Portal data

---

## ⚠️ API Quota Management

**Free Tier**: 1,000 calls/month

| Action | API Calls |
|--------|-----------|
| Ingest 1 coach | ~7-9 |
| Ingest SEC (16 coaches) | ~112 |
| Ingest all (134 coaches) | ~940 |

**Best Practice**: Ingest 1-2 conferences per day

---

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| `Coach not found` | Check spelling, try search API first |
| `429 Too Many Requests` | Hit monthly limit, wait until next month |
| `Database locked` | Close other DB connections |
| `No module named 'requests'` | `pip install requests` |

---

## 📊 Common Queries

### SQL (Direct Database)
```bash
# Count coaches
sqlite3 instance/coaches_master.db "SELECT COUNT(*) FROM coaches;"

# List all coaches
sqlite3 instance/coaches_master.db "SELECT id, name, current_school FROM coaches ORDER BY name;"

# Find coach ID
sqlite3 instance/coaches_master.db "SELECT id FROM coaches WHERE name = 'Kirby Smart';"

# Count games for coach
sqlite3 instance/coaches_master.db "SELECT COUNT(*) FROM games WHERE coach_id = 5;"
```

### Python (Programmatic)
```python
from ingest_coach import CoachIngestor

# Single coach ingest
ingestor = CoachIngestor(api_key="YOUR_KEY")
ingestor.ingest("Kirby Smart")

# Check API usage
print(f"API calls: {ingestor.call_count}")
```

---

## 📈 Progress Tracking

### Check Ingestion Status
```bash
# Via API
curl http://localhost:5555/api/stats

# Via SQL
sqlite3 instance/coaches_master.db << EOF
SELECT 
  (SELECT COUNT(*) FROM coaches) as coaches,
  (SELECT COUNT(*) FROM games) as games,
  (SELECT COUNT(*) FROM recruiting_classes) as recruiting
;
EOF
```

### Expected Milestones
```
After Independent (3 coaches):
  - coaches: 3
  - games: ~400-600
  - recruiting_classes: ~30-50

After SEC (16 coaches):
  - coaches: 16
  - games: ~3,000-4,000
  - recruiting_classes: ~200-300

After all (134 coaches):
  - coaches: 134
  - games: ~18,000-20,000
  - recruiting_classes: ~1,500-2,000
```

---

## 🎯 Recommended Workflow

### Day 1: Setup & Test
```bash
python setup_master_db.py
export CFBD_API_KEY="..."
./test_system.sh
```

### Week 1: Small Conferences
```bash
python batch_ingest.py --conference Independent  # 3 coaches
python batch_ingest.py --conference MAC          # 12 coaches
python batch_ingest.py --conference C-USA        # 9 coaches
```

### Week 2-4: Major Conferences
```bash
python batch_ingest.py --conference SEC          # 16 coaches
python batch_ingest.py --conference "Big Ten"    # 18 coaches
python batch_ingest.py --conference ACC          # 17 coaches
python batch_ingest.py --conference "Big 12"     # 16 coaches
```

### Week 5: Remaining
```bash
python batch_ingest.py --conference AAC
python batch_ingest.py --conference "Mountain West"
python batch_ingest.py --conference "Sun Belt"
```

---

## 📚 Documentation Index

| Document | Use When |
|----------|----------|
| `EXECUTIVE_SUMMARY.md` | High-level overview |
| `COACH_DATABASE_FACTORY_README.md` | Complete system guide |
| `MIGRATION_GUIDE.md` | Moving from prototype |
| `QUICK_REFERENCE.md` | This file (commands) |

---

## 🔗 Key Files

```
instance/
  └── coaches_master.db        # Main database

Production Scripts:
  ├── setup_master_db.py       # Create database
  ├── ingest_coach.py          # Ingestion engine
  ├── batch_ingest.py          # Batch processor
  ├── app_master.py            # Flask API
  └── test_system.sh           # Validation

Prototype (Keep as Backup):
  ├── campbell_test.db         # Single-coach DB
  └── view_campbell_db.py      # Old Flask app
```

---

## 💡 Pro Tips

1. **Always dry-run first**: `--dry-run` flag shows what will happen
2. **Check API calls**: Each coach = ~7 calls, plan accordingly
3. **Validate Matt Campbell**: Compare prototype vs production data
4. **Use search endpoint**: Find coach ID before querying other endpoints
5. **Monitor quota**: Track API usage to avoid hitting limits

---

## 🎉 Success Indicators

✅ `coaches_master.db` file exists  
✅ `./test_system.sh` completes without errors  
✅ Flask API returns JSON for all endpoints  
✅ Database stats show expected row counts  
✅ Matt Campbell data matches prototype  

---

**Last Updated**: December 2025  
**System Version**: 1.0 (Production Ready)
