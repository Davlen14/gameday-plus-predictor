# 🔧 n8n GraphQL Workflow Configuration Guide

> **For Gameday+ n8n workflow at:** `https://gamedayplus.app.n8n.cloud/`  
> **Issue:** The n8n AI assistant incorrectly suggested using REST API instead of GraphQL  
> **Reality:** College Football Data API DOES have a GraphQL endpoint at `https://graphql.collegefootballdata.com/v1/graphql`

---

## ✅ Correct GraphQL Configuration

### **GraphQL Endpoint Details**

```
URL: https://graphql.collegefootballdata.com/v1/graphql
Method: POST
Content-Type: application/json
Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p
```

### **n8n HTTP Request Node Configuration**

For each GraphQL query node in your n8n workflow:

1. **Node Type:** HTTP Request (NOT "GraphQL Request" node)
2. **Method:** POST
3. **URL:** `https://graphql.collegefootballdata.com/v1/graphql`
4. **Authentication:** None (use headers instead)
5. **Headers:**
   ```json
   {
     "Content-Type": "application/json",
     "Authorization": "Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
   }
   ```
6. **Body:**
   ```json
   {
     "query": "YOUR_GRAPHQL_QUERY_HERE",
     "variables": {
       "homeTeamId": {{ $json.home_team_id }},
       "awayTeamId": {{ $json.away_team_id }},
       "currentYear": 2025,
       "currentWeek": 12
     }
   }
   ```

---

## 📋 Complete GraphQL Query (From graphqlpredictor.py)

Use this exact query in your n8n workflow - it's the full production query from `graphqlpredictor.py`:

```graphql
query GamePredictorEnhanced($homeTeamId: Int!, $awayTeamId: Int!, $currentYear: smallint = 2025, $currentYearInt: Int = 2025, $currentWeek: smallint = 12) {
    # Current season team metrics
    homeTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $homeTeamId}, year: {_eq: $currentYear}}) {
        epa epaAllowed explosiveness explosivenessAllowed success successAllowed
        passingEpa passingEpaAllowed rushingEpa rushingEpaAllowed
        passingDownsSuccess passingDownsSuccessAllowed
        standardDownsSuccess standardDownsSuccessAllowed
        lineYards lineYardsAllowed secondLevelYards secondLevelYardsAllowed
        openFieldYards openFieldYardsAllowed highlightYards highlightYardsAllowed
    }
    awayTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $awayTeamId}, year: {_eq: $currentYear}}) {
        epa epaAllowed explosiveness explosivenessAllowed success successAllowed
        passingEpa passingEpaAllowed rushingEpa rushingEpaAllowed
        passingDownsSuccess passingDownsSuccessAllowed
        standardDownsSuccess standardDownsSuccessAllowed
        lineYards lineYardsAllowed secondLevelYards secondLevelYardsAllowed
        openFieldYards openFieldYardsAllowed highlightYards highlightYardsAllowed
    }
    
    # Player metrics
    allPlayers: adjustedPlayerMetrics(
        where: {
            year: {_eq: $currentYear}
        },
        orderBy: {metricValue: DESC},
        limit: 100
    ) {
        athleteId
        metricType
        metricValue
        plays
        athlete {
            name
        }
    }
    
    # Team talent ratings
    homeTeamTalent: teamTalent(where: {team: {teamId: {_eq: $homeTeamId}}, year: {_eq: $currentYear}}) {
        talent
    }
    awayTeamTalent: teamTalent(where: {team: {teamId: {_eq: $awayTeamId}}, year: {_eq: $currentYear}}) {
        talent
    }
    
    # Season games
    homeSeasonGames: game(where: {_or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}], season: {_eq: $currentYear}}, orderBy: {week: ASC}) {
        id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
    }
    awaySeasonGames: game(where: {_or: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $awayTeamId}}], season: {_eq: $currentYear}}, orderBy: {week: ASC}) {
        id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
    }
    
    # Recent form (last 4 games)
    homeRecentGames: game(where: {_or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}], season: {_eq: $currentYear}}, orderBy: {startDate: DESC}, limit: 4) {
        id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
    }
    awayRecentGames: game(where: {_or: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $awayTeamId}}], season: {_eq: $currentYear}}, orderBy: {startDate: DESC}, limit: 4) {
        id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
    }
    
    # Team information
    homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}}) {
        school conference
    }
    awayTeam: currentTeams(where: {teamId: {_eq: $awayTeamId}}) {
        school conference
    }
    
    # Ratings
    homeRatings: ratings(where: {teamId: {_eq: $homeTeamId}, year: {_eq: $currentYear}}) {
        teamId year elo fpi conference team
    }
    awayRatings: ratings(where: {teamId: {_eq: $awayTeamId}, year: {_eq: $currentYear}}) {
        teamId year elo fpi conference team
    }
    
    # Current game data
    currentGame: game(where: {
        _or: [
            {_and: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $awayTeamId}}]},
            {_and: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $homeTeamId}}]}
        ],
        season: {_eq: $currentYear},
        week: {_eq: $currentWeek}
    }) {
        id week startDate venue
        homeTeam awayTeam homeTeamId awayTeamId
        homeStartElo awayStartElo
        weather {
            temperature windSpeed precipitation
        }
        lines {
            provider spread formattedSpread overUnder
        }
        mediaInfo {
            mediaType name
        }
    }
    
    # Coaching records vs ranked opponents
    homeCoaching: coach(where: {seasons: {_contains: [{year: $currentYear, schoolId: $homeTeamId}]}}) {
        firstName lastName
        seasons
    }
    awayCoaching: coach(where: {seasons: {_contains: [{year: $currentYear, schoolId: $awayTeamId}]}}) {
        firstName lastName
        seasons
    }
}
```

