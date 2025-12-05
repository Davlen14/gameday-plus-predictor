Last login: Wed Dec  3 07:30:15 on ttys101
davlenswain@MacBookPro ~ % cd '/Users/davlenswain/Desktop/Gameday_Graphql_Model' && echo '🐍 Starting Flask Backend...' && source .venv/bin/activate && echo '   ✅ Virtual environment activated' && python app.py 2>&1 | tee logs/backend.log
🐍 Starting Flask Backend...
   ✅ Virtual environment activated
🔍 DEBUG: Calling GraphQL with week=15, year=2025
🔍 DEBUG: GraphQL response status: 200
🔍 DEBUG: Response keys: ['data']
🔍 DEBUG: Found 32 games in response
✅ Fetched 32 games with live betting lines from GraphQL
✅ Using live data from GraphQL API
✅ Loaded 1 games from Currentweekgames.json

============================================================
🚀 Starting Flask Backend Server
============================================================
   Host: 0.0.0.0 (all interfaces)
   Port: 5002
   Debug: True
   CORS: Enabled for localhost:5173, localhost:3000
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002
 * Running on http://192.168.1.67:5002
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 408-150-186
127.0.0.1 - - [03/Dec/2025 07:30:21] "GET /health HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:30:37] "OPTIONS /predict HTTP/1.1" 200 -
DataSanityWarning: Extreme total discrepancy detected (>12 points)
127.0.0.1 - - [03/Dec/2025 07:30:41] "POST /predict HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:30:41] "GET /api/live-game?home=Ohio%20State&away=Indiana HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:31:25] "GET /api/player-props/Ohio%20State/Indiana HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:33:25] "OPTIONS /predict HTTP/1.1" 200 -
🔍 DEBUG: Calling GraphQL with week=15, year=2025
🔍 DEBUG: GraphQL response status: 200
🔍 DEBUG: Response keys: ['data']
🔍 DEBUG: Found 32 games in response
✅ Fetched 32 games with live betting lines from GraphQL
✅ Using live data from GraphQL API
✅ Loaded 1 games from Currentweekgames.json

============================================================
🚀 Starting Flask Backend Server
============================================================
   Host: 0.0.0.0 (all interfaces)
   Port: 5002
   Debug: True
   CORS: Enabled for localhost:5173, localhost:3000
============================================================

🔍 Looking up teams: Ohio State (home) vs Indiana (away)
✅ Ohio State (ID: 194)
✅ Indiana (ID: 84)

Predicting game: Ohio State vs Indiana
🔍 Checking rivalry for: 'Ohio State' vs 'Indiana'
   ℹ️  Not a rivalry game
⚠️  Warning: Could not load static data files: [Errno 2] No such file or directory: '/Users/davlenswain/Desktop/Gameday_Graphql_Model/weekly_updates/week_15/coaches_simplified_ranked.json'
   Prediction will work with real-time data only
✅ Static data loaded successfully!
🔍 Debug: Calling predict_game with IDs: 194, 84
🔍 Debug: Team names in request: 'Ohio State', 'Indiana'
🎯 Found gameId: 401777353 - Fetching market lines...
🎯 Fetching game media information...

================================================================================
📊 GAMEDAY+ GRAPHQL DATA ANALYSIS
================================================================================
🏈 MATCHUP: Indiana @ Ohio State
🚀 ADVANCED METRICS ANALYSIS:
   🎯 Passing EPA Differential: 0.157
   🏃 Rushing EPA Differential: -0.116
   📊 Passing Downs Success Diff: -0.007
   📊 Standard Downs Success Diff: -0.016
   🛡️ Line Yards Differential: -0.476
   🏃‍♂️ Second Level Yards Diff: -0.170
   💨 Open Field Yards Diff: -0.038
   ⭐ Highlight Yards Differential: -0.124
   🎯 ADVANCED DIFFERENTIAL: -0.077

📈 ENHANCED TEAM METRICS (2025 Season):
  🏠 Ohio State:
     Overall EPA: 0.298 | EPA Allowed: 0.015
     Passing EPA: 0.495 | Passing EPA Allowed: 0.093
     Rushing EPA: 0.112 | Rushing EPA Allowed: 0.017
     Success Rate: 0.514 | Success Allowed: 0.349
     Explosiveness: 0.895 | Explosiveness Allowed: 0.935
  ✈️  Indiana:
     Overall EPA: 0.317 | EPA Allowed: 0.049
     Passing EPA: 0.420 | Passing EPA Allowed: 0.176
     Rushing EPA: 0.219 | Rushing EPA Allowed: 0.008
     Success Rate: 0.518 | Success Allowed: 0.337
     Explosiveness: 0.976 | Explosiveness Allowed: 0.998

