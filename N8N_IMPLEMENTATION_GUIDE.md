# 🚀 n8n Implementation Guide - Quick Start

> **Practical guide for integrating n8n with Gameday+ in 4 hours**  
> **Prerequisite:** Read N8N_INTEGRATION_ANALYSIS.md for context

---

## 🎯 Phase 1: Foundation (60 minutes)

### **Step 1.1: Access Your n8n Instance**

1. Navigate to: `https://gamedayplus.app.n8n.cloud/projects/VmYJpPrc2MH2H3m8/workflows`
2. Log in with your credentials
3. Verify you see the workflow dashboard

### **Step 1.2: Test Your Flask API**

Open terminal and test your endpoints:

```bash
# Test health endpoint
curl https://graphqlmodel-production.up.railway.app/health

# Expected response:
# {"status":"healthy","service":"Gameday GraphQL Predictor"}

# Test teams endpoint
curl https://graphqlmodel-production.up.railway.app/teams | jq '.[0:3]'

# Test prediction endpoint
curl -X POST https://graphqlmodel-production.up.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "Ohio State",
    "away_team": "Michigan"
  }' | jq '.final_prediction'
```

### **Step 1.3: Create Your First Workflow**

**Name:** `Test Connection - Health Check`

**Nodes:**
1. **Manual Trigger** (start node)
2. **HTTP Request** to your Flask API
3. **Discord** notification (or email)

**Configuration:**

```javascript
// Node 1: Manual Trigger
Type: "Manual Trigger"
// Just click "Execute Workflow" button

// Node 2: HTTP Request
Type: "HTTP Request"
URL: "https://graphqlmodel-production.up.railway.app/health"
Method: "GET"
Response Format: "JSON"

// Node 3: Discord Webhook (optional)
Type: "Webhook"
URL: "YOUR_DISCORD_WEBHOOK_URL"
Content: "✅ Gameday+ API is healthy!"
```

**Execute the workflow and verify it succeeds.**

---

## 🔄 Phase 2: Automated Weekly Data Update (90 minutes)

### **Step 2.1: Add Webhook Endpoint to Flask (Optional)**

This is optional but recommended for better integration.

**File:** `app.py`

Add this after your existing routes:

```python
@app.route('/webhooks/n8n/data-update', methods=['POST'])
def n8n_data_update_webhook():
    """
    Webhook endpoint for n8n to trigger after data updates
    
    Expected payload:
    {
        "week": 12,
        "games_count": 51,
        "timestamp": "2025-12-02T06:00:00Z"
    }
    """
    try:
        data = request.get_json()
        week = data.get('week')
        games_count = data.get('games_count')
        timestamp = data.get('timestamp')
        
        # Log the update
        print(f"n8n Data Update Received - Week {week}: {games_count} games at {timestamp}")
        
        # You could add validation logic here
        # For example, verify games_count is reasonable (20-60)
        if games_count and (games_count < 20 or games_count > 60):
            return jsonify({
                'status': 'warning',
                'message': f'Unusual game count: {games_count}'
            }), 200
        
        return jsonify({
            'status': 'success',
            'message': f'Week {week} data update acknowledged'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/current-week', methods=['GET'])
def get_current_week():
    """
    Return the current week number and game count
    Useful for n8n workflows to determine what week to fetch
    """
    try:
        # Load current week games
        with open('Currentweekgames.json', 'r') as f:
            games = json.load(f)
        
        # Determine current week
        if games and len(games) > 0:
            current_week = games[0].get('week', None)
            return jsonify({
                'current_week': current_week,
                'games_count': len(games),
                'last_updated': os.path.getmtime('Currentweekgames.json')
            }), 200
        else:
            return jsonify({
                'current_week': None,
                'games_count': 0,
                'message': 'No games data available'
            }), 200
            
    except FileNotFoundError:
        return jsonify({
            'error': 'Currentweekgames.json not found'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
```

