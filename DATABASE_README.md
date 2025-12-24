# 🗄️ SQL Database Documentation - Gameday+ Predictor

Welcome to the comprehensive SQL database documentation for the Gameday+ College Football Predictor project!

---

## 📚 Documentation Files

This repository contains complete documentation for all SQL databases in the project:

### 1. [DATABASE_INVENTORY.md](./DATABASE_INVENTORY.md) 📋
**Complete Detailed Inventory**
- Full list of all database files with locations and sizes
- Detailed table listings for each database (53 tables total)
- Database purposes and primary use cases
- Schema relationships and foreign key mappings
- Application-to-database mapping
- Database maintenance recommendations

**When to use:** When you need detailed technical information about database structure, relationships, or want to understand the full architecture.

---

### 2. [DATABASE_QUICK_REFERENCE.md](./DATABASE_QUICK_REFERENCE.md) ⚡
**Quick Access Guide**
- Visual directory tree of database locations
- Quick reference table for "Which database to use?"
- Connection examples in Python and command line
- Most commonly used tables by database
- Update commands and maintenance tips
- File paths and locations

**When to use:** When you need to quickly find which database contains what data, or need connection examples.

---

### 3. [DATABASE_SAMPLE_QUERIES.md](./DATABASE_SAMPLE_QUERIES.md) 💻
**100+ Ready-to-Use SQL Queries**
- Queries organized by database and use case
- Coach information and history queries
- Recruiting and draft pick analysis
- Betting lines and predictions queries
- Team statistics and rankings
- Drive and play-by-play analytics
- Cross-database query examples

**When to use:** When you need SQL query examples for specific data or analysis tasks.

---

### 4. [verify_databases.py](./verify_databases.py) 🔍
**Database Health Check Script**
- Verifies all databases are accessible
- Shows database sizes and table counts
- Displays sample row counts
- Checks schema files
- Security-hardened against SQL injection

**When to use:** To verify database health, check connectivity, or get quick stats.

---

## 🎯 Quick Start

### Verify Your Databases
```bash
python verify_databases.py
```

### Browse a Database
```bash
# Coaches database
sqlite3 instance/coaches_master.db
.tables
SELECT name, school FROM coaches LIMIT 5;

# Predictions database
sqlite3 instance/predictions.db
.tables
SELECT home_team, away_team, spread FROM upcoming_games LIMIT 5;
```

### Python Connection Example
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()

# Run query
cursor.execute('SELECT name, school FROM coaches LIMIT 5')
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## 📍 Main Database Locations

### Active Databases (Ready to Use)

```
instance/
├── coaches_master.db (18 MB) ⭐ Primary coaching database
│   └── 26 tables: coaches, teams, players, recruiting, NIL
│
├── predictions.db (7.5 MB) ⭐ Prediction engine
│   └── 22 tables: upcoming_games, betting_lines, team_stats
│
└── campbell_test.db (100 KB) 🧪 Test database

gameday_analytics.db (31 MB) ⭐ Live game analytics
└── 5 tables: teams, games, drives, plays
```

---

## 🚀 Common Use Cases

| What You Need | Which Database | Key Tables |
|--------------|----------------|------------|
| Coach info & career stats | `coaches_master.db` | coaches, stints, games |
| Game predictions | `predictions.db` | upcoming_games, sportsbook_lines |
| Betting line analysis | `predictions.db` | sportsbook_lines, sportsbook_lines_history |
| Team statistics | `predictions.db` | team_offensive_stats, team_defensive_stats |
| Player rosters | `coaches_master.db` | players, player_stats |
| Live game data | `gameday_analytics.db` | drives, plays |
| Recruiting classes | `coaches_master.db` | recruiting_classes, talent_composite |
| NIL valuations | `coaches_master.db` | nil_players, nil_team_summary |

---

## 🔄 Database Update Commands

Keep your databases fresh with these update scripts:

```bash
# Update betting lines from GraphQL API
python update_betting_lines.py

# Import upcoming games
python import_upcoming_games.py

# Track line movements
python track_line_movements.py

# Import comprehensive rankings
python import_comprehensive_rankings.py
```

---

## 📊 Database Statistics

