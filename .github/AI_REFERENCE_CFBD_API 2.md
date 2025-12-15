# 🛡️ BULLETPROOF AI AGENT REFERENCE - College Football Data API

> **⚠️ MANDATORY**: AI agents MUST read this ENTIRE document before EVERY API call. This is the SINGLE SOURCE OF TRUTH for CFBD API interactions.

---

## 🎯 CURRENT CONTEXT (ALWAYS CHECK FIRST)

```yaml
CURRENT_YEAR: 2025
CURRENT_WEEK: 15
SEASON_TYPE: "regular"
API_STATUS: ✅ VERIFIED WORKING (Last tested: 2025-12-01)
```

**🚨 CRITICAL**: These values change weekly. Before using ANY hardcoded week number, verify it's still current.

---

## ⚠️ COMMON MISTAKES TO AVOID

### ❌ WRONG - Don't Use These URLs
```bash
# THESE WILL FAIL:
https://api.collegefootballdata.com/graphql
https://graph.collegefootballdata.com/graphql
https://api.collegefootballdata.com/graphql/v1
${CFBD_API_KEY}  # Don't use environment variables
"Bearer ${API_KEY}"  # Don't use template literals
```

### ✅ CORRECT - Always Use These
```bash
# GraphQL Endpoint:
https://graphql.collegefootballdata.com/v1/graphql

# REST API Base:
https://api.collegefootballdata.com

# API Key (hardcoded - use EXACTLY as shown):
T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p

# Full Authorization Header:
Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p
```

---

## 🎯 QUICK REFERENCE - WORKING COMMANDS

### 1️⃣ Fetch Games (GraphQL) - RECOMMENDED

```bash
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"query { game(where: {season: {_eq: 2025}, week: {_eq: 15}}, limit: 10) { id season week seasonType homeTeam awayTeam homePoints awayPoints }}"}' \
  | python3 -m json.tool
```

**📌 Key Points**:
- Method: **`POST`** (NOT GET!)
- Endpoint: `https://graphql.collegefootballdata.com/v1/graphql`
- Content-Type: **`application/json`** (REQUIRED)
- Filter syntax: `where: {season: {_eq: 2025}, week: {_eq: 15}}`
- **ALWAYS** include `Authorization: Bearer` header
- Use **raw integers** for numbers: `{_eq: 2025}` NOT `{_eq: "2025"}`

**🔍 Expected Output**:
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

### 2️⃣ Fetch Weather Data (GraphQL)

```bash
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"query { game(where: {season: {_eq: 2025}, week: {_eq: 15}}, limit: 5) { id homeTeam awayTeam weather { temperature humidity precipitation windSpeed windDirection } }}"}' \
  | python3 -m json.tool
```

**📌 Available Weather Fields**:
- ✅ `temperature` → Fahrenheit (Integer)
- ✅ `humidity` → Percentage (Integer)
- ✅ `precipitation` → Inches (Float/null)
- ✅ `windSpeed` → MPH (Integer)
- ✅ `windDirection` → Degrees 0-360 (Integer)

**🚨 DOES NOT EXIST**:
- ❌ `dewPoint` → Will cause GraphQL error!
- ❌ `feelsLike` → Not in schema
- ❌ `visibility` → Not available

**⚠️ Important Notes**:
- Not all games have weather data (outdoor stadiums only)
- `null` values are normal for indoor games
- Weather data may not be available until game day

**🔍 Expected Output**:
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

---

### 3️⃣ Fetch Games (REST API) - ALTERNATIVE

```bash
curl -s "https://api.collegefootballdata.com/games?year=2025&week=15&seasonType=regular" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  | python3 -m json.tool
```

**📌 Key Points**:
- Method: **`GET`** (different from GraphQL!)
- Endpoint: `https://api.collegefootballdata.com/games`
- Query params: `?year=2025&week=15&seasonType=regular`
- Returns **MORE fields** than GraphQL (venue, ELO, excitement, etc.)
- **Use when**: You need complete game data or testing quickly

**🔍 Expected Output**:
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

---

### 4️⃣ Fetch Rankings/AP Poll (REST API)

```bash
curl -s "https://api.collegefootballdata.com/rankings?year=2025&seasonType=regular" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  | python3 -m json.tool
```

**📌 Key Points**:
- Returns **ALL weeks** of rankings for the season
- Includes multiple polls: AP Top 25, Coaches Poll, Playoff Committee
- **Filter by week** in your application code if needed
- **No GraphQL endpoint for rankings** - must use REST

