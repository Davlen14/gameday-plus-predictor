# SQL Sample Queries - Gameday+ Predictor

This document provides ready-to-use SQL queries for exploring the Gameday+ databases.

---

## 🗄️ coaches_master.db Queries

### Basic Coach Information

```sql
-- List all active FBS coaches
SELECT name, school, first_year, last_year 
FROM coaches 
WHERE last_year IS NULL 
ORDER BY name;

-- Get coach with most wins
SELECT name, school, wins, losses, win_percentage
FROM coaches
ORDER BY wins DESC
LIMIT 10;

-- Find coaches at specific school
SELECT name, first_year, last_year, wins, losses
FROM coaches
WHERE school = 'Michigan'
ORDER BY first_year DESC;
```

### Coaching Stints & History

```sql
-- Get all coaching positions for a coach
SELECT c.name, s.school, s.position, s.start_year, s.end_year
FROM coaches c
JOIN stints s ON c.id = s.coach_id
WHERE c.name LIKE '%Saban%'
ORDER BY s.start_year;

-- Find coaches who have coached multiple P5 schools
SELECT c.name, COUNT(DISTINCT s.school) as school_count,
       GROUP_CONCAT(DISTINCT s.school) as schools
FROM coaches c
JOIN stints s ON c.id = s.coach_id
GROUP BY c.id
HAVING school_count > 2
ORDER BY school_count DESC;
```

### Game Results & Records

```sql
-- Get recent games for a coach
SELECT g.season, g.opponent, g.home_away, g.points_for, g.points_against,
       CASE WHEN g.win = 1 THEN 'W' ELSE 'L' END as result
FROM games g
JOIN stints s ON g.stint_id = s.id
JOIN coaches c ON s.coach_id = c.id
WHERE c.name = 'Jim Harbaugh'
ORDER BY g.season DESC, g.week DESC
LIMIT 20;

-- Conference championship games
SELECT g.season, c.name, g.opponent, g.points_for, g.points_against
FROM games g
JOIN stints s ON g.stint_id = s.id
JOIN coaches c ON s.coach_id = c.id
WHERE g.conference_game = 1 AND g.opponent LIKE '%Championship%'
ORDER BY g.season DESC;
```

### Recruiting Data

```sql
-- Top recruiting classes
SELECT c.name, r.year, r.rank, r.avg_rating, r.total_commits
FROM recruiting_classes r
JOIN coaches c ON r.coach_id = c.id
WHERE r.rank <= 5
ORDER BY r.year DESC, r.rank;

-- Coach's recruiting trend
SELECT c.name, r.year, r.rank, r.avg_rating
FROM recruiting_classes r
JOIN coaches c ON r.coach_id = c.id
WHERE c.school = 'Ohio State'
ORDER BY r.year DESC
LIMIT 5;
```

### NFL Draft Success

```sql
-- Coaches with most draft picks
SELECT c.name, c.school, COUNT(d.id) as total_picks,
       SUM(CASE WHEN d.round = 1 THEN 1 ELSE 0 END) as first_round_picks
FROM draft_picks d
JOIN coaches c ON d.coach_id = c.id
GROUP BY c.id
ORDER BY total_picks DESC
LIMIT 10;

-- First round picks by position
SELECT c.name, d.position, COUNT(*) as picks
FROM draft_picks d
JOIN coaches c ON d.coach_id = c.id
WHERE d.round = 1
GROUP BY c.id, d.position
ORDER BY c.name, picks DESC;
```

### NIL Data

```sql
-- Top NIL teams by valuation
SELECT team_name, total_valuation, player_count, avg_valuation
FROM nil_team_summary
ORDER BY total_valuation DESC
LIMIT 10;

-- NIL players at specific position
SELECT p.name, p.team, p.position, p.nil_valuation
FROM nil_players p
WHERE p.position = 'QB'
ORDER BY p.nil_valuation DESC
LIMIT 20;
```

### Team & Player Data

```sql
-- Team roster by position
SELECT t.school, p.position_abbr, COUNT(*) as player_count
FROM players p
JOIN teams t ON p.team_id = t.id
WHERE t.school = 'Alabama'
GROUP BY t.school, p.position_abbr
ORDER BY player_count DESC;

-- Top players by stats (example: rushing yards)
SELECT p.name, t.school, ps.season, ps.rushing_yards, ps.rushing_tds
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN teams t ON p.team_id = t.id
WHERE ps.season = 2024 AND ps.rushing_yards > 0
ORDER BY ps.rushing_yards DESC
LIMIT 20;
```

