# College Football Data GraphQL Schema Documentation

## **🚨 CRITICAL QUICK REFERENCE**

**Key Relationship Patterns:**
- `adjustedTeamMetrics`: Direct field → `teamId: {_eq: Int}`, `year: {_eq: smallint}`
- `currentTeams`: Direct field → `teamId: {_eq: Int}`  
- `teamTalent`: Relationship field → `team: {teamId: {_eq: Int}}`, `year: {_eq: smallint}`
- `game`: Direct fields → `homeTeamId: {_eq: Int}`, `awayTeamId: {_eq: Int}`, `season: {_eq: smallint}`

**Variable Types:**
- Team IDs: `Int`
- Years/Weeks: `smallint`
- Use `year` for adjustedTeamMetrics/teamTalent, use `season` for game table

**Field Name Corrections:**
- ELO: `homeStartElo` / `awayStartElo` (not `homeElo`)
- Win Prob: `homePostgameWinProb` / `awayPostgameWinProb` (not `homePostgameWinProbability`)

---

## **Overview**
This document provides the complete schema structure for the College Football Data GraphQL API based on introspection analysis. Use this as reference to avoid field name issues and understand data relationships.

## **Key Query Tables**

### **1. adjustedTeamMetrics**
**Description:** Advanced team performance metrics (EPA, success rates, etc.)

**Available Fields:**
```graphql
adjustedTeamMetrics {
  epa                     # Expected Points Added
  epaAllowed             # Expected Points Added Allowed  
  explosiveness          # Big play capability
  explosivenessAllowed   # Big plays allowed
  highlightYards         # Explosive rushing yards
  highlightYardsAllowed  # Explosive rushing yards allowed
  lineYards              # Line yards (rushing between tackles)
  lineYardsAllowed       # Line yards allowed
  openFieldYards         # Open field rushing yards  
  openFieldYardsAllowed  # Open field yards allowed
  passingDownsSuccess    # Success rate on passing downs
  passingDownsSuccessAllowed # Success rate allowed on passing downs
  passingEpa             # Passing EPA
  passingEpaAllowed      # Passing EPA allowed
  rushingEpa             # Rushing EPA
  rushingEpaAllowed      # Rushing EPA allowed
  secondLevelYards       # Second level rushing yards
  secondLevelYardsAllowed # Second level yards allowed
  standardDownsSuccess   # Success rate on standard downs
  standardDownsSuccessAllowed # Success rate allowed on standard downs
  success                # Overall success rate
  successAllowed         # Overall success rate allowed
  team                   # Relationship to currentTeams
  teamId                 # Team ID (Int)
  year                   # Year (smallint)
}
```

**Filter Fields:**
- `teamId: {_eq: Int}`
- `year: {_eq: smallint}`

**⚠️ Important Notes:**
- NO `week` field available for filtering
- Data is season-aggregate, not week-by-week
- Use `year` as `smallint`, not `Int`

---

### **2. currentTeams**
**Description:** Current team information and conference affiliations

**Available Fields:**
```graphql
currentTeams {
  abbreviation    # Team abbreviation (String)
  classification  # Division level (division enum)
  conference      # Conference name (String)
  conferenceId    # Conference ID (smallint)
  division        # Division within conference (String)
  school          # School name (String)
  teamId          # Team ID (Int)
}
```

**Filter Fields:**
- `teamId: {_eq: Int}` ✅ 
- `id: {_eq: Int}` ❌ (Does not exist)

**⚠️ Important Notes:**
- Use `teamId` for filtering, NOT `id`
- Contains current conference alignments

---

### **3. teamTalent**
**Description:** Recruiting-based talent ratings for teams

**Available Fields:**
```graphql
teamTalent {
  talent    # Talent rating (numeric)
  team {    # Relationship to currentTeams (NOT a direct ID)
    teamId  # Team ID (Int) - accessed through relationship
    school  # School name
  }
  year      # Year (smallint)
}
```

**Filter Fields:**
```graphql
# ❌ WRONG - This doesn't work:
teamTalent(where: {team: {_eq: Int}})

# ✅ CORRECT - Filter by team relationship:
teamTalent(where: {team: {teamId: {_eq: Int}}})
teamTalent(where: {year: {_eq: smallint}})
```