🏈 SITUATIONAL PERFORMANCE:
  🏠 Ohio State:
     Passing Downs Success: 0.339 | Allowed: 0.257
     Standard Downs Success: 0.548 | Allowed: 0.435
  ✈️  Indiana:
     Passing Downs Success: 0.351 | Allowed: 0.263
     Standard Downs Success: 0.540 | Allowed: 0.410

🎯 FIELD POSITION & YARDS BREAKDOWN:
  🏠 Ohio State:
     Line Yards: 2.964 | Allowed: 2.659
     Second Level: 1.081 | Allowed: 0.883
     Open Field: 1.137 | Allowed: 0.937
     Highlight Yards: 1.860 | Allowed: 1.563
  ✈️  Indiana:
     Line Yards: 3.248 | Allowed: 2.466
     Second Level: 1.221 | Allowed: 0.854
     Open Field: 1.530 | Allowed: 1.292
     Highlight Yards: 2.340 | Allowed: 1.919

🎯 COMPREHENSIVE DIFFERENTIAL ANALYSIS:
     📊 EPA Differentials:
        Overall EPA: 0.015
        Passing EPA: 0.157
        Rushing EPA: -0.116
     ⚡ Performance Metrics:
        Success Rate: -0.016
        Explosiveness: -0.017
     🏈 Situational Success:
        Passing Downs: -0.007
        Standard Downs: -0.016
     📍 Field Position Control:
        Line Yards: -0.476
        Second Level: -0.170
        Open Field: -0.038
        Highlight Yards: -0.124
     🛡️  Defensive Edge:
        EPA Defense: -0.015
        Passing Defense: -0.157
        Rushing Defense: 0.116
        Success Defense: 0.016
        Explosiveness Defense: 0.017
        Situational Defense: 0.012

🌟 TALENT RATINGS:
  🏠 Ohio State: 973.69
  ✈️  Indiana: 645.34
  📊 Talent Gap: -328.4 (Away advantage)

🗓️  2025 SEASON RECORDS & RESULTS:
  Ohio State: 12-0
    Week 8: @ Wisconsin W 34-0
    Week 10: vs Penn State W 38-14
    Week 11: @ Purdue W 34-10
    Week 12: vs UCLA W 48-10
    Week 13: vs Rutgers W 42-9
    Week 14: @ Michigan W 27-9
  Indiana: 12-0
    Week 8: vs Michigan State W 38-13
    Week 9: vs UCLA W 56-6
    Week 10: @ Maryland W 55-10
    Week 11: @ Penn State W 27-24
    Week 12: vs Wisconsin W 31-7
    Week 14: @ Purdue W 56-3

⚡ ELO RATINGS (Current):
  🏠 Ohio State: 2169
  ✈️  Indiana: 2191
  📊 ELO Gap: +22 (Away advantage)

🎯 ENHANCED ANALYSIS (WORKING SCHEMA):
  🎯 Home FPI: 28.505
  🎯 Away FPI: 28.388
  🎯 Home ELO: 2169
  🎯 Away ELO: 2191
  🌤️ Temperature: 53.4°F
  🌤️ Wind: 4.7 mph
  🌤️ Precipitation: 0.0 in
  🏆 Poll data: 50 rankings available with team mapping!
  📅 Calendar data available: 0 weeks
  📊 Market lines: 3 sportsbooks available!
  🏆 Poll data: Available with team mapping!
================================================================================

================================================================================
🎯 APPLYING OPTIMAL WEIGHTS (Research Framework)
================================================================================