---

## 🎲 predictions.db Queries

### Upcoming Games & Betting Lines

```sql
-- Upcoming games with betting lines
SELECT home_team, away_team, game_date, spread, over_under, home_moneyline
FROM upcoming_games
WHERE game_date >= date('now')
ORDER BY game_date
LIMIT 20;

-- Games with largest spreads
SELECT home_team, away_team, spread, game_date
FROM upcoming_games
WHERE spread IS NOT NULL
ORDER BY ABS(spread) DESC
LIMIT 10;

-- High-total games (over/under)
SELECT home_team, away_team, over_under, spread, game_date
FROM upcoming_games
WHERE over_under > 60
ORDER BY over_under DESC;
```

### Multi-Sportsbook Lines

```sql
-- Compare lines across sportsbooks
SELECT home_team, away_team, provider, spread, over_under
FROM sportsbook_lines
WHERE home_team = 'Michigan' OR away_team = 'Michigan'
ORDER BY game_id, provider;

-- Line discrepancies (largest spread differences)
SELECT sl1.home_team, sl1.away_team,
       sl1.provider as book1, sl1.spread as spread1,
       sl2.provider as book2, sl2.spread as spread2,
       ABS(sl1.spread - sl2.spread) as difference
FROM sportsbook_lines sl1
JOIN sportsbook_lines sl2 ON sl1.game_id = sl2.game_id
WHERE sl1.provider < sl2.provider
  AND ABS(sl1.spread - sl2.spread) > 1
ORDER BY difference DESC;
```

### Line Movement Tracking

```sql
-- Recent line movements for a team
SELECT team, game_id, timestamp, old_spread, new_spread, 
       (new_spread - old_spread) as movement
FROM sportsbook_lines_history
WHERE team = 'Ohio State'
ORDER BY timestamp DESC
LIMIT 20;

-- Biggest line moves
SELECT home_team, away_team, ABS(new_spread - old_spread) as movement
FROM sportsbook_lines_history
ORDER BY movement DESC
LIMIT 10;
```

### Team Statistics

```sql
-- Top offensive teams
SELECT team, points_per_game, yards_per_game, yards_per_play
FROM team_offensive_stats
ORDER BY points_per_game DESC
LIMIT 10;

-- Top defensive teams
SELECT team, points_allowed_per_game, yards_allowed_per_game, 
       sacks, interceptions
FROM team_defensive_stats
ORDER BY points_allowed_per_game
LIMIT 10;

-- Drive efficiency leaders
SELECT team, drives_per_game, points_per_drive, yards_per_drive
FROM team_drive_efficiency
ORDER BY points_per_drive DESC
LIMIT 10;
```

### EPA (Expected Points Added) Metrics

```sql
-- Best EPA offenses
SELECT team, overall_epa, passing_epa, rushing_epa, explosiveness
FROM team_epa_metrics
ORDER BY overall_epa DESC
LIMIT 10;

-- Most explosive offenses
SELECT team, explosiveness, overall_epa
FROM team_epa_metrics
ORDER BY explosiveness DESC
LIMIT 10;
```

### Rankings Data

```sql
-- Current AP Poll rankings
SELECT rank, team, points, first_place_votes
FROM ap_poll_rankings
WHERE week = (SELECT MAX(week) FROM ap_poll_rankings)
ORDER BY rank;

-- Coaches Poll rankings
SELECT rank, team, points
FROM coaches_poll_rankings
WHERE week = (SELECT MAX(week) FROM coaches_poll_rankings)
ORDER BY rank;

-- Comprehensive power rankings
SELECT team, overall_rank, elo_rating, talent_rank, recruiting_rank
FROM comprehensive_power_rankings
ORDER BY overall_rank
LIMIT 25;
```

### Historical Results

```sql
-- Head-to-head history
SELECT season, home_team, away_team, home_score, away_score, winner
FROM historical_game_results
WHERE (home_team = 'Ohio State' AND away_team = 'Michigan')
   OR (home_team = 'Michigan' AND away_team = 'Ohio State')
ORDER BY season DESC;

-- Recent results for a team
SELECT season, week, home_team, away_team, home_score, away_score
FROM historical_game_results
WHERE home_team = 'Georgia' OR away_team = 'Georgia'
ORDER BY season DESC, week DESC
LIMIT 10;
```

---