**⚠️ Important Notes:**
- `team` is a RELATIONSHIP, not a direct field
- Filter by `team: {teamId: {_eq: Int}}`, NOT `team: {_eq: Int}`
- Use `year` as `smallint`
- Must select fields from the `team` relationship: `team { teamId }`

---

### **4. game**
**Description:** Game information and results

**Key Fields:**
```graphql
game {
  # Game Identification
  id                    # Game ID (Int)
  season               # Season year (smallint)
  seasonType           # Season type (season_type enum)
  week                 # Week number (smallint)
  startDate            # Game start time (timestamp)
  
  # Teams
  homeTeam             # Home team name (String)
  homeTeamId           # Home team ID (Int) - USE THIS FOR FILTERING  
  awayTeam             # Away team name (String)
  awayTeamId           # Away team ID (Int) - USE THIS FOR FILTERING
  
  # Scores
  homePoints           # Home team points (smallint)
  awayPoints           # Away team points (smallint)
  
  # ELO Ratings
  homeStartElo         # Home team starting ELO (Int)
  homeEndElo           # Home team ending ELO (Int)
  awayStartElo         # Away team starting ELO (Int)  
  awayEndElo           # Away team ending ELO (Int)
  
  # Win Probabilities
  homePostgameWinProb  # Home postgame win probability (numeric)
  awayPostgameWinProb  # Away postgame win probability (numeric)
  
  # Game Details
  excitement           # Game excitement index (numeric)
  neutralSite          # Neutral site game (Boolean)
  conferenceGame       # Conference game (Boolean)
  attendance           # Attendance (Int)
  venueId              # Venue ID (Int)
  
  # Status
  status               # Game status (game_status enum)
  completed            # Game completed (Boolean)
  
  # Relationships
  homeTeamInfo         # Relationship to currentTeams
  awayTeamInfo         # Relationship to currentTeams
  weather              # Relationship to GameWeather
  lines                # Relationship to game_lines
}
```

**Filter Fields:**
```graphql
where: {
  homeTeamId: {_eq: Int}       # Use homeTeamId, not homeTeam
  awayTeamId: {_eq: Int}       # Use awayTeamId, not awayTeam
  season: {_eq: smallint}      # Use 'season' in game table, not 'year'
  week: {_eq: smallint}
  week: {_lte: smallint}       # Less than or equal
  seasonType: {_eq: String}    # "regular", "postseason"
  
  # OR conditions for team games - use TeamId fields!
  _or: [
    {homeTeamId: {_eq: Int}},
    {awayTeamId: {_eq: Int}}
  ]
}
```

**⚠️ Important Notes:**
- Use `season` for filtering, not `year` (different from other tables!)
- ELO fields: `homeStartElo`, `awayStartElo` (not `homeElo`, `awayElo`)
- Win probability fields: `homePostgameWinProb`, `awayPostgameWinProb`

---

### **5. gameLines**
**Description:** Betting lines and odds for games

**Available Fields:**
```graphql
gameLines {
  spread           # Point spread (numeric)
  overUnder        # Total points line (numeric)
  homeMoneyline    # Home team moneyline (Int)
  awayMoneyline    # Away team moneyline (Int)
  provider         # Odds provider (String)
  
  # Game Reference
  homeTeam         # Home team ID (Int)
  awayTeam         # Away team ID (Int)
  year             # Year (smallint)
  week             # Week (smallint)
}
```

**Filter Fields:**
- `homeTeam: {_eq: Int}`
- `awayTeam: {_eq: Int}`
- `year: {_eq: smallint}`
- `week: {_eq: smallint}`

---

### **6. gameWeather**
**Description:** Weather conditions for games

**Available Fields:**
```graphql
gameWeather {
  temperature              # Temperature
  dewPoint                # Dew point
  humidity                # Humidity percentage
  precipitation           # Precipitation
  snowfall                # Snowfall amount
  windDirection           # Wind direction
  windSpeed               # Wind speed
  pressure                # Atmospheric pressure
  visibility              # Visibility
  weatherConditionCode    # Weather condition code
  weatherCondition {      # Weather condition details
    description
  }
}
```

---

## **Common Data Types**

### **Enums:**
- `season_type`: "regular", "postseason"
- `game_status`: Various game status values
- `division`: FBS, FCS, etc.

### **Numeric Types:**
- `smallint`: Small integer (use for years, weeks)
- `Int`: Standard integer (use for IDs)
- `numeric`: Decimal numbers (use for ratings, probabilities)