📊 [1/5] OPPONENT-ADJUSTED METRICS (50%)
🚀 ADVANCED METRICS ANALYSIS:
   🎯 Passing EPA Differential: 0.157
   🏃 Rushing EPA Differential: -0.116
   📊 Passing Downs Success Diff: -0.007
   📊 Standard Downs Success Diff: -0.016
   🛡️ Line Yards Differential: -0.476
   🏃‍♂️ Second Level Yards Diff: -0.170
   💨 Open Field Yards Diff: -0.038
   ⭐ Highlight Yards Differential: -0.124
   🎯 ADVANCED DIFFERENTIAL: -0.077
   Advanced Metrics Diff: -0.077
   Temporal Performance Diff: 1.415
   SoS Adjustment: 0.443
   ✅ Final Component: 0.273

💰 [2/5] MARKET CONSENSUS (20%)
📊 MARKET LINES ANALYSIS:
   📈 Found 3 sportsbook(s)
   🏈 ESPN Bet: Spread -5.5
   🎯 ESPN Bet: Total 48.5
   🏈 DraftKings: Spread -4.0
   🎯 DraftKings: Total 47.5
   🏈 Bovada: Spread -4.0
   🎯 Bovada: Total 47.5
   📊 Consensus Spread: -4.5
   📊 Consensus Total: 47.8
   💰 Moneylines: Home -201 / Away +168
   🎯 Market Consensus Signal: 0.450
   ✅ Market Signal: 0.450

🏆 [3/5] COMPOSITE RATINGS - TALENT (15%)
🎯 COMPOSITE RATINGS (NORMALIZED SIGNALS):
   Home ELO: 2169 | Away ELO: 2191
   ELO Differential: -22
   ELO Win Probability: 46.8%
   ELO Normalized Signal: -0.066
   FPI Differential: +0.12
   FPI Normalized Signal: +0.012
   Mismatch Multiplier: 1.0x
   Composite Signal: -0.035
   Ratings Diff (ELO/FPI): -0.035
   Talent Diff (raw): 328.4 -> normalized: 0.328
   ✅ Composite Score: 0.074

⭐ [4/5] KEY PLAYER IMPACT (10%)
⭐ KEY PLAYERS ANALYSIS:
   📊 Loaded comprehensive player database:
      🏈 203 QBs analyzed
      🏃 543 RBs analyzed
      📡 739 WRs analyzed
      🛡️  1577 DBs analyzed

   🏠 Ohio State Key Players:
      QB: Julian Sayin - Efficiency: 264.0
      RB1: Bo Jackson - Efficiency: 0.0
      RB2: Isaiah West - Efficiency: 0.0
      WR1: Mylan Graham - Efficiency: 0.0
      WR2: Jeremiah Smith - Efficiency: 0.0
      WR3: Brandon Inniss - Efficiency: 0.0

   ✈️  Indiana Key Players:
      QB: Fernando Mendoza - Efficiency: 282.4
      RB1: Lee Beebe - Efficiency: 0.0
      RB2: Roman Hemby - Efficiency: 0.0
      WR1: Elijah Sarratt - Efficiency: 0.0
      WR2: Omar Cooper Jr. - Efficiency: 0.0
      WR3: Charlie Becker - Efficiency: 0.0
   🎯 POSITIONAL BREAKDOWN:
      QB Impact (40%): -0.178
      Skill Positions (35%): -0.019
      Defense (25%): -0.152
   ✅ Total Player Impact: -0.116
   ✅ Player Differential: -0.116
✅ Using specific game weather for game 401777353: 30.4°F, 4.6 mph wind
🌤️  Using REAL weather data from API

🌤️  [5/5] CONTEXTUAL FACTORS (5%)
🌤️  WEATHER ANALYSIS:
   Temperature: 30.4°F
   Wind Speed: 4.6 mph
   Precipitation: 0.0 in
   Weather Factor: 2.0
📊 POLL ANALYSIS (WITH TEAM MAPPING):
   🏠 Ohio State: Rank #1 (1645 pts)
   ✈️  Indiana: Rank #2 (1589 pts)
   📊 Poll Advantage: +0.05 (Home team)
📅 BYE WEEK ANALYSIS:
   Home Bye Weeks: [4, 9, 10, 11, 12, 13, 14]
   Away Bye Weeks: [6, 13]
   Bye Advantage: 5.0
   Weather Impact: 2.000
   Poll Momentum: 0.050
   Bye Week Advantage: 5.000
   ✅ Contextual Score: 2.315

================================================================================
🎲 DYNAMIC WEIGHT CALCULATION
================================================================================
   🤝 EVEN MATCHUP (ELO diff 22): EPA weighted higher (35%)
   🎯 RATING CONSENSUS 94%: Composite boosted +10%

