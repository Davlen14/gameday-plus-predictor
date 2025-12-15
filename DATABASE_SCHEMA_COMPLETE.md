# 🗄️ Complete Database Schema - All 11 Tables

**Database**: `coaches_master.db`  
**Matt Campbell ID**: 26  
**Last Updated**: December 9, 2025

---

## 📊 Table Summary

| Table | Columns | Matt Campbell Records | Purpose |
|-------|---------|----------------------|---------|
| **coaches** | 11 | 1 | Coach biographical data |
| **stints** | 8 | 2 | Coaching positions at schools |
| **games** | 21 | 177 | Individual game results |
| **season_analytics** | 28 | 15 | Per-season aggregate stats |
| **rankings** | 6 | 115 | Weekly AP Poll rankings |
| **draft_picks** | 9 | 15 | NFL Draft players coached |
| **recruiting_classes** | 11 | 16 | Annual recruiting class data |
| **talent_composite** | 6 | 22 | 247Sports talent rankings |
| **transfer_portal** | 7 | 8 | Transfer portal activity |
| **situational_stats** | 18 | 2 | Contextual performance |
| **vs_coaches** | 9 | 0 | Head-to-head coaching records |

---

## 1️⃣ COACHES

**Purpose**: Core biographical and career summary data for each coach

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment coach ID |
| name | VARCHAR(100) | NOT NULL | Full coach name |
| current_school | VARCHAR(100) | NOT NULL | Current coaching position |
| headshot_url | TEXT | NULL | Photo URL |
| career_record | VARCHAR(20) | NOT NULL | Overall W-L record (e.g., "108-69") |
| career_win_pct | FLOAT | NOT NULL | Decimal win percentage |
| total_games | INTEGER | NOT NULL | Career games coached |
| espn_id | TEXT | NULL | ESPN coach identifier |
| cfbd_id | INTEGER | NULL | CFBD API coach ID |
| created_at | DATETIME | NOT NULL | Record creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update timestamp |

**Sample Record (Matt Campbell)**:
```
id: 26
name: Matt Campbell
current_school: Iowa State
career_record: 108-69
career_win_pct: 0.61
total_games: 177
```

---

## 2️⃣ STINTS

**Purpose**: Each coaching position at a school with tenure dates

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment stint ID |
| coach_id | INTEGER | NOT NULL | Foreign key to coaches.id |
| school | VARCHAR(100) | NOT NULL | School name |
| start_year | INTEGER | NOT NULL | First season |
| end_year | INTEGER | NOT NULL | Last season (or current year) |
| games | INTEGER | NULL | Total games in stint |
| wins | INTEGER | NULL | Wins in stint |
| losses | INTEGER | NULL | Losses in stint |

**Sample Records (Matt Campbell)**:
```
Toledo:    2011-2015 (36-14)
Iowa State: 2016-2025 (72-55)
```

---

## 3️⃣ GAMES ⚠️ **CRITICAL ISSUE**

**Purpose**: Individual game results with opponent advanced metrics

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment game ID |
| coach_id | INTEGER | NOT NULL | Foreign key to coaches.id |
| season | INTEGER | NOT NULL | Year (e.g., 2025) |
| week | INTEGER | NOT NULL | Week number |
| season_type | VARCHAR(20) | NULL | "regular" or "postseason" |
| school | VARCHAR(100) | NOT NULL | Coach's team |
| opponent | VARCHAR(100) | NOT NULL | Opponent team name |
| opponent_logo | TEXT | NULL | ESPN logo URL |
| result | VARCHAR(1) | NOT NULL | "W" or "L" |
| coach_score | INTEGER | NOT NULL | Coach's team points |
| opponent_score | INTEGER | NOT NULL | Opponent points |
| opponent_sp_overall | FLOAT | NULL | SP+ overall rating |
| opponent_sp_offense | FLOAT | NULL | SP+ offensive rating |
| opponent_sp_defense | FLOAT | NULL | SP+ defensive rating |
| opponent_fpi | FLOAT | NULL | FPI rating |
| opponent_srs | FLOAT | NULL | Simple Rating System |
| excitement_index | FLOAT | NULL | Game excitement score |
| is_home | BOOLEAN | NOT NULL | 1 if home game |
| is_neutral | BOOLEAN | NOT NULL | 1 if neutral site |
| is_conference | BOOLEAN | NOT NULL | 1 if conference game |
| is_signature | BOOLEAN | NOT NULL | 1 if signature win |

### ⚠️ CRITICAL PROBLEM IDENTIFIED

**Status**: All opponent advanced metrics are **NULL** for all 177 Matt Campbell games

**Expected Values** (from your screenshot):
- opponent_fpi: -11.894, 4.555, 8.846, etc.
- opponent_logo: `http://a.espncdn.com/i/teamlogos/ncaa/500/197.png`
- opponent_sp_defense: 31.9, 28.9, 24.2, etc.
- opponent_sp_offense: 15.9, 31.5, 32.8, etc.
- opponent_sp_overall: -15.6, 3.2, 8.2, etc.
- opponent_srs: -10.5, 4.1, 8.3, etc.