---

## **Correct GraphQL Query Examples**

### **Basic Team Metrics Query:**
```graphql
query GetTeamMetrics($teamId: Int!, $year: smallint!) {
  adjustedTeamMetrics(where: {teamId: {_eq: $teamId}, year: {_eq: $year}}) {
    epa
    epaAllowed
    success
    successAllowed
    explosiveness
    explosivenessAllowed
  }
}
```

### **Team Games Query:**
```graphql
query GetTeamGames($teamId: Int!, $season: smallint!, $maxWeek: smallint!) {
  game(where: {
    _or: [
      {homeTeamId: {_eq: $teamId}}, 
      {awayTeamId: {_eq: $teamId}}
    ], 
    season: {_eq: $season}, 
    week: {_lte: $maxWeek}
  }, orderBy: {week: ASC}) {
    homeTeam
    awayTeam
    homeTeamId
    awayTeamId
    homePoints
    awayPoints
    homeStartElo
    awayStartElo
    homePostgameWinProb
    awayPostgameWinProb
    week
    seasonType
  }
}
```

### **Team Information Query:**
```graphql
query GetTeamInfo($teamId: Int!) {
  currentTeams(where: {teamId: {_eq: $teamId}}) {
    school
    conference
    division
  }
}
```

### **Team Talent Query:**
```graphql
query GetTeamTalent($teamId: Int!, $year: smallint!) {
  teamTalent(where: {team: {teamId: {_eq: $teamId}}, year: {_eq: $year}}) {
    talent
    team {
      teamId
      school
    }
  }
}
```

---

## **Common Mistakes to Avoid**

### **❌ Wrong Field Names:**
```graphql
# Wrong:
homeElo, awayElo
homePostgameWinProbability, awayPostgameWinProbability
season: {_eq: 2025}
team: {_eq: $teamId}      # in teamTalent - team is a relationship!
id: {_eq: $teamId}        # in currentTeams

# Correct:
homeStartElo, awayStartElo
homePostgameWinProb, awayPostgameWinProb  
year: {_eq: 2025}
team: {teamId: {_eq: $teamId}}  # in teamTalent - filter through relationship
teamId: {_eq: $teamId}          # in currentTeams
```

### **❌ Wrong Variable Types:**
```graphql
# Wrong:
$year: Int = 2025

# Correct:  
$year: smallint = 2025
```

### **❌ Non-existent Fields:**
```graphql
# These fields DO NOT exist:
adjustedTeamMetrics(where: {week: {_eq: 6}})       # No week field
game(where: {year: {_eq: 2025}})                   # Use 'season' not 'year' in game table!
teamTalent(where: {team: {_eq: $teamId}})          # team is relationship, not direct field
```

---

## **Performance Tips**

1. **Limit Results:** Always use `limit:` for large queries
2. **Order Results:** Use `orderBy:` for consistent results
3. **Specific Fields:** Only request fields you need
4. **Batch Queries:** Combine related data in single query
5. **Use Aliases:** Use aliases for multiple queries on same table

---

## **Team ID Reference**

**Common Team IDs:**
- Ohio State: 194
- Michigan: 2  
- Illinois: 356
- Alabama: 8
- Georgia: 52
- Texas: 245
- Oregon: 183

**To find team IDs:**
```graphql
query FindTeam($schoolName: String!) {
  currentTeams(where: {school: {_ilike: $schoolName}}) {
    teamId
    school
    conference
  }
}
```

---

# 🚀 ELITE ENHANCEMENT ENDPOINTS - Professional Handicapper Level

## **Professional-Grade Enhancement Endpoints**

The following endpoints elevate the predictor from "good" to **elite professional handicapper intelligence** by providing game flow, situational dominance, and market intelligence data.

### **5. `drives` - Game Flow & Momentum Intelligence**
**Purpose:** Drive-by-drive analysis for game flow patterns and momentum shifts

