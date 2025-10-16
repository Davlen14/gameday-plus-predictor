# 🎯 PROMPT FOR YOUR OTHER AI PROJECT

Copy and paste this into your other AI project to fetch historical game data:

---

## **PROMPT:**

```
I need to fetch comprehensive historical college football game data for backtesting a prediction model. 

Please create a script that queries the college football API and exports complete game data in JSON Lines format.

REQUIREMENTS:

📅 TIME PERIODS:
1. 2025 Season - Weeks 1-6 (all completed games)
2. 2024 Season - Full season (Weeks 1-15 + Bowl games + Playoffs)

📊 DATA FIELDS PER GAME:

### Core Game Info (MUST HAVE):
- game_id (unique identifier)
- season (year)
- week (week number)
- season_type ("regular" or "postseason")
- neutral_site (boolean)
- conference_game (boolean)
- completed (boolean - only include completed games)
- start_date (ISO format timestamp)

### Teams (MUST HAVE):
- home_team (name)
- home_team_id (numeric ID)
- home_conference
- away_team (name)
- away_team_id (numeric ID)
- away_conference

### Actual Results (MUST HAVE):
- home_points (final score)
- away_points (final score)
- home_q1, home_q2, home_q3, home_q4 (quarter scores if available)
- away_q1, away_q2, away_q3, away_q4

### Pre-Game Market Lines (CRITICAL):
- opening_spread (home perspective, negative = home favored)
- closing_spread (most important)
- opening_total (over/under)
- closing_total
- Multiple sportsbooks if available:
  - DraftKings, FanDuel, BetMGM, Caesars
  - For each: spread, total, home_moneyline, away_moneyline

### Pre-Game Rankings (IMPORTANT):
- home_rank_ap (null if unranked)
- away_rank_ap
- home_rank_coaches
- away_rank_coaches
- home_record (e.g., "5-0")
- away_record

### Pre-Game Ratings (IMPORTANT):
- home_elo_pregame
- away_elo_pregame
- home_fpi_pregame (ESPN FPI)
- away_fpi_pregame
- home_sp_plus_pregame (if available)
- away_sp_plus_pregame

### Weather (VALUABLE):
- temperature (Fahrenheit)
- wind_speed (mph)
- precipitation (inches)
- weather_condition (text description)
- indoor (boolean)

### Season Stats UP TO THAT GAME (CRITICAL):
For both home and away teams, include their season stats BEFORE this game:
- games_played
- points_per_game
- points_allowed_per_game  
- total_yards_per_game
- yards_allowed_per_game
- turnovers
- takeaways
- turnover_margin
- epa_offense (if available)
- epa_defense
- success_rate_offense
- success_rate_defense
- explosiveness_offense
- explosiveness_defense

### Context (NICE TO HAVE):
- rivalry_game (boolean)
- home_bye_week_before (boolean)
- away_bye_week_before
- home_days_rest (days since last game)
- away_days_rest
- primetime (boolean)
- tv_network

📁 OUTPUT FORMAT:

JSON Lines (.jsonl) - one game per line for efficient processing:

```jsonl
{"game_id":"401635506","season":2024,"week":7,"home_team":"Georgia","home_team_id":61,"away_team":"Texas","away_team_id":251,"home_points":30,"away_points":15,"closing_spread":-14.0,"closing_total":48.0,"home_elo_pregame":1850,"away_elo_pregame":1720,"home_rank_ap":1,"away_rank_ap":5,"home_conference":"SEC","away_conference":"SEC"}
```

Create TWO files:
1. `cfb_historical_2024_full.jsonl` - All 2024 season games
2. `cfb_historical_2025_weeks_1-6.jsonl` - Current season games

🚫 FILTERS:
- Only FBS vs FBS games (exclude FCS opponents)
- Only completed games (no future games)
- Only games with actual scores recorded

✅ VALIDATION:
- Verify all required fields present
- Check for null values in critical fields
- Confirm dates are pre-game snapshots (no data leakage)
- Print summary stats:
  - Total games fetched
  - Date range coverage
  - Missing data report (which fields, how many games)

🎯 PRIORITY:
1. MUST HAVE: Game results, teams, closing spreads
2. HIGH PRIORITY: Pre-game ELO, rankings, season stats
3. NICE TO HAVE: Weather, context, multiple sportsbooks

Please create this script and run it to generate the two .jsonl files. Include error handling and progress indicators for large datasets.

If any fields are unavailable from the API, note them in the output and fetch as much as possible from what's available.
```

---

## ADDITIONAL CONTEXT TO SHARE:

If your AI asks for clarification, provide:

```
Additional context:
- This is for a college football prediction model
- The model predicts: winner, spread, total, win probability
- Need pre-game data only (no hindsight bias)
- Data will be used to calculate: winner accuracy, ATS performance, Brier score, ROI
- Team IDs should match College Football Data API standard IDs
- If using ESPN API: game IDs are in format "401635506"
- If using CFBD API: use their standard team/game IDs
- Closing line is more important than opening line (more information aggregated)
- For season stats, they should reflect cumulative stats UP TO but NOT INCLUDING the game being predicted
```

---

## FOLLOW-UP QUESTIONS TO ASK YOUR AI:

After it generates the script:

1. **"Can you add a data quality report that shows:**
   - Percentage of games with complete market data
   - Percentage with ELO ratings
   - Percentage with weather data
   - Any systematic gaps by week/conference?"

2. **"Can you also create a quick stats summary showing:**
   - Average total points by conference
   - Home team winning percentage overall
   - Favorite winning percentage (by spread size buckets)?"

3. **"Can you validate no data leakage by:**
   - Checking season stats don't include the current game
   - Verifying rankings are from the week BEFORE the game
   - Confirming all timestamps are pre-kickoff?"

---

## EXPECTED OUTPUT:

You should receive:

1. **Script file** (Python/JavaScript/etc.)
2. **Two .jsonl files**:
   - `cfb_historical_2024_full.jsonl` (~850 games)
   - `cfb_historical_2025_weeks_1-6.jsonl` (~400 games)
3. **Data quality report** showing completeness
4. **Summary statistics** for validation

---

## ONCE YOU HAVE THE DATA:

Transfer the .jsonl files to this project directory and I'll create:

1. **Elite backtesting script** that:
   - Loads historical games
   - Runs your predictor on each
   - Compares predictions to actuals
   - Calculates all metrics (win%, ATS, Brier, ROI, MAE)
   - Generates comprehensive report

2. **Visualization dashboard** showing:
   - Accuracy over time
   - Performance by conference
   - Spread size analysis
   - Confidence calibration curves
   - Market edge detection

3. **Performance report** with:
   - Executive summary
   - Detailed metrics
   - Strengths and weaknesses
   - Comparison to baseline models
   - Recommendations for improvement

Ready to make this ELITE! 🚀