================================================================================
⚖️  WEIGHTED COMPOSITE CALCULATION (DYNAMIC)
================================================================================
   Opponent-Adjusted (31%): 0.086
   Market Consensus (5%):   0.022
   Composite Ratings (44%):  0.032
   Key Player Impact (8%):  -0.009
   Contextual Factors (2%): 0.046

   🎯 RAW DIFFERENTIAL: 0.177
🌤️  WEATHER ANALYSIS:
   Temperature: 30.4°F
   Wind Speed: 4.6 mph
   Precipitation: 0.0 in
   Weather Factor: 2.0

🛡️  DEFENSIVE MISMATCH ANALYSIS
   Home Def vs Away Off: +0.0
   Away Def vs Home Off: +0.0
   Defensive Advantage: +0.00
   Defensive Dampener: 100.00%
   📊 Comprehensive Enhancement: -1.373
      • EPA Diff: +0.015
      • Success Diff: -0.004
      • Explosiveness Diff: -0.080
      • ELO Diff: -22.000
      • Consistency Diff: +0.345
      • Recent vs Early: +0.032
      • Trend Diff: +0.000
      • Defensive Advantage: +0.000 (weight: 10%)
   🚀 Enhancement Factor: +0.000
   🏠 Home Field Advantage: +2.5
   🏆 Conference Bonus: +1.0
   🌧️  Weather Penalty: -2.0

   🎯 ADJUSTED DIFFERENTIAL: 0.274

================================================================================
🎲 PROBABILITY CALIBRATION (Platt Scaling)
================================================================================
   Raw Probability: 50.6%
   Calibrated Probability: 50.6%
   Calibration Adjustment: +0.0 percentage points

================================================================================
🎯 FINAL PREDICTION
================================================================================
   Spread: +0.3 (Home)
   Total: 69.5
   Ohio State: 35 points
   Indiana: 35 points
   Win Probability: Ohio State 50.6% | Indiana 49.4%
🔢 CONFIDENCE BREAKDOWN:
   Base Data: 0.90
   Consistency: +0.07
   Differential: +0.01
   Trend Factor: +0.05
   Weather/Calendar: +0.05
   TOTAL CONFIDENCE: 0.95

🔍 DEBUG: Capturing detailed analysis data...
   - Advanced metrics details: <class 'dict'>, keys: dict_keys(['overall_epa_diff', 'passing_epa_diff', 'rushing_epa_diff', 'success_rate_diff', 'explosiveness_diff', 'passing_downs_diff', 'standard_downs_diff', 'line_yards_diff', 'second_level_diff', 'open_field_diff', 'highlight_yards_diff', 'epa_defense_diff', 'passing_defense_diff', 'rushing_defense_diff', 'success_defense_diff', 'explosiveness_defense_diff', 'situational_defense_diff'])
   - Home record: 12-0
   - Away record: 12-0
   - Home poll rank: None
   - Away poll rank: None

🔢 ALGORITHM WEIGHTS & METHODOLOGY:
     🎯 Advanced Metrics: 44% (Primary Factor)
        - Passing/Rushing EPA, Success Rates, Field Position
        - Situational Performance, Big Play Capability
     📊 Composite Ratings: 35% (FPI + ELO)
        - Expert Rankings & Statistical Models
     🌤️  Environmental: 15% (Weather & Bye Weeks)
        - Temperature, Wind, Precipitation Impact
        - Rest Advantage Analysis
     💪 Team Quality: 6% (Talent & Consistency)
        - Recruiting Rankings & Performance Trends

💰 CORRECTED BETTING ANALYSIS:
==================================================
Model Projection: Indiana -0.3  (Total 69.5)
Market Consensus: Indiana +4.5  (Total 47.8)
Value Edge (spread): -4.8 points
Best Available Spread Line: Indiana +5.5 @ ESPN Bet
✅ Indiana +5.5 @ ESPN Bet — Market overvaluing Ohio State
Value Edge (total): +21.7 points
Best Available Total Line: OVER 47.5 @ DraftKings
✅ OVER 47.5 @ DraftKings — Model projects higher scoring
DataSanityWarning: Extreme total discrepancy detected (>12 points)