**Test the new endpoints:**

```bash
# Test current week endpoint
curl https://graphqlmodel-production.up.railway.app/api/current-week

# Test webhook endpoint
curl -X POST https://graphqlmodel-production.up.railway.app/webhooks/n8n/data-update \
  -H "Content-Type: application/json" \
  -d '{
    "week": 12,
    "games_count": 51,
    "timestamp": "2025-12-02T06:00:00Z"
  }'
```

### **Step 2.2: Create Weekly Data Update Workflow**

**Name:** `Weekly Data Update - Automated`

**Nodes:**

1. **Cron Trigger** - Monday at 6 AM ET
2. **HTTP Request** - Get current week number
3. **Code Node** - Calculate next week
4. **HTTP Request** - Fetch AP Poll from ESPN
5. **HTTP Request** - Fetch betting lines from GraphQL
6. **Code Node** - Transform and merge data
7. **HTTP Request** - Update GitHub repository
8. **Discord/Slack** - Success notification

**Detailed Configuration:**

```javascript
// Node 1: Cron Trigger
{
  "type": "n8n-nodes-base.cron",
  "parameters": {
    "triggerTimes": {
      "item": [
        {
          "mode": "everyWeek",
          "hour": 6,
          "minute": 0,
          "dayOfWeek": 1,  // Monday
          "timezone": "America/New_York"
        }
      ]
    }
  },
  "name": "Monday 6 AM ET"
}

// Node 2: Get Current Week
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://graphqlmodel-production.up.railway.app/api/current-week",
    "method": "GET",
    "responseFormat": "json"
  },
  "name": "Get Current Week"
}

// Node 3: Calculate Next Week
{
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "const currentWeek = items[0].json.current_week;\nconst nextWeek = currentWeek + 1;\n\nreturn [\n  {\n    json: {\n      week: nextWeek,\n      currentWeek: currentWeek\n    }\n  }\n];"
  },
  "name": "Calculate Next Week"
}

// Node 4: Fetch AP Poll
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings",
    "method": "GET",
    "responseFormat": "json"
  },
  "name": "Fetch AP Poll"
}

// Node 5: Fetch Betting Lines (GraphQL)
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://graphql.collegefootballdata.com/v1/graphql",
    "method": "POST",
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "bodyParameters": {
      "parameters": [
        {
          "name": "query",
          "value": "{\n  games(where: {year: {_eq: 2025}, week: {_eq: {{$node[\"Calculate Next Week\"].json[\"week\"]}}}, seasonType: {_eq: \"regular\"}}) {\n    id\n    week\n    homeTeam {\n      id\n      school\n      abbreviation\n      color\n      logos\n    }\n    awayTeam {\n      id\n      school\n      abbreviation\n      color\n      logos\n    }\n    lines {\n      provider\n      spread\n      formattedSpread\n      overUnder\n    }\n    mediaInfo {\n      mediaType\n      name\n    }\n    startDate\n    venue\n  }\n}"
        }
      ]
    },
    "responseFormat": "json"
  },
  "name": "Fetch Betting Lines"
}

// Node 6: Transform and Merge Data
{
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "// Get data from previous nodes\nconst apPoll = $node[\"Fetch AP Poll\"].json;\nconst bettingData = $node[\"Fetch Betting Lines\"].json.data.games;\nconst week = $node[\"Calculate Next Week\"].json.week;\n\n// Transform to Currentweekgames.json format\nconst transformedGames = bettingData.map(game => {\n  // Find rankings from AP Poll\n  const homeRank = null; // Implement AP poll lookup\n  const awayRank = null; // Implement AP poll lookup\n  \n  // Extract primary betting line\n  const primaryLine = game.lines && game.lines.length > 0 ? game.lines[0] : null;\n  \n  return {\n    week: game.week,\n    homeTeam: {\n      id: game.homeTeam.id,\n      school: game.homeTeam.school,\n      abbreviation: game.homeTeam.abbreviation,\n      rank: homeRank,\n      color: game.homeTeam.color,\n      logos: game.homeTeam.logos\n    },\n    awayTeam: {\n      id: game.awayTeam.id,\n      school: game.awayTeam.school,\n      abbreviation: game.awayTeam.abbreviation,\n      rank: awayRank,\n      color: game.awayTeam.color,\n      logos: game.awayTeam.logos\n    },\n    lines: game.lines,\n    spread: primaryLine ? primaryLine.spread : null,\n    overUnder: primaryLine ? primaryLine.overUnder : null,\n    network: game.mediaInfo && game.mediaInfo.length > 0 ? game.mediaInfo[0].name : \"TBD\",\n    startDate: game.startDate,\n    venue: game.venue\n  };\n});\n\nreturn [\n  {\n    json: {\n      week: week,\n      games: transformedGames,\n      updated: new Date().toISOString()\n    }\n  }\n];"
  },
  "name": "Transform Data"
}

// Node 7: Commit to GitHub (requires GitHub credentials in n8n)
// Alternative: Use HTTP Request to GitHub API
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.github.com/repos/Davlen14/gameday-plus-predictor/contents/Currentweekgames.json",
    "method": "PUT",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "githubApi",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "message",
          "value": "n8n: Update Week {{$node[\"Calculate Next Week\"].json[\"week\"]}} betting data"
        },
        {
          "name": "content",
          "value": "={{$base64(JSON.stringify($node[\"Transform Data\"].json.games, null, 2))}}"
        },
        {
          "name": "sha",
          "value": "GET_FROM_PREVIOUS_REQUEST" // You need to fetch current file SHA first
        }
      ]
    }
  },
  "name": "Update GitHub"
}

// Node 8: Discord Notification
{
  "type": "n8n-nodes-base.discord",
  "parameters": {
    "webhook": {
      "webhookUrl": "YOUR_DISCORD_WEBHOOK_URL"
    },
    "content": "🏈 Week {{$node[\"Calculate Next Week\"].json[\"week\"]}} data updated!\n\n📊 Games: {{$node[\"Transform Data\"].json.games.length}}\n⏰ Updated: {{$now.format('YYYY-MM-DD HH:mm:ss')}}\n\n✅ Currentweekgames.json committed to GitHub"
  },
  "name": "Notify Discord"
}
```

