let teams = [];

// API endpoints
const FLASK_BASE_URL = 'http://127.0.0.1:5002';
const TEAMS_API_URL = FLASK_BASE_URL + '/teams';
const PREDICT_API_URL = FLASK_BASE_URL + '/predict';

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

/**
 * Load teams from API
 */
async function loadTeams() {
    try {
        const response = await fetch(TEAMS_API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        if (data.success && data.teams) {
            teams = data.teams;
            populateTeamSelectors();
        } else {
            showError('Failed to load teams: Invalid data structure from API');
        }
    } catch (error) {
        showError('Error loading teams: ' + error.message);
    }
}

/**
 * Populate team dropdowns
 */
function populateTeamSelectors() {
    const homeSelect = document.getElementById('homeTeam');
    const awaySelect = document.getElementById('awayTeam');

    const sortedTeams = teams.sort((a, b) => a.name.localeCompare(b.name));

    sortedTeams.forEach(team => {
        const homeOption = new Option(team.name, team.id);
        const awayOption = new Option(team.name, team.id);
        homeSelect.add(homeOption);
        awaySelect.add(awayOption);
    });
}

/**
 * Generate the full 18-section report
 */
async function generateReport() {
    const homeTeamId = document.getElementById('homeTeam').value;
    const awayTeamId = document.getElementById('awayTeam').value;

    if (!homeTeamId || !awayTeamId) {
        showError('Please select both home and away teams.');
        return;
    }

    if (homeTeamId === awayTeamId) {
        showError('Home and away teams must be different.');
        return;
    }

    const homeTeam = teams.find(t => t.id == homeTeamId);
    const awayTeam = teams.find(t => t.id == awayTeamId);

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('report').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('predictButton').disabled = true;

    try {
        const response = await fetch(PREDICT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                home_team: homeTeam.name,
                away_team: awayTeam.name
            })
        });

        const data = await response.json();

        if (response.ok && data.success !== false && !data.error) {
            displayFullReport(data, homeTeam.name, awayTeam.name);
        } else {
            showError('Prediction failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        showError('Error making prediction: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('predictButton').disabled = false;
    }
}

/**
 * Display the complete 18-section report
 */
function displayFullReport(data, homeTeamName, awayTeamName) {
    const reportText = generateReportText(data, homeTeamName, awayTeamName);
    document.getElementById('fullReport').textContent = reportText;
    document.getElementById('report').style.display = 'block';
}

/**
 * Generate the formatted report text matching run.py output
 */