**🔍 Expected Output**:
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

---

## 📋 GRAPHQL SYNTAX RULES

### Filter Operators (Hasura-style)
```graphql
where: {
  season: {_eq: 2025}         # ✅ Equal to
  week: {_eq: 15}             # ✅ Equal to
  homeTeamId: {_eq: 194}      # ✅ Equal to (use Int for IDs)
  homeTeam: {_ilike: "%Ohio%"} # ✅ Case-insensitive search
  homePoints: {_gt: 30}       # ✅ Greater than
  homePoints: {_gte: 30}      # ✅ Greater than or equal
  week: {_in: [14, 15, 16]}   # ✅ In array
}
```

### Type Requirements (CRITICAL)
| Field Type | Correct Format | ❌ Wrong Format |
|-----------|----------------|----------------|
| Years/Weeks | `{_eq: 2025}` | `{_eq: "2025"}` |
| Team IDs | `{_eq: 194}` | `{_eq: "194"}` |
| Points/Scores | `{_gt: 30}` | `{_gt: "30"}` |
| Team Names | `"Ohio State"` | `Ohio State` |
| Season Type | `"regular"` | `regular` |

**🚨 CRITICAL**: GraphQL will **silently return no results** if you use string `"2025"` instead of integer `2025`

---

### Nested Objects (Available Fields)
```graphql
game {
  id
  season
  week
  homeTeam
  awayTeam
  
  # Nested Weather Object
  weather {
    temperature       # ✅ Available
    humidity          # ✅ Available
    precipitation     # ✅ Available
    windSpeed         # ✅ Available
    windDirection     # ✅ Available
    # dewPoint        # ❌ DOES NOT EXIST
  }
  
  # Nested Betting Object
  betting {
    spread            # ✅ Available
    overUnder         # ✅ Available
    homeMoneyline     # ✅ Available
    awayMoneyline     # ✅ Available
  }
}
```

---

### Query Modifiers
```graphql
game(
  where: {season: {_eq: 2025}}
  limit: 10              # ✅ Limit results
  offset: 20             # ✅ Skip first 20 (pagination)
  order_by: {week: asc}  # ✅ Sort by week ascending
) {
  id
  homeTeam
}
```

---

## 🔑 AUTHENTICATION

### ✅ CORRECT Format
```bash
# Full Header (copy-paste exactly):
-H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# Python requests:
headers = {
    "Authorization": "Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p",
    "Content-Type": "application/json"
}

# JavaScript fetch:
headers: {
  'Authorization': 'Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p',
  'Content-Type': 'application/json'
}
```

### ❌ WRONG Formats (DO NOT USE)
```bash
# Missing "Bearer" prefix:
-H "Authorization: T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# Using environment variable:
-H "Authorization: Bearer ${CFBD_API_KEY}"

# Using template literal:
-H "Authorization: Bearer `${process.env.API_KEY}`"

# No Authorization header at all (will return HTML/Swagger UI)
```

---

## 🚨 ERROR DEBUGGING FLOWCHART

### Error: "HTML Response / Swagger UI / JSON Parse Error"

**Problem**: Wrong endpoint or missing authentication

**Debug Steps**:
1. ✅ Check URL is **exactly**: `https://graphql.collegefootballdata.com/v1/graphql`
2. ✅ Verify `Authorization: Bearer` header is present
3. ✅ Confirm API key has no extra spaces or line breaks
4. ✅ Ensure `Content-Type: application/json` header exists

**Solution**:
```bash
# ✅ CORRECT:
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"..."}'
```

---

### Error: "field 'X' not found in type 'game'"

**Problem**: Field doesn't exist in GraphQL schema

**Debug Steps**:
1. ✅ Check `College_Football_Data_GraphQL_Schema.md` for correct field names
2. ✅ Common mistakes:
   - ❌ `dewPoint` → Does not exist in weather
   - ❌ `team_id` → Use `homeTeamId` (camelCase)
   - ❌ `season_type` → Use `seasonType` (camelCase)

**Solution**: Use exact field names from schema documentation

---

### Error: "Expecting value: line 1 column 1"

**Problem**: API returned HTML instead of JSON (authentication/endpoint issue)

**Debug Steps**:
1. ✅ Verify GraphQL endpoint ends with `/v1/graphql`
2. ✅ Check `Authorization` header is included
3. ✅ Confirm you're using `POST` method (not `GET`)
4. ✅ Ensure `-d` data payload is valid JSON