**Note:** The GitHub commit part is complex. Easier alternative:

### **Alternative: Use Railway Deployment Webhook**

Instead of committing to GitHub, trigger a Railway deployment webhook after manually updating the file:

1. Manual process stays the same (update JSON file)
2. n8n triggers Railway redeploy automatically
3. Sends notifications

---

## 💰 Phase 3: Value Pick Alerts (60 minutes)

### **Step 3.1: Create Value Pick Detection Workflow**

**Name:** `Value Pick Alerts - 3x Daily`

**Trigger:** 9 AM, 3 PM, 9 PM ET (Tuesday-Saturday)

**Nodes:**

```javascript
// Node 1: Cron Trigger (3x daily)
{
  "type": "n8n-nodes-base.cron",
  "parameters": {
    "triggerTimes": {
      "item": [
        {
          "mode": "everyDay",
          "hour": 9,
          "minute": 0,
          "timezone": "America/New_York",
          "dayOfWeek": [2,3,4,5,6] // Tue-Sat
        },
        {
          "mode": "everyDay",
          "hour": 15,
          "minute": 0,
          "timezone": "America/New_York",
          "dayOfWeek": [2,3,4,5,6]
        },
        {
          "mode": "everyDay",
          "hour": 21,
          "minute": 0,
          "timezone": "America/New_York",
          "dayOfWeek": [2,3,4,5,6]
        }
      ]
    }
  },
  "name": "3x Daily Trigger"
}

// Node 2: Load Current Week Games
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://graphqlmodel-production.up.railway.app/api/current-week",
    "method": "GET"
  },
  "name": "Get Games"
}

// Node 3: Code - Extract Ranked Matchups
{
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "// Load current week games from file (you'd need to fetch this)\n// For now, assume we have a list of game IDs\nconst games = [\n  {home: 'Ohio State', away: 'Michigan'},\n  {home: 'Georgia', away: 'Alabama'},\n  // ... more games\n];\n\nreturn games.map(game => ({\n  json: {\n    home_team: game.home,\n    away_team: game.away\n  }\n}));"
  },
  "name": "Extract Games"
}

// Node 4: Loop - Get Predictions (one per game)
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://graphqlmodel-production.up.railway.app/predict",
    "method": "POST",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "home_team",
          "value": "={{$json[\"home_team\"]}}"
        },
        {
          "name": "away_team",
          "value": "={{$json[\"away_team\"]}}"
        }
      ]
    }
  },
  "name": "Get Predictions",
  "executeOnce": false // Process all items
}

// Node 5: Filter - Only High Value Picks
{
  "type": "n8n-nodes-base.filter",
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{$json[\"market_comparison\"][\"edge\"]}}", 
          "value2": 10,
          "operation": "larger"
        }
      ],
      "combineOperation": "any"
    }
  },
  "name": "Filter Value Picks"
}

// Node 6: Discord Alert
{
  "type": "n8n-nodes-base.discord",
  "parameters": {
    "webhook": {
      "webhookUrl": "YOUR_DISCORD_WEBHOOK_URL"
    },
    "content": "🚨 **VALUE PICK ALERT** 🚨\n\n🏈 {{$json[\"final_prediction\"][\"home_team\"]}} vs {{$json[\"final_prediction\"][\"away_team\"]}}\n\n📊 **Model:** {{$json[\"final_prediction\"][\"spread\"]}}\n💰 **Vegas:** {{$json[\"market_comparison\"][\"consensus_spread\"]}}\n⚡ **Edge:** {{$json[\"market_comparison\"][\"edge\"]}} points\n\n🎯 **Recommendation:** {{$json[\"market_comparison\"][\"recommendation\"]}}\n🔥 **Confidence:** {{$json[\"confidence\"][\"overall_confidence\"]}}%"
  },
  "name": "Alert Discord"
}
```

