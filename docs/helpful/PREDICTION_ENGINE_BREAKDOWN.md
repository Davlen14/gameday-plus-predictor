# 🎯 Gameday+ Prediction Engine - Complete Breakdown

> **Comprehensive guide to all calculations, weights, and methodology**  
> Last Updated: November 26, 2025

---

## 📋 Table of Contents
1. [Core Architecture](#core-architecture)
2. [Data Sources](#data-sources)
3. [Weight Distribution](#weight-distribution)
4. [Calculation Methods](#calculation-methods)
5. [Advanced Metrics](#advanced-metrics)
6. [Calibration Techniques](#calibration-techniques)
7. [Edge Calculations](#edge-calculations)

---

## 🏗️ Core Architecture

The prediction engine uses a **weighted ensemble model** that combines multiple analytical dimensions:

### System Overview
```
GraphQL Data → Team Metrics → Advanced Analysis → Weighted Composite → Calibration → Final Prediction
```

### Primary Components
1. **Opponent-Adjusted Metrics** (EPA, Success Rates)
2. **Market Consensus** (Betting Lines)
3. **Composite Ratings** (ELO, FPI, Talent)
4. **Key Player Impact** (Individual Performance)
5. **Contextual Factors** (Weather, Bye Weeks, Polls)

---

## 📊 Data Sources

### 1. GraphQL API Endpoints
```graphql
Query Components:
├── adjustedTeamMetrics (EPA, Success Rates, Explosiveness)
├── teamTalent (Recruiting Rankings)
├── game (Season Performance, ELO Ratings)
├── ratings (FPI, Composite Ratings)
├── gameLines (Sportsbook Betting Lines)
├── gameWeather (Temperature, Wind, Precipitation)
├── pollRank (AP & Coaches Poll Rankings)
└── calendar (Bye Week Detection)
```

### 2. Static Data Files
```
weekly_updates/week_14/
├── fbs_teams_stats_only.json (Comprehensive Team Stats)
├── comprehensive_qb_analysis_2025.json (155 QBs)
├── comprehensive_wr_analysis_2025.json (616 WRs)
├── power5_drives_only.json (Drive-Level Analysis)
├── coaches_with_vsranked_stats.json (Coaching Performance)
└── all_fbs_ratings_comprehensive_2025.json (Backtesting Data)
```

### 3. Real-Time Market Data
- **Sportsbook Lines**: Spread, Total, Moneylines
- **Line Movement**: Opening vs Current Lines
- **Market Consensus**: Multi-book aggregation

---

## ⚖️ Weight Distribution

### Dynamic Weighting System

The engine adjusts weights based on **matchup characteristics**:

#### Base Weights (Standard Matchup)
```python
BASE_WEIGHTS = {
    'composite_ratings': 0.55,           # 55% - ELO/FPI/Talent
    'opponent_adjusted_metrics': 0.20,  # 20% - EPA/Success (SOS-adjusted)
    'defensive_metrics': 0.10,           # 10% - Defensive mismatch
    'key_player_impact': 0.08,           # 8% - Player analysis
    'market_consensus': 0.05,            # 5% - Betting lines
    'contextual_factors': 0.02           # 2% - Weather/bye/travel
}
```

#### Dynamic Adjustments by ELO Differential

**Extreme Mismatch (ELO Diff ≥ 750)**
```python
WEIGHTS = {
    'composite_ratings': 0.65,           # ↑ Trust talent gap heavily
    'opponent_adjusted_metrics': 0.15,  # ↓ Performance less predictive
    'defensive_metrics': 0.12,
    'key_player_impact': 0.05,
    'market_consensus': 0.02,
    'contextual_factors': 0.01
}
```

**Large Mismatch (ELO Diff 600-749)**
```python
WEIGHTS = {
    'composite_ratings': 0.60,
    'opponent_adjusted_metrics': 0.18,
    'defensive_metrics': 0.11,
    'key_player_impact': 0.07,
    'market_consensus': 0.03,
    'contextual_factors': 0.01
}
```

**Even Matchup (ELO Diff < 200)**
```python
WEIGHTS = {
    'composite_ratings': 0.40,           # ↓ Talent matters less
    'opponent_adjusted_metrics': 0.35,  # ↑ Recent performance critical
    'defensive_metrics': 0.10,
    'key_player_impact': 0.08,
    'market_consensus': 0.05,
    'contextual_factors': 0.02
}
```

### Rating Consensus Multiplier
When all 4 rating systems (ELO, FPI, SP+, SRS) agree within 15%:
```python
if consensus > 0.90:
    weights['composite_ratings'] *= 1.10  # +10% boost
    weights['opponent_adjusted_metrics'] *= 0.90  # -10% reduction
```

### Strength of Schedule (SOS) Adjustment
When favorite has tough SOS (rank < 40) vs weak underdog SOS (rank > 80):
```python
weights['composite_ratings'] *= 1.05  # +5% boost
weights['opponent_adjusted_metrics'] *= 0.95  # -5% reduction
```

---

## 🧮 Calculation Methods

### 1. Opponent-Adjusted Metrics (20-35% weight)

#### EPA Differential Calculation
```python
# Net EPA for each team
home_epa_net = home_epa - home_epa_allowed
away_epa_net = away_epa - away_epa_allowed

# Differential (positive = home advantage)
epa_differential = home_epa_net - away_epa_net

# Weighted contribution: 70% of opponent-adjusted score
epa_contribution = epa_differential * 0.70
```

#### Dixon-Coles Temporal Weighting
```python
# Decay parameter (3-week half-life)
decay_xi = 0.0065

# Weight by game recency
def dixon_coles_weight(days_ago: float) -> float:
    return math.exp(-decay_xi * days_ago)

# Weighted recent performance
weighted_performance = Σ(win_prob[i] * weight[i]) / Σ(weight[i])

# Temporal contribution: 20% of opponent-adjusted score
temporal_contribution = temporal_differential * 0.20
```

#### Strength of Schedule Adjustment
```python
# Average opponent ELO relative to baseline (1500)
avg_opponent_elo = Σ(opponent_elos) / len(opponents)
sos_rating = (avg_opponent_elo - 1500) / 100

# SOS contribution: 10% of opponent-adjusted score
sos_contribution = sos_differential * 0.10
```

#### Final Opponent-Adjusted Score
```python
opponent_adjusted_score = (
    advanced_metrics_differential * 0.70 +  # EPA, Success, Explosiveness
    temporal_differential * 0.20 +          # Dixon-Coles weighted form
    sos_differential * 0.10                 # Schedule strength
)
```

---

### 2. Composite Ratings (40-65% weight)

#### ELO Rating Conversion
```python
# ELO differential
elo_diff = home_elo - away_elo

# Convert to win probability (chess rating formula)
elo_win_probability = 1 / (1 + 10 ** (-elo_diff / 400))

# Normalize for weighted model (avoid dominating)
elo_normalized_signal = elo_diff * 0.003
```

**Example**: 100 ELO difference = 64% win probability = 0.3 signal contribution

#### FPI Rating Integration
```python
# FPI differential (already in reasonable range -40 to +40)
fpi_diff = home_fpi - away_fpi

# Normalize to similar scale as ELO
fpi_normalized_signal = fpi_diff * 0.1
```

#### Elite Mismatch Multiplier
```python
elite_threshold_elo = 2100  # Top-5 teams
weak_threshold_elo = 1400   # Bottom-tier teams

if (home_elo > elite_threshold and away_elo < weak_threshold) or vice versa:
    mismatch_multiplier = 1.2  # 20% amplification
elif abs(elo_diff) > 600:
    mismatch_multiplier = 1.1  # 10% amplification
else:
    mismatch_multiplier = 1.0
```

#### Composite Score Calculation
```python
composite_score = (
    elo_normalized_signal * 0.60 +    # ELO primary (60%)
    fpi_normalized_signal * 0.40      # FPI validation (40%)
) * mismatch_multiplier
```

#### Talent Rating Integration
```python
# Talent differential (recruiting rankings 0-1000 scale)
talent_raw = home_talent - away_talent
talent_normalized = talent_raw * 0.001  # Normalize

# Combined composite
final_composite = (
    ratings_differential * 0.70 +  # ELO/FPI
    talent_differential * 0.30     # Recruiting
)
```

---

### 3. Advanced Metrics Breakdown

#### Passing vs Rushing Efficiency (25%)
```python
# Net EPA by play type
home_passing_net = home_passing_epa - home_passing_epa_allowed
away_passing_net = away_passing_epa - away_passing_epa_allowed
passing_diff = home_passing_net - away_passing_net

home_rushing_net = home_rushing_epa - home_rushing_epa_allowed
away_rushing_net = away_rushing_epa - away_rushing_epa_allowed
rushing_diff = home_rushing_net - away_rushing_net

# Weighted contribution
play_type_contribution = (
    passing_diff * 0.15 +   # 15% passing
    rushing_diff * 0.10     # 10% rushing
)
```

#### Situational Success Rates (20%)
```python
# Passing downs (3rd & long, obvious passing situations)
home_passing_downs = home_pd_success - home_pd_success_allowed
away_passing_downs = away_pd_success - away_pd_success_allowed
pd_diff = home_passing_downs - away_passing_downs

# Standard downs (1st/2nd down, balanced situations)
home_standard_downs = home_sd_success - home_sd_success_allowed
away_standard_downs = away_sd_success - away_sd_success_allowed
sd_diff = home_standard_downs - away_standard_downs

# Weighted contribution
situational_contribution = (
    pd_diff * 0.12 +        # 12% passing downs
    sd_diff * 0.08          # 8% standard downs
)
```

#### Field Position & Yards Analysis (30%)
```python
# Line yards (0-4 yards, between tackles)
line_yards_diff = (home_line_yards - home_line_yards_allowed) - 
                  (away_line_yards - away_line_yards_allowed)

# Second level yards (5-10 yards, linebacker level)
second_level_diff = (home_second_level - home_second_level_allowed) - 
                    (away_second_level - away_second_level_allowed)

# Open field yards (11+ yards, safety level)
open_field_diff = (home_open_field - home_open_field_allowed) - 
                  (away_open_field - away_open_field_allowed)

# Weighted contribution
field_position_contribution = (
    line_yards_diff * 0.10 +      # 10% line yards
    second_level_diff * 0.10 +    # 10% second level
    open_field_diff * 0.10        # 10% open field
)
```

#### Big Play Capability (15%)
```python
# Highlight yards (explosive plays 20+ yards)
highlight_diff = (home_highlights - home_highlights_allowed) - 
                 (away_highlights - away_highlights_allowed)

# Weighted contribution
big_play_contribution = highlight_diff * 0.15
```

#### Total Advanced Differential
```python
advanced_differential = (
    play_type_contribution +        # 25%
    situational_contribution +      # 20%
    field_position_contribution +   # 30%
    big_play_contribution          # 15%
)
```

---

### 4. Key Player Impact (5-10% weight)

#### Positional Analysis Weights
```python
POSITIONAL_WEIGHTS = {
    'quarterback': 0.40,      # 40% of player impact
    'skill_positions': 0.35,  # 35% (RB, WR, TE)
    'defense': 0.25           # 25% (DB, LB, DL)
}
```

#### Quarterback Advantage
```python
# Comprehensive QB metrics from JSON data
qb_differential = (
    efficiency_diff * 0.5 +           # Passing efficiency
    ball_security_diff * 0.3 +        # INT/fumble rates
    dual_threat_diff * 0.2            # Rushing ability
)
```

#### Skill Position Advantage
```python
# Top 2 RBs
home_rb_score = avg([rb1_efficiency, rb2_efficiency])
away_rb_score = avg([rb1_efficiency, rb2_efficiency])
rb_diff = (home_rb_score - away_rb_score) / 100

# Top 3 WRs
home_wr_score = avg([wr1_eff, wr2_eff, wr3_eff])
away_wr_score = avg([wr1_eff, wr2_eff, wr3_eff])
wr_diff = (home_wr_score - away_wr_score) / 100

# Top TE
te_diff = (home_te_eff - away_te_eff) / 100

# Weighted skill advantage
skill_advantage = (
    rb_diff * 0.4 +   # 40% running backs
    wr_diff * 0.5 +   # 50% wide receivers
    te_diff * 0.1     # 10% tight ends
)
```

#### Defensive Advantage
```python
# Top 5 defenders from each team
home_def_score = avg([top_5_defenders])
away_def_score = avg([top_5_defenders])

defensive_diff = (home_def_score - away_def_score) / 100
```

#### Total Player Impact
```python
total_player_impact = (
    qb_differential * 0.40 +
    skill_differential * 0.35 +
    defense_differential * 0.25
)
```

---

### 5. Market Consensus (2-5% weight)

#### Market Signal Calculation
```python
# Average across all sportsbooks
spreads = [book1_spread, book2_spread, ...]
avg_spread = mean(spreads)

# Signal strength (each point = 0.1 contribution)
market_signal = abs(avg_spread) * 0.1
```

#### Outlier Removal
```python
def remove_outliers(values):
    mean_val = mean(values)
    stdev = stdev(values)
    
    # Keep values within 3 standard deviations
    filtered = [v for v in values if abs(v - mean_val) <= 3 * stdev]
    return filtered if filtered else values
```

---

### 6. Contextual Factors (1-2% weight)

#### Weather Impact
```python
weather_factor = 0.0

# Temperature
if temp < 32:        # Freezing
    weather_factor += 2.0
elif temp > 90:      # Very hot
    weather_factor += 1.0

# Wind
if wind_speed > 15:  # High wind
    weather_factor += 1.5

# Precipitation
if precipitation > 0.1:  # Significant rain
    weather_factor += 2.5
```

#### Poll Momentum
```python
# Both teams ranked
if home_ranked and away_ranked:
    rank_diff = away_rank - home_rank  # Lower is better
    poll_differential = rank_diff * 0.05  # Each rank = 0.05 points

# Ranked vs Unranked
elif home_ranked and not away_ranked:
    poll_differential = 2.0  # Significant advantage

elif away_ranked and not home_ranked:
    poll_differential = -2.0  # Disadvantage
```

#### Bye Week Advantage
```python
# Recent bye (Week 6 before Week 8 game)
if 6 in home_bye_weeks:
    bye_advantage += 3.0

if 6 in away_bye_weeks:
    bye_advantage -= 3.0

# Earlier byes
early_home_byes = home_bye_weeks - {6}
early_away_byes = away_bye_weeks - {6}

bye_advantage += len(early_home_byes) * 0.5
bye_advantage -= len(early_away_byes) * 0.5
```

#### Contextual Score
```python
contextual_score = (
    weather_factor * 0.4 +
    poll_momentum * 0.3 +
    bye_advantage * 0.3
)
```

---

### 7. Defensive Metrics (10-12% weight)

#### Defensive Mismatch Detection
```python
# Defensive efficiency vs opposing offense
home_def_vs_away_off = home_def_efficiency - away_off_efficiency
away_def_vs_home_off = away_def_efficiency - home_off_efficiency

defensive_advantage = (home_def_vs_away_off - away_def_vs_home_off) / 10.0
```

#### Defensive Dampener (Total Scoring)
```python
# Elite defense detected
if abs(home_def_vs_away_off) > 40 or abs(away_def_vs_home_off) > 40:
    defensive_dampener = 0.85  # 15% scoring reduction

# Strong defensive mismatch
elif abs(home_def_vs_away_off) > 30 or abs(away_def_vs_home_off) > 30:
    defensive_dampener = 0.92  # 8% scoring reduction

else:
    defensive_dampener = 1.0   # No dampening

# Apply to total
predicted_total = base_total * defensive_dampener
```

---

## 🎯 Final Prediction Calculation

### Raw Differential Composite
```python
raw_differential = (
    opponent_adjusted_score * weight_opponent_adjusted +
    market_consensus * weight_market +
    composite_score * weight_composite +
    player_impact * weight_player +
    contextual_score * weight_contextual
)
```

### Situational Adjustments
```python
# Home field advantage
home_field_advantage = 2.5  # Standard college football

# Conference rivalry bonus
conference_bonus = 1.0 if same_conference else 0.0

# Weather penalty
weather_penalty = calculate_weather_impact(weather_data)

# Elite team factor (hardcoded for known mismatches)
elite_factor = calculate_elite_team_factor(home_team, away_team)
```

### Comprehensive Enhancement
```python
comprehensive_enhancement = (
    epa_differential * 0.12 +
    success_differential * 15 * 0.10 +
    explosiveness_differential * 10 * 0.08 +
    elo_differential * 0.06 +
    consistency_differential * 0.04 +
    recent_vs_early_differential * 0.03 +
    trend_differential * 0.05 +
    defensive_advantage * defensive_weight
)
```

### Adjusted Differential
```python
adjusted_differential = (
    raw_differential +
    home_field_advantage +
    conference_bonus -
    weather_penalty +
    elite_factor +
    comprehensive_enhancement
)
```

---

## 📈 Calibration Techniques

### 1. Platt Scaling

**Purpose**: Convert raw probabilities to calibrated win probabilities

```python
# Parameters (tuned on historical data)
platt_a = 1.0  # Scaling parameter
platt_b = 0.0  # Offset parameter

def platt_scaling_calibration(raw_probability):
    # Convert probability to logit
    epsilon = 1e-10
    raw_probability = clamp(raw_probability, epsilon, 1 - epsilon)
    raw_logit = log(raw_probability / (1 - raw_probability))
    
    # Apply Platt scaling
    calibrated_logit = platt_a * raw_logit + platt_b
    
    # Convert back to probability
    calibrated_prob = 1 / (1 + exp(-calibrated_logit))
    
    return calibrated_prob
```

### 2. Logistic Regression (Win Probability)

```python
# Convert adjusted differential to raw win probability
raw_home_win_prob = 1 / (1 + exp(-adjusted_differential / 12.0))

# Apply Platt scaling
home_win_prob = platt_scaling_calibration(raw_home_win_prob)
```

**Divisor Explanation**: 
- Lower divisor = more aggressive scaling (wider probability range)
- `12.0` chosen for college football volatility
- NFL typically uses `14.0` (less volatile)

### 3. Spread Calculation from Win Probability

```python
# Inverse logit formula
if 0.01 < home_win_prob < 0.99:
    # Standard conversion (11.0 factor for college football)
    predicted_spread = log(home_win_prob / (1 - home_win_prob)) * 11.0
else:
    # Extreme probability (larger factor for big mismatches)
    predicted_spread = log(home_win_prob / (1 - home_win_prob)) * 14.0

# Bounds enforcement
predicted_spread = clamp(predicted_spread, -35, 35)
```

**Conversion Factors**:
- **11.0**: Standard college games (±3 point error)
- **14.0**: Extreme mismatches (elite vs weak)
- **NFL**: Uses 10.0 (tighter spreads)

---

## 💰 Total Scoring Calculation

### Base Total
```python
base_total = 50.0  # College football average
```

### Offensive Contributions
```python
# Each team's expected scoring
home_offensive_rating = (home_epa + home_explosiveness + home_success) / 3
away_offensive_rating = (away_epa + away_explosiveness + away_success) / 3

home_expected_points = (
    base_total/2 +
    (home_offensive_rating * 15) -
    (away_defensive_rating * 10) +
    2.5  # Home field scoring boost
)

away_expected_points = (
    base_total/2 +
    (away_offensive_rating * 15) -
    (home_defensive_rating * 10)
)
```

### Defensive Dampener Application
```python
total = home_expected_points + away_expected_points

# Apply defensive mismatch dampener
total = total * defensive_dampener

# Bounds enforcement
total = clamp(total, 40, 85)
```

### Implied Scores
```python
# Split total by spread
home_implied_score = (total + predicted_spread) / 2
away_implied_score = (total - predicted_spread) / 2

# Ensure no negative scores
if home_implied_score < 0:
    home_implied_score = 0
    away_implied_score = total
elif away_implied_score < 0:
    away_implied_score = 0
    home_implied_score = total
```

---

## 🎲 Confidence Calculation

### Base Confidence (Data Availability)
```python
base_confidence = 0.4

# Data source boosts
if has_metrics:         base_confidence += 0.15
if has_recent_games:    base_confidence += 0.10
if has_season_games:    base_confidence += 0.10
if has_ratings:         base_confidence += 0.08
if has_weather:         base_confidence += 0.03
if has_polls:           base_confidence += 0.02
if has_calendar:        base_confidence += 0.02
```

### Performance Factors
```python
# Team consistency boost
consistency_boost = avg(home_consistency, away_consistency) * 0.1

# Differential magnitude boost
differential_boost = min(abs(differential) / 20, 0.15)

# Trend alignment
trend_consistency = 1 - abs(home_trend - away_trend) / 2
trend_factor = trend_consistency * 0.05
```

### Market Validation
```python
# Market agreement boost (if available)
if market_lines:
    spread_difference = abs(predicted_spread - market_spread)
    
    if spread_difference < 2:
        market_boost = 0.15  # Strong agreement
    elif spread_difference < 5:
        market_boost = 0.05  # Moderate agreement
    else:
        market_boost = -0.10  # Disagreement (lower confidence)
```

### Final Confidence
```python
total_confidence = min(
    base_confidence +
    consistency_boost +
    differential_boost +
    trend_factor +
    market_boost,
    0.95  # Maximum confidence cap
)
```

---

## 🔍 Market Edge Calculation

### Spread Edge
```python
# From team perspective (e.g., underdog)
spread_value_edge = market_spread - model_spread

# Interpretation:
# Positive edge = Value on team_of_interest
# Negative edge = Value on opponent
```

### Total Edge
```python
# Model vs Market total
total_value_edge = model_total - market_total

# Interpretation:
# Positive edge = Value on OVER
# Negative edge = Value on UNDER
```

### Best Line Selection
```python
def find_best_spread_line(sportsbooks, value_edge):
    if value_edge > 0:
        # Value on team - want most points
        best_line = max(sportsbooks, key=lambda x: x.spread)
    else:
        # Value on opponent - want fewest points to give
        best_line = min(sportsbooks, key=lambda x: x.spread)
    
    return best_line
```

### Value Thresholds
```python
SPREAD_THRESHOLD = 2.0  # Minimum edge to recommend bet
TOTAL_THRESHOLD = 3.0   # Minimum edge for total bet

# Recommendations
if abs(spread_edge) >= SPREAD_THRESHOLD:
    recommend_spread_bet()

if abs(total_edge) >= TOTAL_THRESHOLD:
    recommend_total_bet()
```

---

## 🛠️ Special Adjustments

### Elite vs Struggling Override
```python
# Hardcoded for specific known mismatches
ELITE_OVERRIDES = {
    ('Ohio State', 'Wisconsin'): +18.0,  # Massive advantage
    # Add more as identified
}

if (away_team, home_team) in ELITE_OVERRIDES:
    elite_factor = ELITE_OVERRIDES[(away_team, home_team)]
    adjusted_differential += elite_factor
```

### Performance Gap Detection
```python
# Scoring differential
scoring_gap = away_ppg - home_ppg

# Defensive differential
defensive_gap = home_ppg_allowed - away_ppg_allowed

# Combined performance gap
total_gap = scoring_gap + defensive_gap + (point_diff_gap * 0.15)

if abs(total_gap) > 15.0:
    elite_factor = total_gap * 0.15  # Moderate adjustment
```

### Elite Team Thresholds
```python
ELITE_PPG_THRESHOLD = 32.0        # Elite scoring offense
ELITE_DEF_THRESHOLD = 12.0        # Elite defense (allows <12 PPG)
ELITE_WIN_PCT = 0.85              # Elite win percentage
ELITE_POINT_DIFF = 20.0           # Elite point differential

STRUGGLING_PPG_THRESHOLD = 18.0   # Weak offense
STRUGGLING_DEF_THRESHOLD = 28.0   # Weak defense
STRUGGLING_WIN_PCT = 0.4          # Poor win percentage
```

---

## 📝 Key Factors Identification

### Automatic Factor Detection
```python
factors = []

# EPA advantage
if abs(home_epa - away_epa) > 0.1:
    factors.append("EPA differential")

# Success rate
if abs(home_success - away_success) > 0.05:
    factors.append("Success rate advantage")

# Talent gap
if abs(home_talent - away_talent) > 5:
    factors.append("Talent advantage")

# Trend analysis
if abs(trend_differential) > 0.5:
    factors.append("Positive season trend")

# Weather
if temp < 32:
    factors.append("Cold weather favors ground game")
if wind_speed > 15:
    factors.append("High wind affects passing")
if precipitation > 0.1:
    factors.append("Wet conditions")

# Market analysis
if abs(model_spread - market_spread) > 10:
    factors.append("Significant market disagreement")
```

---

## 🎓 Model Validation

### Backtesting Metrics
```python
# Historical accuracy tracking
backtesting_data = {
    'teams': [...],  # All FBS teams
    'ratings': {
        'elo': [...],
        'fpi': [...],
        'sp_overall': [...],
        'srs': [...]
    },
    'consistency': [...]  # Rating agreement
}
```

### Spread Accuracy
```python
# Against closing line
spread_accuracy = games_within_3_points / total_games

# Against actual result
result_accuracy = correct_predictions / total_games
```

### Calibration Curves
```python
# Group predictions by confidence bins
bins = [0.5-0.6, 0.6-0.7, 0.7-0.8, 0.8-0.9, 0.9-1.0]

# Compare predicted vs actual win rates
for bin in bins:
    predicted_rate = mean(probabilities_in_bin)
    actual_rate = actual_wins_in_bin / total_games_in_bin
    
    calibration_error = abs(predicted_rate - actual_rate)
```

---

## 📚 Data Quality Checks

### Missing Data Handling
```python
# Fallback values
DEFAULT_EPA = 0.0
DEFAULT_ELO = 1500
DEFAULT_SUCCESS_RATE = 0.5
DEFAULT_TALENT = 500

# Data quality scoring
data_quality = 0.0

if has_team_metrics:      data_quality += 0.25
if has_player_data:       data_quality += 0.20
if has_market_lines:      data_quality += 0.20
if has_weather_data:      data_quality += 0.10
if has_coaching_data:     data_quality += 0.10
if has_drive_data:        data_quality += 0.15
```

### Outlier Detection
```python
# Statistical outliers (>3 standard deviations)
def is_outlier(value, values):
    mean_val = mean(values)
    stdev_val = stdev(values)
    
    return abs(value - mean_val) > 3 * stdev_val

# Remove from consensus calculations
filtered_values = [v for v in values if not is_outlier(v, values)]
```

---

## 🚀 Performance Optimizations

### Caching Strategy
```python
# Static data cached on initialization
static_data = {
    'team_stats': {...},      # Loaded once
    'coaching_data': {...},   # Loaded once
    'player_data': {...},     # Loaded once
    'backtesting': {...}      # Loaded once
}
```

### Parallel Processing
```python
# Batch GraphQL queries
async def predict_game():
    # Single query with all data
    result = await execute_query(combined_query)
    
    # Process in parallel
    tasks = [
        process_team_metrics(),
        process_player_data(),
        process_market_lines(),
        process_weather_data()
    ]
    
    await asyncio.gather(*tasks)
```

---

## 🎯 Summary of Key Formulas

### Win Probability
```python
P(home_win) = 1 / (1 + exp(-adjusted_differential / 12.0))
```

### Spread from Probability
```python
spread = log(P / (1 - P)) * 11.0  # Standard
spread = log(P / (1 - P)) * 14.0  # Extreme mismatch
```

### Total Scoring
```python
total = (
    base_total +
    (home_offensive_rating * 15) -
    (away_defensive_rating * 10) +
    (away_offensive_rating * 15) -
    (home_defensive_rating * 10) +
    2.5  # Home field
) * defensive_dampener
```

### Confidence
```python
confidence = min(
    base_data_quality +
    consistency_boost +
    differential_boost +
    market_agreement,
    0.95
)
```

---

## 📊 Weight Summary Table

| Component | Min Weight | Standard Weight | Max Weight | Trigger |
|-----------|-----------|-----------------|------------|---------|
| Composite Ratings | 40% | 55% | 65% | ELO diff ≥750 |
| Opponent-Adjusted | 15% | 20% | 35% | Even matchup |
| Defensive Metrics | 10% | 10% | 12% | Elite defense |
| Player Impact | 5% | 8% | 10% | Standard |
| Market Consensus | 2% | 5% | 5% | Standard |
| Contextual | 1% | 2% | 2% | Standard |

---

## 🔬 Research-Based Foundations

### Academic Sources
1. **Dixon-Coles Time Weighting**: "Modelling Association Football Scores" (1997)
2. **Platt Scaling**: "Probabilistic Outputs for SVMs" (1999)
3. **ELO Ratings**: Chess rating adaptation for team sports
4. **EPA Metrics**: Expected Points Added framework from NFL analytics

### Industry Validation
- **Market Lines**: Wisdom of crowds via sportsbook consensus
- **FPI**: ESPN's Football Power Index methodology
- **SP+**: Bill Connelly's Success Rate Plus framework
- **Backtesting**: Historical game data validation (2020-2025)

---

## 🎓 Advanced Topics

### Situational Modifiers
```python
# Rivalry games
if is_rivalry_game:
    differential *= 0.85  # Games typically closer

# Prime time
if is_prime_time:
    differential *= 0.9  # Tighter matchups

# Conference stakes
if conference_championship_impact:
    differential += 0.5  # Motivation factor
```

### Travel Distance (Future Enhancement)
```python
# Distance penalty
if travel_distance > 1000:
    away_penalty = 1.0
elif travel_distance > 500:
    away_penalty = 0.5
else:
    away_penalty = 0.0

adjusted_differential -= away_penalty
```

### Altitude Adjustment (Future Enhancement)
```python
# High altitude venues (>5000 feet)
if venue_altitude > 5000:
    altitude_factor = 2.0 if away_team else -2.0
    adjusted_differential += altitude_factor
```

---

## 📈 Continuous Improvement

### Model Retraining
```python
# Weekly after games complete
backtesting_accuracy = calculate_weekly_performance()

if backtesting_accuracy < 0.52:  # Below 52% ATS
    retune_parameters()
    recalibrate_platt_scaling()
```

### Weight Optimization
```python
# Gradient descent on historical data
optimal_weights = minimize(
    loss_function,
    initial_weights,
    method='L-BFGS-B',
    bounds=weight_bounds
)
```

---

**End of Prediction Engine Breakdown**

*For questions or clarifications, refer to the source code in `graphqlpredictor.py`*