**Available Fields:**
```graphql
drives {
  gameId                 # Game identifier (Int)
  driveId                # Unique drive identifier (Int) 
  driveNumber            # Sequential drive number in game (Int)
  offenseTeam            # Offensive team ID (Int)
  defenseTeam            # Defensive team ID (Int)
  startPeriod            # Starting quarter/period (Int)
  endPeriod              # Ending quarter/period (Int)
  startYardLine          # Starting field position 0-100 (Int)
  endYardLine            # Ending field position 0-100 (Int)
  startTime              # Starting game clock (String)
  endTime                # Ending game clock (String) 
  elapsed                # Time elapsed on drive (String)
  plays                  # Number of plays in drive (Int)
  yards                  # Total yards gained/lost (Int)
  driveResult            # Drive outcome (String)
  scoringOpportunities   # Red zone opportunities (Int)
  isScoring              # Whether drive resulted in points (Boolean)
}
```

**Drive Result Values:**
- "TD" - Touchdown
- "FG" - Field Goal
- "PUNT" - Punt
- "INT" - Interception
- "FUMBLE" - Fumble
- "DOWNS" - Turnover on downs
- "END_HALF" - End of half/game
- "SAFETY" - Safety

**Filter Fields:**
- `gameId: {_eq: Int}`
- `offenseTeam: {_eq: Int}` or `defenseTeam: {_eq: Int}`
- Team analysis: `_or: [{offenseTeam: {_eq: $teamId}}, {defenseTeam: {_eq: $teamId}}]`
- Season filtering via game relationship: `game: {season: {_eq: smallint}}`

**Elite Metrics Derived:**
- Opening drive success rates (competitive edge indicator)
- Red zone efficiency (finishing ability)
- Three-and-out frequency (momentum killer analysis)
- Fourth quarter clutch performance (pressure response)
- Scoring drive percentage (offensive consistency)

---

### **6. `plays` - Situational Dominance & Money Downs**
**Purpose:** Play-by-play analysis for critical situations and money downs

**Available Fields:**
```graphql
plays {
  gameId                 # Game identifier (Int)
  driveId                # Drive identifier (Int)
  playId                 # Unique play identifier (Int)
  offenseTeam            # Offensive team ID (Int)
  defenseTeam            # Defensive team ID (Int)
  period                 # Quarter/period (Int)
  clock                  # Game clock remaining (String)
  down                   # Down number 1-4 (Int)
  distance               # Yards to go for first down (Int)
  yardLine               # Field position 0-100 (Int)
  yardsGained            # Result of play in yards (Int)
  playType               # Type of play (String)
  epa                    # Expected Points Added (Float)
  wpa                    # Win Probability Added (Float)
  success                # Successful play by EPA standards (Boolean)
  ppa                    # Predicted Points Added (Float)
  scoringPlay            # Whether play resulted in score (Boolean)
}
```

**Play Type Values:**
- "pass" - Passing play
- "rush" - Running play
- "punt" - Punting play
- "kick" - Field goal/PAT attempt
- "kickoff" - Kickoff
- "penalty" - Penalty

**Critical Situation Filters:**
```graphql
# Third down conversions (money downs)
{down: {_eq: 3}}

# Fourth down attempts (coaching aggression)  
{down: {_eq: 4}}

# Red zone plays (scoring efficiency)
{yardLine: {_lte: 20}}

# Fourth quarter execution (clutch performance)
{period: {_eq: 4}}

# High-leverage moments (game-changing plays)
{wpa: {_gte: 0.05}}
```

**Elite Metrics Derived:**
- Third down conversion rates (drive sustainability)
- Fourth down aggression rates (coaching philosophy)
- Red zone touchdown vs field goal rates (finishing ability)
- Late-game execution under pressure
- High-leverage play success rates

---

### **7. `playerStats` - Key Player Impact Analysis**
**Purpose:** Individual player performance for team strength assessment

**Available Fields:**
```graphql
playerStats {
  playerId               # Player identifier (Int)
  player                 # Player name (String)
  teamId                 # Team identifier (Int)
  year                   # Season year (smallint)
  category               # Stat category (String)
  statType               # Specific stat type (String)
  stat                   # Stat abbreviation (String)
  value                  # Statistical value (Float)
}
```

**Category Values:**
- "passing" - Quarterback statistics
- "rushing" - Running back statistics
- "receiving" - Receiver statistics
- "defensive" - Defensive player statistics
- "kicking" - Kicker statistics
- "punting" - Punter statistics

**Key Player Analysis:**
- Quarterback consistency and performance trends
- Offensive line effectiveness (sacks allowed analysis)
- Running back explosiveness and reliability
- Key skill position player impact
- Defensive impact player identification

---

### **8. `gameLines` - Market Intelligence & Betting Data**
**Purpose:** Professional betting lines and market consensus analysis

