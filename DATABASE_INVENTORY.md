# SQL Database Inventory - Gameday+ Predictor

This document provides a comprehensive overview of all SQL databases in the Gameday+ project.

---

## 📍 Database File Locations

### Primary Databases (Active)

#### 1. **instance/coaches_master.db** (18 MB)
**Location:** `/instance/coaches_master.db`  
**Purpose:** Master database for coaching data, team information, and historical analytics

**Tables (24):**
- `coaches` - Coach biographical information and career data
- `coach_rankings` - Coach performance rankings
- `coach_timeline_data` - Timeline of coaching career events
- `stints` - Coaching position history at different schools
- `games` - Game-by-game results
- `draft_picks` - NFL draft picks by coach/team
- `rankings` - AP Poll and other ranking data
- `season_analytics` - Advanced season-level analytics
- `situational_stats` - Situational performance metrics
- `vs_coaches` - Head-to-head coaching records
- `recruiting_classes` - Recruiting class data
- `talent_composite` - Talent composite ratings
- `transfer_portal` - Transfer portal data
- `teams` - FBS team information
- `team_rankings` - Team ranking history
- `team_seasons` - Season-level team statistics
- `nil_players` - NIL player data
- `nil_position_groups` - NIL position group data
- `nil_rankings` - NIL rankings
- `nil_team_summary` - NIL team summary data
- `players` - Player roster information
- `player_stats` - Player statistics
- `player_season_stats` - Season-level player stats
- `drives` - Drive-level game data
- `plays` - Play-by-play data

**Primary Use Cases:**
- Coach comparison and analysis (`app_master.py`)
- Coaching history and career progression
- Team roster and player data
- NIL analytics
- Recruiting analysis

---

#### 2. **instance/predictions.db** (7.5 MB)
**Location:** `/instance/predictions.db`  
**Purpose:** Prediction engine data, upcoming games, betting lines, and advanced team analytics

**Tables (20):**
- `upcoming_games` - Future games with betting information
- `sportsbook_lines` - Multi-sportsbook betting lines
- `sportsbook_lines_history` - Historical line movement tracking
- `historical_game_results` - Historical game outcomes
- `ap_poll_rankings` - AP Poll rankings
- `coaches_poll_rankings` - Coaches Poll rankings
- `coach_rankings` - Coach performance rankings
- `coaches_rankings_data` - Extended coach ranking data
- `comprehensive_power_rankings` - Comprehensive power ratings
- `fbs_ratings_comprehensive` - FBS team ratings
- `team_power_rankings` - Team power rankings
- `team_offensive_stats` - Offensive statistics
- `team_defensive_stats` - Defensive statistics
- `team_drive_efficiency` - Drive efficiency metrics
- `team_epa_metrics` - Expected Points Added (EPA) metrics
- `team_season_summaries` - Season summary data
- `win_probability_curves` - Win probability data
- `player_efficiency` - Player efficiency ratings
- `player_metrics_data` - Player metrics and analytics
- `drives_complete` - Complete drive data
- `conferences` - Conference information

**Primary Use Cases:**
- Game predictions (`graphqlpredictor.py`)
- Betting line analysis (`betting_lines_manager.py`)
- Team performance analytics
- Player efficiency metrics
- Advanced statistical modeling

---

#### 3. **gameday_analytics.db** (31 MB - Root directory)
**Location:** `/gameday_analytics.db`  
**Purpose:** Real-time game analytics, drives, and play-by-play data

**Tables (4):**
- `teams` - Team information
- `games` - Game data
- `drives` - Drive-level analytics
- `plays` - Play-by-play details

**Primary Use Cases:**
- Live game tracking
- Drive-by-drive analysis
- Play-by-play breakdown
- Game flow analytics

---

#### 4. **instance/campbell_test.db** (100 KB)
**Location:** `/instance/campbell_test.db`  
**Purpose:** Test database (likely for development/testing)

---

#### 5. **instance/gameday_analytics.db** (0 bytes - Empty)
**Location:** `/instance/gameday_analytics.db`  
**Status:** Empty placeholder file

---

#### 6. **instance/cfb_database.db** (0 bytes - Empty)
**Location:** `/instance/cfb_database.db`  
**Status:** Empty placeholder file

---

#### 7. **coaches_master.db** (0 bytes - Root directory)
**Location:** `/coaches_master.db` (root)  
**Status:** Empty placeholder file (active version in `/instance/`)

---

### Backup Databases

#### Backup Location: `/backups/cleanup_20251214_103010/`
Contains backup copies of all main databases from December 14, 2025:
- `instance/campbell_test.db`
- `instance/coaches_master.db`
- `instance/gameday_analytics.db`
- `instance/cfb_database.db`
- `instance/predictions.db`
- `data/cfb_database.db`

---

### Archived Databases

#### Archive Location: `/archived_scripts/`
- `campbell_test.db` - Archived test database

---

## 📄 SQL Schema Files

### 1. **create_espn_tables.sql**
**Location:** `/create_espn_tables.sql`  
**Purpose:** Schema definitions for ESPN data integration

