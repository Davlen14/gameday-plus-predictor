# College Football Data API - Successful cURL Commands Reference

> **Purpose**: Quick reference for working cURL commands to the CFBD API (both REST and GraphQL endpoints)

---

## 🔑 API Authentication

**API Key**: `T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p`

**Header Format**: 
```bash
-H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🎯 GraphQL Endpoint

**Base URL**: `https://graphql.collegefootballdata.com/v1/graphql`

**Content-Type**: `application/json`

### ✅ Fetch Week 15 Games (2025)

```bash
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"query { game(where: {season: {_eq: 2025}, week: {_eq: 15}}, limit: 10) { id season week seasonType homeTeam awayTeam homePoints awayPoints }}"}' \
  | python3 -m json.tool
```

**How It Works**:
- `POST` request to GraphQL endpoint
- Query uses `where` clause with `season: {_eq: 2025}` and `week: {_eq: 15}` filters
- `limit: 10` restricts results to 10 games
- Returns game data with team names, points, and metadata
- Pipe to `python3 -m json.tool` for pretty-printed JSON output

**Response Structure**:
```json
{
  "data": {
    "game": [
      {
        "id": 401777353,
        "season": 2025,
        "week": 15,
        "seasonType": "regular",
        "homeTeam": "Ohio State",
        "awayTeam": "Indiana",
        "homePoints": null,
        "awayPoints": null
      }
    ]
  }
}
```

---

## 🏈 REST API Endpoint

**Base URL**: `https://api.collegefootballdata.com`

### ✅ Fetch Week 15 Games (2025)

```bash
curl -s "https://api.collegefootballdata.com/games?year=2025&week=15&seasonType=regular" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  | python3 -m json.tool
```

**How It Works**:
- `GET` request to REST endpoint
- Query parameters: `year=2025`, `week=15`, `seasonType=regular`
- `-s` flag for silent mode (no progress bar)
- Returns comprehensive game data including venue, ELO ratings, conference info

**Response Structure**:
```json
[
  {
    "id": 401777353,
    "season": 2025,
    "week": 15,
    "seasonType": "regular",
    "startDate": "2025-12-07T01:00:00.000Z",
    "homeId": 194,
    "homeTeam": "Ohio State",
    "homeConference": "Big Ten",
    "homePoints": null,
    "awayId": 84,
    "awayTeam": "Indiana",
    "awayConference": "Big Ten",
    "awayPoints": null,
    "venue": "Lucas Oil Stadium",
    "homePregameElo": 2169,
    "awayPregameElo": 2191
  }
]
```

### ✅ Fetch AP Poll Rankings (2025)

```bash
curl -s "https://api.collegefootballdata.com/rankings?year=2025&seasonType=regular" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  | python3 -m json.tool
```

**How It Works**:
- `GET` request to `/rankings` endpoint
- Query parameters: `year=2025`, `seasonType=regular`
- Returns all polls (AP Top 25, Coaches Poll, Playoff Committee Rankings) for all weeks
- Data includes rankings by week with team names, conferences, votes, and points

**Response Structure**:
```json
[
  {
    "season": 2025,
    "seasonType": "regular",
    "week": 15,
    "polls": [
      {
        "poll": "AP Top 25",
        "ranks": [
          {
            "rank": 1,
            "teamId": 194,
            "school": "Ohio State",
            "conference": "Big Ten",
            "firstPlaceVotes": 61,
            "points": 1645
          }
        ]
      }
    ]
  }
]
```

### ✅ Fetch Weather Data for Games (GraphQL)

```bash
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"query { game(where: {season: {_eq: 2025}, week: {_eq: 15}}, limit: 5) { id homeTeam awayTeam weather { temperature humidity precipitation windSpeed windDirection } }}"}' \
  | python3 -m json.tool
```

**How It Works**:
- GraphQL query includes nested `weather` object within game query
- Weather fields available:
  - `temperature`: Temperature in Fahrenheit
  - `humidity`: Humidity percentage (0-100)
  - `precipitation`: Precipitation amount
  - `windSpeed`: Wind speed in mph
  - `windDirection`: Wind direction in degrees (0-360)
- Not all games have weather data (returns `null` for games without weather)
- Weather data is more commonly available for FBS games

**Response Structure**:
```json
{
  "data": {
    "game": [
      {
        "id": 401777350,
        "homeTeam": "Jackson State",
        "awayTeam": "Prairie View A&M",
        "weather": {
          "temperature": 55.8,
          "humidity": 60.0,
          "precipitation": 0.0,
          "windSpeed": 9.2,
          "windDirection": 294.0
        }
      }
    ]
  }
}
```

**Note**: There is NO `dewPoint` field - attempting to query it will cause a validation error.

---

## 🔧 Key Differences: REST vs GraphQL

| Feature | REST API | GraphQL API |
|---------|----------|-------------|
| **URL** | `https://api.collegefootballdata.com` | `https://graphql.collegefootballdata.com/v1/graphql` |
| **Method** | GET | POST |
| **Query Style** | URL parameters | JSON body with query string |
| **Filtering** | `?year=2025&week=15` | `where: {season: {_eq: 2025}, week: {_eq: 15}}` |
| **Field Selection** | Returns all fields | Select specific fields in query |
| **Data Structure** | Array of objects | `{ data: { table: [...] } }` |

---

## 💡 Common Issues & Solutions

### ❌ Wrong GraphQL URL
**Problem**: Using `https://api.collegefootballdata.com/graphql` or `https://graph.collegefootballdata.com/graphql`
**Solution**: Use `https://graphql.collegefootballdata.com/v1/graphql`

### ❌ Missing Authorization Header
**Problem**: 403 Forbidden or HTML response (Swagger UI)
**Solution**: Always include `-H "Authorization: Bearer YOUR_API_KEY"`

### ❌ Wrong Year/Week Types
**Problem**: GraphQL errors about type mismatch
**Solution**: 
- Use `smallint` for years/weeks: `{_eq: 2025}` not `{_eq: "2025"}`
- REST API uses query params: `year=2025` (as string in URL)

### ❌ Field Name Errors
**Problem**: "field 'X' not found in type"
**Solution**: Check `College_Football_Data_GraphQL_Schema.md` for correct field names
- Example: Use `homeStartElo` not `homeElo`
- Example: Use `homePostgameWinProb` not `homePostgameWinProbability`

---

## 📚 Quick Reference

**Always use**:
- ✅ `https://graphql.collegefootballdata.com/v1/graphql` for GraphQL
- ✅ `https://api.collegefootballdata.com` for REST
- ✅ `Authorization: Bearer` header with API key
- ✅ `python3 -m json.tool` for readable output

**Never use**:
- ❌ `https://api.collegefootballdata.com/graphql` (doesn't exist)
- ❌ `https://graph.collegefootballdata.com` (wrong domain)
- ❌ Environment variables like `${CFBD_API_KEY}` (use actual key)

---

*Last Updated: December 1, 2025*