**Test Command**:
```bash
# This should return JSON (not HTML):
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { game(limit: 1) { id } }"}'
```

---

### Error: Empty Results `{"data": {"game": []}}`

**Problem**: No data matches your filters (not an error!)

**Debug Steps**:
1. ✅ Check if games exist for that year/week/season
2. ✅ Verify you're using integers: `{_eq: 2025}` NOT `{_eq: "2025"}`
3. ✅ Try broader query (remove filters one by one)
4. ✅ Test with known working values: `season: 2024, week: 1`

**Test Query**:
```bash
# Remove all filters to see if ANY data returns:
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { game(limit: 5) { id season week homeTeam awayTeam } }"}' \
  | python3 -m json.tool
```

---

### Error: GraphQL Validation Error

**Problem**: Syntax error in GraphQL query

**Common Issues**:
- Missing commas between fields
- Unmatched braces `{ }`
- Wrong filter syntax
- Typos in field names

**Solution Template**:
```graphql
query {
  game(
    where: {season: {_eq: 2025}, week: {_eq: 15}}
    limit: 10
  ) {
    id
    season
    week
    homeTeam
    awayTeam
  }
}
```

---

## 💡 DECISION TREE: WHEN TO USE WHICH API

```
Need College Football Data?
│
├─ Need Rankings/Polls?
│  └─ ✅ Use REST API `/rankings`
│     (GraphQL doesn't support rankings)
│
├─ Need COMPLETE game data (venue, ELO, excitement)?
│  └─ ✅ Use REST API `/games`
│     (Returns all fields by default)
│
├─ Need SPECIFIC fields only (optimize payload)?
│  └─ ✅ Use GraphQL
│     (Select only what you need)
│
├─ Already using GraphQL elsewhere in project?
│  └─ ✅ Use GraphQL
│     (Maintain consistency)
│
└─ Quick terminal testing?
   └─ ✅ Use REST API
      (Simpler GET request)
```

---

### Use GraphQL When:
- ✅ You need **specific fields only** (reduces payload size)
- ✅ Working with the **prediction engine** (already uses GraphQL)
- ✅ Need **nested data** (weather, betting lines, team stats)
- ✅ Want to **avoid over-fetching** (mobile/bandwidth concerns)
- ✅ Building a **complex query** with multiple filters

**Example Use Case**: Fetching games with weather for a prediction model
```graphql
game(where: {season: {_eq: 2025}, week: {_eq: 15}}) {
  homeTeam
  awayTeam
  weather { temperature windSpeed }
  betting { spread }
}
```

---