| Database | Size | Tables | Primary Content |
|----------|------|--------|-----------------|
| coaches_master.db | 18 MB | 26 | Coaches, teams, players, recruiting, NIL |
| predictions.db | 7.5 MB | 22 | Games, betting lines, analytics, rankings |
| gameday_analytics.db | 31 MB | 5 | Live drives and play-by-play data |
| **Total** | **56 MB** | **53** | **Complete CFB data platform** |

---

## 🛠️ Application Usage

### Full Stack Application (port 5002)
**Script:** `start-fullstack.sh` → `app.py`  
**Uses:** `predictions.db` + `coaches_master.db`  
**For:** ML predictions, betting analysis, full UI

### Coach Database API (port 5555)
**Script:** `app_master.py`  
**Uses:** `coaches_master.db` only  
**For:** Coach/team exploration, NIL data, recruiting

---

## 📖 Documentation Guide

### For Developers
1. Start with **DATABASE_QUICK_REFERENCE.md** to understand the structure
2. Use **DATABASE_SAMPLE_QUERIES.md** for query examples
3. Refer to **DATABASE_INVENTORY.md** for detailed technical specs

### For Data Analysts
1. Use **DATABASE_SAMPLE_QUERIES.md** for ready-to-run queries
2. Check **DATABASE_QUICK_REFERENCE.md** for which database has your data
3. Run `verify_databases.py` to confirm data availability

### For System Administrators
1. Review **DATABASE_INVENTORY.md** for architecture and relationships
2. Use `verify_databases.py` for health checks
3. Check backup locations in **DATABASE_INVENTORY.md**

---

## 🔐 Security Notes

All database documentation and scripts follow security best practices:
- ✅ SQL injection protection in verification script
- ✅ Parameterized queries in examples
- ✅ No hardcoded credentials
- ✅ Proper identifier quoting
- ✅ CodeQL security scanned

---

## 💡 Tips & Best Practices

1. **Always use `instance/` databases** - The root directory has empty placeholder files
2. **Update betting lines regularly** - Lines change frequently, especially during bowl season
3. **Use `.schema tablename`** to see table structure before querying
4. **Run `VACUUM`** periodically to optimize database performance
5. **Check `verify_databases.py`** output to ensure data is current

---

## 🆘 Troubleshooting

### Database locked error
```bash
# Check for open connections
lsof | grep coaches_master.db

# Make sure no other process is using it
pkill -9 python  # (if safe to do so)
```

### Empty results
```bash
# Verify table has data
sqlite3 instance/coaches_master.db
SELECT COUNT(*) FROM coaches;
```

### Connection issues
```bash
# Verify file exists and is readable
ls -lh instance/coaches_master.db

# Check permissions
chmod 644 instance/coaches_master.db
```

---

## 📝 Schema Files

- **create_espn_tables.sql** - ESPN data integration schema (players, drives, plays)
- **add_missing_columns.sql** - Box score statistics migration

---

## 🔗 Related Documentation

- [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) - Overall project guide
- [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) - System architecture
- [DATABASE_SCHEMA_COMPLETE.md](./DATABASE_SCHEMA_COMPLETE.md) - Schema details
- [GRAPHQL_MIGRATION_GUIDE.md](./GRAPHQL_MIGRATION_GUIDE.md) - API migration

---

## 📞 Need Help?

1. **Check the docs first:** Review the 4 documentation files in order
2. **Run verification:** `python verify_databases.py`
3. **Try sample queries:** Copy from DATABASE_SAMPLE_QUERIES.md
4. **Check existing code:** Look at `app.py` or `app_master.py` for examples

---

## ✨ Summary

This documentation package provides:
- ✅ Complete inventory of all 7 database files
- ✅ 53 tables documented across all databases
- ✅ 100+ ready-to-use SQL queries
- ✅ Secure verification script
- ✅ Quick reference guides
- ✅ Connection examples
- ✅ Update procedures
- ✅ Security best practices

**All databases verified and accessible!** 🎉

---

**Last Updated:** December 16, 2025  
**Project:** Gameday+ College Football Predictor  
**Repository:** [Davlen14/gameday-plus-predictor](https://github.com/Davlen14/gameday-plus-predictor)