**Available Fields:**
```graphql
gameLines {
  gameId                 # Game identifier (Int)
  homeTeam               # Home team name (String)
  awayTeam               # Away team name (String)
  year                   # Season year (smallint)
  week                   # Week number (Int)
  spread                 # Point spread (Float, negative = home favored)
  overUnder              # Total points line (Float)
  homeMoneyline          # Home team moneyline odds (Int)
  awayMoneyline          # Away team moneyline odds (Int)
  provider               # Sportsbook provider (String)
}
```

**Provider Values:**
- "consensus" - Market consensus line
- "draftkings" - DraftKings sportsbook
- "fanduel" - FanDuel sportsbook
- "espn" - ESPN BET
- "bovada" - Bovada sportsbook

**Market Intelligence Metrics:**
- Line movement analysis (market sentiment)
- Consensus vs specific book differences
- Moneyline implied probability vs model prediction
- Market efficiency indicators

---

### **9. `ratings` - Advanced Team Ratings & Rankings**
**Purpose:** Composite ratings from multiple rating systems for cross-validation

**Available Fields:**
```graphql
ratings {
  teamId                 # Team identifier (Int)
  year                   # Season year (smallint)
  week                   # Week number (Int)
  overallElo             # Overall ELO rating (Float)
  offenseElo             # Offensive ELO rating (Float)
  defenseElo             # Defensive ELO rating (Float)
  fpi                    # ESPN Football Power Index (Float)
  sp                     # S&P+ rating (Float)
  strengthOfSchedule     # Schedule difficulty rating (Float)
  expectedWins           # Model-projected wins (Float)
}
```

**Rating System Cross-Validation:**
- ELO ratings for historical performance context
- FPI for ESPN's computer model consensus
- S&P+ for advanced statistical analysis
- Strength of schedule for opponent quality context

---

### **10. `gameWeather` - Weather Impact Analysis**
**Purpose:** Weather conditions for outdoor games and environmental factors

**Available Fields:**
```graphql
gameWeather {
  gameId                 # Game identifier (Int)
  temperature            # Temperature in Fahrenheit (Int)
  dewPoint               # Dew point temperature (Int)
  humidity               # Relative humidity percentage (Int)
  precipitation          # Chance of precipitation (Float)
  snowfall               # Expected snowfall amount (Float)
  windDirection          # Wind direction (String)
  windSpeed              # Wind speed in MPH (Int)
  pressure               # Barometric pressure (Float)
  visibility             # Visibility in miles (Float)
}
```

**Weather Impact Factors:**
- Temperature effects on performance (cold weather games)
- Wind speed impact on passing games
- Precipitation effects on ball handling and field conditions
- Visibility impact on aerial attack effectiveness

---

### **11. `venues` - Stadium & Venue Intelligence**
**Purpose:** Home field advantage and venue-specific factors

**Available Fields:**
```graphql
venues {
  venueId                # Venue identifier (Int)
  name                   # Stadium name (String)
  city                   # City location (String)
  state                  # State location (String)
  zip                    # ZIP code (String)
  countryCode            # Country code (String)
  timezone               # Time zone (String)
  latitude               # GPS latitude (Float)
  longitude              # GPS longitude (Float)
  elevation              # Elevation above sea level (Int)
  capacity               # Stadium capacity (Int)
  yearConstructed        # Construction year (Int)
  grass                  # Natural grass vs artificial (Boolean)
  domeType               # Stadium type (String)
}
```

**Dome Type Values:**
- "outdoor" - Open-air stadium
- "dome" - Fully enclosed dome
- "retractable" - Retractable roof

**Venue Advantage Factors:**
- Elevation impact on kicking and conditioning
- Grass vs artificial turf performance differences
- Stadium capacity for crowd noise impact
- Geographic and climate considerations

---

## **Enhanced Elite Query Patterns**