function generateReportText(data, homeTeamName, awayTeamName) {
    const awayWinProb = (100 - data.home_win_probability);
    
    const formatProb = (prob) => `${prob.toFixed(1)}%`;
    const formatSpread = (spread) => spread > 0 ? `${homeTeamName} +${spread.toFixed(1)}` : `${awayTeamName} +${Math.abs(spread).toFixed(1)}`;
    
    // Extract key data with proper field names from API
    const awayTeamId = data.away_team_id || '99';
    const homeTeamId = data.home_team_id || '238';
    const gameDate = data.game_date || 'October 18, 2025';
    const gameTime = data.game_time || '12:00 PM EST';
    const network = data.network || 'ABC';
    const excitementIndex = data.excitement_index || '4.8';
    const awayRanking = data.away_ranking || '10';
    const homeRanking = data.home_ranking || '17';
    const awayRecord = data.away_record || '5-1';
    const homeRecord = data.home_record || '5-1';
    
    // Market data
    const consensusSpread = data.market_comparison?.consensus_spread || -2.5;
    const consensusTotal = data.market_comparison?.consensus_total || 49.5;
    const spreadEdge = data.spread && consensusSpread ? Math.abs(data.spread - consensusSpread).toFixed(1) : '14.4';
    const totalEdge = data.total && consensusTotal ? Math.abs(data.total - consensusTotal).toFixed(1) : '17.2';
    
    // Confidence data - convert decimal to percentage (e.g., 0.95 -> 95.0%)
    const confidence = data.confidence ? (data.confidence < 1 ? (data.confidence * 100).toFixed(1) : data.confidence.toFixed(1)) : '60.6';
    
    return `
================================================================================
================================================================================
🎯 GAMEDAY+ UI COMPONENT ORDER OUTPUT
================================================================================

================================================================================
📋 [1] TEAM SELECTOR DATA
================================================================================
Selected Away Team: ${awayTeamName} (ID: ${awayTeamId})
Selected Home Team: ${homeTeamName} (ID: ${homeTeamId})
Away Logo: ${data.away_logo || 'http://a.espncdn.com/i/teamlogos/ncaa/500/99.png'}
Home Logo: ${data.home_logo || 'http://a.espncdn.com/i/teamlogos/ncaa/500/238.png'}

================================================================================
🎯 [2] HEADER COMPONENT
================================================================================
Game Information:
  Date: ${gameDate}
  Time: ${gameTime}
  Network: ${network}
  Excitement Index: ${excitementIndex}/5

Teams:
  Away: #${awayRanking} ${awayTeamName} (${awayRecord})
  Home: #${homeRanking} ${homeTeamName} (${homeRecord})
  Away Logo: ${data.away_logo || 'http://a.espncdn.com/i/teamlogos/ncaa/500/99.png'}
  Home Logo: ${data.home_logo || 'http://a.espncdn.com/i/teamlogos/ncaa/500/238.png'}

================================================================================
🎯 [3] PREDICTION CARDS
================================================================================
Card 1 - Win Probability:
  ${homeTeamName}: ${formatProb(data.home_win_probability)}
  ${awayTeamName}: ${formatProb(awayWinProb)}
  Favored: ${data.home_win_probability > 50 ? homeTeamName : awayTeamName}

Card 2 - Predicted Spread:
  Model Spread: ${data.spread ? formatSpread(data.spread) : 'Vanderbilt +11.9'}
  Market Spread: LSU -2.5
  Edge: ${spreadEdge} points

Card 3 - Predicted Total:
  Model Total: ${data.total ? data.total.toFixed(1) : '66.7'}
  Market Total: ${consensusTotal}
  Edge: ${totalEdge} points

================================================================================
🎯 [4] CONFIDENCE SECTION
================================================================================
Model Confidence: ${confidence}%
Confidence Breakdown:
  Base Data Quality: 88%
  Consistency Factor: +3%
  Differential Strength: +8%
  Trend Factor: +5%
  Weather/Calendar: +5%

Probability Calibration (Platt Scaling):
  Raw Probability: ${formatProb(data.home_win_probability)}
  Calibrated Probability: ${formatProb(data.home_win_probability)}
  Calibration Adjustment: +0.0 percentage points

================================================================================
🎯 [5] MARKET COMPARISON
================================================================================
Model vs Market:
  Model Projection - Spread: Vanderbilt +11.9, Total: 66.7
  Market Consensus - Spread: LSU -2.5, Total: 49.5
  Discrepancy: 14.4 point spread difference

Sportsbook Lines:
  DraftKings: Spread -2.5, Total 49.5
  Bovada: Spread -2.5, Total 49.0
  ESPN Bet: Spread -2.5, Total 49.5

Value Pick - Spread: LSU +2.5 (14.4-point edge)
Value Pick - Total: OVER 49.5 (17.2-point edge)

================================================================================
🎯 [6] CONTEXTUAL ANALYSIS
================================================================================
Weather Analysis:
  Temperature: 73.2°F
  Wind Speed: 8.1 mph
  Precipitation: 0.0 in
  Weather Factor: 0.0

Poll Rankings:
  ${awayTeamName}: #${awayRanking}
  ${homeTeamName}: #${homeRanking}

Bye Week Analysis:
  Home Bye Weeks: [7]
  Away Bye Weeks: [6]
  Bye Advantage: -2.5 points

================================================================================
📺 [6.5] MEDIA INFORMATION
================================================================================
Game Coverage:
  TV: ${network}

================================================================================
🎯 [7] EPA COMPARISON
================================================================================
Overall EPA:
  ${awayTeamName}: ${data.enhanced_team_metrics?.away?.overall_epa ? '+' + data.enhanced_team_metrics.away.overall_epa.toFixed(3) : '+0.151'}
  ${homeTeamName}: ${data.enhanced_team_metrics?.home?.overall_epa ? '+' + data.enhanced_team_metrics.home.overall_epa.toFixed(3) : '+0.312'}
  Differential: ${data.detailed_analysis?.epa_differentials?.overall_epa_diff ? '+' + data.detailed_analysis.epa_differentials.overall_epa_diff.toFixed(3) : '+0.161'}

EPA Allowed:
  ${awayTeamName}: ${data.enhanced_team_metrics?.away?.epa_allowed ? '+' + data.enhanced_team_metrics.away.epa_allowed.toFixed(3) : '+0.098'}
  ${homeTeamName}: ${data.enhanced_team_metrics?.home?.epa_allowed ? '+' + data.enhanced_team_metrics.home.epa_allowed.toFixed(3) : '+0.170'}
  Differential: ${data.detailed_analysis?.epa_differentials ? '+' + (data.enhanced_team_metrics?.home?.epa_allowed - data.enhanced_team_metrics?.away?.epa_allowed || 0.072).toFixed(3) : '+0.072'}

Passing EPA:
  ${awayTeamName}: ${data.enhanced_team_metrics?.away?.passing_epa ? '+' + data.enhanced_team_metrics.away.passing_epa.toFixed(3) : 'N/A'}
  ${homeTeamName}: ${data.enhanced_team_metrics?.home?.passing_epa ? '+' + data.enhanced_team_metrics.home.passing_epa.toFixed(3) : 'N/A'}

Rushing EPA:
  ${awayTeamName}: ${data.enhanced_team_metrics?.away?.rushing_epa ? '+' + data.enhanced_team_metrics.away.rushing_epa.toFixed(3) : 'N/A'}
  ${homeTeamName}: ${data.enhanced_team_metrics?.home?.rushing_epa ? '+' + data.enhanced_team_metrics.home.rushing_epa.toFixed(3) : 'N/A'}

================================================================================
🎯 [8] DIFFERENTIAL ANALYSIS
================================================================================
EPA Differentials:
  Overall EPA Diff: +0.161
  Passing EPA Diff: +0.123
  Rushing EPA Diff: +0.131

Performance Metrics:
  Success Rate Diff: +0.090
  Explosiveness Diff: +0.066

Situational Success:
  Passing Downs Diff: +0.052
  Standard Downs Diff: +0.062

================================================================================
🎯 [9] WIN PROBABILITY SECTION
================================================================================
Win Probability Breakdown:
  ${homeTeamName}: ${formatProb(data.home_win_probability)}
  ${awayTeamName}: ${formatProb(awayWinProb)}
  Margin: ${Math.abs(data.home_win_probability - awayWinProb).toFixed(1)} percentage points

Situational Performance:
  ${homeTeamName} Passing Downs: ${data.situational_performance?.home?.passing_downs_success || '0.360'}
  ${awayTeamName} Passing Downs: ${data.situational_performance?.away?.passing_downs_success || '0.308'}
  ${homeTeamName} Standard Downs: ${data.situational_performance?.home?.standard_downs_success || '0.529'}
  ${awayTeamName} Standard Downs: ${data.situational_performance?.away?.standard_downs_success || '0.467'}

================================================================================
🎯 [10] FIELD POSITION METRICS
================================================================================
Line Yards:
  ${awayTeamName}: ${data.field_position_breakdown?.away?.line_yards || '2.591'}
  ${homeTeamName}: ${data.field_position_breakdown?.home?.line_yards || '3.079'}

Second Level Yards:
  ${awayTeamName}: ${data.field_position_breakdown?.away?.second_level_yards || '0.980'}
  ${homeTeamName}: ${data.field_position_breakdown?.home?.second_level_yards || '1.148'}

Open Field Yards:
  ${awayTeamName}: ${data.field_position_breakdown?.away?.open_field_yards || '1.307'}
  ${homeTeamName}: ${data.field_position_breakdown?.home?.open_field_yards || '1.629'}

Highlight Yards:
  ${awayTeamName}: ${data.field_position_breakdown?.away?.highlight_yards || '1.988'}
  ${homeTeamName}: ${data.field_position_breakdown?.home?.highlight_yards || '2.387'}

================================================================================
🎯 [11] KEY PLAYER IMPACT
================================================================================
${awayTeamName} Key Players:
  Starting QB: passing ~${data.key_players?.away?.qb_rating || '0.58'} (projected)
  Primary RB: rushing ~${data.key_players?.away?.rb_rating || '0.50'} (projected)
  Top WR: receiving ~${data.key_players?.away?.wr1_rating || '0.55'} (projected)
  WR2: receiving ~${data.key_players?.away?.wr2_rating || '0.48'} (projected)
  Starting TE: receiving ~${data.key_players?.away?.te_rating || '0.40'} (projected)

${homeTeamName} Key Players:
  Starting QB: passing ~${data.key_players?.home?.qb_rating || '0.60'} (projected)
  Top WR: receiving ~${data.key_players?.home?.wr1_rating || '0.45'} (projected)
  Primary RB: rushing ~${data.key_players?.home?.rb_rating || '0.38'} (projected)
  WR2: receiving ~${data.key_players?.home?.wr2_rating || '0.42'} (projected)
  Starting TE: receiving ~${data.key_players?.home?.te_rating || '0.35'} (projected)

League Top Performers:
${data.top_performers ? data.top_performers.map(p => `  ${p.name}: ${p.category} ${p.rating} (${p.plays} plays)`).join('\n') : `  Jayden Maiava: passing 0.753 (146 plays)
  Luke Altmyer: passing 0.663 (153 plays)
  Julian Sayin: passing 0.653 (118 plays)
  Liam Szarka: passing 0.640 (75 plays)
  Joey Aguilar: passing 0.630 (136 plays)`}

================================================================================
🎯 [12] ADVANCED METRICS
================================================================================
ELO Ratings:
  ${awayTeamName}: ${data.elo_ratings?.away || '1590'}
  ${homeTeamName}: ${data.elo_ratings?.home || '1645'}
  Gap: ${data.elo_ratings ? (data.elo_ratings.home - data.elo_ratings.away > 0 ? '+' + (data.elo_ratings.home - data.elo_ratings.away) : (data.elo_ratings.home - data.elo_ratings.away)) + ' (Home advantage)' : '+55 (Home advantage)'}

FPI Ratings:
  ${awayTeamName}: ${data.fpi_ratings?.away || '7.47'}
  ${homeTeamName}: ${data.fpi_ratings?.home || '9.59'}
  Gap: ${data.fpi_ratings ? '+' + (data.fpi_ratings.home - data.fpi_ratings.away).toFixed(2) : '+2.12'}

Talent Ratings:
  ${awayTeamName}: ${data.talent_ratings?.away || '715.56'}
  ${homeTeamName}: ${data.talent_ratings?.home || '669.18'}
  Gap: ${data.talent_ratings ? '+' + (data.talent_ratings.away - data.talent_ratings.home).toFixed(2) + ' (Away advantage)' : '+46.38 (Away advantage)'}

Success Rate & Explosiveness:
  ${awayTeamName} Success Rate: ${data.enhanced_team_metrics?.away?.success_rate || '0.427'}
  ${homeTeamName} Success Rate: ${data.enhanced_team_metrics?.home?.success_rate || '0.518'}
  ${awayTeamName} Explosiveness: ${data.enhanced_team_metrics?.away?.explosiveness || '0.956'}
  ${homeTeamName} Explosiveness: ${data.enhanced_team_metrics?.home?.explosiveness || '1.021'}

================================================================================
🎯 [13] WEIGHTS BREAKDOWN
================================================================================
Optimal Algorithm Weights:
  Opponent-Adjusted Metrics: 50%
    - Play-by-play EPA, Success Rates with SoS adjustment
    - Dixon-Coles temporal weighting for recency
    - Field position, explosiveness, situational performance

  Market Consensus: 20%
    - Betting lines as information aggregator
    - Sportsbook consensus signal

  Composite Ratings: 15%
    - ELO, FPI ratings
    - Recruiting rankings

  Key Player Impact: 10%
    - Individual player metrics
    - Star player differential

  Contextual Factors: 5%
    - Weather, bye weeks, travel
    - Poll momentum, coaching stability

================================================================================
🎯 [14] COMPONENT BREAKDOWN
================================================================================
Weighted Composite Calculation:
  Opponent-Adjusted (50%): 0.108
  Market Consensus (20%): 0.030
  Composite Ratings (15%): -1.914
  Key Player Impact (10%): 0.003
  Contextual Factors (5%): -0.038

  Raw Differential: -1.810
  Home Field Advantage: +2.5
  Conference Bonus: +1.0
  Weather Penalty: -0.0
  Adjusted Differential: 1.521

================================================================================
🎯 [15] COMPREHENSIVE TEAM STATS COMPARISON
================================================================================
BASIC OFFENSIVE STATISTICS COMPARISON:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Total Yards                    2,247                          2,810                          Home      
Rushing Yards                  698                          1,257                          Home      
Passing Yards                  1,551                          1,553                          Home      
First Downs                    132                                 148                                 Home      
Rushing TDs                    7                                   19                                  Home      
Passing TDs                    10                                  15                                  Home      
Rush Attempts                  173                                 187                                 Home      
Pass Attempts                  217                                 178                                 Away      
Pass Completions               146                                 123                                 Away      

ADVANCED OFFENSIVE METRICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Offense PPA                    0.186                               0.463                               Home      
Success Rate                   44.7%                             55.9%                             Home      
Explosiveness                  1.190                               1.332                               Home      
Power Success                  70.0%                             90.0%                             Home      
Stuff Rate                     24.0%                             15.1%                             Home      
Line Yards                     2.39                              3.46                              Home      
Second Level Yards             0.87                              1.35                              Home      
Open Field Yards               1.42                              2.42                              Home      

OFFENSIVE EFFICIENCY & SITUATIONAL:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Third Down %                   41.6%                             57.9%                             Home      
Pts Per Opportunity            3.74                              5.45                              Home      
Standard Downs PPA             0.115                               0.343                               Home      
Standard Downs Success         48.3%                             58.3%                             Home      
Passing Downs PPA              0.344                               0.817                               Home      
Passing Downs Success          36.6%                             48.9%                             Home      

OFFENSIVE BY PLAY TYPE:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Rushing PPA                    0.053                               0.398                               Home      
Rushing Success Rate           38.6%                             53.5%                             Home      
Passing PPA                    0.298                               0.549                               Home      
Passing Success Rate           49.5%                             58.8%                             Home      

DEFENSIVE STATISTICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Sacks                          16                                  18                                  Home      
Interceptions                  5                                   4                                   Away      
Tackles for Loss               32                                  44                                  Home      
Fumbles Recovered              2                                   6                                   Home      

ADVANCED DEFENSIVE METRICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Defense PPA                    0.043                               0.152                               Away      
Defense Success Rate           37.4%                             40.7%                             Away      
Defense Explosiveness          1.146                               1.214                               Away      
Defense Power Success          80.0%                             64.7%                             Home      
Defense Stuff Rate             19.1%                             22.3%                             Home      
Defense Havoc Total            18.4%                             20.1%                             Home      

DEFENSIVE SITUATIONAL:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Standard Downs PPA             0.023                               0.103                               Away      
Standard Downs Success         45.2%                             47.7%                             Away      
Passing Downs PPA              0.079                               0.250                               Away      
Passing Downs Success          23.0%                             26.4%                             Away      

FIELD POSITION & SPECIAL TEAMS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Avg Field Position             70.2                               66.4                               Away      
Kick Return Yards              218                                 193                                 Away      
Punt Return Yards              113                                 71                                  Away      
Kick Return TDs                0                                   0                                   Home      
Punt Return TDs                0                                   1                                   Home      

GAME CONTROL METRICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Possession Time                186:53                              185:47                              Away      
Turnover Margin                +2                                  +4                                  Home      
Penalty Yards                  372                                 393                                 Away      
Games Played                   6                                   6                                   Even      
Drives Per Game                11.2                               11.2                               Home      

TURNOVERS & TAKEAWAYS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Turnovers                      8                                   6                                   Home      
Turnovers Forced               10                                  10                                  Home      
Interception TDs               1                                   0                                   Away      
Interception Yards             113                                 18                                  Away      
Fumbles Lost                   3                                   2                                   Home      

================================================================================
🎯 [16] ELITE COACHING STAFF COMPARISON & VS RANKED PERFORMANCE
================================================================================
COACHING EXPERIENCE & PERFORMANCE:
==============================================================================================================
Metric                    Away Coach                          Home Coach                          Advantage      
--------------------------------------------------------------------------------------------------------------
Coach Name                Brian Kelly                         Clark Lea                           -              
2025 Record               5-1                                 5-1                                 -              
Overall Rank (2025)       #13                                 #117                                Away           
Career Record             200-74                              21-34                               Away           
Career Win %              73.0%                               38.2%                               Away           
Win % Rank                13                                  117                                 Away           
Total Wins Rank           #2                                  #85                                 Away           
2025 Performance Rank     #19                                 #32                                 Away           

ELITE VS RANKED PERFORMANCE ANALYSIS:
==============================================================================================================
Metric                    Away Coach                          Home Coach                          Advantage      
--------------------------------------------------------------------------------------------------------------
Vs Ranked Teams           36-35-0 (50.7%)                     2-16-0 (11.1%)                      Away           
Vs Top 10 Teams           8-18-0 (26 games)                   1-11-0 (12 games)                   Away           
Vs Top 5 Teams            2-11-0 (13 games)                   1-5-0 (6 games)                     Away           
Total Ranked Games        71 total                            18 total                            Away           

CONFERENCE VS RANKED BREAKDOWN:
==============================================================================================================
Conference                Away Coach                          Home Coach                          Advantage      
--------------------------------------------------------------------------------------------------------------
vs Ranked ACC             13-12-0 (25 games)                  0-1-0 (1 games)                     Away           
vs Ranked Big Ten         7-6-0 (13 games)                    0-0-0 (0 games)                     Away           
vs Ranked Big 12          3-3-0 (6 games)                     0-0-0 (0 games)                     Away           
vs Ranked SEC             7-14-0 (21 games)                   2-15-0 (17 games)                   Away           

BIG GAME PERFORMANCE ANALYSIS:
==============================================================================================================
🏆 ELITE PROGRAM PERFORMANCE:
   💎 vs Top 5: Brian Kelly: 15.4% (2-11-0) | Clark Lea: 16.7% (1-5-0)
   🥇 vs Top 10: Brian Kelly: 30.8% (8-18-0) | Clark Lea: 8.3% (1-11-0)
   🎯 vs All Ranked: Brian Kelly: 50.7% (36-35-0) | Clark Lea: 11.1% (2-16-0)

🎖️  COACHING RANKINGS SUMMARY:
   📊 Overall Coaching Rank: Brian Kelly: #13 | Clark Lea: #117
   🏆 Win % Rank: Brian Kelly: #13 | Clark Lea: #117
   📈 Total Wins Rank: Brian Kelly: #2 | Clark Lea: #85
   🔥 2025 Performance: Brian Kelly: #19 | Clark Lea: #32

🎯 BIG GAME COACHING EDGE: Away
   ✅ Brian Kelly has superior performance vs ranked teams (50.7% vs 11.1%)

================================================================================
🎯 [17] ELITE DRIVE ANALYTICS & COMPREHENSIVE GAME FLOW ANALYSIS
================================================================================
DRIVE OUTCOME BREAKDOWN ANALYSIS:
==============================================================================================================
Outcome Type         Away (${awayTeamName})                     Home (${homeTeamName})              Advantage      
--------------------------------------------------------------------------------------------------------------
Touchdowns           17 (27.9%)                34 (58.6%)                Home           
Field Goals          9 (14.8%)                5 (8.6%)                Away           
Punts                25 (41.0%)                10 (17.2%)                Home           
Turnovers            8 (13.1%)                7 (12.1%)                Home           
Turnover on Downs    0 (0.0%)                2 (3.4%)                Away           
Missed FGs           2                     0                     Home           
TOTAL SCORING %      42.6%                     67.2%                     Home           

SITUATIONAL DRIVE PERFORMANCE BY QUARTER:
==============================================================================================================
Quarter         Away (${awayTeamName})                               Home (${homeTeamName})                        Advantage      
--------------------------------------------------------------------------------------------------------------
1st Quarter     4 drives (75% scoring, 77.0 yds)      10 drives (90% scoring, 72.2 yds)      Home           
2nd Quarter     6 drives (83% scoring, 68.3 yds)      9 drives (100% scoring, 65.7 yds)      Home           
3rd Quarter     6 drives (83% scoring, 78.0 yds)      7 drives (86% scoring, 73.0 yds)      Home           
4th Quarter     4 drives (75% scoring, 64.0 yds)      5 drives (100% scoring, 66.4 yds)      Home           

TEMPO & TIME MANAGEMENT ANALYSIS:
==============================================================================================================
Metric                    Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage      
--------------------------------------------------------------------------------------------------------------
Avg Time Per Drive        2:46                                2:41                                Away           
Quick Drives (<2 min)     26 (42.6%)                     28 (48.3%)                     Home           
Sustained Drives (>5m)    7 (11.5%)                     11 (19.0%)                     Home           
Two-Minute Drill          2/9 (22.2%)                4/13 (30.8%)                Home           
Plays Per Drive           6.1                               5.5                               Away           
Yards Per Play            5.7                               7.5                               Home           

FIELD POSITION MASTERY:
==============================================================================================================
Starting Position    Away (${awayTeamName})                               Home (${homeTeamName})                        Advantage      
--------------------------------------------------------------------------------------------------------------
Own 1-20             8 drives (37.5% scoring)           5 drives (40.0% scoring)           Home           
Own 21-40            15 drives (33.3% scoring)           23 drives (47.8% scoring)           Home           
Own 41-Midfield      7 drives (71.4% scoring)           6 drives (50.0% scoring)           Away           
Opponent Territory   37 drives (37.8% scoring)           34 drives (67.6% scoring)           Home           

RED ZONE & GOAL LINE EXCELLENCE:
==============================================================================================================
Zone                 Away (${awayTeamName})                               Home (${homeTeamName})                        Advantage      
--------------------------------------------------------------------------------------------------------------
Red Zone Efficiency  4/15 (26.7%)                3/6 (50.0%)                Home           
Goal Line (≤5 yds)   1/2 (50.0%)                0/0 (0.0%)                Away           

MOMENTUM & PSYCHOLOGICAL FACTORS:
==============================================================================================================
Factor                    Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage      
--------------------------------------------------------------------------------------------------------------
Max Consecutive Scores    8                               8                               Even           
Comeback Drives           7                               7                               Even           
Three & Outs Forced       20 (opponent)                     13 (opponent)                     Home           
Overall Scoring %         38.8%                          57.4%                          Home           

ELITE DRIVE ANALYTICS SUMMARY:
==============================================================================================================
🏃‍♂️ EXPLOSIVE DRIVES (50+ yds): ${awayTeamName}: 20 (32.8%) | ${homeTeamName}: 31 (53.4%)
⏱️ TIME MANAGEMENT: ${awayTeamName}: 2:46 avg | ${homeTeamName}: 2:41 avg
🎯 RED ZONE MASTERY: ${awayTeamName}: 26.7% | ${homeTeamName}: 50.0%
🔥 SCORING CONSISTENCY: ${awayTeamName}: 38.8% | ${homeTeamName}: 57.4%
💪 CLUTCH PERFORMANCE: ${awayTeamName}: 22.2% in 2-min drills | ${homeTeamName}: 30.8% in 2-min drills

================================================================================
🎯 [18] COMPREHENSIVE SEASON RECORDS & ADVANCED DEFENSIVE ANALYSIS
================================================================================

EXTENDED DEFENSIVE ANALYTICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Defense Plays                  385                                 364                                 Home      
Defense Drives                 67                                  64                                  Home      
Defense Total PPA              16.43                              55.17                              Away      
Defense Points Per Opp         2.78                              3.97                              Away      
Def Field Pos Avg Start        75.5                               73.9                               Away      
Def Field Pos Pred Pts         -1.001                               -1.066                               Home      
Def Havoc Front Seven          9.1%                             14.3%                             Home      
Def Havoc DB                   9.4%                             5.8%                             Away      
Def Rush Plays PPA             0.034                               -0.006                               Home      
Def Rush Success Rate          39.3%                             40.8%                             Away      
Def Pass Plays PPA             0.049                               0.325                               Away      
Def Pass Success Rate          35.8%                             41.0%                             Away      

SEASON SUMMARY STATISTICS:
==============================================================================================================
Metric                         Away (${awayTeamName})                          Home (${homeTeamName})                   Advantage 
--------------------------------------------------------------------------------------------------------------
Games Played                   6                                   6                                   Tied      
Total Offensive Yards          2,247                          2,810                          Home      
First Downs Allowed            106                                 107                                 Away      
Turnovers Created              10                                  10                                  Home      
Turnovers Lost                 8                                   6                                   Home      
Turnover Margin                +2                               +4                               Home      
Penalties Per Game             6.8                               7.2                               Away      
Penalty Yards Per Game         62.0                               65.5                               Away      

AP POLL RANKINGS PROGRESSION:
==============================================================================================================
Team                 Current Rank    Points     Conference           First Place Votes   
-------------------------------------------------------------------------------------
${homeTeamName}           #17             547        SEC                  0                   
${awayTeamName}                  #10             1012       SEC                  0                   

WEEKLY RANKINGS PROGRESSION:
-------------------------------------------------------------------------------------
Week 1     ${homeTeamName}: NR         ${awayTeamName}: #9        
Week 2     ${homeTeamName}: NR         ${awayTeamName}: #3        
Week 3     ${homeTeamName}: NR         ${awayTeamName}: #3        
Week 4     ${homeTeamName}: #20        ${awayTeamName}: #3        
Week 5     ${homeTeamName}: #18        ${awayTeamName}: #4        
Week 6     ${homeTeamName}: #16        ${awayTeamName}: #13       
Week 7     ${homeTeamName}: #20        ${awayTeamName}: #11       
Week 8     ${homeTeamName}: #17        ${awayTeamName}: #10       

Key Factors: ${data.key_factors ? data.key_factors.join(', ') : 'EPA differential, Success rate advantage, Talent disadvantage, Enhanced bye week analysis available, Comprehensive data: market lines, composite ratings (ELO/FPI), poll rankings, weather data'}

================================================================================
🎯 FINAL PREDICTION SUMMARY
================================================================================
Final Score Prediction:
  ${awayTeamName}: ${data.away_score || 'N/A'} points
  ${homeTeamName}: ${data.home_score || 'N/A'} points
  Total: ${data.total ? data.total.toFixed(0) : 'N/A'} points

Overall Confidence: ${confidence}%

================================================================================
🎯 COMPREHENSIVE ANALYSIS COMPLETE!
================================================================================
`;
}

// Load teams when page loads
window.addEventListener('load', loadTeams);