**Actual Values** (current database):
- opponent_fpi: NULL
- opponent_logo: NULL
- opponent_sp_defense: NULL
- opponent_sp_offense: NULL
- opponent_sp_overall: NULL
- opponent_srs: NULL

**Root Cause**: The GraphQL games query in `ingest_coach_graphql.py` only fetches:
```graphql
id, season, week, homeTeam, awayTeam, homePoints, awayPoints, 
excitement, neutralSite, conferenceGame
```

**Missing Fields**:
- `opponent_fpi` - requires separate team season FPI query
- `opponent_logo` - ESPN logo URLs
- `opponent_sp_*` - requires SP+ ratings API query
- `opponent_srs` - requires SRS ratings query

---

## 4️⃣ SEASON_ANALYTICS

**Purpose**: Per-season aggregate offensive and defensive statistics

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| season | INTEGER | NOT NULL | Year |
| school | VARCHAR(100) | NOT NULL | School name |
| points_per_game | FLOAT | NULL | Offensive PPG |
| yards_per_game | FLOAT | NULL | Total yards per game |
| yards_per_play | FLOAT | NULL | Yards per play |
| passing_yards_pg | FLOAT | NULL | Pass yards per game |
| rushing_yards_pg | FLOAT | NULL | Rush yards per game |
| third_down_pct | FLOAT | NULL | 3rd down conversion % |
| fourth_down_pct | FLOAT | NULL | 4th down conversion % |
| red_zone_pct | FLOAT | NULL | Red zone TD % |
| points_allowed_pg | FLOAT | NULL | Defensive points allowed |
| yards_allowed_pg | FLOAT | NULL | Yards allowed per game |
| yards_per_play_allowed | FLOAT | NULL | YPP allowed |
| passing_yards_allowed_pg | FLOAT | NULL | Pass yards allowed |
| rushing_yards_allowed_pg | FLOAT | NULL | Rush yards allowed |
| sacks_per_game | FLOAT | NULL | Sacks per game |
| tackles_for_loss_pg | FLOAT | NULL | TFL per game |
| turnovers_gained_pg | FLOAT | NULL | Takeaways per game |
| sp_overall | FLOAT | NULL | SP+ overall rating |
| sp_offense | FLOAT | NULL | SP+ offense rating |
| sp_defense | FLOAT | NULL | SP+ defense rating |
| fpi | FLOAT | NULL | FPI rating |
| srs | FLOAT | NULL | SRS rating |
| elo_rating | FLOAT | NULL | Elo rating |
| avg_time_of_possession | FLOAT | NULL | TOP in minutes |
| pace_plays_per_game | FLOAT | NULL | Plays per game |

**Data Quality**: ✅ Working correctly after REST API parsing fix

---

## 5️⃣ RANKINGS

**Purpose**: Weekly AP Poll rankings

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| season | INTEGER | NOT NULL | Year |
| week | INTEGER | NOT NULL | Week number |
| rank | INTEGER | NOT NULL | AP Poll rank (1-25) |
| school | VARCHAR(100) | NOT NULL | School name |

**Matt Campbell**: 115 ranked weeks across both Toledo and Iowa State

---

## 6️⃣ DRAFT_PICKS

**Purpose**: NFL Draft selections of players coached

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| player_name | VARCHAR(100) | NOT NULL | Player full name |
| year | INTEGER | NOT NULL | Draft year |
| round | INTEGER | NOT NULL | Draft round |
| pick | INTEGER | NULL | Overall pick number |
| nfl_team | VARCHAR(100) | NOT NULL | NFL team name |
| college_school | VARCHAR(100) | NULL | College school |
| position | VARCHAR(10) | NULL | Position code |

**Matt Campbell**: 15 draft picks (properly filtered by tenure)

---

## 7️⃣ RECRUITING_CLASSES

**Purpose**: Annual recruiting class rankings and composition

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| school | VARCHAR(100) | NOT NULL | School name |
| year | INTEGER | NOT NULL | Recruiting class year |
| class_rank | INTEGER | NULL | National ranking |
| total_commits | INTEGER | NULL | Number of commits |
| avg_rating | FLOAT | NULL | Average star rating |
| total_rating | FLOAT | NULL | Composite rating |
| five_stars | INTEGER | NULL | 5-star recruits |
| four_stars | INTEGER | NULL | 4-star recruits |
| three_stars | INTEGER | NULL | 3-star recruits |

**Matt Campbell**: 16 recruiting classes

---

## 8️⃣ TALENT_COMPOSITE

**Purpose**: 247Sports team talent composite rankings

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| school | VARCHAR(100) | NOT NULL | School name |
| year | INTEGER | NOT NULL | Year |
| talent_rank | INTEGER | NULL | National talent rank |
| talent_rating | FLOAT | NULL | Composite talent score |