---

## 📊 Phase 4: Performance Tracking (60 minutes)

### **Step 4.1: Create Google Sheet for Tracking**

1. Create new Google Sheet: "Gameday+ Prediction Tracker"
2. Columns:
   - Date
   - Week
   - Home Team
   - Away Team
   - Model Spread
   - Actual Spread
   - Model Total
   - Actual Total
   - Model Win Prob
   - Actual Result
   - Spread Correct (Y/N)
   - Total Correct (Y/N)
   - Edge
   - Confidence

### **Step 4.2: Create Prediction Logging Workflow**

**Name:** `Log Predictions to Sheet`

**Trigger:** Manual (called from other workflows) or webhook

```javascript
// Node 1: HTTP Request - Get Prediction
// (Same as before)

// Node 2: Google Sheets - Append Row
{
  "type": "n8n-nodes-base.googleSheets",
  "parameters": {
    "operation": "append",
    "sheetId": "YOUR_GOOGLE_SHEET_ID",
    "range": "Sheet1",
    "options": {},
    "columns": {
      "mappings": [
        {
          "from": "date",
          "to": "={{$now.format('YYYY-MM-DD HH:mm:ss')}}"
        },
        {
          "from": "week",
          "to": "={{$json[\"contextual_analysis\"][\"current_week\"]}}"
        },
        {
          "from": "home_team",
          "to": "={{$json[\"final_prediction\"][\"home_team\"]}}"
        },
        {
          "from": "away_team",
          "to": "={{$json[\"final_prediction\"][\"away_team\"]}}"
        },
        {
          "from": "model_spread",
          "to": "={{$json[\"final_prediction\"][\"spread\"]}}"
        },
        {
          "from": "model_total",
          "to": "={{$json[\"final_prediction\"][\"total\"]}}"
        },
        {
          "from": "confidence",
          "to": "={{$json[\"confidence\"][\"overall_confidence\"]}}"
        },
        {
          "from": "edge",
          "to": "={{$json[\"market_comparison\"][\"edge\"]}}"
        }
      ]
    }
  },
  "name": "Log to Sheet"
}
```