---

## 🔍 Simplified Test Query

If the full query is overwhelming, start with this simplified test:

```graphql
query TestQuery($homeTeamId: Int!, $awayTeamId: Int!) {
    homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}}) {
        school conference
    }
    awayTeam: currentTeams(where: {teamId: {_eq: $awayTeamId}}) {
        school conference
    }
    homeTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $homeTeamId}, year: {_eq: 2025}}) {
        epa
        success
    }
}
```

**Test with:**
- `homeTeamId: 194` (Ohio State)
- `awayTeamId: 130` (Michigan)

---

## 🎯 n8n Workflow Architecture

### **Recommended Node Structure:**

```
1. Webhook Node
   ↓
2. Code Node: "Convert Team Names to IDs"
   - Input: {home_team: "Ohio State", away_team: "Michigan"}
   - Output: {home_team_id: 194, away_team_id: 130}
   ↓
3. HTTP Request: "GraphQL Query"
   - URL: https://graphql.collegefootballdata.com/v1/graphql
   - Method: POST
   - Body: {query: "...", variables: {...}}
   ↓
4. Code Node: "Process GraphQL Response"
   - Parse response.data
   - Format for Flask API structure
   ↓
5. HTTP Response: "Return to Flask"
```

---

## 📊 Team Name → ID Conversion

Your n8n workflow needs to convert team names to IDs. Use this lookup table (from `fbs.json`):

```javascript
// Code Node: Convert Team Names to IDs
const teamLookup = {
  "Alabama": 333,
  "Ohio State": 194,
  "Michigan": 130,
  "Georgia": 61,
  "Texas": 251,
  "Penn State": 213,
  "Oregon": 2483,
  "Notre Dame": 87,
  "Miami": 2390,
  "Ole Miss": 145,
  // ... see fbs.json for complete list
};

const homeTeamName = $input.first().json.home_team;
const awayTeamName = $input.first().json.away_team;

return [{
  json: {
    home_team: homeTeamName,
    away_team: awayTeamName,
    home_team_id: teamLookup[homeTeamName],
    away_team_id: teamLookup[awayTeamName]
  }
}];
```

**Better approach:** Fetch from GitHub:

```javascript
// HTTP Request Node to get team lookup
// URL: https://raw.githubusercontent.com/Davlen14/gameday-plus-predictor/main/fbs.json
// Then use Code node to search by school name
```

---

## 🐛 Common Issues & Solutions

### **Issue 1: "Resource not found" Error**

**Cause:** Using wrong URL or missing authentication  
**Solution:** 
```
✅ Correct URL: https://graphql.collegefootballdata.com/v1/graphql
❌ Wrong URL: https://api.collegefootballdata.com/graphql
```

### **Issue 2: Empty Team Names**

**Cause:** Incorrect variable access in n8n  
**Solution:**
```javascript
// If data comes from webhook body:
const homeTeam = $input.first().json.body.home_team;

// If data comes from previous node:
const homeTeam = $node["Previous Node"].json.home_team;

// If data is in current item:
const homeTeam = $json.home_team;
```

### **Issue 3: Authentication Failed**

**Cause:** API key not in headers  
**Solution:**
```json
{
  "Authorization": "Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
}
```

**Note:** Store API key in n8n credentials, not hardcoded!

### **Issue 4: Query Syntax Error**

**Cause:** Missing variables or wrong GraphQL syntax  
**Solution:**
- Test query in GraphQL Playground first: https://graphql.collegefootballdata.com/v1/graphql
- Ensure variables match query definition
- Check for typos in field names

---

## 🚀 Quick Setup Steps

1. **Create HTTP Request Node**
   - Name: "GraphQL Team Data Query"
   - Method: POST
   - URL: `https://graphql.collegefootballdata.com/v1/graphql`

2. **Add Headers**
   ```
   Content-Type: application/json
   Authorization: Bearer {{$credentials.collegefootballdata.apiKey}}
   ```

3. **Set Body (JSON)**
   ```json
   {
     "query": "query TestQuery($homeTeamId: Int!, $awayTeamId: Int!) { homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}}) { school conference } }",
     "variables": {
       "homeTeamId": {{ $json.home_team_id }},
       "awayTeamId": {{ $json.away_team_id }}
     }
   }
   ```

4. **Test with Sample Data**
   ```json
   {
     "home_team_id": 194,
     "away_team_id": 130
   }
   ```

5. **Check Response**
   - Should return: `response.data.homeTeam[0].school = "Ohio State"`

---

## 📖 Additional Resources

- **GraphQL Schema Explorer:** https://graphql.collegefootballdata.com/v1/graphql
- **Your Production Query:** `graphqlpredictor.py` lines 2669-2847
- **Team ID Lookup:** `fbs.json` in repository
- **n8n GraphQL Guide:** https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/

---

## 💡 Pro Tips

1. **Use n8n Credentials Manager** - Don't hardcode API key
2. **Test incrementally** - Start with simple query, add complexity
3. **Use Code nodes** for data transformation between steps
4. **Enable error workflows** - Get notified when queries fail
5. **Log responses** - Add debug Code nodes to inspect GraphQL responses

---

## ✅ Validation Checklist

Before running your workflow:

- [ ] GraphQL endpoint URL is correct
- [ ] Authorization header includes API key
- [ ] Content-Type is `application/json`
- [ ] Query syntax is valid (test in GraphQL Playground)
- [ ] Variables match query parameters
- [ ] Team IDs are integers, not strings
- [ ] Response handling code can parse GraphQL response format

---

**Last Updated:** December 2, 2025  
**Status:** GraphQL API is ACTIVE and WORKING  
**Common Misconception:** The AI suggesting REST API is incorrect - use GraphQL!