### Use REST API When:
- ✅ Need **complete game data** with all fields
- ✅ Fetching **rankings/polls** (GraphQL doesn't support this)
- ✅ **Quick testing** in terminal (`curl` with query params)
- ✅ **Simpler query requirements** (no nested data needed)
- ✅ Want **predictable response format** (always same structure)

**Example Use Case**: Getting all game details for display
```bash
curl "https://api.collegefootballdata.com/games?year=2025&week=15"
```

---

## 📚 RELATED DOCUMENTATION

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `College_Football_Data_GraphQL_Schema.md` | Complete GraphQL schema reference | When you need to check available fields |
| `CFBD_API_CURL_COMMANDS.md` | Detailed command examples | When building new queries |
| `graphqlpredictor.py` (line 49) | Shows correct endpoint in code | When debugging existing Python code |

---

## ✅ PRE-FLIGHT CHECKLIST (MANDATORY)

**Before making ANY API call, verify:**

- [ ] **Using correct endpoint URL**
  - GraphQL: `https://graphql.collegefootballdata.com/v1/graphql`
  - REST: `https://api.collegefootballdata.com`

- [ ] **Using correct API key directly** (not environment variable)
  - `T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p`

- [ ] **Including Authorization header**
  - `Authorization: Bearer <API_KEY>`

- [ ] **Using correct HTTP method**
  - GraphQL: `POST`
  - REST: `GET`

- [ ] **Using correct Content-Type** (GraphQL only)
  - `Content-Type: application/json`

- [ ] **Using correct data types**
  - Integers: `{_eq: 2025}` NOT `{_eq: "2025"}`
  - Strings: `"regular"` NOT `regular`

- [ ] **Using correct field names** (check schema if unsure)
  - ✅ `homeTeam` NOT `home_team`
  - ✅ `seasonType` NOT `season_type`

- [ ] **Piping to json formatter** (for readability)
  - `| python3 -m json.tool`

---

## 🧪 VALIDATION TEST (RUN THIS FIRST)

**Copy-paste this command to verify API access:**

```bash
curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  -d '{"query":"query { game(limit: 1) { id season week homeTeam awayTeam } }"}' \
  | python3 -m json.tool
```

**✅ Expected Success Output:**
```json
{
  "data": {
    "game": [
      {
        "id": 401234567,
        "season": 2025,
        "week": 15,
        "homeTeam": "Some Team",
        "awayTeam": "Another Team"
      }
    ]
  }
}
```

**❌ If you see HTML/Swagger UI**: Authentication or endpoint issue (re-read Authentication section)

**❌ If you see `"errors": [...]`**: GraphQL syntax error (check query format)

**❌ If you see `curl: command not found`**: Use Git Bash or WSL on Windows

---

## 🎓 AI AGENT LEARNING SECTION

### Why AI Agents Fail With This API:

1. **❌ Using outdated patterns from training data**
   - AI was trained on generic API examples
   - CFBD uses Hasura GraphQL syntax (not standard)

2. **❌ Forgetting project-specific details**
   - Loses context about which year/week is current
   - Forgets custom authentication method

3. **❌ Mixing REST and GraphQL syntax**
   - Tries to use query params with GraphQL
   - Uses `POST` with REST endpoints

4. **❌ Type confusion**
   - Sends strings instead of integers
   - Causes silent failures (empty results)

5. **❌ Hallucinating fields**
   - Suggests fields that don't exist (`dewPoint`, `feelsLike`)
   - Doesn't verify against actual schema

---

### How To Prevent These Failures:

1. **📌 Always reference this document first**
   - Don't improvise based on generic API knowledge
   - Use tested examples as templates

2. **📌 Copy exact commands from "Quick Reference" section**
   - Modify only the filter values
   - Don't change URL/headers/syntax

3. **📌 Validate field names in schema documentation**
   - Before adding a new field to query
   - Check `College_Football_Data_GraphQL_Schema.md`

4. **📌 Use integers for numeric values**
   - `{_eq: 2025}` always works
   - `{_eq: "2025"}` always fails silently

5. **📌 Test incrementally**
   - Start with minimal query (just `id`)
   - Add fields one at a time
   - Easier to isolate errors

---

## 🔒 FINAL SAFETY RULES

### DO:
✅ Copy commands exactly from this document  
✅ Test in terminal before implementing in code  
✅ Check schema doc before adding new fields  
✅ Use integers for years/weeks/IDs  
✅ Include Authorization header ALWAYS  
✅ Pipe output to `python3 -m json.tool`  

### DON'T:
❌ Use environment variables for API key  
❌ Mix REST and GraphQL syntax  
❌ Assume fields exist without checking schema  
❌ Use string `"2025"` instead of integer `2025`  
❌ Forget `Content-Type: application/json` for GraphQL  
❌ Try to debug without checking error message type  

---

## 📊 QUICK COMPARISON TABLE

| Feature | GraphQL | REST API |
|---------|---------|----------|
| **Endpoint** | `https://graphql.collegefootballdata.com/v1/graphql` | `https://api.collegefootballdata.com` |
| **Method** | `POST` | `GET` |
| **Content-Type** | `application/json` (required) | Not needed |
| **Query Style** | JSON body with `{"query": "..."}` | URL query params `?year=2025` |
| **Field Selection** | Choose specific fields | Returns all fields |
| **Nested Data** | ✅ Yes (weather, betting) | ✅ Yes (but more verbose) |
| **Rankings/Polls** | ❌ Not available | ✅ Available |
| **Best For** | Complex queries, optimization | Simple queries, testing |
| **Learning Curve** | Steeper (GraphQL syntax) | Easier (standard GET) |

---

## 🆘 EMERGENCY CONTACT

**If nothing works:**
1. Run validation test command (see "Validation Test" section)
2. Verify internet connection: `ping api.collegefootballdata.com`
3. Try REST API instead of GraphQL (simpler debugging)
4. Check if API is having issues (try in browser)

---

**📝 Document Version**: 2.0  
**🗓️ Last Updated**: December 1, 2025  
**✅ Last Verified**: December 1, 2025 (All commands tested working)  
**🎯 Purpose**: Bulletproof reference for AI agents to prevent repeated API mistakes  
**👤 Maintained By**: User with GraphQL prediction engine integration  

---

**🚨 REMEMBER**: This document is the SINGLE SOURCE OF TRUTH. Do NOT improvise or use generic API patterns. When in doubt, copy-paste examples exactly as shown.