## 📈 gameday_analytics.db Queries

### Teams

```sql
-- All FBS teams
SELECT id, school, mascot, abbreviation, conference
FROM teams
ORDER BY school;

-- Teams by conference
SELECT conference, COUNT(*) as team_count
FROM teams
GROUP BY conference
ORDER BY team_count DESC;
```

### Games

```sql
-- Recent games
SELECT home_team, away_team, home_score, away_score, game_date
FROM games
ORDER BY game_date DESC
LIMIT 20;

-- High-scoring games
SELECT home_team, away_team, home_score, away_score, 
       (home_score + away_score) as total_points
FROM games
WHERE home_score IS NOT NULL
ORDER BY total_points DESC
LIMIT 10;
```

### Drives Analysis

```sql
-- Scoring drives
SELECT team_id, COUNT(*) as scoring_drives, AVG(yards) as avg_yards
FROM drives
WHERE result IN ('TD', 'FG')
GROUP BY team_id
ORDER BY scoring_drives DESC;

-- Average drive statistics
SELECT team_id, 
       COUNT(*) as total_drives,
       AVG(yards) as avg_yards,
       AVG(plays_count) as avg_plays,
       SUM(CASE WHEN result = 'TD' THEN 1 ELSE 0 END) as touchdowns
FROM drives
GROUP BY team_id
ORDER BY touchdowns DESC;
```

### Play-by-Play

```sql
-- Scoring plays
SELECT game_id, play_text, away_score, home_score
FROM plays
WHERE scoring_play = 1
ORDER BY game_id DESC
LIMIT 20;

-- Turnovers
SELECT game_id, play_text, period, clock
FROM plays
WHERE turnover = 1
ORDER BY game_id DESC
LIMIT 20;

-- Big plays (explosive plays)
SELECT game_id, play_text, yards_gained
FROM plays
WHERE yards_gained > 20
ORDER BY yards_gained DESC
LIMIT 20;
```

---

## 🔍 Cross-Database Queries

### Coaches with Upcoming Games

```sql
-- In coaches_master.db, find coach ID
SELECT id, name, school FROM coaches WHERE school = 'Michigan';

-- Then in predictions.db
SELECT home_team, away_team, game_date, spread
FROM upcoming_games
WHERE home_team = 'Michigan' OR away_team = 'Michigan';
```

### Team Performance vs Rankings

```sql
-- Get team stats from predictions.db
SELECT team, points_per_game FROM team_offensive_stats WHERE team = 'Alabama';

-- Get team rankings from predictions.db
SELECT rank, team FROM ap_poll_rankings WHERE team = 'Alabama';
```

---

## 💡 Tips for Querying

1. **Use EXPLAIN QUERY PLAN** to optimize slow queries:
   ```sql
   EXPLAIN QUERY PLAN
   SELECT * FROM coaches WHERE school = 'Ohio State';
   ```

2. **Create temporary indexes for one-time queries**:
   ```sql
   CREATE INDEX IF NOT EXISTS idx_temp ON table_name(column_name);
   ```

3. **Use LIMIT** to preview large result sets:
   ```sql
   SELECT * FROM table_name LIMIT 10;
   ```

4. **Check table schema**:
   ```sql
   .schema table_name
   ```

5. **Count rows efficiently**:
   ```sql
   SELECT COUNT(*) FROM table_name;
   ```

---

## 🛠️ Running These Queries

### Command Line:
```bash
# coaches_master.db
sqlite3 instance/coaches_master.db < query.sql

# predictions.db
sqlite3 instance/predictions.db < query.sql

# Interactive mode
sqlite3 instance/coaches_master.db
sqlite> SELECT * FROM coaches LIMIT 5;
```

### Python:
```python
import sqlite3

conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()

cursor.execute('SELECT name, school FROM coaches LIMIT 5')
for row in cursor.fetchall():
    print(row)

conn.close()
```

### Flask Application:
```python
from flask import g
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('instance/coaches_master.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# In route
db = get_db()
cursor = db.cursor()
cursor.execute('SELECT * FROM coaches')
coaches = cursor.fetchall()
```

---

**Related Documentation:**
- `DATABASE_INVENTORY.md` - Complete database inventory
- `DATABASE_QUICK_REFERENCE.md` - Quick reference guide
- `create_espn_tables.sql` - Table schemas
- `DATABASE_SCHEMA_COMPLETE.md` - Schema documentation

**Last Updated:** December 16, 2025