### **Game Flow Intelligence Query**
```graphql
query GameFlowIntelligence($teamId: Int!, $currentYear: smallint!) {
  # Drive-level analysis for momentum patterns
  teamDrives: drives(where: {
    _or: [{offenseTeam: {_eq: $teamId}}, {defenseTeam: {_eq: $teamId}}],
    game: {season: {_eq: $currentYear}}
  }) {
    offenseTeam defenseTeam gameId startPeriod endPeriod
    driveResult startYardLine endYardLine plays elapsed
    scoringOpportunities isScoring yards
  }
  
  # Critical situational performance
  moneyDowns: plays(where: {
    _or: [{offenseTeam: {_eq: $teamId}}, {defenseTeam: {_eq: $teamId}}],
    game: {season: {_eq: $currentYear}},
    down: {_in: [3, 4]}
  }) {
    offenseTeam defenseTeam down distance yardLine period
    success epa wpa playType scoringPlay
  }
  
  # Red zone efficiency analysis
  redZoneSnaps: plays(where: {
    _or: [{offenseTeam: {_eq: $teamId}}, {defenseTeam: {_eq: $teamId}}],
    game: {season: {_eq: $currentYear}},
    yardLine: {_lte: 20}
  }) {
    offenseTeam defenseTeam playType epa success scoringPlay
    down distance yardLine
  }
}
```

### **Market Intelligence & Ratings Consensus Query**
```graphql
query MarketIntelligence($homeTeamId: Int!, $awayTeamId: Int!, $currentYear: smallint!, $currentWeek: Int!) {
  # Professional betting lines
  currentLines: gameLines(where: {
    homeTeam: {teamId: {_eq: $homeTeamId}},
    awayTeam: {teamId: {_eq: $awayTeamId}},
    year: {_eq: $currentYear},
    week: {_eq: $currentWeek}
  }) {
    spread overUnder homeMoneyline awayMoneyline provider
  }
  
  # Advanced composite ratings
  homeRatings: ratings(where: {
    teamId: {_eq: $homeTeamId},
    year: {_eq: $currentYear},
    week: {_eq: $currentWeek}
  }) {
    overallElo offenseElo defenseElo fpi sp 
    strengthOfSchedule expectedWins
  }
  
  awayRatings: ratings(where: {
    teamId: {_eq: $awayTeamId},
    year: {_eq: $currentYear},
    week: {_eq: $currentWeek}
  }) {
    overallElo offenseElo defenseElo fpi sp 
    strengthOfSchedule expectedWins
  }
}
```

### **Environmental & Venue Factors Query**
```graphql
query EnvironmentalFactors($homeTeamId: Int!, $awayTeamId: Int!, $currentYear: smallint!, $currentWeek: Int!) {
  # Weather impact analysis
  gameWeather: gameWeather(where: {
    game: {
      homeTeam: {teamId: {_eq: $homeTeamId}},
      awayTeam: {teamId: {_eq: $awayTeamId}},
      season: {_eq: $currentYear},
      week: {_eq: $currentWeek}
    }
  }) {
    temperature windSpeed precipitation visibility
    humidity pressure dewPoint snowfall windDirection
  }
  
  # Stadium and venue intelligence
  venue: venues(where: {
    games: {
      homeTeam: {teamId: {_eq: $homeTeamId}},
      season: {_eq: $currentYear}
    }
  }) {
    name city state elevation capacity yearConstructed
    grass domeType timezone latitude longitude
  }
}
```

## **Elite Predictor Implementation Framework**

### **Enhanced Prediction Factors (Professional Grade)**

**Core Performance Metrics (25%)**
- EPA differential analysis
- Success rate advantages
- Explosiveness comparisons

**Game Flow Intelligence (20%)**
- Opening drive success patterns
- Fourth quarter clutch performance
- Red zone efficiency differentials
- Three-and-out frequency analysis

**Situational Dominance (15%)**
- Third down conversion rates (money downs)
- Fourth down aggression and success
- High-leverage moment performance
- Late-game execution under pressure

**Opponent-Adjusted Performance (15%)**
- Performance weighted by opponent strength
- Schedule difficulty considerations
- Quality win analysis

**Market Intelligence (10%)**
- Betting line movement analysis
- Market consensus vs model disagreement
- Professional sharp money indicators

**Environmental Factors (8%)**
- Weather impact on game style
- Venue advantages and elevation effects
- Travel and time zone considerations

**Advanced Ratings Consensus (7%)**
- Multiple rating system validation
- ELO, FPI, S&P+ cross-verification
- Expected wins vs actual performance

This enhanced schema provides the foundation for elite-level professional handicapping intelligence, moving beyond basic statistics to comprehensive game analysis.

---

This schema documentation should prevent future field name issues and provide a complete reference for building GraphQL queries against the College Football Data API.