---

## 🎯 Testing Checklist

### **Before Going Live:**

- [ ] Test health check workflow manually
- [ ] Verify Flask API responses match expected format
- [ ] Test Discord/Slack notifications
- [ ] Verify cron schedules are in correct timezone (ET)
- [ ] Test error handling (what happens if API is down?)
- [ ] Set up email notifications for workflow failures
- [ ] Document all webhook URLs and API keys securely

### **After First Automated Run:**

- [ ] Check data quality in Currentweekgames.json
- [ ] Verify predictions are being generated correctly
- [ ] Review Google Sheet for accurate logging
- [ ] Check notification channels for alerts
- [ ] Review n8n execution logs for errors

---

## 🔒 Security Best Practices

1. **API Keys:**
   - Store in n8n credentials manager (not in workflow code)
   - Use environment variables in Flask
   - Never commit keys to GitHub

2. **Webhook URLs:**
   - Keep Discord/Slack webhooks private
   - Use authentication for sensitive endpoints
   - Consider rate limiting

3. **Access Control:**
   - Limit n8n workflow access to authorized users
   - Use Railway environment variables for secrets
   - Rotate credentials periodically

---

## 🐛 Troubleshooting

### **Workflow Won't Execute:**
- Check cron trigger timezone (America/New_York)
- Verify workflow is "Active" (toggle in top right)
- Check n8n execution logs for errors

### **API Requests Failing:**
- Test endpoint manually with curl
- Check Railway logs for backend errors
- Verify request body format matches API expectations

### **Notifications Not Sending:**
- Test webhook URL in browser/Postman
- Check Discord/Slack webhook permissions
- Verify n8n has internet access

### **Data Quality Issues:**
- Add validation steps in workflows
- Compare against previous week's data
- Manual spot-check on key games

---

## 📚 Quick Reference

### **Useful n8n Expressions:**

```javascript
// Current date/time
{{$now.format('YYYY-MM-DD HH:mm:ss')}}

// Access previous node data
{{$node["Node Name"].json["field"]}}

// Loop through array
{{$json["array"].map(item => item.field)}}

// Conditional
{{$json["value"] > 10 ? "High" : "Low"}}

// Base64 encode (for GitHub)
{{$base64($json["content"])}}
```

### **Gameday+ API Quick Hits:**

```bash
# Health check
curl https://graphqlmodel-production.up.railway.app/health

# Get teams
curl https://graphqlmodel-production.up.railway.app/teams

# Get prediction
curl -X POST https://graphqlmodel-production.up.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Ohio State", "away_team": "Michigan"}'

# Get current week
curl https://graphqlmodel-production.up.railway.app/api/current-week
```

---

## 🎉 Success Metrics

After implementing n8n, you should see:

✅ **Time Savings:**
- 45 min/week saved on data updates
- 30 min/week saved on prediction runs
- 1 hour/week saved on monitoring

✅ **Consistency:**
- Data always updated on time
- No missed updates during busy weeks
- Predictable workflow execution

✅ **Insights:**
- Automated tracking in Google Sheets
- Easy to analyze performance trends
- Data-driven model improvements

✅ **Distribution:**
- Predictions shared across multiple channels
- Real-time value pick alerts
- Growing audience engagement

---

**Next:** Read N8N_INTEGRATION_ANALYSIS.md for strategic context and long-term planning.

**Support:** n8n Community Forum - https://community.n8n.io/

