# Advanced GraphQL Schema

## Table of Contents

1. [Overview](#overview)
2. [API Information](#api-information)
   - [Endpoints](#endpoints)
   - [Authentication](#authentication)
   - [Access Requirements](#access-requirements)
3. [GraphQL Types](#graphql-types)
   - [Player Metrics](#player-metrics)
   - [Team Metrics](#team-metrics)
   - [Athletes](#athletes)
   - [Coaches](#coaches)
   - [Games](#games)
   - [Recruiting](#recruiting)
   - [Draft](#draft)
   - [Polls & Rankings](#polls--rankings)
   - [Utility Types](#utility-types)
4. [Queries](#queries)
5. [Subscriptions](#subscriptions)
6. [Tutorials & Resources](#tutorials--resources)

---

## Overview

Welcome to the CFBD (College Football Data) GraphQL API documentation. This API provides mechanisms for querying and subscribing to the comprehensive CFBD dataset using GraphQL, offering a more dynamic way to access college football data compared to traditional REST APIs.

### Key Features
- **Dynamic Queries**: Flexible GraphQL queries for precise data retrieval
- **Real-time Updates**: GraphQL subscriptions for live data
- **Comprehensive Dataset**: Access to player stats, team metrics, recruiting data, and more
- **Type-Safe**: Strongly typed schema with detailed type definitions

### Contact & Support
- **Email**: admin@collegefootballdata.com
- **Website**: https://collegefootballdata.com/about
- **Terms of Service**: https://collegefootballdata.com/about

---

## API Information

### Endpoints

**Production Environment:**
```
https://graphql.collegefootballdata.com/v1/graphql
```

**Headers:**
```
Authorization: Bearer <YOUR_API_KEY>
```

### Authentication

All requests must include your API key in the Authorization header as a Bearer token.

**Example:**
```
Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p
```

### Access Requirements

- **Patreon Tier 3+**: You must be subscribed to Patreon Tier 3 or higher to access the GraphQL API
- **API Key**: Use the same API key from the REST API, or register at https://collegefootballdata.com/key
- **Key Generation**: Auto-generated and emailed upon Patreon subscription
- **Sync Time**: Allow up to 15 minutes for Patreon benefits to sync

---

## GraphQL Types

### Player Metrics

#### AdjustedPlayerMetrics
Core type for player-adjusted performance metrics.

**Related Types:**
- AdjustedPlayerMetricsAggregate
- AdjustedPlayerMetricsAggregateBoolExp
- AdjustedPlayerMetricsAggregateFields
- AdjustedPlayerMetricsAggregateOrderBy
- AdjustedPlayerMetricsAvgFields
- AdjustedPlayerMetricsAvgOrderBy
- AdjustedPlayerMetricsBoolExp
- AdjustedPlayerMetricsMaxFields
- AdjustedPlayerMetricsMaxOrderBy
- AdjustedPlayerMetricsMinFields
- AdjustedPlayerMetricsMinOrderBy
- AdjustedPlayerMetricsOrderBy
- AdjustedPlayerMetricsSelectColumn
- AdjustedPlayerMetricsStddevFields
- AdjustedPlayerMetricsStddevOrderBy
- AdjustedPlayerMetricsStddevPopFields
- AdjustedPlayerMetricsStddevPopOrderBy
- AdjustedPlayerMetricsStddevSampFields
- AdjustedPlayerMetricsStddevSampOrderBy
- AdjustedPlayerMetricsSumFields
- AdjustedPlayerMetricsSumOrderBy
- AdjustedPlayerMetricsVarPopFields
- AdjustedPlayerMetricsVarPopOrderBy
- AdjustedPlayerMetricsVarSampFields
- AdjustedPlayerMetricsVarSampOrderBy
- AdjustedPlayerMetricsVarianceFields
- AdjustedPlayerMetricsVarianceOrderBy
- adjustedPlayerMetricsAggregateBoolExpCount
- player_adjusted_metric_type (enum)

### Team Metrics

#### AdjustedTeamMetrics
Core type for team-adjusted performance metrics including EPA, explosiveness, and success rates.

**Related Types:**
- AdjustedTeamMetricsAggregate
- AdjustedTeamMetricsAggregateFields
- AdjustedTeamMetricsAvgFields
- AdjustedTeamMetricsBoolExp
- AdjustedTeamMetricsMaxFields
- AdjustedTeamMetricsMinFields
- AdjustedTeamMetricsOrderBy
- AdjustedTeamMetricsSelectColumn
- AdjustedTeamMetricsStddevFields
- AdjustedTeamMetricsStddevPopFields
- AdjustedTeamMetricsStddevSampFields
- AdjustedTeamMetricsSumFields
- AdjustedTeamMetricsVarPopFields
- AdjustedTeamMetricsVarSampFields
- AdjustedTeamMetricsVarianceFields

#### TeamTalent
Team talent composite ratings.

**Related Types:**
- TeamTalentAggregate
- TeamTalentAggregateFields
- TeamTalentAvgFields
- TeamTalentBoolExp
- TeamTalentMaxFields
- TeamTalentMinFields
- TeamTalentOrderBy
- TeamTalentSelectColumn
- TeamTalentStddevFields
- TeamTalentStddevPopFields
- TeamTalentStddevSampFields
- TeamTalentSumFields
- TeamTalentVarPopFields
- TeamTalentVarSampFields
- TeamTalentVarianceFields

#### Teams
**Current Teams:**
- currentTeams
- currentTeamsAggregate
- currentTeamsAggregateFields
- currentTeamsAvgFields
- currentTeamsBoolExp
- currentTeamsMaxFields
- currentTeamsMinFields
- currentTeamsOrderBy
- currentTeamsSelectColumn
- currentTeamsStddevFields
- currentTeamsStddevPopFields
- currentTeamsStddevSampFields
- currentTeamsSumFields
- currentTeamsVarPopFields
- currentTeamsVarSampFields
- currentTeamsVarianceFields

**Historical Teams:**
- historicalTeam
- historicalTeamAggregate
- historicalTeamAggregateFields
- historicalTeamAvgFields
- historicalTeamBoolExp
- historicalTeamMaxFields
- historicalTeamMinFields
- historicalTeamOrderBy
- historicalTeamSelectColumn
- historicalTeamStddevFields
- historicalTeamStddevPopFields
- historicalTeamStddevSampFields
- historicalTeamSumFields
- historicalTeamVarPopFields
- historicalTeamVarSampFields
- historicalTeamVarianceFields

### Athletes

#### Athlete
Core athlete/player information.

**Related Types:**
- AthleteAggregate
- AthleteAggregateBoolExp
- AthleteAggregateFields
- AthleteAggregateOrderBy
- AthleteAvgFields
- AthleteAvgOrderBy
- AthleteBoolExp
- AthleteMaxFields
- AthleteMaxOrderBy
- AthleteMinFields
- AthleteMinOrderBy
- AthleteOrderBy
- AthleteSelectColumn
- AthleteStddevFields
- AthleteStddevOrderBy
- AthleteStddevPopFields
- AthleteStddevPopOrderBy
- AthleteStddevSampFields
- AthleteStddevSampOrderBy
- AthleteSumFields
- AthleteSumOrderBy
- AthleteVarPopFields
- AthleteVarPopOrderBy
- AthleteVarSampFields
- AthleteVarSampOrderBy
- AthleteVarianceFields
- AthleteVarianceOrderBy
- athleteAggregateBoolExpCount

#### AthleteTeam
Athlete team affiliation information.

**Related Types:**
- AthleteTeamAggregate
- AthleteTeamAggregateBoolExp
- AthleteTeamAggregateFields
- AthleteTeamAggregateOrderBy
- AthleteTeamAvgFields
- AthleteTeamAvgOrderBy
- AthleteTeamBoolExp
- AthleteTeamMaxFields
- AthleteTeamMaxOrderBy
- AthleteTeamMinFields
- AthleteTeamMinOrderBy
- AthleteTeamOrderBy
- AthleteTeamSelectColumn
- AthleteTeamStddevFields
- AthleteTeamStddevOrderBy
- AthleteTeamStddevPopFields
- AthleteTeamStddevPopOrderBy
- AthleteTeamStddevSampFields
- AthleteTeamStddevSampOrderBy
- AthleteTeamSumFields
- AthleteTeamSumOrderBy
- AthleteTeamVarPopFields
- AthleteTeamVarPopOrderBy
- AthleteTeamVarSampFields
- AthleteTeamVarSampOrderBy
- AthleteTeamVarianceFields
- AthleteTeamVarianceOrderBy
- athleteTeamAggregateBoolExpCount

### Coaches

#### Coach
Core coach information.

**Related Types:**
- CoachAggregate
- CoachAggregateFields
- CoachAvgFields
- CoachBoolExp
- CoachMaxFields
- CoachMinFields
- CoachOrderBy
- CoachSelectColumn
- CoachStddevFields
- CoachStddevPopFields
- CoachStddevSampFields
- CoachSumFields
- CoachVarPopFields
- CoachVarSampFields
- CoachVarianceFields

#### CoachSeason
Season-specific coach records and statistics.

**Related Types:**
- CoachSeasonAggregate
- CoachSeasonAggregateBoolExp
- CoachSeasonAggregateFields
- CoachSeasonAggregateOrderBy
- CoachSeasonAvgFields
- CoachSeasonAvgOrderBy
- CoachSeasonBoolExp
- CoachSeasonMaxFields
- CoachSeasonMaxOrderBy
- CoachSeasonMinFields
- CoachSeasonMinOrderBy
- CoachSeasonOrderBy
- CoachSeasonSelectColumn
- CoachSeasonStddevFields
- CoachSeasonStddevOrderBy
- CoachSeasonStddevPopFields
- CoachSeasonStddevPopOrderBy
- CoachSeasonStddevSampFields
- CoachSeasonStddevSampOrderBy
- CoachSeasonSumFields
- CoachSeasonSumOrderBy
- CoachSeasonVarPopFields
- CoachSeasonVarPopOrderBy
- CoachSeasonVarSampFields
- CoachSeasonVarSampOrderBy
- CoachSeasonVarianceFields
- CoachSeasonVarianceOrderBy
- coachSeasonAggregateBoolExpCount

### Games

#### game
Core game information.

**Related Types:**
- gameAggregate
- gameAggregateFields
- gameAvgFields
- gameBoolExp
- gameMaxFields
- gameMinFields
- gameOrderBy
- gameSelectColumn
- gameStddevFields
- gameStddevPopFields
- gameStddevSampFields
- gameSumFields
- gameVarPopFields
- gameVarSampFields
- gameVarianceFields
- game_status (enum)

#### GameLines
Betting lines and spread information.

**Related Types:**
- GameLinesAggregate
- GameLinesAggregateBoolExp
- GameLinesAggregateFields
- GameLinesAggregateOrderBy
- GameLinesAvgFields
- GameLinesAvgOrderBy
- GameLinesBoolExp
- GameLinesMaxFields
- GameLinesMaxOrderBy
- GameLinesMinFields
- GameLinesMinOrderBy
- GameLinesOrderBy
- GameLinesSelectColumn
- GameLinesStddevFields
- GameLinesStddevOrderBy
- GameLinesStddevPopFields
- GameLinesStddevPopOrderBy
- GameLinesStddevSampFields
- GameLinesStddevSampOrderBy
- GameLinesSumFields
- GameLinesSumOrderBy
- GameLinesVarPopFields
- GameLinesVarPopOrderBy
- GameLinesVarSampFields
- GameLinesVarSampOrderBy
- GameLinesVarianceFields
- GameLinesVarianceOrderBy
- gameLinesAggregateBoolExpCount

#### GamePlayerStat
Player statistics within games.

**Related Types:**
- GamePlayerStatAggregate
- GamePlayerStatAggregateBoolExp
- GamePlayerStatAggregateFields
- GamePlayerStatAggregateOrderBy
- GamePlayerStatAvgFields
- GamePlayerStatAvgOrderBy
- GamePlayerStatBoolExp
- GamePlayerStatMaxFields
- GamePlayerStatMaxOrderBy
- GamePlayerStatMinFields
- GamePlayerStatMinOrderBy
- GamePlayerStatOrderBy
- GamePlayerStatSelectColumn
- GamePlayerStatStddevFields
- GamePlayerStatStddevOrderBy
- GamePlayerStatStddevPopFields
- GamePlayerStatStddevPopOrderBy
- GamePlayerStatStddevSampFields
- GamePlayerStatStddevSampOrderBy
- GamePlayerStatSumFields
- GamePlayerStatSumOrderBy
- GamePlayerStatVarPopFields
- GamePlayerStatVarPopOrderBy
- GamePlayerStatVarSampFields
- GamePlayerStatVarSampOrderBy
- GamePlayerStatVarianceFields
- GamePlayerStatVarianceOrderBy
- gamePlayerStatAggregateBoolExpCount

#### GameTeam
Team information within game context.

**Related Types:**
- GameTeamBoolExp
- GameTeamOrderBy
- GameTeamSelectColumn

#### GameMedia
Game broadcast and media information.

**Related Types:**
- GameMediaAggregateOrderBy
- GameMediaBoolExp
- GameMediaMaxOrderBy
- GameMediaMinOrderBy
- GameMediaOrderBy
- GameMediaSelectColumn
- media_type (enum)

#### GameWeather
Weather conditions for games.

**Related Types:**
- GameWeatherBoolExp
- GameWeatherOrderBy
- GameWeatherSelectColumn
- WeatherCondition
- WeatherConditionBoolExp
- WeatherConditionOrderBy
- WeatherConditionSelectColumn

#### Scoreboard
Live scoring and game status information.

**Related Types:**
- ScoreboardBoolExp
- ScoreboardOrderBy
- ScoreboardSelectColumn

#### Calendar
Game scheduling and calendar information.

**Related Types:**
- CalendarBoolExp
- CalendarOrderBy
- CalendarSelectColumn

#### PredictedPoints
Game prediction data.

**Related Types:**
- predictedPoints
- predictedPointsAggregate
- predictedPointsAggregateFields
- predictedPointsAvgFields
- predictedPointsBoolExp
- predictedPointsMaxFields
- predictedPointsMinFields
- predictedPointsOrderBy
- predictedPointsSelectColumn
- predictedPointsStddevFields
- predictedPointsStddevPopFields
- predictedPointsStddevSampFields
- predictedPointsSumFields
- predictedPointsVarPopFields
- predictedPointsVarSampFields
- predictedPointsVarianceFields

### Recruiting

#### Recruit
Core recruit information.

**Related Types:**
- RecruitAggregate
- RecruitAggregateBoolExp
- RecruitAggregateFields
- RecruitAggregateOrderBy
- RecruitAvgFields
- RecruitAvgOrderBy
- RecruitBoolExp
- RecruitMaxFields
- RecruitMaxOrderBy
- RecruitMinFields
- RecruitMinOrderBy
- RecruitOrderBy
- RecruitSelectColumn
- RecruitStddevFields
- RecruitStddevOrderBy
- RecruitStddevPopFields
- RecruitStddevPopOrderBy
- RecruitStddevSampFields
- RecruitStddevSampOrderBy
- RecruitSumFields
- RecruitSumOrderBy
- RecruitVarPopFields
- RecruitVarPopOrderBy
- RecruitVarSampFields
- RecruitVarSampOrderBy
- RecruitVarianceFields
- RecruitVarianceOrderBy
- recruitAggregateBoolExpCount
- recruit_type (enum)

#### RecruitPosition
Recruit position information.

**Related Types:**
- RecruitPositionAggregate
- RecruitPositionAggregateFields
- RecruitPositionAvgFields
- RecruitPositionBoolExp
- RecruitPositionMaxFields
- RecruitPositionMinFields
- RecruitPositionOrderBy
- RecruitPositionSelectColumn
- RecruitPositionStddevFields
- RecruitPositionStddevPopFields
- RecruitPositionStddevSampFields
- RecruitPositionSumFields
- RecruitPositionVarPopFields
- RecruitPositionVarSampFields
- RecruitPositionVarianceFields

#### RecruitSchool
School recruiting information.

**Related Types:**
- RecruitSchoolAggregate
- RecruitSchoolAggregateFields
- RecruitSchoolAvgFields
- RecruitSchoolBoolExp
- RecruitSchoolMaxFields
- RecruitSchoolMinFields
- RecruitSchoolOrderBy
- RecruitSchoolSelectColumn
- RecruitSchoolStddevFields
- RecruitSchoolStddevPopFields
- RecruitSchoolStddevSampFields
- RecruitSchoolSumFields
- RecruitSchoolVarPopFields
- RecruitSchoolVarSampFields
- RecruitSchoolVarianceFields

#### RecruitingTeam
Team recruiting rankings and information.

**Related Types:**
- RecruitingTeamAggregate
- RecruitingTeamAggregateFields
- RecruitingTeamAvgFields
- RecruitingTeamBoolExp
- RecruitingTeamMaxFields
- RecruitingTeamMinFields
- RecruitingTeamOrderBy
- RecruitingTeamSelectColumn
- RecruitingTeamStddevFields
- RecruitingTeamStddevPopFields
- RecruitingTeamStddevSampFields
- RecruitingTeamSumFields
- RecruitingTeamVarPopFields
- RecruitingTeamVarSampFields
- RecruitingTeamVarianceFields

### Draft

#### DraftPicks
NFL Draft pick information.

**Related Types:**
- DraftPicksAggregate
- DraftPicksAggregateBoolExp
- DraftPicksAggregateFields
- DraftPicksAggregateOrderBy
- DraftPicksAvgFields
- DraftPicksAvgOrderBy
- DraftPicksBoolExp
- DraftPicksMaxFields
- DraftPicksMaxOrderBy
- DraftPicksMinFields
- DraftPicksMinOrderBy
- DraftPicksOrderBy
- DraftPicksSelectColumn
- DraftPicksStddevFields
- DraftPicksStddevOrderBy
- DraftPicksStddevPopFields
- DraftPicksStddevPopOrderBy
- DraftPicksStddevSampFields
- DraftPicksStddevSampOrderBy
- DraftPicksSumFields
- DraftPicksSumOrderBy
- DraftPicksVarPopFields
- DraftPicksVarPopOrderBy
- DraftPicksVarSampFields
- DraftPicksVarSampOrderBy
- DraftPicksVarianceFields
- DraftPicksVarianceOrderBy
- draftPicksAggregateBoolExpCount

#### DraftPosition
Draft position information.

**Related Types:**
- DraftPositionBoolExp
- DraftPositionOrderBy
- DraftPositionSelectColumn

#### DraftTeam
NFL team draft information.

**Related Types:**
- DraftTeamBoolExp
- DraftTeamOrderBy
- DraftTeamSelectColumn

### Polls & Rankings

#### Poll
Polling data (AP, Coaches, etc.).

**Related Types:**
- PollAggregateOrderBy
- PollAvgOrderBy
- PollBoolExp
- PollMaxOrderBy
- PollMinOrderBy
- PollOrderBy
- PollSelectColumn
- PollStddevOrderBy
- PollStddevPopOrderBy
- PollStddevSampOrderBy
- PollSumOrderBy
- PollVarPopOrderBy
- PollVarSampOrderBy
- PollVarianceOrderBy

#### PollRank
Individual poll rankings.

**Related Types:**
- PollRankAggregateOrderBy
- PollRankAvgOrderBy
- PollRankBoolExp
- PollRankMaxOrderBy
- PollRankMinOrderBy
- PollRankOrderBy
- PollRankSelectColumn
- PollRankStddevOrderBy
- PollRankStddevPopOrderBy
- PollRankStddevSampOrderBy
- PollRankSumOrderBy
- PollRankVarPopOrderBy
- PollRankVarSampOrderBy
- PollRankVarianceOrderBy

#### PollType
Type of poll (AP, Coaches Poll, etc.).

**Related Types:**
- PollTypeBoolExp
- PollTypeOrderBy
- PollTypeSelectColumn

#### Ratings
Team ratings and rankings.

**Related Types:**
- ratings
- ratingsBoolExp
- ratingsOrderBy
- ratingsSelectColumn

### Utility Types

#### General Utility Types
- Position
- PositionBoolExp
- PositionOrderBy
- PositionSelectColumn
- Conference
- ConferenceBoolExp
- ConferenceOrderBy
- ConferenceSelectColumn
- Hometown
- HometownAggregate
- HometownAggregateFields
- HometownAvgFields
- HometownBoolExp
- HometownMaxFields
- HometownMinFields
- HometownOrderBy
- HometownSelectColumn
- HometownStddevFields
- HometownStddevPopFields
- HometownStddevSampFields
- HometownSumFields
- HometownVarPopFields
- HometownVarSampFields
- HometownVarianceFields
- LinesProvider
- LinesProviderAggregate
- LinesProviderAggregateFields
- LinesProviderAvgFields
- LinesProviderBoolExp
- LinesProviderMaxFields
- LinesProviderMinFields
- LinesProviderOrderBy
- LinesProviderSelectColumn
- LinesProviderStddevFields
- LinesProviderStddevPopFields
- LinesProviderStddevSampFields
- LinesProviderSumFields
- LinesProviderVarPopFields
- LinesProviderVarSampFields
- LinesProviderVarianceFields
- PlayerStatCategory
- PlayerStatCategoryAggregate
- PlayerStatCategoryAggregateFields
- PlayerStatCategoryBoolExp
- PlayerStatCategoryMaxFields
- PlayerStatCategoryMinFields
- PlayerStatCategoryOrderBy
- PlayerStatCategorySelectColumn
- PlayerStatType
- PlayerStatTypeAggregate
- PlayerStatTypeAggregateFields
- PlayerStatTypeBoolExp
- PlayerStatTypeMaxFields
- PlayerStatTypeMinFields
- PlayerStatTypeOrderBy
- PlayerStatTypeSelectColumn
- Transfer
- TransferBoolExp
- TransferOrderBy
- TransferSelectColumn

#### Comparison & Filter Types
- BigintComparisonExp
- BooleanComparisonExp
- DivisionComparisonExp
- FloatComparisonExp
- GameStatusComparisonExp
- HomeAwayComparisonExp
- IntComparisonExp
- MediaTypeComparisonExp
- NumericComparisonExp
- PlayerAdjustedMetricTypeComparisonExp
- RecruitTypeComparisonExp
- SeasonTypeComparisonExp
- SmallintArrayComparisonExp
- SmallintComparisonExp
- StringArrayComparisonExp
- StringComparisonExp
- TimestampComparisonExp
- TimestamptzComparisonExp

#### Primitive Types
- Boolean
- Float
- Int
- String
- bigint
- division
- home_away
- numeric
- smallint
- timestamp
- timestamptz

#### Ordering
- OrderBy (enum for ASC/DESC ordering)

---

## Queries
AdjustedPlayerMetrics
AdjustedPlayerMetricsAggregate
AdjustedPlayerMetricsAggregateBoolExp
AdjustedPlayerMetricsAggregateFields
AdjustedPlayerMetricsAggregateOrderBy
AdjustedPlayerMetricsAvgFields
AdjustedPlayerMetricsAvgOrderBy
AdjustedPlayerMetricsBoolExp
AdjustedPlayerMetricsMaxFields
AdjustedPlayerMetricsMaxOrderBy
AdjustedPlayerMetricsMinFields
AdjustedPlayerMetricsMinOrderBy
AdjustedPlayerMetricsOrderBy
AdjustedPlayerMetricsSelectColumn
AdjustedPlayerMetricsStddevFields
AdjustedPlayerMetricsStddevOrderBy
AdjustedPlayerMetricsStddevPopFields
AdjustedPlayerMetricsStddevPopOrderBy
AdjustedPlayerMetricsStddevSampFields
AdjustedPlayerMetricsStddevSampOrderBy
AdjustedPlayerMetricsSumFields
AdjustedPlayerMetricsSumOrderBy
AdjustedPlayerMetricsVarPopFields
AdjustedPlayerMetricsVarPopOrderBy
AdjustedPlayerMetricsVarSampFields
AdjustedPlayerMetricsVarSampOrderBy
AdjustedPlayerMetricsVarianceFields
AdjustedPlayerMetricsVarianceOrderBy
AdjustedTeamMetrics
AdjustedTeamMetricsAggregate
AdjustedTeamMetricsAggregateFields
AdjustedTeamMetricsAvgFields
AdjustedTeamMetricsBoolExp
AdjustedTeamMetricsMaxFields
AdjustedTeamMetricsMinFields
AdjustedTeamMetricsOrderBy
AdjustedTeamMetricsSelectColumn
AdjustedTeamMetricsStddevFields
AdjustedTeamMetricsStddevPopFields
AdjustedTeamMetricsStddevSampFields
AdjustedTeamMetricsSumFields
AdjustedTeamMetricsVarPopFields
AdjustedTeamMetricsVarSampFields
AdjustedTeamMetricsVarianceFields
Athlete
AthleteAggregate
AthleteAggregateBoolExp
AthleteAggregateFields
AthleteAggregateOrderBy
AthleteAvgFields
AthleteAvgOrderBy
AthleteBoolExp
AthleteMaxFields
AthleteMaxOrderBy
AthleteMinFields
AthleteMinOrderBy
AthleteOrderBy
AthleteSelectColumn
AthleteStddevFields
AthleteStddevOrderBy
AthleteStddevPopFields
AthleteStddevPopOrderBy
AthleteStddevSampFields
AthleteStddevSampOrderBy
AthleteSumFields
AthleteSumOrderBy
AthleteTeam
AthleteTeamAggregate
AthleteTeamAggregateBoolExp
AthleteTeamAggregateFields
AthleteTeamAggregateOrderBy
AthleteTeamAvgFields
AthleteTeamAvgOrderBy
AthleteTeamBoolExp
AthleteTeamMaxFields
AthleteTeamMaxOrderBy
AthleteTeamMinFields
AthleteTeamMinOrderBy
AthleteTeamOrderBy
AthleteTeamSelectColumn
AthleteTeamStddevFields
AthleteTeamStddevOrderBy
AthleteTeamStddevPopFields
AthleteTeamStddevPopOrderBy
AthleteTeamStddevSampFields
AthleteTeamStddevSampOrderBy
AthleteTeamSumFields
AthleteTeamSumOrderBy
AthleteTeamVarPopFields
AthleteTeamVarPopOrderBy
AthleteTeamVarSampFields
AthleteTeamVarSampOrderBy
AthleteTeamVarianceFields
AthleteTeamVarianceOrderBy
AthleteVarPopFields
AthleteVarPopOrderBy
AthleteVarSampFields
AthleteVarSampOrderBy
AthleteVarianceFields
AthleteVarianceOrderBy
BigintComparisonExp
Boolean
BooleanComparisonExp
Calendar
CalendarBoolExp
CalendarOrderBy
CalendarSelectColumn
Coach
CoachAggregate
CoachAggregateFields
CoachAvgFields
CoachBoolExp
CoachMaxFields
CoachMinFields
CoachOrderBy
CoachSeason
CoachSeasonAggregate
CoachSeasonAggregateBoolExp
CoachSeasonAggregateFields
CoachSeasonAggregateOrderBy
CoachSeasonAvgFields
CoachSeasonAvgOrderBy
CoachSeasonBoolExp
CoachSeasonMaxFields
CoachSeasonMaxOrderBy
CoachSeasonMinFields
CoachSeasonMinOrderBy
CoachSeasonOrderBy
CoachSeasonSelectColumn
CoachSeasonStddevFields
CoachSeasonStddevOrderBy
CoachSeasonStddevPopFields
CoachSeasonStddevPopOrderBy
CoachSeasonStddevSampFields
CoachSeasonStddevSampOrderBy
CoachSeasonSumFields
CoachSeasonSumOrderBy
CoachSeasonVarPopFields
CoachSeasonVarPopOrderBy
CoachSeasonVarSampFields
CoachSeasonVarSampOrderBy
CoachSeasonVarianceFields
CoachSeasonVarianceOrderBy
CoachSelectColumn
CoachStddevFields
CoachStddevPopFields
CoachStddevSampFields
CoachSumFields
CoachVarPopFields
CoachVarSampFields
CoachVarianceFields
Conference
ConferenceBoolExp
ConferenceOrderBy
ConferenceSelectColumn
DivisionComparisonExp
DraftPicks
DraftPicksAggregate
DraftPicksAggregateBoolExp
DraftPicksAggregateFields
DraftPicksAggregateOrderBy
DraftPicksAvgFields
DraftPicksAvgOrderBy
DraftPicksBoolExp
DraftPicksMaxFields
DraftPicksMaxOrderBy
DraftPicksMinFields
DraftPicksMinOrderBy
DraftPicksOrderBy
DraftPicksSelectColumn
DraftPicksStddevFields
DraftPicksStddevOrderBy
DraftPicksStddevPopFields
DraftPicksStddevPopOrderBy
DraftPicksStddevSampFields
DraftPicksStddevSampOrderBy
DraftPicksSumFields
DraftPicksSumOrderBy
DraftPicksVarPopFields
DraftPicksVarPopOrderBy
DraftPicksVarSampFields
DraftPicksVarSampOrderBy
DraftPicksVarianceFields
DraftPicksVarianceOrderBy
DraftPosition
DraftPositionBoolExp
DraftPositionOrderBy
DraftPositionSelectColumn
DraftTeam
DraftTeamBoolExp
DraftTeamOrderBy
DraftTeamSelectColumn
Float
FloatComparisonExp
GameLines
GameLinesAggregate
GameLinesAggregateBoolExp
GameLinesAggregateFields
GameLinesAggregateOrderBy
GameLinesAvgFields
GameLinesAvgOrderBy
GameLinesBoolExp
GameLinesMaxFields
GameLinesMaxOrderBy
GameLinesMinFields
GameLinesMinOrderBy
GameLinesOrderBy
GameLinesSelectColumn
GameLinesStddevFields
GameLinesStddevOrderBy
GameLinesStddevPopFields
GameLinesStddevPopOrderBy
GameLinesStddevSampFields
GameLinesStddevSampOrderBy
GameLinesSumFields
GameLinesSumOrderBy
GameLinesVarPopFields
GameLinesVarPopOrderBy
GameLinesVarSampFields
GameLinesVarSampOrderBy
GameLinesVarianceFields
GameLinesVarianceOrderBy
GameMedia
GameMediaAggregateOrderBy
GameMediaBoolExp
GameMediaMaxOrderBy
GameMediaMinOrderBy
GameMediaOrderBy
GameMediaSelectColumn
GamePlayerStat
GamePlayerStatAggregate
GamePlayerStatAggregateBoolExp
GamePlayerStatAggregateFields
GamePlayerStatAggregateOrderBy
GamePlayerStatAvgFields
GamePlayerStatAvgOrderBy
GamePlayerStatBoolExp
GamePlayerStatMaxFields
GamePlayerStatMaxOrderBy
GamePlayerStatMinFields
GamePlayerStatMinOrderBy
GamePlayerStatOrderBy
GamePlayerStatSelectColumn
GamePlayerStatStddevFields
GamePlayerStatStddevOrderBy
GamePlayerStatStddevPopFields
GamePlayerStatStddevPopOrderBy
GamePlayerStatStddevSampFields
GamePlayerStatStddevSampOrderBy
GamePlayerStatSumFields
GamePlayerStatSumOrderBy
GamePlayerStatVarPopFields
GamePlayerStatVarPopOrderBy
GamePlayerStatVarSampFields
GamePlayerStatVarSampOrderBy
GamePlayerStatVarianceFields
GamePlayerStatVarianceOrderBy
GameStatusComparisonExp
GameTeam
GameTeamBoolExp
GameTeamOrderBy
GameTeamSelectColumn
GameWeather
GameWeatherBoolExp
GameWeatherOrderBy
GameWeatherSelectColumn
HomeAwayComparisonExp
Hometown
HometownAggregate
HometownAggregateFields
HometownAvgFields
HometownBoolExp
HometownMaxFields
HometownMinFields
HometownOrderBy
HometownSelectColumn
HometownStddevFields
HometownStddevPopFields
HometownStddevSampFields
HometownSumFields
HometownVarPopFields
HometownVarSampFields
HometownVarianceFields
Int
IntComparisonExp
LinesProvider
LinesProviderAggregate
LinesProviderAggregateFields
LinesProviderAvgFields
LinesProviderBoolExp
LinesProviderMaxFields
LinesProviderMinFields
LinesProviderOrderBy
LinesProviderSelectColumn
LinesProviderStddevFields
LinesProviderStddevPopFields
LinesProviderStddevSampFields
LinesProviderSumFields
LinesProviderVarPopFields
LinesProviderVarSampFields
LinesProviderVarianceFields
MediaTypeComparisonExp
NumericComparisonExp
OrderBy
PlayerAdjustedMetricTypeComparisonExp
PlayerStatCategory
PlayerStatCategoryAggregate
PlayerStatCategoryAggregateFields
PlayerStatCategoryBoolExp
PlayerStatCategoryMaxFields
PlayerStatCategoryMinFields
PlayerStatCategoryOrderBy
PlayerStatCategorySelectColumn
PlayerStatType
PlayerStatTypeAggregate
PlayerStatTypeAggregateFields
PlayerStatTypeBoolExp
PlayerStatTypeMaxFields
PlayerStatTypeMinFields
PlayerStatTypeOrderBy
PlayerStatTypeSelectColumn
Poll
PollAggregateOrderBy
PollAvgOrderBy
PollBoolExp
PollMaxOrderBy
PollMinOrderBy
PollOrderBy
PollRank
PollRankAggregateOrderBy
PollRankAvgOrderBy
PollRankBoolExp
PollRankMaxOrderBy
PollRankMinOrderBy
PollRankOrderBy
PollRankSelectColumn
PollRankStddevOrderBy
PollRankStddevPopOrderBy
PollRankStddevSampOrderBy
PollRankSumOrderBy
PollRankVarPopOrderBy
PollRankVarSampOrderBy
PollRankVarianceOrderBy
PollSelectColumn
PollStddevOrderBy
PollStddevPopOrderBy
PollStddevSampOrderBy
PollSumOrderBy
PollType
PollTypeBoolExp
PollTypeOrderBy
PollTypeSelectColumn
PollVarPopOrderBy
PollVarSampOrderBy
PollVarianceOrderBy
Position
PositionBoolExp
PositionOrderBy
PositionSelectColumn
Recruit
RecruitAggregate
RecruitAggregateBoolExp
RecruitAggregateFields
RecruitAggregateOrderBy
RecruitAvgFields
RecruitAvgOrderBy
RecruitBoolExp
RecruitMaxFields
RecruitMaxOrderBy
RecruitMinFields
RecruitMinOrderBy
RecruitOrderBy
RecruitPosition
RecruitPositionAggregate
RecruitPositionAggregateFields
RecruitPositionAvgFields
RecruitPositionBoolExp
RecruitPositionMaxFields
RecruitPositionMinFields
RecruitPositionOrderBy
RecruitPositionSelectColumn
RecruitPositionStddevFields
RecruitPositionStddevPopFields
RecruitPositionStddevSampFields
RecruitPositionSumFields
RecruitPositionVarPopFields
RecruitPositionVarSampFields
RecruitPositionVarianceFields
RecruitSchool
RecruitSchoolAggregate
RecruitSchoolAggregateFields
RecruitSchoolAvgFields
RecruitSchoolBoolExp
RecruitSchoolMaxFields
RecruitSchoolMinFields
RecruitSchoolOrderBy
RecruitSchoolSelectColumn
RecruitSchoolStddevFields
RecruitSchoolStddevPopFields
RecruitSchoolStddevSampFields
RecruitSchoolSumFields
RecruitSchoolVarPopFields
RecruitSchoolVarSampFields
RecruitSchoolVarianceFields
RecruitSelectColumn
RecruitStddevFields
RecruitStddevOrderBy
RecruitStddevPopFields
RecruitStddevPopOrderBy
RecruitStddevSampFields
RecruitStddevSampOrderBy
RecruitSumFields
RecruitSumOrderBy
RecruitTypeComparisonExp
RecruitVarPopFields
RecruitVarPopOrderBy
RecruitVarSampFields
RecruitVarSampOrderBy
RecruitVarianceFields
RecruitVarianceOrderBy
RecruitingTeam
RecruitingTeamAggregate
RecruitingTeamAggregateFields
RecruitingTeamAvgFields
RecruitingTeamBoolExp
RecruitingTeamMaxFields
RecruitingTeamMinFields
RecruitingTeamOrderBy
RecruitingTeamSelectColumn
RecruitingTeamStddevFields
RecruitingTeamStddevPopFields
RecruitingTeamStddevSampFields
RecruitingTeamSumFields
RecruitingTeamVarPopFields
RecruitingTeamVarSampFields
RecruitingTeamVarianceFields
Scoreboard
ScoreboardBoolExp
ScoreboardOrderBy
ScoreboardSelectColumn
SeasonTypeComparisonExp
SmallintArrayComparisonExp
SmallintComparisonExp
String
StringArrayComparisonExp
StringComparisonExp
TeamTalent
TeamTalentAggregate
TeamTalentAggregateFields
TeamTalentAvgFields
TeamTalentBoolExp
TeamTalentMaxFields
TeamTalentMinFields
TeamTalentOrderBy
TeamTalentSelectColumn
TeamTalentStddevFields
TeamTalentStddevPopFields
TeamTalentStddevSampFields
TeamTalentSumFields
TeamTalentVarPopFields
TeamTalentVarSampFields
TeamTalentVarianceFields
TimestampComparisonExp
TimestamptzComparisonExp
Transfer
TransferBoolExp
TransferOrderBy
TransferSelectColumn
WeatherCondition
WeatherConditionBoolExp
WeatherConditionOrderBy
WeatherConditionSelectColumn
adjustedPlayerMetricsAggregateBoolExpCount
athleteAggregateBoolExpCount
athleteTeamAggregateBoolExpCount
bigint
coachSeasonAggregateBoolExpCount
currentTeams
currentTeamsAggregate
currentTeamsAggregateFields
currentTeamsAvgFields
currentTeamsBoolExp
currentTeamsMaxFields
currentTeamsMinFields
currentTeamsOrderBy
currentTeamsSelectColumn
currentTeamsStddevFields
currentTeamsStddevPopFields
currentTeamsStddevSampFields
currentTeamsSumFields
currentTeamsVarPopFields
currentTeamsVarSampFields
currentTeamsVarianceFields
division
draftPicksAggregateBoolExpCount
game
gameAggregate
gameAggregateFields
gameAvgFields
gameBoolExp
gameLinesAggregateBoolExpCount
gameMaxFields
gameMinFields
gameOrderBy
gamePlayerStatAggregateBoolExpCount
gameSelectColumn
gameStddevFields
gameStddevPopFields
gameStddevSampFields
gameSumFields
gameVarPopFields
gameVarSampFields
gameVarianceFields
game_status
historicalTeam
historicalTeamAggregate
historicalTeamAggregateFields
historicalTeamAvgFields
historicalTeamBoolExp
historicalTeamMaxFields
historicalTeamMinFields
historicalTeamOrderBy
historicalTeamSelectColumn
historicalTeamStddevFields
historicalTeamStddevPopFields
historicalTeamStddevSampFields
historicalTeamSumFields
historicalTeamVarPopFields
historicalTeamVarSampFields
historicalTeamVarianceFields
home_away
media_type
numeric
player_adjusted_metric_type
predictedPoints
predictedPointsAggregate
predictedPointsAggregateFields
predictedPointsAvgFields
predictedPointsBoolExp
predictedPointsMaxFields
predictedPointsMinFields
predictedPointsOrderBy
predictedPointsSelectColumn
predictedPointsStddevFields
predictedPointsStddevPopFields
predictedPointsStddevSampFields
predictedPointsSumFields
predictedPointsVarPopFields
predictedPointsVarSampFields
predictedPointsVarianceFields
ratings
ratingsBoolExp
ratingsOrderBy
ratingsSelectColumn
recruitAggregateBoolExpCount
recruit_type
season_type
smallint
timestamp
timestamptz

---

## Queries

The GraphQL API provides comprehensive query capabilities for accessing college football data. All queries support:
- **Filtering** via `where` clauses
- **Sorting** via `orderBy` parameters
- **Pagination** via `limit` and `offset`
- **Distinct selection** via `distinctOn`
- **Aggregations** for statistical operations

### Common Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `distinctOn` | Array | Select distinct rows based on specified columns |
| `limit` | Int | Maximum number of rows to return |
| `offset` | Int | Number of rows to skip (use with orderBy) |
| `orderBy` | Array | Sort results by one or more columns |
| `where` | Object | Filter conditions for the query |

---

### adjustedPlayerMetrics

**Description:** Query player-adjusted performance metrics.

**Returns:** `[AdjustedPlayerMetrics!]!`

**Arguments:**
- `distinctOn` - [AdjustedPlayerMetricsSelectColumn!] - distinct select on columns
- `limit` - Int - limit the number of rows returned
- `offset` - Int - skip the first n rows. Use only with order_by
- `orderBy` - [AdjustedPlayerMetricsOrderBy!] - sort the rows by one or more columns
- `where` - AdjustedPlayerMetricsBoolExp - filter the rows returned

**Example Query:**
```graphql
query AdjustedPlayerMetrics(
  $distinctOn: [AdjustedPlayerMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedPlayerMetricsOrderBy!],
  $where: AdjustedPlayerMetricsBoolExp
) {
  adjustedPlayerMetrics(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    metricType
    metricValue
    plays
    year
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AdjustedPlayerMetricsOrderBy],
  "where": AdjustedPlayerMetricsBoolExp
}
Response
{
  "data": {
    "adjustedPlayerMetrics": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "metricType": player_adjusted_metric_type,
        "metricValue": numeric,
        "plays": smallint,
        "year": smallint
      }
    ]
  }
}
Queries
adjustedPlayerMetricsAggregate
Description
An aggregate relationship

Response
Returns an AdjustedPlayerMetricsAggregate!

Arguments
Name	Description
distinctOn - [AdjustedPlayerMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedPlayerMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedPlayerMetricsBoolExp	filter the rows returned
Example
Query
query AdjustedPlayerMetricsAggregate(
  $distinctOn: [AdjustedPlayerMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedPlayerMetricsOrderBy!],
  $where: AdjustedPlayerMetricsBoolExp
) {
  adjustedPlayerMetricsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AdjustedPlayerMetricsAvgFieldsFragment
      }
      count
      max {
        ...AdjustedPlayerMetricsMaxFieldsFragment
      }
      min {
        ...AdjustedPlayerMetricsMinFieldsFragment
      }
      stddev {
        ...AdjustedPlayerMetricsStddevFieldsFragment
      }
      stddevPop {
        ...AdjustedPlayerMetricsStddevPopFieldsFragment
      }
      stddevSamp {
        ...AdjustedPlayerMetricsStddevSampFieldsFragment
      }
      sum {
        ...AdjustedPlayerMetricsSumFieldsFragment
      }
      varPop {
        ...AdjustedPlayerMetricsVarPopFieldsFragment
      }
      varSamp {
        ...AdjustedPlayerMetricsVarSampFieldsFragment
      }
      variance {
        ...AdjustedPlayerMetricsVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 987,
  "orderBy": [AdjustedPlayerMetricsOrderBy],
  "where": AdjustedPlayerMetricsBoolExp
}
Response
{
  "data": {
    "adjustedPlayerMetricsAggregate": {
      "aggregate": AdjustedPlayerMetricsAggregateFields,
      "nodes": [AdjustedPlayerMetrics]
    }
  }
}
Queries
adjustedTeamMetrics
Description
fetch data from the table: "adjusted_team_metrics"

Response
Returns [AdjustedTeamMetrics!]!

Arguments
Name	Description
distinctOn - [AdjustedTeamMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedTeamMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedTeamMetricsBoolExp	filter the rows returned
Example
Query
query AdjustedTeamMetrics(
  $distinctOn: [AdjustedTeamMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedTeamMetricsOrderBy!],
  $where: AdjustedTeamMetricsBoolExp
) {
  adjustedTeamMetrics(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    epa
    epaAllowed
    explosiveness
    explosivenessAllowed
    highlightYards
    highlightYardsAllowed
    lineYards
    lineYardsAllowed
    openFieldYards
    openFieldYardsAllowed
    passingDownsSuccess
    passingDownsSuccessAllowed
    passingEpa
    passingEpaAllowed
    rushingEpa
    rushingEpaAllowed
    secondLevelYards
    secondLevelYardsAllowed
    standardDownsSuccess
    standardDownsSuccessAllowed
    success
    successAllowed
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    teamId
    year
  }
}
Variables
{
  "distinctOn": ["epa"],
  "limit": 123,
  "offset": 123,
  "orderBy": [AdjustedTeamMetricsOrderBy],
  "where": AdjustedTeamMetricsBoolExp
}
Response
{
  "data": {
    "adjustedTeamMetrics": [
      {
        "epa": numeric,
        "epaAllowed": numeric,
        "explosiveness": numeric,
        "explosivenessAllowed": numeric,
        "highlightYards": numeric,
        "highlightYardsAllowed": numeric,
        "lineYards": numeric,
        "lineYardsAllowed": numeric,
        "openFieldYards": numeric,
        "openFieldYardsAllowed": numeric,
        "passingDownsSuccess": numeric,
        "passingDownsSuccessAllowed": numeric,
        "passingEpa": numeric,
        "passingEpaAllowed": numeric,
        "rushingEpa": numeric,
        "rushingEpaAllowed": numeric,
        "secondLevelYards": numeric,
        "secondLevelYardsAllowed": numeric,
        "standardDownsSuccess": numeric,
        "standardDownsSuccessAllowed": numeric,
        "success": numeric,
        "successAllowed": numeric,
        "team": currentTeams,
        "teamId": 987,
        "year": smallint
      }
    ]
  }
}
Queries
adjustedTeamMetricsAggregate
Description
fetch aggregated fields from the table: "adjusted_team_metrics"

Response
Returns an AdjustedTeamMetricsAggregate!

Arguments
Name	Description
distinctOn - [AdjustedTeamMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedTeamMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedTeamMetricsBoolExp	filter the rows returned
Example
Query
query AdjustedTeamMetricsAggregate(
  $distinctOn: [AdjustedTeamMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedTeamMetricsOrderBy!],
  $where: AdjustedTeamMetricsBoolExp
) {
  adjustedTeamMetricsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AdjustedTeamMetricsAvgFieldsFragment
      }
      count
      max {
        ...AdjustedTeamMetricsMaxFieldsFragment
      }
      min {
        ...AdjustedTeamMetricsMinFieldsFragment
      }
      stddev {
        ...AdjustedTeamMetricsStddevFieldsFragment
      }
      stddevPop {
        ...AdjustedTeamMetricsStddevPopFieldsFragment
      }
      stddevSamp {
        ...AdjustedTeamMetricsStddevSampFieldsFragment
      }
      sum {
        ...AdjustedTeamMetricsSumFieldsFragment
      }
      varPop {
        ...AdjustedTeamMetricsVarPopFieldsFragment
      }
      varSamp {
        ...AdjustedTeamMetricsVarSampFieldsFragment
      }
      variance {
        ...AdjustedTeamMetricsVarianceFieldsFragment
      }
    }
    nodes {
      epa
      epaAllowed
      explosiveness
      explosivenessAllowed
      highlightYards
      highlightYardsAllowed
      lineYards
      lineYardsAllowed
      openFieldYards
      openFieldYardsAllowed
      passingDownsSuccess
      passingDownsSuccessAllowed
      passingEpa
      passingEpaAllowed
      rushingEpa
      rushingEpaAllowed
      secondLevelYards
      secondLevelYardsAllowed
      standardDownsSuccess
      standardDownsSuccessAllowed
      success
      successAllowed
      team {
        ...currentTeamsFragment
      }
      teamId
      year
    }
  }
}
Variables
{
  "distinctOn": ["epa"],
  "limit": 123,
  "offset": 987,
  "orderBy": [AdjustedTeamMetricsOrderBy],
  "where": AdjustedTeamMetricsBoolExp
}
Response
{
  "data": {
    "adjustedTeamMetricsAggregate": {
      "aggregate": AdjustedTeamMetricsAggregateFields,
      "nodes": [AdjustedTeamMetrics]
    }
  }
}
Queries
athlete
Description
fetch data from the table: "athlete"

Response
Returns [Athlete!]!

Arguments
Name	Description
distinctOn - [AthleteSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteOrderBy!]	sort the rows by one or more columns
where - AthleteBoolExp	filter the rows returned
Example
Query
query Athlete(
  $distinctOn: [AthleteSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteOrderBy!],
  $where: AthleteBoolExp
) {
  athlete(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    adjustedPlayerMetrics {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
    adjustedPlayerMetricsAggregate {
      aggregate {
        ...AdjustedPlayerMetricsAggregateFieldsFragment
      }
      nodes {
        ...AdjustedPlayerMetricsFragment
      }
    }
    athleteTeams {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
    athleteTeamsAggregate {
      aggregate {
        ...AthleteTeamAggregateFieldsFragment
      }
      nodes {
        ...AthleteTeamFragment
      }
    }
    firstName
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    hometownId
    id
    jersey
    lastName
    name
    position {
      abbreviation
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      displayName
      id
      name
    }
    positionId
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    teamId
    weight
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 987,
  "offset": 123,
  "orderBy": [AthleteOrderBy],
  "where": AthleteBoolExp
}
Response
{
  "data": {
    "athlete": [
      {
        "adjustedPlayerMetrics": [AdjustedPlayerMetrics],
        "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregate,
        "athleteTeams": [AthleteTeam],
        "athleteTeamsAggregate": AthleteTeamAggregate,
        "firstName": "xyz789",
        "height": smallint,
        "hometown": Hometown,
        "hometownId": 123,
        "id": bigint,
        "jersey": smallint,
        "lastName": "xyz789",
        "name": "xyz789",
        "position": Position,
        "positionId": smallint,
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate,
        "teamId": 123,
        "weight": smallint
      }
    ]
  }
}
Queries
athleteAggregate
Description
fetch aggregated fields from the table: "athlete"

Response
Returns an AthleteAggregate!

Arguments
Name	Description
distinctOn - [AthleteSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteOrderBy!]	sort the rows by one or more columns
where - AthleteBoolExp	filter the rows returned
Example
Query
query AthleteAggregate(
  $distinctOn: [AthleteSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteOrderBy!],
  $where: AthleteBoolExp
) {
  athleteAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AthleteAvgFieldsFragment
      }
      count
      max {
        ...AthleteMaxFieldsFragment
      }
      min {
        ...AthleteMinFieldsFragment
      }
      stddev {
        ...AthleteStddevFieldsFragment
      }
      stddevPop {
        ...AthleteStddevPopFieldsFragment
      }
      stddevSamp {
        ...AthleteStddevSampFieldsFragment
      }
      sum {
        ...AthleteSumFieldsFragment
      }
      varPop {
        ...AthleteVarPopFieldsFragment
      }
      varSamp {
        ...AthleteVarSampFieldsFragment
      }
      variance {
        ...AthleteVarianceFieldsFragment
      }
    }
    nodes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 123,
  "offset": 987,
  "orderBy": [AthleteOrderBy],
  "where": AthleteBoolExp
}
Response
{
  "data": {
    "athleteAggregate": {
      "aggregate": AthleteAggregateFields,
      "nodes": [Athlete]
    }
  }
}
Queries
athleteByPk
Description
fetch data from the table: "athlete" using primary key columns

Response
Returns an Athlete

Arguments
Name	Description
id - bigint!	
Example
Query
query AthleteByPk($id: bigint!) {
  athleteByPk(id: $id) {
    adjustedPlayerMetrics {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
    adjustedPlayerMetricsAggregate {
      aggregate {
        ...AdjustedPlayerMetricsAggregateFieldsFragment
      }
      nodes {
        ...AdjustedPlayerMetricsFragment
      }
    }
    athleteTeams {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
    athleteTeamsAggregate {
      aggregate {
        ...AthleteTeamAggregateFieldsFragment
      }
      nodes {
        ...AthleteTeamFragment
      }
    }
    firstName
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    hometownId
    id
    jersey
    lastName
    name
    position {
      abbreviation
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      displayName
      id
      name
    }
    positionId
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    teamId
    weight
  }
}
Variables
{"id": bigint}
Response
{
  "data": {
    "athleteByPk": {
      "adjustedPlayerMetrics": [AdjustedPlayerMetrics],
      "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregate,
      "athleteTeams": [AthleteTeam],
      "athleteTeamsAggregate": AthleteTeamAggregate,
      "firstName": "xyz789",
      "height": smallint,
      "hometown": Hometown,
      "hometownId": 987,
      "id": bigint,
      "jersey": smallint,
      "lastName": "xyz789",
      "name": "abc123",
      "position": Position,
      "positionId": smallint,
      "recruits": [Recruit],
      "recruitsAggregate": RecruitAggregate,
      "teamId": 987,
      "weight": smallint
    }
  }
}
Queries
athleteTeam
Description
fetch data from the table: "athlete_team"

Response
Returns [AthleteTeam!]!

Arguments
Name	Description
distinctOn - [AthleteTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteTeamOrderBy!]	sort the rows by one or more columns
where - AthleteTeamBoolExp	filter the rows returned
Example
Query
query AthleteTeam(
  $distinctOn: [AthleteTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteTeamOrderBy!],
  $where: AthleteTeamBoolExp
) {
  athleteTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    endYear
    startYear
    team {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
    teamId
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AthleteTeamOrderBy],
  "where": AthleteTeamBoolExp
}
Response
{
  "data": {
    "athleteTeam": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "endYear": smallint,
        "startYear": smallint,
        "team": historicalTeam,
        "teamId": 987
      }
    ]
  }
}
Queries
athleteTeamAggregate
Description
fetch aggregated fields from the table: "athlete_team"

Response
Returns an AthleteTeamAggregate!

Arguments
Name	Description
distinctOn - [AthleteTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteTeamOrderBy!]	sort the rows by one or more columns
where - AthleteTeamBoolExp	filter the rows returned
Example
Query
query AthleteTeamAggregate(
  $distinctOn: [AthleteTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteTeamOrderBy!],
  $where: AthleteTeamBoolExp
) {
  athleteTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AthleteTeamAvgFieldsFragment
      }
      count
      max {
        ...AthleteTeamMaxFieldsFragment
      }
      min {
        ...AthleteTeamMinFieldsFragment
      }
      stddev {
        ...AthleteTeamStddevFieldsFragment
      }
      stddevPop {
        ...AthleteTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...AthleteTeamStddevSampFieldsFragment
      }
      sum {
        ...AthleteTeamSumFieldsFragment
      }
      varPop {
        ...AthleteTeamVarPopFieldsFragment
      }
      varSamp {
        ...AthleteTeamVarSampFieldsFragment
      }
      variance {
        ...AthleteTeamVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 123,
  "orderBy": [AthleteTeamOrderBy],
  "where": AthleteTeamBoolExp
}
Response
{
  "data": {
    "athleteTeamAggregate": {
      "aggregate": AthleteTeamAggregateFields,
      "nodes": [AthleteTeam]
    }
  }
}
Queries
calendar
Description
fetch data from the table: "calendar"

Response
Returns [Calendar!]!

Arguments
Name	Description
distinctOn - [CalendarSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CalendarOrderBy!]	sort the rows by one or more columns
where - CalendarBoolExp	filter the rows returned
Example
Query
query Calendar(
  $distinctOn: [CalendarSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CalendarOrderBy!],
  $where: CalendarBoolExp
) {
  calendar(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    endDate
    seasonType
    startDate
    week
    year
  }
}
Variables
{
  "distinctOn": ["endDate"],
  "limit": 987,
  "offset": 123,
  "orderBy": [CalendarOrderBy],
  "where": CalendarBoolExp
}
Response
{
  "data": {
    "calendar": [
      {
        "endDate": timestamp,
        "seasonType": season_type,
        "startDate": timestamp,
        "week": smallint,
        "year": smallint
      }
    ]
  }
}
Queries
coach
Description
fetch data from the table: "coach"

Response
Returns [Coach!]!

Arguments
Name	Description
distinctOn - [CoachSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachOrderBy!]	sort the rows by one or more columns
where - CoachBoolExp	filter the rows returned
Example
Query
query Coach(
  $distinctOn: [CoachSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachOrderBy!],
  $where: CoachBoolExp
) {
  coach(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    firstName
    id
    lastName
    seasons {
      coach {
        ...CoachFragment
      }
      games
      losses
      postseasonRank
      preseasonRank
      team {
        ...currentTeamsFragment
      }
      ties
      wins
      year
    }
    seasonsAggregate {
      aggregate {
        ...CoachSeasonAggregateFieldsFragment
      }
      nodes {
        ...CoachSeasonFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 123,
  "offset": 123,
  "orderBy": [CoachOrderBy],
  "where": CoachBoolExp
}
Response
{
  "data": {
    "coach": [
      {
        "firstName": "abc123",
        "id": 123,
        "lastName": "xyz789",
        "seasons": [CoachSeason],
        "seasonsAggregate": CoachSeasonAggregate
      }
    ]
  }
}
Queries
coachAggregate
Description
fetch aggregated fields from the table: "coach"

Response
Returns a CoachAggregate!

Arguments
Name	Description
distinctOn - [CoachSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachOrderBy!]	sort the rows by one or more columns
where - CoachBoolExp	filter the rows returned
Example
Query
query CoachAggregate(
  $distinctOn: [CoachSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachOrderBy!],
  $where: CoachBoolExp
) {
  coachAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...CoachAvgFieldsFragment
      }
      count
      max {
        ...CoachMaxFieldsFragment
      }
      min {
        ...CoachMinFieldsFragment
      }
      stddev {
        ...CoachStddevFieldsFragment
      }
      stddevPop {
        ...CoachStddevPopFieldsFragment
      }
      stddevSamp {
        ...CoachStddevSampFieldsFragment
      }
      sum {
        ...CoachSumFieldsFragment
      }
      varPop {
        ...CoachVarPopFieldsFragment
      }
      varSamp {
        ...CoachVarSampFieldsFragment
      }
      variance {
        ...CoachVarianceFieldsFragment
      }
    }
    nodes {
      firstName
      id
      lastName
      seasons {
        ...CoachSeasonFragment
      }
      seasonsAggregate {
        ...CoachSeasonAggregateFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 987,
  "offset": 987,
  "orderBy": [CoachOrderBy],
  "where": CoachBoolExp
}
Response
{
  "data": {
    "coachAggregate": {
      "aggregate": CoachAggregateFields,
      "nodes": [Coach]
    }
  }
}
Queries
coachSeason
Description
fetch data from the table: "coach_season"

Response
Returns [CoachSeason!]!

Arguments
Name	Description
distinctOn - [CoachSeasonSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachSeasonOrderBy!]	sort the rows by one or more columns
where - CoachSeasonBoolExp	filter the rows returned
Example
Query
query CoachSeason(
  $distinctOn: [CoachSeasonSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachSeasonOrderBy!],
  $where: CoachSeasonBoolExp
) {
  coachSeason(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    coach {
      firstName
      id
      lastName
      seasons {
        ...CoachSeasonFragment
      }
      seasonsAggregate {
        ...CoachSeasonAggregateFragment
      }
    }
    games
    losses
    postseasonRank
    preseasonRank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    ties
    wins
    year
  }
}
Variables
{
  "distinctOn": ["games"],
  "limit": 987,
  "offset": 123,
  "orderBy": [CoachSeasonOrderBy],
  "where": CoachSeasonBoolExp
}
Response
{
  "data": {
    "coachSeason": [
      {
        "coach": Coach,
        "games": smallint,
        "losses": smallint,
        "postseasonRank": smallint,
        "preseasonRank": smallint,
        "team": currentTeams,
        "ties": smallint,
        "wins": smallint,
        "year": smallint
      }
    ]
  }
}
Queries
coachSeasonAggregate
Description
fetch aggregated fields from the table: "coach_season"

Response
Returns a CoachSeasonAggregate!

Arguments
Name	Description
distinctOn - [CoachSeasonSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachSeasonOrderBy!]	sort the rows by one or more columns
where - CoachSeasonBoolExp	filter the rows returned
Example
Query
query CoachSeasonAggregate(
  $distinctOn: [CoachSeasonSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachSeasonOrderBy!],
  $where: CoachSeasonBoolExp
) {
  coachSeasonAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...CoachSeasonAvgFieldsFragment
      }
      count
      max {
        ...CoachSeasonMaxFieldsFragment
      }
      min {
        ...CoachSeasonMinFieldsFragment
      }
      stddev {
        ...CoachSeasonStddevFieldsFragment
      }
      stddevPop {
        ...CoachSeasonStddevPopFieldsFragment
      }
      stddevSamp {
        ...CoachSeasonStddevSampFieldsFragment
      }
      sum {
        ...CoachSeasonSumFieldsFragment
      }
      varPop {
        ...CoachSeasonVarPopFieldsFragment
      }
      varSamp {
        ...CoachSeasonVarSampFieldsFragment
      }
      variance {
        ...CoachSeasonVarianceFieldsFragment
      }
    }
    nodes {
      coach {
        ...CoachFragment
      }
      games
      losses
      postseasonRank
      preseasonRank
      team {
        ...currentTeamsFragment
      }
      ties
      wins
      year
    }
  }
}
Variables
{
  "distinctOn": ["games"],
  "limit": 987,
  "offset": 987,
  "orderBy": [CoachSeasonOrderBy],
  "where": CoachSeasonBoolExp
}
Response
{
  "data": {
    "coachSeasonAggregate": {
      "aggregate": CoachSeasonAggregateFields,
      "nodes": [CoachSeason]
    }
  }
}
Queries
conference
Description
fetch data from the table: "conference"

Response
Returns [Conference!]!

Arguments
Name	Description
distinctOn - [ConferenceSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ConferenceOrderBy!]	sort the rows by one or more columns
where - ConferenceBoolExp	filter the rows returned
Example
Query
query Conference(
  $distinctOn: [ConferenceSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ConferenceOrderBy!],
  $where: ConferenceBoolExp
) {
  conference(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    division
    id
    name
    shortName
    srName
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [ConferenceOrderBy],
  "where": ConferenceBoolExp
}
Response
{
  "data": {
    "conference": [
      {
        "abbreviation": "abc123",
        "division": division,
        "id": smallint,
        "name": "xyz789",
        "shortName": "xyz789",
        "srName": "abc123"
      }
    ]
  }
}
Queries
currentTeams
Description
fetch data from the table: "current_conferences"

Response
Returns [currentTeams!]!

Arguments
Name	Description
distinctOn - [currentTeamsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [currentTeamsOrderBy!]	sort the rows by one or more columns
where - currentTeamsBoolExp	filter the rows returned
Example
Query
query CurrentTeams(
  $distinctOn: [currentTeamsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [currentTeamsOrderBy!],
  $where: currentTeamsBoolExp
) {
  currentTeams(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    classification
    conference
    conferenceId
    division
    school
    teamId
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [currentTeamsOrderBy],
  "where": currentTeamsBoolExp
}
Response
{
  "data": {
    "currentTeams": [
      {
        "abbreviation": "abc123",
        "classification": division,
        "conference": "xyz789",
        "conferenceId": smallint,
        "division": "xyz789",
        "school": "xyz789",
        "teamId": 123
      }
    ]
  }
}
Queries
currentTeamsAggregate
Description
fetch aggregated fields from the table: "current_conferences"

Response
Returns a currentTeamsAggregate!

Arguments
Name	Description
distinctOn - [currentTeamsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [currentTeamsOrderBy!]	sort the rows by one or more columns
where - currentTeamsBoolExp	filter the rows returned
Example
Query
query CurrentTeamsAggregate(
  $distinctOn: [currentTeamsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [currentTeamsOrderBy!],
  $where: currentTeamsBoolExp
) {
  currentTeamsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...currentTeamsAvgFieldsFragment
      }
      count
      max {
        ...currentTeamsMaxFieldsFragment
      }
      min {
        ...currentTeamsMinFieldsFragment
      }
      stddev {
        ...currentTeamsStddevFieldsFragment
      }
      stddevPop {
        ...currentTeamsStddevPopFieldsFragment
      }
      stddevSamp {
        ...currentTeamsStddevSampFieldsFragment
      }
      sum {
        ...currentTeamsSumFieldsFragment
      }
      varPop {
        ...currentTeamsVarPopFieldsFragment
      }
      varSamp {
        ...currentTeamsVarSampFieldsFragment
      }
      variance {
        ...currentTeamsVarianceFieldsFragment
      }
    }
    nodes {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 987,
  "orderBy": [currentTeamsOrderBy],
  "where": currentTeamsBoolExp
}
Response
{
  "data": {
    "currentTeamsAggregate": {
      "aggregate": currentTeamsAggregateFields,
      "nodes": [currentTeams]
    }
  }
}
Queries
draftPicks
Description
fetch data from the table: "draft_picks"

Response
Returns [DraftPicks!]!

Arguments
Name	Description
distinctOn - [DraftPicksSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftPicksOrderBy!]	sort the rows by one or more columns
where - DraftPicksBoolExp	filter the rows returned
Example
Query
query DraftPicks(
  $distinctOn: [DraftPicksSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftPicksOrderBy!],
  $where: DraftPicksBoolExp
) {
  draftPicks(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    collegeAthleteRecord {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    collegeId
    collegeTeam {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
    collegeTeamId
    draftTeam {
      displayName
      id
      location
      logo
      mascot
      nickname
      picks {
        ...DraftPicksFragment
      }
      picksAggregate {
        ...DraftPicksAggregateFragment
      }
      shortDisplayName
    }
    grade
    height
    name
    nflTeamId
    overall
    overallRank
    pick
    position {
      abbreviation
      id
      name
    }
    positionId
    positionRank
    round
    weight
    year
  }
}
Variables
{
  "distinctOn": ["collegeId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [DraftPicksOrderBy],
  "where": DraftPicksBoolExp
}
Response
{
  "data": {
    "draftPicks": [
      {
        "collegeAthleteRecord": Athlete,
        "collegeId": 123,
        "collegeTeam": historicalTeam,
        "collegeTeamId": 987,
        "draftTeam": DraftTeam,
        "grade": smallint,
        "height": smallint,
        "name": "abc123",
        "nflTeamId": smallint,
        "overall": smallint,
        "overallRank": smallint,
        "pick": smallint,
        "position": DraftPosition,
        "positionId": smallint,
        "positionRank": smallint,
        "round": smallint,
        "weight": smallint,
        "year": smallint
      }
    ]
  }
}
Queries
draftPosition
Description
fetch data from the table: "draft_position"

Response
Returns [DraftPosition!]!

Arguments
Name	Description
distinctOn - [DraftPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftPositionOrderBy!]	sort the rows by one or more columns
where - DraftPositionBoolExp	filter the rows returned
Example
Query
query DraftPosition(
  $distinctOn: [DraftPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftPositionOrderBy!],
  $where: DraftPositionBoolExp
) {
  draftPosition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    id
    name
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 123,
  "orderBy": [DraftPositionOrderBy],
  "where": DraftPositionBoolExp
}
Response
{
  "data": {
    "draftPosition": [
      {
        "abbreviation": "abc123",
        "id": smallint,
        "name": "abc123"
      }
    ]
  }
}
Queries
draftTeam
Description
fetch data from the table: "draft_team"

Response
Returns [DraftTeam!]!

Arguments
Name	Description
distinctOn - [DraftTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftTeamOrderBy!]	sort the rows by one or more columns
where - DraftTeamBoolExp	filter the rows returned
Example
Query
query DraftTeam(
  $distinctOn: [DraftTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftTeamOrderBy!],
  $where: DraftTeamBoolExp
) {
  draftTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    displayName
    id
    location
    logo
    mascot
    nickname
    picks {
      collegeAthleteRecord {
        ...AthleteFragment
      }
      collegeId
      collegeTeam {
        ...historicalTeamFragment
      }
      collegeTeamId
      draftTeam {
        ...DraftTeamFragment
      }
      grade
      height
      name
      nflTeamId
      overall
      overallRank
      pick
      position {
        ...DraftPositionFragment
      }
      positionId
      positionRank
      round
      weight
      year
    }
    picksAggregate {
      aggregate {
        ...DraftPicksAggregateFieldsFragment
      }
      nodes {
        ...DraftPicksFragment
      }
    }
    shortDisplayName
  }
}
Variables
{
  "distinctOn": ["displayName"],
  "limit": 123,
  "offset": 123,
  "orderBy": [DraftTeamOrderBy],
  "where": DraftTeamBoolExp
}
Response
{
  "data": {
    "draftTeam": [
      {
        "displayName": "xyz789",
        "id": smallint,
        "location": "abc123",
        "logo": "xyz789",
        "mascot": "abc123",
        "nickname": "abc123",
        "picks": [DraftPicks],
        "picksAggregate": DraftPicksAggregate,
        "shortDisplayName": "xyz789"
      }
    ]
  }
}
Queries
game
Description
fetch data from the table: "game_info"

Response
Returns [game!]!

Arguments
Name	Description
distinctOn - [gameSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [gameOrderBy!]	sort the rows by one or more columns
where - gameBoolExp	filter the rows returned
Example
Query
query Game(
  $distinctOn: [gameSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [gameOrderBy!],
  $where: gameBoolExp
) {
  game(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    attendance
    awayClassification
    awayConference
    awayConferenceId
    awayConferenceInfo {
      abbreviation
      division
      id
      name
      shortName
      srName
    }
    awayEndElo
    awayLineScores
    awayPoints
    awayPostgameWinProb
    awayStartElo
    awayTeam
    awayTeamId
    awayTeamInfo {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    conferenceGame
    excitement
    homeClassification
    homeConference
    homeConferenceId
    homeConferenceInfo {
      abbreviation
      division
      id
      name
      shortName
      srName
    }
    homeEndElo
    homeLineScores
    homePoints
    homePostgameWinProb
    homeStartElo
    homeTeam
    homeTeamId
    homeTeamInfo {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    id
    lines {
      gameId
      linesProviderId
      moneylineAway
      moneylineHome
      overUnder
      overUnderOpen
      provider {
        ...LinesProviderFragment
      }
      spread
      spreadOpen
    }
    linesAggregate {
      aggregate {
        ...GameLinesAggregateFieldsFragment
      }
      nodes {
        ...GameLinesFragment
      }
    }
    mediaInfo {
      mediaType
      name
    }
    neutralSite
    notes
    season
    seasonType
    startDate
    startTimeTbd
    status
    venueId
    weather {
      condition {
        ...WeatherConditionFragment
      }
      dewpoint
      gameId
      humidity
      precipitation
      pressure
      snowfall
      temperature
      weatherConditionCode
      windDirection
      windGust
      windSpeed
    }
    week
  }
}
Variables
{
  "distinctOn": ["attendance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [gameOrderBy],
  "where": gameBoolExp
}
Response
{
  "data": {
    "game": [
      {
        "attendance": 987,
        "awayClassification": division,
        "awayConference": "abc123",
        "awayConferenceId": smallint,
        "awayConferenceInfo": Conference,
        "awayEndElo": 123,
        "awayLineScores": [smallint],
        "awayPoints": smallint,
        "awayPostgameWinProb": numeric,
        "awayStartElo": 123,
        "awayTeam": "xyz789",
        "awayTeamId": 123,
        "awayTeamInfo": currentTeams,
        "conferenceGame": true,
        "excitement": numeric,
        "homeClassification": division,
        "homeConference": "abc123",
        "homeConferenceId": smallint,
        "homeConferenceInfo": Conference,
        "homeEndElo": 987,
        "homeLineScores": [smallint],
        "homePoints": smallint,
        "homePostgameWinProb": numeric,
        "homeStartElo": 987,
        "homeTeam": "abc123",
        "homeTeamId": 123,
        "homeTeamInfo": currentTeams,
        "id": 987,
        "lines": [GameLines],
        "linesAggregate": GameLinesAggregate,
        "mediaInfo": [GameMedia],
        "neutralSite": true,
        "notes": "abc123",
        "season": smallint,
        "seasonType": season_type,
        "startDate": timestamp,
        "startTimeTbd": true,
        "status": game_status,
        "venueId": 987,
        "weather": GameWeather,
        "week": smallint
      }
    ]
  }
}
Queries
gameAggregate
Description
fetch aggregated fields from the table: "game_info"

Response
Returns a gameAggregate!

Arguments
Name	Description
distinctOn - [gameSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [gameOrderBy!]	sort the rows by one or more columns
where - gameBoolExp	filter the rows returned
Example
Query
query GameAggregate(
  $distinctOn: [gameSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [gameOrderBy!],
  $where: gameBoolExp
) {
  gameAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...gameAvgFieldsFragment
      }
      count
      max {
        ...gameMaxFieldsFragment
      }
      min {
        ...gameMinFieldsFragment
      }
      stddev {
        ...gameStddevFieldsFragment
      }
      stddevPop {
        ...gameStddevPopFieldsFragment
      }
      stddevSamp {
        ...gameStddevSampFieldsFragment
      }
      sum {
        ...gameSumFieldsFragment
      }
      varPop {
        ...gameVarPopFieldsFragment
      }
      varSamp {
        ...gameVarSampFieldsFragment
      }
      variance {
        ...gameVarianceFieldsFragment
      }
    }
    nodes {
      attendance
      awayClassification
      awayConference
      awayConferenceId
      awayConferenceInfo {
        ...ConferenceFragment
      }
      awayEndElo
      awayLineScores
      awayPoints
      awayPostgameWinProb
      awayStartElo
      awayTeam
      awayTeamId
      awayTeamInfo {
        ...currentTeamsFragment
      }
      conferenceGame
      excitement
      homeClassification
      homeConference
      homeConferenceId
      homeConferenceInfo {
        ...ConferenceFragment
      }
      homeEndElo
      homeLineScores
      homePoints
      homePostgameWinProb
      homeStartElo
      homeTeam
      homeTeamId
      homeTeamInfo {
        ...currentTeamsFragment
      }
      id
      lines {
        ...GameLinesFragment
      }
      linesAggregate {
        ...GameLinesAggregateFragment
      }
      mediaInfo {
        ...GameMediaFragment
      }
      neutralSite
      notes
      season
      seasonType
      startDate
      startTimeTbd
      status
      venueId
      weather {
        ...GameWeatherFragment
      }
      week
    }
  }
}
Variables
{
  "distinctOn": ["attendance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [gameOrderBy],
  "where": gameBoolExp
}
Response
{
  "data": {
    "gameAggregate": {
      "aggregate": gameAggregateFields,
      "nodes": [game]
    }
  }
}
Queries
gameLines
Description
fetch data from the table: "game_lines"

Response
Returns [GameLines!]!

Arguments
Name	Description
distinctOn - [GameLinesSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameLinesOrderBy!]	sort the rows by one or more columns
where - GameLinesBoolExp	filter the rows returned
Example
Query
query GameLines(
  $distinctOn: [GameLinesSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameLinesOrderBy!],
  $where: GameLinesBoolExp
) {
  gameLines(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    gameId
    linesProviderId
    moneylineAway
    moneylineHome
    overUnder
    overUnderOpen
    provider {
      id
      name
    }
    spread
    spreadOpen
  }
}
Variables
{
  "distinctOn": ["gameId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [GameLinesOrderBy],
  "where": GameLinesBoolExp
}
Response
{
  "data": {
    "gameLines": [
      {
        "gameId": 987,
        "linesProviderId": 123,
        "moneylineAway": 123,
        "moneylineHome": 987,
        "overUnder": numeric,
        "overUnderOpen": numeric,
        "provider": LinesProvider,
        "spread": numeric,
        "spreadOpen": numeric
      }
    ]
  }
}
Queries
gameLinesAggregate
Description
fetch aggregated fields from the table: "game_lines"

Response
Returns a GameLinesAggregate!

Arguments
Name	Description
distinctOn - [GameLinesSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameLinesOrderBy!]	sort the rows by one or more columns
where - GameLinesBoolExp	filter the rows returned
Example
Query
query GameLinesAggregate(
  $distinctOn: [GameLinesSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameLinesOrderBy!],
  $where: GameLinesBoolExp
) {
  gameLinesAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...GameLinesAvgFieldsFragment
      }
      count
      max {
        ...GameLinesMaxFieldsFragment
      }
      min {
        ...GameLinesMinFieldsFragment
      }
      stddev {
        ...GameLinesStddevFieldsFragment
      }
      stddevPop {
        ...GameLinesStddevPopFieldsFragment
      }
      stddevSamp {
        ...GameLinesStddevSampFieldsFragment
      }
      sum {
        ...GameLinesSumFieldsFragment
      }
      varPop {
        ...GameLinesVarPopFieldsFragment
      }
      varSamp {
        ...GameLinesVarSampFieldsFragment
      }
      variance {
        ...GameLinesVarianceFieldsFragment
      }
    }
    nodes {
      gameId
      linesProviderId
      moneylineAway
      moneylineHome
      overUnder
      overUnderOpen
      provider {
        ...LinesProviderFragment
      }
      spread
      spreadOpen
    }
  }
}
Variables
{
  "distinctOn": ["gameId"],
  "limit": 987,
  "offset": 123,
  "orderBy": [GameLinesOrderBy],
  "where": GameLinesBoolExp
}
Response
{
  "data": {
    "gameLinesAggregate": {
      "aggregate": GameLinesAggregateFields,
      "nodes": [GameLines]
    }
  }
}
Queries
gameMedia
Description
fetch data from the table: "game_media"

Response
Returns [GameMedia!]!

Arguments
Name	Description
distinctOn - [GameMediaSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameMediaOrderBy!]	sort the rows by one or more columns
where - GameMediaBoolExp	filter the rows returned
Example
Query
query GameMedia(
  $distinctOn: [GameMediaSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameMediaOrderBy!],
  $where: GameMediaBoolExp
) {
  gameMedia(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    mediaType
    name
  }
}
Variables
{
  "distinctOn": ["mediaType"],
  "limit": 987,
  "offset": 123,
  "orderBy": [GameMediaOrderBy],
  "where": GameMediaBoolExp
}
Response
{
  "data": {
    "gameMedia": [
      {
        "mediaType": media_type,
        "name": "xyz789"
      }
    ]
  }
}
Queries
gamePlayerStat
Description
fetch data from the table: "game_player_stat"

Response
Returns [GamePlayerStat!]!

Arguments
Name	Description
distinctOn - [GamePlayerStatSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GamePlayerStatOrderBy!]	sort the rows by one or more columns
where - GamePlayerStatBoolExp	filter the rows returned
Example
Query
query GamePlayerStat(
  $distinctOn: [GamePlayerStatSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GamePlayerStatOrderBy!],
  $where: GamePlayerStatBoolExp
) {
  gamePlayerStat(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    gameTeam {
      endElo
      game {
        ...gameFragment
      }
      gameId
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      homeAway
      lineScores
      points
      startElo
      teamId
      winProb
    }
    gameTeamId
    id
    playerStatCategory {
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      name
    }
    playerStatType {
      name
    }
    stat
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [GamePlayerStatOrderBy],
  "where": GamePlayerStatBoolExp
}
Response
{
  "data": {
    "gamePlayerStat": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "gameTeam": GameTeam,
        "gameTeamId": bigint,
        "id": bigint,
        "playerStatCategory": PlayerStatCategory,
        "playerStatType": PlayerStatType,
        "stat": "xyz789"
      }
    ]
  }
}
Queries
gamePlayerStatAggregate
Description
fetch aggregated fields from the table: "game_player_stat"

Response
Returns a GamePlayerStatAggregate!

Arguments
Name	Description
distinctOn - [GamePlayerStatSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GamePlayerStatOrderBy!]	sort the rows by one or more columns
where - GamePlayerStatBoolExp	filter the rows returned
Example
Query
query GamePlayerStatAggregate(
  $distinctOn: [GamePlayerStatSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GamePlayerStatOrderBy!],
  $where: GamePlayerStatBoolExp
) {
  gamePlayerStatAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...GamePlayerStatAvgFieldsFragment
      }
      count
      max {
        ...GamePlayerStatMaxFieldsFragment
      }
      min {
        ...GamePlayerStatMinFieldsFragment
      }
      stddev {
        ...GamePlayerStatStddevFieldsFragment
      }
      stddevPop {
        ...GamePlayerStatStddevPopFieldsFragment
      }
      stddevSamp {
        ...GamePlayerStatStddevSampFieldsFragment
      }
      sum {
        ...GamePlayerStatSumFieldsFragment
      }
      varPop {
        ...GamePlayerStatVarPopFieldsFragment
      }
      varSamp {
        ...GamePlayerStatVarSampFieldsFragment
      }
      variance {
        ...GamePlayerStatVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 123,
  "orderBy": [GamePlayerStatOrderBy],
  "where": GamePlayerStatBoolExp
}
Response
{
  "data": {
    "gamePlayerStatAggregate": {
      "aggregate": GamePlayerStatAggregateFields,
      "nodes": [GamePlayerStat]
    }
  }
}
Queries
gameTeam
Description
fetch data from the table: "game_team"

Response
Returns [GameTeam!]!

Arguments
Name	Description
distinctOn - [GameTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameTeamOrderBy!]	sort the rows by one or more columns
where - GameTeamBoolExp	filter the rows returned
Example
Query
query GameTeam(
  $distinctOn: [GameTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameTeamOrderBy!],
  $where: GameTeamBoolExp
) {
  gameTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    endElo
    game {
      attendance
      awayClassification
      awayConference
      awayConferenceId
      awayConferenceInfo {
        ...ConferenceFragment
      }
      awayEndElo
      awayLineScores
      awayPoints
      awayPostgameWinProb
      awayStartElo
      awayTeam
      awayTeamId
      awayTeamInfo {
        ...currentTeamsFragment
      }
      conferenceGame
      excitement
      homeClassification
      homeConference
      homeConferenceId
      homeConferenceInfo {
        ...ConferenceFragment
      }
      homeEndElo
      homeLineScores
      homePoints
      homePostgameWinProb
      homeStartElo
      homeTeam
      homeTeamId
      homeTeamInfo {
        ...currentTeamsFragment
      }
      id
      lines {
        ...GameLinesFragment
      }
      linesAggregate {
        ...GameLinesAggregateFragment
      }
      mediaInfo {
        ...GameMediaFragment
      }
      neutralSite
      notes
      season
      seasonType
      startDate
      startTimeTbd
      status
      venueId
      weather {
        ...GameWeatherFragment
      }
      week
    }
    gameId
    gamePlayerStats {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
    gamePlayerStatsAggregate {
      aggregate {
        ...GamePlayerStatAggregateFieldsFragment
      }
      nodes {
        ...GamePlayerStatFragment
      }
    }
    homeAway
    lineScores
    points
    startElo
    teamId
    winProb
  }
}
Variables
{
  "distinctOn": ["endElo"],
  "limit": 123,
  "offset": 123,
  "orderBy": [GameTeamOrderBy],
  "where": GameTeamBoolExp
}
Response
{
  "data": {
    "gameTeam": [
      {
        "endElo": 987,
        "game": game,
        "gameId": 987,
        "gamePlayerStats": [GamePlayerStat],
        "gamePlayerStatsAggregate": GamePlayerStatAggregate,
        "homeAway": home_away,
        "lineScores": [smallint],
        "points": smallint,
        "startElo": 123,
        "teamId": 987,
        "winProb": numeric
      }
    ]
  }
}
Queries
gameWeather
Description
fetch data from the table: "game_weather"

Response
Returns [GameWeather!]!

Arguments
Name	Description
distinctOn - [GameWeatherSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameWeatherOrderBy!]	sort the rows by one or more columns
where - GameWeatherBoolExp	filter the rows returned
Example
Query
query GameWeather(
  $distinctOn: [GameWeatherSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameWeatherOrderBy!],
  $where: GameWeatherBoolExp
) {
  gameWeather(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    condition {
      description
      id
    }
    dewpoint
    gameId
    humidity
    precipitation
    pressure
    snowfall
    temperature
    weatherConditionCode
    windDirection
    windGust
    windSpeed
  }
}
Variables
{
  "distinctOn": ["dewpoint"],
  "limit": 123,
  "offset": 987,
  "orderBy": [GameWeatherOrderBy],
  "where": GameWeatherBoolExp
}
Response
{
  "data": {
    "gameWeather": [
      {
        "condition": WeatherCondition,
        "dewpoint": numeric,
        "gameId": 123,
        "humidity": numeric,
        "precipitation": numeric,
        "pressure": numeric,
        "snowfall": numeric,
        "temperature": numeric,
        "weatherConditionCode": smallint,
        "windDirection": numeric,
        "windGust": numeric,
        "windSpeed": numeric
      }
    ]
  }
}
Queries
historicalTeam
Description
fetch data from the table: "team_info"

Response
Returns [historicalTeam!]!

Arguments
Name	Description
distinctOn - [historicalTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [historicalTeamOrderBy!]	sort the rows by one or more columns
where - historicalTeamBoolExp	filter the rows returned
Example
Query
query HistoricalTeam(
  $distinctOn: [historicalTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [historicalTeamOrderBy!],
  $where: historicalTeamBoolExp
) {
  historicalTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    active
    altColor
    altName
    classification
    color
    conference
    conferenceAbbreviation
    conferenceId
    conferenceShortName
    countryCode
    displayName
    division
    endYear
    id
    images
    mascot
    ncaaName
    nickname
    school
    shortDisplayName
    startYear
    twitter
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 123,
  "orderBy": [historicalTeamOrderBy],
  "where": historicalTeamBoolExp
}
Response
{
  "data": {
    "historicalTeam": [
      {
        "abbreviation": "abc123",
        "active": true,
        "altColor": "abc123",
        "altName": "abc123",
        "classification": division,
        "color": "xyz789",
        "conference": "abc123",
        "conferenceAbbreviation": "xyz789",
        "conferenceId": smallint,
        "conferenceShortName": "xyz789",
        "countryCode": "abc123",
        "displayName": "abc123",
        "division": "abc123",
        "endYear": smallint,
        "id": 123,
        "images": ["abc123"],
        "mascot": "xyz789",
        "ncaaName": "abc123",
        "nickname": "xyz789",
        "school": "xyz789",
        "shortDisplayName": "xyz789",
        "startYear": smallint,
        "twitter": "xyz789"
      }
    ]
  }
}
Queries
historicalTeamAggregate
Description
fetch aggregated fields from the table: "team_info"

Response
Returns a historicalTeamAggregate!

Arguments
Name	Description
distinctOn - [historicalTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [historicalTeamOrderBy!]	sort the rows by one or more columns
where - historicalTeamBoolExp	filter the rows returned
Example
Query
query HistoricalTeamAggregate(
  $distinctOn: [historicalTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [historicalTeamOrderBy!],
  $where: historicalTeamBoolExp
) {
  historicalTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...historicalTeamAvgFieldsFragment
      }
      count
      max {
        ...historicalTeamMaxFieldsFragment
      }
      min {
        ...historicalTeamMinFieldsFragment
      }
      stddev {
        ...historicalTeamStddevFieldsFragment
      }
      stddevPop {
        ...historicalTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...historicalTeamStddevSampFieldsFragment
      }
      sum {
        ...historicalTeamSumFieldsFragment
      }
      varPop {
        ...historicalTeamVarPopFieldsFragment
      }
      varSamp {
        ...historicalTeamVarSampFieldsFragment
      }
      variance {
        ...historicalTeamVarianceFieldsFragment
      }
    }
    nodes {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [historicalTeamOrderBy],
  "where": historicalTeamBoolExp
}
Response
{
  "data": {
    "historicalTeamAggregate": {
      "aggregate": historicalTeamAggregateFields,
      "nodes": [historicalTeam]
    }
  }
}
Queries
hometown
Description
fetch data from the table: "hometown"

Response
Returns [Hometown!]!

Arguments
Name	Description
distinctOn - [HometownSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [HometownOrderBy!]	sort the rows by one or more columns
where - HometownBoolExp	filter the rows returned
Example
Query
query Hometown(
  $distinctOn: [HometownSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [HometownOrderBy!],
  $where: HometownBoolExp
) {
  hometown(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athletes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athletesAggregate {
      aggregate {
        ...AthleteAggregateFieldsFragment
      }
      nodes {
        ...AthleteFragment
      }
    }
    city
    country
    countyFips
    latitude
    longitude
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    state
  }
}
Variables
{
  "distinctOn": ["city"],
  "limit": 987,
  "offset": 987,
  "orderBy": [HometownOrderBy],
  "where": HometownBoolExp
}
Response
{
  "data": {
    "hometown": [
      {
        "athletes": [Athlete],
        "athletesAggregate": AthleteAggregate,
        "city": "xyz789",
        "country": "abc123",
        "countyFips": "abc123",
        "latitude": numeric,
        "longitude": numeric,
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate,
        "state": "xyz789"
      }
    ]
  }
}
Queries
hometownAggregate
Description
fetch aggregated fields from the table: "hometown"

Response
Returns a HometownAggregate!

Arguments
Name	Description
distinctOn - [HometownSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [HometownOrderBy!]	sort the rows by one or more columns
where - HometownBoolExp	filter the rows returned
Example
Query
query HometownAggregate(
  $distinctOn: [HometownSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [HometownOrderBy!],
  $where: HometownBoolExp
) {
  hometownAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...HometownAvgFieldsFragment
      }
      count
      max {
        ...HometownMaxFieldsFragment
      }
      min {
        ...HometownMinFieldsFragment
      }
      stddev {
        ...HometownStddevFieldsFragment
      }
      stddevPop {
        ...HometownStddevPopFieldsFragment
      }
      stddevSamp {
        ...HometownStddevSampFieldsFragment
      }
      sum {
        ...HometownSumFieldsFragment
      }
      varPop {
        ...HometownVarPopFieldsFragment
      }
      varSamp {
        ...HometownVarSampFieldsFragment
      }
      variance {
        ...HometownVarianceFieldsFragment
      }
    }
    nodes {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
  }
}
Variables
{
  "distinctOn": ["city"],
  "limit": 123,
  "offset": 123,
  "orderBy": [HometownOrderBy],
  "where": HometownBoolExp
}
Response
{
  "data": {
    "hometownAggregate": {
      "aggregate": HometownAggregateFields,
      "nodes": [Hometown]
    }
  }
}
Queries
linesProvider
Description
fetch data from the table: "lines_provider"

Response
Returns [LinesProvider!]!

Arguments
Name	Description
distinctOn - [LinesProviderSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [LinesProviderOrderBy!]	sort the rows by one or more columns
where - LinesProviderBoolExp	filter the rows returned
Example
Query
query LinesProvider(
  $distinctOn: [LinesProviderSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [LinesProviderOrderBy!],
  $where: LinesProviderBoolExp
) {
  linesProvider(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    name
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [LinesProviderOrderBy],
  "where": LinesProviderBoolExp
}
Response
{
  "data": {
    "linesProvider": [
      {"id": 123, "name": "xyz789"}
    ]
  }
}
Queries
linesProviderAggregate
Description
fetch aggregated fields from the table: "lines_provider"

Response
Returns a LinesProviderAggregate!

Arguments
Name	Description
distinctOn - [LinesProviderSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [LinesProviderOrderBy!]	sort the rows by one or more columns
where - LinesProviderBoolExp	filter the rows returned
Example
Query
query LinesProviderAggregate(
  $distinctOn: [LinesProviderSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [LinesProviderOrderBy!],
  $where: LinesProviderBoolExp
) {
  linesProviderAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...LinesProviderAvgFieldsFragment
      }
      count
      max {
        ...LinesProviderMaxFieldsFragment
      }
      min {
        ...LinesProviderMinFieldsFragment
      }
      stddev {
        ...LinesProviderStddevFieldsFragment
      }
      stddevPop {
        ...LinesProviderStddevPopFieldsFragment
      }
      stddevSamp {
        ...LinesProviderStddevSampFieldsFragment
      }
      sum {
        ...LinesProviderSumFieldsFragment
      }
      varPop {
        ...LinesProviderVarPopFieldsFragment
      }
      varSamp {
        ...LinesProviderVarSampFieldsFragment
      }
      variance {
        ...LinesProviderVarianceFieldsFragment
      }
    }
    nodes {
      id
      name
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [LinesProviderOrderBy],
  "where": LinesProviderBoolExp
}
Response
{
  "data": {
    "linesProviderAggregate": {
      "aggregate": LinesProviderAggregateFields,
      "nodes": [LinesProvider]
    }
  }
}
Queries
playerStatCategory
Description
fetch data from the table: "player_stat_category"

Response
Returns [PlayerStatCategory!]!

Arguments
Name	Description
distinctOn - [PlayerStatCategorySelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatCategoryOrderBy!]	sort the rows by one or more columns
where - PlayerStatCategoryBoolExp	filter the rows returned
Example
Query
query PlayerStatCategory(
  $distinctOn: [PlayerStatCategorySelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatCategoryOrderBy!],
  $where: PlayerStatCategoryBoolExp
) {
  playerStatCategory(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    gamePlayerStats {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
    gamePlayerStatsAggregate {
      aggregate {
        ...GamePlayerStatAggregateFieldsFragment
      }
      nodes {
        ...GamePlayerStatFragment
      }
    }
    name
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PlayerStatCategoryOrderBy],
  "where": PlayerStatCategoryBoolExp
}
Response
{
  "data": {
    "playerStatCategory": [
      {
        "gamePlayerStats": [GamePlayerStat],
        "gamePlayerStatsAggregate": GamePlayerStatAggregate,
        "name": "abc123"
      }
    ]
  }
}
Queries
playerStatCategoryAggregate
Description
fetch aggregated fields from the table: "player_stat_category"

Response
Returns a PlayerStatCategoryAggregate!

Arguments
Name	Description
distinctOn - [PlayerStatCategorySelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatCategoryOrderBy!]	sort the rows by one or more columns
where - PlayerStatCategoryBoolExp	filter the rows returned
Example
Query
query PlayerStatCategoryAggregate(
  $distinctOn: [PlayerStatCategorySelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatCategoryOrderBy!],
  $where: PlayerStatCategoryBoolExp
) {
  playerStatCategoryAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      count
      max {
        ...PlayerStatCategoryMaxFieldsFragment
      }
      min {
        ...PlayerStatCategoryMinFieldsFragment
      }
    }
    nodes {
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      name
    }
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PlayerStatCategoryOrderBy],
  "where": PlayerStatCategoryBoolExp
}
Response
{
  "data": {
    "playerStatCategoryAggregate": {
      "aggregate": PlayerStatCategoryAggregateFields,
      "nodes": [PlayerStatCategory]
    }
  }
}
Queries
playerStatType
Description
fetch data from the table: "player_stat_type"

Response
Returns [PlayerStatType!]!

Arguments
Name	Description
distinctOn - [PlayerStatTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatTypeOrderBy!]	sort the rows by one or more columns
where - PlayerStatTypeBoolExp	filter the rows returned
Example
Query
query PlayerStatType(
  $distinctOn: [PlayerStatTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatTypeOrderBy!],
  $where: PlayerStatTypeBoolExp
) {
  playerStatType(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    name
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PlayerStatTypeOrderBy],
  "where": PlayerStatTypeBoolExp
}
Response
{
  "data": {
    "playerStatType": [{"name": "abc123"}]
  }
}
Queries
playerStatTypeAggregate
Description
fetch aggregated fields from the table: "player_stat_type"

Response
Returns a PlayerStatTypeAggregate!

Arguments
Name	Description
distinctOn - [PlayerStatTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatTypeOrderBy!]	sort the rows by one or more columns
where - PlayerStatTypeBoolExp	filter the rows returned
Example
Query
query PlayerStatTypeAggregate(
  $distinctOn: [PlayerStatTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatTypeOrderBy!],
  $where: PlayerStatTypeBoolExp
) {
  playerStatTypeAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      count
      max {
        ...PlayerStatTypeMaxFieldsFragment
      }
      min {
        ...PlayerStatTypeMinFieldsFragment
      }
    }
    nodes {
      name
    }
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PlayerStatTypeOrderBy],
  "where": PlayerStatTypeBoolExp
}
Response
{
  "data": {
    "playerStatTypeAggregate": {
      "aggregate": PlayerStatTypeAggregateFields,
      "nodes": [PlayerStatType]
    }
  }
}
Queries
poll
Description
fetch data from the table: "poll"

Response
Returns [Poll!]!

Arguments
Name	Description
distinctOn - [PollSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollOrderBy!]	sort the rows by one or more columns
where - PollBoolExp	filter the rows returned
Example
Query
query Poll(
  $distinctOn: [PollSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollOrderBy!],
  $where: PollBoolExp
) {
  poll(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    pollType {
      abbreviation
      id
      name
      polls {
        ...PollFragment
      }
      shortName
    }
    rankings {
      firstPlaceVotes
      points
      poll {
        ...PollFragment
      }
      rank
      team {
        ...currentTeamsFragment
      }
    }
    season
    seasonType
    week
  }
}
Variables
{
  "distinctOn": ["season"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PollOrderBy],
  "where": PollBoolExp
}
Response
{
  "data": {
    "poll": [
      {
        "pollType": PollType,
        "rankings": [PollRank],
        "season": 123,
        "seasonType": season_type,
        "week": smallint
      }
    ]
  }
}
Queries
pollRank
Description
fetch data from the table: "poll_rank"

Response
Returns [PollRank!]!

Arguments
Name	Description
distinctOn - [PollRankSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollRankOrderBy!]	sort the rows by one or more columns
where - PollRankBoolExp	filter the rows returned
Example
Query
query PollRank(
  $distinctOn: [PollRankSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollRankOrderBy!],
  $where: PollRankBoolExp
) {
  pollRank(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    firstPlaceVotes
    points
    poll {
      pollType {
        ...PollTypeFragment
      }
      rankings {
        ...PollRankFragment
      }
      season
      seasonType
      week
    }
    rank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["firstPlaceVotes"],
  "limit": 123,
  "offset": 987,
  "orderBy": [PollRankOrderBy],
  "where": PollRankBoolExp
}
Response
{
  "data": {
    "pollRank": [
      {
        "firstPlaceVotes": smallint,
        "points": 987,
        "poll": Poll,
        "rank": smallint,
        "team": currentTeams
      }
    ]
  }
}
Queries
pollType
Description
fetch data from the table: "poll_type"

Response
Returns [PollType!]!

Arguments
Name	Description
distinctOn - [PollTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollTypeOrderBy!]	sort the rows by one or more columns
where - PollTypeBoolExp	filter the rows returned
Example
Query
query PollType(
  $distinctOn: [PollTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollTypeOrderBy!],
  $where: PollTypeBoolExp
) {
  pollType(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    id
    name
    polls {
      pollType {
        ...PollTypeFragment
      }
      rankings {
        ...PollRankFragment
      }
      season
      seasonType
      week
    }
    shortName
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PollTypeOrderBy],
  "where": PollTypeBoolExp
}
Response
{
  "data": {
    "pollType": [
      {
        "abbreviation": "abc123",
        "id": 123,
        "name": "xyz789",
        "polls": [Poll],
        "shortName": "xyz789"
      }
    ]
  }
}
Queries
position
Description
fetch data from the table: "position"

Response
Returns [Position!]!

Arguments
Name	Description
distinctOn - [PositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PositionOrderBy!]	sort the rows by one or more columns
where - PositionBoolExp	filter the rows returned
Example
Query
query Position(
  $distinctOn: [PositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PositionOrderBy!],
  $where: PositionBoolExp
) {
  position(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    athletes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athletesAggregate {
      aggregate {
        ...AthleteAggregateFieldsFragment
      }
      nodes {
        ...AthleteFragment
      }
    }
    displayName
    id
    name
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PositionOrderBy],
  "where": PositionBoolExp
}
Response
{
  "data": {
    "position": [
      {
        "abbreviation": "abc123",
        "athletes": [Athlete],
        "athletesAggregate": AthleteAggregate,
        "displayName": "xyz789",
        "id": smallint,
        "name": "abc123"
      }
    ]
  }
}
Queries
predictedPoints
Description
fetch data from the table: "ppa"

Response
Returns [predictedPoints!]!

Arguments
Name	Description
distinctOn - [predictedPointsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [predictedPointsOrderBy!]	sort the rows by one or more columns
where - predictedPointsBoolExp	filter the rows returned
Example
Query
query PredictedPoints(
  $distinctOn: [predictedPointsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [predictedPointsOrderBy!],
  $where: predictedPointsBoolExp
) {
  predictedPoints(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    distance
    down
    predictedPoints
    yardLine
  }
}
Variables
{
  "distinctOn": ["distance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [predictedPointsOrderBy],
  "where": predictedPointsBoolExp
}
Response
{
  "data": {
    "predictedPoints": [
      {
        "distance": smallint,
        "down": smallint,
        "predictedPoints": numeric,
        "yardLine": smallint
      }
    ]
  }
}
Queries
predictedPointsAggregate
Description
fetch aggregated fields from the table: "ppa"

Response
Returns a predictedPointsAggregate!

Arguments
Name	Description
distinctOn - [predictedPointsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [predictedPointsOrderBy!]	sort the rows by one or more columns
where - predictedPointsBoolExp	filter the rows returned
Example
Query
query PredictedPointsAggregate(
  $distinctOn: [predictedPointsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [predictedPointsOrderBy!],
  $where: predictedPointsBoolExp
) {
  predictedPointsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...predictedPointsAvgFieldsFragment
      }
      count
      max {
        ...predictedPointsMaxFieldsFragment
      }
      min {
        ...predictedPointsMinFieldsFragment
      }
      stddev {
        ...predictedPointsStddevFieldsFragment
      }
      stddevPop {
        ...predictedPointsStddevPopFieldsFragment
      }
      stddevSamp {
        ...predictedPointsStddevSampFieldsFragment
      }
      sum {
        ...predictedPointsSumFieldsFragment
      }
      varPop {
        ...predictedPointsVarPopFieldsFragment
      }
      varSamp {
        ...predictedPointsVarSampFieldsFragment
      }
      variance {
        ...predictedPointsVarianceFieldsFragment
      }
    }
    nodes {
      distance
      down
      predictedPoints
      yardLine
    }
  }
}
Variables
{
  "distinctOn": ["distance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [predictedPointsOrderBy],
  "where": predictedPointsBoolExp
}
Response
{
  "data": {
    "predictedPointsAggregate": {
      "aggregate": predictedPointsAggregateFields,
      "nodes": [predictedPoints]
    }
  }
}
Queries
ratings
Description
fetch data from the table: "rating_systems"

Response
Returns [ratings!]!

Arguments
Name	Description
distinctOn - [ratingsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ratingsOrderBy!]	sort the rows by one or more columns
where - ratingsBoolExp	filter the rows returned
Example
Query
query Ratings(
  $distinctOn: [ratingsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ratingsOrderBy!],
  $where: ratingsBoolExp
) {
  ratings(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    conference
    conferenceId
    elo
    fpi
    fpiAvgWinProbabilityRank
    fpiDefensiveEfficiency
    fpiGameControlRank
    fpiOffensiveEfficiency
    fpiOverallEfficiency
    fpiRemainingSosRank
    fpiResumeRank
    fpiSosRank
    fpiSpecialTeamsEfficiency
    fpiStrengthOfRecordRank
    spDefense
    spOffense
    spOverall
    spSpecialTeams
    srs
    team
    teamId
    year
  }
}
Variables
{
  "distinctOn": ["conference"],
  "limit": 987,
  "offset": 123,
  "orderBy": [ratingsOrderBy],
  "where": ratingsBoolExp
}
Response
{
  "data": {
    "ratings": [
      {
        "conference": "xyz789",
        "conferenceId": smallint,
        "elo": 123,
        "fpi": numeric,
        "fpiAvgWinProbabilityRank": smallint,
        "fpiDefensiveEfficiency": numeric,
        "fpiGameControlRank": smallint,
        "fpiOffensiveEfficiency": numeric,
        "fpiOverallEfficiency": numeric,
        "fpiRemainingSosRank": smallint,
        "fpiResumeRank": smallint,
        "fpiSosRank": smallint,
        "fpiSpecialTeamsEfficiency": numeric,
        "fpiStrengthOfRecordRank": smallint,
        "spDefense": numeric,
        "spOffense": numeric,
        "spOverall": numeric,
        "spSpecialTeams": numeric,
        "srs": numeric,
        "team": "abc123",
        "teamId": 123,
        "year": smallint
      }
    ]
  }
}
Queries
recruit
Description
fetch data from the table: "recruit"

Response
Returns [Recruit!]!

Arguments
Name	Description
distinctOn - [RecruitSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitOrderBy!]	sort the rows by one or more columns
where - RecruitBoolExp	filter the rows returned
Example
Query
query Recruit(
  $distinctOn: [RecruitSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitOrderBy!],
  $where: RecruitBoolExp
) {
  recruit(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    college {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    id
    name
    overallRank
    position {
      id
      position
      positionGroup
    }
    positionRank
    ranking
    rating
    recruitSchool {
      id
      name
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
    }
    recruitType
    stars
    weight
    year
  }
}
Variables
{
  "distinctOn": ["height"],
  "limit": 123,
  "offset": 987,
  "orderBy": [RecruitOrderBy],
  "where": RecruitBoolExp
}
Response
{
  "data": {
    "recruit": [
      {
        "athlete": Athlete,
        "college": currentTeams,
        "height": 987.65,
        "hometown": Hometown,
        "id": bigint,
        "name": "xyz789",
        "overallRank": smallint,
        "position": RecruitPosition,
        "positionRank": smallint,
        "ranking": smallint,
        "rating": 987.65,
        "recruitSchool": RecruitSchool,
        "recruitType": recruit_type,
        "stars": smallint,
        "weight": smallint,
        "year": smallint
      }
    ]
  }
}
Queries
recruitAggregate
Description
fetch aggregated fields from the table: "recruit"

Response
Returns a RecruitAggregate!

Arguments
Name	Description
distinctOn - [RecruitSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitOrderBy!]	sort the rows by one or more columns
where - RecruitBoolExp	filter the rows returned
Example
Query
query RecruitAggregate(
  $distinctOn: [RecruitSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitOrderBy!],
  $where: RecruitBoolExp
) {
  recruitAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitAvgFieldsFragment
      }
      count
      max {
        ...RecruitMaxFieldsFragment
      }
      min {
        ...RecruitMinFieldsFragment
      }
      stddev {
        ...RecruitStddevFieldsFragment
      }
      stddevPop {
        ...RecruitStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitStddevSampFieldsFragment
      }
      sum {
        ...RecruitSumFieldsFragment
      }
      varPop {
        ...RecruitVarPopFieldsFragment
      }
      varSamp {
        ...RecruitVarSampFieldsFragment
      }
      variance {
        ...RecruitVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
  }
}
Variables
{
  "distinctOn": ["height"],
  "limit": 123,
  "offset": 123,
  "orderBy": [RecruitOrderBy],
  "where": RecruitBoolExp
}
Response
{
  "data": {
    "recruitAggregate": {
      "aggregate": RecruitAggregateFields,
      "nodes": [Recruit]
    }
  }
}
Queries
recruitPosition
Description
fetch data from the table: "recruit_position"

Response
Returns [RecruitPosition!]!

Arguments
Name	Description
distinctOn - [RecruitPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitPositionOrderBy!]	sort the rows by one or more columns
where - RecruitPositionBoolExp	filter the rows returned
Example
Query
query RecruitPosition(
  $distinctOn: [RecruitPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitPositionOrderBy!],
  $where: RecruitPositionBoolExp
) {
  recruitPosition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    position
    positionGroup
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [RecruitPositionOrderBy],
  "where": RecruitPositionBoolExp
}
Response
{
  "data": {
    "recruitPosition": [
      {
        "id": smallint,
        "position": "abc123",
        "positionGroup": "xyz789"
      }
    ]
  }
}
Queries
recruitPositionAggregate
Description
fetch aggregated fields from the table: "recruit_position"

Response
Returns a RecruitPositionAggregate!

Arguments
Name	Description
distinctOn - [RecruitPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitPositionOrderBy!]	sort the rows by one or more columns
where - RecruitPositionBoolExp	filter the rows returned
Example
Query
query RecruitPositionAggregate(
  $distinctOn: [RecruitPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitPositionOrderBy!],
  $where: RecruitPositionBoolExp
) {
  recruitPositionAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitPositionAvgFieldsFragment
      }
      count
      max {
        ...RecruitPositionMaxFieldsFragment
      }
      min {
        ...RecruitPositionMinFieldsFragment
      }
      stddev {
        ...RecruitPositionStddevFieldsFragment
      }
      stddevPop {
        ...RecruitPositionStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitPositionStddevSampFieldsFragment
      }
      sum {
        ...RecruitPositionSumFieldsFragment
      }
      varPop {
        ...RecruitPositionVarPopFieldsFragment
      }
      varSamp {
        ...RecruitPositionVarSampFieldsFragment
      }
      variance {
        ...RecruitPositionVarianceFieldsFragment
      }
    }
    nodes {
      id
      position
      positionGroup
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 987,
  "orderBy": [RecruitPositionOrderBy],
  "where": RecruitPositionBoolExp
}
Response
{
  "data": {
    "recruitPositionAggregate": {
      "aggregate": RecruitPositionAggregateFields,
      "nodes": [RecruitPosition]
    }
  }
}
Queries
recruitSchool
Description
fetch data from the table: "recruit_school"

Response
Returns [RecruitSchool!]!

Arguments
Name	Description
distinctOn - [RecruitSchoolSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitSchoolOrderBy!]	sort the rows by one or more columns
where - RecruitSchoolBoolExp	filter the rows returned
Example
Query
query RecruitSchool(
  $distinctOn: [RecruitSchoolSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitSchoolOrderBy!],
  $where: RecruitSchoolBoolExp
) {
  recruitSchool(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    name
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [RecruitSchoolOrderBy],
  "where": RecruitSchoolBoolExp
}
Response
{
  "data": {
    "recruitSchool": [
      {
        "id": 123,
        "name": "xyz789",
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate
      }
    ]
  }
}
Queries
recruitSchoolAggregate
Description
fetch aggregated fields from the table: "recruit_school"

Response
Returns a RecruitSchoolAggregate!

Arguments
Name	Description
distinctOn - [RecruitSchoolSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitSchoolOrderBy!]	sort the rows by one or more columns
where - RecruitSchoolBoolExp	filter the rows returned
Example
Query
query RecruitSchoolAggregate(
  $distinctOn: [RecruitSchoolSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitSchoolOrderBy!],
  $where: RecruitSchoolBoolExp
) {
  recruitSchoolAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitSchoolAvgFieldsFragment
      }
      count
      max {
        ...RecruitSchoolMaxFieldsFragment
      }
      min {
        ...RecruitSchoolMinFieldsFragment
      }
      stddev {
        ...RecruitSchoolStddevFieldsFragment
      }
      stddevPop {
        ...RecruitSchoolStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitSchoolStddevSampFieldsFragment
      }
      sum {
        ...RecruitSchoolSumFieldsFragment
      }
      varPop {
        ...RecruitSchoolVarPopFieldsFragment
      }
      varSamp {
        ...RecruitSchoolVarSampFieldsFragment
      }
      variance {
        ...RecruitSchoolVarianceFieldsFragment
      }
    }
    nodes {
      id
      name
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 123,
  "offset": 987,
  "orderBy": [RecruitSchoolOrderBy],
  "where": RecruitSchoolBoolExp
}
Response
{
  "data": {
    "recruitSchoolAggregate": {
      "aggregate": RecruitSchoolAggregateFields,
      "nodes": [RecruitSchool]
    }
  }
}
Queries
recruitingTeam
Description
fetch data from the table: "recruiting_team"

Response
Returns [RecruitingTeam!]!

Arguments
Name	Description
distinctOn - [RecruitingTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitingTeamOrderBy!]	sort the rows by one or more columns
where - RecruitingTeamBoolExp	filter the rows returned
Example
Query
query RecruitingTeam(
  $distinctOn: [RecruitingTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitingTeamOrderBy!],
  $where: RecruitingTeamBoolExp
) {
  recruitingTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    points
    rank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    year
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [RecruitingTeamOrderBy],
  "where": RecruitingTeamBoolExp
}
Response
{
  "data": {
    "recruitingTeam": [
      {
        "id": 987,
        "points": numeric,
        "rank": smallint,
        "team": currentTeams,
        "year": smallint
      }
    ]
  }
}
Queries
recruitingTeamAggregate
Description
fetch aggregated fields from the table: "recruiting_team"

Response
Returns a RecruitingTeamAggregate!

Arguments
Name	Description
distinctOn - [RecruitingTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitingTeamOrderBy!]	sort the rows by one or more columns
where - RecruitingTeamBoolExp	filter the rows returned
Example
Query
query RecruitingTeamAggregate(
  $distinctOn: [RecruitingTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitingTeamOrderBy!],
  $where: RecruitingTeamBoolExp
) {
  recruitingTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitingTeamAvgFieldsFragment
      }
      count
      max {
        ...RecruitingTeamMaxFieldsFragment
      }
      min {
        ...RecruitingTeamMinFieldsFragment
      }
      stddev {
        ...RecruitingTeamStddevFieldsFragment
      }
      stddevPop {
        ...RecruitingTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitingTeamStddevSampFieldsFragment
      }
      sum {
        ...RecruitingTeamSumFieldsFragment
      }
      varPop {
        ...RecruitingTeamVarPopFieldsFragment
      }
      varSamp {
        ...RecruitingTeamVarSampFieldsFragment
      }
      variance {
        ...RecruitingTeamVarianceFieldsFragment
      }
    }
    nodes {
      id
      points
      rank
      team {
        ...currentTeamsFragment
      }
      year
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [RecruitingTeamOrderBy],
  "where": RecruitingTeamBoolExp
}
Response
{
  "data": {
    "recruitingTeamAggregate": {
      "aggregate": RecruitingTeamAggregateFields,
      "nodes": [RecruitingTeam]
    }
  }
}
Queries
scoreboard
Description
fetch data from the table: "scoreboard"

Response
Returns [Scoreboard!]!

Arguments
Name	Description
distinctOn - [ScoreboardSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ScoreboardOrderBy!]	sort the rows by one or more columns
where - ScoreboardBoolExp	filter the rows returned
Example
Query
query Scoreboard(
  $distinctOn: [ScoreboardSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ScoreboardOrderBy!],
  $where: ScoreboardBoolExp
) {
  scoreboard(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    awayClassification
    awayConference
    awayConferenceAbbreviation
    awayId
    awayLineScores
    awayPoints
    awayTeam
    city
    conferenceGame
    currentClock
    currentPeriod
    currentPossession
    currentSituation
    homeClassification
    homeConference
    homeConferenceAbbreviation
    homeId
    homeLineScores
    homePoints
    homeTeam
    id
    lastPlay
    moneylineAway
    moneylineHome
    neutralSite
    overUnder
    spread
    startDate
    startTimeTbd
    state
    status
    temperature
    tv
    venue
    weatherDescription
    windDirection
    windSpeed
  }
}
Variables
{
  "distinctOn": ["awayClassification"],
  "limit": 123,
  "offset": 987,
  "orderBy": [ScoreboardOrderBy],
  "where": ScoreboardBoolExp
}
Response
{
  "data": {
    "scoreboard": [
      {
        "awayClassification": division,
        "awayConference": "xyz789",
        "awayConferenceAbbreviation": "abc123",
        "awayId": 987,
        "awayLineScores": [smallint],
        "awayPoints": smallint,
        "awayTeam": "abc123",
        "city": "xyz789",
        "conferenceGame": false,
        "currentClock": "abc123",
        "currentPeriod": smallint,
        "currentPossession": "xyz789",
        "currentSituation": "xyz789",
        "homeClassification": division,
        "homeConference": "xyz789",
        "homeConferenceAbbreviation": "xyz789",
        "homeId": 123,
        "homeLineScores": [smallint],
        "homePoints": smallint,
        "homeTeam": "abc123",
        "id": 123,
        "lastPlay": "xyz789",
        "moneylineAway": 987,
        "moneylineHome": 987,
        "neutralSite": true,
        "overUnder": numeric,
        "spread": numeric,
        "startDate": timestamptz,
        "startTimeTbd": false,
        "state": "xyz789",
        "status": game_status,
        "temperature": numeric,
        "tv": "xyz789",
        "venue": "abc123",
        "weatherDescription": "xyz789",
        "windDirection": numeric,
        "windSpeed": numeric
      }
    ]
  }
}
Queries
teamTalent
Description
fetch data from the table: "team_talent"

Response
Returns [TeamTalent!]!

Arguments
Name	Description
distinctOn - [TeamTalentSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TeamTalentOrderBy!]	sort the rows by one or more columns
where - TeamTalentBoolExp	filter the rows returned
Example
Query
query TeamTalent(
  $distinctOn: [TeamTalentSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TeamTalentOrderBy!],
  $where: TeamTalentBoolExp
) {
  teamTalent(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    talent
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    year
  }
}
Variables
{
  "distinctOn": ["talent"],
  "limit": 987,
  "offset": 123,
  "orderBy": [TeamTalentOrderBy],
  "where": TeamTalentBoolExp
}
Response
{
  "data": {
    "teamTalent": [
      {
        "talent": numeric,
        "team": currentTeams,
        "year": smallint
      }
    ]
  }
}
Queries
teamTalentAggregate
Description
fetch aggregated fields from the table: "team_talent"

Response
Returns a TeamTalentAggregate!

Arguments
Name	Description
distinctOn - [TeamTalentSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TeamTalentOrderBy!]	sort the rows by one or more columns
where - TeamTalentBoolExp	filter the rows returned
Example
Query
query TeamTalentAggregate(
  $distinctOn: [TeamTalentSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TeamTalentOrderBy!],
  $where: TeamTalentBoolExp
) {
  teamTalentAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...TeamTalentAvgFieldsFragment
      }
      count
      max {
        ...TeamTalentMaxFieldsFragment
      }
      min {
        ...TeamTalentMinFieldsFragment
      }
      stddev {
        ...TeamTalentStddevFieldsFragment
      }
      stddevPop {
        ...TeamTalentStddevPopFieldsFragment
      }
      stddevSamp {
        ...TeamTalentStddevSampFieldsFragment
      }
      sum {
        ...TeamTalentSumFieldsFragment
      }
      varPop {
        ...TeamTalentVarPopFieldsFragment
      }
      varSamp {
        ...TeamTalentVarSampFieldsFragment
      }
      variance {
        ...TeamTalentVarianceFieldsFragment
      }
    }
    nodes {
      talent
      team {
        ...currentTeamsFragment
      }
      year
    }
  }
}
Variables
{
  "distinctOn": ["talent"],
  "limit": 987,
  "offset": 987,
  "orderBy": [TeamTalentOrderBy],
  "where": TeamTalentBoolExp
}
Response
{
  "data": {
    "teamTalentAggregate": {
      "aggregate": TeamTalentAggregateFields,
      "nodes": [TeamTalent]
    }
  }
}
Queries
transfer
Description
fetch data from the table: "transfer"

Response
Returns [Transfer!]!

Arguments
Name	Description
distinctOn - [TransferSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TransferOrderBy!]	sort the rows by one or more columns
where - TransferBoolExp	filter the rows returned
Example
Query
query Transfer(
  $distinctOn: [TransferSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TransferOrderBy!],
  $where: TransferBoolExp
) {
  transfer(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    eligibility
    firstName
    fromTeam {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    lastName
    position {
      id
      position
      positionGroup
    }
    rating
    season
    stars
    toTeam {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    transferDate
  }
}
Variables
{
  "distinctOn": ["eligibility"],
  "limit": 987,
  "offset": 987,
  "orderBy": [TransferOrderBy],
  "where": TransferBoolExp
}
Response
{
  "data": {
    "transfer": [
      {
        "eligibility": "abc123",
        "firstName": "abc123",
        "fromTeam": currentTeams,
        "lastName": "abc123",
        "position": RecruitPosition,
        "rating": numeric,
        "season": smallint,
        "stars": smallint,
        "toTeam": currentTeams,
        "transferDate": timestamp
      }
    ]
  }
}
Queries
weatherCondition
Description
fetch data from the table: "weather_condition"

Response
Returns [WeatherCondition!]!

Arguments
Name	Description
distinctOn - [WeatherConditionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [WeatherConditionOrderBy!]	sort the rows by one or more columns
where - WeatherConditionBoolExp	filter the rows returned
Example
Query
query WeatherCondition(
  $distinctOn: [WeatherConditionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [WeatherConditionOrderBy!],
  $where: WeatherConditionBoolExp
) {
  weatherCondition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    description
    id
  }
}
Variables
{
  "distinctOn": ["description"],
  "limit": 123,
  "offset": 987,
  "orderBy": [WeatherConditionOrderBy],
  "where": WeatherConditionBoolExp
}
Response
{
  "data": {
    "weatherCondition": [
      {
        "description": "abc123",
        "id": smallint
      }
    ]
  }
}
Subscriptions
adjustedPlayerMetrics
Description
An array relationship

Response
Returns [AdjustedPlayerMetrics!]!

Arguments
Name	Description
distinctOn - [AdjustedPlayerMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedPlayerMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedPlayerMetricsBoolExp	filter the rows returned
Example
Query
subscription AdjustedPlayerMetrics(
  $distinctOn: [AdjustedPlayerMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedPlayerMetricsOrderBy!],
  $where: AdjustedPlayerMetricsBoolExp
) {
  adjustedPlayerMetrics(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    metricType
    metricValue
    plays
    year
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AdjustedPlayerMetricsOrderBy],
  "where": AdjustedPlayerMetricsBoolExp
}
Response
{
  "data": {
    "adjustedPlayerMetrics": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "metricType": player_adjusted_metric_type,
        "metricValue": numeric,
        "plays": smallint,
        "year": smallint
      }
    ]
  }
}
Subscriptions
adjustedPlayerMetricsAggregate
Description
An aggregate relationship

Response
Returns an AdjustedPlayerMetricsAggregate!

Arguments
Name	Description
distinctOn - [AdjustedPlayerMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedPlayerMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedPlayerMetricsBoolExp	filter the rows returned
Example
Query
subscription AdjustedPlayerMetricsAggregate(
  $distinctOn: [AdjustedPlayerMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedPlayerMetricsOrderBy!],
  $where: AdjustedPlayerMetricsBoolExp
) {
  adjustedPlayerMetricsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AdjustedPlayerMetricsAvgFieldsFragment
      }
      count
      max {
        ...AdjustedPlayerMetricsMaxFieldsFragment
      }
      min {
        ...AdjustedPlayerMetricsMinFieldsFragment
      }
      stddev {
        ...AdjustedPlayerMetricsStddevFieldsFragment
      }
      stddevPop {
        ...AdjustedPlayerMetricsStddevPopFieldsFragment
      }
      stddevSamp {
        ...AdjustedPlayerMetricsStddevSampFieldsFragment
      }
      sum {
        ...AdjustedPlayerMetricsSumFieldsFragment
      }
      varPop {
        ...AdjustedPlayerMetricsVarPopFieldsFragment
      }
      varSamp {
        ...AdjustedPlayerMetricsVarSampFieldsFragment
      }
      variance {
        ...AdjustedPlayerMetricsVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AdjustedPlayerMetricsOrderBy],
  "where": AdjustedPlayerMetricsBoolExp
}
Response
{
  "data": {
    "adjustedPlayerMetricsAggregate": {
      "aggregate": AdjustedPlayerMetricsAggregateFields,
      "nodes": [AdjustedPlayerMetrics]
    }
  }
}
Subscriptions
adjustedTeamMetrics
Description
fetch data from the table: "adjusted_team_metrics"

Response
Returns [AdjustedTeamMetrics!]!

Arguments
Name	Description
distinctOn - [AdjustedTeamMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedTeamMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedTeamMetricsBoolExp	filter the rows returned
Example
Query
subscription AdjustedTeamMetrics(
  $distinctOn: [AdjustedTeamMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedTeamMetricsOrderBy!],
  $where: AdjustedTeamMetricsBoolExp
) {
  adjustedTeamMetrics(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    epa
    epaAllowed
    explosiveness
    explosivenessAllowed
    highlightYards
    highlightYardsAllowed
    lineYards
    lineYardsAllowed
    openFieldYards
    openFieldYardsAllowed
    passingDownsSuccess
    passingDownsSuccessAllowed
    passingEpa
    passingEpaAllowed
    rushingEpa
    rushingEpaAllowed
    secondLevelYards
    secondLevelYardsAllowed
    standardDownsSuccess
    standardDownsSuccessAllowed
    success
    successAllowed
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    teamId
    year
  }
}
Variables
{
  "distinctOn": ["epa"],
  "limit": 123,
  "offset": 123,
  "orderBy": [AdjustedTeamMetricsOrderBy],
  "where": AdjustedTeamMetricsBoolExp
}
Response
{
  "data": {
    "adjustedTeamMetrics": [
      {
        "epa": numeric,
        "epaAllowed": numeric,
        "explosiveness": numeric,
        "explosivenessAllowed": numeric,
        "highlightYards": numeric,
        "highlightYardsAllowed": numeric,
        "lineYards": numeric,
        "lineYardsAllowed": numeric,
        "openFieldYards": numeric,
        "openFieldYardsAllowed": numeric,
        "passingDownsSuccess": numeric,
        "passingDownsSuccessAllowed": numeric,
        "passingEpa": numeric,
        "passingEpaAllowed": numeric,
        "rushingEpa": numeric,
        "rushingEpaAllowed": numeric,
        "secondLevelYards": numeric,
        "secondLevelYardsAllowed": numeric,
        "standardDownsSuccess": numeric,
        "standardDownsSuccessAllowed": numeric,
        "success": numeric,
        "successAllowed": numeric,
        "team": currentTeams,
        "teamId": 123,
        "year": smallint
      }
    ]
  }
}
Subscriptions
adjustedTeamMetricsAggregate
Description
fetch aggregated fields from the table: "adjusted_team_metrics"

Response
Returns an AdjustedTeamMetricsAggregate!

Arguments
Name	Description
distinctOn - [AdjustedTeamMetricsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AdjustedTeamMetricsOrderBy!]	sort the rows by one or more columns
where - AdjustedTeamMetricsBoolExp	filter the rows returned
Example
Query
subscription AdjustedTeamMetricsAggregate(
  $distinctOn: [AdjustedTeamMetricsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AdjustedTeamMetricsOrderBy!],
  $where: AdjustedTeamMetricsBoolExp
) {
  adjustedTeamMetricsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AdjustedTeamMetricsAvgFieldsFragment
      }
      count
      max {
        ...AdjustedTeamMetricsMaxFieldsFragment
      }
      min {
        ...AdjustedTeamMetricsMinFieldsFragment
      }
      stddev {
        ...AdjustedTeamMetricsStddevFieldsFragment
      }
      stddevPop {
        ...AdjustedTeamMetricsStddevPopFieldsFragment
      }
      stddevSamp {
        ...AdjustedTeamMetricsStddevSampFieldsFragment
      }
      sum {
        ...AdjustedTeamMetricsSumFieldsFragment
      }
      varPop {
        ...AdjustedTeamMetricsVarPopFieldsFragment
      }
      varSamp {
        ...AdjustedTeamMetricsVarSampFieldsFragment
      }
      variance {
        ...AdjustedTeamMetricsVarianceFieldsFragment
      }
    }
    nodes {
      epa
      epaAllowed
      explosiveness
      explosivenessAllowed
      highlightYards
      highlightYardsAllowed
      lineYards
      lineYardsAllowed
      openFieldYards
      openFieldYardsAllowed
      passingDownsSuccess
      passingDownsSuccessAllowed
      passingEpa
      passingEpaAllowed
      rushingEpa
      rushingEpaAllowed
      secondLevelYards
      secondLevelYardsAllowed
      standardDownsSuccess
      standardDownsSuccessAllowed
      success
      successAllowed
      team {
        ...currentTeamsFragment
      }
      teamId
      year
    }
  }
}
Variables
{
  "distinctOn": ["epa"],
  "limit": 123,
  "offset": 123,
  "orderBy": [AdjustedTeamMetricsOrderBy],
  "where": AdjustedTeamMetricsBoolExp
}
Response
{
  "data": {
    "adjustedTeamMetricsAggregate": {
      "aggregate": AdjustedTeamMetricsAggregateFields,
      "nodes": [AdjustedTeamMetrics]
    }
  }
}
Subscriptions
athlete
Description
fetch data from the table: "athlete"

Response
Returns [Athlete!]!

Arguments
Name	Description
distinctOn - [AthleteSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteOrderBy!]	sort the rows by one or more columns
where - AthleteBoolExp	filter the rows returned
Example
Query
subscription Athlete(
  $distinctOn: [AthleteSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteOrderBy!],
  $where: AthleteBoolExp
) {
  athlete(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    adjustedPlayerMetrics {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
    adjustedPlayerMetricsAggregate {
      aggregate {
        ...AdjustedPlayerMetricsAggregateFieldsFragment
      }
      nodes {
        ...AdjustedPlayerMetricsFragment
      }
    }
    athleteTeams {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
    athleteTeamsAggregate {
      aggregate {
        ...AthleteTeamAggregateFieldsFragment
      }
      nodes {
        ...AthleteTeamFragment
      }
    }
    firstName
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    hometownId
    id
    jersey
    lastName
    name
    position {
      abbreviation
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      displayName
      id
      name
    }
    positionId
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    teamId
    weight
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AthleteOrderBy],
  "where": AthleteBoolExp
}
Response
{
  "data": {
    "athlete": [
      {
        "adjustedPlayerMetrics": [AdjustedPlayerMetrics],
        "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregate,
        "athleteTeams": [AthleteTeam],
        "athleteTeamsAggregate": AthleteTeamAggregate,
        "firstName": "abc123",
        "height": smallint,
        "hometown": Hometown,
        "hometownId": 123,
        "id": bigint,
        "jersey": smallint,
        "lastName": "abc123",
        "name": "xyz789",
        "position": Position,
        "positionId": smallint,
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate,
        "teamId": 987,
        "weight": smallint
      }
    ]
  }
}
Subscriptions
athleteAggregate
Description
fetch aggregated fields from the table: "athlete"

Response
Returns an AthleteAggregate!

Arguments
Name	Description
distinctOn - [AthleteSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteOrderBy!]	sort the rows by one or more columns
where - AthleteBoolExp	filter the rows returned
Example
Query
subscription AthleteAggregate(
  $distinctOn: [AthleteSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteOrderBy!],
  $where: AthleteBoolExp
) {
  athleteAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AthleteAvgFieldsFragment
      }
      count
      max {
        ...AthleteMaxFieldsFragment
      }
      min {
        ...AthleteMinFieldsFragment
      }
      stddev {
        ...AthleteStddevFieldsFragment
      }
      stddevPop {
        ...AthleteStddevPopFieldsFragment
      }
      stddevSamp {
        ...AthleteStddevSampFieldsFragment
      }
      sum {
        ...AthleteSumFieldsFragment
      }
      varPop {
        ...AthleteVarPopFieldsFragment
      }
      varSamp {
        ...AthleteVarSampFieldsFragment
      }
      variance {
        ...AthleteVarianceFieldsFragment
      }
    }
    nodes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 987,
  "offset": 123,
  "orderBy": [AthleteOrderBy],
  "where": AthleteBoolExp
}
Response
{
  "data": {
    "athleteAggregate": {
      "aggregate": AthleteAggregateFields,
      "nodes": [Athlete]
    }
  }
}
Subscriptions
athleteByPk
Description
fetch data from the table: "athlete" using primary key columns

Response
Returns an Athlete

Arguments
Name	Description
id - bigint!	
Example
Query
subscription AthleteByPk($id: bigint!) {
  athleteByPk(id: $id) {
    adjustedPlayerMetrics {
      athlete {
        ...AthleteFragment
      }
      athleteId
      metricType
      metricValue
      plays
      year
    }
    adjustedPlayerMetricsAggregate {
      aggregate {
        ...AdjustedPlayerMetricsAggregateFieldsFragment
      }
      nodes {
        ...AdjustedPlayerMetricsFragment
      }
    }
    athleteTeams {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
    athleteTeamsAggregate {
      aggregate {
        ...AthleteTeamAggregateFieldsFragment
      }
      nodes {
        ...AthleteTeamFragment
      }
    }
    firstName
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    hometownId
    id
    jersey
    lastName
    name
    position {
      abbreviation
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      displayName
      id
      name
    }
    positionId
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    teamId
    weight
  }
}
Variables
{"id": bigint}
Response
{
  "data": {
    "athleteByPk": {
      "adjustedPlayerMetrics": [AdjustedPlayerMetrics],
      "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregate,
      "athleteTeams": [AthleteTeam],
      "athleteTeamsAggregate": AthleteTeamAggregate,
      "firstName": "xyz789",
      "height": smallint,
      "hometown": Hometown,
      "hometownId": 123,
      "id": bigint,
      "jersey": smallint,
      "lastName": "abc123",
      "name": "abc123",
      "position": Position,
      "positionId": smallint,
      "recruits": [Recruit],
      "recruitsAggregate": RecruitAggregate,
      "teamId": 987,
      "weight": smallint
    }
  }
}
Subscriptions
athleteTeam
Description
fetch data from the table: "athlete_team"

Response
Returns [AthleteTeam!]!

Arguments
Name	Description
distinctOn - [AthleteTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteTeamOrderBy!]	sort the rows by one or more columns
where - AthleteTeamBoolExp	filter the rows returned
Example
Query
subscription AthleteTeam(
  $distinctOn: [AthleteTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteTeamOrderBy!],
  $where: AthleteTeamBoolExp
) {
  athleteTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    endYear
    startYear
    team {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
    teamId
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 123,
  "orderBy": [AthleteTeamOrderBy],
  "where": AthleteTeamBoolExp
}
Response
{
  "data": {
    "athleteTeam": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "endYear": smallint,
        "startYear": smallint,
        "team": historicalTeam,
        "teamId": 123
      }
    ]
  }
}
Subscriptions
athleteTeamAggregate
Description
fetch aggregated fields from the table: "athlete_team"

Response
Returns an AthleteTeamAggregate!

Arguments
Name	Description
distinctOn - [AthleteTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [AthleteTeamOrderBy!]	sort the rows by one or more columns
where - AthleteTeamBoolExp	filter the rows returned
Example
Query
subscription AthleteTeamAggregate(
  $distinctOn: [AthleteTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [AthleteTeamOrderBy!],
  $where: AthleteTeamBoolExp
) {
  athleteTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...AthleteTeamAvgFieldsFragment
      }
      count
      max {
        ...AthleteTeamMaxFieldsFragment
      }
      min {
        ...AthleteTeamMinFieldsFragment
      }
      stddev {
        ...AthleteTeamStddevFieldsFragment
      }
      stddevPop {
        ...AthleteTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...AthleteTeamStddevSampFieldsFragment
      }
      sum {
        ...AthleteTeamSumFieldsFragment
      }
      varPop {
        ...AthleteTeamVarPopFieldsFragment
      }
      varSamp {
        ...AthleteTeamVarSampFieldsFragment
      }
      variance {
        ...AthleteTeamVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      endYear
      startYear
      team {
        ...historicalTeamFragment
      }
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [AthleteTeamOrderBy],
  "where": AthleteTeamBoolExp
}
Response
{
  "data": {
    "athleteTeamAggregate": {
      "aggregate": AthleteTeamAggregateFields,
      "nodes": [AthleteTeam]
    }
  }
}
Subscriptions
calendar
Description
fetch data from the table: "calendar"

Response
Returns [Calendar!]!

Arguments
Name	Description
distinctOn - [CalendarSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CalendarOrderBy!]	sort the rows by one or more columns
where - CalendarBoolExp	filter the rows returned
Example
Query
subscription Calendar(
  $distinctOn: [CalendarSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CalendarOrderBy!],
  $where: CalendarBoolExp
) {
  calendar(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    endDate
    seasonType
    startDate
    week
    year
  }
}
Variables
{
  "distinctOn": ["endDate"],
  "limit": 987,
  "offset": 123,
  "orderBy": [CalendarOrderBy],
  "where": CalendarBoolExp
}
Response
{
  "data": {
    "calendar": [
      {
        "endDate": timestamp,
        "seasonType": season_type,
        "startDate": timestamp,
        "week": smallint,
        "year": smallint
      }
    ]
  }
}
Subscriptions
coach
Description
fetch data from the table: "coach"

Response
Returns [Coach!]!

Arguments
Name	Description
distinctOn - [CoachSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachOrderBy!]	sort the rows by one or more columns
where - CoachBoolExp	filter the rows returned
Example
Query
subscription Coach(
  $distinctOn: [CoachSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachOrderBy!],
  $where: CoachBoolExp
) {
  coach(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    firstName
    id
    lastName
    seasons {
      coach {
        ...CoachFragment
      }
      games
      losses
      postseasonRank
      preseasonRank
      team {
        ...currentTeamsFragment
      }
      ties
      wins
      year
    }
    seasonsAggregate {
      aggregate {
        ...CoachSeasonAggregateFieldsFragment
      }
      nodes {
        ...CoachSeasonFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 123,
  "offset": 987,
  "orderBy": [CoachOrderBy],
  "where": CoachBoolExp
}
Response
{
  "data": {
    "coach": [
      {
        "firstName": "abc123",
        "id": 123,
        "lastName": "abc123",
        "seasons": [CoachSeason],
        "seasonsAggregate": CoachSeasonAggregate
      }
    ]
  }
}
Subscriptions
coachAggregate
Description
fetch aggregated fields from the table: "coach"

Response
Returns a CoachAggregate!

Arguments
Name	Description
distinctOn - [CoachSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachOrderBy!]	sort the rows by one or more columns
where - CoachBoolExp	filter the rows returned
Example
Query
subscription CoachAggregate(
  $distinctOn: [CoachSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachOrderBy!],
  $where: CoachBoolExp
) {
  coachAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...CoachAvgFieldsFragment
      }
      count
      max {
        ...CoachMaxFieldsFragment
      }
      min {
        ...CoachMinFieldsFragment
      }
      stddev {
        ...CoachStddevFieldsFragment
      }
      stddevPop {
        ...CoachStddevPopFieldsFragment
      }
      stddevSamp {
        ...CoachStddevSampFieldsFragment
      }
      sum {
        ...CoachSumFieldsFragment
      }
      varPop {
        ...CoachVarPopFieldsFragment
      }
      varSamp {
        ...CoachVarSampFieldsFragment
      }
      variance {
        ...CoachVarianceFieldsFragment
      }
    }
    nodes {
      firstName
      id
      lastName
      seasons {
        ...CoachSeasonFragment
      }
      seasonsAggregate {
        ...CoachSeasonAggregateFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["firstName"],
  "limit": 123,
  "offset": 123,
  "orderBy": [CoachOrderBy],
  "where": CoachBoolExp
}
Response
{
  "data": {
    "coachAggregate": {
      "aggregate": CoachAggregateFields,
      "nodes": [Coach]
    }
  }
}
Subscriptions
coachSeason
Description
fetch data from the table: "coach_season"

Response
Returns [CoachSeason!]!

Arguments
Name	Description
distinctOn - [CoachSeasonSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachSeasonOrderBy!]	sort the rows by one or more columns
where - CoachSeasonBoolExp	filter the rows returned
Example
Query
subscription CoachSeason(
  $distinctOn: [CoachSeasonSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachSeasonOrderBy!],
  $where: CoachSeasonBoolExp
) {
  coachSeason(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    coach {
      firstName
      id
      lastName
      seasons {
        ...CoachSeasonFragment
      }
      seasonsAggregate {
        ...CoachSeasonAggregateFragment
      }
    }
    games
    losses
    postseasonRank
    preseasonRank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    ties
    wins
    year
  }
}
Variables
{
  "distinctOn": ["games"],
  "limit": 987,
  "offset": 123,
  "orderBy": [CoachSeasonOrderBy],
  "where": CoachSeasonBoolExp
}
Response
{
  "data": {
    "coachSeason": [
      {
        "coach": Coach,
        "games": smallint,
        "losses": smallint,
        "postseasonRank": smallint,
        "preseasonRank": smallint,
        "team": currentTeams,
        "ties": smallint,
        "wins": smallint,
        "year": smallint
      }
    ]
  }
}
Subscriptions
coachSeasonAggregate
Description
fetch aggregated fields from the table: "coach_season"

Response
Returns a CoachSeasonAggregate!

Arguments
Name	Description
distinctOn - [CoachSeasonSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [CoachSeasonOrderBy!]	sort the rows by one or more columns
where - CoachSeasonBoolExp	filter the rows returned
Example
Query
subscription CoachSeasonAggregate(
  $distinctOn: [CoachSeasonSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [CoachSeasonOrderBy!],
  $where: CoachSeasonBoolExp
) {
  coachSeasonAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...CoachSeasonAvgFieldsFragment
      }
      count
      max {
        ...CoachSeasonMaxFieldsFragment
      }
      min {
        ...CoachSeasonMinFieldsFragment
      }
      stddev {
        ...CoachSeasonStddevFieldsFragment
      }
      stddevPop {
        ...CoachSeasonStddevPopFieldsFragment
      }
      stddevSamp {
        ...CoachSeasonStddevSampFieldsFragment
      }
      sum {
        ...CoachSeasonSumFieldsFragment
      }
      varPop {
        ...CoachSeasonVarPopFieldsFragment
      }
      varSamp {
        ...CoachSeasonVarSampFieldsFragment
      }
      variance {
        ...CoachSeasonVarianceFieldsFragment
      }
    }
    nodes {
      coach {
        ...CoachFragment
      }
      games
      losses
      postseasonRank
      preseasonRank
      team {
        ...currentTeamsFragment
      }
      ties
      wins
      year
    }
  }
}
Variables
{
  "distinctOn": ["games"],
  "limit": 123,
  "offset": 987,
  "orderBy": [CoachSeasonOrderBy],
  "where": CoachSeasonBoolExp
}
Response
{
  "data": {
    "coachSeasonAggregate": {
      "aggregate": CoachSeasonAggregateFields,
      "nodes": [CoachSeason]
    }
  }
}
Subscriptions
conference
Description
fetch data from the table: "conference"

Response
Returns [Conference!]!

Arguments
Name	Description
distinctOn - [ConferenceSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ConferenceOrderBy!]	sort the rows by one or more columns
where - ConferenceBoolExp	filter the rows returned
Example
Query
subscription Conference(
  $distinctOn: [ConferenceSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ConferenceOrderBy!],
  $where: ConferenceBoolExp
) {
  conference(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    division
    id
    name
    shortName
    srName
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [ConferenceOrderBy],
  "where": ConferenceBoolExp
}
Response
{
  "data": {
    "conference": [
      {
        "abbreviation": "xyz789",
        "division": division,
        "id": smallint,
        "name": "xyz789",
        "shortName": "xyz789",
        "srName": "xyz789"
      }
    ]
  }
}
Subscriptions
currentTeams
Description
fetch data from the table: "current_conferences"

Response
Returns [currentTeams!]!

Arguments
Name	Description
distinctOn - [currentTeamsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [currentTeamsOrderBy!]	sort the rows by one or more columns
where - currentTeamsBoolExp	filter the rows returned
Example
Query
subscription CurrentTeams(
  $distinctOn: [currentTeamsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [currentTeamsOrderBy!],
  $where: currentTeamsBoolExp
) {
  currentTeams(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    classification
    conference
    conferenceId
    division
    school
    teamId
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 123,
  "orderBy": [currentTeamsOrderBy],
  "where": currentTeamsBoolExp
}
Response
{
  "data": {
    "currentTeams": [
      {
        "abbreviation": "xyz789",
        "classification": division,
        "conference": "xyz789",
        "conferenceId": smallint,
        "division": "xyz789",
        "school": "xyz789",
        "teamId": 987
      }
    ]
  }
}
Subscriptions
currentTeamsAggregate
Description
fetch aggregated fields from the table: "current_conferences"

Response
Returns a currentTeamsAggregate!

Arguments
Name	Description
distinctOn - [currentTeamsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [currentTeamsOrderBy!]	sort the rows by one or more columns
where - currentTeamsBoolExp	filter the rows returned
Example
Query
subscription CurrentTeamsAggregate(
  $distinctOn: [currentTeamsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [currentTeamsOrderBy!],
  $where: currentTeamsBoolExp
) {
  currentTeamsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...currentTeamsAvgFieldsFragment
      }
      count
      max {
        ...currentTeamsMaxFieldsFragment
      }
      min {
        ...currentTeamsMinFieldsFragment
      }
      stddev {
        ...currentTeamsStddevFieldsFragment
      }
      stddevPop {
        ...currentTeamsStddevPopFieldsFragment
      }
      stddevSamp {
        ...currentTeamsStddevSampFieldsFragment
      }
      sum {
        ...currentTeamsSumFieldsFragment
      }
      varPop {
        ...currentTeamsVarPopFieldsFragment
      }
      varSamp {
        ...currentTeamsVarSampFieldsFragment
      }
      variance {
        ...currentTeamsVarianceFieldsFragment
      }
    }
    nodes {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 123,
  "orderBy": [currentTeamsOrderBy],
  "where": currentTeamsBoolExp
}
Response
{
  "data": {
    "currentTeamsAggregate": {
      "aggregate": currentTeamsAggregateFields,
      "nodes": [currentTeams]
    }
  }
}
Subscriptions
draftPicks
Description
fetch data from the table: "draft_picks"

Response
Returns [DraftPicks!]!

Arguments
Name	Description
distinctOn - [DraftPicksSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftPicksOrderBy!]	sort the rows by one or more columns
where - DraftPicksBoolExp	filter the rows returned
Example
Query
subscription DraftPicks(
  $distinctOn: [DraftPicksSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftPicksOrderBy!],
  $where: DraftPicksBoolExp
) {
  draftPicks(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    collegeAthleteRecord {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    collegeId
    collegeTeam {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
    collegeTeamId
    draftTeam {
      displayName
      id
      location
      logo
      mascot
      nickname
      picks {
        ...DraftPicksFragment
      }
      picksAggregate {
        ...DraftPicksAggregateFragment
      }
      shortDisplayName
    }
    grade
    height
    name
    nflTeamId
    overall
    overallRank
    pick
    position {
      abbreviation
      id
      name
    }
    positionId
    positionRank
    round
    weight
    year
  }
}
Variables
{
  "distinctOn": ["collegeId"],
  "limit": 987,
  "offset": 123,
  "orderBy": [DraftPicksOrderBy],
  "where": DraftPicksBoolExp
}
Response
{
  "data": {
    "draftPicks": [
      {
        "collegeAthleteRecord": Athlete,
        "collegeId": 123,
        "collegeTeam": historicalTeam,
        "collegeTeamId": 987,
        "draftTeam": DraftTeam,
        "grade": smallint,
        "height": smallint,
        "name": "xyz789",
        "nflTeamId": smallint,
        "overall": smallint,
        "overallRank": smallint,
        "pick": smallint,
        "position": DraftPosition,
        "positionId": smallint,
        "positionRank": smallint,
        "round": smallint,
        "weight": smallint,
        "year": smallint
      }
    ]
  }
}
Subscriptions
draftPosition
Description
fetch data from the table: "draft_position"

Response
Returns [DraftPosition!]!

Arguments
Name	Description
distinctOn - [DraftPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftPositionOrderBy!]	sort the rows by one or more columns
where - DraftPositionBoolExp	filter the rows returned
Example
Query
subscription DraftPosition(
  $distinctOn: [DraftPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftPositionOrderBy!],
  $where: DraftPositionBoolExp
) {
  draftPosition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    id
    name
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 123,
  "orderBy": [DraftPositionOrderBy],
  "where": DraftPositionBoolExp
}
Response
{
  "data": {
    "draftPosition": [
      {
        "abbreviation": "xyz789",
        "id": smallint,
        "name": "xyz789"
      }
    ]
  }
}
Subscriptions
draftTeam
Description
fetch data from the table: "draft_team"

Response
Returns [DraftTeam!]!

Arguments
Name	Description
distinctOn - [DraftTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [DraftTeamOrderBy!]	sort the rows by one or more columns
where - DraftTeamBoolExp	filter the rows returned
Example
Query
subscription DraftTeam(
  $distinctOn: [DraftTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [DraftTeamOrderBy!],
  $where: DraftTeamBoolExp
) {
  draftTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    displayName
    id
    location
    logo
    mascot
    nickname
    picks {
      collegeAthleteRecord {
        ...AthleteFragment
      }
      collegeId
      collegeTeam {
        ...historicalTeamFragment
      }
      collegeTeamId
      draftTeam {
        ...DraftTeamFragment
      }
      grade
      height
      name
      nflTeamId
      overall
      overallRank
      pick
      position {
        ...DraftPositionFragment
      }
      positionId
      positionRank
      round
      weight
      year
    }
    picksAggregate {
      aggregate {
        ...DraftPicksAggregateFieldsFragment
      }
      nodes {
        ...DraftPicksFragment
      }
    }
    shortDisplayName
  }
}
Variables
{
  "distinctOn": ["displayName"],
  "limit": 123,
  "offset": 123,
  "orderBy": [DraftTeamOrderBy],
  "where": DraftTeamBoolExp
}
Response
{
  "data": {
    "draftTeam": [
      {
        "displayName": "xyz789",
        "id": smallint,
        "location": "abc123",
        "logo": "abc123",
        "mascot": "abc123",
        "nickname": "xyz789",
        "picks": [DraftPicks],
        "picksAggregate": DraftPicksAggregate,
        "shortDisplayName": "xyz789"
      }
    ]
  }
}
Subscriptions
game
Description
fetch data from the table: "game_info"

Response
Returns [game!]!

Arguments
Name	Description
distinctOn - [gameSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [gameOrderBy!]	sort the rows by one or more columns
where - gameBoolExp	filter the rows returned
Example
Query
subscription Game(
  $distinctOn: [gameSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [gameOrderBy!],
  $where: gameBoolExp
) {
  game(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    attendance
    awayClassification
    awayConference
    awayConferenceId
    awayConferenceInfo {
      abbreviation
      division
      id
      name
      shortName
      srName
    }
    awayEndElo
    awayLineScores
    awayPoints
    awayPostgameWinProb
    awayStartElo
    awayTeam
    awayTeamId
    awayTeamInfo {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    conferenceGame
    excitement
    homeClassification
    homeConference
    homeConferenceId
    homeConferenceInfo {
      abbreviation
      division
      id
      name
      shortName
      srName
    }
    homeEndElo
    homeLineScores
    homePoints
    homePostgameWinProb
    homeStartElo
    homeTeam
    homeTeamId
    homeTeamInfo {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    id
    lines {
      gameId
      linesProviderId
      moneylineAway
      moneylineHome
      overUnder
      overUnderOpen
      provider {
        ...LinesProviderFragment
      }
      spread
      spreadOpen
    }
    linesAggregate {
      aggregate {
        ...GameLinesAggregateFieldsFragment
      }
      nodes {
        ...GameLinesFragment
      }
    }
    mediaInfo {
      mediaType
      name
    }
    neutralSite
    notes
    season
    seasonType
    startDate
    startTimeTbd
    status
    venueId
    weather {
      condition {
        ...WeatherConditionFragment
      }
      dewpoint
      gameId
      humidity
      precipitation
      pressure
      snowfall
      temperature
      weatherConditionCode
      windDirection
      windGust
      windSpeed
    }
    week
  }
}
Variables
{
  "distinctOn": ["attendance"],
  "limit": 123,
  "offset": 987,
  "orderBy": [gameOrderBy],
  "where": gameBoolExp
}
Response
{
  "data": {
    "game": [
      {
        "attendance": 987,
        "awayClassification": division,
        "awayConference": "abc123",
        "awayConferenceId": smallint,
        "awayConferenceInfo": Conference,
        "awayEndElo": 123,
        "awayLineScores": [smallint],
        "awayPoints": smallint,
        "awayPostgameWinProb": numeric,
        "awayStartElo": 987,
        "awayTeam": "xyz789",
        "awayTeamId": 123,
        "awayTeamInfo": currentTeams,
        "conferenceGame": true,
        "excitement": numeric,
        "homeClassification": division,
        "homeConference": "abc123",
        "homeConferenceId": smallint,
        "homeConferenceInfo": Conference,
        "homeEndElo": 123,
        "homeLineScores": [smallint],
        "homePoints": smallint,
        "homePostgameWinProb": numeric,
        "homeStartElo": 987,
        "homeTeam": "xyz789",
        "homeTeamId": 123,
        "homeTeamInfo": currentTeams,
        "id": 123,
        "lines": [GameLines],
        "linesAggregate": GameLinesAggregate,
        "mediaInfo": [GameMedia],
        "neutralSite": false,
        "notes": "xyz789",
        "season": smallint,
        "seasonType": season_type,
        "startDate": timestamp,
        "startTimeTbd": false,
        "status": game_status,
        "venueId": 123,
        "weather": GameWeather,
        "week": smallint
      }
    ]
  }
}
Subscriptions
gameAggregate
Description
fetch aggregated fields from the table: "game_info"

Response
Returns a gameAggregate!

Arguments
Name	Description
distinctOn - [gameSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [gameOrderBy!]	sort the rows by one or more columns
where - gameBoolExp	filter the rows returned
Example
Query
subscription GameAggregate(
  $distinctOn: [gameSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [gameOrderBy!],
  $where: gameBoolExp
) {
  gameAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...gameAvgFieldsFragment
      }
      count
      max {
        ...gameMaxFieldsFragment
      }
      min {
        ...gameMinFieldsFragment
      }
      stddev {
        ...gameStddevFieldsFragment
      }
      stddevPop {
        ...gameStddevPopFieldsFragment
      }
      stddevSamp {
        ...gameStddevSampFieldsFragment
      }
      sum {
        ...gameSumFieldsFragment
      }
      varPop {
        ...gameVarPopFieldsFragment
      }
      varSamp {
        ...gameVarSampFieldsFragment
      }
      variance {
        ...gameVarianceFieldsFragment
      }
    }
    nodes {
      attendance
      awayClassification
      awayConference
      awayConferenceId
      awayConferenceInfo {
        ...ConferenceFragment
      }
      awayEndElo
      awayLineScores
      awayPoints
      awayPostgameWinProb
      awayStartElo
      awayTeam
      awayTeamId
      awayTeamInfo {
        ...currentTeamsFragment
      }
      conferenceGame
      excitement
      homeClassification
      homeConference
      homeConferenceId
      homeConferenceInfo {
        ...ConferenceFragment
      }
      homeEndElo
      homeLineScores
      homePoints
      homePostgameWinProb
      homeStartElo
      homeTeam
      homeTeamId
      homeTeamInfo {
        ...currentTeamsFragment
      }
      id
      lines {
        ...GameLinesFragment
      }
      linesAggregate {
        ...GameLinesAggregateFragment
      }
      mediaInfo {
        ...GameMediaFragment
      }
      neutralSite
      notes
      season
      seasonType
      startDate
      startTimeTbd
      status
      venueId
      weather {
        ...GameWeatherFragment
      }
      week
    }
  }
}
Variables
{
  "distinctOn": ["attendance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [gameOrderBy],
  "where": gameBoolExp
}
Response
{
  "data": {
    "gameAggregate": {
      "aggregate": gameAggregateFields,
      "nodes": [game]
    }
  }
}
Subscriptions
gameLines
Description
fetch data from the table: "game_lines"

Response
Returns [GameLines!]!

Arguments
Name	Description
distinctOn - [GameLinesSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameLinesOrderBy!]	sort the rows by one or more columns
where - GameLinesBoolExp	filter the rows returned
Example
Query
subscription GameLines(
  $distinctOn: [GameLinesSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameLinesOrderBy!],
  $where: GameLinesBoolExp
) {
  gameLines(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    gameId
    linesProviderId
    moneylineAway
    moneylineHome
    overUnder
    overUnderOpen
    provider {
      id
      name
    }
    spread
    spreadOpen
  }
}
Variables
{
  "distinctOn": ["gameId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [GameLinesOrderBy],
  "where": GameLinesBoolExp
}
Response
{
  "data": {
    "gameLines": [
      {
        "gameId": 123,
        "linesProviderId": 987,
        "moneylineAway": 123,
        "moneylineHome": 987,
        "overUnder": numeric,
        "overUnderOpen": numeric,
        "provider": LinesProvider,
        "spread": numeric,
        "spreadOpen": numeric
      }
    ]
  }
}
Subscriptions
gameLinesAggregate
Description
fetch aggregated fields from the table: "game_lines"

Response
Returns a GameLinesAggregate!

Arguments
Name	Description
distinctOn - [GameLinesSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameLinesOrderBy!]	sort the rows by one or more columns
where - GameLinesBoolExp	filter the rows returned
Example
Query
subscription GameLinesAggregate(
  $distinctOn: [GameLinesSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameLinesOrderBy!],
  $where: GameLinesBoolExp
) {
  gameLinesAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...GameLinesAvgFieldsFragment
      }
      count
      max {
        ...GameLinesMaxFieldsFragment
      }
      min {
        ...GameLinesMinFieldsFragment
      }
      stddev {
        ...GameLinesStddevFieldsFragment
      }
      stddevPop {
        ...GameLinesStddevPopFieldsFragment
      }
      stddevSamp {
        ...GameLinesStddevSampFieldsFragment
      }
      sum {
        ...GameLinesSumFieldsFragment
      }
      varPop {
        ...GameLinesVarPopFieldsFragment
      }
      varSamp {
        ...GameLinesVarSampFieldsFragment
      }
      variance {
        ...GameLinesVarianceFieldsFragment
      }
    }
    nodes {
      gameId
      linesProviderId
      moneylineAway
      moneylineHome
      overUnder
      overUnderOpen
      provider {
        ...LinesProviderFragment
      }
      spread
      spreadOpen
    }
  }
}
Variables
{
  "distinctOn": ["gameId"],
  "limit": 987,
  "offset": 987,
  "orderBy": [GameLinesOrderBy],
  "where": GameLinesBoolExp
}
Response
{
  "data": {
    "gameLinesAggregate": {
      "aggregate": GameLinesAggregateFields,
      "nodes": [GameLines]
    }
  }
}
Subscriptions
gameMedia
Description
fetch data from the table: "game_media"

Response
Returns [GameMedia!]!

Arguments
Name	Description
distinctOn - [GameMediaSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameMediaOrderBy!]	sort the rows by one or more columns
where - GameMediaBoolExp	filter the rows returned
Example
Query
subscription GameMedia(
  $distinctOn: [GameMediaSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameMediaOrderBy!],
  $where: GameMediaBoolExp
) {
  gameMedia(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    mediaType
    name
  }
}
Variables
{
  "distinctOn": ["mediaType"],
  "limit": 123,
  "offset": 987,
  "orderBy": [GameMediaOrderBy],
  "where": GameMediaBoolExp
}
Response
{
  "data": {
    "gameMedia": [
      {
        "mediaType": media_type,
        "name": "xyz789"
      }
    ]
  }
}
Subscriptions
gamePlayerStat
Description
fetch data from the table: "game_player_stat"

Response
Returns [GamePlayerStat!]!

Arguments
Name	Description
distinctOn - [GamePlayerStatSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GamePlayerStatOrderBy!]	sort the rows by one or more columns
where - GamePlayerStatBoolExp	filter the rows returned
Example
Query
subscription GamePlayerStat(
  $distinctOn: [GamePlayerStatSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GamePlayerStatOrderBy!],
  $where: GamePlayerStatBoolExp
) {
  gamePlayerStat(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athleteId
    gameTeam {
      endElo
      game {
        ...gameFragment
      }
      gameId
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      homeAway
      lineScores
      points
      startElo
      teamId
      winProb
    }
    gameTeamId
    id
    playerStatCategory {
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      name
    }
    playerStatType {
      name
    }
    stat
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 123,
  "orderBy": [GamePlayerStatOrderBy],
  "where": GamePlayerStatBoolExp
}
Response
{
  "data": {
    "gamePlayerStat": [
      {
        "athlete": Athlete,
        "athleteId": bigint,
        "gameTeam": GameTeam,
        "gameTeamId": bigint,
        "id": bigint,
        "playerStatCategory": PlayerStatCategory,
        "playerStatType": PlayerStatType,
        "stat": "abc123"
      }
    ]
  }
}
Subscriptions
gamePlayerStatAggregate
Description
fetch aggregated fields from the table: "game_player_stat"

Response
Returns a GamePlayerStatAggregate!

Arguments
Name	Description
distinctOn - [GamePlayerStatSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GamePlayerStatOrderBy!]	sort the rows by one or more columns
where - GamePlayerStatBoolExp	filter the rows returned
Example
Query
subscription GamePlayerStatAggregate(
  $distinctOn: [GamePlayerStatSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GamePlayerStatOrderBy!],
  $where: GamePlayerStatBoolExp
) {
  gamePlayerStatAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...GamePlayerStatAvgFieldsFragment
      }
      count
      max {
        ...GamePlayerStatMaxFieldsFragment
      }
      min {
        ...GamePlayerStatMinFieldsFragment
      }
      stddev {
        ...GamePlayerStatStddevFieldsFragment
      }
      stddevPop {
        ...GamePlayerStatStddevPopFieldsFragment
      }
      stddevSamp {
        ...GamePlayerStatStddevSampFieldsFragment
      }
      sum {
        ...GamePlayerStatSumFieldsFragment
      }
      varPop {
        ...GamePlayerStatVarPopFieldsFragment
      }
      varSamp {
        ...GamePlayerStatVarSampFieldsFragment
      }
      variance {
        ...GamePlayerStatVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
  }
}
Variables
{
  "distinctOn": ["athleteId"],
  "limit": 123,
  "offset": 987,
  "orderBy": [GamePlayerStatOrderBy],
  "where": GamePlayerStatBoolExp
}
Response
{
  "data": {
    "gamePlayerStatAggregate": {
      "aggregate": GamePlayerStatAggregateFields,
      "nodes": [GamePlayerStat]
    }
  }
}
Subscriptions
gameTeam
Description
fetch data from the table: "game_team"

Response
Returns [GameTeam!]!

Arguments
Name	Description
distinctOn - [GameTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameTeamOrderBy!]	sort the rows by one or more columns
where - GameTeamBoolExp	filter the rows returned
Example
Query
subscription GameTeam(
  $distinctOn: [GameTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameTeamOrderBy!],
  $where: GameTeamBoolExp
) {
  gameTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    endElo
    game {
      attendance
      awayClassification
      awayConference
      awayConferenceId
      awayConferenceInfo {
        ...ConferenceFragment
      }
      awayEndElo
      awayLineScores
      awayPoints
      awayPostgameWinProb
      awayStartElo
      awayTeam
      awayTeamId
      awayTeamInfo {
        ...currentTeamsFragment
      }
      conferenceGame
      excitement
      homeClassification
      homeConference
      homeConferenceId
      homeConferenceInfo {
        ...ConferenceFragment
      }
      homeEndElo
      homeLineScores
      homePoints
      homePostgameWinProb
      homeStartElo
      homeTeam
      homeTeamId
      homeTeamInfo {
        ...currentTeamsFragment
      }
      id
      lines {
        ...GameLinesFragment
      }
      linesAggregate {
        ...GameLinesAggregateFragment
      }
      mediaInfo {
        ...GameMediaFragment
      }
      neutralSite
      notes
      season
      seasonType
      startDate
      startTimeTbd
      status
      venueId
      weather {
        ...GameWeatherFragment
      }
      week
    }
    gameId
    gamePlayerStats {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
    gamePlayerStatsAggregate {
      aggregate {
        ...GamePlayerStatAggregateFieldsFragment
      }
      nodes {
        ...GamePlayerStatFragment
      }
    }
    homeAway
    lineScores
    points
    startElo
    teamId
    winProb
  }
}
Variables
{
  "distinctOn": ["endElo"],
  "limit": 123,
  "offset": 123,
  "orderBy": [GameTeamOrderBy],
  "where": GameTeamBoolExp
}
Response
{
  "data": {
    "gameTeam": [
      {
        "endElo": 123,
        "game": game,
        "gameId": 123,
        "gamePlayerStats": [GamePlayerStat],
        "gamePlayerStatsAggregate": GamePlayerStatAggregate,
        "homeAway": home_away,
        "lineScores": [smallint],
        "points": smallint,
        "startElo": 987,
        "teamId": 987,
        "winProb": numeric
      }
    ]
  }
}
Subscriptions
gameWeather
Description
fetch data from the table: "game_weather"

Response
Returns [GameWeather!]!

Arguments
Name	Description
distinctOn - [GameWeatherSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [GameWeatherOrderBy!]	sort the rows by one or more columns
where - GameWeatherBoolExp	filter the rows returned
Example
Query
subscription GameWeather(
  $distinctOn: [GameWeatherSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [GameWeatherOrderBy!],
  $where: GameWeatherBoolExp
) {
  gameWeather(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    condition {
      description
      id
    }
    dewpoint
    gameId
    humidity
    precipitation
    pressure
    snowfall
    temperature
    weatherConditionCode
    windDirection
    windGust
    windSpeed
  }
}
Variables
{
  "distinctOn": ["dewpoint"],
  "limit": 123,
  "offset": 987,
  "orderBy": [GameWeatherOrderBy],
  "where": GameWeatherBoolExp
}
Response
{
  "data": {
    "gameWeather": [
      {
        "condition": WeatherCondition,
        "dewpoint": numeric,
        "gameId": 123,
        "humidity": numeric,
        "precipitation": numeric,
        "pressure": numeric,
        "snowfall": numeric,
        "temperature": numeric,
        "weatherConditionCode": smallint,
        "windDirection": numeric,
        "windGust": numeric,
        "windSpeed": numeric
      }
    ]
  }
}
Subscriptions
historicalTeam
Description
fetch data from the table: "team_info"

Response
Returns [historicalTeam!]!

Arguments
Name	Description
distinctOn - [historicalTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [historicalTeamOrderBy!]	sort the rows by one or more columns
where - historicalTeamBoolExp	filter the rows returned
Example
Query
subscription HistoricalTeam(
  $distinctOn: [historicalTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [historicalTeamOrderBy!],
  $where: historicalTeamBoolExp
) {
  historicalTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    active
    altColor
    altName
    classification
    color
    conference
    conferenceAbbreviation
    conferenceId
    conferenceShortName
    countryCode
    displayName
    division
    endYear
    id
    images
    mascot
    ncaaName
    nickname
    school
    shortDisplayName
    startYear
    twitter
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 123,
  "orderBy": [historicalTeamOrderBy],
  "where": historicalTeamBoolExp
}
Response
{
  "data": {
    "historicalTeam": [
      {
        "abbreviation": "xyz789",
        "active": true,
        "altColor": "xyz789",
        "altName": "xyz789",
        "classification": division,
        "color": "abc123",
        "conference": "abc123",
        "conferenceAbbreviation": "xyz789",
        "conferenceId": smallint,
        "conferenceShortName": "xyz789",
        "countryCode": "abc123",
        "displayName": "xyz789",
        "division": "abc123",
        "endYear": smallint,
        "id": 123,
        "images": ["xyz789"],
        "mascot": "abc123",
        "ncaaName": "abc123",
        "nickname": "xyz789",
        "school": "xyz789",
        "shortDisplayName": "xyz789",
        "startYear": smallint,
        "twitter": "xyz789"
      }
    ]
  }
}
Subscriptions
historicalTeamAggregate
Description
fetch aggregated fields from the table: "team_info"

Response
Returns a historicalTeamAggregate!

Arguments
Name	Description
distinctOn - [historicalTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [historicalTeamOrderBy!]	sort the rows by one or more columns
where - historicalTeamBoolExp	filter the rows returned
Example
Query
subscription HistoricalTeamAggregate(
  $distinctOn: [historicalTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [historicalTeamOrderBy!],
  $where: historicalTeamBoolExp
) {
  historicalTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...historicalTeamAvgFieldsFragment
      }
      count
      max {
        ...historicalTeamMaxFieldsFragment
      }
      min {
        ...historicalTeamMinFieldsFragment
      }
      stddev {
        ...historicalTeamStddevFieldsFragment
      }
      stddevPop {
        ...historicalTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...historicalTeamStddevSampFieldsFragment
      }
      sum {
        ...historicalTeamSumFieldsFragment
      }
      varPop {
        ...historicalTeamVarPopFieldsFragment
      }
      varSamp {
        ...historicalTeamVarSampFieldsFragment
      }
      variance {
        ...historicalTeamVarianceFieldsFragment
      }
    }
    nodes {
      abbreviation
      active
      altColor
      altName
      classification
      color
      conference
      conferenceAbbreviation
      conferenceId
      conferenceShortName
      countryCode
      displayName
      division
      endYear
      id
      images
      mascot
      ncaaName
      nickname
      school
      shortDisplayName
      startYear
      twitter
    }
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 987,
  "orderBy": [historicalTeamOrderBy],
  "where": historicalTeamBoolExp
}
Response
{
  "data": {
    "historicalTeamAggregate": {
      "aggregate": historicalTeamAggregateFields,
      "nodes": [historicalTeam]
    }
  }
}
Subscriptions
hometown
Description
fetch data from the table: "hometown"

Response
Returns [Hometown!]!

Arguments
Name	Description
distinctOn - [HometownSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [HometownOrderBy!]	sort the rows by one or more columns
where - HometownBoolExp	filter the rows returned
Example
Query
subscription Hometown(
  $distinctOn: [HometownSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [HometownOrderBy!],
  $where: HometownBoolExp
) {
  hometown(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athletes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athletesAggregate {
      aggregate {
        ...AthleteAggregateFieldsFragment
      }
      nodes {
        ...AthleteFragment
      }
    }
    city
    country
    countyFips
    latitude
    longitude
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
    state
  }
}
Variables
{
  "distinctOn": ["city"],
  "limit": 123,
  "offset": 987,
  "orderBy": [HometownOrderBy],
  "where": HometownBoolExp
}
Response
{
  "data": {
    "hometown": [
      {
        "athletes": [Athlete],
        "athletesAggregate": AthleteAggregate,
        "city": "abc123",
        "country": "abc123",
        "countyFips": "abc123",
        "latitude": numeric,
        "longitude": numeric,
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate,
        "state": "abc123"
      }
    ]
  }
}
Subscriptions
hometownAggregate
Description
fetch aggregated fields from the table: "hometown"

Response
Returns a HometownAggregate!

Arguments
Name	Description
distinctOn - [HometownSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [HometownOrderBy!]	sort the rows by one or more columns
where - HometownBoolExp	filter the rows returned
Example
Query
subscription HometownAggregate(
  $distinctOn: [HometownSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [HometownOrderBy!],
  $where: HometownBoolExp
) {
  hometownAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...HometownAvgFieldsFragment
      }
      count
      max {
        ...HometownMaxFieldsFragment
      }
      min {
        ...HometownMinFieldsFragment
      }
      stddev {
        ...HometownStddevFieldsFragment
      }
      stddevPop {
        ...HometownStddevPopFieldsFragment
      }
      stddevSamp {
        ...HometownStddevSampFieldsFragment
      }
      sum {
        ...HometownSumFieldsFragment
      }
      varPop {
        ...HometownVarPopFieldsFragment
      }
      varSamp {
        ...HometownVarSampFieldsFragment
      }
      variance {
        ...HometownVarianceFieldsFragment
      }
    }
    nodes {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
  }
}
Variables
{
  "distinctOn": ["city"],
  "limit": 123,
  "offset": 987,
  "orderBy": [HometownOrderBy],
  "where": HometownBoolExp
}
Response
{
  "data": {
    "hometownAggregate": {
      "aggregate": HometownAggregateFields,
      "nodes": [Hometown]
    }
  }
}
Subscriptions
linesProvider
Description
fetch data from the table: "lines_provider"

Response
Returns [LinesProvider!]!

Arguments
Name	Description
distinctOn - [LinesProviderSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [LinesProviderOrderBy!]	sort the rows by one or more columns
where - LinesProviderBoolExp	filter the rows returned
Example
Query
subscription LinesProvider(
  $distinctOn: [LinesProviderSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [LinesProviderOrderBy!],
  $where: LinesProviderBoolExp
) {
  linesProvider(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    name
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [LinesProviderOrderBy],
  "where": LinesProviderBoolExp
}
Response
{
  "data": {
    "linesProvider": [
      {"id": 987, "name": "xyz789"}
    ]
  }
}
Subscriptions
linesProviderAggregate
Description
fetch aggregated fields from the table: "lines_provider"

Response
Returns a LinesProviderAggregate!

Arguments
Name	Description
distinctOn - [LinesProviderSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [LinesProviderOrderBy!]	sort the rows by one or more columns
where - LinesProviderBoolExp	filter the rows returned
Example
Query
subscription LinesProviderAggregate(
  $distinctOn: [LinesProviderSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [LinesProviderOrderBy!],
  $where: LinesProviderBoolExp
) {
  linesProviderAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...LinesProviderAvgFieldsFragment
      }
      count
      max {
        ...LinesProviderMaxFieldsFragment
      }
      min {
        ...LinesProviderMinFieldsFragment
      }
      stddev {
        ...LinesProviderStddevFieldsFragment
      }
      stddevPop {
        ...LinesProviderStddevPopFieldsFragment
      }
      stddevSamp {
        ...LinesProviderStddevSampFieldsFragment
      }
      sum {
        ...LinesProviderSumFieldsFragment
      }
      varPop {
        ...LinesProviderVarPopFieldsFragment
      }
      varSamp {
        ...LinesProviderVarSampFieldsFragment
      }
      variance {
        ...LinesProviderVarianceFieldsFragment
      }
    }
    nodes {
      id
      name
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 123,
  "offset": 987,
  "orderBy": [LinesProviderOrderBy],
  "where": LinesProviderBoolExp
}
Response
{
  "data": {
    "linesProviderAggregate": {
      "aggregate": LinesProviderAggregateFields,
      "nodes": [LinesProvider]
    }
  }
}
Subscriptions
playerStatCategory
Description
fetch data from the table: "player_stat_category"

Response
Returns [PlayerStatCategory!]!

Arguments
Name	Description
distinctOn - [PlayerStatCategorySelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatCategoryOrderBy!]	sort the rows by one or more columns
where - PlayerStatCategoryBoolExp	filter the rows returned
Example
Query
subscription PlayerStatCategory(
  $distinctOn: [PlayerStatCategorySelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatCategoryOrderBy!],
  $where: PlayerStatCategoryBoolExp
) {
  playerStatCategory(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    gamePlayerStats {
      athlete {
        ...AthleteFragment
      }
      athleteId
      gameTeam {
        ...GameTeamFragment
      }
      gameTeamId
      id
      playerStatCategory {
        ...PlayerStatCategoryFragment
      }
      playerStatType {
        ...PlayerStatTypeFragment
      }
      stat
    }
    gamePlayerStatsAggregate {
      aggregate {
        ...GamePlayerStatAggregateFieldsFragment
      }
      nodes {
        ...GamePlayerStatFragment
      }
    }
    name
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 123,
  "offset": 123,
  "orderBy": [PlayerStatCategoryOrderBy],
  "where": PlayerStatCategoryBoolExp
}
Response
{
  "data": {
    "playerStatCategory": [
      {
        "gamePlayerStats": [GamePlayerStat],
        "gamePlayerStatsAggregate": GamePlayerStatAggregate,
        "name": "xyz789"
      }
    ]
  }
}
Subscriptions
playerStatCategoryAggregate
Description
fetch aggregated fields from the table: "player_stat_category"

Response
Returns a PlayerStatCategoryAggregate!

Arguments
Name	Description
distinctOn - [PlayerStatCategorySelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatCategoryOrderBy!]	sort the rows by one or more columns
where - PlayerStatCategoryBoolExp	filter the rows returned
Example
Query
subscription PlayerStatCategoryAggregate(
  $distinctOn: [PlayerStatCategorySelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatCategoryOrderBy!],
  $where: PlayerStatCategoryBoolExp
) {
  playerStatCategoryAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      count
      max {
        ...PlayerStatCategoryMaxFieldsFragment
      }
      min {
        ...PlayerStatCategoryMinFieldsFragment
      }
    }
    nodes {
      gamePlayerStats {
        ...GamePlayerStatFragment
      }
      gamePlayerStatsAggregate {
        ...GamePlayerStatAggregateFragment
      }
      name
    }
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PlayerStatCategoryOrderBy],
  "where": PlayerStatCategoryBoolExp
}
Response
{
  "data": {
    "playerStatCategoryAggregate": {
      "aggregate": PlayerStatCategoryAggregateFields,
      "nodes": [PlayerStatCategory]
    }
  }
}
Subscriptions
playerStatType
Description
fetch data from the table: "player_stat_type"

Response
Returns [PlayerStatType!]!

Arguments
Name	Description
distinctOn - [PlayerStatTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatTypeOrderBy!]	sort the rows by one or more columns
where - PlayerStatTypeBoolExp	filter the rows returned
Example
Query
subscription PlayerStatType(
  $distinctOn: [PlayerStatTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatTypeOrderBy!],
  $where: PlayerStatTypeBoolExp
) {
  playerStatType(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    name
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 123,
  "offset": 123,
  "orderBy": [PlayerStatTypeOrderBy],
  "where": PlayerStatTypeBoolExp
}
Response
{
  "data": {
    "playerStatType": [{"name": "abc123"}]
  }
}
Subscriptions
playerStatTypeAggregate
Description
fetch aggregated fields from the table: "player_stat_type"

Response
Returns a PlayerStatTypeAggregate!

Arguments
Name	Description
distinctOn - [PlayerStatTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PlayerStatTypeOrderBy!]	sort the rows by one or more columns
where - PlayerStatTypeBoolExp	filter the rows returned
Example
Query
subscription PlayerStatTypeAggregate(
  $distinctOn: [PlayerStatTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PlayerStatTypeOrderBy!],
  $where: PlayerStatTypeBoolExp
) {
  playerStatTypeAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      count
      max {
        ...PlayerStatTypeMaxFieldsFragment
      }
      min {
        ...PlayerStatTypeMinFieldsFragment
      }
    }
    nodes {
      name
    }
  }
}
Variables
{
  "distinctOn": ["name"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PlayerStatTypeOrderBy],
  "where": PlayerStatTypeBoolExp
}
Response
{
  "data": {
    "playerStatTypeAggregate": {
      "aggregate": PlayerStatTypeAggregateFields,
      "nodes": [PlayerStatType]
    }
  }
}
Subscriptions
poll
Description
fetch data from the table: "poll"

Response
Returns [Poll!]!

Arguments
Name	Description
distinctOn - [PollSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollOrderBy!]	sort the rows by one or more columns
where - PollBoolExp	filter the rows returned
Example
Query
subscription Poll(
  $distinctOn: [PollSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollOrderBy!],
  $where: PollBoolExp
) {
  poll(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    pollType {
      abbreviation
      id
      name
      polls {
        ...PollFragment
      }
      shortName
    }
    rankings {
      firstPlaceVotes
      points
      poll {
        ...PollFragment
      }
      rank
      team {
        ...currentTeamsFragment
      }
    }
    season
    seasonType
    week
  }
}
Variables
{
  "distinctOn": ["season"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PollOrderBy],
  "where": PollBoolExp
}
Response
{
  "data": {
    "poll": [
      {
        "pollType": PollType,
        "rankings": [PollRank],
        "season": 987,
        "seasonType": season_type,
        "week": smallint
      }
    ]
  }
}
Subscriptions
pollRank
Description
fetch data from the table: "poll_rank"

Response
Returns [PollRank!]!

Arguments
Name	Description
distinctOn - [PollRankSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollRankOrderBy!]	sort the rows by one or more columns
where - PollRankBoolExp	filter the rows returned
Example
Query
subscription PollRank(
  $distinctOn: [PollRankSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollRankOrderBy!],
  $where: PollRankBoolExp
) {
  pollRank(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    firstPlaceVotes
    points
    poll {
      pollType {
        ...PollTypeFragment
      }
      rankings {
        ...PollRankFragment
      }
      season
      seasonType
      week
    }
    rank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
  }
}
Variables
{
  "distinctOn": ["firstPlaceVotes"],
  "limit": 987,
  "offset": 987,
  "orderBy": [PollRankOrderBy],
  "where": PollRankBoolExp
}
Response
{
  "data": {
    "pollRank": [
      {
        "firstPlaceVotes": smallint,
        "points": 987,
        "poll": Poll,
        "rank": smallint,
        "team": currentTeams
      }
    ]
  }
}
Subscriptions
pollType
Description
fetch data from the table: "poll_type"

Response
Returns [PollType!]!

Arguments
Name	Description
distinctOn - [PollTypeSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PollTypeOrderBy!]	sort the rows by one or more columns
where - PollTypeBoolExp	filter the rows returned
Example
Query
subscription PollType(
  $distinctOn: [PollTypeSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PollTypeOrderBy!],
  $where: PollTypeBoolExp
) {
  pollType(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    id
    name
    polls {
      pollType {
        ...PollTypeFragment
      }
      rankings {
        ...PollRankFragment
      }
      season
      seasonType
      week
    }
    shortName
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 123,
  "offset": 987,
  "orderBy": [PollTypeOrderBy],
  "where": PollTypeBoolExp
}
Response
{
  "data": {
    "pollType": [
      {
        "abbreviation": "xyz789",
        "id": 123,
        "name": "xyz789",
        "polls": [Poll],
        "shortName": "xyz789"
      }
    ]
  }
}
Subscriptions
position
Description
fetch data from the table: "position"

Response
Returns [Position!]!

Arguments
Name	Description
distinctOn - [PositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [PositionOrderBy!]	sort the rows by one or more columns
where - PositionBoolExp	filter the rows returned
Example
Query
subscription Position(
  $distinctOn: [PositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [PositionOrderBy!],
  $where: PositionBoolExp
) {
  position(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    abbreviation
    athletes {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    athletesAggregate {
      aggregate {
        ...AthleteAggregateFieldsFragment
      }
      nodes {
        ...AthleteFragment
      }
    }
    displayName
    id
    name
  }
}
Variables
{
  "distinctOn": ["abbreviation"],
  "limit": 987,
  "offset": 123,
  "orderBy": [PositionOrderBy],
  "where": PositionBoolExp
}
Response
{
  "data": {
    "position": [
      {
        "abbreviation": "abc123",
        "athletes": [Athlete],
        "athletesAggregate": AthleteAggregate,
        "displayName": "xyz789",
        "id": smallint,
        "name": "xyz789"
      }
    ]
  }
}
Subscriptions
predictedPoints
Description
fetch data from the table: "ppa"

Response
Returns [predictedPoints!]!

Arguments
Name	Description
distinctOn - [predictedPointsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [predictedPointsOrderBy!]	sort the rows by one or more columns
where - predictedPointsBoolExp	filter the rows returned
Example
Query
subscription PredictedPoints(
  $distinctOn: [predictedPointsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [predictedPointsOrderBy!],
  $where: predictedPointsBoolExp
) {
  predictedPoints(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    distance
    down
    predictedPoints
    yardLine
  }
}
Variables
{
  "distinctOn": ["distance"],
  "limit": 123,
  "offset": 987,
  "orderBy": [predictedPointsOrderBy],
  "where": predictedPointsBoolExp
}
Response
{
  "data": {
    "predictedPoints": [
      {
        "distance": smallint,
        "down": smallint,
        "predictedPoints": numeric,
        "yardLine": smallint
      }
    ]
  }
}
Subscriptions
predictedPointsAggregate
Description
fetch aggregated fields from the table: "ppa"

Response
Returns a predictedPointsAggregate!

Arguments
Name	Description
distinctOn - [predictedPointsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [predictedPointsOrderBy!]	sort the rows by one or more columns
where - predictedPointsBoolExp	filter the rows returned
Example
Query
subscription PredictedPointsAggregate(
  $distinctOn: [predictedPointsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [predictedPointsOrderBy!],
  $where: predictedPointsBoolExp
) {
  predictedPointsAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...predictedPointsAvgFieldsFragment
      }
      count
      max {
        ...predictedPointsMaxFieldsFragment
      }
      min {
        ...predictedPointsMinFieldsFragment
      }
      stddev {
        ...predictedPointsStddevFieldsFragment
      }
      stddevPop {
        ...predictedPointsStddevPopFieldsFragment
      }
      stddevSamp {
        ...predictedPointsStddevSampFieldsFragment
      }
      sum {
        ...predictedPointsSumFieldsFragment
      }
      varPop {
        ...predictedPointsVarPopFieldsFragment
      }
      varSamp {
        ...predictedPointsVarSampFieldsFragment
      }
      variance {
        ...predictedPointsVarianceFieldsFragment
      }
    }
    nodes {
      distance
      down
      predictedPoints
      yardLine
    }
  }
}
Variables
{
  "distinctOn": ["distance"],
  "limit": 123,
  "offset": 123,
  "orderBy": [predictedPointsOrderBy],
  "where": predictedPointsBoolExp
}
Response
{
  "data": {
    "predictedPointsAggregate": {
      "aggregate": predictedPointsAggregateFields,
      "nodes": [predictedPoints]
    }
  }
}
Subscriptions
ratings
Description
fetch data from the table: "rating_systems"

Response
Returns [ratings!]!

Arguments
Name	Description
distinctOn - [ratingsSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ratingsOrderBy!]	sort the rows by one or more columns
where - ratingsBoolExp	filter the rows returned
Example
Query
subscription Ratings(
  $distinctOn: [ratingsSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ratingsOrderBy!],
  $where: ratingsBoolExp
) {
  ratings(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    conference
    conferenceId
    elo
    fpi
    fpiAvgWinProbabilityRank
    fpiDefensiveEfficiency
    fpiGameControlRank
    fpiOffensiveEfficiency
    fpiOverallEfficiency
    fpiRemainingSosRank
    fpiResumeRank
    fpiSosRank
    fpiSpecialTeamsEfficiency
    fpiStrengthOfRecordRank
    spDefense
    spOffense
    spOverall
    spSpecialTeams
    srs
    team
    teamId
    year
  }
}
Variables
{
  "distinctOn": ["conference"],
  "limit": 123,
  "offset": 987,
  "orderBy": [ratingsOrderBy],
  "where": ratingsBoolExp
}
Response
{
  "data": {
    "ratings": [
      {
        "conference": "abc123",
        "conferenceId": smallint,
        "elo": 123,
        "fpi": numeric,
        "fpiAvgWinProbabilityRank": smallint,
        "fpiDefensiveEfficiency": numeric,
        "fpiGameControlRank": smallint,
        "fpiOffensiveEfficiency": numeric,
        "fpiOverallEfficiency": numeric,
        "fpiRemainingSosRank": smallint,
        "fpiResumeRank": smallint,
        "fpiSosRank": smallint,
        "fpiSpecialTeamsEfficiency": numeric,
        "fpiStrengthOfRecordRank": smallint,
        "spDefense": numeric,
        "spOffense": numeric,
        "spOverall": numeric,
        "spSpecialTeams": numeric,
        "srs": numeric,
        "team": "xyz789",
        "teamId": 987,
        "year": smallint
      }
    ]
  }
}
Subscriptions
recruit
Description
fetch data from the table: "recruit"

Response
Returns [Recruit!]!

Arguments
Name	Description
distinctOn - [RecruitSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitOrderBy!]	sort the rows by one or more columns
where - RecruitBoolExp	filter the rows returned
Example
Query
subscription Recruit(
  $distinctOn: [RecruitSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitOrderBy!],
  $where: RecruitBoolExp
) {
  recruit(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    athlete {
      adjustedPlayerMetrics {
        ...AdjustedPlayerMetricsFragment
      }
      adjustedPlayerMetricsAggregate {
        ...AdjustedPlayerMetricsAggregateFragment
      }
      athleteTeams {
        ...AthleteTeamFragment
      }
      athleteTeamsAggregate {
        ...AthleteTeamAggregateFragment
      }
      firstName
      height
      hometown {
        ...HometownFragment
      }
      hometownId
      id
      jersey
      lastName
      name
      position {
        ...PositionFragment
      }
      positionId
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      teamId
      weight
    }
    college {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    height
    hometown {
      athletes {
        ...AthleteFragment
      }
      athletesAggregate {
        ...AthleteAggregateFragment
      }
      city
      country
      countyFips
      latitude
      longitude
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
      state
    }
    id
    name
    overallRank
    position {
      id
      position
      positionGroup
    }
    positionRank
    ranking
    rating
    recruitSchool {
      id
      name
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
    }
    recruitType
    stars
    weight
    year
  }
}
Variables
{
  "distinctOn": ["height"],
  "limit": 987,
  "offset": 987,
  "orderBy": [RecruitOrderBy],
  "where": RecruitBoolExp
}
Response
{
  "data": {
    "recruit": [
      {
        "athlete": Athlete,
        "college": currentTeams,
        "height": 987.65,
        "hometown": Hometown,
        "id": bigint,
        "name": "xyz789",
        "overallRank": smallint,
        "position": RecruitPosition,
        "positionRank": smallint,
        "ranking": smallint,
        "rating": 123.45,
        "recruitSchool": RecruitSchool,
        "recruitType": recruit_type,
        "stars": smallint,
        "weight": smallint,
        "year": smallint
      }
    ]
  }
}
Subscriptions
recruitAggregate
Description
fetch aggregated fields from the table: "recruit"

Response
Returns a RecruitAggregate!

Arguments
Name	Description
distinctOn - [RecruitSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitOrderBy!]	sort the rows by one or more columns
where - RecruitBoolExp	filter the rows returned
Example
Query
subscription RecruitAggregate(
  $distinctOn: [RecruitSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitOrderBy!],
  $where: RecruitBoolExp
) {
  recruitAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitAvgFieldsFragment
      }
      count
      max {
        ...RecruitMaxFieldsFragment
      }
      min {
        ...RecruitMinFieldsFragment
      }
      stddev {
        ...RecruitStddevFieldsFragment
      }
      stddevPop {
        ...RecruitStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitStddevSampFieldsFragment
      }
      sum {
        ...RecruitSumFieldsFragment
      }
      varPop {
        ...RecruitVarPopFieldsFragment
      }
      varSamp {
        ...RecruitVarSampFieldsFragment
      }
      variance {
        ...RecruitVarianceFieldsFragment
      }
    }
    nodes {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
  }
}
Variables
{
  "distinctOn": ["height"],
  "limit": 123,
  "offset": 987,
  "orderBy": [RecruitOrderBy],
  "where": RecruitBoolExp
}
Response
{
  "data": {
    "recruitAggregate": {
      "aggregate": RecruitAggregateFields,
      "nodes": [Recruit]
    }
  }
}
Subscriptions
recruitPosition
Description
fetch data from the table: "recruit_position"

Response
Returns [RecruitPosition!]!

Arguments
Name	Description
distinctOn - [RecruitPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitPositionOrderBy!]	sort the rows by one or more columns
where - RecruitPositionBoolExp	filter the rows returned
Example
Query
subscription RecruitPosition(
  $distinctOn: [RecruitPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitPositionOrderBy!],
  $where: RecruitPositionBoolExp
) {
  recruitPosition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    position
    positionGroup
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 123,
  "offset": 123,
  "orderBy": [RecruitPositionOrderBy],
  "where": RecruitPositionBoolExp
}
Response
{
  "data": {
    "recruitPosition": [
      {
        "id": smallint,
        "position": "abc123",
        "positionGroup": "xyz789"
      }
    ]
  }
}
Subscriptions
recruitPositionAggregate
Description
fetch aggregated fields from the table: "recruit_position"

Response
Returns a RecruitPositionAggregate!

Arguments
Name	Description
distinctOn - [RecruitPositionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitPositionOrderBy!]	sort the rows by one or more columns
where - RecruitPositionBoolExp	filter the rows returned
Example
Query
subscription RecruitPositionAggregate(
  $distinctOn: [RecruitPositionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitPositionOrderBy!],
  $where: RecruitPositionBoolExp
) {
  recruitPositionAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitPositionAvgFieldsFragment
      }
      count
      max {
        ...RecruitPositionMaxFieldsFragment
      }
      min {
        ...RecruitPositionMinFieldsFragment
      }
      stddev {
        ...RecruitPositionStddevFieldsFragment
      }
      stddevPop {
        ...RecruitPositionStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitPositionStddevSampFieldsFragment
      }
      sum {
        ...RecruitPositionSumFieldsFragment
      }
      varPop {
        ...RecruitPositionVarPopFieldsFragment
      }
      varSamp {
        ...RecruitPositionVarSampFieldsFragment
      }
      variance {
        ...RecruitPositionVarianceFieldsFragment
      }
    }
    nodes {
      id
      position
      positionGroup
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 987,
  "orderBy": [RecruitPositionOrderBy],
  "where": RecruitPositionBoolExp
}
Response
{
  "data": {
    "recruitPositionAggregate": {
      "aggregate": RecruitPositionAggregateFields,
      "nodes": [RecruitPosition]
    }
  }
}
Subscriptions
recruitSchool
Description
fetch data from the table: "recruit_school"

Response
Returns [RecruitSchool!]!

Arguments
Name	Description
distinctOn - [RecruitSchoolSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitSchoolOrderBy!]	sort the rows by one or more columns
where - RecruitSchoolBoolExp	filter the rows returned
Example
Query
subscription RecruitSchool(
  $distinctOn: [RecruitSchoolSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitSchoolOrderBy!],
  $where: RecruitSchoolBoolExp
) {
  recruitSchool(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    name
    recruits {
      athlete {
        ...AthleteFragment
      }
      college {
        ...currentTeamsFragment
      }
      height
      hometown {
        ...HometownFragment
      }
      id
      name
      overallRank
      position {
        ...RecruitPositionFragment
      }
      positionRank
      ranking
      rating
      recruitSchool {
        ...RecruitSchoolFragment
      }
      recruitType
      stars
      weight
      year
    }
    recruitsAggregate {
      aggregate {
        ...RecruitAggregateFieldsFragment
      }
      nodes {
        ...RecruitFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 123,
  "offset": 123,
  "orderBy": [RecruitSchoolOrderBy],
  "where": RecruitSchoolBoolExp
}
Response
{
  "data": {
    "recruitSchool": [
      {
        "id": 123,
        "name": "xyz789",
        "recruits": [Recruit],
        "recruitsAggregate": RecruitAggregate
      }
    ]
  }
}
Subscriptions
recruitSchoolAggregate
Description
fetch aggregated fields from the table: "recruit_school"

Response
Returns a RecruitSchoolAggregate!

Arguments
Name	Description
distinctOn - [RecruitSchoolSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitSchoolOrderBy!]	sort the rows by one or more columns
where - RecruitSchoolBoolExp	filter the rows returned
Example
Query
subscription RecruitSchoolAggregate(
  $distinctOn: [RecruitSchoolSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitSchoolOrderBy!],
  $where: RecruitSchoolBoolExp
) {
  recruitSchoolAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitSchoolAvgFieldsFragment
      }
      count
      max {
        ...RecruitSchoolMaxFieldsFragment
      }
      min {
        ...RecruitSchoolMinFieldsFragment
      }
      stddev {
        ...RecruitSchoolStddevFieldsFragment
      }
      stddevPop {
        ...RecruitSchoolStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitSchoolStddevSampFieldsFragment
      }
      sum {
        ...RecruitSchoolSumFieldsFragment
      }
      varPop {
        ...RecruitSchoolVarPopFieldsFragment
      }
      varSamp {
        ...RecruitSchoolVarSampFieldsFragment
      }
      variance {
        ...RecruitSchoolVarianceFieldsFragment
      }
    }
    nodes {
      id
      name
      recruits {
        ...RecruitFragment
      }
      recruitsAggregate {
        ...RecruitAggregateFragment
      }
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 987,
  "orderBy": [RecruitSchoolOrderBy],
  "where": RecruitSchoolBoolExp
}
Response
{
  "data": {
    "recruitSchoolAggregate": {
      "aggregate": RecruitSchoolAggregateFields,
      "nodes": [RecruitSchool]
    }
  }
}
Subscriptions
recruitingTeam
Description
fetch data from the table: "recruiting_team"

Response
Returns [RecruitingTeam!]!

Arguments
Name	Description
distinctOn - [RecruitingTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitingTeamOrderBy!]	sort the rows by one or more columns
where - RecruitingTeamBoolExp	filter the rows returned
Example
Query
subscription RecruitingTeam(
  $distinctOn: [RecruitingTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitingTeamOrderBy!],
  $where: RecruitingTeamBoolExp
) {
  recruitingTeam(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    id
    points
    rank
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    year
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 123,
  "orderBy": [RecruitingTeamOrderBy],
  "where": RecruitingTeamBoolExp
}
Response
{
  "data": {
    "recruitingTeam": [
      {
        "id": 987,
        "points": numeric,
        "rank": smallint,
        "team": currentTeams,
        "year": smallint
      }
    ]
  }
}
Subscriptions
recruitingTeamAggregate
Description
fetch aggregated fields from the table: "recruiting_team"

Response
Returns a RecruitingTeamAggregate!

Arguments
Name	Description
distinctOn - [RecruitingTeamSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [RecruitingTeamOrderBy!]	sort the rows by one or more columns
where - RecruitingTeamBoolExp	filter the rows returned
Example
Query
subscription RecruitingTeamAggregate(
  $distinctOn: [RecruitingTeamSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [RecruitingTeamOrderBy!],
  $where: RecruitingTeamBoolExp
) {
  recruitingTeamAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...RecruitingTeamAvgFieldsFragment
      }
      count
      max {
        ...RecruitingTeamMaxFieldsFragment
      }
      min {
        ...RecruitingTeamMinFieldsFragment
      }
      stddev {
        ...RecruitingTeamStddevFieldsFragment
      }
      stddevPop {
        ...RecruitingTeamStddevPopFieldsFragment
      }
      stddevSamp {
        ...RecruitingTeamStddevSampFieldsFragment
      }
      sum {
        ...RecruitingTeamSumFieldsFragment
      }
      varPop {
        ...RecruitingTeamVarPopFieldsFragment
      }
      varSamp {
        ...RecruitingTeamVarSampFieldsFragment
      }
      variance {
        ...RecruitingTeamVarianceFieldsFragment
      }
    }
    nodes {
      id
      points
      rank
      team {
        ...currentTeamsFragment
      }
      year
    }
  }
}
Variables
{
  "distinctOn": ["id"],
  "limit": 987,
  "offset": 987,
  "orderBy": [RecruitingTeamOrderBy],
  "where": RecruitingTeamBoolExp
}
Response
{
  "data": {
    "recruitingTeamAggregate": {
      "aggregate": RecruitingTeamAggregateFields,
      "nodes": [RecruitingTeam]
    }
  }
}
Subscriptions
scoreboard
Description
fetch data from the table: "scoreboard"

Response
Returns [Scoreboard!]!

Arguments
Name	Description
distinctOn - [ScoreboardSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [ScoreboardOrderBy!]	sort the rows by one or more columns
where - ScoreboardBoolExp	filter the rows returned
Example
Query
subscription Scoreboard(
  $distinctOn: [ScoreboardSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [ScoreboardOrderBy!],
  $where: ScoreboardBoolExp
) {
  scoreboard(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    awayClassification
    awayConference
    awayConferenceAbbreviation
    awayId
    awayLineScores
    awayPoints
    awayTeam
    city
    conferenceGame
    currentClock
    currentPeriod
    currentPossession
    currentSituation
    homeClassification
    homeConference
    homeConferenceAbbreviation
    homeId
    homeLineScores
    homePoints
    homeTeam
    id
    lastPlay
    moneylineAway
    moneylineHome
    neutralSite
    overUnder
    spread
    startDate
    startTimeTbd
    state
    status
    temperature
    tv
    venue
    weatherDescription
    windDirection
    windSpeed
  }
}
Variables
{
  "distinctOn": ["awayClassification"],
  "limit": 123,
  "offset": 123,
  "orderBy": [ScoreboardOrderBy],
  "where": ScoreboardBoolExp
}
Response
{
  "data": {
    "scoreboard": [
      {
        "awayClassification": division,
        "awayConference": "xyz789",
        "awayConferenceAbbreviation": "abc123",
        "awayId": 987,
        "awayLineScores": [smallint],
        "awayPoints": smallint,
        "awayTeam": "abc123",
        "city": "xyz789",
        "conferenceGame": true,
        "currentClock": "xyz789",
        "currentPeriod": smallint,
        "currentPossession": "abc123",
        "currentSituation": "abc123",
        "homeClassification": division,
        "homeConference": "abc123",
        "homeConferenceAbbreviation": "abc123",
        "homeId": 123,
        "homeLineScores": [smallint],
        "homePoints": smallint,
        "homeTeam": "xyz789",
        "id": 987,
        "lastPlay": "abc123",
        "moneylineAway": 987,
        "moneylineHome": 987,
        "neutralSite": false,
        "overUnder": numeric,
        "spread": numeric,
        "startDate": timestamptz,
        "startTimeTbd": false,
        "state": "abc123",
        "status": game_status,
        "temperature": numeric,
        "tv": "abc123",
        "venue": "xyz789",
        "weatherDescription": "xyz789",
        "windDirection": numeric,
        "windSpeed": numeric
      }
    ]
  }
}
Subscriptions
teamTalent
Description
fetch data from the table: "team_talent"

Response
Returns [TeamTalent!]!

Arguments
Name	Description
distinctOn - [TeamTalentSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TeamTalentOrderBy!]	sort the rows by one or more columns
where - TeamTalentBoolExp	filter the rows returned
Example
Query
subscription TeamTalent(
  $distinctOn: [TeamTalentSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TeamTalentOrderBy!],
  $where: TeamTalentBoolExp
) {
  teamTalent(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    talent
    team {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    year
  }
}
Variables
{
  "distinctOn": ["talent"],
  "limit": 987,
  "offset": 123,
  "orderBy": [TeamTalentOrderBy],
  "where": TeamTalentBoolExp
}
Response
{
  "data": {
    "teamTalent": [
      {
        "talent": numeric,
        "team": currentTeams,
        "year": smallint
      }
    ]
  }
}
Subscriptions
teamTalentAggregate
Description
fetch aggregated fields from the table: "team_talent"

Response
Returns a TeamTalentAggregate!

Arguments
Name	Description
distinctOn - [TeamTalentSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TeamTalentOrderBy!]	sort the rows by one or more columns
where - TeamTalentBoolExp	filter the rows returned
Example
Query
subscription TeamTalentAggregate(
  $distinctOn: [TeamTalentSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TeamTalentOrderBy!],
  $where: TeamTalentBoolExp
) {
  teamTalentAggregate(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    aggregate {
      avg {
        ...TeamTalentAvgFieldsFragment
      }
      count
      max {
        ...TeamTalentMaxFieldsFragment
      }
      min {
        ...TeamTalentMinFieldsFragment
      }
      stddev {
        ...TeamTalentStddevFieldsFragment
      }
      stddevPop {
        ...TeamTalentStddevPopFieldsFragment
      }
      stddevSamp {
        ...TeamTalentStddevSampFieldsFragment
      }
      sum {
        ...TeamTalentSumFieldsFragment
      }
      varPop {
        ...TeamTalentVarPopFieldsFragment
      }
      varSamp {
        ...TeamTalentVarSampFieldsFragment
      }
      variance {
        ...TeamTalentVarianceFieldsFragment
      }
    }
    nodes {
      talent
      team {
        ...currentTeamsFragment
      }
      year
    }
  }
}
Variables
{
  "distinctOn": ["talent"],
  "limit": 987,
  "offset": 123,
  "orderBy": [TeamTalentOrderBy],
  "where": TeamTalentBoolExp
}
Response
{
  "data": {
    "teamTalentAggregate": {
      "aggregate": TeamTalentAggregateFields,
      "nodes": [TeamTalent]
    }
  }
}
Subscriptions
transfer
Description
fetch data from the table: "transfer"

Response
Returns [Transfer!]!

Arguments
Name	Description
distinctOn - [TransferSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [TransferOrderBy!]	sort the rows by one or more columns
where - TransferBoolExp	filter the rows returned
Example
Query
subscription Transfer(
  $distinctOn: [TransferSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [TransferOrderBy!],
  $where: TransferBoolExp
) {
  transfer(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    eligibility
    firstName
    fromTeam {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    lastName
    position {
      id
      position
      positionGroup
    }
    rating
    season
    stars
    toTeam {
      abbreviation
      classification
      conference
      conferenceId
      division
      school
      teamId
    }
    transferDate
  }
}
Variables
{
  "distinctOn": ["eligibility"],
  "limit": 123,
  "offset": 987,
  "orderBy": [TransferOrderBy],
  "where": TransferBoolExp
}
Response
{
  "data": {
    "transfer": [
      {
        "eligibility": "xyz789",
        "firstName": "xyz789",
        "fromTeam": currentTeams,
        "lastName": "xyz789",
        "position": RecruitPosition,
        "rating": numeric,
        "season": smallint,
        "stars": smallint,
        "toTeam": currentTeams,
        "transferDate": timestamp
      }
    ]
  }
}
Subscriptions
weatherCondition
Description
fetch data from the table: "weather_condition"

Response
Returns [WeatherCondition!]!

Arguments
Name	Description
distinctOn - [WeatherConditionSelectColumn!]	distinct select on columns
limit - Int	limit the number of rows returned
offset - Int	skip the first n rows. Use only with order_by
orderBy - [WeatherConditionOrderBy!]	sort the rows by one or more columns
where - WeatherConditionBoolExp	filter the rows returned
Example
Query
subscription WeatherCondition(
  $distinctOn: [WeatherConditionSelectColumn!],
  $limit: Int,
  $offset: Int,
  $orderBy: [WeatherConditionOrderBy!],
  $where: WeatherConditionBoolExp
) {
  weatherCondition(
    distinctOn: $distinctOn,
    limit: $limit,
    offset: $offset,
    orderBy: $orderBy,
    where: $where
  ) {
    description
    id
  }
}
Variables
{
  "distinctOn": ["description"],
  "limit": 123,
  "offset": 123,
  "orderBy": [WeatherConditionOrderBy],
  "where": WeatherConditionBoolExp
}
Response
{
  "data": {
    "weatherCondition": [
      {
        "description": "xyz789",
        "id": smallint
      }
    ]
  }
}
Types
AdjustedPlayerMetrics
Description
columns and relationships of "adjusted_player_metrics"

Fields
Field Name	Description
athlete - Athlete!	An object relationship
athleteId - bigint!	
metricType - player_adjusted_metric_type!	
metricValue - numeric!	
plays - smallint	
year - smallint!	
Example
{
  "athlete": Athlete,
  "athleteId": bigint,
  "metricType": player_adjusted_metric_type,
  "metricValue": numeric,
  "plays": smallint,
  "year": smallint
}
Types
AdjustedPlayerMetricsAggregate
Description
aggregated selection of "adjusted_player_metrics"

Fields
Field Name	Description
aggregate - AdjustedPlayerMetricsAggregateFields	
nodes - [AdjustedPlayerMetrics!]!	
Example
{
  "aggregate": AdjustedPlayerMetricsAggregateFields,
  "nodes": [AdjustedPlayerMetrics]
}
Types
AdjustedPlayerMetricsAggregateBoolExp
Fields
Input Field	Description
count - adjustedPlayerMetricsAggregateBoolExpCount	
Example
{"count": adjustedPlayerMetricsAggregateBoolExpCount}
Types
AdjustedPlayerMetricsAggregateFields
Description
aggregate fields of "adjusted_player_metrics"

Fields
Field Name	Description
avg - AdjustedPlayerMetricsAvgFields	
count - Int!	
Arguments
columns - [AdjustedPlayerMetricsSelectColumn!]
distinct - Boolean
max - AdjustedPlayerMetricsMaxFields	
min - AdjustedPlayerMetricsMinFields	
stddev - AdjustedPlayerMetricsStddevFields	
stddevPop - AdjustedPlayerMetricsStddevPopFields	
stddevSamp - AdjustedPlayerMetricsStddevSampFields	
sum - AdjustedPlayerMetricsSumFields	
varPop - AdjustedPlayerMetricsVarPopFields	
varSamp - AdjustedPlayerMetricsVarSampFields	
variance - AdjustedPlayerMetricsVarianceFields	
Example
{
  "avg": AdjustedPlayerMetricsAvgFields,
  "count": 987,
  "max": AdjustedPlayerMetricsMaxFields,
  "min": AdjustedPlayerMetricsMinFields,
  "stddev": AdjustedPlayerMetricsStddevFields,
  "stddevPop": AdjustedPlayerMetricsStddevPopFields,
  "stddevSamp": AdjustedPlayerMetricsStddevSampFields,
  "sum": AdjustedPlayerMetricsSumFields,
  "varPop": AdjustedPlayerMetricsVarPopFields,
  "varSamp": AdjustedPlayerMetricsVarSampFields,
  "variance": AdjustedPlayerMetricsVarianceFields
}
Types
AdjustedPlayerMetricsAggregateOrderBy
Description
order by aggregate values of table "adjusted_player_metrics"

Fields
Input Field	Description
avg - AdjustedPlayerMetricsAvgOrderBy	
count - OrderBy	
max - AdjustedPlayerMetricsMaxOrderBy	
min - AdjustedPlayerMetricsMinOrderBy	
stddev - AdjustedPlayerMetricsStddevOrderBy	
stddevPop - AdjustedPlayerMetricsStddevPopOrderBy	
stddevSamp - AdjustedPlayerMetricsStddevSampOrderBy	
sum - AdjustedPlayerMetricsSumOrderBy	
varPop - AdjustedPlayerMetricsVarPopOrderBy	
varSamp - AdjustedPlayerMetricsVarSampOrderBy	
variance - AdjustedPlayerMetricsVarianceOrderBy	
Example
{
  "avg": AdjustedPlayerMetricsAvgOrderBy,
  "count": "ASC",
  "max": AdjustedPlayerMetricsMaxOrderBy,
  "min": AdjustedPlayerMetricsMinOrderBy,
  "stddev": AdjustedPlayerMetricsStddevOrderBy,
  "stddevPop": AdjustedPlayerMetricsStddevPopOrderBy,
  "stddevSamp": AdjustedPlayerMetricsStddevSampOrderBy,
  "sum": AdjustedPlayerMetricsSumOrderBy,
  "varPop": AdjustedPlayerMetricsVarPopOrderBy,
  "varSamp": AdjustedPlayerMetricsVarSampOrderBy,
  "variance": AdjustedPlayerMetricsVarianceOrderBy
}
Types
AdjustedPlayerMetricsAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 987.65, "plays": 123.45, "year": 123.45}
Types
AdjustedPlayerMetricsAvgOrderBy
Description
order by avg() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsBoolExp
Description
Boolean expression to filter rows from the table "adjusted_player_metrics". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [AdjustedPlayerMetricsBoolExp!]	
_not - AdjustedPlayerMetricsBoolExp	
_or - [AdjustedPlayerMetricsBoolExp!]	
athlete - AthleteBoolExp	
athleteId - BigintComparisonExp	
metricType - PlayerAdjustedMetricTypeComparisonExp	
metricValue - NumericComparisonExp	
plays - SmallintComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [AdjustedPlayerMetricsBoolExp],
  "_not": AdjustedPlayerMetricsBoolExp,
  "_or": [AdjustedPlayerMetricsBoolExp],
  "athlete": AthleteBoolExp,
  "athleteId": BigintComparisonExp,
  "metricType": PlayerAdjustedMetricTypeComparisonExp,
  "metricValue": NumericComparisonExp,
  "plays": SmallintComparisonExp,
  "year": SmallintComparisonExp
}
Types
AdjustedPlayerMetricsMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
athleteId - bigint	
metricType - player_adjusted_metric_type	
metricValue - numeric	
plays - smallint	
year - smallint	
Example
{
  "athleteId": bigint,
  "metricType": player_adjusted_metric_type,
  "metricValue": numeric,
  "plays": smallint,
  "year": smallint
}
Types
AdjustedPlayerMetricsMaxOrderBy
Description
order by max() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricType - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{
  "athleteId": "ASC",
  "metricType": "ASC",
  "metricValue": "ASC",
  "plays": "ASC",
  "year": "ASC"
}
Types
AdjustedPlayerMetricsMinFields
Description
aggregate min on columns

Fields
Field Name	Description
athleteId - bigint	
metricType - player_adjusted_metric_type	
metricValue - numeric	
plays - smallint	
year - smallint	
Example
{
  "athleteId": bigint,
  "metricType": player_adjusted_metric_type,
  "metricValue": numeric,
  "plays": smallint,
  "year": smallint
}
Types
AdjustedPlayerMetricsMinOrderBy
Description
order by min() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricType - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{
  "athleteId": "ASC",
  "metricType": "ASC",
  "metricValue": "ASC",
  "plays": "ASC",
  "year": "ASC"
}
Types
AdjustedPlayerMetricsOrderBy
Description
Ordering options when selecting data from "adjusted_player_metrics".

Fields
Input Field	Description
athlete - AthleteOrderBy	
athleteId - OrderBy	
metricType - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{
  "athlete": AthleteOrderBy,
  "athleteId": "ASC",
  "metricType": "ASC",
  "metricValue": "ASC",
  "plays": "ASC",
  "year": "ASC"
}
Types
AdjustedPlayerMetricsSelectColumn
Description
select columns of table "adjusted_player_metrics"

Values
Enum Value	Description
athleteId

column name
metricType

column name
metricValue

column name
plays

column name
year

column name
Example
"athleteId"
Types
AdjustedPlayerMetricsStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 987.65, "plays": 987.65, "year": 987.65}
Types
AdjustedPlayerMetricsStddevOrderBy
Description
order by stddev() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 987.65, "plays": 987.65, "year": 987.65}
Types
AdjustedPlayerMetricsStddevPopOrderBy
Description
order by stddevPop() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 123.45, "plays": 987.65, "year": 987.65}
Types
AdjustedPlayerMetricsStddevSampOrderBy
Description
order by stddevSamp() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
athleteId - bigint	
metricValue - numeric	
plays - smallint	
year - smallint	
Example
{
  "athleteId": bigint,
  "metricValue": numeric,
  "plays": smallint,
  "year": smallint
}
Types
AdjustedPlayerMetricsSumOrderBy
Description
order by sum() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 987.65, "plays": 987.65, "year": 123.45}
Types
AdjustedPlayerMetricsVarPopOrderBy
Description
order by varPop() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 123.45, "metricValue": 123.45, "plays": 123.45, "year": 123.45}
Types
AdjustedPlayerMetricsVarSampOrderBy
Description
order by varSamp() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedPlayerMetricsVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
athleteId - Float	
metricValue - Float	
plays - Float	
year - Float	
Example
{"athleteId": 987.65, "metricValue": 987.65, "plays": 123.45, "year": 123.45}
Types
AdjustedPlayerMetricsVarianceOrderBy
Description
order by variance() on columns of table "adjusted_player_metrics"

Fields
Input Field	Description
athleteId - OrderBy	
metricValue - OrderBy	
plays - OrderBy	
year - OrderBy	
Example
{"athleteId": "ASC", "metricValue": "ASC", "plays": "ASC", "year": "ASC"}
Types
AdjustedTeamMetrics
Description
columns and relationships of "adjusted_team_metrics"

Fields
Field Name	Description
epa - numeric!	
epaAllowed - numeric!	
explosiveness - numeric!	
explosivenessAllowed - numeric!	
highlightYards - numeric!	
highlightYardsAllowed - numeric!	
lineYards - numeric!	
lineYardsAllowed - numeric!	
openFieldYards - numeric!	
openFieldYardsAllowed - numeric!	
passingDownsSuccess - numeric!	
passingDownsSuccessAllowed - numeric!	
passingEpa - numeric!	
passingEpaAllowed - numeric!	
rushingEpa - numeric!	
rushingEpaAllowed - numeric!	
secondLevelYards - numeric!	
secondLevelYardsAllowed - numeric!	
standardDownsSuccess - numeric!	
standardDownsSuccessAllowed - numeric!	
success - numeric!	
successAllowed - numeric!	
team - currentTeams	An object relationship
teamId - Int!	
year - smallint!	
Example
{
  "epa": numeric,
  "epaAllowed": numeric,
  "explosiveness": numeric,
  "explosivenessAllowed": numeric,
  "highlightYards": numeric,
  "highlightYardsAllowed": numeric,
  "lineYards": numeric,
  "lineYardsAllowed": numeric,
  "openFieldYards": numeric,
  "openFieldYardsAllowed": numeric,
  "passingDownsSuccess": numeric,
  "passingDownsSuccessAllowed": numeric,
  "passingEpa": numeric,
  "passingEpaAllowed": numeric,
  "rushingEpa": numeric,
  "rushingEpaAllowed": numeric,
  "secondLevelYards": numeric,
  "secondLevelYardsAllowed": numeric,
  "standardDownsSuccess": numeric,
  "standardDownsSuccessAllowed": numeric,
  "success": numeric,
  "successAllowed": numeric,
  "team": currentTeams,
  "teamId": 123,
  "year": smallint
}
Types
AdjustedTeamMetricsAggregate
Description
aggregated selection of "adjusted_team_metrics"

Fields
Field Name	Description
aggregate - AdjustedTeamMetricsAggregateFields	
nodes - [AdjustedTeamMetrics!]!	
Example
{
  "aggregate": AdjustedTeamMetricsAggregateFields,
  "nodes": [AdjustedTeamMetrics]
}
Types
AdjustedTeamMetricsAggregateFields
Description
aggregate fields of "adjusted_team_metrics"

Fields
Field Name	Description
avg - AdjustedTeamMetricsAvgFields	
count - Int!	
Arguments
columns - [AdjustedTeamMetricsSelectColumn!]
distinct - Boolean
max - AdjustedTeamMetricsMaxFields	
min - AdjustedTeamMetricsMinFields	
stddev - AdjustedTeamMetricsStddevFields	
stddevPop - AdjustedTeamMetricsStddevPopFields	
stddevSamp - AdjustedTeamMetricsStddevSampFields	
sum - AdjustedTeamMetricsSumFields	
varPop - AdjustedTeamMetricsVarPopFields	
varSamp - AdjustedTeamMetricsVarSampFields	
variance - AdjustedTeamMetricsVarianceFields	
Example
{
  "avg": AdjustedTeamMetricsAvgFields,
  "count": 123,
  "max": AdjustedTeamMetricsMaxFields,
  "min": AdjustedTeamMetricsMinFields,
  "stddev": AdjustedTeamMetricsStddevFields,
  "stddevPop": AdjustedTeamMetricsStddevPopFields,
  "stddevSamp": AdjustedTeamMetricsStddevSampFields,
  "sum": AdjustedTeamMetricsSumFields,
  "varPop": AdjustedTeamMetricsVarPopFields,
  "varSamp": AdjustedTeamMetricsVarSampFields,
  "variance": AdjustedTeamMetricsVarianceFields
}
Types
AdjustedTeamMetricsAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 123.45,
  "explosiveness": 987.65,
  "explosivenessAllowed": 987.65,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 987.65,
  "lineYards": 987.65,
  "lineYardsAllowed": 123.45,
  "openFieldYards": 123.45,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 987.65,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 987.65,
  "passingEpaAllowed": 987.65,
  "rushingEpa": 987.65,
  "rushingEpaAllowed": 123.45,
  "secondLevelYards": 123.45,
  "secondLevelYardsAllowed": 987.65,
  "standardDownsSuccess": 987.65,
  "standardDownsSuccessAllowed": 123.45,
  "success": 987.65,
  "successAllowed": 987.65,
  "teamId": 987.65,
  "year": 123.45
}
Types
AdjustedTeamMetricsBoolExp
Description
Boolean expression to filter rows from the table "adjusted_team_metrics". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [AdjustedTeamMetricsBoolExp!]	
_not - AdjustedTeamMetricsBoolExp	
_or - [AdjustedTeamMetricsBoolExp!]	
epa - NumericComparisonExp	
epaAllowed - NumericComparisonExp	
explosiveness - NumericComparisonExp	
explosivenessAllowed - NumericComparisonExp	
highlightYards - NumericComparisonExp	
highlightYardsAllowed - NumericComparisonExp	
lineYards - NumericComparisonExp	
lineYardsAllowed - NumericComparisonExp	
openFieldYards - NumericComparisonExp	
openFieldYardsAllowed - NumericComparisonExp	
passingDownsSuccess - NumericComparisonExp	
passingDownsSuccessAllowed - NumericComparisonExp	
passingEpa - NumericComparisonExp	
passingEpaAllowed - NumericComparisonExp	
rushingEpa - NumericComparisonExp	
rushingEpaAllowed - NumericComparisonExp	
secondLevelYards - NumericComparisonExp	
secondLevelYardsAllowed - NumericComparisonExp	
standardDownsSuccess - NumericComparisonExp	
standardDownsSuccessAllowed - NumericComparisonExp	
success - NumericComparisonExp	
successAllowed - NumericComparisonExp	
team - currentTeamsBoolExp	
teamId - IntComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [AdjustedTeamMetricsBoolExp],
  "_not": AdjustedTeamMetricsBoolExp,
  "_or": [AdjustedTeamMetricsBoolExp],
  "epa": NumericComparisonExp,
  "epaAllowed": NumericComparisonExp,
  "explosiveness": NumericComparisonExp,
  "explosivenessAllowed": NumericComparisonExp,
  "highlightYards": NumericComparisonExp,
  "highlightYardsAllowed": NumericComparisonExp,
  "lineYards": NumericComparisonExp,
  "lineYardsAllowed": NumericComparisonExp,
  "openFieldYards": NumericComparisonExp,
  "openFieldYardsAllowed": NumericComparisonExp,
  "passingDownsSuccess": NumericComparisonExp,
  "passingDownsSuccessAllowed": NumericComparisonExp,
  "passingEpa": NumericComparisonExp,
  "passingEpaAllowed": NumericComparisonExp,
  "rushingEpa": NumericComparisonExp,
  "rushingEpaAllowed": NumericComparisonExp,
  "secondLevelYards": NumericComparisonExp,
  "secondLevelYardsAllowed": NumericComparisonExp,
  "standardDownsSuccess": NumericComparisonExp,
  "standardDownsSuccessAllowed": NumericComparisonExp,
  "success": NumericComparisonExp,
  "successAllowed": NumericComparisonExp,
  "team": currentTeamsBoolExp,
  "teamId": IntComparisonExp,
  "year": SmallintComparisonExp
}
Types
AdjustedTeamMetricsMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
epa - numeric	
epaAllowed - numeric	
explosiveness - numeric	
explosivenessAllowed - numeric	
highlightYards - numeric	
highlightYardsAllowed - numeric	
lineYards - numeric	
lineYardsAllowed - numeric	
openFieldYards - numeric	
openFieldYardsAllowed - numeric	
passingDownsSuccess - numeric	
passingDownsSuccessAllowed - numeric	
passingEpa - numeric	
passingEpaAllowed - numeric	
rushingEpa - numeric	
rushingEpaAllowed - numeric	
secondLevelYards - numeric	
secondLevelYardsAllowed - numeric	
standardDownsSuccess - numeric	
standardDownsSuccessAllowed - numeric	
success - numeric	
successAllowed - numeric	
teamId - Int	
year - smallint	
Example
{
  "epa": numeric,
  "epaAllowed": numeric,
  "explosiveness": numeric,
  "explosivenessAllowed": numeric,
  "highlightYards": numeric,
  "highlightYardsAllowed": numeric,
  "lineYards": numeric,
  "lineYardsAllowed": numeric,
  "openFieldYards": numeric,
  "openFieldYardsAllowed": numeric,
  "passingDownsSuccess": numeric,
  "passingDownsSuccessAllowed": numeric,
  "passingEpa": numeric,
  "passingEpaAllowed": numeric,
  "rushingEpa": numeric,
  "rushingEpaAllowed": numeric,
  "secondLevelYards": numeric,
  "secondLevelYardsAllowed": numeric,
  "standardDownsSuccess": numeric,
  "standardDownsSuccessAllowed": numeric,
  "success": numeric,
  "successAllowed": numeric,
  "teamId": 123,
  "year": smallint
}
Types
AdjustedTeamMetricsMinFields
Description
aggregate min on columns

Fields
Field Name	Description
epa - numeric	
epaAllowed - numeric	
explosiveness - numeric	
explosivenessAllowed - numeric	
highlightYards - numeric	
highlightYardsAllowed - numeric	
lineYards - numeric	
lineYardsAllowed - numeric	
openFieldYards - numeric	
openFieldYardsAllowed - numeric	
passingDownsSuccess - numeric	
passingDownsSuccessAllowed - numeric	
passingEpa - numeric	
passingEpaAllowed - numeric	
rushingEpa - numeric	
rushingEpaAllowed - numeric	
secondLevelYards - numeric	
secondLevelYardsAllowed - numeric	
standardDownsSuccess - numeric	
standardDownsSuccessAllowed - numeric	
success - numeric	
successAllowed - numeric	
teamId - Int	
year - smallint	
Example
{
  "epa": numeric,
  "epaAllowed": numeric,
  "explosiveness": numeric,
  "explosivenessAllowed": numeric,
  "highlightYards": numeric,
  "highlightYardsAllowed": numeric,
  "lineYards": numeric,
  "lineYardsAllowed": numeric,
  "openFieldYards": numeric,
  "openFieldYardsAllowed": numeric,
  "passingDownsSuccess": numeric,
  "passingDownsSuccessAllowed": numeric,
  "passingEpa": numeric,
  "passingEpaAllowed": numeric,
  "rushingEpa": numeric,
  "rushingEpaAllowed": numeric,
  "secondLevelYards": numeric,
  "secondLevelYardsAllowed": numeric,
  "standardDownsSuccess": numeric,
  "standardDownsSuccessAllowed": numeric,
  "success": numeric,
  "successAllowed": numeric,
  "teamId": 987,
  "year": smallint
}
Types
AdjustedTeamMetricsOrderBy
Description
Ordering options when selecting data from "adjusted_team_metrics".

Fields
Input Field	Description
epa - OrderBy	
epaAllowed - OrderBy	
explosiveness - OrderBy	
explosivenessAllowed - OrderBy	
highlightYards - OrderBy	
highlightYardsAllowed - OrderBy	
lineYards - OrderBy	
lineYardsAllowed - OrderBy	
openFieldYards - OrderBy	
openFieldYardsAllowed - OrderBy	
passingDownsSuccess - OrderBy	
passingDownsSuccessAllowed - OrderBy	
passingEpa - OrderBy	
passingEpaAllowed - OrderBy	
rushingEpa - OrderBy	
rushingEpaAllowed - OrderBy	
secondLevelYards - OrderBy	
secondLevelYardsAllowed - OrderBy	
standardDownsSuccess - OrderBy	
standardDownsSuccessAllowed - OrderBy	
success - OrderBy	
successAllowed - OrderBy	
team - currentTeamsOrderBy	
teamId - OrderBy	
year - OrderBy	
Example
{
  "epa": "ASC",
  "epaAllowed": "ASC",
  "explosiveness": "ASC",
  "explosivenessAllowed": "ASC",
  "highlightYards": "ASC",
  "highlightYardsAllowed": "ASC",
  "lineYards": "ASC",
  "lineYardsAllowed": "ASC",
  "openFieldYards": "ASC",
  "openFieldYardsAllowed": "ASC",
  "passingDownsSuccess": "ASC",
  "passingDownsSuccessAllowed": "ASC",
  "passingEpa": "ASC",
  "passingEpaAllowed": "ASC",
  "rushingEpa": "ASC",
  "rushingEpaAllowed": "ASC",
  "secondLevelYards": "ASC",
  "secondLevelYardsAllowed": "ASC",
  "standardDownsSuccess": "ASC",
  "standardDownsSuccessAllowed": "ASC",
  "success": "ASC",
  "successAllowed": "ASC",
  "team": currentTeamsOrderBy,
  "teamId": "ASC",
  "year": "ASC"
}
Types
AdjustedTeamMetricsSelectColumn
Description
select columns of table "adjusted_team_metrics"

Values
Enum Value	Description
epa

column name
epaAllowed

column name
explosiveness

column name
explosivenessAllowed

column name
highlightYards

column name
highlightYardsAllowed

column name
lineYards

column name
lineYardsAllowed

column name
openFieldYards

column name
openFieldYardsAllowed

column name
passingDownsSuccess

column name
passingDownsSuccessAllowed

column name
passingEpa

column name
passingEpaAllowed

column name
rushingEpa

column name
rushingEpaAllowed

column name
secondLevelYards

column name
secondLevelYardsAllowed

column name
standardDownsSuccess

column name
standardDownsSuccessAllowed

column name
success

column name
successAllowed

column name
teamId

column name
year

column name
Example
"epa"
Types
AdjustedTeamMetricsStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 123.45,
  "explosiveness": 987.65,
  "explosivenessAllowed": 123.45,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 987.65,
  "lineYards": 987.65,
  "lineYardsAllowed": 987.65,
  "openFieldYards": 987.65,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 123.45,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 123.45,
  "passingEpaAllowed": 987.65,
  "rushingEpa": 123.45,
  "rushingEpaAllowed": 987.65,
  "secondLevelYards": 987.65,
  "secondLevelYardsAllowed": 987.65,
  "standardDownsSuccess": 123.45,
  "standardDownsSuccessAllowed": 123.45,
  "success": 123.45,
  "successAllowed": 987.65,
  "teamId": 987.65,
  "year": 123.45
}
Types
AdjustedTeamMetricsStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 987.65,
  "epaAllowed": 987.65,
  "explosiveness": 123.45,
  "explosivenessAllowed": 123.45,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 987.65,
  "lineYards": 123.45,
  "lineYardsAllowed": 123.45,
  "openFieldYards": 123.45,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 123.45,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 987.65,
  "passingEpaAllowed": 123.45,
  "rushingEpa": 987.65,
  "rushingEpaAllowed": 123.45,
  "secondLevelYards": 987.65,
  "secondLevelYardsAllowed": 123.45,
  "standardDownsSuccess": 123.45,
  "standardDownsSuccessAllowed": 123.45,
  "success": 987.65,
  "successAllowed": 987.65,
  "teamId": 987.65,
  "year": 123.45
}
Types
AdjustedTeamMetricsStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 987.65,
  "explosiveness": 987.65,
  "explosivenessAllowed": 123.45,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 987.65,
  "lineYards": 987.65,
  "lineYardsAllowed": 987.65,
  "openFieldYards": 987.65,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 123.45,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 123.45,
  "passingEpaAllowed": 987.65,
  "rushingEpa": 987.65,
  "rushingEpaAllowed": 987.65,
  "secondLevelYards": 123.45,
  "secondLevelYardsAllowed": 123.45,
  "standardDownsSuccess": 987.65,
  "standardDownsSuccessAllowed": 123.45,
  "success": 123.45,
  "successAllowed": 123.45,
  "teamId": 987.65,
  "year": 123.45
}
Types
AdjustedTeamMetricsSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
epa - numeric	
epaAllowed - numeric	
explosiveness - numeric	
explosivenessAllowed - numeric	
highlightYards - numeric	
highlightYardsAllowed - numeric	
lineYards - numeric	
lineYardsAllowed - numeric	
openFieldYards - numeric	
openFieldYardsAllowed - numeric	
passingDownsSuccess - numeric	
passingDownsSuccessAllowed - numeric	
passingEpa - numeric	
passingEpaAllowed - numeric	
rushingEpa - numeric	
rushingEpaAllowed - numeric	
secondLevelYards - numeric	
secondLevelYardsAllowed - numeric	
standardDownsSuccess - numeric	
standardDownsSuccessAllowed - numeric	
success - numeric	
successAllowed - numeric	
teamId - Int	
year - smallint	
Example
{
  "epa": numeric,
  "epaAllowed": numeric,
  "explosiveness": numeric,
  "explosivenessAllowed": numeric,
  "highlightYards": numeric,
  "highlightYardsAllowed": numeric,
  "lineYards": numeric,
  "lineYardsAllowed": numeric,
  "openFieldYards": numeric,
  "openFieldYardsAllowed": numeric,
  "passingDownsSuccess": numeric,
  "passingDownsSuccessAllowed": numeric,
  "passingEpa": numeric,
  "passingEpaAllowed": numeric,
  "rushingEpa": numeric,
  "rushingEpaAllowed": numeric,
  "secondLevelYards": numeric,
  "secondLevelYardsAllowed": numeric,
  "standardDownsSuccess": numeric,
  "standardDownsSuccessAllowed": numeric,
  "success": numeric,
  "successAllowed": numeric,
  "teamId": 123,
  "year": smallint
}
Types
AdjustedTeamMetricsVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 123.45,
  "explosiveness": 123.45,
  "explosivenessAllowed": 123.45,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 987.65,
  "lineYards": 987.65,
  "lineYardsAllowed": 987.65,
  "openFieldYards": 123.45,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 987.65,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 123.45,
  "passingEpaAllowed": 123.45,
  "rushingEpa": 987.65,
  "rushingEpaAllowed": 123.45,
  "secondLevelYards": 987.65,
  "secondLevelYardsAllowed": 123.45,
  "standardDownsSuccess": 123.45,
  "standardDownsSuccessAllowed": 987.65,
  "success": 987.65,
  "successAllowed": 123.45,
  "teamId": 987.65,
  "year": 987.65
}
Types
AdjustedTeamMetricsVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 987.65,
  "explosiveness": 987.65,
  "explosivenessAllowed": 123.45,
  "highlightYards": 123.45,
  "highlightYardsAllowed": 123.45,
  "lineYards": 987.65,
  "lineYardsAllowed": 123.45,
  "openFieldYards": 987.65,
  "openFieldYardsAllowed": 123.45,
  "passingDownsSuccess": 987.65,
  "passingDownsSuccessAllowed": 123.45,
  "passingEpa": 123.45,
  "passingEpaAllowed": 123.45,
  "rushingEpa": 987.65,
  "rushingEpaAllowed": 987.65,
  "secondLevelYards": 123.45,
  "secondLevelYardsAllowed": 123.45,
  "standardDownsSuccess": 987.65,
  "standardDownsSuccessAllowed": 123.45,
  "success": 123.45,
  "successAllowed": 987.65,
  "teamId": 123.45,
  "year": 987.65
}
Types
AdjustedTeamMetricsVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
epa - Float	
epaAllowed - Float	
explosiveness - Float	
explosivenessAllowed - Float	
highlightYards - Float	
highlightYardsAllowed - Float	
lineYards - Float	
lineYardsAllowed - Float	
openFieldYards - Float	
openFieldYardsAllowed - Float	
passingDownsSuccess - Float	
passingDownsSuccessAllowed - Float	
passingEpa - Float	
passingEpaAllowed - Float	
rushingEpa - Float	
rushingEpaAllowed - Float	
secondLevelYards - Float	
secondLevelYardsAllowed - Float	
standardDownsSuccess - Float	
standardDownsSuccessAllowed - Float	
success - Float	
successAllowed - Float	
teamId - Float	
year - Float	
Example
{
  "epa": 123.45,
  "epaAllowed": 123.45,
  "explosiveness": 123.45,
  "explosivenessAllowed": 987.65,
  "highlightYards": 987.65,
  "highlightYardsAllowed": 123.45,
  "lineYards": 123.45,
  "lineYardsAllowed": 987.65,
  "openFieldYards": 123.45,
  "openFieldYardsAllowed": 987.65,
  "passingDownsSuccess": 123.45,
  "passingDownsSuccessAllowed": 987.65,
  "passingEpa": 987.65,
  "passingEpaAllowed": 123.45,
  "rushingEpa": 123.45,
  "rushingEpaAllowed": 987.65,
  "secondLevelYards": 123.45,
  "secondLevelYardsAllowed": 123.45,
  "standardDownsSuccess": 987.65,
  "standardDownsSuccessAllowed": 123.45,
  "success": 987.65,
  "successAllowed": 987.65,
  "teamId": 123.45,
  "year": 987.65
}
Types
Athlete
Description
columns and relationships of "athlete"

Fields
Field Name	Description
adjustedPlayerMetrics - [AdjustedPlayerMetrics!]!	An array relationship
Arguments
distinctOn - [AdjustedPlayerMetricsSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AdjustedPlayerMetricsOrderBy!]
sort the rows by one or more columns

where - AdjustedPlayerMetricsBoolExp
filter the rows returned

adjustedPlayerMetricsAggregate - AdjustedPlayerMetricsAggregate!	An aggregate relationship
Arguments
distinctOn - [AdjustedPlayerMetricsSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AdjustedPlayerMetricsOrderBy!]
sort the rows by one or more columns

where - AdjustedPlayerMetricsBoolExp
filter the rows returned

athleteTeams - [AthleteTeam!]!	An array relationship
Arguments
distinctOn - [AthleteTeamSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteTeamOrderBy!]
sort the rows by one or more columns

where - AthleteTeamBoolExp
filter the rows returned

athleteTeamsAggregate - AthleteTeamAggregate!	An aggregate relationship
Arguments
distinctOn - [AthleteTeamSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteTeamOrderBy!]
sort the rows by one or more columns

where - AthleteTeamBoolExp
filter the rows returned

firstName - String	
height - smallint	
hometown - Hometown	An object relationship
hometownId - Int	
id - bigint!	
jersey - smallint	
lastName - String	
name - String!	
position - Position	An object relationship
positionId - smallint	
recruits - [Recruit!]!	An array relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

recruitsAggregate - RecruitAggregate!	An aggregate relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

teamId - Int	
weight - smallint	
Example
{
  "adjustedPlayerMetrics": [AdjustedPlayerMetrics],
  "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregate,
  "athleteTeams": [AthleteTeam],
  "athleteTeamsAggregate": AthleteTeamAggregate,
  "firstName": "abc123",
  "height": smallint,
  "hometown": Hometown,
  "hometownId": 987,
  "id": bigint,
  "jersey": smallint,
  "lastName": "abc123",
  "name": "abc123",
  "position": Position,
  "positionId": smallint,
  "recruits": [Recruit],
  "recruitsAggregate": RecruitAggregate,
  "teamId": 123,
  "weight": smallint
}
Types
AthleteAggregate
Description
aggregated selection of "athlete"

Fields
Field Name	Description
aggregate - AthleteAggregateFields	
nodes - [Athlete!]!	
Example
{
  "aggregate": AthleteAggregateFields,
  "nodes": [Athlete]
}
Types
AthleteAggregateBoolExp
Fields
Input Field	Description
count - athleteAggregateBoolExpCount	
Example
{"count": athleteAggregateBoolExpCount}
Types
AthleteAggregateFields
Description
aggregate fields of "athlete"

Fields
Field Name	Description
avg - AthleteAvgFields	
count - Int!	
Arguments
columns - [AthleteSelectColumn!]
distinct - Boolean
max - AthleteMaxFields	
min - AthleteMinFields	
stddev - AthleteStddevFields	
stddevPop - AthleteStddevPopFields	
stddevSamp - AthleteStddevSampFields	
sum - AthleteSumFields	
varPop - AthleteVarPopFields	
varSamp - AthleteVarSampFields	
variance - AthleteVarianceFields	
Example
{
  "avg": AthleteAvgFields,
  "count": 123,
  "max": AthleteMaxFields,
  "min": AthleteMinFields,
  "stddev": AthleteStddevFields,
  "stddevPop": AthleteStddevPopFields,
  "stddevSamp": AthleteStddevSampFields,
  "sum": AthleteSumFields,
  "varPop": AthleteVarPopFields,
  "varSamp": AthleteVarSampFields,
  "variance": AthleteVarianceFields
}
Types
AthleteAggregateOrderBy
Description
order by aggregate values of table "athlete"

Fields
Input Field	Description
avg - AthleteAvgOrderBy	
count - OrderBy	
max - AthleteMaxOrderBy	
min - AthleteMinOrderBy	
stddev - AthleteStddevOrderBy	
stddevPop - AthleteStddevPopOrderBy	
stddevSamp - AthleteStddevSampOrderBy	
sum - AthleteSumOrderBy	
varPop - AthleteVarPopOrderBy	
varSamp - AthleteVarSampOrderBy	
variance - AthleteVarianceOrderBy	
Example
{
  "avg": AthleteAvgOrderBy,
  "count": "ASC",
  "max": AthleteMaxOrderBy,
  "min": AthleteMinOrderBy,
  "stddev": AthleteStddevOrderBy,
  "stddevPop": AthleteStddevPopOrderBy,
  "stddevSamp": AthleteStddevSampOrderBy,
  "sum": AthleteSumOrderBy,
  "varPop": AthleteVarPopOrderBy,
  "varSamp": AthleteVarSampOrderBy,
  "variance": AthleteVarianceOrderBy
}
Types
AthleteAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 987.65,
  "hometownId": 123.45,
  "id": 123.45,
  "jersey": 987.65,
  "positionId": 987.65,
  "teamId": 987.65,
  "weight": 987.65
}
Types
AthleteAvgOrderBy
Description
order by avg() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteBoolExp
Description
Boolean expression to filter rows from the table "athlete". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [AthleteBoolExp!]	
_not - AthleteBoolExp	
_or - [AthleteBoolExp!]	
adjustedPlayerMetrics - AdjustedPlayerMetricsBoolExp	
adjustedPlayerMetricsAggregate - AdjustedPlayerMetricsAggregateBoolExp	
athleteTeams - AthleteTeamBoolExp	
athleteTeamsAggregate - AthleteTeamAggregateBoolExp	
firstName - StringComparisonExp	
height - SmallintComparisonExp	
hometown - HometownBoolExp	
hometownId - IntComparisonExp	
id - BigintComparisonExp	
jersey - SmallintComparisonExp	
lastName - StringComparisonExp	
name - StringComparisonExp	
position - PositionBoolExp	
positionId - SmallintComparisonExp	
recruits - RecruitBoolExp	
recruitsAggregate - RecruitAggregateBoolExp	
teamId - IntComparisonExp	
weight - SmallintComparisonExp	
Example
{
  "_and": [AthleteBoolExp],
  "_not": AthleteBoolExp,
  "_or": [AthleteBoolExp],
  "adjustedPlayerMetrics": AdjustedPlayerMetricsBoolExp,
  "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregateBoolExp,
  "athleteTeams": AthleteTeamBoolExp,
  "athleteTeamsAggregate": AthleteTeamAggregateBoolExp,
  "firstName": StringComparisonExp,
  "height": SmallintComparisonExp,
  "hometown": HometownBoolExp,
  "hometownId": IntComparisonExp,
  "id": BigintComparisonExp,
  "jersey": SmallintComparisonExp,
  "lastName": StringComparisonExp,
  "name": StringComparisonExp,
  "position": PositionBoolExp,
  "positionId": SmallintComparisonExp,
  "recruits": RecruitBoolExp,
  "recruitsAggregate": RecruitAggregateBoolExp,
  "teamId": IntComparisonExp,
  "weight": SmallintComparisonExp
}
Types
AthleteMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
firstName - String	
height - smallint	
hometownId - Int	
id - bigint	
jersey - smallint	
lastName - String	
name - String	
positionId - smallint	
teamId - Int	
weight - smallint	
Example
{
  "firstName": "xyz789",
  "height": smallint,
  "hometownId": 987,
  "id": bigint,
  "jersey": smallint,
  "lastName": "abc123",
  "name": "abc123",
  "positionId": smallint,
  "teamId": 123,
  "weight": smallint
}
Types
AthleteMaxOrderBy
Description
order by max() on columns of table "athlete"

Fields
Input Field	Description
firstName - OrderBy	
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
lastName - OrderBy	
name - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "firstName": "ASC",
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "lastName": "ASC",
  "name": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteMinFields
Description
aggregate min on columns

Fields
Field Name	Description
firstName - String	
height - smallint	
hometownId - Int	
id - bigint	
jersey - smallint	
lastName - String	
name - String	
positionId - smallint	
teamId - Int	
weight - smallint	
Example
{
  "firstName": "xyz789",
  "height": smallint,
  "hometownId": 123,
  "id": bigint,
  "jersey": smallint,
  "lastName": "abc123",
  "name": "abc123",
  "positionId": smallint,
  "teamId": 123,
  "weight": smallint
}
Types
AthleteMinOrderBy
Description
order by min() on columns of table "athlete"

Fields
Input Field	Description
firstName - OrderBy	
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
lastName - OrderBy	
name - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "firstName": "ASC",
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "lastName": "ASC",
  "name": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteOrderBy
Description
Ordering options when selecting data from "athlete".

Fields
Input Field	Description
adjustedPlayerMetricsAggregate - AdjustedPlayerMetricsAggregateOrderBy	
athleteTeamsAggregate - AthleteTeamAggregateOrderBy	
firstName - OrderBy	
height - OrderBy	
hometown - HometownOrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
lastName - OrderBy	
name - OrderBy	
position - PositionOrderBy	
positionId - OrderBy	
recruitsAggregate - RecruitAggregateOrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "adjustedPlayerMetricsAggregate": AdjustedPlayerMetricsAggregateOrderBy,
  "athleteTeamsAggregate": AthleteTeamAggregateOrderBy,
  "firstName": "ASC",
  "height": "ASC",
  "hometown": HometownOrderBy,
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "lastName": "ASC",
  "name": "ASC",
  "position": PositionOrderBy,
  "positionId": "ASC",
  "recruitsAggregate": RecruitAggregateOrderBy,
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteSelectColumn
Description
select columns of table "athlete"

Values
Enum Value	Description
firstName

column name
height

column name
hometownId

column name
id

column name
jersey

column name
lastName

column name
name

column name
positionId

column name
teamId

column name
weight

column name
Example
"firstName"
Types
AthleteStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 123.45,
  "hometownId": 123.45,
  "id": 123.45,
  "jersey": 987.65,
  "positionId": 123.45,
  "teamId": 123.45,
  "weight": 123.45
}
Types
AthleteStddevOrderBy
Description
order by stddev() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 123.45,
  "hometownId": 987.65,
  "id": 123.45,
  "jersey": 123.45,
  "positionId": 123.45,
  "teamId": 123.45,
  "weight": 123.45
}
Types
AthleteStddevPopOrderBy
Description
order by stddevPop() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 123.45,
  "hometownId": 123.45,
  "id": 987.65,
  "jersey": 987.65,
  "positionId": 123.45,
  "teamId": 123.45,
  "weight": 987.65
}
Types
AthleteStddevSampOrderBy
Description
order by stddevSamp() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
height - smallint	
hometownId - Int	
id - bigint	
jersey - smallint	
positionId - smallint	
teamId - Int	
weight - smallint	
Example
{
  "height": smallint,
  "hometownId": 123,
  "id": bigint,
  "jersey": smallint,
  "positionId": smallint,
  "teamId": 987,
  "weight": smallint
}
Types
AthleteSumOrderBy
Description
order by sum() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteTeam
Description
columns and relationships of "athlete_team"

Fields
Field Name	Description
athlete - Athlete	An object relationship
athleteId - bigint!	
endYear - smallint	
startYear - smallint	
team - historicalTeam	An object relationship
teamId - Int!	
Example
{
  "athlete": Athlete,
  "athleteId": bigint,
  "endYear": smallint,
  "startYear": smallint,
  "team": historicalTeam,
  "teamId": 987
}
Types
AthleteTeamAggregate
Description
aggregated selection of "athlete_team"

Fields
Field Name	Description
aggregate - AthleteTeamAggregateFields	
nodes - [AthleteTeam!]!	
Example
{
  "aggregate": AthleteTeamAggregateFields,
  "nodes": [AthleteTeam]
}
Types
AthleteTeamAggregateBoolExp
Fields
Input Field	Description
count - athleteTeamAggregateBoolExpCount	
Example
{"count": athleteTeamAggregateBoolExpCount}
Types
AthleteTeamAggregateFields
Description
aggregate fields of "athlete_team"

Fields
Field Name	Description
avg - AthleteTeamAvgFields	
count - Int!	
Arguments
columns - [AthleteTeamSelectColumn!]
distinct - Boolean
max - AthleteTeamMaxFields	
min - AthleteTeamMinFields	
stddev - AthleteTeamStddevFields	
stddevPop - AthleteTeamStddevPopFields	
stddevSamp - AthleteTeamStddevSampFields	
sum - AthleteTeamSumFields	
varPop - AthleteTeamVarPopFields	
varSamp - AthleteTeamVarSampFields	
variance - AthleteTeamVarianceFields	
Example
{
  "avg": AthleteTeamAvgFields,
  "count": 123,
  "max": AthleteTeamMaxFields,
  "min": AthleteTeamMinFields,
  "stddev": AthleteTeamStddevFields,
  "stddevPop": AthleteTeamStddevPopFields,
  "stddevSamp": AthleteTeamStddevSampFields,
  "sum": AthleteTeamSumFields,
  "varPop": AthleteTeamVarPopFields,
  "varSamp": AthleteTeamVarSampFields,
  "variance": AthleteTeamVarianceFields
}
Types
AthleteTeamAggregateOrderBy
Description
order by aggregate values of table "athlete_team"

Fields
Input Field	Description
avg - AthleteTeamAvgOrderBy	
count - OrderBy	
max - AthleteTeamMaxOrderBy	
min - AthleteTeamMinOrderBy	
stddev - AthleteTeamStddevOrderBy	
stddevPop - AthleteTeamStddevPopOrderBy	
stddevSamp - AthleteTeamStddevSampOrderBy	
sum - AthleteTeamSumOrderBy	
varPop - AthleteTeamVarPopOrderBy	
varSamp - AthleteTeamVarSampOrderBy	
variance - AthleteTeamVarianceOrderBy	
Example
{
  "avg": AthleteTeamAvgOrderBy,
  "count": "ASC",
  "max": AthleteTeamMaxOrderBy,
  "min": AthleteTeamMinOrderBy,
  "stddev": AthleteTeamStddevOrderBy,
  "stddevPop": AthleteTeamStddevPopOrderBy,
  "stddevSamp": AthleteTeamStddevSampOrderBy,
  "sum": AthleteTeamSumOrderBy,
  "varPop": AthleteTeamVarPopOrderBy,
  "varSamp": AthleteTeamVarSampOrderBy,
  "variance": AthleteTeamVarianceOrderBy
}
Types
AthleteTeamAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 123.45, "endYear": 987.65, "startYear": 123.45, "teamId": 123.45}
Types
AthleteTeamAvgOrderBy
Description
order by avg() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamBoolExp
Description
Boolean expression to filter rows from the table "athlete_team". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [AthleteTeamBoolExp!]	
_not - AthleteTeamBoolExp	
_or - [AthleteTeamBoolExp!]	
athlete - AthleteBoolExp	
athleteId - BigintComparisonExp	
endYear - SmallintComparisonExp	
startYear - SmallintComparisonExp	
team - historicalTeamBoolExp	
teamId - IntComparisonExp	
Example
{
  "_and": [AthleteTeamBoolExp],
  "_not": AthleteTeamBoolExp,
  "_or": [AthleteTeamBoolExp],
  "athlete": AthleteBoolExp,
  "athleteId": BigintComparisonExp,
  "endYear": SmallintComparisonExp,
  "startYear": SmallintComparisonExp,
  "team": historicalTeamBoolExp,
  "teamId": IntComparisonExp
}
Types
AthleteTeamMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
athleteId - bigint	
endYear - smallint	
startYear - smallint	
teamId - Int	
Example
{
  "athleteId": bigint,
  "endYear": smallint,
  "startYear": smallint,
  "teamId": 123
}
Types
AthleteTeamMaxOrderBy
Description
order by max() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamMinFields
Description
aggregate min on columns

Fields
Field Name	Description
athleteId - bigint	
endYear - smallint	
startYear - smallint	
teamId - Int	
Example
{
  "athleteId": bigint,
  "endYear": smallint,
  "startYear": smallint,
  "teamId": 123
}
Types
AthleteTeamMinOrderBy
Description
order by min() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamOrderBy
Description
Ordering options when selecting data from "athlete_team".

Fields
Input Field	Description
athlete - AthleteOrderBy	
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
team - historicalTeamOrderBy	
teamId - OrderBy	
Example
{
  "athlete": AthleteOrderBy,
  "athleteId": "ASC",
  "endYear": "ASC",
  "startYear": "ASC",
  "team": historicalTeamOrderBy,
  "teamId": "ASC"
}
Types
AthleteTeamSelectColumn
Description
select columns of table "athlete_team"

Values
Enum Value	Description
athleteId

column name
endYear

column name
startYear

column name
teamId

column name
Example
"athleteId"
Types
AthleteTeamStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 987.65, "endYear": 987.65, "startYear": 123.45, "teamId": 123.45}
Types
AthleteTeamStddevOrderBy
Description
order by stddev() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 987.65, "endYear": 123.45, "startYear": 987.65, "teamId": 123.45}
Types
AthleteTeamStddevPopOrderBy
Description
order by stddevPop() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 123.45, "endYear": 987.65, "startYear": 123.45, "teamId": 123.45}
Types
AthleteTeamStddevSampOrderBy
Description
order by stddevSamp() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
athleteId - bigint	
endYear - smallint	
startYear - smallint	
teamId - Int	
Example
{
  "athleteId": bigint,
  "endYear": smallint,
  "startYear": smallint,
  "teamId": 123
}
Types
AthleteTeamSumOrderBy
Description
order by sum() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 987.65, "endYear": 987.65, "startYear": 123.45, "teamId": 123.45}
Types
AthleteTeamVarPopOrderBy
Description
order by varPop() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 123.45, "endYear": 123.45, "startYear": 123.45, "teamId": 987.65}
Types
AthleteTeamVarSampOrderBy
Description
order by varSamp() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteTeamVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
athleteId - Float	
endYear - Float	
startYear - Float	
teamId - Float	
Example
{"athleteId": 987.65, "endYear": 987.65, "startYear": 987.65, "teamId": 987.65}
Types
AthleteTeamVarianceOrderBy
Description
order by variance() on columns of table "athlete_team"

Fields
Input Field	Description
athleteId - OrderBy	
endYear - OrderBy	
startYear - OrderBy	
teamId - OrderBy	
Example
{"athleteId": "ASC", "endYear": "ASC", "startYear": "ASC", "teamId": "ASC"}
Types
AthleteVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 123.45,
  "hometownId": 987.65,
  "id": 987.65,
  "jersey": 987.65,
  "positionId": 987.65,
  "teamId": 987.65,
  "weight": 123.45
}
Types
AthleteVarPopOrderBy
Description
order by varPop() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 987.65,
  "hometownId": 987.65,
  "id": 987.65,
  "jersey": 123.45,
  "positionId": 987.65,
  "teamId": 123.45,
  "weight": 123.45
}
Types
AthleteVarSampOrderBy
Description
order by varSamp() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
AthleteVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
height - Float	
hometownId - Float	
id - Float	
jersey - Float	
positionId - Float	
teamId - Float	
weight - Float	
Example
{
  "height": 987.65,
  "hometownId": 123.45,
  "id": 123.45,
  "jersey": 123.45,
  "positionId": 987.65,
  "teamId": 987.65,
  "weight": 123.45
}
Types
AthleteVarianceOrderBy
Description
order by variance() on columns of table "athlete"

Fields
Input Field	Description
height - OrderBy	
hometownId - OrderBy	
id - OrderBy	
jersey - OrderBy	
positionId - OrderBy	
teamId - OrderBy	
weight - OrderBy	
Example
{
  "height": "ASC",
  "hometownId": "ASC",
  "id": "ASC",
  "jersey": "ASC",
  "positionId": "ASC",
  "teamId": "ASC",
  "weight": "ASC"
}
Types
BigintComparisonExp
Description
Boolean expression to compare columns of type "bigint". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - bigint	
_gt - bigint	
_gte - bigint	
_in - [bigint!]	
_isNull - Boolean	
_lt - bigint	
_lte - bigint	
_neq - bigint	
_nin - [bigint!]	
Example
{
  "_eq": bigint,
  "_gt": bigint,
  "_gte": bigint,
  "_in": [bigint],
  "_isNull": false,
  "_lt": bigint,
  "_lte": bigint,
  "_neq": bigint,
  "_nin": [bigint]
}
Types
Boolean
Types
BooleanComparisonExp
Description
Boolean expression to compare columns of type "Boolean". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - Boolean	
_gt - Boolean	
_gte - Boolean	
_in - [Boolean!]	
_isNull - Boolean	
_lt - Boolean	
_lte - Boolean	
_neq - Boolean	
_nin - [Boolean!]	
Example
{
  "_eq": false,
  "_gt": true,
  "_gte": false,
  "_in": [true],
  "_isNull": true,
  "_lt": true,
  "_lte": false,
  "_neq": true,
  "_nin": [false]
}
Types
Calendar
Description
columns and relationships of "calendar"

Fields
Field Name	Description
endDate - timestamp!	
seasonType - season_type!	
startDate - timestamp!	
week - smallint!	
year - smallint!	
Example
{
  "endDate": timestamp,
  "seasonType": season_type,
  "startDate": timestamp,
  "week": smallint,
  "year": smallint
}
Types
CalendarBoolExp
Description
Boolean expression to filter rows from the table "calendar". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [CalendarBoolExp!]	
_not - CalendarBoolExp	
_or - [CalendarBoolExp!]	
endDate - TimestampComparisonExp	
seasonType - SeasonTypeComparisonExp	
startDate - TimestampComparisonExp	
week - SmallintComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [CalendarBoolExp],
  "_not": CalendarBoolExp,
  "_or": [CalendarBoolExp],
  "endDate": TimestampComparisonExp,
  "seasonType": SeasonTypeComparisonExp,
  "startDate": TimestampComparisonExp,
  "week": SmallintComparisonExp,
  "year": SmallintComparisonExp
}
Types
CalendarOrderBy
Description
Ordering options when selecting data from "calendar".

Fields
Input Field	Description
endDate - OrderBy	
seasonType - OrderBy	
startDate - OrderBy	
week - OrderBy	
year - OrderBy	
Example
{
  "endDate": "ASC",
  "seasonType": "ASC",
  "startDate": "ASC",
  "week": "ASC",
  "year": "ASC"
}
Types
CalendarSelectColumn
Description
select columns of table "calendar"

Values
Enum Value	Description
endDate

column name
seasonType

column name
startDate

column name
week

column name
year

column name
Example
"endDate"
Types
Coach
Description
columns and relationships of "coach"

Fields
Field Name	Description
firstName - String!	
id - Int!	
lastName - String!	
seasons - [CoachSeason!]!	An array relationship
Arguments
distinctOn - [CoachSeasonSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [CoachSeasonOrderBy!]
sort the rows by one or more columns

where - CoachSeasonBoolExp
filter the rows returned

seasonsAggregate - CoachSeasonAggregate!	An aggregate relationship
Arguments
distinctOn - [CoachSeasonSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [CoachSeasonOrderBy!]
sort the rows by one or more columns

where - CoachSeasonBoolExp
filter the rows returned

Example
{
  "firstName": "abc123",
  "id": 987,
  "lastName": "xyz789",
  "seasons": [CoachSeason],
  "seasonsAggregate": CoachSeasonAggregate
}
Types
CoachAggregate
Description
aggregated selection of "coach"

Fields
Field Name	Description
aggregate - CoachAggregateFields	
nodes - [Coach!]!	
Example
{
  "aggregate": CoachAggregateFields,
  "nodes": [Coach]
}
Types
CoachAggregateFields
Description
aggregate fields of "coach"

Fields
Field Name	Description
avg - CoachAvgFields	
count - Int!	
Arguments
columns - [CoachSelectColumn!]
distinct - Boolean
max - CoachMaxFields	
min - CoachMinFields	
stddev - CoachStddevFields	
stddevPop - CoachStddevPopFields	
stddevSamp - CoachStddevSampFields	
sum - CoachSumFields	
varPop - CoachVarPopFields	
varSamp - CoachVarSampFields	
variance - CoachVarianceFields	
Example
{
  "avg": CoachAvgFields,
  "count": 987,
  "max": CoachMaxFields,
  "min": CoachMinFields,
  "stddev": CoachStddevFields,
  "stddevPop": CoachStddevPopFields,
  "stddevSamp": CoachStddevSampFields,
  "sum": CoachSumFields,
  "varPop": CoachVarPopFields,
  "varSamp": CoachVarSampFields,
  "variance": CoachVarianceFields
}
Types
CoachAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
CoachBoolExp
Description
Boolean expression to filter rows from the table "coach". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [CoachBoolExp!]	
_not - CoachBoolExp	
_or - [CoachBoolExp!]	
firstName - StringComparisonExp	
id - IntComparisonExp	
lastName - StringComparisonExp	
seasons - CoachSeasonBoolExp	
seasonsAggregate - CoachSeasonAggregateBoolExp	
Example
{
  "_and": [CoachBoolExp],
  "_not": CoachBoolExp,
  "_or": [CoachBoolExp],
  "firstName": StringComparisonExp,
  "id": IntComparisonExp,
  "lastName": StringComparisonExp,
  "seasons": CoachSeasonBoolExp,
  "seasonsAggregate": CoachSeasonAggregateBoolExp
}
Types
CoachMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
firstName - String	
id - Int	
lastName - String	
Example
{
  "firstName": "xyz789",
  "id": 987,
  "lastName": "abc123"
}
Types
CoachMinFields
Description
aggregate min on columns

Fields
Field Name	Description
firstName - String	
id - Int	
lastName - String	
Example
{
  "firstName": "abc123",
  "id": 987,
  "lastName": "abc123"
}
Types
CoachOrderBy
Description
Ordering options when selecting data from "coach".

Fields
Input Field	Description
firstName - OrderBy	
id - OrderBy	
lastName - OrderBy	
seasonsAggregate - CoachSeasonAggregateOrderBy	
Example
{
  "firstName": "ASC",
  "id": "ASC",
  "lastName": "ASC",
  "seasonsAggregate": CoachSeasonAggregateOrderBy
}
Types
CoachSeason
Description
columns and relationships of "coach_season"

Fields
Field Name	Description
coach - Coach!	An object relationship
games - smallint!	
losses - smallint!	
postseasonRank - smallint	
preseasonRank - smallint	
team - currentTeams	An object relationship
ties - smallint!	
wins - smallint!	
year - smallint!	
Example
{
  "coach": Coach,
  "games": smallint,
  "losses": smallint,
  "postseasonRank": smallint,
  "preseasonRank": smallint,
  "team": currentTeams,
  "ties": smallint,
  "wins": smallint,
  "year": smallint
}
Types
CoachSeasonAggregate
Description
aggregated selection of "coach_season"

Fields
Field Name	Description
aggregate - CoachSeasonAggregateFields	
nodes - [CoachSeason!]!	
Example
{
  "aggregate": CoachSeasonAggregateFields,
  "nodes": [CoachSeason]
}
Types
CoachSeasonAggregateBoolExp
Fields
Input Field	Description
count - coachSeasonAggregateBoolExpCount	
Example
{"count": coachSeasonAggregateBoolExpCount}
Types
CoachSeasonAggregateFields
Description
aggregate fields of "coach_season"

Fields
Field Name	Description
avg - CoachSeasonAvgFields	
count - Int!	
Arguments
columns - [CoachSeasonSelectColumn!]
distinct - Boolean
max - CoachSeasonMaxFields	
min - CoachSeasonMinFields	
stddev - CoachSeasonStddevFields	
stddevPop - CoachSeasonStddevPopFields	
stddevSamp - CoachSeasonStddevSampFields	
sum - CoachSeasonSumFields	
varPop - CoachSeasonVarPopFields	
varSamp - CoachSeasonVarSampFields	
variance - CoachSeasonVarianceFields	
Example
{
  "avg": CoachSeasonAvgFields,
  "count": 123,
  "max": CoachSeasonMaxFields,
  "min": CoachSeasonMinFields,
  "stddev": CoachSeasonStddevFields,
  "stddevPop": CoachSeasonStddevPopFields,
  "stddevSamp": CoachSeasonStddevSampFields,
  "sum": CoachSeasonSumFields,
  "varPop": CoachSeasonVarPopFields,
  "varSamp": CoachSeasonVarSampFields,
  "variance": CoachSeasonVarianceFields
}
Types
CoachSeasonAggregateOrderBy
Description
order by aggregate values of table "coach_season"

Fields
Input Field	Description
avg - CoachSeasonAvgOrderBy	
count - OrderBy	
max - CoachSeasonMaxOrderBy	
min - CoachSeasonMinOrderBy	
stddev - CoachSeasonStddevOrderBy	
stddevPop - CoachSeasonStddevPopOrderBy	
stddevSamp - CoachSeasonStddevSampOrderBy	
sum - CoachSeasonSumOrderBy	
varPop - CoachSeasonVarPopOrderBy	
varSamp - CoachSeasonVarSampOrderBy	
variance - CoachSeasonVarianceOrderBy	
Example
{
  "avg": CoachSeasonAvgOrderBy,
  "count": "ASC",
  "max": CoachSeasonMaxOrderBy,
  "min": CoachSeasonMinOrderBy,
  "stddev": CoachSeasonStddevOrderBy,
  "stddevPop": CoachSeasonStddevPopOrderBy,
  "stddevSamp": CoachSeasonStddevSampOrderBy,
  "sum": CoachSeasonSumOrderBy,
  "varPop": CoachSeasonVarPopOrderBy,
  "varSamp": CoachSeasonVarSampOrderBy,
  "variance": CoachSeasonVarianceOrderBy
}
Types
CoachSeasonAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 123.45,
  "losses": 123.45,
  "postseasonRank": 987.65,
  "preseasonRank": 987.65,
  "ties": 123.45,
  "wins": 123.45,
  "year": 987.65
}
Types
CoachSeasonAvgOrderBy
Description
order by avg() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonBoolExp
Description
Boolean expression to filter rows from the table "coach_season". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [CoachSeasonBoolExp!]	
_not - CoachSeasonBoolExp	
_or - [CoachSeasonBoolExp!]	
coach - CoachBoolExp	
games - SmallintComparisonExp	
losses - SmallintComparisonExp	
postseasonRank - SmallintComparisonExp	
preseasonRank - SmallintComparisonExp	
team - currentTeamsBoolExp	
ties - SmallintComparisonExp	
wins - SmallintComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [CoachSeasonBoolExp],
  "_not": CoachSeasonBoolExp,
  "_or": [CoachSeasonBoolExp],
  "coach": CoachBoolExp,
  "games": SmallintComparisonExp,
  "losses": SmallintComparisonExp,
  "postseasonRank": SmallintComparisonExp,
  "preseasonRank": SmallintComparisonExp,
  "team": currentTeamsBoolExp,
  "ties": SmallintComparisonExp,
  "wins": SmallintComparisonExp,
  "year": SmallintComparisonExp
}
Types
CoachSeasonMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
games - smallint	
losses - smallint	
postseasonRank - smallint	
preseasonRank - smallint	
ties - smallint	
wins - smallint	
year - smallint	
Example
{
  "games": smallint,
  "losses": smallint,
  "postseasonRank": smallint,
  "preseasonRank": smallint,
  "ties": smallint,
  "wins": smallint,
  "year": smallint
}
Types
CoachSeasonMaxOrderBy
Description
order by max() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonMinFields
Description
aggregate min on columns

Fields
Field Name	Description
games - smallint	
losses - smallint	
postseasonRank - smallint	
preseasonRank - smallint	
ties - smallint	
wins - smallint	
year - smallint	
Example
{
  "games": smallint,
  "losses": smallint,
  "postseasonRank": smallint,
  "preseasonRank": smallint,
  "ties": smallint,
  "wins": smallint,
  "year": smallint
}
Types
CoachSeasonMinOrderBy
Description
order by min() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonOrderBy
Description
Ordering options when selecting data from "coach_season".

Fields
Input Field	Description
coach - CoachOrderBy	
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
team - currentTeamsOrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "coach": CoachOrderBy,
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "team": currentTeamsOrderBy,
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonSelectColumn
Description
select columns of table "coach_season"

Values
Enum Value	Description
games

column name
losses

column name
postseasonRank

column name
preseasonRank

column name
ties

column name
wins

column name
year

column name
Example
"games"
Types
CoachSeasonStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 123.45,
  "losses": 987.65,
  "postseasonRank": 987.65,
  "preseasonRank": 123.45,
  "ties": 123.45,
  "wins": 123.45,
  "year": 123.45
}
Types
CoachSeasonStddevOrderBy
Description
order by stddev() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 123.45,
  "losses": 123.45,
  "postseasonRank": 987.65,
  "preseasonRank": 123.45,
  "ties": 987.65,
  "wins": 123.45,
  "year": 987.65
}
Types
CoachSeasonStddevPopOrderBy
Description
order by stddevPop() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 987.65,
  "losses": 123.45,
  "postseasonRank": 987.65,
  "preseasonRank": 987.65,
  "ties": 123.45,
  "wins": 123.45,
  "year": 123.45
}
Types
CoachSeasonStddevSampOrderBy
Description
order by stddevSamp() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
games - smallint	
losses - smallint	
postseasonRank - smallint	
preseasonRank - smallint	
ties - smallint	
wins - smallint	
year - smallint	
Example
{
  "games": smallint,
  "losses": smallint,
  "postseasonRank": smallint,
  "preseasonRank": smallint,
  "ties": smallint,
  "wins": smallint,
  "year": smallint
}
Types
CoachSeasonSumOrderBy
Description
order by sum() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 123.45,
  "losses": 123.45,
  "postseasonRank": 987.65,
  "preseasonRank": 987.65,
  "ties": 987.65,
  "wins": 987.65,
  "year": 987.65
}
Types
CoachSeasonVarPopOrderBy
Description
order by varPop() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 123.45,
  "losses": 987.65,
  "postseasonRank": 123.45,
  "preseasonRank": 123.45,
  "ties": 123.45,
  "wins": 123.45,
  "year": 123.45
}
Types
CoachSeasonVarSampOrderBy
Description
order by varSamp() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSeasonVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
games - Float	
losses - Float	
postseasonRank - Float	
preseasonRank - Float	
ties - Float	
wins - Float	
year - Float	
Example
{
  "games": 987.65,
  "losses": 123.45,
  "postseasonRank": 987.65,
  "preseasonRank": 987.65,
  "ties": 987.65,
  "wins": 123.45,
  "year": 987.65
}
Types
CoachSeasonVarianceOrderBy
Description
order by variance() on columns of table "coach_season"

Fields
Input Field	Description
games - OrderBy	
losses - OrderBy	
postseasonRank - OrderBy	
preseasonRank - OrderBy	
ties - OrderBy	
wins - OrderBy	
year - OrderBy	
Example
{
  "games": "ASC",
  "losses": "ASC",
  "postseasonRank": "ASC",
  "preseasonRank": "ASC",
  "ties": "ASC",
  "wins": "ASC",
  "year": "ASC"
}
Types
CoachSelectColumn
Description
select columns of table "coach"

Values
Enum Value	Description
firstName

column name
id

column name
lastName

column name
Example
"firstName"
Types
CoachStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
CoachStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
CoachStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
CoachSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
id - Int	
Example
{"id": 123}
Types
CoachVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
CoachVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
CoachVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
Conference
Description
columns and relationships of "conference"

Fields
Field Name	Description
abbreviation - String	
division - division	
id - smallint!	
name - String!	
shortName - String	
srName - String	
Example
{
  "abbreviation": "abc123",
  "division": division,
  "id": smallint,
  "name": "xyz789",
  "shortName": "abc123",
  "srName": "abc123"
}
Types
ConferenceBoolExp
Description
Boolean expression to filter rows from the table "conference". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [ConferenceBoolExp!]	
_not - ConferenceBoolExp	
_or - [ConferenceBoolExp!]	
abbreviation - StringComparisonExp	
division - DivisionComparisonExp	
id - SmallintComparisonExp	
name - StringComparisonExp	
shortName - StringComparisonExp	
srName - StringComparisonExp	
Example
{
  "_and": [ConferenceBoolExp],
  "_not": ConferenceBoolExp,
  "_or": [ConferenceBoolExp],
  "abbreviation": StringComparisonExp,
  "division": DivisionComparisonExp,
  "id": SmallintComparisonExp,
  "name": StringComparisonExp,
  "shortName": StringComparisonExp,
  "srName": StringComparisonExp
}
Types
ConferenceOrderBy
Description
Ordering options when selecting data from "conference".

Fields
Input Field	Description
abbreviation - OrderBy	
division - OrderBy	
id - OrderBy	
name - OrderBy	
shortName - OrderBy	
srName - OrderBy	
Example
{
  "abbreviation": "ASC",
  "division": "ASC",
  "id": "ASC",
  "name": "ASC",
  "shortName": "ASC",
  "srName": "ASC"
}
Types
ConferenceSelectColumn
Description
select columns of table "conference"

Values
Enum Value	Description
abbreviation

column name
division

column name
id

column name
name

column name
shortName

column name
srName

column name
Example
"abbreviation"
Types
DivisionComparisonExp
Description
Boolean expression to compare columns of type "division". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - division	
_gt - division	
_gte - division	
_in - [division!]	
_isNull - Boolean	
_lt - division	
_lte - division	
_neq - division	
_nin - [division!]	
Example
{
  "_eq": division,
  "_gt": division,
  "_gte": division,
  "_in": [division],
  "_isNull": true,
  "_lt": division,
  "_lte": division,
  "_neq": division,
  "_nin": [division]
}
Types
DraftPicks
Description
columns and relationships of "draft_picks"

Fields
Field Name	Description
collegeAthleteRecord - Athlete	An object relationship
collegeId - Int	
collegeTeam - historicalTeam	An object relationship
collegeTeamId - Int!	
draftTeam - DraftTeam!	An object relationship
grade - smallint	
height - smallint	
name - String!	
nflTeamId - smallint!	
overall - smallint!	
overallRank - smallint	
pick - smallint!	
position - DraftPosition!	An object relationship
positionId - smallint!	
positionRank - smallint	
round - smallint!	
weight - smallint	
year - smallint!	
Example
{
  "collegeAthleteRecord": Athlete,
  "collegeId": 123,
  "collegeTeam": historicalTeam,
  "collegeTeamId": 123,
  "draftTeam": DraftTeam,
  "grade": smallint,
  "height": smallint,
  "name": "abc123",
  "nflTeamId": smallint,
  "overall": smallint,
  "overallRank": smallint,
  "pick": smallint,
  "position": DraftPosition,
  "positionId": smallint,
  "positionRank": smallint,
  "round": smallint,
  "weight": smallint,
  "year": smallint
}
Types
DraftPicksAggregate
Description
aggregated selection of "draft_picks"

Fields
Field Name	Description
aggregate - DraftPicksAggregateFields	
nodes - [DraftPicks!]!	
Example
{
  "aggregate": DraftPicksAggregateFields,
  "nodes": [DraftPicks]
}
Types
DraftPicksAggregateBoolExp
Fields
Input Field	Description
count - draftPicksAggregateBoolExpCount	
Example
{"count": draftPicksAggregateBoolExpCount}
Types
DraftPicksAggregateFields
Description
aggregate fields of "draft_picks"

Fields
Field Name	Description
avg - DraftPicksAvgFields	
count - Int!	
Arguments
columns - [DraftPicksSelectColumn!]
distinct - Boolean
max - DraftPicksMaxFields	
min - DraftPicksMinFields	
stddev - DraftPicksStddevFields	
stddevPop - DraftPicksStddevPopFields	
stddevSamp - DraftPicksStddevSampFields	
sum - DraftPicksSumFields	
varPop - DraftPicksVarPopFields	
varSamp - DraftPicksVarSampFields	
variance - DraftPicksVarianceFields	
Example
{
  "avg": DraftPicksAvgFields,
  "count": 123,
  "max": DraftPicksMaxFields,
  "min": DraftPicksMinFields,
  "stddev": DraftPicksStddevFields,
  "stddevPop": DraftPicksStddevPopFields,
  "stddevSamp": DraftPicksStddevSampFields,
  "sum": DraftPicksSumFields,
  "varPop": DraftPicksVarPopFields,
  "varSamp": DraftPicksVarSampFields,
  "variance": DraftPicksVarianceFields
}
Types
DraftPicksAggregateOrderBy
Description
order by aggregate values of table "draft_picks"

Fields
Input Field	Description
avg - DraftPicksAvgOrderBy	
count - OrderBy	
max - DraftPicksMaxOrderBy	
min - DraftPicksMinOrderBy	
stddev - DraftPicksStddevOrderBy	
stddevPop - DraftPicksStddevPopOrderBy	
stddevSamp - DraftPicksStddevSampOrderBy	
sum - DraftPicksSumOrderBy	
varPop - DraftPicksVarPopOrderBy	
varSamp - DraftPicksVarSampOrderBy	
variance - DraftPicksVarianceOrderBy	
Example
{
  "avg": DraftPicksAvgOrderBy,
  "count": "ASC",
  "max": DraftPicksMaxOrderBy,
  "min": DraftPicksMinOrderBy,
  "stddev": DraftPicksStddevOrderBy,
  "stddevPop": DraftPicksStddevPopOrderBy,
  "stddevSamp": DraftPicksStddevSampOrderBy,
  "sum": DraftPicksSumOrderBy,
  "varPop": DraftPicksVarPopOrderBy,
  "varSamp": DraftPicksVarSampOrderBy,
  "variance": DraftPicksVarianceOrderBy
}
Types
DraftPicksAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 123.45,
  "grade": 987.65,
  "height": 987.65,
  "nflTeamId": 123.45,
  "overall": 123.45,
  "overallRank": 987.65,
  "pick": 987.65,
  "positionId": 123.45,
  "positionRank": 123.45,
  "round": 987.65,
  "weight": 987.65,
  "year": 987.65
}
Types
DraftPicksAvgOrderBy
Description
order by avg() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksBoolExp
Description
Boolean expression to filter rows from the table "draft_picks". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [DraftPicksBoolExp!]	
_not - DraftPicksBoolExp	
_or - [DraftPicksBoolExp!]	
collegeAthleteRecord - AthleteBoolExp	
collegeId - IntComparisonExp	
collegeTeam - historicalTeamBoolExp	
collegeTeamId - IntComparisonExp	
draftTeam - DraftTeamBoolExp	
grade - SmallintComparisonExp	
height - SmallintComparisonExp	
name - StringComparisonExp	
nflTeamId - SmallintComparisonExp	
overall - SmallintComparisonExp	
overallRank - SmallintComparisonExp	
pick - SmallintComparisonExp	
position - DraftPositionBoolExp	
positionId - SmallintComparisonExp	
positionRank - SmallintComparisonExp	
round - SmallintComparisonExp	
weight - SmallintComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [DraftPicksBoolExp],
  "_not": DraftPicksBoolExp,
  "_or": [DraftPicksBoolExp],
  "collegeAthleteRecord": AthleteBoolExp,
  "collegeId": IntComparisonExp,
  "collegeTeam": historicalTeamBoolExp,
  "collegeTeamId": IntComparisonExp,
  "draftTeam": DraftTeamBoolExp,
  "grade": SmallintComparisonExp,
  "height": SmallintComparisonExp,
  "name": StringComparisonExp,
  "nflTeamId": SmallintComparisonExp,
  "overall": SmallintComparisonExp,
  "overallRank": SmallintComparisonExp,
  "pick": SmallintComparisonExp,
  "position": DraftPositionBoolExp,
  "positionId": SmallintComparisonExp,
  "positionRank": SmallintComparisonExp,
  "round": SmallintComparisonExp,
  "weight": SmallintComparisonExp,
  "year": SmallintComparisonExp
}
Types
DraftPicksMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
collegeId - Int	
collegeTeamId - Int	
grade - smallint	
height - smallint	
name - String	
nflTeamId - smallint	
overall - smallint	
overallRank - smallint	
pick - smallint	
positionId - smallint	
positionRank - smallint	
round - smallint	
weight - smallint	
year - smallint	
Example
{
  "collegeId": 123,
  "collegeTeamId": 123,
  "grade": smallint,
  "height": smallint,
  "name": "xyz789",
  "nflTeamId": smallint,
  "overall": smallint,
  "overallRank": smallint,
  "pick": smallint,
  "positionId": smallint,
  "positionRank": smallint,
  "round": smallint,
  "weight": smallint,
  "year": smallint
}
Types
DraftPicksMaxOrderBy
Description
order by max() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
name - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "name": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksMinFields
Description
aggregate min on columns

Fields
Field Name	Description
collegeId - Int	
collegeTeamId - Int	
grade - smallint	
height - smallint	
name - String	
nflTeamId - smallint	
overall - smallint	
overallRank - smallint	
pick - smallint	
positionId - smallint	
positionRank - smallint	
round - smallint	
weight - smallint	
year - smallint	
Example
{
  "collegeId": 123,
  "collegeTeamId": 123,
  "grade": smallint,
  "height": smallint,
  "name": "abc123",
  "nflTeamId": smallint,
  "overall": smallint,
  "overallRank": smallint,
  "pick": smallint,
  "positionId": smallint,
  "positionRank": smallint,
  "round": smallint,
  "weight": smallint,
  "year": smallint
}
Types
DraftPicksMinOrderBy
Description
order by min() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
name - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "name": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksOrderBy
Description
Ordering options when selecting data from "draft_picks".

Fields
Input Field	Description
collegeAthleteRecord - AthleteOrderBy	
collegeId - OrderBy	
collegeTeam - historicalTeamOrderBy	
collegeTeamId - OrderBy	
draftTeam - DraftTeamOrderBy	
grade - OrderBy	
height - OrderBy	
name - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
position - DraftPositionOrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeAthleteRecord": AthleteOrderBy,
  "collegeId": "ASC",
  "collegeTeam": historicalTeamOrderBy,
  "collegeTeamId": "ASC",
  "draftTeam": DraftTeamOrderBy,
  "grade": "ASC",
  "height": "ASC",
  "name": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "position": DraftPositionOrderBy,
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksSelectColumn
Description
select columns of table "draft_picks"

Values
Enum Value	Description
collegeId

column name
collegeTeamId

column name
grade

column name
height

column name
name

column name
nflTeamId

column name
overall

column name
overallRank

column name
pick

column name
positionId

column name
positionRank

column name
round

column name
weight

column name
year

column name
Example
"collegeId"
Types
DraftPicksStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 123.45,
  "grade": 123.45,
  "height": 987.65,
  "nflTeamId": 987.65,
  "overall": 987.65,
  "overallRank": 987.65,
  "pick": 987.65,
  "positionId": 987.65,
  "positionRank": 987.65,
  "round": 123.45,
  "weight": 123.45,
  "year": 987.65
}
Types
DraftPicksStddevOrderBy
Description
order by stddev() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 987.65,
  "grade": 987.65,
  "height": 123.45,
  "nflTeamId": 123.45,
  "overall": 987.65,
  "overallRank": 987.65,
  "pick": 123.45,
  "positionId": 123.45,
  "positionRank": 987.65,
  "round": 123.45,
  "weight": 123.45,
  "year": 987.65
}
Types
DraftPicksStddevPopOrderBy
Description
order by stddevPop() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 123.45,
  "grade": 987.65,
  "height": 987.65,
  "nflTeamId": 123.45,
  "overall": 123.45,
  "overallRank": 987.65,
  "pick": 987.65,
  "positionId": 987.65,
  "positionRank": 987.65,
  "round": 987.65,
  "weight": 123.45,
  "year": 123.45
}
Types
DraftPicksStddevSampOrderBy
Description
order by stddevSamp() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
collegeId - Int	
collegeTeamId - Int	
grade - smallint	
height - smallint	
nflTeamId - smallint	
overall - smallint	
overallRank - smallint	
pick - smallint	
positionId - smallint	
positionRank - smallint	
round - smallint	
weight - smallint	
year - smallint	
Example
{
  "collegeId": 987,
  "collegeTeamId": 987,
  "grade": smallint,
  "height": smallint,
  "nflTeamId": smallint,
  "overall": smallint,
  "overallRank": smallint,
  "pick": smallint,
  "positionId": smallint,
  "positionRank": smallint,
  "round": smallint,
  "weight": smallint,
  "year": smallint
}
Types
DraftPicksSumOrderBy
Description
order by sum() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 123.45,
  "collegeTeamId": 123.45,
  "grade": 987.65,
  "height": 987.65,
  "nflTeamId": 987.65,
  "overall": 123.45,
  "overallRank": 123.45,
  "pick": 987.65,
  "positionId": 987.65,
  "positionRank": 987.65,
  "round": 123.45,
  "weight": 123.45,
  "year": 123.45
}
Types
DraftPicksVarPopOrderBy
Description
order by varPop() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 123.45,
  "grade": 987.65,
  "height": 123.45,
  "nflTeamId": 987.65,
  "overall": 123.45,
  "overallRank": 987.65,
  "pick": 123.45,
  "positionId": 123.45,
  "positionRank": 987.65,
  "round": 123.45,
  "weight": 123.45,
  "year": 123.45
}
Types
DraftPicksVarSampOrderBy
Description
order by varSamp() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPicksVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
collegeId - Float	
collegeTeamId - Float	
grade - Float	
height - Float	
nflTeamId - Float	
overall - Float	
overallRank - Float	
pick - Float	
positionId - Float	
positionRank - Float	
round - Float	
weight - Float	
year - Float	
Example
{
  "collegeId": 987.65,
  "collegeTeamId": 123.45,
  "grade": 123.45,
  "height": 987.65,
  "nflTeamId": 123.45,
  "overall": 987.65,
  "overallRank": 123.45,
  "pick": 123.45,
  "positionId": 123.45,
  "positionRank": 987.65,
  "round": 123.45,
  "weight": 123.45,
  "year": 987.65
}
Types
DraftPicksVarianceOrderBy
Description
order by variance() on columns of table "draft_picks"

Fields
Input Field	Description
collegeId - OrderBy	
collegeTeamId - OrderBy	
grade - OrderBy	
height - OrderBy	
nflTeamId - OrderBy	
overall - OrderBy	
overallRank - OrderBy	
pick - OrderBy	
positionId - OrderBy	
positionRank - OrderBy	
round - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "collegeId": "ASC",
  "collegeTeamId": "ASC",
  "grade": "ASC",
  "height": "ASC",
  "nflTeamId": "ASC",
  "overall": "ASC",
  "overallRank": "ASC",
  "pick": "ASC",
  "positionId": "ASC",
  "positionRank": "ASC",
  "round": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
DraftPosition
Description
columns and relationships of "draft_position"

Fields
Field Name	Description
abbreviation - String!	
id - smallint!	
name - String!	
Example
{
  "abbreviation": "abc123",
  "id": smallint,
  "name": "xyz789"
}
Types
DraftPositionBoolExp
Description
Boolean expression to filter rows from the table "draft_position". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [DraftPositionBoolExp!]	
_not - DraftPositionBoolExp	
_or - [DraftPositionBoolExp!]	
abbreviation - StringComparisonExp	
id - SmallintComparisonExp	
name - StringComparisonExp	
Example
{
  "_and": [DraftPositionBoolExp],
  "_not": DraftPositionBoolExp,
  "_or": [DraftPositionBoolExp],
  "abbreviation": StringComparisonExp,
  "id": SmallintComparisonExp,
  "name": StringComparisonExp
}
Types
DraftPositionOrderBy
Description
Ordering options when selecting data from "draft_position".

Fields
Input Field	Description
abbreviation - OrderBy	
id - OrderBy	
name - OrderBy	
Example
{"abbreviation": "ASC", "id": "ASC", "name": "ASC"}
Types
DraftPositionSelectColumn
Description
select columns of table "draft_position"

Values
Enum Value	Description
abbreviation

column name
id

column name
name

column name
Example
"abbreviation"
Types
DraftTeam
Description
columns and relationships of "draft_team"

Fields
Field Name	Description
displayName - String	
id - smallint!	
location - String!	
logo - String	
mascot - String	
nickname - String	
picks - [DraftPicks!]!	An array relationship
Arguments
distinctOn - [DraftPicksSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [DraftPicksOrderBy!]
sort the rows by one or more columns

where - DraftPicksBoolExp
filter the rows returned

picksAggregate - DraftPicksAggregate!	An aggregate relationship
Arguments
distinctOn - [DraftPicksSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [DraftPicksOrderBy!]
sort the rows by one or more columns

where - DraftPicksBoolExp
filter the rows returned

shortDisplayName - String	
Example
{
  "displayName": "abc123",
  "id": smallint,
  "location": "abc123",
  "logo": "xyz789",
  "mascot": "abc123",
  "nickname": "xyz789",
  "picks": [DraftPicks],
  "picksAggregate": DraftPicksAggregate,
  "shortDisplayName": "xyz789"
}
Types
DraftTeamBoolExp
Description
Boolean expression to filter rows from the table "draft_team". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [DraftTeamBoolExp!]	
_not - DraftTeamBoolExp	
_or - [DraftTeamBoolExp!]	
displayName - StringComparisonExp	
id - SmallintComparisonExp	
location - StringComparisonExp	
logo - StringComparisonExp	
mascot - StringComparisonExp	
nickname - StringComparisonExp	
picks - DraftPicksBoolExp	
picksAggregate - DraftPicksAggregateBoolExp	
shortDisplayName - StringComparisonExp	
Example
{
  "_and": [DraftTeamBoolExp],
  "_not": DraftTeamBoolExp,
  "_or": [DraftTeamBoolExp],
  "displayName": StringComparisonExp,
  "id": SmallintComparisonExp,
  "location": StringComparisonExp,
  "logo": StringComparisonExp,
  "mascot": StringComparisonExp,
  "nickname": StringComparisonExp,
  "picks": DraftPicksBoolExp,
  "picksAggregate": DraftPicksAggregateBoolExp,
  "shortDisplayName": StringComparisonExp
}
Types
DraftTeamOrderBy
Description
Ordering options when selecting data from "draft_team".

Fields
Input Field	Description
displayName - OrderBy	
id - OrderBy	
location - OrderBy	
logo - OrderBy	
mascot - OrderBy	
nickname - OrderBy	
picksAggregate - DraftPicksAggregateOrderBy	
shortDisplayName - OrderBy	
Example
{
  "displayName": "ASC",
  "id": "ASC",
  "location": "ASC",
  "logo": "ASC",
  "mascot": "ASC",
  "nickname": "ASC",
  "picksAggregate": DraftPicksAggregateOrderBy,
  "shortDisplayName": "ASC"
}
Types
DraftTeamSelectColumn
Description
select columns of table "draft_team"

Values
Enum Value	Description
displayName

column name
id

column name
location

column name
logo

column name
mascot

column name
nickname

column name
shortDisplayName

column name
Example
"displayName"
Types
Float
Example
123.45
Types
FloatComparisonExp
Description
Boolean expression to compare columns of type "Float". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - Float	
_gt - Float	
_gte - Float	
_in - [Float!]	
_isNull - Boolean	
_lt - Float	
_lte - Float	
_neq - Float	
_nin - [Float!]	
Example
{
  "_eq": 123.45,
  "_gt": 123.45,
  "_gte": 987.65,
  "_in": [987.65],
  "_isNull": false,
  "_lt": 123.45,
  "_lte": 123.45,
  "_neq": 987.65,
  "_nin": [987.65]
}
Types
GameLines
Description
columns and relationships of "game_lines"

Fields
Field Name	Description
gameId - Int!	
linesProviderId - Int!	
moneylineAway - Int	
moneylineHome - Int	
overUnder - numeric	
overUnderOpen - numeric	
provider - LinesProvider	An object relationship
spread - numeric	
spreadOpen - numeric	
Example
{
  "gameId": 123,
  "linesProviderId": 987,
  "moneylineAway": 987,
  "moneylineHome": 123,
  "overUnder": numeric,
  "overUnderOpen": numeric,
  "provider": LinesProvider,
  "spread": numeric,
  "spreadOpen": numeric
}
Types
GameLinesAggregate
Description
aggregated selection of "game_lines"

Fields
Field Name	Description
aggregate - GameLinesAggregateFields	
nodes - [GameLines!]!	
Example
{
  "aggregate": GameLinesAggregateFields,
  "nodes": [GameLines]
}
Types
GameLinesAggregateBoolExp
Fields
Input Field	Description
count - gameLinesAggregateBoolExpCount	
Example
{"count": gameLinesAggregateBoolExpCount}
Types
GameLinesAggregateFields
Description
aggregate fields of "game_lines"

Fields
Field Name	Description
avg - GameLinesAvgFields	
count - Int!	
Arguments
columns - [GameLinesSelectColumn!]
distinct - Boolean
max - GameLinesMaxFields	
min - GameLinesMinFields	
stddev - GameLinesStddevFields	
stddevPop - GameLinesStddevPopFields	
stddevSamp - GameLinesStddevSampFields	
sum - GameLinesSumFields	
varPop - GameLinesVarPopFields	
varSamp - GameLinesVarSampFields	
variance - GameLinesVarianceFields	
Example
{
  "avg": GameLinesAvgFields,
  "count": 987,
  "max": GameLinesMaxFields,
  "min": GameLinesMinFields,
  "stddev": GameLinesStddevFields,
  "stddevPop": GameLinesStddevPopFields,
  "stddevSamp": GameLinesStddevSampFields,
  "sum": GameLinesSumFields,
  "varPop": GameLinesVarPopFields,
  "varSamp": GameLinesVarSampFields,
  "variance": GameLinesVarianceFields
}
Types
GameLinesAggregateOrderBy
Description
order by aggregate values of table "game_lines"

Fields
Input Field	Description
avg - GameLinesAvgOrderBy	
count - OrderBy	
max - GameLinesMaxOrderBy	
min - GameLinesMinOrderBy	
stddev - GameLinesStddevOrderBy	
stddevPop - GameLinesStddevPopOrderBy	
stddevSamp - GameLinesStddevSampOrderBy	
sum - GameLinesSumOrderBy	
varPop - GameLinesVarPopOrderBy	
varSamp - GameLinesVarSampOrderBy	
variance - GameLinesVarianceOrderBy	
Example
{
  "avg": GameLinesAvgOrderBy,
  "count": "ASC",
  "max": GameLinesMaxOrderBy,
  "min": GameLinesMinOrderBy,
  "stddev": GameLinesStddevOrderBy,
  "stddevPop": GameLinesStddevPopOrderBy,
  "stddevSamp": GameLinesStddevSampOrderBy,
  "sum": GameLinesSumOrderBy,
  "varPop": GameLinesVarPopOrderBy,
  "varSamp": GameLinesVarSampOrderBy,
  "variance": GameLinesVarianceOrderBy
}
Types
GameLinesAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 987.65,
  "linesProviderId": 123.45,
  "moneylineAway": 987.65,
  "moneylineHome": 987.65,
  "overUnder": 123.45,
  "overUnderOpen": 123.45,
  "spread": 123.45,
  "spreadOpen": 123.45
}
Types
GameLinesAvgOrderBy
Description
order by avg() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesBoolExp
Description
Boolean expression to filter rows from the table "game_lines". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [GameLinesBoolExp!]	
_not - GameLinesBoolExp	
_or - [GameLinesBoolExp!]	
gameId - IntComparisonExp	
linesProviderId - IntComparisonExp	
moneylineAway - IntComparisonExp	
moneylineHome - IntComparisonExp	
overUnder - NumericComparisonExp	
overUnderOpen - NumericComparisonExp	
provider - LinesProviderBoolExp	
spread - NumericComparisonExp	
spreadOpen - NumericComparisonExp	
Example
{
  "_and": [GameLinesBoolExp],
  "_not": GameLinesBoolExp,
  "_or": [GameLinesBoolExp],
  "gameId": IntComparisonExp,
  "linesProviderId": IntComparisonExp,
  "moneylineAway": IntComparisonExp,
  "moneylineHome": IntComparisonExp,
  "overUnder": NumericComparisonExp,
  "overUnderOpen": NumericComparisonExp,
  "provider": LinesProviderBoolExp,
  "spread": NumericComparisonExp,
  "spreadOpen": NumericComparisonExp
}
Types
GameLinesMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
gameId - Int	
linesProviderId - Int	
moneylineAway - Int	
moneylineHome - Int	
overUnder - numeric	
overUnderOpen - numeric	
spread - numeric	
spreadOpen - numeric	
Example
{
  "gameId": 123,
  "linesProviderId": 987,
  "moneylineAway": 987,
  "moneylineHome": 123,
  "overUnder": numeric,
  "overUnderOpen": numeric,
  "spread": numeric,
  "spreadOpen": numeric
}
Types
GameLinesMaxOrderBy
Description
order by max() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesMinFields
Description
aggregate min on columns

Fields
Field Name	Description
gameId - Int	
linesProviderId - Int	
moneylineAway - Int	
moneylineHome - Int	
overUnder - numeric	
overUnderOpen - numeric	
spread - numeric	
spreadOpen - numeric	
Example
{
  "gameId": 987,
  "linesProviderId": 123,
  "moneylineAway": 987,
  "moneylineHome": 987,
  "overUnder": numeric,
  "overUnderOpen": numeric,
  "spread": numeric,
  "spreadOpen": numeric
}
Types
GameLinesMinOrderBy
Description
order by min() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesOrderBy
Description
Ordering options when selecting data from "game_lines".

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
provider - LinesProviderOrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "provider": LinesProviderOrderBy,
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesSelectColumn
Description
select columns of table "game_lines"

Values
Enum Value	Description
gameId

column name
linesProviderId

column name
moneylineAway

column name
moneylineHome

column name
overUnder

column name
overUnderOpen

column name
spread

column name
spreadOpen

column name
Example
"gameId"
Types
GameLinesStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 123.45,
  "linesProviderId": 123.45,
  "moneylineAway": 987.65,
  "moneylineHome": 123.45,
  "overUnder": 987.65,
  "overUnderOpen": 123.45,
  "spread": 123.45,
  "spreadOpen": 123.45
}
Types
GameLinesStddevOrderBy
Description
order by stddev() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 987.65,
  "linesProviderId": 123.45,
  "moneylineAway": 123.45,
  "moneylineHome": 123.45,
  "overUnder": 987.65,
  "overUnderOpen": 123.45,
  "spread": 123.45,
  "spreadOpen": 987.65
}
Types
GameLinesStddevPopOrderBy
Description
order by stddevPop() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 123.45,
  "linesProviderId": 987.65,
  "moneylineAway": 123.45,
  "moneylineHome": 987.65,
  "overUnder": 987.65,
  "overUnderOpen": 123.45,
  "spread": 987.65,
  "spreadOpen": 123.45
}
Types
GameLinesStddevSampOrderBy
Description
order by stddevSamp() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
gameId - Int	
linesProviderId - Int	
moneylineAway - Int	
moneylineHome - Int	
overUnder - numeric	
overUnderOpen - numeric	
spread - numeric	
spreadOpen - numeric	
Example
{
  "gameId": 987,
  "linesProviderId": 123,
  "moneylineAway": 123,
  "moneylineHome": 987,
  "overUnder": numeric,
  "overUnderOpen": numeric,
  "spread": numeric,
  "spreadOpen": numeric
}
Types
GameLinesSumOrderBy
Description
order by sum() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 123.45,
  "linesProviderId": 123.45,
  "moneylineAway": 987.65,
  "moneylineHome": 123.45,
  "overUnder": 123.45,
  "overUnderOpen": 123.45,
  "spread": 987.65,
  "spreadOpen": 123.45
}
Types
GameLinesVarPopOrderBy
Description
order by varPop() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 123.45,
  "linesProviderId": 123.45,
  "moneylineAway": 123.45,
  "moneylineHome": 123.45,
  "overUnder": 987.65,
  "overUnderOpen": 123.45,
  "spread": 123.45,
  "spreadOpen": 123.45
}
Types
GameLinesVarSampOrderBy
Description
order by varSamp() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameLinesVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
gameId - Float	
linesProviderId - Float	
moneylineAway - Float	
moneylineHome - Float	
overUnder - Float	
overUnderOpen - Float	
spread - Float	
spreadOpen - Float	
Example
{
  "gameId": 123.45,
  "linesProviderId": 987.65,
  "moneylineAway": 123.45,
  "moneylineHome": 987.65,
  "overUnder": 123.45,
  "overUnderOpen": 987.65,
  "spread": 987.65,
  "spreadOpen": 987.65
}
Types
GameLinesVarianceOrderBy
Description
order by variance() on columns of table "game_lines"

Fields
Input Field	Description
gameId - OrderBy	
linesProviderId - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
overUnder - OrderBy	
overUnderOpen - OrderBy	
spread - OrderBy	
spreadOpen - OrderBy	
Example
{
  "gameId": "ASC",
  "linesProviderId": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "overUnder": "ASC",
  "overUnderOpen": "ASC",
  "spread": "ASC",
  "spreadOpen": "ASC"
}
Types
GameMedia
Description
columns and relationships of "game_media"

Fields
Field Name	Description
mediaType - media_type!	
name - String!	
Example
{
  "mediaType": media_type,
  "name": "xyz789"
}
Types
GameMediaAggregateOrderBy
Description
order by aggregate values of table "game_media"

Fields
Input Field	Description
count - OrderBy	
max - GameMediaMaxOrderBy	
min - GameMediaMinOrderBy	
Example
{
  "count": "ASC",
  "max": GameMediaMaxOrderBy,
  "min": GameMediaMinOrderBy
}
Types
GameMediaBoolExp
Description
Boolean expression to filter rows from the table "game_media". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [GameMediaBoolExp!]	
_not - GameMediaBoolExp	
_or - [GameMediaBoolExp!]	
mediaType - MediaTypeComparisonExp	
name - StringComparisonExp	
Example
{
  "_and": [GameMediaBoolExp],
  "_not": GameMediaBoolExp,
  "_or": [GameMediaBoolExp],
  "mediaType": MediaTypeComparisonExp,
  "name": StringComparisonExp
}
Types
GameMediaMaxOrderBy
Description
order by max() on columns of table "game_media"

Fields
Input Field	Description
mediaType - OrderBy	
name - OrderBy	
Example
{"mediaType": "ASC", "name": "ASC"}
Types
GameMediaMinOrderBy
Description
order by min() on columns of table "game_media"

Fields
Input Field	Description
mediaType - OrderBy	
name - OrderBy	
Example
{"mediaType": "ASC", "name": "ASC"}
Types
GameMediaOrderBy
Description
Ordering options when selecting data from "game_media".

Fields
Input Field	Description
mediaType - OrderBy	
name - OrderBy	
Example
{"mediaType": "ASC", "name": "ASC"}
Types
GameMediaSelectColumn
Description
select columns of table "game_media"

Values
Enum Value	Description
mediaType

column name
name

column name
Example
"mediaType"
Types
GamePlayerStat
Description
columns and relationships of "game_player_stat"

Fields
Field Name	Description
athlete - Athlete!	An object relationship
athleteId - bigint!	
gameTeam - GameTeam!	An object relationship
gameTeamId - bigint!	
id - bigint!	
playerStatCategory - PlayerStatCategory!	An object relationship
playerStatType - PlayerStatType!	An object relationship
stat - String!	
Example
{
  "athlete": Athlete,
  "athleteId": bigint,
  "gameTeam": GameTeam,
  "gameTeamId": bigint,
  "id": bigint,
  "playerStatCategory": PlayerStatCategory,
  "playerStatType": PlayerStatType,
  "stat": "abc123"
}
Types
GamePlayerStatAggregate
Description
aggregated selection of "game_player_stat"

Fields
Field Name	Description
aggregate - GamePlayerStatAggregateFields	
nodes - [GamePlayerStat!]!	
Example
{
  "aggregate": GamePlayerStatAggregateFields,
  "nodes": [GamePlayerStat]
}
Types
GamePlayerStatAggregateBoolExp
Fields
Input Field	Description
count - gamePlayerStatAggregateBoolExpCount	
Example
{"count": gamePlayerStatAggregateBoolExpCount}
Types
GamePlayerStatAggregateFields
Description
aggregate fields of "game_player_stat"

Fields
Field Name	Description
avg - GamePlayerStatAvgFields	
count - Int!	
Arguments
columns - [GamePlayerStatSelectColumn!]
distinct - Boolean
max - GamePlayerStatMaxFields	
min - GamePlayerStatMinFields	
stddev - GamePlayerStatStddevFields	
stddevPop - GamePlayerStatStddevPopFields	
stddevSamp - GamePlayerStatStddevSampFields	
sum - GamePlayerStatSumFields	
varPop - GamePlayerStatVarPopFields	
varSamp - GamePlayerStatVarSampFields	
variance - GamePlayerStatVarianceFields	
Example
{
  "avg": GamePlayerStatAvgFields,
  "count": 987,
  "max": GamePlayerStatMaxFields,
  "min": GamePlayerStatMinFields,
  "stddev": GamePlayerStatStddevFields,
  "stddevPop": GamePlayerStatStddevPopFields,
  "stddevSamp": GamePlayerStatStddevSampFields,
  "sum": GamePlayerStatSumFields,
  "varPop": GamePlayerStatVarPopFields,
  "varSamp": GamePlayerStatVarSampFields,
  "variance": GamePlayerStatVarianceFields
}
Types
GamePlayerStatAggregateOrderBy
Description
order by aggregate values of table "game_player_stat"

Fields
Input Field	Description
avg - GamePlayerStatAvgOrderBy	
count - OrderBy	
max - GamePlayerStatMaxOrderBy	
min - GamePlayerStatMinOrderBy	
stddev - GamePlayerStatStddevOrderBy	
stddevPop - GamePlayerStatStddevPopOrderBy	
stddevSamp - GamePlayerStatStddevSampOrderBy	
sum - GamePlayerStatSumOrderBy	
varPop - GamePlayerStatVarPopOrderBy	
varSamp - GamePlayerStatVarSampOrderBy	
variance - GamePlayerStatVarianceOrderBy	
Example
{
  "avg": GamePlayerStatAvgOrderBy,
  "count": "ASC",
  "max": GamePlayerStatMaxOrderBy,
  "min": GamePlayerStatMinOrderBy,
  "stddev": GamePlayerStatStddevOrderBy,
  "stddevPop": GamePlayerStatStddevPopOrderBy,
  "stddevSamp": GamePlayerStatStddevSampOrderBy,
  "sum": GamePlayerStatSumOrderBy,
  "varPop": GamePlayerStatVarPopOrderBy,
  "varSamp": GamePlayerStatVarSampOrderBy,
  "variance": GamePlayerStatVarianceOrderBy
}
Types
GamePlayerStatAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 987.65, "gameTeamId": 123.45, "id": 123.45}
Types
GamePlayerStatAvgOrderBy
Description
order by avg() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatBoolExp
Description
Boolean expression to filter rows from the table "game_player_stat". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [GamePlayerStatBoolExp!]	
_not - GamePlayerStatBoolExp	
_or - [GamePlayerStatBoolExp!]	
athlete - AthleteBoolExp	
athleteId - BigintComparisonExp	
gameTeam - GameTeamBoolExp	
gameTeamId - BigintComparisonExp	
id - BigintComparisonExp	
playerStatCategory - PlayerStatCategoryBoolExp	
playerStatType - PlayerStatTypeBoolExp	
stat - StringComparisonExp	
Example
{
  "_and": [GamePlayerStatBoolExp],
  "_not": GamePlayerStatBoolExp,
  "_or": [GamePlayerStatBoolExp],
  "athlete": AthleteBoolExp,
  "athleteId": BigintComparisonExp,
  "gameTeam": GameTeamBoolExp,
  "gameTeamId": BigintComparisonExp,
  "id": BigintComparisonExp,
  "playerStatCategory": PlayerStatCategoryBoolExp,
  "playerStatType": PlayerStatTypeBoolExp,
  "stat": StringComparisonExp
}
Types
GamePlayerStatMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
athleteId - bigint	
gameTeamId - bigint	
id - bigint	
stat - String	
Example
{
  "athleteId": bigint,
  "gameTeamId": bigint,
  "id": bigint,
  "stat": "abc123"
}
Types
GamePlayerStatMaxOrderBy
Description
order by max() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
stat - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC", "stat": "ASC"}
Types
GamePlayerStatMinFields
Description
aggregate min on columns

Fields
Field Name	Description
athleteId - bigint	
gameTeamId - bigint	
id - bigint	
stat - String	
Example
{
  "athleteId": bigint,
  "gameTeamId": bigint,
  "id": bigint,
  "stat": "xyz789"
}
Types
GamePlayerStatMinOrderBy
Description
order by min() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
stat - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC", "stat": "ASC"}
Types
GamePlayerStatOrderBy
Description
Ordering options when selecting data from "game_player_stat".

Fields
Input Field	Description
athlete - AthleteOrderBy	
athleteId - OrderBy	
gameTeam - GameTeamOrderBy	
gameTeamId - OrderBy	
id - OrderBy	
playerStatCategory - PlayerStatCategoryOrderBy	
playerStatType - PlayerStatTypeOrderBy	
stat - OrderBy	
Example
{
  "athlete": AthleteOrderBy,
  "athleteId": "ASC",
  "gameTeam": GameTeamOrderBy,
  "gameTeamId": "ASC",
  "id": "ASC",
  "playerStatCategory": PlayerStatCategoryOrderBy,
  "playerStatType": PlayerStatTypeOrderBy,
  "stat": "ASC"
}
Types
GamePlayerStatSelectColumn
Description
select columns of table "game_player_stat"

Values
Enum Value	Description
athleteId

column name
gameTeamId

column name
id

column name
stat

column name
Example
"athleteId"
Types
GamePlayerStatStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 987.65, "gameTeamId": 123.45, "id": 987.65}
Types
GamePlayerStatStddevOrderBy
Description
order by stddev() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 987.65, "gameTeamId": 123.45, "id": 123.45}
Types
GamePlayerStatStddevPopOrderBy
Description
order by stddevPop() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 987.65, "gameTeamId": 123.45, "id": 987.65}
Types
GamePlayerStatStddevSampOrderBy
Description
order by stddevSamp() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
athleteId - bigint	
gameTeamId - bigint	
id - bigint	
Example
{
  "athleteId": bigint,
  "gameTeamId": bigint,
  "id": bigint
}
Types
GamePlayerStatSumOrderBy
Description
order by sum() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 123.45, "gameTeamId": 123.45, "id": 123.45}
Types
GamePlayerStatVarPopOrderBy
Description
order by varPop() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 123.45, "gameTeamId": 123.45, "id": 123.45}
Types
GamePlayerStatVarSampOrderBy
Description
order by varSamp() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GamePlayerStatVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
athleteId - Float	
gameTeamId - Float	
id - Float	
Example
{"athleteId": 123.45, "gameTeamId": 987.65, "id": 123.45}
Types
GamePlayerStatVarianceOrderBy
Description
order by variance() on columns of table "game_player_stat"

Fields
Input Field	Description
athleteId - OrderBy	
gameTeamId - OrderBy	
id - OrderBy	
Example
{"athleteId": "ASC", "gameTeamId": "ASC", "id": "ASC"}
Types
GameStatusComparisonExp
Description
Boolean expression to compare columns of type "game_status". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - game_status	
_gt - game_status	
_gte - game_status	
_in - [game_status!]	
_isNull - Boolean	
_lt - game_status	
_lte - game_status	
_neq - game_status	
_nin - [game_status!]	
Example
{
  "_eq": game_status,
  "_gt": game_status,
  "_gte": game_status,
  "_in": [game_status],
  "_isNull": false,
  "_lt": game_status,
  "_lte": game_status,
  "_neq": game_status,
  "_nin": [game_status]
}
Types
GameTeam
Description
columns and relationships of "game_team"

Fields
Field Name	Description
endElo - Int	
game - game	An object relationship
gameId - Int!	
gamePlayerStats - [GamePlayerStat!]!	An array relationship
Arguments
distinctOn - [GamePlayerStatSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GamePlayerStatOrderBy!]
sort the rows by one or more columns

where - GamePlayerStatBoolExp
filter the rows returned

gamePlayerStatsAggregate - GamePlayerStatAggregate!	An aggregate relationship
Arguments
distinctOn - [GamePlayerStatSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GamePlayerStatOrderBy!]
sort the rows by one or more columns

where - GamePlayerStatBoolExp
filter the rows returned

homeAway - home_away!	
lineScores - [smallint!]	
points - smallint	
startElo - Int	
teamId - Int!	
winProb - numeric	
Example
{
  "endElo": 987,
  "game": game,
  "gameId": 987,
  "gamePlayerStats": [GamePlayerStat],
  "gamePlayerStatsAggregate": GamePlayerStatAggregate,
  "homeAway": home_away,
  "lineScores": [smallint],
  "points": smallint,
  "startElo": 987,
  "teamId": 123,
  "winProb": numeric
}
Types
GameTeamBoolExp
Description
Boolean expression to filter rows from the table "game_team". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [GameTeamBoolExp!]	
_not - GameTeamBoolExp	
_or - [GameTeamBoolExp!]	
endElo - IntComparisonExp	
game - gameBoolExp	
gameId - IntComparisonExp	
gamePlayerStats - GamePlayerStatBoolExp	
gamePlayerStatsAggregate - GamePlayerStatAggregateBoolExp	
homeAway - HomeAwayComparisonExp	
lineScores - SmallintArrayComparisonExp	
points - SmallintComparisonExp	
startElo - IntComparisonExp	
teamId - IntComparisonExp	
winProb - NumericComparisonExp	
Example
{
  "_and": [GameTeamBoolExp],
  "_not": GameTeamBoolExp,
  "_or": [GameTeamBoolExp],
  "endElo": IntComparisonExp,
  "game": gameBoolExp,
  "gameId": IntComparisonExp,
  "gamePlayerStats": GamePlayerStatBoolExp,
  "gamePlayerStatsAggregate": GamePlayerStatAggregateBoolExp,
  "homeAway": HomeAwayComparisonExp,
  "lineScores": SmallintArrayComparisonExp,
  "points": SmallintComparisonExp,
  "startElo": IntComparisonExp,
  "teamId": IntComparisonExp,
  "winProb": NumericComparisonExp
}
Types
GameTeamOrderBy
Description
Ordering options when selecting data from "game_team".

Fields
Input Field	Description
endElo - OrderBy	
game - gameOrderBy	
gameId - OrderBy	
gamePlayerStatsAggregate - GamePlayerStatAggregateOrderBy	
homeAway - OrderBy	
lineScores - OrderBy	
points - OrderBy	
startElo - OrderBy	
teamId - OrderBy	
winProb - OrderBy	
Example
{
  "endElo": "ASC",
  "game": gameOrderBy,
  "gameId": "ASC",
  "gamePlayerStatsAggregate": GamePlayerStatAggregateOrderBy,
  "homeAway": "ASC",
  "lineScores": "ASC",
  "points": "ASC",
  "startElo": "ASC",
  "teamId": "ASC",
  "winProb": "ASC"
}
Types
GameTeamSelectColumn
Description
select columns of table "game_team"

Values
Enum Value	Description
endElo

column name
gameId

column name
homeAway

column name
lineScores

column name
points

column name
startElo

column name
teamId

column name
winProb

column name
Example
"endElo"
Types
GameWeather
Description
columns and relationships of "game_weather"

Fields
Field Name	Description
condition - WeatherCondition	An object relationship
dewpoint - numeric	
gameId - Int!	
humidity - numeric	
precipitation - numeric	
pressure - numeric	
snowfall - numeric	
temperature - numeric	
weatherConditionCode - smallint	
windDirection - numeric	
windGust - numeric	
windSpeed - numeric	
Example
{
  "condition": WeatherCondition,
  "dewpoint": numeric,
  "gameId": 123,
  "humidity": numeric,
  "precipitation": numeric,
  "pressure": numeric,
  "snowfall": numeric,
  "temperature": numeric,
  "weatherConditionCode": smallint,
  "windDirection": numeric,
  "windGust": numeric,
  "windSpeed": numeric
}
Types
GameWeatherBoolExp
Description
Boolean expression to filter rows from the table "game_weather". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [GameWeatherBoolExp!]	
_not - GameWeatherBoolExp	
_or - [GameWeatherBoolExp!]	
condition - WeatherConditionBoolExp	
dewpoint - NumericComparisonExp	
gameId - IntComparisonExp	
humidity - NumericComparisonExp	
precipitation - NumericComparisonExp	
pressure - NumericComparisonExp	
snowfall - NumericComparisonExp	
temperature - NumericComparisonExp	
weatherConditionCode - SmallintComparisonExp	
windDirection - NumericComparisonExp	
windGust - NumericComparisonExp	
windSpeed - NumericComparisonExp	
Example
{
  "_and": [GameWeatherBoolExp],
  "_not": GameWeatherBoolExp,
  "_or": [GameWeatherBoolExp],
  "condition": WeatherConditionBoolExp,
  "dewpoint": NumericComparisonExp,
  "gameId": IntComparisonExp,
  "humidity": NumericComparisonExp,
  "precipitation": NumericComparisonExp,
  "pressure": NumericComparisonExp,
  "snowfall": NumericComparisonExp,
  "temperature": NumericComparisonExp,
  "weatherConditionCode": SmallintComparisonExp,
  "windDirection": NumericComparisonExp,
  "windGust": NumericComparisonExp,
  "windSpeed": NumericComparisonExp
}
Types
GameWeatherOrderBy
Description
Ordering options when selecting data from "game_weather".

Fields
Input Field	Description
condition - WeatherConditionOrderBy	
dewpoint - OrderBy	
gameId - OrderBy	
humidity - OrderBy	
precipitation - OrderBy	
pressure - OrderBy	
snowfall - OrderBy	
temperature - OrderBy	
weatherConditionCode - OrderBy	
windDirection - OrderBy	
windGust - OrderBy	
windSpeed - OrderBy	
Example
{
  "condition": WeatherConditionOrderBy,
  "dewpoint": "ASC",
  "gameId": "ASC",
  "humidity": "ASC",
  "precipitation": "ASC",
  "pressure": "ASC",
  "snowfall": "ASC",
  "temperature": "ASC",
  "weatherConditionCode": "ASC",
  "windDirection": "ASC",
  "windGust": "ASC",
  "windSpeed": "ASC"
}
Types
GameWeatherSelectColumn
Description
select columns of table "game_weather"

Values
Enum Value	Description
dewpoint

column name
gameId

column name
humidity

column name
precipitation

column name
pressure

column name
snowfall

column name
temperature

column name
weatherConditionCode

column name
windDirection

column name
windGust

column name
windSpeed

column name
Example
"dewpoint"
Types
HomeAwayComparisonExp
Description
Boolean expression to compare columns of type "home_away". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - home_away	
_gt - home_away	
_gte - home_away	
_in - [home_away!]	
_isNull - Boolean	
_lt - home_away	
_lte - home_away	
_neq - home_away	
_nin - [home_away!]	
Example
{
  "_eq": home_away,
  "_gt": home_away,
  "_gte": home_away,
  "_in": [home_away],
  "_isNull": false,
  "_lt": home_away,
  "_lte": home_away,
  "_neq": home_away,
  "_nin": [home_away]
}
Types
Hometown
Description
columns and relationships of "hometown"

Fields
Field Name	Description
athletes - [Athlete!]!	An array relationship
Arguments
distinctOn - [AthleteSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteOrderBy!]
sort the rows by one or more columns

where - AthleteBoolExp
filter the rows returned

athletesAggregate - AthleteAggregate!	An aggregate relationship
Arguments
distinctOn - [AthleteSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteOrderBy!]
sort the rows by one or more columns

where - AthleteBoolExp
filter the rows returned

city - String	
country - String	
countyFips - String	
latitude - numeric	
longitude - numeric	
recruits - [Recruit!]!	An array relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

recruitsAggregate - RecruitAggregate!	An aggregate relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

state - String	
Example
{
  "athletes": [Athlete],
  "athletesAggregate": AthleteAggregate,
  "city": "abc123",
  "country": "xyz789",
  "countyFips": "xyz789",
  "latitude": numeric,
  "longitude": numeric,
  "recruits": [Recruit],
  "recruitsAggregate": RecruitAggregate,
  "state": "abc123"
}
Types
HometownAggregate
Description
aggregated selection of "hometown"

Fields
Field Name	Description
aggregate - HometownAggregateFields	
nodes - [Hometown!]!	
Example
{
  "aggregate": HometownAggregateFields,
  "nodes": [Hometown]
}
Types
HometownAggregateFields
Description
aggregate fields of "hometown"

Fields
Field Name	Description
avg - HometownAvgFields	
count - Int!	
Arguments
columns - [HometownSelectColumn!]
distinct - Boolean
max - HometownMaxFields	
min - HometownMinFields	
stddev - HometownStddevFields	
stddevPop - HometownStddevPopFields	
stddevSamp - HometownStddevSampFields	
sum - HometownSumFields	
varPop - HometownVarPopFields	
varSamp - HometownVarSampFields	
variance - HometownVarianceFields	
Example
{
  "avg": HometownAvgFields,
  "count": 987,
  "max": HometownMaxFields,
  "min": HometownMinFields,
  "stddev": HometownStddevFields,
  "stddevPop": HometownStddevPopFields,
  "stddevSamp": HometownStddevSampFields,
  "sum": HometownSumFields,
  "varPop": HometownVarPopFields,
  "varSamp": HometownVarSampFields,
  "variance": HometownVarianceFields
}
Types
HometownAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 987.65, "longitude": 987.65}
Types
HometownBoolExp
Description
Boolean expression to filter rows from the table "hometown". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [HometownBoolExp!]	
_not - HometownBoolExp	
_or - [HometownBoolExp!]	
athletes - AthleteBoolExp	
athletesAggregate - AthleteAggregateBoolExp	
city - StringComparisonExp	
country - StringComparisonExp	
countyFips - StringComparisonExp	
latitude - NumericComparisonExp	
longitude - NumericComparisonExp	
recruits - RecruitBoolExp	
recruitsAggregate - RecruitAggregateBoolExp	
state - StringComparisonExp	
Example
{
  "_and": [HometownBoolExp],
  "_not": HometownBoolExp,
  "_or": [HometownBoolExp],
  "athletes": AthleteBoolExp,
  "athletesAggregate": AthleteAggregateBoolExp,
  "city": StringComparisonExp,
  "country": StringComparisonExp,
  "countyFips": StringComparisonExp,
  "latitude": NumericComparisonExp,
  "longitude": NumericComparisonExp,
  "recruits": RecruitBoolExp,
  "recruitsAggregate": RecruitAggregateBoolExp,
  "state": StringComparisonExp
}
Types
HometownMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
city - String	
country - String	
countyFips - String	
latitude - numeric	
longitude - numeric	
state - String	
Example
{
  "city": "xyz789",
  "country": "abc123",
  "countyFips": "xyz789",
  "latitude": numeric,
  "longitude": numeric,
  "state": "xyz789"
}
Types
HometownMinFields
Description
aggregate min on columns

Fields
Field Name	Description
city - String	
country - String	
countyFips - String	
latitude - numeric	
longitude - numeric	
state - String	
Example
{
  "city": "abc123",
  "country": "abc123",
  "countyFips": "abc123",
  "latitude": numeric,
  "longitude": numeric,
  "state": "xyz789"
}
Types
HometownOrderBy
Description
Ordering options when selecting data from "hometown".

Fields
Input Field	Description
athletesAggregate - AthleteAggregateOrderBy	
city - OrderBy	
country - OrderBy	
countyFips - OrderBy	
latitude - OrderBy	
longitude - OrderBy	
recruitsAggregate - RecruitAggregateOrderBy	
state - OrderBy	
Example
{
  "athletesAggregate": AthleteAggregateOrderBy,
  "city": "ASC",
  "country": "ASC",
  "countyFips": "ASC",
  "latitude": "ASC",
  "longitude": "ASC",
  "recruitsAggregate": RecruitAggregateOrderBy,
  "state": "ASC"
}
Types
HometownSelectColumn
Description
select columns of table "hometown"

Values
Enum Value	Description
city

column name
country

column name
countyFips

column name
latitude

column name
longitude

column name
state

column name
Example
"city"
Types
HometownStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 987.65, "longitude": 123.45}
Types
HometownStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 987.65, "longitude": 987.65}
Types
HometownStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 987.65, "longitude": 123.45}
Types
HometownSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
latitude - numeric	
longitude - numeric	
Example
{
  "latitude": numeric,
  "longitude": numeric
}
Types
HometownVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 123.45, "longitude": 123.45}
Types
HometownVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 123.45, "longitude": 987.65}
Types
HometownVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
latitude - Float	
longitude - Float	
Example
{"latitude": 123.45, "longitude": 123.45}
Types
Int
Example
987
Types
IntComparisonExp
Description
Boolean expression to compare columns of type "Int". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - Int	
_gt - Int	
_gte - Int	
_in - [Int!]	
_isNull - Boolean	
_lt - Int	
_lte - Int	
_neq - Int	
_nin - [Int!]	
Example
{
  "_eq": 987,
  "_gt": 987,
  "_gte": 123,
  "_in": [123],
  "_isNull": true,
  "_lt": 987,
  "_lte": 123,
  "_neq": 123,
  "_nin": [987]
}
Types
LinesProvider
Description
columns and relationships of "lines_provider"

Fields
Field Name	Description
id - Int!	
name - String!	
Example
{"id": 123, "name": "xyz789"}
Types
LinesProviderAggregate
Description
aggregated selection of "lines_provider"

Fields
Field Name	Description
aggregate - LinesProviderAggregateFields	
nodes - [LinesProvider!]!	
Example
{
  "aggregate": LinesProviderAggregateFields,
  "nodes": [LinesProvider]
}
Types
LinesProviderAggregateFields
Description
aggregate fields of "lines_provider"

Fields
Field Name	Description
avg - LinesProviderAvgFields	
count - Int!	
Arguments
columns - [LinesProviderSelectColumn!]
distinct - Boolean
max - LinesProviderMaxFields	
min - LinesProviderMinFields	
stddev - LinesProviderStddevFields	
stddevPop - LinesProviderStddevPopFields	
stddevSamp - LinesProviderStddevSampFields	
sum - LinesProviderSumFields	
varPop - LinesProviderVarPopFields	
varSamp - LinesProviderVarSampFields	
variance - LinesProviderVarianceFields	
Example
{
  "avg": LinesProviderAvgFields,
  "count": 123,
  "max": LinesProviderMaxFields,
  "min": LinesProviderMinFields,
  "stddev": LinesProviderStddevFields,
  "stddevPop": LinesProviderStddevPopFields,
  "stddevSamp": LinesProviderStddevSampFields,
  "sum": LinesProviderSumFields,
  "varPop": LinesProviderVarPopFields,
  "varSamp": LinesProviderVarSampFields,
  "variance": LinesProviderVarianceFields
}
Types
LinesProviderAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
LinesProviderBoolExp
Description
Boolean expression to filter rows from the table "lines_provider". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [LinesProviderBoolExp!]	
_not - LinesProviderBoolExp	
_or - [LinesProviderBoolExp!]	
id - IntComparisonExp	
name - StringComparisonExp	
Example
{
  "_and": [LinesProviderBoolExp],
  "_not": LinesProviderBoolExp,
  "_or": [LinesProviderBoolExp],
  "id": IntComparisonExp,
  "name": StringComparisonExp
}
Types
LinesProviderMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
id - Int	
name - String	
Example
{"id": 123, "name": "xyz789"}
Types
LinesProviderMinFields
Description
aggregate min on columns

Fields
Field Name	Description
id - Int	
name - String	
Example
{"id": 987, "name": "xyz789"}
Types
LinesProviderOrderBy
Description
Ordering options when selecting data from "lines_provider".

Fields
Input Field	Description
id - OrderBy	
name - OrderBy	
Example
{"id": "ASC", "name": "ASC"}
Types
LinesProviderSelectColumn
Description
select columns of table "lines_provider"

Values
Enum Value	Description
id

column name
name

column name
Example
"id"
Types
LinesProviderStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
LinesProviderStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
LinesProviderStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
LinesProviderSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
id - Int	
Example
{"id": 123}
Types
LinesProviderVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
LinesProviderVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
LinesProviderVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
MediaTypeComparisonExp
Description
Boolean expression to compare columns of type "media_type". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - media_type	
_gt - media_type	
_gte - media_type	
_in - [media_type!]	
_isNull - Boolean	
_lt - media_type	
_lte - media_type	
_neq - media_type	
_nin - [media_type!]	
Example
{
  "_eq": media_type,
  "_gt": media_type,
  "_gte": media_type,
  "_in": [media_type],
  "_isNull": false,
  "_lt": media_type,
  "_lte": media_type,
  "_neq": media_type,
  "_nin": [media_type]
}
Types
NumericComparisonExp
Description
Boolean expression to compare columns of type "numeric". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - numeric	
_gt - numeric	
_gte - numeric	
_in - [numeric!]	
_isNull - Boolean	
_lt - numeric	
_lte - numeric	
_neq - numeric	
_nin - [numeric!]	
Example
{
  "_eq": numeric,
  "_gt": numeric,
  "_gte": numeric,
  "_in": [numeric],
  "_isNull": true,
  "_lt": numeric,
  "_lte": numeric,
  "_neq": numeric,
  "_nin": [numeric]
}
Types
OrderBy
Description
column ordering options

Values
Enum Value	Description
ASC

in ascending order, nulls last
ASC_NULLS_FIRST

in ascending order, nulls first
ASC_NULLS_LAST

in ascending order, nulls last
DESC

in descending order, nulls first
DESC_NULLS_FIRST

in descending order, nulls first
DESC_NULLS_LAST

in descending order, nulls last
Example
"ASC"
Types
PlayerAdjustedMetricTypeComparisonExp
Description
Boolean expression to compare columns of type "player_adjusted_metric_type". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - player_adjusted_metric_type	
_gt - player_adjusted_metric_type	
_gte - player_adjusted_metric_type	
_in - [player_adjusted_metric_type!]	
_isNull - Boolean	
_lt - player_adjusted_metric_type	
_lte - player_adjusted_metric_type	
_neq - player_adjusted_metric_type	
_nin - [player_adjusted_metric_type!]	
Example
{
  "_eq": player_adjusted_metric_type,
  "_gt": player_adjusted_metric_type,
  "_gte": player_adjusted_metric_type,
  "_in": [player_adjusted_metric_type],
  "_isNull": true,
  "_lt": player_adjusted_metric_type,
  "_lte": player_adjusted_metric_type,
  "_neq": player_adjusted_metric_type,
  "_nin": [player_adjusted_metric_type]
}
Types
PlayerStatCategory
Description
columns and relationships of "player_stat_category"

Fields
Field Name	Description
gamePlayerStats - [GamePlayerStat!]!	An array relationship
Arguments
distinctOn - [GamePlayerStatSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GamePlayerStatOrderBy!]
sort the rows by one or more columns

where - GamePlayerStatBoolExp
filter the rows returned

gamePlayerStatsAggregate - GamePlayerStatAggregate!	An aggregate relationship
Arguments
distinctOn - [GamePlayerStatSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GamePlayerStatOrderBy!]
sort the rows by one or more columns

where - GamePlayerStatBoolExp
filter the rows returned

name - String!	
Example
{
  "gamePlayerStats": [GamePlayerStat],
  "gamePlayerStatsAggregate": GamePlayerStatAggregate,
  "name": "xyz789"
}
Types
PlayerStatCategoryAggregate
Description
aggregated selection of "player_stat_category"

Fields
Field Name	Description
aggregate - PlayerStatCategoryAggregateFields	
nodes - [PlayerStatCategory!]!	
Example
{
  "aggregate": PlayerStatCategoryAggregateFields,
  "nodes": [PlayerStatCategory]
}
Types
PlayerStatCategoryAggregateFields
Description
aggregate fields of "player_stat_category"

Fields
Field Name	Description
count - Int!	
Arguments
columns - [PlayerStatCategorySelectColumn!]
distinct - Boolean
max - PlayerStatCategoryMaxFields	
min - PlayerStatCategoryMinFields	
Example
{
  "count": 987,
  "max": PlayerStatCategoryMaxFields,
  "min": PlayerStatCategoryMinFields
}
Types
PlayerStatCategoryBoolExp
Description
Boolean expression to filter rows from the table "player_stat_category". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PlayerStatCategoryBoolExp!]	
_not - PlayerStatCategoryBoolExp	
_or - [PlayerStatCategoryBoolExp!]	
gamePlayerStats - GamePlayerStatBoolExp	
gamePlayerStatsAggregate - GamePlayerStatAggregateBoolExp	
name - StringComparisonExp	
Example
{
  "_and": [PlayerStatCategoryBoolExp],
  "_not": PlayerStatCategoryBoolExp,
  "_or": [PlayerStatCategoryBoolExp],
  "gamePlayerStats": GamePlayerStatBoolExp,
  "gamePlayerStatsAggregate": GamePlayerStatAggregateBoolExp,
  "name": StringComparisonExp
}
Types
PlayerStatCategoryMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
name - String	
Example
{"name": "xyz789"}
Types
PlayerStatCategoryMinFields
Description
aggregate min on columns

Fields
Field Name	Description
name - String	
Example
{"name": "abc123"}
Types
PlayerStatCategoryOrderBy
Description
Ordering options when selecting data from "player_stat_category".

Fields
Input Field	Description
gamePlayerStatsAggregate - GamePlayerStatAggregateOrderBy	
name - OrderBy	
Example
{
  "gamePlayerStatsAggregate": GamePlayerStatAggregateOrderBy,
  "name": "ASC"
}
Types
PlayerStatCategorySelectColumn
Description
select columns of table "player_stat_category"

Values
Enum Value	Description
name

column name
Example
"name"
Types
PlayerStatType
Description
columns and relationships of "player_stat_type"

Fields
Field Name	Description
name - String!	
Example
{"name": "xyz789"}
Types
PlayerStatTypeAggregate
Description
aggregated selection of "player_stat_type"

Fields
Field Name	Description
aggregate - PlayerStatTypeAggregateFields	
nodes - [PlayerStatType!]!	
Example
{
  "aggregate": PlayerStatTypeAggregateFields,
  "nodes": [PlayerStatType]
}
Types
PlayerStatTypeAggregateFields
Description
aggregate fields of "player_stat_type"

Fields
Field Name	Description
count - Int!	
Arguments
columns - [PlayerStatTypeSelectColumn!]
distinct - Boolean
max - PlayerStatTypeMaxFields	
min - PlayerStatTypeMinFields	
Example
{
  "count": 987,
  "max": PlayerStatTypeMaxFields,
  "min": PlayerStatTypeMinFields
}
Types
PlayerStatTypeBoolExp
Description
Boolean expression to filter rows from the table "player_stat_type". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PlayerStatTypeBoolExp!]	
_not - PlayerStatTypeBoolExp	
_or - [PlayerStatTypeBoolExp!]	
name - StringComparisonExp	
Example
{
  "_and": [PlayerStatTypeBoolExp],
  "_not": PlayerStatTypeBoolExp,
  "_or": [PlayerStatTypeBoolExp],
  "name": StringComparisonExp
}
Types
PlayerStatTypeMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
name - String	
Example
{"name": "xyz789"}
Types
PlayerStatTypeMinFields
Description
aggregate min on columns

Fields
Field Name	Description
name - String	
Example
{"name": "abc123"}
Types
PlayerStatTypeOrderBy
Description
Ordering options when selecting data from "player_stat_type".

Fields
Input Field	Description
name - OrderBy	
Example
{"name": "ASC"}
Types
PlayerStatTypeSelectColumn
Description
select columns of table "player_stat_type"

Values
Enum Value	Description
name

column name
Example
"name"
Types
Poll
Description
columns and relationships of "poll"

Fields
Field Name	Description
pollType - PollType!	An object relationship
rankings - [PollRank!]!	An array relationship
Arguments
distinctOn - [PollRankSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [PollRankOrderBy!]
sort the rows by one or more columns

where - PollRankBoolExp
filter the rows returned

season - Int!	
seasonType - season_type!	
week - smallint!	
Example
{
  "pollType": PollType,
  "rankings": [PollRank],
  "season": 123,
  "seasonType": season_type,
  "week": smallint
}
Types
PollAggregateOrderBy
Description
order by aggregate values of table "poll"

Fields
Input Field	Description
avg - PollAvgOrderBy	
count - OrderBy	
max - PollMaxOrderBy	
min - PollMinOrderBy	
stddev - PollStddevOrderBy	
stddevPop - PollStddevPopOrderBy	
stddevSamp - PollStddevSampOrderBy	
sum - PollSumOrderBy	
varPop - PollVarPopOrderBy	
varSamp - PollVarSampOrderBy	
variance - PollVarianceOrderBy	
Example
{
  "avg": PollAvgOrderBy,
  "count": "ASC",
  "max": PollMaxOrderBy,
  "min": PollMinOrderBy,
  "stddev": PollStddevOrderBy,
  "stddevPop": PollStddevPopOrderBy,
  "stddevSamp": PollStddevSampOrderBy,
  "sum": PollSumOrderBy,
  "varPop": PollVarPopOrderBy,
  "varSamp": PollVarSampOrderBy,
  "variance": PollVarianceOrderBy
}
Types
PollAvgOrderBy
Description
order by avg() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollBoolExp
Description
Boolean expression to filter rows from the table "poll". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PollBoolExp!]	
_not - PollBoolExp	
_or - [PollBoolExp!]	
pollType - PollTypeBoolExp	
rankings - PollRankBoolExp	
season - IntComparisonExp	
seasonType - SeasonTypeComparisonExp	
week - SmallintComparisonExp	
Example
{
  "_and": [PollBoolExp],
  "_not": PollBoolExp,
  "_or": [PollBoolExp],
  "pollType": PollTypeBoolExp,
  "rankings": PollRankBoolExp,
  "season": IntComparisonExp,
  "seasonType": SeasonTypeComparisonExp,
  "week": SmallintComparisonExp
}
Types
PollMaxOrderBy
Description
order by max() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
seasonType - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "seasonType": "ASC", "week": "ASC"}
Types
PollMinOrderBy
Description
order by min() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
seasonType - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "seasonType": "ASC", "week": "ASC"}
Types
PollOrderBy
Description
Ordering options when selecting data from "poll".

Fields
Input Field	Description
pollType - PollTypeOrderBy	
rankingsAggregate - PollRankAggregateOrderBy	
season - OrderBy	
seasonType - OrderBy	
week - OrderBy	
Example
{
  "pollType": PollTypeOrderBy,
  "rankingsAggregate": PollRankAggregateOrderBy,
  "season": "ASC",
  "seasonType": "ASC",
  "week": "ASC"
}
Types
PollRank
Description
columns and relationships of "poll_rank"

Fields
Field Name	Description
firstPlaceVotes - smallint	
points - Int	
poll - Poll!	An object relationship
rank - smallint	
team - currentTeams	An object relationship
Example
{
  "firstPlaceVotes": smallint,
  "points": 987,
  "poll": Poll,
  "rank": smallint,
  "team": currentTeams
}
Types
PollRankAggregateOrderBy
Description
order by aggregate values of table "poll_rank"

Fields
Input Field	Description
avg - PollRankAvgOrderBy	
count - OrderBy	
max - PollRankMaxOrderBy	
min - PollRankMinOrderBy	
stddev - PollRankStddevOrderBy	
stddevPop - PollRankStddevPopOrderBy	
stddevSamp - PollRankStddevSampOrderBy	
sum - PollRankSumOrderBy	
varPop - PollRankVarPopOrderBy	
varSamp - PollRankVarSampOrderBy	
variance - PollRankVarianceOrderBy	
Example
{
  "avg": PollRankAvgOrderBy,
  "count": "ASC",
  "max": PollRankMaxOrderBy,
  "min": PollRankMinOrderBy,
  "stddev": PollRankStddevOrderBy,
  "stddevPop": PollRankStddevPopOrderBy,
  "stddevSamp": PollRankStddevSampOrderBy,
  "sum": PollRankSumOrderBy,
  "varPop": PollRankVarPopOrderBy,
  "varSamp": PollRankVarSampOrderBy,
  "variance": PollRankVarianceOrderBy
}
Types
PollRankAvgOrderBy
Description
order by avg() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankBoolExp
Description
Boolean expression to filter rows from the table "poll_rank". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PollRankBoolExp!]	
_not - PollRankBoolExp	
_or - [PollRankBoolExp!]	
firstPlaceVotes - SmallintComparisonExp	
points - IntComparisonExp	
poll - PollBoolExp	
rank - SmallintComparisonExp	
team - currentTeamsBoolExp	
Example
{
  "_and": [PollRankBoolExp],
  "_not": PollRankBoolExp,
  "_or": [PollRankBoolExp],
  "firstPlaceVotes": SmallintComparisonExp,
  "points": IntComparisonExp,
  "poll": PollBoolExp,
  "rank": SmallintComparisonExp,
  "team": currentTeamsBoolExp
}
Types
PollRankMaxOrderBy
Description
order by max() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankMinOrderBy
Description
order by min() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankOrderBy
Description
Ordering options when selecting data from "poll_rank".

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
poll - PollOrderBy	
rank - OrderBy	
team - currentTeamsOrderBy	
Example
{
  "firstPlaceVotes": "ASC",
  "points": "ASC",
  "poll": PollOrderBy,
  "rank": "ASC",
  "team": currentTeamsOrderBy
}
Types
PollRankSelectColumn
Description
select columns of table "poll_rank"

Values
Enum Value	Description
firstPlaceVotes

column name
points

column name
rank

column name
Example
"firstPlaceVotes"
Types
PollRankStddevOrderBy
Description
order by stddev() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankStddevPopOrderBy
Description
order by stddevPop() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankStddevSampOrderBy
Description
order by stddevSamp() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankSumOrderBy
Description
order by sum() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankVarPopOrderBy
Description
order by varPop() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankVarSampOrderBy
Description
order by varSamp() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollRankVarianceOrderBy
Description
order by variance() on columns of table "poll_rank"

Fields
Input Field	Description
firstPlaceVotes - OrderBy	
points - OrderBy	
rank - OrderBy	
Example
{"firstPlaceVotes": "ASC", "points": "ASC", "rank": "ASC"}
Types
PollSelectColumn
Description
select columns of table "poll"

Values
Enum Value	Description
season

column name
seasonType

column name
week

column name
Example
"season"
Types
PollStddevOrderBy
Description
order by stddev() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollStddevPopOrderBy
Description
order by stddevPop() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollStddevSampOrderBy
Description
order by stddevSamp() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollSumOrderBy
Description
order by sum() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollType
Description
columns and relationships of "poll_type"

Fields
Field Name	Description
abbreviation - String	
id - Int!	
name - String!	
polls - [Poll!]!	An array relationship
Arguments
distinctOn - [PollSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [PollOrderBy!]
sort the rows by one or more columns

where - PollBoolExp
filter the rows returned

shortName - String!	
Example
{
  "abbreviation": "xyz789",
  "id": 987,
  "name": "xyz789",
  "polls": [Poll],
  "shortName": "abc123"
}
Types
PollTypeBoolExp
Description
Boolean expression to filter rows from the table "poll_type". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PollTypeBoolExp!]	
_not - PollTypeBoolExp	
_or - [PollTypeBoolExp!]	
abbreviation - StringComparisonExp	
id - IntComparisonExp	
name - StringComparisonExp	
polls - PollBoolExp	
shortName - StringComparisonExp	
Example
{
  "_and": [PollTypeBoolExp],
  "_not": PollTypeBoolExp,
  "_or": [PollTypeBoolExp],
  "abbreviation": StringComparisonExp,
  "id": IntComparisonExp,
  "name": StringComparisonExp,
  "polls": PollBoolExp,
  "shortName": StringComparisonExp
}
Types
PollTypeOrderBy
Description
Ordering options when selecting data from "poll_type".

Fields
Input Field	Description
abbreviation - OrderBy	
id - OrderBy	
name - OrderBy	
pollsAggregate - PollAggregateOrderBy	
shortName - OrderBy	
Example
{
  "abbreviation": "ASC",
  "id": "ASC",
  "name": "ASC",
  "pollsAggregate": PollAggregateOrderBy,
  "shortName": "ASC"
}
Types
PollTypeSelectColumn
Description
select columns of table "poll_type"

Values
Enum Value	Description
abbreviation

column name
id

column name
name

column name
shortName

column name
Example
"abbreviation"
Types
PollVarPopOrderBy
Description
order by varPop() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollVarSampOrderBy
Description
order by varSamp() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
PollVarianceOrderBy
Description
order by variance() on columns of table "poll"

Fields
Input Field	Description
season - OrderBy	
week - OrderBy	
Example
{"season": "ASC", "week": "ASC"}
Types
Position
Description
columns and relationships of "position"

Fields
Field Name	Description
abbreviation - String!	
athletes - [Athlete!]!	An array relationship
Arguments
distinctOn - [AthleteSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteOrderBy!]
sort the rows by one or more columns

where - AthleteBoolExp
filter the rows returned

athletesAggregate - AthleteAggregate!	An aggregate relationship
Arguments
distinctOn - [AthleteSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [AthleteOrderBy!]
sort the rows by one or more columns

where - AthleteBoolExp
filter the rows returned

displayName - String!	
id - smallint!	
name - String!	
Example
{
  "abbreviation": "xyz789",
  "athletes": [Athlete],
  "athletesAggregate": AthleteAggregate,
  "displayName": "xyz789",
  "id": smallint,
  "name": "xyz789"
}
Types
PositionBoolExp
Description
Boolean expression to filter rows from the table "position". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [PositionBoolExp!]	
_not - PositionBoolExp	
_or - [PositionBoolExp!]	
abbreviation - StringComparisonExp	
athletes - AthleteBoolExp	
athletesAggregate - AthleteAggregateBoolExp	
displayName - StringComparisonExp	
id - SmallintComparisonExp	
name - StringComparisonExp	
Example
{
  "_and": [PositionBoolExp],
  "_not": PositionBoolExp,
  "_or": [PositionBoolExp],
  "abbreviation": StringComparisonExp,
  "athletes": AthleteBoolExp,
  "athletesAggregate": AthleteAggregateBoolExp,
  "displayName": StringComparisonExp,
  "id": SmallintComparisonExp,
  "name": StringComparisonExp
}
Types
PositionOrderBy
Description
Ordering options when selecting data from "position".

Fields
Input Field	Description
abbreviation - OrderBy	
athletesAggregate - AthleteAggregateOrderBy	
displayName - OrderBy	
id - OrderBy	
name - OrderBy	
Example
{
  "abbreviation": "ASC",
  "athletesAggregate": AthleteAggregateOrderBy,
  "displayName": "ASC",
  "id": "ASC",
  "name": "ASC"
}
Types
PositionSelectColumn
Description
select columns of table "position"

Values
Enum Value	Description
abbreviation

column name
displayName

column name
id

column name
name

column name
Example
"abbreviation"
Types
Recruit
Description
columns and relationships of "recruit"

Fields
Field Name	Description
athlete - Athlete	An object relationship
college - currentTeams	An object relationship
height - Float	
hometown - Hometown	An object relationship
id - bigint!	
name - String!	
overallRank - smallint	
position - RecruitPosition	An object relationship
positionRank - smallint	
ranking - smallint	
rating - Float!	
recruitSchool - RecruitSchool	An object relationship
recruitType - recruit_type!	
stars - smallint!	
weight - smallint	
year - smallint!	
Example
{
  "athlete": Athlete,
  "college": currentTeams,
  "height": 123.45,
  "hometown": Hometown,
  "id": bigint,
  "name": "xyz789",
  "overallRank": smallint,
  "position": RecruitPosition,
  "positionRank": smallint,
  "ranking": smallint,
  "rating": 123.45,
  "recruitSchool": RecruitSchool,
  "recruitType": recruit_type,
  "stars": smallint,
  "weight": smallint,
  "year": smallint
}
Types
RecruitAggregate
Description
aggregated selection of "recruit"

Fields
Field Name	Description
aggregate - RecruitAggregateFields	
nodes - [Recruit!]!	
Example
{
  "aggregate": RecruitAggregateFields,
  "nodes": [Recruit]
}
Types
RecruitAggregateBoolExp
Fields
Input Field	Description
count - recruitAggregateBoolExpCount	
Example
{"count": recruitAggregateBoolExpCount}
Types
RecruitAggregateFields
Description
aggregate fields of "recruit"

Fields
Field Name	Description
avg - RecruitAvgFields	
count - Int!	
Arguments
columns - [RecruitSelectColumn!]
distinct - Boolean
max - RecruitMaxFields	
min - RecruitMinFields	
stddev - RecruitStddevFields	
stddevPop - RecruitStddevPopFields	
stddevSamp - RecruitStddevSampFields	
sum - RecruitSumFields	
varPop - RecruitVarPopFields	
varSamp - RecruitVarSampFields	
variance - RecruitVarianceFields	
Example
{
  "avg": RecruitAvgFields,
  "count": 987,
  "max": RecruitMaxFields,
  "min": RecruitMinFields,
  "stddev": RecruitStddevFields,
  "stddevPop": RecruitStddevPopFields,
  "stddevSamp": RecruitStddevSampFields,
  "sum": RecruitSumFields,
  "varPop": RecruitVarPopFields,
  "varSamp": RecruitVarSampFields,
  "variance": RecruitVarianceFields
}
Types
RecruitAggregateOrderBy
Description
order by aggregate values of table "recruit"

Fields
Input Field	Description
avg - RecruitAvgOrderBy	
count - OrderBy	
max - RecruitMaxOrderBy	
min - RecruitMinOrderBy	
stddev - RecruitStddevOrderBy	
stddevPop - RecruitStddevPopOrderBy	
stddevSamp - RecruitStddevSampOrderBy	
sum - RecruitSumOrderBy	
varPop - RecruitVarPopOrderBy	
varSamp - RecruitVarSampOrderBy	
variance - RecruitVarianceOrderBy	
Example
{
  "avg": RecruitAvgOrderBy,
  "count": "ASC",
  "max": RecruitMaxOrderBy,
  "min": RecruitMinOrderBy,
  "stddev": RecruitStddevOrderBy,
  "stddevPop": RecruitStddevPopOrderBy,
  "stddevSamp": RecruitStddevSampOrderBy,
  "sum": RecruitSumOrderBy,
  "varPop": RecruitVarPopOrderBy,
  "varSamp": RecruitVarSampOrderBy,
  "variance": RecruitVarianceOrderBy
}
Types
RecruitAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 123.45,
  "id": 987.65,
  "overallRank": 987.65,
  "positionRank": 123.45,
  "ranking": 987.65,
  "rating": 987.65,
  "stars": 123.45,
  "weight": 987.65,
  "year": 123.45
}
Types
RecruitAvgOrderBy
Description
order by avg() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitBoolExp
Description
Boolean expression to filter rows from the table "recruit". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [RecruitBoolExp!]	
_not - RecruitBoolExp	
_or - [RecruitBoolExp!]	
athlete - AthleteBoolExp	
college - currentTeamsBoolExp	
height - FloatComparisonExp	
hometown - HometownBoolExp	
id - BigintComparisonExp	
name - StringComparisonExp	
overallRank - SmallintComparisonExp	
position - RecruitPositionBoolExp	
positionRank - SmallintComparisonExp	
ranking - SmallintComparisonExp	
rating - FloatComparisonExp	
recruitSchool - RecruitSchoolBoolExp	
recruitType - RecruitTypeComparisonExp	
stars - SmallintComparisonExp	
weight - SmallintComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [RecruitBoolExp],
  "_not": RecruitBoolExp,
  "_or": [RecruitBoolExp],
  "athlete": AthleteBoolExp,
  "college": currentTeamsBoolExp,
  "height": FloatComparisonExp,
  "hometown": HometownBoolExp,
  "id": BigintComparisonExp,
  "name": StringComparisonExp,
  "overallRank": SmallintComparisonExp,
  "position": RecruitPositionBoolExp,
  "positionRank": SmallintComparisonExp,
  "ranking": SmallintComparisonExp,
  "rating": FloatComparisonExp,
  "recruitSchool": RecruitSchoolBoolExp,
  "recruitType": RecruitTypeComparisonExp,
  "stars": SmallintComparisonExp,
  "weight": SmallintComparisonExp,
  "year": SmallintComparisonExp
}
Types
RecruitMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
height - Float	
id - bigint	
name - String	
overallRank - smallint	
positionRank - smallint	
ranking - smallint	
rating - Float	
recruitType - recruit_type	
stars - smallint	
weight - smallint	
year - smallint	
Example
{
  "height": 123.45,
  "id": bigint,
  "name": "xyz789",
  "overallRank": smallint,
  "positionRank": smallint,
  "ranking": smallint,
  "rating": 123.45,
  "recruitType": recruit_type,
  "stars": smallint,
  "weight": smallint,
  "year": smallint
}
Types
RecruitMaxOrderBy
Description
order by max() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
name - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
recruitType - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "name": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "recruitType": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitMinFields
Description
aggregate min on columns

Fields
Field Name	Description
height - Float	
id - bigint	
name - String	
overallRank - smallint	
positionRank - smallint	
ranking - smallint	
rating - Float	
recruitType - recruit_type	
stars - smallint	
weight - smallint	
year - smallint	
Example
{
  "height": 123.45,
  "id": bigint,
  "name": "abc123",
  "overallRank": smallint,
  "positionRank": smallint,
  "ranking": smallint,
  "rating": 123.45,
  "recruitType": recruit_type,
  "stars": smallint,
  "weight": smallint,
  "year": smallint
}
Types
RecruitMinOrderBy
Description
order by min() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
name - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
recruitType - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "name": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "recruitType": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitOrderBy
Description
Ordering options when selecting data from "recruit".

Fields
Input Field	Description
athlete - AthleteOrderBy	
college - currentTeamsOrderBy	
height - OrderBy	
hometown - HometownOrderBy	
id - OrderBy	
name - OrderBy	
overallRank - OrderBy	
position - RecruitPositionOrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
recruitSchool - RecruitSchoolOrderBy	
recruitType - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "athlete": AthleteOrderBy,
  "college": currentTeamsOrderBy,
  "height": "ASC",
  "hometown": HometownOrderBy,
  "id": "ASC",
  "name": "ASC",
  "overallRank": "ASC",
  "position": RecruitPositionOrderBy,
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "recruitSchool": RecruitSchoolOrderBy,
  "recruitType": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitPosition
Description
columns and relationships of "recruit_position"

Fields
Field Name	Description
id - smallint!	
position - String!	
positionGroup - String	
Example
{
  "id": smallint,
  "position": "abc123",
  "positionGroup": "xyz789"
}
Types
RecruitPositionAggregate
Description
aggregated selection of "recruit_position"

Fields
Field Name	Description
aggregate - RecruitPositionAggregateFields	
nodes - [RecruitPosition!]!	
Example
{
  "aggregate": RecruitPositionAggregateFields,
  "nodes": [RecruitPosition]
}
Types
RecruitPositionAggregateFields
Description
aggregate fields of "recruit_position"

Fields
Field Name	Description
avg - RecruitPositionAvgFields	
count - Int!	
Arguments
columns - [RecruitPositionSelectColumn!]
distinct - Boolean
max - RecruitPositionMaxFields	
min - RecruitPositionMinFields	
stddev - RecruitPositionStddevFields	
stddevPop - RecruitPositionStddevPopFields	
stddevSamp - RecruitPositionStddevSampFields	
sum - RecruitPositionSumFields	
varPop - RecruitPositionVarPopFields	
varSamp - RecruitPositionVarSampFields	
variance - RecruitPositionVarianceFields	
Example
{
  "avg": RecruitPositionAvgFields,
  "count": 987,
  "max": RecruitPositionMaxFields,
  "min": RecruitPositionMinFields,
  "stddev": RecruitPositionStddevFields,
  "stddevPop": RecruitPositionStddevPopFields,
  "stddevSamp": RecruitPositionStddevSampFields,
  "sum": RecruitPositionSumFields,
  "varPop": RecruitPositionVarPopFields,
  "varSamp": RecruitPositionVarSampFields,
  "variance": RecruitPositionVarianceFields
}
Types
RecruitPositionAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitPositionBoolExp
Description
Boolean expression to filter rows from the table "recruit_position". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [RecruitPositionBoolExp!]	
_not - RecruitPositionBoolExp	
_or - [RecruitPositionBoolExp!]	
id - SmallintComparisonExp	
position - StringComparisonExp	
positionGroup - StringComparisonExp	
Example
{
  "_and": [RecruitPositionBoolExp],
  "_not": RecruitPositionBoolExp,
  "_or": [RecruitPositionBoolExp],
  "id": SmallintComparisonExp,
  "position": StringComparisonExp,
  "positionGroup": StringComparisonExp
}
Types
RecruitPositionMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
id - smallint	
position - String	
positionGroup - String	
Example
{
  "id": smallint,
  "position": "abc123",
  "positionGroup": "abc123"
}
Types
RecruitPositionMinFields
Description
aggregate min on columns

Fields
Field Name	Description
id - smallint	
position - String	
positionGroup - String	
Example
{
  "id": smallint,
  "position": "abc123",
  "positionGroup": "xyz789"
}
Types
RecruitPositionOrderBy
Description
Ordering options when selecting data from "recruit_position".

Fields
Input Field	Description
id - OrderBy	
position - OrderBy	
positionGroup - OrderBy	
Example
{"id": "ASC", "position": "ASC", "positionGroup": "ASC"}
Types
RecruitPositionSelectColumn
Description
select columns of table "recruit_position"

Values
Enum Value	Description
id

column name
position

column name
positionGroup

column name
Example
"id"
Types
RecruitPositionStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitPositionStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitPositionStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitPositionSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
id - smallint	
Example
{"id": smallint}
Types
RecruitPositionVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitPositionVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitPositionVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitSchool
Description
columns and relationships of "recruit_school"

Fields
Field Name	Description
id - Int!	
name - String!	
recruits - [Recruit!]!	An array relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

recruitsAggregate - RecruitAggregate!	An aggregate relationship
Arguments
distinctOn - [RecruitSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [RecruitOrderBy!]
sort the rows by one or more columns

where - RecruitBoolExp
filter the rows returned

Example
{
  "id": 123,
  "name": "abc123",
  "recruits": [Recruit],
  "recruitsAggregate": RecruitAggregate
}
Types
RecruitSchoolAggregate
Description
aggregated selection of "recruit_school"

Fields
Field Name	Description
aggregate - RecruitSchoolAggregateFields	
nodes - [RecruitSchool!]!	
Example
{
  "aggregate": RecruitSchoolAggregateFields,
  "nodes": [RecruitSchool]
}
Types
RecruitSchoolAggregateFields
Description
aggregate fields of "recruit_school"

Fields
Field Name	Description
avg - RecruitSchoolAvgFields	
count - Int!	
Arguments
columns - [RecruitSchoolSelectColumn!]
distinct - Boolean
max - RecruitSchoolMaxFields	
min - RecruitSchoolMinFields	
stddev - RecruitSchoolStddevFields	
stddevPop - RecruitSchoolStddevPopFields	
stddevSamp - RecruitSchoolStddevSampFields	
sum - RecruitSchoolSumFields	
varPop - RecruitSchoolVarPopFields	
varSamp - RecruitSchoolVarSampFields	
variance - RecruitSchoolVarianceFields	
Example
{
  "avg": RecruitSchoolAvgFields,
  "count": 987,
  "max": RecruitSchoolMaxFields,
  "min": RecruitSchoolMinFields,
  "stddev": RecruitSchoolStddevFields,
  "stddevPop": RecruitSchoolStddevPopFields,
  "stddevSamp": RecruitSchoolStddevSampFields,
  "sum": RecruitSchoolSumFields,
  "varPop": RecruitSchoolVarPopFields,
  "varSamp": RecruitSchoolVarSampFields,
  "variance": RecruitSchoolVarianceFields
}
Types
RecruitSchoolAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitSchoolBoolExp
Description
Boolean expression to filter rows from the table "recruit_school". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [RecruitSchoolBoolExp!]	
_not - RecruitSchoolBoolExp	
_or - [RecruitSchoolBoolExp!]	
id - IntComparisonExp	
name - StringComparisonExp	
recruits - RecruitBoolExp	
recruitsAggregate - RecruitAggregateBoolExp	
Example
{
  "_and": [RecruitSchoolBoolExp],
  "_not": RecruitSchoolBoolExp,
  "_or": [RecruitSchoolBoolExp],
  "id": IntComparisonExp,
  "name": StringComparisonExp,
  "recruits": RecruitBoolExp,
  "recruitsAggregate": RecruitAggregateBoolExp
}
Types
RecruitSchoolMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
id - Int	
name - String	
Example
{"id": 123, "name": "xyz789"}
Types
RecruitSchoolMinFields
Description
aggregate min on columns

Fields
Field Name	Description
id - Int	
name - String	
Example
{"id": 123, "name": "xyz789"}
Types
RecruitSchoolOrderBy
Description
Ordering options when selecting data from "recruit_school".

Fields
Input Field	Description
id - OrderBy	
name - OrderBy	
recruitsAggregate - RecruitAggregateOrderBy	
Example
{
  "id": "ASC",
  "name": "ASC",
  "recruitsAggregate": RecruitAggregateOrderBy
}
Types
RecruitSchoolSelectColumn
Description
select columns of table "recruit_school"

Values
Enum Value	Description
id

column name
name

column name
Example
"id"
Types
RecruitSchoolStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitSchoolStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitSchoolStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 987.65}
Types
RecruitSchoolSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
id - Int	
Example
{"id": 987}
Types
RecruitSchoolVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitSchoolVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitSchoolVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
id - Float	
Example
{"id": 123.45}
Types
RecruitSelectColumn
Description
select columns of table "recruit"

Values
Enum Value	Description
height

column name
id

column name
name

column name
overallRank

column name
positionRank

column name
ranking

column name
rating

column name
recruitType

column name
stars

column name
weight

column name
year

column name
Example
"height"
Types
RecruitStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 987.65,
  "id": 987.65,
  "overallRank": 123.45,
  "positionRank": 987.65,
  "ranking": 123.45,
  "rating": 987.65,
  "stars": 123.45,
  "weight": 123.45,
  "year": 987.65
}
Types
RecruitStddevOrderBy
Description
order by stddev() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 123.45,
  "id": 123.45,
  "overallRank": 987.65,
  "positionRank": 123.45,
  "ranking": 123.45,
  "rating": 987.65,
  "stars": 987.65,
  "weight": 987.65,
  "year": 123.45
}
Types
RecruitStddevPopOrderBy
Description
order by stddevPop() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 123.45,
  "id": 987.65,
  "overallRank": 123.45,
  "positionRank": 123.45,
  "ranking": 123.45,
  "rating": 123.45,
  "stars": 987.65,
  "weight": 123.45,
  "year": 123.45
}
Types
RecruitStddevSampOrderBy
Description
order by stddevSamp() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
height - Float	
id - bigint	
overallRank - smallint	
positionRank - smallint	
ranking - smallint	
rating - Float	
stars - smallint	
weight - smallint	
year - smallint	
Example
{
  "height": 123.45,
  "id": bigint,
  "overallRank": smallint,
  "positionRank": smallint,
  "ranking": smallint,
  "rating": 987.65,
  "stars": smallint,
  "weight": smallint,
  "year": smallint
}
Types
RecruitSumOrderBy
Description
order by sum() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitTypeComparisonExp
Description
Boolean expression to compare columns of type "recruit_type". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - recruit_type	
_gt - recruit_type	
_gte - recruit_type	
_in - [recruit_type!]	
_isNull - Boolean	
_lt - recruit_type	
_lte - recruit_type	
_neq - recruit_type	
_nin - [recruit_type!]	
Example
{
  "_eq": recruit_type,
  "_gt": recruit_type,
  "_gte": recruit_type,
  "_in": [recruit_type],
  "_isNull": false,
  "_lt": recruit_type,
  "_lte": recruit_type,
  "_neq": recruit_type,
  "_nin": [recruit_type]
}
Types
RecruitVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 987.65,
  "id": 987.65,
  "overallRank": 987.65,
  "positionRank": 987.65,
  "ranking": 987.65,
  "rating": 123.45,
  "stars": 123.45,
  "weight": 123.45,
  "year": 987.65
}
Types
RecruitVarPopOrderBy
Description
order by varPop() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 123.45,
  "id": 123.45,
  "overallRank": 987.65,
  "positionRank": 123.45,
  "ranking": 123.45,
  "rating": 123.45,
  "stars": 123.45,
  "weight": 123.45,
  "year": 123.45
}
Types
RecruitVarSampOrderBy
Description
order by varSamp() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
height - Float	
id - Float	
overallRank - Float	
positionRank - Float	
ranking - Float	
rating - Float	
stars - Float	
weight - Float	
year - Float	
Example
{
  "height": 123.45,
  "id": 123.45,
  "overallRank": 987.65,
  "positionRank": 987.65,
  "ranking": 123.45,
  "rating": 987.65,
  "stars": 987.65,
  "weight": 123.45,
  "year": 123.45
}
Types
RecruitVarianceOrderBy
Description
order by variance() on columns of table "recruit"

Fields
Input Field	Description
height - OrderBy	
id - OrderBy	
overallRank - OrderBy	
positionRank - OrderBy	
ranking - OrderBy	
rating - OrderBy	
stars - OrderBy	
weight - OrderBy	
year - OrderBy	
Example
{
  "height": "ASC",
  "id": "ASC",
  "overallRank": "ASC",
  "positionRank": "ASC",
  "ranking": "ASC",
  "rating": "ASC",
  "stars": "ASC",
  "weight": "ASC",
  "year": "ASC"
}
Types
RecruitingTeam
Description
columns and relationships of "recruiting_team"

Fields
Field Name	Description
id - Int!	
points - numeric!	
rank - smallint!	
team - currentTeams	An object relationship
year - smallint!	
Example
{
  "id": 123,
  "points": numeric,
  "rank": smallint,
  "team": currentTeams,
  "year": smallint
}
Types
RecruitingTeamAggregate
Description
aggregated selection of "recruiting_team"

Fields
Field Name	Description
aggregate - RecruitingTeamAggregateFields	
nodes - [RecruitingTeam!]!	
Example
{
  "aggregate": RecruitingTeamAggregateFields,
  "nodes": [RecruitingTeam]
}
Types
RecruitingTeamAggregateFields
Description
aggregate fields of "recruiting_team"

Fields
Field Name	Description
avg - RecruitingTeamAvgFields	
count - Int!	
Arguments
columns - [RecruitingTeamSelectColumn!]
distinct - Boolean
max - RecruitingTeamMaxFields	
min - RecruitingTeamMinFields	
stddev - RecruitingTeamStddevFields	
stddevPop - RecruitingTeamStddevPopFields	
stddevSamp - RecruitingTeamStddevSampFields	
sum - RecruitingTeamSumFields	
varPop - RecruitingTeamVarPopFields	
varSamp - RecruitingTeamVarSampFields	
variance - RecruitingTeamVarianceFields	
Example
{
  "avg": RecruitingTeamAvgFields,
  "count": 123,
  "max": RecruitingTeamMaxFields,
  "min": RecruitingTeamMinFields,
  "stddev": RecruitingTeamStddevFields,
  "stddevPop": RecruitingTeamStddevPopFields,
  "stddevSamp": RecruitingTeamStddevSampFields,
  "sum": RecruitingTeamSumFields,
  "varPop": RecruitingTeamVarPopFields,
  "varSamp": RecruitingTeamVarSampFields,
  "variance": RecruitingTeamVarianceFields
}
Types
RecruitingTeamAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 987.65, "points": 123.45, "rank": 123.45, "year": 123.45}
Types
RecruitingTeamBoolExp
Description
Boolean expression to filter rows from the table "recruiting_team". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [RecruitingTeamBoolExp!]	
_not - RecruitingTeamBoolExp	
_or - [RecruitingTeamBoolExp!]	
id - IntComparisonExp	
points - NumericComparisonExp	
rank - SmallintComparisonExp	
team - currentTeamsBoolExp	
year - SmallintComparisonExp	
Example
{
  "_and": [RecruitingTeamBoolExp],
  "_not": RecruitingTeamBoolExp,
  "_or": [RecruitingTeamBoolExp],
  "id": IntComparisonExp,
  "points": NumericComparisonExp,
  "rank": SmallintComparisonExp,
  "team": currentTeamsBoolExp,
  "year": SmallintComparisonExp
}
Types
RecruitingTeamMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
id - Int	
points - numeric	
rank - smallint	
year - smallint	
Example
{
  "id": 123,
  "points": numeric,
  "rank": smallint,
  "year": smallint
}
Types
RecruitingTeamMinFields
Description
aggregate min on columns

Fields
Field Name	Description
id - Int	
points - numeric	
rank - smallint	
year - smallint	
Example
{
  "id": 123,
  "points": numeric,
  "rank": smallint,
  "year": smallint
}
Types
RecruitingTeamOrderBy
Description
Ordering options when selecting data from "recruiting_team".

Fields
Input Field	Description
id - OrderBy	
points - OrderBy	
rank - OrderBy	
team - currentTeamsOrderBy	
year - OrderBy	
Example
{
  "id": "ASC",
  "points": "ASC",
  "rank": "ASC",
  "team": currentTeamsOrderBy,
  "year": "ASC"
}
Types
RecruitingTeamSelectColumn
Description
select columns of table "recruiting_team"

Values
Enum Value	Description
id

column name
points

column name
rank

column name
year

column name
Example
"id"
Types
RecruitingTeamStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 123.45, "points": 123.45, "rank": 987.65, "year": 987.65}
Types
RecruitingTeamStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 987.65, "points": 123.45, "rank": 987.65, "year": 987.65}
Types
RecruitingTeamStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 123.45, "points": 987.65, "rank": 987.65, "year": 987.65}
Types
RecruitingTeamSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
id - Int	
points - numeric	
rank - smallint	
year - smallint	
Example
{
  "id": 123,
  "points": numeric,
  "rank": smallint,
  "year": smallint
}
Types
RecruitingTeamVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 987.65, "points": 987.65, "rank": 123.45, "year": 123.45}
Types
RecruitingTeamVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 987.65, "points": 123.45, "rank": 123.45, "year": 987.65}
Types
RecruitingTeamVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
id - Float	
points - Float	
rank - Float	
year - Float	
Example
{"id": 123.45, "points": 123.45, "rank": 123.45, "year": 123.45}
Types
Scoreboard
Description
columns and relationships of "scoreboard"

Fields
Field Name	Description
awayClassification - division	
awayConference - String	
awayConferenceAbbreviation - String	
awayId - Int	
awayLineScores - [smallint!]	
awayPoints - smallint	
awayTeam - String	
city - String	
conferenceGame - Boolean	
currentClock - String	
currentPeriod - smallint	
currentPossession - String	
currentSituation - String	
homeClassification - division	
homeConference - String	
homeConferenceAbbreviation - String	
homeId - Int	
homeLineScores - [smallint!]	
homePoints - smallint	
homeTeam - String	
id - Int	
lastPlay - String	
moneylineAway - Int	
moneylineHome - Int	
neutralSite - Boolean	
overUnder - numeric	
spread - numeric	
startDate - timestamptz	
startTimeTbd - Boolean	
state - String	
status - game_status	
temperature - numeric	
tv - String	
venue - String	
weatherDescription - String	
windDirection - numeric	
windSpeed - numeric	
Example
{
  "awayClassification": division,
  "awayConference": "abc123",
  "awayConferenceAbbreviation": "abc123",
  "awayId": 987,
  "awayLineScores": [smallint],
  "awayPoints": smallint,
  "awayTeam": "abc123",
  "city": "xyz789",
  "conferenceGame": true,
  "currentClock": "abc123",
  "currentPeriod": smallint,
  "currentPossession": "xyz789",
  "currentSituation": "abc123",
  "homeClassification": division,
  "homeConference": "xyz789",
  "homeConferenceAbbreviation": "xyz789",
  "homeId": 123,
  "homeLineScores": [smallint],
  "homePoints": smallint,
  "homeTeam": "xyz789",
  "id": 123,
  "lastPlay": "abc123",
  "moneylineAway": 987,
  "moneylineHome": 987,
  "neutralSite": true,
  "overUnder": numeric,
  "spread": numeric,
  "startDate": timestamptz,
  "startTimeTbd": true,
  "state": "abc123",
  "status": game_status,
  "temperature": numeric,
  "tv": "xyz789",
  "venue": "xyz789",
  "weatherDescription": "abc123",
  "windDirection": numeric,
  "windSpeed": numeric
}
Types
ScoreboardBoolExp
Description
Boolean expression to filter rows from the table "scoreboard". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [ScoreboardBoolExp!]	
_not - ScoreboardBoolExp	
_or - [ScoreboardBoolExp!]	
awayClassification - DivisionComparisonExp	
awayConference - StringComparisonExp	
awayConferenceAbbreviation - StringComparisonExp	
awayId - IntComparisonExp	
awayLineScores - SmallintArrayComparisonExp	
awayPoints - SmallintComparisonExp	
awayTeam - StringComparisonExp	
city - StringComparisonExp	
conferenceGame - BooleanComparisonExp	
currentClock - StringComparisonExp	
currentPeriod - SmallintComparisonExp	
currentPossession - StringComparisonExp	
currentSituation - StringComparisonExp	
homeClassification - DivisionComparisonExp	
homeConference - StringComparisonExp	
homeConferenceAbbreviation - StringComparisonExp	
homeId - IntComparisonExp	
homeLineScores - SmallintArrayComparisonExp	
homePoints - SmallintComparisonExp	
homeTeam - StringComparisonExp	
id - IntComparisonExp	
lastPlay - StringComparisonExp	
moneylineAway - IntComparisonExp	
moneylineHome - IntComparisonExp	
neutralSite - BooleanComparisonExp	
overUnder - NumericComparisonExp	
spread - NumericComparisonExp	
startDate - TimestamptzComparisonExp	
startTimeTbd - BooleanComparisonExp	
state - StringComparisonExp	
status - GameStatusComparisonExp	
temperature - NumericComparisonExp	
tv - StringComparisonExp	
venue - StringComparisonExp	
weatherDescription - StringComparisonExp	
windDirection - NumericComparisonExp	
windSpeed - NumericComparisonExp	
Example
{
  "_and": [ScoreboardBoolExp],
  "_not": ScoreboardBoolExp,
  "_or": [ScoreboardBoolExp],
  "awayClassification": DivisionComparisonExp,
  "awayConference": StringComparisonExp,
  "awayConferenceAbbreviation": StringComparisonExp,
  "awayId": IntComparisonExp,
  "awayLineScores": SmallintArrayComparisonExp,
  "awayPoints": SmallintComparisonExp,
  "awayTeam": StringComparisonExp,
  "city": StringComparisonExp,
  "conferenceGame": BooleanComparisonExp,
  "currentClock": StringComparisonExp,
  "currentPeriod": SmallintComparisonExp,
  "currentPossession": StringComparisonExp,
  "currentSituation": StringComparisonExp,
  "homeClassification": DivisionComparisonExp,
  "homeConference": StringComparisonExp,
  "homeConferenceAbbreviation": StringComparisonExp,
  "homeId": IntComparisonExp,
  "homeLineScores": SmallintArrayComparisonExp,
  "homePoints": SmallintComparisonExp,
  "homeTeam": StringComparisonExp,
  "id": IntComparisonExp,
  "lastPlay": StringComparisonExp,
  "moneylineAway": IntComparisonExp,
  "moneylineHome": IntComparisonExp,
  "neutralSite": BooleanComparisonExp,
  "overUnder": NumericComparisonExp,
  "spread": NumericComparisonExp,
  "startDate": TimestamptzComparisonExp,
  "startTimeTbd": BooleanComparisonExp,
  "state": StringComparisonExp,
  "status": GameStatusComparisonExp,
  "temperature": NumericComparisonExp,
  "tv": StringComparisonExp,
  "venue": StringComparisonExp,
  "weatherDescription": StringComparisonExp,
  "windDirection": NumericComparisonExp,
  "windSpeed": NumericComparisonExp
}
Types
ScoreboardOrderBy
Description
Ordering options when selecting data from "scoreboard".

Fields
Input Field	Description
awayClassification - OrderBy	
awayConference - OrderBy	
awayConferenceAbbreviation - OrderBy	
awayId - OrderBy	
awayLineScores - OrderBy	
awayPoints - OrderBy	
awayTeam - OrderBy	
city - OrderBy	
conferenceGame - OrderBy	
currentClock - OrderBy	
currentPeriod - OrderBy	
currentPossession - OrderBy	
currentSituation - OrderBy	
homeClassification - OrderBy	
homeConference - OrderBy	
homeConferenceAbbreviation - OrderBy	
homeId - OrderBy	
homeLineScores - OrderBy	
homePoints - OrderBy	
homeTeam - OrderBy	
id - OrderBy	
lastPlay - OrderBy	
moneylineAway - OrderBy	
moneylineHome - OrderBy	
neutralSite - OrderBy	
overUnder - OrderBy	
spread - OrderBy	
startDate - OrderBy	
startTimeTbd - OrderBy	
state - OrderBy	
status - OrderBy	
temperature - OrderBy	
tv - OrderBy	
venue - OrderBy	
weatherDescription - OrderBy	
windDirection - OrderBy	
windSpeed - OrderBy	
Example
{
  "awayClassification": "ASC",
  "awayConference": "ASC",
  "awayConferenceAbbreviation": "ASC",
  "awayId": "ASC",
  "awayLineScores": "ASC",
  "awayPoints": "ASC",
  "awayTeam": "ASC",
  "city": "ASC",
  "conferenceGame": "ASC",
  "currentClock": "ASC",
  "currentPeriod": "ASC",
  "currentPossession": "ASC",
  "currentSituation": "ASC",
  "homeClassification": "ASC",
  "homeConference": "ASC",
  "homeConferenceAbbreviation": "ASC",
  "homeId": "ASC",
  "homeLineScores": "ASC",
  "homePoints": "ASC",
  "homeTeam": "ASC",
  "id": "ASC",
  "lastPlay": "ASC",
  "moneylineAway": "ASC",
  "moneylineHome": "ASC",
  "neutralSite": "ASC",
  "overUnder": "ASC",
  "spread": "ASC",
  "startDate": "ASC",
  "startTimeTbd": "ASC",
  "state": "ASC",
  "status": "ASC",
  "temperature": "ASC",
  "tv": "ASC",
  "venue": "ASC",
  "weatherDescription": "ASC",
  "windDirection": "ASC",
  "windSpeed": "ASC"
}
Types
ScoreboardSelectColumn
Description
select columns of table "scoreboard"

Values
Enum Value	Description
awayClassification

column name
awayConference

column name
awayConferenceAbbreviation

column name
awayId

column name
awayLineScores

column name
awayPoints

column name
awayTeam

column name
city

column name
conferenceGame

column name
currentClock

column name
currentPeriod

column name
currentPossession

column name
currentSituation

column name
homeClassification

column name
homeConference

column name
homeConferenceAbbreviation

column name
homeId

column name
homeLineScores

column name
homePoints

column name
homeTeam

column name
id

column name
lastPlay

column name
moneylineAway

column name
moneylineHome

column name
neutralSite

column name
overUnder

column name
spread

column name
startDate

column name
startTimeTbd

column name
state

column name
status

column name
temperature

column name
tv

column name
venue

column name
weatherDescription

column name
windDirection

column name
windSpeed

column name
Example
"awayClassification"
Types
SeasonTypeComparisonExp
Description
Boolean expression to compare columns of type "season_type". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - season_type	
_gt - season_type	
_gte - season_type	
_in - [season_type!]	
_isNull - Boolean	
_lt - season_type	
_lte - season_type	
_neq - season_type	
_nin - [season_type!]	
Example
{
  "_eq": season_type,
  "_gt": season_type,
  "_gte": season_type,
  "_in": [season_type],
  "_isNull": true,
  "_lt": season_type,
  "_lte": season_type,
  "_neq": season_type,
  "_nin": [season_type]
}
Types
SmallintArrayComparisonExp
Description
Boolean expression to compare columns of type "smallint". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_containedIn - [smallint!]	is the array contained in the given array value
_contains - [smallint!]	does the array contain the given value
_eq - [smallint!]	
_gt - [smallint!]	
_gte - [smallint!]	
_in - [smallint!]	
_isNull - Boolean	
_lt - [smallint!]	
_lte - [smallint!]	
_neq - [smallint!]	
_nin - [smallint!]	
Example
{
  "_containedIn": [smallint],
  "_contains": [smallint],
  "_eq": [smallint],
  "_gt": [smallint],
  "_gte": [smallint],
  "_in": [smallint],
  "_isNull": false,
  "_lt": [smallint],
  "_lte": [smallint],
  "_neq": [smallint],
  "_nin": [smallint]
}
Types
SmallintComparisonExp
Description
Boolean expression to compare columns of type "smallint". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - smallint	
_gt - smallint	
_gte - smallint	
_in - [smallint!]	
_isNull - Boolean	
_lt - smallint	
_lte - smallint	
_neq - smallint	
_nin - [smallint!]	
Example
{
  "_eq": smallint,
  "_gt": smallint,
  "_gte": smallint,
  "_in": [smallint],
  "_isNull": false,
  "_lt": smallint,
  "_lte": smallint,
  "_neq": smallint,
  "_nin": [smallint]
}
Types
String
Example
"xyz789"
Types
StringArrayComparisonExp
Description
Boolean expression to compare columns of type "String". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_containedIn - [String!]	is the array contained in the given array value
_contains - [String!]	does the array contain the given value
_eq - [String!]	
_gt - [String!]	
_gte - [String!]	
_in - [String!]	
_isNull - Boolean	
_lt - [String!]	
_lte - [String!]	
_neq - [String!]	
_nin - [String!]	
Example
{
  "_containedIn": ["xyz789"],
  "_contains": ["xyz789"],
  "_eq": ["abc123"],
  "_gt": ["xyz789"],
  "_gte": ["abc123"],
  "_in": ["abc123"],
  "_isNull": false,
  "_lt": ["xyz789"],
  "_lte": ["xyz789"],
  "_neq": ["xyz789"],
  "_nin": ["abc123"]
}
Types
StringComparisonExp
Description
Boolean expression to compare columns of type "String". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - String	
_gt - String	
_gte - String	
_ilike - String	does the column match the given case-insensitive pattern
_in - [String!]	
_iregex - String	does the column match the given POSIX regular expression, case insensitive
_isNull - Boolean	
_like - String	does the column match the given pattern
_lt - String	
_lte - String	
_neq - String	
_nilike - String	does the column NOT match the given case-insensitive pattern
_nin - [String!]	
_niregex - String	does the column NOT match the given POSIX regular expression, case insensitive
_nlike - String	does the column NOT match the given pattern
_nregex - String	does the column NOT match the given POSIX regular expression, case sensitive
_nsimilar - String	does the column NOT match the given SQL regular expression
_regex - String	does the column match the given POSIX regular expression, case sensitive
_similar - String	does the column match the given SQL regular expression
Example
{
  "_eq": "xyz789",
  "_gt": "xyz789",
  "_gte": "xyz789",
  "_ilike": "abc123",
  "_in": ["xyz789"],
  "_iregex": "xyz789",
  "_isNull": true,
  "_like": "abc123",
  "_lt": "abc123",
  "_lte": "xyz789",
  "_neq": "abc123",
  "_nilike": "abc123",
  "_nin": ["abc123"],
  "_niregex": "xyz789",
  "_nlike": "xyz789",
  "_nregex": "abc123",
  "_nsimilar": "xyz789",
  "_regex": "xyz789",
  "_similar": "abc123"
}
Types
TeamTalent
Description
columns and relationships of "team_talent"

Fields
Field Name	Description
talent - numeric!	
team - currentTeams	An object relationship
year - smallint!	
Example
{
  "talent": numeric,
  "team": currentTeams,
  "year": smallint
}
Types
TeamTalentAggregate
Description
aggregated selection of "team_talent"

Fields
Field Name	Description
aggregate - TeamTalentAggregateFields	
nodes - [TeamTalent!]!	
Example
{
  "aggregate": TeamTalentAggregateFields,
  "nodes": [TeamTalent]
}
Types
TeamTalentAggregateFields
Description
aggregate fields of "team_talent"

Fields
Field Name	Description
avg - TeamTalentAvgFields	
count - Int!	
Arguments
columns - [TeamTalentSelectColumn!]
distinct - Boolean
max - TeamTalentMaxFields	
min - TeamTalentMinFields	
stddev - TeamTalentStddevFields	
stddevPop - TeamTalentStddevPopFields	
stddevSamp - TeamTalentStddevSampFields	
sum - TeamTalentSumFields	
varPop - TeamTalentVarPopFields	
varSamp - TeamTalentVarSampFields	
variance - TeamTalentVarianceFields	
Example
{
  "avg": TeamTalentAvgFields,
  "count": 123,
  "max": TeamTalentMaxFields,
  "min": TeamTalentMinFields,
  "stddev": TeamTalentStddevFields,
  "stddevPop": TeamTalentStddevPopFields,
  "stddevSamp": TeamTalentStddevSampFields,
  "sum": TeamTalentSumFields,
  "varPop": TeamTalentVarPopFields,
  "varSamp": TeamTalentVarSampFields,
  "variance": TeamTalentVarianceFields
}
Types
TeamTalentAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 123.45, "year": 987.65}
Types
TeamTalentBoolExp
Description
Boolean expression to filter rows from the table "team_talent". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [TeamTalentBoolExp!]	
_not - TeamTalentBoolExp	
_or - [TeamTalentBoolExp!]	
talent - NumericComparisonExp	
team - currentTeamsBoolExp	
year - SmallintComparisonExp	
Example
{
  "_and": [TeamTalentBoolExp],
  "_not": TeamTalentBoolExp,
  "_or": [TeamTalentBoolExp],
  "talent": NumericComparisonExp,
  "team": currentTeamsBoolExp,
  "year": SmallintComparisonExp
}
Types
TeamTalentMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
talent - numeric	
year - smallint	
Example
{
  "talent": numeric,
  "year": smallint
}
Types
TeamTalentMinFields
Description
aggregate min on columns

Fields
Field Name	Description
talent - numeric	
year - smallint	
Example
{
  "talent": numeric,
  "year": smallint
}
Types
TeamTalentOrderBy
Description
Ordering options when selecting data from "team_talent".

Fields
Input Field	Description
talent - OrderBy	
team - currentTeamsOrderBy	
year - OrderBy	
Example
{
  "talent": "ASC",
  "team": currentTeamsOrderBy,
  "year": "ASC"
}
Types
TeamTalentSelectColumn
Description
select columns of table "team_talent"

Values
Enum Value	Description
talent

column name
year

column name
Example
"talent"
Types
TeamTalentStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 123.45, "year": 123.45}
Types
TeamTalentStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 987.65, "year": 987.65}
Types
TeamTalentStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 123.45, "year": 987.65}
Types
TeamTalentSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
talent - numeric	
year - smallint	
Example
{
  "talent": numeric,
  "year": smallint
}
Types
TeamTalentVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 123.45, "year": 123.45}
Types
TeamTalentVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 987.65, "year": 123.45}
Types
TeamTalentVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
talent - Float	
year - Float	
Example
{"talent": 123.45, "year": 987.65}
Types
TimestampComparisonExp
Description
Boolean expression to compare columns of type "timestamp". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - timestamp	
_gt - timestamp	
_gte - timestamp	
_in - [timestamp!]	
_isNull - Boolean	
_lt - timestamp	
_lte - timestamp	
_neq - timestamp	
_nin - [timestamp!]	
Example
{
  "_eq": timestamp,
  "_gt": timestamp,
  "_gte": timestamp,
  "_in": [timestamp],
  "_isNull": true,
  "_lt": timestamp,
  "_lte": timestamp,
  "_neq": timestamp,
  "_nin": [timestamp]
}
Types
TimestamptzComparisonExp
Description
Boolean expression to compare columns of type "timestamptz". All fields are combined with logical 'AND'.

Fields
Input Field	Description
_eq - timestamptz	
_gt - timestamptz	
_gte - timestamptz	
_in - [timestamptz!]	
_isNull - Boolean	
_lt - timestamptz	
_lte - timestamptz	
_neq - timestamptz	
_nin - [timestamptz!]	
Example
{
  "_eq": timestamptz,
  "_gt": timestamptz,
  "_gte": timestamptz,
  "_in": [timestamptz],
  "_isNull": true,
  "_lt": timestamptz,
  "_lte": timestamptz,
  "_neq": timestamptz,
  "_nin": [timestamptz]
}
Types
Transfer
Description
columns and relationships of "transfer"

Fields
Field Name	Description
eligibility - String	
firstName - String!	
fromTeam - currentTeams	An object relationship
lastName - String!	
position - RecruitPosition	An object relationship
rating - numeric	
season - smallint!	
stars - smallint	
toTeam - currentTeams	An object relationship
transferDate - timestamp	
Example
{
  "eligibility": "xyz789",
  "firstName": "xyz789",
  "fromTeam": currentTeams,
  "lastName": "xyz789",
  "position": RecruitPosition,
  "rating": numeric,
  "season": smallint,
  "stars": smallint,
  "toTeam": currentTeams,
  "transferDate": timestamp
}
Types
TransferBoolExp
Description
Boolean expression to filter rows from the table "transfer". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [TransferBoolExp!]	
_not - TransferBoolExp	
_or - [TransferBoolExp!]	
eligibility - StringComparisonExp	
firstName - StringComparisonExp	
fromTeam - currentTeamsBoolExp	
lastName - StringComparisonExp	
position - RecruitPositionBoolExp	
rating - NumericComparisonExp	
season - SmallintComparisonExp	
stars - SmallintComparisonExp	
toTeam - currentTeamsBoolExp	
transferDate - TimestampComparisonExp	
Example
{
  "_and": [TransferBoolExp],
  "_not": TransferBoolExp,
  "_or": [TransferBoolExp],
  "eligibility": StringComparisonExp,
  "firstName": StringComparisonExp,
  "fromTeam": currentTeamsBoolExp,
  "lastName": StringComparisonExp,
  "position": RecruitPositionBoolExp,
  "rating": NumericComparisonExp,
  "season": SmallintComparisonExp,
  "stars": SmallintComparisonExp,
  "toTeam": currentTeamsBoolExp,
  "transferDate": TimestampComparisonExp
}
Types
TransferOrderBy
Description
Ordering options when selecting data from "transfer".

Fields
Input Field	Description
eligibility - OrderBy	
firstName - OrderBy	
fromTeam - currentTeamsOrderBy	
lastName - OrderBy	
position - RecruitPositionOrderBy	
rating - OrderBy	
season - OrderBy	
stars - OrderBy	
toTeam - currentTeamsOrderBy	
transferDate - OrderBy	
Example
{
  "eligibility": "ASC",
  "firstName": "ASC",
  "fromTeam": currentTeamsOrderBy,
  "lastName": "ASC",
  "position": RecruitPositionOrderBy,
  "rating": "ASC",
  "season": "ASC",
  "stars": "ASC",
  "toTeam": currentTeamsOrderBy,
  "transferDate": "ASC"
}
Types
TransferSelectColumn
Description
select columns of table "transfer"

Values
Enum Value	Description
eligibility

column name
firstName

column name
lastName

column name
rating

column name
season

column name
stars

column name
transferDate

column name
Example
"eligibility"
Types
WeatherCondition
Description
columns and relationships of "weather_condition"

Fields
Field Name	Description
description - String!	
id - smallint!	
Example
{
  "description": "xyz789",
  "id": smallint
}
Types
WeatherConditionBoolExp
Description
Boolean expression to filter rows from the table "weather_condition". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [WeatherConditionBoolExp!]	
_not - WeatherConditionBoolExp	
_or - [WeatherConditionBoolExp!]	
description - StringComparisonExp	
id - SmallintComparisonExp	
Example
{
  "_and": [WeatherConditionBoolExp],
  "_not": WeatherConditionBoolExp,
  "_or": [WeatherConditionBoolExp],
  "description": StringComparisonExp,
  "id": SmallintComparisonExp
}
Types
WeatherConditionOrderBy
Description
Ordering options when selecting data from "weather_condition".

Fields
Input Field	Description
description - OrderBy	
id - OrderBy	
Example
{"description": "ASC", "id": "ASC"}
Types
WeatherConditionSelectColumn
Description
select columns of table "weather_condition"

Values
Enum Value	Description
description

column name
id

column name
Example
"description"
Types
adjustedPlayerMetricsAggregateBoolExpCount
Fields
Input Field	Description
arguments - [AdjustedPlayerMetricsSelectColumn!]	
distinct - Boolean	
filter - AdjustedPlayerMetricsBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["athleteId"],
  "distinct": false,
  "filter": AdjustedPlayerMetricsBoolExp,
  "predicate": IntComparisonExp
}
Types
athleteAggregateBoolExpCount
Fields
Input Field	Description
arguments - [AthleteSelectColumn!]	
distinct - Boolean	
filter - AthleteBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["firstName"],
  "distinct": false,
  "filter": AthleteBoolExp,
  "predicate": IntComparisonExp
}
Types
athleteTeamAggregateBoolExpCount
Fields
Input Field	Description
arguments - [AthleteTeamSelectColumn!]	
distinct - Boolean	
filter - AthleteTeamBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["athleteId"],
  "distinct": true,
  "filter": AthleteTeamBoolExp,
  "predicate": IntComparisonExp
}
Types
bigint
Example
bigint
Types
coachSeasonAggregateBoolExpCount
Fields
Input Field	Description
arguments - [CoachSeasonSelectColumn!]	
distinct - Boolean	
filter - CoachSeasonBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["games"],
  "distinct": true,
  "filter": CoachSeasonBoolExp,
  "predicate": IntComparisonExp
}
Types
currentTeams
Description
columns and relationships of "current_conferences"

Fields
Field Name	Description
abbreviation - String	
classification - division	
conference - String	
conferenceId - smallint	
division - String	
school - String	
teamId - Int	
Example
{
  "abbreviation": "xyz789",
  "classification": division,
  "conference": "abc123",
  "conferenceId": smallint,
  "division": "xyz789",
  "school": "abc123",
  "teamId": 987
}
Types
currentTeamsAggregate
Description
aggregated selection of "current_conferences"

Fields
Field Name	Description
aggregate - currentTeamsAggregateFields	
nodes - [currentTeams!]!	
Example
{
  "aggregate": currentTeamsAggregateFields,
  "nodes": [currentTeams]
}
Types
currentTeamsAggregateFields
Description
aggregate fields of "current_conferences"

Fields
Field Name	Description
avg - currentTeamsAvgFields	
count - Int!	
Arguments
columns - [currentTeamsSelectColumn!]
distinct - Boolean
max - currentTeamsMaxFields	
min - currentTeamsMinFields	
stddev - currentTeamsStddevFields	
stddevPop - currentTeamsStddevPopFields	
stddevSamp - currentTeamsStddevSampFields	
sum - currentTeamsSumFields	
varPop - currentTeamsVarPopFields	
varSamp - currentTeamsVarSampFields	
variance - currentTeamsVarianceFields	
Example
{
  "avg": currentTeamsAvgFields,
  "count": 123,
  "max": currentTeamsMaxFields,
  "min": currentTeamsMinFields,
  "stddev": currentTeamsStddevFields,
  "stddevPop": currentTeamsStddevPopFields,
  "stddevSamp": currentTeamsStddevSampFields,
  "sum": currentTeamsSumFields,
  "varPop": currentTeamsVarPopFields,
  "varSamp": currentTeamsVarSampFields,
  "variance": currentTeamsVarianceFields
}
Types
currentTeamsAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 123.45, "teamId": 123.45}
Types
currentTeamsBoolExp
Description
Boolean expression to filter rows from the table "current_conferences". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [currentTeamsBoolExp!]	
_not - currentTeamsBoolExp	
_or - [currentTeamsBoolExp!]	
abbreviation - StringComparisonExp	
classification - DivisionComparisonExp	
conference - StringComparisonExp	
conferenceId - SmallintComparisonExp	
division - StringComparisonExp	
school - StringComparisonExp	
teamId - IntComparisonExp	
Example
{
  "_and": [currentTeamsBoolExp],
  "_not": currentTeamsBoolExp,
  "_or": [currentTeamsBoolExp],
  "abbreviation": StringComparisonExp,
  "classification": DivisionComparisonExp,
  "conference": StringComparisonExp,
  "conferenceId": SmallintComparisonExp,
  "division": StringComparisonExp,
  "school": StringComparisonExp,
  "teamId": IntComparisonExp
}
Types
currentTeamsMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
abbreviation - String	
classification - division	
conference - String	
conferenceId - smallint	
division - String	
school - String	
teamId - Int	
Example
{
  "abbreviation": "abc123",
  "classification": division,
  "conference": "abc123",
  "conferenceId": smallint,
  "division": "xyz789",
  "school": "xyz789",
  "teamId": 987
}
Types
currentTeamsMinFields
Description
aggregate min on columns

Fields
Field Name	Description
abbreviation - String	
classification - division	
conference - String	
conferenceId - smallint	
division - String	
school - String	
teamId - Int	
Example
{
  "abbreviation": "abc123",
  "classification": division,
  "conference": "xyz789",
  "conferenceId": smallint,
  "division": "xyz789",
  "school": "xyz789",
  "teamId": 987
}
Types
currentTeamsOrderBy
Description
Ordering options when selecting data from "current_conferences".

Fields
Input Field	Description
abbreviation - OrderBy	
classification - OrderBy	
conference - OrderBy	
conferenceId - OrderBy	
division - OrderBy	
school - OrderBy	
teamId - OrderBy	
Example
{
  "abbreviation": "ASC",
  "classification": "ASC",
  "conference": "ASC",
  "conferenceId": "ASC",
  "division": "ASC",
  "school": "ASC",
  "teamId": "ASC"
}
Types
currentTeamsSelectColumn
Description
select columns of table "current_conferences"

Values
Enum Value	Description
abbreviation

column name
classification

column name
conference

column name
conferenceId

column name
division

column name
school

column name
teamId

column name
Example
"abbreviation"
Types
currentTeamsStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 123.45, "teamId": 987.65}
Types
currentTeamsStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 123.45, "teamId": 123.45}
Types
currentTeamsStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 987.65, "teamId": 123.45}
Types
currentTeamsSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
conferenceId - smallint	
teamId - Int	
Example
{"conferenceId": smallint, "teamId": 123}
Types
currentTeamsVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 987.65, "teamId": 123.45}
Types
currentTeamsVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 987.65, "teamId": 123.45}
Types
currentTeamsVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
conferenceId - Float	
teamId - Float	
Example
{"conferenceId": 987.65, "teamId": 123.45}
Types
division
Example
division
Types
draftPicksAggregateBoolExpCount
Fields
Input Field	Description
arguments - [DraftPicksSelectColumn!]	
distinct - Boolean	
filter - DraftPicksBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["collegeId"],
  "distinct": false,
  "filter": DraftPicksBoolExp,
  "predicate": IntComparisonExp
}
Types
game
Description
columns and relationships of "game_info"

Fields
Field Name	Description
attendance - Int	
awayClassification - division	
awayConference - String	
awayConferenceId - smallint	
awayConferenceInfo - Conference	An object relationship
awayEndElo - Int	
awayLineScores - [smallint!]	
awayPoints - smallint	
awayPostgameWinProb - numeric	
awayStartElo - Int	
awayTeam - String	
awayTeamId - Int	
awayTeamInfo - currentTeams	An object relationship
conferenceGame - Boolean	
excitement - numeric	
homeClassification - division	
homeConference - String	
homeConferenceId - smallint	
homeConferenceInfo - Conference	An object relationship
homeEndElo - Int	
homeLineScores - [smallint!]	
homePoints - smallint	
homePostgameWinProb - numeric	
homeStartElo - Int	
homeTeam - String	
homeTeamId - Int	
homeTeamInfo - currentTeams	An object relationship
id - Int	
lines - [GameLines!]!	An array relationship
Arguments
distinctOn - [GameLinesSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GameLinesOrderBy!]
sort the rows by one or more columns

where - GameLinesBoolExp
filter the rows returned

linesAggregate - GameLinesAggregate!	An aggregate relationship
Arguments
distinctOn - [GameLinesSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GameLinesOrderBy!]
sort the rows by one or more columns

where - GameLinesBoolExp
filter the rows returned

mediaInfo - [GameMedia!]!	An array relationship
Arguments
distinctOn - [GameMediaSelectColumn!]
distinct select on columns

limit - Int
limit the number of rows returned

offset - Int
skip the first n rows. Use only with order_by

orderBy - [GameMediaOrderBy!]
sort the rows by one or more columns

where - GameMediaBoolExp
filter the rows returned

neutralSite - Boolean	
notes - String	
season - smallint	
seasonType - season_type	
startDate - timestamp	
startTimeTbd - Boolean	
status - game_status	
venueId - Int	
weather - GameWeather	An object relationship
week - smallint	
Example
{
  "attendance": 987,
  "awayClassification": division,
  "awayConference": "abc123",
  "awayConferenceId": smallint,
  "awayConferenceInfo": Conference,
  "awayEndElo": 987,
  "awayLineScores": [smallint],
  "awayPoints": smallint,
  "awayPostgameWinProb": numeric,
  "awayStartElo": 987,
  "awayTeam": "abc123",
  "awayTeamId": 987,
  "awayTeamInfo": currentTeams,
  "conferenceGame": false,
  "excitement": numeric,
  "homeClassification": division,
  "homeConference": "abc123",
  "homeConferenceId": smallint,
  "homeConferenceInfo": Conference,
  "homeEndElo": 123,
  "homeLineScores": [smallint],
  "homePoints": smallint,
  "homePostgameWinProb": numeric,
  "homeStartElo": 123,
  "homeTeam": "xyz789",
  "homeTeamId": 987,
  "homeTeamInfo": currentTeams,
  "id": 123,
  "lines": [GameLines],
  "linesAggregate": GameLinesAggregate,
  "mediaInfo": [GameMedia],
  "neutralSite": true,
  "notes": "abc123",
  "season": smallint,
  "seasonType": season_type,
  "startDate": timestamp,
  "startTimeTbd": false,
  "status": game_status,
  "venueId": 987,
  "weather": GameWeather,
  "week": smallint
}
Types
gameAggregate
Description
aggregated selection of "game_info"

Fields
Field Name	Description
aggregate - gameAggregateFields	
nodes - [game!]!	
Example
{
  "aggregate": gameAggregateFields,
  "nodes": [game]
}
Types
gameAggregateFields
Description
aggregate fields of "game_info"

Fields
Field Name	Description
avg - gameAvgFields	
count - Int!	
Arguments
columns - [gameSelectColumn!]
distinct - Boolean
max - gameMaxFields	
min - gameMinFields	
stddev - gameStddevFields	
stddevPop - gameStddevPopFields	
stddevSamp - gameStddevSampFields	
sum - gameSumFields	
varPop - gameVarPopFields	
varSamp - gameVarSampFields	
variance - gameVarianceFields	
Example
{
  "avg": gameAvgFields,
  "count": 123,
  "max": gameMaxFields,
  "min": gameMinFields,
  "stddev": gameStddevFields,
  "stddevPop": gameStddevPopFields,
  "stddevSamp": gameStddevSampFields,
  "sum": gameSumFields,
  "varPop": gameVarPopFields,
  "varSamp": gameVarSampFields,
  "variance": gameVarianceFields
}
Types
gameAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 987.65,
  "awayConferenceId": 123.45,
  "awayEndElo": 987.65,
  "awayPoints": 123.45,
  "awayPostgameWinProb": 123.45,
  "awayStartElo": 123.45,
  "awayTeamId": 123.45,
  "excitement": 987.65,
  "homeConferenceId": 123.45,
  "homeEndElo": 123.45,
  "homePoints": 987.65,
  "homePostgameWinProb": 123.45,
  "homeStartElo": 123.45,
  "homeTeamId": 123.45,
  "id": 987.65,
  "season": 987.65,
  "venueId": 987.65,
  "week": 987.65
}
Types
gameBoolExp
Description
Boolean expression to filter rows from the table "game_info". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [gameBoolExp!]	
_not - gameBoolExp	
_or - [gameBoolExp!]	
attendance - IntComparisonExp	
awayClassification - DivisionComparisonExp	
awayConference - StringComparisonExp	
awayConferenceId - SmallintComparisonExp	
awayConferenceInfo - ConferenceBoolExp	
awayEndElo - IntComparisonExp	
awayLineScores - SmallintArrayComparisonExp	
awayPoints - SmallintComparisonExp	
awayPostgameWinProb - NumericComparisonExp	
awayStartElo - IntComparisonExp	
awayTeam - StringComparisonExp	
awayTeamId - IntComparisonExp	
awayTeamInfo - currentTeamsBoolExp	
conferenceGame - BooleanComparisonExp	
excitement - NumericComparisonExp	
homeClassification - DivisionComparisonExp	
homeConference - StringComparisonExp	
homeConferenceId - SmallintComparisonExp	
homeConferenceInfo - ConferenceBoolExp	
homeEndElo - IntComparisonExp	
homeLineScores - SmallintArrayComparisonExp	
homePoints - SmallintComparisonExp	
homePostgameWinProb - NumericComparisonExp	
homeStartElo - IntComparisonExp	
homeTeam - StringComparisonExp	
homeTeamId - IntComparisonExp	
homeTeamInfo - currentTeamsBoolExp	
id - IntComparisonExp	
lines - GameLinesBoolExp	
linesAggregate - GameLinesAggregateBoolExp	
mediaInfo - GameMediaBoolExp	
neutralSite - BooleanComparisonExp	
notes - StringComparisonExp	
season - SmallintComparisonExp	
seasonType - SeasonTypeComparisonExp	
startDate - TimestampComparisonExp	
startTimeTbd - BooleanComparisonExp	
status - GameStatusComparisonExp	
venueId - IntComparisonExp	
weather - GameWeatherBoolExp	
week - SmallintComparisonExp	
Example
{
  "_and": [gameBoolExp],
  "_not": gameBoolExp,
  "_or": [gameBoolExp],
  "attendance": IntComparisonExp,
  "awayClassification": DivisionComparisonExp,
  "awayConference": StringComparisonExp,
  "awayConferenceId": SmallintComparisonExp,
  "awayConferenceInfo": ConferenceBoolExp,
  "awayEndElo": IntComparisonExp,
  "awayLineScores": SmallintArrayComparisonExp,
  "awayPoints": SmallintComparisonExp,
  "awayPostgameWinProb": NumericComparisonExp,
  "awayStartElo": IntComparisonExp,
  "awayTeam": StringComparisonExp,
  "awayTeamId": IntComparisonExp,
  "awayTeamInfo": currentTeamsBoolExp,
  "conferenceGame": BooleanComparisonExp,
  "excitement": NumericComparisonExp,
  "homeClassification": DivisionComparisonExp,
  "homeConference": StringComparisonExp,
  "homeConferenceId": SmallintComparisonExp,
  "homeConferenceInfo": ConferenceBoolExp,
  "homeEndElo": IntComparisonExp,
  "homeLineScores": SmallintArrayComparisonExp,
  "homePoints": SmallintComparisonExp,
  "homePostgameWinProb": NumericComparisonExp,
  "homeStartElo": IntComparisonExp,
  "homeTeam": StringComparisonExp,
  "homeTeamId": IntComparisonExp,
  "homeTeamInfo": currentTeamsBoolExp,
  "id": IntComparisonExp,
  "lines": GameLinesBoolExp,
  "linesAggregate": GameLinesAggregateBoolExp,
  "mediaInfo": GameMediaBoolExp,
  "neutralSite": BooleanComparisonExp,
  "notes": StringComparisonExp,
  "season": SmallintComparisonExp,
  "seasonType": SeasonTypeComparisonExp,
  "startDate": TimestampComparisonExp,
  "startTimeTbd": BooleanComparisonExp,
  "status": GameStatusComparisonExp,
  "venueId": IntComparisonExp,
  "weather": GameWeatherBoolExp,
  "week": SmallintComparisonExp
}
Types
gameLinesAggregateBoolExpCount
Fields
Input Field	Description
arguments - [GameLinesSelectColumn!]	
distinct - Boolean	
filter - GameLinesBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["gameId"],
  "distinct": false,
  "filter": GameLinesBoolExp,
  "predicate": IntComparisonExp
}
Types
gameMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
attendance - Int	
awayClassification - division	
awayConference - String	
awayConferenceId - smallint	
awayEndElo - Int	
awayLineScores - [smallint!]	
awayPoints - smallint	
awayPostgameWinProb - numeric	
awayStartElo - Int	
awayTeam - String	
awayTeamId - Int	
excitement - numeric	
homeClassification - division	
homeConference - String	
homeConferenceId - smallint	
homeEndElo - Int	
homeLineScores - [smallint!]	
homePoints - smallint	
homePostgameWinProb - numeric	
homeStartElo - Int	
homeTeam - String	
homeTeamId - Int	
id - Int	
notes - String	
season - smallint	
seasonType - season_type	
startDate - timestamp	
status - game_status	
venueId - Int	
week - smallint	
Example
{
  "attendance": 123,
  "awayClassification": division,
  "awayConference": "xyz789",
  "awayConferenceId": smallint,
  "awayEndElo": 987,
  "awayLineScores": [smallint],
  "awayPoints": smallint,
  "awayPostgameWinProb": numeric,
  "awayStartElo": 987,
  "awayTeam": "xyz789",
  "awayTeamId": 987,
  "excitement": numeric,
  "homeClassification": division,
  "homeConference": "xyz789",
  "homeConferenceId": smallint,
  "homeEndElo": 987,
  "homeLineScores": [smallint],
  "homePoints": smallint,
  "homePostgameWinProb": numeric,
  "homeStartElo": 987,
  "homeTeam": "abc123",
  "homeTeamId": 987,
  "id": 987,
  "notes": "abc123",
  "season": smallint,
  "seasonType": season_type,
  "startDate": timestamp,
  "status": game_status,
  "venueId": 987,
  "week": smallint
}
Types
gameMinFields
Description
aggregate min on columns

Fields
Field Name	Description
attendance - Int	
awayClassification - division	
awayConference - String	
awayConferenceId - smallint	
awayEndElo - Int	
awayLineScores - [smallint!]	
awayPoints - smallint	
awayPostgameWinProb - numeric	
awayStartElo - Int	
awayTeam - String	
awayTeamId - Int	
excitement - numeric	
homeClassification - division	
homeConference - String	
homeConferenceId - smallint	
homeEndElo - Int	
homeLineScores - [smallint!]	
homePoints - smallint	
homePostgameWinProb - numeric	
homeStartElo - Int	
homeTeam - String	
homeTeamId - Int	
id - Int	
notes - String	
season - smallint	
seasonType - season_type	
startDate - timestamp	
status - game_status	
venueId - Int	
week - smallint	
Example
{
  "attendance": 987,
  "awayClassification": division,
  "awayConference": "abc123",
  "awayConferenceId": smallint,
  "awayEndElo": 987,
  "awayLineScores": [smallint],
  "awayPoints": smallint,
  "awayPostgameWinProb": numeric,
  "awayStartElo": 987,
  "awayTeam": "xyz789",
  "awayTeamId": 123,
  "excitement": numeric,
  "homeClassification": division,
  "homeConference": "xyz789",
  "homeConferenceId": smallint,
  "homeEndElo": 987,
  "homeLineScores": [smallint],
  "homePoints": smallint,
  "homePostgameWinProb": numeric,
  "homeStartElo": 987,
  "homeTeam": "abc123",
  "homeTeamId": 123,
  "id": 987,
  "notes": "xyz789",
  "season": smallint,
  "seasonType": season_type,
  "startDate": timestamp,
  "status": game_status,
  "venueId": 987,
  "week": smallint
}
Types
gameOrderBy
Description
Ordering options when selecting data from "game_info".

Fields
Input Field	Description
attendance - OrderBy	
awayClassification - OrderBy	
awayConference - OrderBy	
awayConferenceId - OrderBy	
awayConferenceInfo - ConferenceOrderBy	
awayEndElo - OrderBy	
awayLineScores - OrderBy	
awayPoints - OrderBy	
awayPostgameWinProb - OrderBy	
awayStartElo - OrderBy	
awayTeam - OrderBy	
awayTeamId - OrderBy	
awayTeamInfo - currentTeamsOrderBy	
conferenceGame - OrderBy	
excitement - OrderBy	
homeClassification - OrderBy	
homeConference - OrderBy	
homeConferenceId - OrderBy	
homeConferenceInfo - ConferenceOrderBy	
homeEndElo - OrderBy	
homeLineScores - OrderBy	
homePoints - OrderBy	
homePostgameWinProb - OrderBy	
homeStartElo - OrderBy	
homeTeam - OrderBy	
homeTeamId - OrderBy	
homeTeamInfo - currentTeamsOrderBy	
id - OrderBy	
linesAggregate - GameLinesAggregateOrderBy	
mediaInfoAggregate - GameMediaAggregateOrderBy	
neutralSite - OrderBy	
notes - OrderBy	
season - OrderBy	
seasonType - OrderBy	
startDate - OrderBy	
startTimeTbd - OrderBy	
status - OrderBy	
venueId - OrderBy	
weather - GameWeatherOrderBy	
week - OrderBy	
Example
{
  "attendance": "ASC",
  "awayClassification": "ASC",
  "awayConference": "ASC",
  "awayConferenceId": "ASC",
  "awayConferenceInfo": ConferenceOrderBy,
  "awayEndElo": "ASC",
  "awayLineScores": "ASC",
  "awayPoints": "ASC",
  "awayPostgameWinProb": "ASC",
  "awayStartElo": "ASC",
  "awayTeam": "ASC",
  "awayTeamId": "ASC",
  "awayTeamInfo": currentTeamsOrderBy,
  "conferenceGame": "ASC",
  "excitement": "ASC",
  "homeClassification": "ASC",
  "homeConference": "ASC",
  "homeConferenceId": "ASC",
  "homeConferenceInfo": ConferenceOrderBy,
  "homeEndElo": "ASC",
  "homeLineScores": "ASC",
  "homePoints": "ASC",
  "homePostgameWinProb": "ASC",
  "homeStartElo": "ASC",
  "homeTeam": "ASC",
  "homeTeamId": "ASC",
  "homeTeamInfo": currentTeamsOrderBy,
  "id": "ASC",
  "linesAggregate": GameLinesAggregateOrderBy,
  "mediaInfoAggregate": GameMediaAggregateOrderBy,
  "neutralSite": "ASC",
  "notes": "ASC",
  "season": "ASC",
  "seasonType": "ASC",
  "startDate": "ASC",
  "startTimeTbd": "ASC",
  "status": "ASC",
  "venueId": "ASC",
  "weather": GameWeatherOrderBy,
  "week": "ASC"
}
Types
gamePlayerStatAggregateBoolExpCount
Fields
Input Field	Description
arguments - [GamePlayerStatSelectColumn!]	
distinct - Boolean	
filter - GamePlayerStatBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["athleteId"],
  "distinct": false,
  "filter": GamePlayerStatBoolExp,
  "predicate": IntComparisonExp
}
Types
gameSelectColumn
Description
select columns of table "game_info"

Values
Enum Value	Description
attendance

column name
awayClassification

column name
awayConference

column name
awayConferenceId

column name
awayEndElo

column name
awayLineScores

column name
awayPoints

column name
awayPostgameWinProb

column name
awayStartElo

column name
awayTeam

column name
awayTeamId

column name
conferenceGame

column name
excitement

column name
homeClassification

column name
homeConference

column name
homeConferenceId

column name
homeEndElo

column name
homeLineScores

column name
homePoints

column name
homePostgameWinProb

column name
homeStartElo

column name
homeTeam

column name
homeTeamId

column name
id

column name
neutralSite

column name
notes

column name
season

column name
seasonType

column name
startDate

column name
startTimeTbd

column name
status

column name
venueId

column name
week

column name
Example
"attendance"
Types
gameStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 987.65,
  "awayConferenceId": 987.65,
  "awayEndElo": 987.65,
  "awayPoints": 987.65,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 123.45,
  "awayTeamId": 123.45,
  "excitement": 123.45,
  "homeConferenceId": 123.45,
  "homeEndElo": 987.65,
  "homePoints": 987.65,
  "homePostgameWinProb": 123.45,
  "homeStartElo": 987.65,
  "homeTeamId": 987.65,
  "id": 987.65,
  "season": 987.65,
  "venueId": 123.45,
  "week": 987.65
}
Types
gameStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 987.65,
  "awayConferenceId": 123.45,
  "awayEndElo": 987.65,
  "awayPoints": 123.45,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 123.45,
  "awayTeamId": 123.45,
  "excitement": 123.45,
  "homeConferenceId": 987.65,
  "homeEndElo": 123.45,
  "homePoints": 123.45,
  "homePostgameWinProb": 123.45,
  "homeStartElo": 123.45,
  "homeTeamId": 987.65,
  "id": 123.45,
  "season": 987.65,
  "venueId": 123.45,
  "week": 987.65
}
Types
gameStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 987.65,
  "awayConferenceId": 123.45,
  "awayEndElo": 987.65,
  "awayPoints": 123.45,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 987.65,
  "awayTeamId": 123.45,
  "excitement": 123.45,
  "homeConferenceId": 987.65,
  "homeEndElo": 123.45,
  "homePoints": 987.65,
  "homePostgameWinProb": 987.65,
  "homeStartElo": 987.65,
  "homeTeamId": 123.45,
  "id": 987.65,
  "season": 123.45,
  "venueId": 123.45,
  "week": 123.45
}
Types
gameSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
attendance - Int	
awayConferenceId - smallint	
awayEndElo - Int	
awayPoints - smallint	
awayPostgameWinProb - numeric	
awayStartElo - Int	
awayTeamId - Int	
excitement - numeric	
homeConferenceId - smallint	
homeEndElo - Int	
homePoints - smallint	
homePostgameWinProb - numeric	
homeStartElo - Int	
homeTeamId - Int	
id - Int	
season - smallint	
venueId - Int	
week - smallint	
Example
{
  "attendance": 987,
  "awayConferenceId": smallint,
  "awayEndElo": 123,
  "awayPoints": smallint,
  "awayPostgameWinProb": numeric,
  "awayStartElo": 987,
  "awayTeamId": 987,
  "excitement": numeric,
  "homeConferenceId": smallint,
  "homeEndElo": 987,
  "homePoints": smallint,
  "homePostgameWinProb": numeric,
  "homeStartElo": 987,
  "homeTeamId": 123,
  "id": 987,
  "season": smallint,
  "venueId": 123,
  "week": smallint
}
Types
gameVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 123.45,
  "awayConferenceId": 987.65,
  "awayEndElo": 123.45,
  "awayPoints": 123.45,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 123.45,
  "awayTeamId": 987.65,
  "excitement": 987.65,
  "homeConferenceId": 987.65,
  "homeEndElo": 123.45,
  "homePoints": 987.65,
  "homePostgameWinProb": 987.65,
  "homeStartElo": 987.65,
  "homeTeamId": 123.45,
  "id": 123.45,
  "season": 987.65,
  "venueId": 987.65,
  "week": 987.65
}
Types
gameVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 123.45,
  "awayConferenceId": 987.65,
  "awayEndElo": 987.65,
  "awayPoints": 987.65,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 987.65,
  "awayTeamId": 987.65,
  "excitement": 987.65,
  "homeConferenceId": 123.45,
  "homeEndElo": 123.45,
  "homePoints": 987.65,
  "homePostgameWinProb": 123.45,
  "homeStartElo": 123.45,
  "homeTeamId": 987.65,
  "id": 123.45,
  "season": 987.65,
  "venueId": 123.45,
  "week": 123.45
}
Types
gameVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
attendance - Float	
awayConferenceId - Float	
awayEndElo - Float	
awayPoints - Float	
awayPostgameWinProb - Float	
awayStartElo - Float	
awayTeamId - Float	
excitement - Float	
homeConferenceId - Float	
homeEndElo - Float	
homePoints - Float	
homePostgameWinProb - Float	
homeStartElo - Float	
homeTeamId - Float	
id - Float	
season - Float	
venueId - Float	
week - Float	
Example
{
  "attendance": 987.65,
  "awayConferenceId": 123.45,
  "awayEndElo": 123.45,
  "awayPoints": 123.45,
  "awayPostgameWinProb": 987.65,
  "awayStartElo": 123.45,
  "awayTeamId": 987.65,
  "excitement": 123.45,
  "homeConferenceId": 987.65,
  "homeEndElo": 123.45,
  "homePoints": 987.65,
  "homePostgameWinProb": 123.45,
  "homeStartElo": 123.45,
  "homeTeamId": 123.45,
  "id": 987.65,
  "season": 123.45,
  "venueId": 987.65,
  "week": 123.45
}
Types
game_status
Example
game_status
Types
historicalTeam
Description
columns and relationships of "team_info"

Fields
Field Name	Description
abbreviation - String	
active - Boolean	
altColor - String	
altName - String	
classification - division	
color - String	
conference - String	
conferenceAbbreviation - String	
conferenceId - smallint	
conferenceShortName - String	
countryCode - String	
displayName - String	
division - String	
endYear - smallint	
id - Int	
images - [String!]	
mascot - String	
ncaaName - String	
nickname - String	
school - String	
shortDisplayName - String	
startYear - smallint	
twitter - String	
Example
{
  "abbreviation": "xyz789",
  "active": true,
  "altColor": "xyz789",
  "altName": "abc123",
  "classification": division,
  "color": "abc123",
  "conference": "xyz789",
  "conferenceAbbreviation": "xyz789",
  "conferenceId": smallint,
  "conferenceShortName": "abc123",
  "countryCode": "xyz789",
  "displayName": "abc123",
  "division": "abc123",
  "endYear": smallint,
  "id": 987,
  "images": ["xyz789"],
  "mascot": "abc123",
  "ncaaName": "abc123",
  "nickname": "abc123",
  "school": "xyz789",
  "shortDisplayName": "xyz789",
  "startYear": smallint,
  "twitter": "abc123"
}
Types
historicalTeamAggregate
Description
aggregated selection of "team_info"

Fields
Field Name	Description
aggregate - historicalTeamAggregateFields	
nodes - [historicalTeam!]!	
Example
{
  "aggregate": historicalTeamAggregateFields,
  "nodes": [historicalTeam]
}
Types
historicalTeamAggregateFields
Description
aggregate fields of "team_info"

Fields
Field Name	Description
avg - historicalTeamAvgFields	
count - Int!	
Arguments
columns - [historicalTeamSelectColumn!]
distinct - Boolean
max - historicalTeamMaxFields	
min - historicalTeamMinFields	
stddev - historicalTeamStddevFields	
stddevPop - historicalTeamStddevPopFields	
stddevSamp - historicalTeamStddevSampFields	
sum - historicalTeamSumFields	
varPop - historicalTeamVarPopFields	
varSamp - historicalTeamVarSampFields	
variance - historicalTeamVarianceFields	
Example
{
  "avg": historicalTeamAvgFields,
  "count": 123,
  "max": historicalTeamMaxFields,
  "min": historicalTeamMinFields,
  "stddev": historicalTeamStddevFields,
  "stddevPop": historicalTeamStddevPopFields,
  "stddevSamp": historicalTeamStddevSampFields,
  "sum": historicalTeamSumFields,
  "varPop": historicalTeamVarPopFields,
  "varSamp": historicalTeamVarSampFields,
  "variance": historicalTeamVarianceFields
}
Types
historicalTeamAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 987.65, "endYear": 123.45, "id": 123.45, "startYear": 123.45}
Types
historicalTeamBoolExp
Description
Boolean expression to filter rows from the table "team_info". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [historicalTeamBoolExp!]	
_not - historicalTeamBoolExp	
_or - [historicalTeamBoolExp!]	
abbreviation - StringComparisonExp	
active - BooleanComparisonExp	
altColor - StringComparisonExp	
altName - StringComparisonExp	
classification - DivisionComparisonExp	
color - StringComparisonExp	
conference - StringComparisonExp	
conferenceAbbreviation - StringComparisonExp	
conferenceId - SmallintComparisonExp	
conferenceShortName - StringComparisonExp	
countryCode - StringComparisonExp	
displayName - StringComparisonExp	
division - StringComparisonExp	
endYear - SmallintComparisonExp	
id - IntComparisonExp	
images - StringArrayComparisonExp	
mascot - StringComparisonExp	
ncaaName - StringComparisonExp	
nickname - StringComparisonExp	
school - StringComparisonExp	
shortDisplayName - StringComparisonExp	
startYear - SmallintComparisonExp	
twitter - StringComparisonExp	
Example
{
  "_and": [historicalTeamBoolExp],
  "_not": historicalTeamBoolExp,
  "_or": [historicalTeamBoolExp],
  "abbreviation": StringComparisonExp,
  "active": BooleanComparisonExp,
  "altColor": StringComparisonExp,
  "altName": StringComparisonExp,
  "classification": DivisionComparisonExp,
  "color": StringComparisonExp,
  "conference": StringComparisonExp,
  "conferenceAbbreviation": StringComparisonExp,
  "conferenceId": SmallintComparisonExp,
  "conferenceShortName": StringComparisonExp,
  "countryCode": StringComparisonExp,
  "displayName": StringComparisonExp,
  "division": StringComparisonExp,
  "endYear": SmallintComparisonExp,
  "id": IntComparisonExp,
  "images": StringArrayComparisonExp,
  "mascot": StringComparisonExp,
  "ncaaName": StringComparisonExp,
  "nickname": StringComparisonExp,
  "school": StringComparisonExp,
  "shortDisplayName": StringComparisonExp,
  "startYear": SmallintComparisonExp,
  "twitter": StringComparisonExp
}
Types
historicalTeamMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
abbreviation - String	
altColor - String	
altName - String	
classification - division	
color - String	
conference - String	
conferenceAbbreviation - String	
conferenceId - smallint	
conferenceShortName - String	
countryCode - String	
displayName - String	
division - String	
endYear - smallint	
id - Int	
images - [String!]	
mascot - String	
ncaaName - String	
nickname - String	
school - String	
shortDisplayName - String	
startYear - smallint	
twitter - String	
Example
{
  "abbreviation": "xyz789",
  "altColor": "abc123",
  "altName": "abc123",
  "classification": division,
  "color": "xyz789",
  "conference": "abc123",
  "conferenceAbbreviation": "xyz789",
  "conferenceId": smallint,
  "conferenceShortName": "xyz789",
  "countryCode": "abc123",
  "displayName": "xyz789",
  "division": "abc123",
  "endYear": smallint,
  "id": 123,
  "images": ["xyz789"],
  "mascot": "abc123",
  "ncaaName": "xyz789",
  "nickname": "abc123",
  "school": "xyz789",
  "shortDisplayName": "abc123",
  "startYear": smallint,
  "twitter": "abc123"
}
Types
historicalTeamMinFields
Description
aggregate min on columns

Fields
Field Name	Description
abbreviation - String	
altColor - String	
altName - String	
classification - division	
color - String	
conference - String	
conferenceAbbreviation - String	
conferenceId - smallint	
conferenceShortName - String	
countryCode - String	
displayName - String	
division - String	
endYear - smallint	
id - Int	
images - [String!]	
mascot - String	
ncaaName - String	
nickname - String	
school - String	
shortDisplayName - String	
startYear - smallint	
twitter - String	
Example
{
  "abbreviation": "xyz789",
  "altColor": "xyz789",
  "altName": "abc123",
  "classification": division,
  "color": "xyz789",
  "conference": "abc123",
  "conferenceAbbreviation": "abc123",
  "conferenceId": smallint,
  "conferenceShortName": "abc123",
  "countryCode": "abc123",
  "displayName": "xyz789",
  "division": "xyz789",
  "endYear": smallint,
  "id": 123,
  "images": ["abc123"],
  "mascot": "abc123",
  "ncaaName": "abc123",
  "nickname": "xyz789",
  "school": "xyz789",
  "shortDisplayName": "abc123",
  "startYear": smallint,
  "twitter": "xyz789"
}
Types
historicalTeamOrderBy
Description
Ordering options when selecting data from "team_info".

Fields
Input Field	Description
abbreviation - OrderBy	
active - OrderBy	
altColor - OrderBy	
altName - OrderBy	
classification - OrderBy	
color - OrderBy	
conference - OrderBy	
conferenceAbbreviation - OrderBy	
conferenceId - OrderBy	
conferenceShortName - OrderBy	
countryCode - OrderBy	
displayName - OrderBy	
division - OrderBy	
endYear - OrderBy	
id - OrderBy	
images - OrderBy	
mascot - OrderBy	
ncaaName - OrderBy	
nickname - OrderBy	
school - OrderBy	
shortDisplayName - OrderBy	
startYear - OrderBy	
twitter - OrderBy	
Example
{
  "abbreviation": "ASC",
  "active": "ASC",
  "altColor": "ASC",
  "altName": "ASC",
  "classification": "ASC",
  "color": "ASC",
  "conference": "ASC",
  "conferenceAbbreviation": "ASC",
  "conferenceId": "ASC",
  "conferenceShortName": "ASC",
  "countryCode": "ASC",
  "displayName": "ASC",
  "division": "ASC",
  "endYear": "ASC",
  "id": "ASC",
  "images": "ASC",
  "mascot": "ASC",
  "ncaaName": "ASC",
  "nickname": "ASC",
  "school": "ASC",
  "shortDisplayName": "ASC",
  "startYear": "ASC",
  "twitter": "ASC"
}
Types
historicalTeamSelectColumn
Description
select columns of table "team_info"

Values
Enum Value	Description
abbreviation

column name
active

column name
altColor

column name
altName

column name
classification

column name
color

column name
conference

column name
conferenceAbbreviation

column name
conferenceId

column name
conferenceShortName

column name
countryCode

column name
displayName

column name
division

column name
endYear

column name
id

column name
images

column name
mascot

column name
ncaaName

column name
nickname

column name
school

column name
shortDisplayName

column name
startYear

column name
twitter

column name
Example
"abbreviation"
Types
historicalTeamStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 123.45, "endYear": 987.65, "id": 123.45, "startYear": 987.65}
Types
historicalTeamStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 987.65, "endYear": 123.45, "id": 123.45, "startYear": 987.65}
Types
historicalTeamStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 123.45, "endYear": 987.65, "id": 987.65, "startYear": 987.65}
Types
historicalTeamSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
conferenceId - smallint	
endYear - smallint	
id - Int	
startYear - smallint	
Example
{
  "conferenceId": smallint,
  "endYear": smallint,
  "id": 987,
  "startYear": smallint
}
Types
historicalTeamVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 987.65, "endYear": 123.45, "id": 987.65, "startYear": 987.65}
Types
historicalTeamVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 987.65, "endYear": 123.45, "id": 123.45, "startYear": 123.45}
Types
historicalTeamVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
conferenceId - Float	
endYear - Float	
id - Float	
startYear - Float	
Example
{"conferenceId": 123.45, "endYear": 123.45, "id": 987.65, "startYear": 123.45}
Types
home_away
Example
home_away
Types
media_type
Example
media_type
Types
numeric
Example
numeric
Types
player_adjusted_metric_type
Example
player_adjusted_metric_type
Types
predictedPoints
Description
columns and relationships of "ppa"

Fields
Field Name	Description
distance - smallint!	
down - smallint!	
predictedPoints - numeric!	
yardLine - smallint!	
Example
{
  "distance": smallint,
  "down": smallint,
  "predictedPoints": numeric,
  "yardLine": smallint
}
Types
predictedPointsAggregate
Description
aggregated selection of "ppa"

Fields
Field Name	Description
aggregate - predictedPointsAggregateFields	
nodes - [predictedPoints!]!	
Example
{
  "aggregate": predictedPointsAggregateFields,
  "nodes": [predictedPoints]
}
Types
predictedPointsAggregateFields
Description
aggregate fields of "ppa"

Fields
Field Name	Description
avg - predictedPointsAvgFields	
count - Int!	
Arguments
columns - [predictedPointsSelectColumn!]
distinct - Boolean
max - predictedPointsMaxFields	
min - predictedPointsMinFields	
stddev - predictedPointsStddevFields	
stddevPop - predictedPointsStddevPopFields	
stddevSamp - predictedPointsStddevSampFields	
sum - predictedPointsSumFields	
varPop - predictedPointsVarPopFields	
varSamp - predictedPointsVarSampFields	
variance - predictedPointsVarianceFields	
Example
{
  "avg": predictedPointsAvgFields,
  "count": 123,
  "max": predictedPointsMaxFields,
  "min": predictedPointsMinFields,
  "stddev": predictedPointsStddevFields,
  "stddevPop": predictedPointsStddevPopFields,
  "stddevSamp": predictedPointsStddevSampFields,
  "sum": predictedPointsSumFields,
  "varPop": predictedPointsVarPopFields,
  "varSamp": predictedPointsVarSampFields,
  "variance": predictedPointsVarianceFields
}
Types
predictedPointsAvgFields
Description
aggregate avg on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 987.65,
  "down": 987.65,
  "predictedPoints": 123.45,
  "yardLine": 123.45
}
Types
predictedPointsBoolExp
Description
Boolean expression to filter rows from the table "ppa". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [predictedPointsBoolExp!]	
_not - predictedPointsBoolExp	
_or - [predictedPointsBoolExp!]	
distance - SmallintComparisonExp	
down - SmallintComparisonExp	
predictedPoints - NumericComparisonExp	
yardLine - SmallintComparisonExp	
Example
{
  "_and": [predictedPointsBoolExp],
  "_not": predictedPointsBoolExp,
  "_or": [predictedPointsBoolExp],
  "distance": SmallintComparisonExp,
  "down": SmallintComparisonExp,
  "predictedPoints": NumericComparisonExp,
  "yardLine": SmallintComparisonExp
}
Types
predictedPointsMaxFields
Description
aggregate max on columns

Fields
Field Name	Description
distance - smallint	
down - smallint	
predictedPoints - numeric	
yardLine - smallint	
Example
{
  "distance": smallint,
  "down": smallint,
  "predictedPoints": numeric,
  "yardLine": smallint
}
Types
predictedPointsMinFields
Description
aggregate min on columns

Fields
Field Name	Description
distance - smallint	
down - smallint	
predictedPoints - numeric	
yardLine - smallint	
Example
{
  "distance": smallint,
  "down": smallint,
  "predictedPoints": numeric,
  "yardLine": smallint
}
Types
predictedPointsOrderBy
Description
Ordering options when selecting data from "ppa".

Fields
Input Field	Description
distance - OrderBy	
down - OrderBy	
predictedPoints - OrderBy	
yardLine - OrderBy	
Example
{"distance": "ASC", "down": "ASC", "predictedPoints": "ASC", "yardLine": "ASC"}
Types
predictedPointsSelectColumn
Description
select columns of table "ppa"

Values
Enum Value	Description
distance

column name
down

column name
predictedPoints

column name
yardLine

column name
Example
"distance"
Types
predictedPointsStddevFields
Description
aggregate stddev on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 123.45,
  "down": 123.45,
  "predictedPoints": 123.45,
  "yardLine": 987.65
}
Types
predictedPointsStddevPopFields
Description
aggregate stddevPop on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 987.65,
  "down": 987.65,
  "predictedPoints": 987.65,
  "yardLine": 123.45
}
Types
predictedPointsStddevSampFields
Description
aggregate stddevSamp on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 987.65,
  "down": 123.45,
  "predictedPoints": 123.45,
  "yardLine": 987.65
}
Types
predictedPointsSumFields
Description
aggregate sum on columns

Fields
Field Name	Description
distance - smallint	
down - smallint	
predictedPoints - numeric	
yardLine - smallint	
Example
{
  "distance": smallint,
  "down": smallint,
  "predictedPoints": numeric,
  "yardLine": smallint
}
Types
predictedPointsVarPopFields
Description
aggregate varPop on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 123.45,
  "down": 123.45,
  "predictedPoints": 123.45,
  "yardLine": 987.65
}
Types
predictedPointsVarSampFields
Description
aggregate varSamp on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 987.65,
  "down": 123.45,
  "predictedPoints": 123.45,
  "yardLine": 987.65
}
Types
predictedPointsVarianceFields
Description
aggregate variance on columns

Fields
Field Name	Description
distance - Float	
down - Float	
predictedPoints - Float	
yardLine - Float	
Example
{
  "distance": 123.45,
  "down": 987.65,
  "predictedPoints": 987.65,
  "yardLine": 123.45
}
Types
ratings
Description
columns and relationships of "rating_systems"

Fields
Field Name	Description
conference - String	
conferenceId - smallint	
elo - Int	
fpi - numeric	
fpiAvgWinProbabilityRank - smallint	
fpiDefensiveEfficiency - numeric	
fpiGameControlRank - smallint	
fpiOffensiveEfficiency - numeric	
fpiOverallEfficiency - numeric	
fpiRemainingSosRank - smallint	
fpiResumeRank - smallint	
fpiSosRank - smallint	
fpiSpecialTeamsEfficiency - numeric	
fpiStrengthOfRecordRank - smallint	
spDefense - numeric	
spOffense - numeric	
spOverall - numeric	
spSpecialTeams - numeric	
srs - numeric	
team - String	
teamId - Int	
year - smallint	
Example
{
  "conference": "abc123",
  "conferenceId": smallint,
  "elo": 987,
  "fpi": numeric,
  "fpiAvgWinProbabilityRank": smallint,
  "fpiDefensiveEfficiency": numeric,
  "fpiGameControlRank": smallint,
  "fpiOffensiveEfficiency": numeric,
  "fpiOverallEfficiency": numeric,
  "fpiRemainingSosRank": smallint,
  "fpiResumeRank": smallint,
  "fpiSosRank": smallint,
  "fpiSpecialTeamsEfficiency": numeric,
  "fpiStrengthOfRecordRank": smallint,
  "spDefense": numeric,
  "spOffense": numeric,
  "spOverall": numeric,
  "spSpecialTeams": numeric,
  "srs": numeric,
  "team": "abc123",
  "teamId": 987,
  "year": smallint
}
Types
ratingsBoolExp
Description
Boolean expression to filter rows from the table "rating_systems". All fields are combined with a logical 'AND'.

Fields
Input Field	Description
_and - [ratingsBoolExp!]	
_not - ratingsBoolExp	
_or - [ratingsBoolExp!]	
conference - StringComparisonExp	
conferenceId - SmallintComparisonExp	
elo - IntComparisonExp	
fpi - NumericComparisonExp	
fpiAvgWinProbabilityRank - SmallintComparisonExp	
fpiDefensiveEfficiency - NumericComparisonExp	
fpiGameControlRank - SmallintComparisonExp	
fpiOffensiveEfficiency - NumericComparisonExp	
fpiOverallEfficiency - NumericComparisonExp	
fpiRemainingSosRank - SmallintComparisonExp	
fpiResumeRank - SmallintComparisonExp	
fpiSosRank - SmallintComparisonExp	
fpiSpecialTeamsEfficiency - NumericComparisonExp	
fpiStrengthOfRecordRank - SmallintComparisonExp	
spDefense - NumericComparisonExp	
spOffense - NumericComparisonExp	
spOverall - NumericComparisonExp	
spSpecialTeams - NumericComparisonExp	
srs - NumericComparisonExp	
team - StringComparisonExp	
teamId - IntComparisonExp	
year - SmallintComparisonExp	
Example
{
  "_and": [ratingsBoolExp],
  "_not": ratingsBoolExp,
  "_or": [ratingsBoolExp],
  "conference": StringComparisonExp,
  "conferenceId": SmallintComparisonExp,
  "elo": IntComparisonExp,
  "fpi": NumericComparisonExp,
  "fpiAvgWinProbabilityRank": SmallintComparisonExp,
  "fpiDefensiveEfficiency": NumericComparisonExp,
  "fpiGameControlRank": SmallintComparisonExp,
  "fpiOffensiveEfficiency": NumericComparisonExp,
  "fpiOverallEfficiency": NumericComparisonExp,
  "fpiRemainingSosRank": SmallintComparisonExp,
  "fpiResumeRank": SmallintComparisonExp,
  "fpiSosRank": SmallintComparisonExp,
  "fpiSpecialTeamsEfficiency": NumericComparisonExp,
  "fpiStrengthOfRecordRank": SmallintComparisonExp,
  "spDefense": NumericComparisonExp,
  "spOffense": NumericComparisonExp,
  "spOverall": NumericComparisonExp,
  "spSpecialTeams": NumericComparisonExp,
  "srs": NumericComparisonExp,
  "team": StringComparisonExp,
  "teamId": IntComparisonExp,
  "year": SmallintComparisonExp
}
Types
ratingsOrderBy
Description
Ordering options when selecting data from "rating_systems".

Fields
Input Field	Description
conference - OrderBy	
conferenceId - OrderBy	
elo - OrderBy	
fpi - OrderBy	
fpiAvgWinProbabilityRank - OrderBy	
fpiDefensiveEfficiency - OrderBy	
fpiGameControlRank - OrderBy	
fpiOffensiveEfficiency - OrderBy	
fpiOverallEfficiency - OrderBy	
fpiRemainingSosRank - OrderBy	
fpiResumeRank - OrderBy	
fpiSosRank - OrderBy	
fpiSpecialTeamsEfficiency - OrderBy	
fpiStrengthOfRecordRank - OrderBy	
spDefense - OrderBy	
spOffense - OrderBy	
spOverall - OrderBy	
spSpecialTeams - OrderBy	
srs - OrderBy	
team - OrderBy	
teamId - OrderBy	
year - OrderBy	
Example
{
  "conference": "ASC",
  "conferenceId": "ASC",
  "elo": "ASC",
  "fpi": "ASC",
  "fpiAvgWinProbabilityRank": "ASC",
  "fpiDefensiveEfficiency": "ASC",
  "fpiGameControlRank": "ASC",
  "fpiOffensiveEfficiency": "ASC",
  "fpiOverallEfficiency": "ASC",
  "fpiRemainingSosRank": "ASC",
  "fpiResumeRank": "ASC",
  "fpiSosRank": "ASC",
  "fpiSpecialTeamsEfficiency": "ASC",
  "fpiStrengthOfRecordRank": "ASC",
  "spDefense": "ASC",
  "spOffense": "ASC",
  "spOverall": "ASC",
  "spSpecialTeams": "ASC",
  "srs": "ASC",
  "team": "ASC",
  "teamId": "ASC",
  "year": "ASC"
}
Types
ratingsSelectColumn
Description
select columns of table "rating_systems"

Values
Enum Value	Description
conference

column name
conferenceId

column name
elo

column name
fpi

column name
fpiAvgWinProbabilityRank

column name
fpiDefensiveEfficiency

column name
fpiGameControlRank

column name
fpiOffensiveEfficiency

column name
fpiOverallEfficiency

column name
fpiRemainingSosRank

column name
fpiResumeRank

column name
fpiSosRank

column name
fpiSpecialTeamsEfficiency

column name
fpiStrengthOfRecordRank

column name
spDefense

column name
spOffense

column name
spOverall

column name
spSpecialTeams

column name
srs

column name
team

column name
teamId

column name
year

column name
Example
"conference"
Types
recruitAggregateBoolExpCount
Fields
Input Field	Description
arguments - [RecruitSelectColumn!]	
distinct - Boolean	
filter - RecruitBoolExp	
predicate - IntComparisonExp!	
Example
{
  "arguments": ["height"],
  "distinct": true,
  "filter": RecruitBoolExp,
  "predicate": IntComparisonExp
}

---

## Tutorials & Resources

### Official Tutorials

1. **General GraphQL Tutorial**
   - Visit the [CFBD Blog](https://blog.collegefootballdata.com) for a comprehensive tutorial on using the GraphQL API
   - Learn query basics, filtering, and data retrieval patterns

2. **GraphQL Subscriptions Tutorial**
   - In-depth tutorial on real-time data updates
   - Available on the [CFBD Blog](https://blog.collegefootballdata.com)
   - Essential for live game tracking and real-time statistics

### Quick Start Guide

#### 1. Authentication Setup
```bash
# Set your API key as an environment variable
export CFBD_API_KEY="your_api_key_here"
```

#### 2. Basic Query Example
```graphql
query GetTeamStats {
  currentTeams(where: {school: {_eq: "Alabama"}}) {
    school
    conference
    division
    abbreviation
  }
}
```

#### 3. Using Headers
```http
POST https://graphql.collegefootballdata.com/v1/graphql
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Best Practices

1. **Pagination**: Always use `limit` and `offset` for large datasets
2. **Filtering**: Use `where` clauses to minimize data transfer
3. **Selective Fields**: Only request fields you need
4. **Aggregations**: Use aggregate queries for statistical summaries
5. **Caching**: Implement caching for frequently accessed data

### Common Use Cases

#### 1. Team Statistics Analysis
```graphql
query TeamStats($year: smallint!, $team: String!) {
  adjustedTeamMetrics(where: {year: {_eq: $year}, team: {school: {_eq: $team}}}) {
    epa
    explosiveness
    passingEpa
    rushingEpa
    success
  }
}
```

#### 2. Player Performance Tracking
```graphql
query PlayerMetrics($athleteId: bigint!) {
  adjustedPlayerMetrics(where: {athleteId: {_eq: $athleteId}}) {
    metricType
    metricValue
    year
    plays
  }
}
```

#### 3. Game Results and Betting Lines
```graphql
query GameData($season: smallint!, $week: smallint!) {
  game(where: {season: {_eq: $season}, week: {_eq: $week}}) {
    homeTeam
    awayTeam
    homePoints
    awayPoints
    gameLines {
      spread
      overUnder
      provider {
        name
      }
    }
  }
}
```

#### 4. Recruiting Rankings
```graphql
query RecruitingData($year: smallint!) {
  recruitingTeam(where: {year: {_eq: $year}}, orderBy: {rank: ASC}, limit: 25) {
    team
    rank
    points
  }
}
```

### Support & Community

- **API Support**: admin@collegefootballdata.com
- **Documentation**: https://collegefootballdata.com
- **Patreon**: https://patreon.com/collegefootballdata
- **Twitter**: Follow for updates and announcements

### Rate Limits & Guidelines

- Respect rate limits to ensure API availability for all users
- Cache responses when possible
- Use efficient queries with appropriate filters
- Report bugs or issues to the support team

---

## Additional Information

### Data Coverage

The GraphQL API provides access to:
- **Historical Data**: Complete historical records
- **Current Season**: Real-time updates during games
- **Player Stats**: Individual and aggregated metrics
- **Team Stats**: Offensive, defensive, and special teams
- **Recruiting**: Rankings and player commitments
- **Draft Data**: NFL Draft picks and positions
- **Betting Lines**: Multiple provider coverage
- **Advanced Metrics**: EPA, explosiveness, success rates

### API Status

For API status and uptime information, visit the CFBD website or contact support.

### Version Information

This documentation covers GraphQL API v1. Check the website for updates and new features.

---

**Last Updated:** October 2025  
**API Version:** v1  
**Documentation Version:** 1.0
Types
recruit_type
Example
recruit_type
Types
season_type
Example
season_type
Types
smallint
Example
smallint
Types
timestamp
Example
timestamp
Types
timestamptz
Example
timestamptz
Documentation by Anvil SpectaQL