================================================================================
🔢 OPTIMIZED ALGORITHM WEIGHTS (Research Framework)
================================================================================
     🎯 Opponent-Adjusted Metrics: 31% (Primary Factor)
        - Play-by-play EPA, Success Rates with SoS adjustment
        - Dixon-Coles temporal weighting for recency
        - Field position, explosiveness, situational performance

     � Market Consensus: 5% ⬆️ (Strong Bayesian Prior)
        - Betting lines as information aggregator
        - Sportsbook consensus signal

     🏆 Composite Ratings: 44% (Talent/Rankings)
        - ELO, FPI ratings
        - Recruiting rankings

     ⭐ Key Player Impact: 8% ⬆️ (Value-Based)
        - Individual player metrics
        - Star player differential

     🌤️  Contextual Factors: 2%
        - Weather, bye weeks, travel
        - Poll momentum, coaching stability

     🎲 Calibration: Platt Scaling
        - Transforms raw probabilities to calibrated estimates
================================================================================

================================================================================
📊 COMPREHENSIVE TEAM STATISTICS
================================================================================

👨‍🏫 COACHING ANALYSIS:

🚗 DRIVE EFFICIENCY & GAME FLOW:
================================================================================

🏈 Indiana @ Ohio State
🎯 Home Win Probability: 50.6%
📊 Predicted Spread: Ohio State +0.3
🔢 Predicted Total: 69.5
🎪 Confidence: 80.8%

💰 VALUE PICK (Spread): ✅ Indiana +5.5 @ ESPN Bet — Market overvaluing Ohio State (4.8-point edge)
💰 VALUE PICK (Total): ✅ OVER 47.5 @ DraftKings — Model projects higher scoring (21.7-point edge)

🔑 Key Factors: Talent advantage, More consistent performance, 📅 Enhanced bye week analysis available, ✅ Comprehensive data: market lines, composite ratings (ELO/FPI), poll rankings, weather data, 📊 Model aligns with market consensus, ⚖️ Evenly matched teams, ⚠️ DataSanityWarning: Extreme total discrepancy detected (>12 points)
🎨 TEAM LOGOS:
   🏠 Ohio State: https://a.espncdn.com/i/teamlogos/ncaa/500/194.png (light), https://a.espncdn.com/i/teamlogos/ncaa/500-dark/194.png (dark)
   ✈️  Indiana: https://a.espncdn.com/i/teamlogos/ncaa/500/84.png (light), https://a.espncdn.com/i/teamlogos/ncaa/500-dark/84.png (dark)

================================================================================
🎯 GENERATING COMPREHENSIVE 18-SECTION ANALYSIS...
================================================================================
🔍 DEBUG: Captured 11 sections in formatted analysis
🔍 DEBUG: Total analysis length: 10239 characters
⚠️  WARNING: Only 11 sections captured, expected 18
🎯 Integrating betting lines for Ohio State vs Indiana
🔍 Model spread: 0.3, Model total: 69.5
🔍 DEBUG: home_team_data.get('school') = 'None'
🔍 DEBUG: away_team_data.get('school') = 'None'
🔍 DEBUG: Calling betting_manager.get_betting_analysis('Ohio State', 'Indiana', 0.3, 69.5)
🔍 Same favorite (Ohio State): Market 4.5 - Model 0.3 = 4.2
🔍 Model spread raw: 0.3, Market spread raw: -4.5
📊 Betting analysis integrated: College Football Data API
🔍 DEBUG: betting_analysis keys: ['market_spread', 'market_total', 'formatted_spread', 'spread_edge', 'total_edge', 'spread_recommendation', 'total_recommendation', 'is_upset_alert', 'model_favorite', 'market_favorite', 'sportsbooks', 'data_source', 'last_updated']
🔍 DEBUG: individual_books count: 3
🔍 DEBUG: Flask weather_data keys: ['temperature', 'wind_speed', 'precipitation', 'humidity', 'dewpoint', 'pressure', 'snowfall', 'wind_direction', 'wind_gust', 'weather_condition_code']
DataSanityWarning: Extreme total discrepancy detected (>12 points)
127.0.0.1 - - [03/Dec/2025 07:33:27] "POST /predict HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:33:27] "GET /api/live-game?home=Ohio%20State&away=Indiana HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 07:34:07] "GET /api/player-props/Ohio%20State/Indiana HTTP/1.1" 200 -