**Matt Campbell**: 22 years of talent data

---

## 9️⃣ TRANSFER_PORTAL

**Purpose**: Transfer portal incoming and outgoing player counts

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| school | VARCHAR(100) | NOT NULL | School name |
| year | INTEGER | NOT NULL | Year |
| transfers_in | INTEGER | NULL | Incoming transfers |
| transfers_out | INTEGER | NULL | Outgoing transfers |
| net_transfers | INTEGER | NULL | Net transfer balance |

**Matt Campbell**: 8 seasons of portal data

---

## 🔟 SITUATIONAL_STATS

**Purpose**: Contextual performance metrics (vs ranked, home/away, etc.)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| stint_id | INTEGER | NULL | Foreign key to stints.id |
| school | VARCHAR(100) | NULL | School name |
| vs_ranked_record | VARCHAR(10) | NULL | Record vs AP ranked teams |
| vs_top_10_record | VARCHAR(10) | NULL | Record vs Top 10 |
| vs_top_25_record | VARCHAR(10) | NULL | Record vs Top 25 |
| home_record | VARCHAR(10) | NULL | Home game record |
| away_record | VARCHAR(10) | NULL | Away game record |
| neutral_record | VARCHAR(10) | NULL | Neutral site record |
| blowout_wins | INTEGER | NULL | Wins by 20+ points |
| blowout_losses | INTEGER | NULL | Losses by 20+ points |
| one_score_wins | INTEGER | NULL | Wins by ≤8 points |
| one_score_losses | INTEGER | NULL | Losses by ≤8 points |
| comeback_wins | INTEGER | NULL | Wins after trailing |
| conference_record | VARCHAR(10) | NULL | Conference game record |
| conference_championship_appearances | INTEGER | NULL | CCG appearances |
| bowl_record | VARCHAR(10) | NULL | Bowl game record |

**Data Quality**: ✅ Working correctly, 2 records (Toledo + Iowa State)

---

## 1️⃣1️⃣ VS_COACHES

**Purpose**: Head-to-head records against other coaches

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | INTEGER | PRIMARY | Auto-increment ID |
| coach_id | INTEGER | NOT NULL | Foreign key |
| opponent_coach_id | INTEGER | NOT NULL | Opposing coach ID |
| opponent_coach_name | VARCHAR(100) | NOT NULL | Opposing coach name |
| school | VARCHAR(100) | NULL | Coach's school |
| opponent_school | VARCHAR(100) | NULL | Opponent school |
| wins | INTEGER | NULL | Wins vs this coach |
| losses | INTEGER | NULL | Losses vs this coach |
| last_meeting_year | INTEGER | NULL | Most recent matchup year |

**Data Quality**: ⚠️ **EMPTY** - GraphQL query needs opponent coach matching logic

---

## 🔧 Priority Fixes Required

### 1. **GAMES TABLE - Opponent Advanced Metrics** (CRITICAL)

The games table has the correct schema but all opponent metrics are NULL. Need to enhance ingestion script to fetch:

**Required GraphQL Queries**:
1. **Team Season Stats** - for opponent SP+, FPI, SRS ratings
2. **Team Logos** - ESPN logo URLs
3. **Excitement Index** - game excitement ratings

**Impact**: This data is essential for:
- Game quality analysis
- Strength of schedule calculations
- Coaching performance context
- UI display (your screenshot shows all these values)

### 2. **VS_COACHES TABLE** (Low Priority)

Empty because GraphQL game data doesn't include opponent coach information. Would require:
- Cross-referencing game opponents with coach stints
- Matching years to determine which coach was at opponent school
- Aggregating head-to-head records

---

## ✅ Verification Status

**Working Correctly**:
- ✅ Coaches table (1 record)
- ✅ Stints table (2 records: Toledo + Iowa State)
- ✅ Draft picks (15, properly filtered by tenure)
- ✅ Situational stats (2 records with correct stint IDs)
- ✅ Season analytics (15 records with real PPG/YPG data)
- ✅ Recruiting classes (16 classes)
- ✅ Talent composite (22 years)
- ✅ Transfer portal (8 seasons)
- ✅ Rankings (115 weeks ranked)

**Needs Enhancement**:
- ⚠️ Games table - all opponent metrics NULL (177 games affected)
- ⚠️ VS Coaches table - empty (documented but not blocking)

---

## 📝 Next Steps

1. **Fix games opponent metrics ingestion** - add GraphQL queries for:
   - Team season stats (SP+, FPI, SRS)
   - ESPN logo URLs
   - Excitement index values

2. **Re-ingest Matt Campbell** with enhanced script

3. **Verify all metrics match your screenshot** (opponent_fpi, opponent_sp_*, opponent_srs)

4. **Bulk ingest all 134 FBS coaches** after verification

---

**Database Location**: `instance/coaches_master.db`  
**Ingestion Script**: `ingest_coach_graphql.py`  
**Verification Script**: `verify_campbell_data.py`