**Defines Tables:**
- `players` - ESPN player roster data
- `player_stats` - Player season statistics
- `drives` - ESPN drive data
- `plays` - ESPN play-by-play data

**Includes Indexes:**
- Player team and position indexes
- Drive game and team indexes
- Play drive, game, and scoring indexes

---

### 2. **add_missing_columns.sql**
**Location:** `/add_missing_columns.sql`  
**Purpose:** Schema migration to add box score statistics

**Adds Columns to `team_seasons`:**
- `possession_time`
- `possession_time_opponent`
- `turnovers`
- `turnovers_opponent`
- `turnover_margin`
- `penalty_yards`
- `sacks`
- `interceptions`
- `tackles_for_loss`
- `fumbles_recovered`
- `fumbles_lost`

---

## 🔧 Database Access by Application

### Full Stack Application (port 5002)
**Script:** `start-fullstack.sh` → runs `app.py`  
**Databases Used:**
- `instance/predictions.db` - Primary prediction data
- `instance/coaches_master.db` - Coach and team data (via database_helper)

**Key Modules:**
- `graphqlpredictor.py` - ML prediction engine
- `betting_lines_manager.py` - Betting lines (lazy loading)
- `game_media_service.py` - Game broadcast info
- `batch_rivalry_analyzer.py` - Rivalry analysis

---

### Coach Database API (port 5555)
**Script:** `app_master.py`  
**Databases Used:**
- `instance/coaches_master.db` - Primary database

**Endpoints Serve Data From:**
- Coaches, teams, stints, games
- Rankings, draft picks, recruiting
- NIL data, talent composite
- Transfer portal, situational stats

---

## 💾 Database Sizes Summary

| Database | Size | Status | Location |
|----------|------|--------|----------|
| coaches_master.db | 18 MB | ✅ Active | /instance/ |
| predictions.db | 7.5 MB | ✅ Active | /instance/ |
| gameday_analytics.db | 31 MB | ✅ Active | / (root) |
| campbell_test.db | 100 KB | 🧪 Test | /instance/ |
| cfb_database.db | 0 bytes | 🔴 Empty | /instance/ |
| gameday_analytics.db | 0 bytes | 🔴 Empty | /instance/ |
| coaches_master.db | 0 bytes | 🔴 Empty | / (root) |

---

## 🔍 How to Query the Databases

### Using SQLite Command Line:

```bash
# Coaches Master Database
sqlite3 instance/coaches_master.db

# List all tables
.tables

# Schema for a specific table
.schema coaches

# Query example
SELECT name, school FROM coaches LIMIT 10;
```

### Using Python:

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()

# Query
cursor.execute('SELECT * FROM coaches LIMIT 5')
results = cursor.fetchall()

conn.close()
```

---

## 🔄 Database Update Scripts

### Update Betting Lines:
```bash
python update_betting_lines.py
```
Updates `sportsbook_lines` table in `predictions.db` with latest odds from GraphQL API.

### Import Comprehensive Rankings:
```bash
python import_comprehensive_rankings.py
# or auto version:
python import_comprehensive_rankings_auto.py
```
Updates ranking data in `predictions.db`.

### Import Upcoming Games:
```bash
python import_upcoming_games.py
```
Updates `upcoming_games` table in `predictions.db`.

### Track Line Movements:
```bash
python track_line_movements.py
```
Tracks betting line changes over time in `sportsbook_lines_history`.

---

## 📊 Key Database Relationships

### coaches_master.db
```
coaches
  ├── stints (one-to-many)
  ├── games (one-to-many via stints)
  ├── recruiting_classes (one-to-many)
  ├── draft_picks (one-to-many)
  └── vs_coaches (many-to-many)

teams
  ├── team_seasons (one-to-many)
  ├── players (one-to-many)
  └── team_rankings (one-to-many)

players
  └── player_stats (one-to-many)
```

### predictions.db
```
upcoming_games
  └── sportsbook_lines (one-to-many)

teams
  ├── team_offensive_stats (one-to-many)
  ├── team_defensive_stats (one-to-many)
  └── team_drive_efficiency (one-to-many)
```

---

## 🎯 Database Recommendations

1. **Clean Up Empty Files:**
   - Remove or populate empty `.db` files in root and `/instance/`
   - Consolidate duplicate database files

2. **Consolidation Opportunities:**
   - Consider merging `gameday_analytics.db` (root) with `instance/predictions.db`
   - Standardize on single location for active databases

3. **Documentation:**
   - Add ER diagrams for complex relationships
   - Document foreign key constraints
   - Create data dictionary for column definitions

4. **Maintenance:**
   - Regular vacuum operations for database optimization
   - Automated backup schedule beyond manual backups
   - Index optimization based on query patterns

---

## 📝 Additional Notes

- All active databases use SQLite format
- Primary development happens in `/instance/` directory
- Flask applications expect databases in `/instance/` by default
- Backup strategy: Manual backups in `/backups/` directory
- Schema changes tracked via SQL migration files

---

**Last Updated:** December 16, 2025  
**Project:** Gameday+ College Football Predictor  
**Repository:** Davlen14/gameday-plus-predictor
