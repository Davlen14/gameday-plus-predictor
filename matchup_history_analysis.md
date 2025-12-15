# College Football Matchup History Analysis

## API Endpoint Used
```bash
https://api.collegefootballdata.com/teams/matchup?team1={TEAM1}&team2={TEAM2}
```

---

## 🏈 Alabama vs Georgia

### Overall Series Record
- **Total Games**: 73 games (1902-2025)
- **Alabama Wins**: 45 (61.6%)
- **Georgia Wins**: 25 (34.2%)
- **Ties**: 3 (4.1%)

### Recent Dominance (2012-2025)
Alabama has won **9 of the last 10 meetings**, with Georgia's only win coming in the 2021 National Championship (33-18).

### Last 10 Matchups
| Season | Winner | Score | Location | Context |
|--------|--------|-------|----------|---------|
| 2025 | Alabama | 24-21 | @ Georgia | Regular Season Week 5 |
| 2024 | Alabama | 41-34 | @ Alabama | Regular Season Week 5 |
| 2023 | Alabama | 27-24 | Neutral (Mercedes-Benz) | SEC Championship |
| 2021 | **Georgia** | 33-18 | Neutral (Lucas Oil) | **National Championship** |
| 2021 | Alabama | 41-24 | Neutral (Mercedes-Benz) | SEC Championship |
| 2020 | Alabama | 41-24 | @ Alabama | Regular Season Week 7 |
| 2018 | Alabama | 35-28 | Neutral (Mercedes-Benz) | SEC Championship |
| 2017 | Alabama | 26-23 | Neutral (Mercedes-Benz) | **National Championship (OT)** |
| 2015 | Alabama | 38-10 | @ Georgia | Regular Season Week 5 |
| 2012 | Alabama | 32-28 | Neutral (Georgia Dome) | SEC Championship |

### Key Insights
- **Neutral Site Battles**: 6 of the last 10 meetings were at neutral sites (SEC Championships & Playoffs)
- **Close Games**: 4 games decided by 7 points or less
- **High Scoring**: Average combined score of 58.4 points in last 10 games
- **Championship Implications**: Most recent meetings have had major playoff/championship stakes

---

## 🌰 Ohio State vs Indiana

### Overall Series Record
- **Total Games**: 98 games (1901-2024)
- **Ohio State Wins**: 81 (82.7%)
- **Indiana Wins**: 12 (12.2%)
- **Ties**: 5 (5.1%)

### Dominance Pattern
Ohio State has won **28 consecutive games** (1991-2024) - one of the longest active winning streaks in FBS.

### Last 10 Matchups
| Season | Winner | Score | Location | Margin |
|--------|--------|-------|----------|--------|
| 2024 | Ohio State | 38-15 | @ Ohio State | 23 pts |
| 2023 | Ohio State | 23-3 | @ Indiana | 20 pts |
| 2022 | Ohio State | 56-14 | @ Ohio State | 42 pts |
| 2021 | Ohio State | 54-7 | @ Indiana | 47 pts |
| 2020 | Ohio State | 42-35 | @ Ohio State | 7 pts |
| 2019 | Ohio State | 51-10 | @ Indiana | 41 pts |
| 2018 | Ohio State | 49-26 | @ Ohio State | 23 pts |
| 2017 | Ohio State | 49-21 | @ Indiana | 28 pts |
| 2016 | Ohio State | 38-17 | @ Ohio State | 21 pts |
| 2015 | Ohio State | 34-27 | @ Indiana | 7 pts |

### Key Insights
- **Average Margin of Victory**: 27.9 points in last 10 games
- **Closest Game**: 2020 (42-35) - only single-digit margin in last decade
- **Indiana's Last Win**: 1988 (41-7 @ Indiana) - **37 years ago**
- **Alternating Venues**: Series alternates home/away each year (Big Ten scheduling)
- **2025 Matchup Context**: Indiana is 12-0 this year, best record in program history going into potential playoff game

---

## 🔍 API Response Structure

Both endpoints return:
```json
{
  "team1": "Team Name",
  "team2": "Team Name",
  "team1Wins": 45,
  "team2Wins": 25,
  "ties": 3,
  "games": [
    {
      "season": 2025,
      "week": 5,
      "seasonType": "regular|postseason",
      "date": "2025-09-27T23:30:00.000Z",
      "neutralSite": false,
      "venue": "Sanford Stadium",
      "homeTeam": "Georgia",
      "homeScore": 21,
      "awayTeam": "Alabama",
      "awayScore": 24,
      "winner": "Alabama"
    }
  ]
}
```

### Available Data Points
- ✅ Historical win/loss records
- ✅ Game-by-game results with scores
- ✅ Home/Away/Neutral site designation
- ✅ Specific venues (for modern games)
- ✅ Season type (regular vs postseason)
- ✅ Date/week information

### Potential Use Cases for Frontend
1. **Head-to-Head Widget**: Display series record before prediction
2. **Recent History Chart**: Show last 10 games with score differentials
3. **Historical Context**: Add "Last met: [date], [winner] won [score]"
4. **Streak Tracker**: "Ohio State has won 28 straight vs Indiana"
5. **Rivalry Intensity**: Calculate average margin, total meetings, etc.

---

## 📊 Comparison: Competitive Balance

| Metric | Alabama vs Georgia | Ohio State vs Indiana |
|--------|-------------------|---------------------|
| **Series Length** | 73 games (123 years) | 98 games (124 years) |
| **Dominant Team Win %** | 61.6% (Alabama) | 82.7% (Ohio State) |
| **Competitive Rating** | ⭐⭐⭐⭐ Highly Competitive | ⭐⭐ One-Sided |
| **Current Streak** | Alabama 9 of 10 | Ohio State 28 straight |
| **Avg Margin (Last 10)** | 11.3 points | 27.9 points |
| **Playoff Meetings** | Yes (2017, 2021) | No |
| **Championship Stakes** | Frequent | Rare |

