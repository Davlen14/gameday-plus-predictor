# 🏈 N8N INTEGRATION GUIDE FOR GAMEDAY PROJECT

## 📋 Table of Contents
1. [What This Guide Does](#what-this-guide-does)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Workflow 1: Single Game Prediction](#workflow-1-single-game-prediction)
5. [Workflow 2: Multiple Games Prediction](#workflow-2-multiple-games-prediction)
6. [Making It Automatic](#making-it-automatic)
7. [Adding Outputs](#adding-outputs)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Use Cases](#advanced-use-cases)

---

## What This Guide Does

This guide shows you how to integrate your **Gameday_Graphql_Model** Flask API with **n8n** (automation tool) to:
- Automatically run predictions on schedule
- Process multiple games at once
- Send predictions via email, Slack, Discord, or Google Sheets
- Build automated betting analysis workflows

**Important:** You DON'T drag your project into n8n. Instead, n8n **calls your Flask API** to get predictions.

---

## Prerequisites

### What You Need Running:

1. **Your Flask Server Must Be Running**
   ```bash
   cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
   python app.py
   ```
   Keep this terminal window open while using n8n!

2. **n8n Installed and Running**
   - If you don't have n8n: `npx n8n` or desktop app
   - Access it at: `http://localhost:5678`

3. **Verify Your API Works**
   Open another terminal and test:
   ```bash
   curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"home_team": "Ohio State", "away_team": "Michigan"}'
   ```
   You should see JSON prediction data.

---

## Quick Start

### Step 1: Start Your Flask Server
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
python app.py
```
**Keep this running!**

### Step 2: Open n8n
- Go to `http://localhost:5678`
- Click **"Start from scratch"** or **"Create new workflow"**

### Step 3: Test Connection
1. Add **HTTP Request** node
2. Configure:
   - Method: `POST`
   - URL: `http://localhost:5001/predict`
   - Body (JSON):
   ```json
   {
     "home_team": "Ohio State",
     "away_team": "Michigan"
   }
   ```
3. Click **"Execute Node"**
4. See your prediction! ✅

---

## Workflow 1: Single Game Prediction

### Visual Flow:
```
Manual Trigger → HTTP Request → Format Results → Output (Email/Slack/etc)
```

### Step-by-Step Setup:

#### Node 1: Manual Trigger (Already Added)
- Default node when creating new workflow
- Click it to test workflow manually

#### Node 2: HTTP Request Node
1. Click **+** after the trigger
2. Search for **"HTTP Request"**
3. Configure:

```yaml
Method: POST
URL: http://localhost:5001/predict
Authentication: None
Send Body: Yes (toggle on)
Body Content Type: JSON
```

**JSON Body:**
```json
{
  "home_team": "Ohio State",
  "away_team": "Michigan"
}
```

**Options:**
- Timeout: 30000ms (30 seconds)
- Response Format: JSON

#### Node 3: Code Node (Format Output)
1. Click **+** after HTTP Request
2. Search for **"Code"**
3. Select **"Run Once for All Items"**
4. Paste this code:

```javascript
// Extract the prediction data
const prediction = $input.first().json;

// Format a nice summary
const summary = {
  game: `${prediction.away_team} @ ${prediction.home_team}`,
  predicted_winner: prediction.predicted_winner,
  predicted_score: `${prediction.predicted_home_score} - ${prediction.predicted_away_score}`,
  confidence: `${(prediction.confidence * 100).toFixed(1)}%`,
  spread_prediction: prediction.spread_prediction,
  value_pick: prediction.value_pick || 'No edge detected',
  timestamp: new Date().toLocaleString(),
  
  // Additional metrics if available
  home_win_prob: prediction.home_win_probability ? 
    `${(prediction.home_win_probability * 100).toFixed(1)}%` : 'N/A',
  away_win_prob: prediction.away_win_probability ? 
    `${(prediction.away_win_probability * 100).toFixed(1)}%` : 'N/A'
};

return { json: summary };
```

#### Node 4: Set Output Node (Choose One)

**Option A: Discord Webhook**
1. Add **"Discord"** node
2. Webhook URL: Your Discord webhook
3. Message:
```
🏈 **{{$json.game}}**

**Predicted Winner:** {{$json.predicted_winner}}
**Score Prediction:** {{$json.predicted_score}}
**Confidence:** {{$json.confidence}}

**Spread:** {{$json.spread_prediction}}
**Value Pick:** {{$json.value_pick}}

*Generated: {{$json.timestamp}}*
```

**Option B: Send Email**
1. Add **"Send Email"** node
2. To: `your@email.com`
3. Subject: `CFB Prediction: {{$json.game}}`
4. Body: Same as Discord message above

**Option C: Google Sheets**
1. Add **"Google Sheets"** node
2. Operation: Append
3. Document: Select your spreadsheet
4. Sheet: "Predictions"
5. Columns:
   - A: `{{$json.game}}`
   - B: `{{$json.predicted_winner}}`
   - C: `{{$json.predicted_score}}`
   - D: `{{$json.confidence}}`
   - E: `{{$json.value_pick}}`
   - F: `{{$json.timestamp}}`

### Test Your Workflow
1. Click **"Test workflow"** button at top
2. Check all nodes turn green ✅
3. Verify output received (email/Discord/Sheets)
4. Click **"Save"** to save workflow

---

## Workflow 2: Multiple Games Prediction

### Visual Flow:
```
Trigger → Read JSON File → Parse Games → Loop: HTTP Request → Aggregate → Output
```

### Step-by-Step Setup:

#### Node 1: Manual Trigger
- Default starting node

#### Node 2: Read Binary File
1. Click **+** after trigger
2. Search **"Read Binary File"**
3. Configure:
   - File Path: `/Users/davlenswain/Desktop/Gameday_Graphql_Model/week15.json`

#### Node 3: Code Node (Parse Games)
1. Click **+** after Read File
2. Add **"Code"** node
3. Paste this code:

```javascript
// Parse the JSON file
const fileContent = $input.first().binary.data;
const jsonString = Buffer.from(fileContent, 'base64').toString('utf8');
const gamesData = JSON.parse(jsonString);

// Extract games array (adjust based on your JSON structure)
let games = [];

// Handle different JSON structures
if (Array.isArray(gamesData)) {
  games = gamesData;
} else if (gamesData.games) {
  games = gamesData.games;
} else if (gamesData.data) {
  games = gamesData.data;
} else if (gamesData.week && gamesData.week.games) {
  games = gamesData.week.games;
}

console.log(`Found ${games.length} games to process`);

// Return each game as a separate item for processing
return games.map((game, index) => ({
  json: {
    game_number: index + 1,
    home_team: game.home_team || game.homeTeam || game.home || game.home_school,
    away_team: game.away_team || game.awayTeam || game.away || game.away_school,
    game_id: game.id || game.game_id,
    week: game.week || game.season_week
  }
}));
```

#### Node 4: HTTP Request (Predict Each Game)
1. Click **+** after Parse Games
2. Add **"HTTP Request"** node
3. Configure:

```yaml
Method: POST
URL: http://localhost:5001/predict
Authentication: None
Send Body: Yes
Body Content Type: JSON
```

**JSON Body (use expressions):**
```json
{
  "home_team": "={{$json.home_team}}",
  "away_team": "={{$json.away_team}}"
}
```

**IMPORTANT - Set Batching:**
- Click **"Add Option"**
- Select **"Batching"**
- Batch Size: `1`
- Batch Interval: `2000` (2 seconds between requests)

This prevents overwhelming your API!

#### Node 5: Code Node (Aggregate Results)
1. Click **+** after HTTP Request
2. Add **"Code"** node
3. Select **"Run Once for All Items"**
4. Paste this code:

```javascript
// Collect all predictions into one array
const items = $input.all();

const allPredictions = items.map((item, index) => {
  const pred = item.json;
  return {
    game_number: index + 1,
    game: `${pred.away_team} @ ${pred.home_team}`,
    winner: pred.predicted_winner,
    home_score: pred.predicted_home_score,
    away_score: pred.predicted_away_score,
    score_display: `${pred.predicted_home_score} - ${pred.predicted_away_score}`,
    confidence: parseFloat((pred.confidence * 100).toFixed(1)),
    confidence_display: `${(pred.confidence * 100).toFixed(1)}%`,
    spread: pred.spread_prediction,
    value: pred.value_pick || 'No edge',
    has_value: (pred.value_pick && pred.value_pick !== 'No edge detected')
  };
});

// Sort by confidence (highest first)
allPredictions.sort((a, b) => b.confidence - a.confidence);

// Separate high-confidence picks
const highConfidence = allPredictions.filter(p => p.confidence >= 70);
const valuePicks = allPredictions.filter(p => p.has_value);

// Create summary
const summary = {
  total_games: allPredictions.length,
  high_confidence_count: highConfidence.length,
  value_picks_count: valuePicks.length,
  generated_at: new Date().toLocaleString(),
  all_predictions: allPredictions,
  high_confidence_picks: highConfidence,
  value_picks: valuePicks
};

return [{ json: summary }];
```

#### Node 6: Output Node (Choose One)

**Option A: Email Report**
1. Add **"Send Email"** node
2. Subject: `Week {{$json.week}} CFB Predictions - {{$json.total_games}} Games`
3. Body (HTML or Text):

```html
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: Arial, sans-serif; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
  th { background-color: #4CAF50; color: white; }
  .high-conf { background-color: #d4edda; }
  .value-pick { background-color: #fff3cd; }
</style>
</head>
<body>
  <h1>🏈 College Football Predictions</h1>
  <p><strong>Total Games:</strong> {{$json.total_games}}</p>
  <p><strong>High Confidence Picks:</strong> {{$json.high_confidence_count}}</p>
  <p><strong>Value Picks:</strong> {{$json.value_picks_count}}</p>
  <p><strong>Generated:</strong> {{$json.generated_at}}</p>

  <h2>High Confidence Picks (70%+)</h2>
  <table>
    <tr>
      <th>Game</th>
      <th>Winner</th>
      <th>Score</th>
      <th>Confidence</th>
      <th>Value</th>
    </tr>
    {{#each $json.high_confidence_picks}}
    <tr class="high-conf">
      <td>{{game}}</td>
      <td>{{winner}}</td>
      <td>{{score_display}}</td>
      <td>{{confidence_display}}</td>
      <td>{{value}}</td>
    </tr>
    {{/each}}
  </table>

  <h2>All Predictions</h2>
  <table>
    <tr>
      <th>#</th>
      <th>Game</th>
      <th>Winner</th>
      <th>Score</th>
      <th>Confidence</th>
      <th>Spread</th>
      <th>Value</th>
    </tr>
    {{#each $json.all_predictions}}
    <tr>
      <td>{{game_number}}</td>
      <td>{{game}}</td>
      <td>{{winner}}</td>
      <td>{{score_display}}</td>
      <td>{{confidence_display}}</td>
      <td>{{spread}}</td>
      <td>{{value}}</td>
    </tr>
    {{/each}}
  </table>
</body>
</html>
```

**Option B: Discord Webhook**
1. Add **"Discord"** node
2. Message:

```
🏈 **WEEK PREDICTIONS READY**

**Total Games:** {{$json.total_games}}
**High Confidence:** {{$json.high_confidence_count}}
**Value Picks:** {{$json.value_picks_count}}

**TOP 5 PICKS:**
{{#each $json.high_confidence_picks.[0-4]}}
{{game_number}}. {{game}}
   Winner: {{winner}} ({{confidence_display}})
   Score: {{score_display}}
   Value: {{value}}
{{/each}}

*Full report generated at {{$json.generated_at}}*
```

**Option C: Google Sheets**
1. Add **"Google Sheets"** node
2. Operation: **Clear** (clear old data first)
3. Then add another **Google Sheets** node
4. Operation: **Append**
5. Use **Loop Over Items** for each prediction
6. Map columns from `{{$json.all_predictions}}`

### Test Multiple Games Workflow
1. Ensure `week15.json` exists with game data
2. Click **"Test workflow"**
3. Watch it process each game (may take time!)
4. Check final output
5. **Save** workflow

---

## Making It Automatic

### Replace Manual Trigger with Schedule

#### For Weekly Predictions (Every Saturday):

1. **Delete** the Manual Trigger node
2. Click **"Add trigger node"**
3. Search **"Schedule Trigger"**
4. Configure:

```yaml
Trigger Interval: Days of the Week
Week Days: Saturday
Hour: 09 (9 AM)
Minute: 00
Timezone: America/New_York (or your timezone)
```

5. **Save and Activate** workflow (toggle switch at top)

#### For Daily Updates:

```yaml
Trigger Interval: Every Day
Hour: 10
Minute: 00
```

#### For Specific Game Times:

```yaml
Trigger Interval: Custom
Cron Expression: 0 12 * * 6
```
(Saturdays at noon)

### Activate Your Workflow
1. Click the **toggle switch** at top right
2. It turns blue when active
3. Workflow will run automatically on schedule!

---

## Adding Outputs

### Email Setup

**Using Gmail:**
1. Add **"Gmail"** node
2. Click **"Create New Credential"**
3. Sign in with Google
4. Configure message as shown above

**Using SMTP:**
1. Add **"Send Email"** node
2. Configure SMTP settings:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - Username: your email
   - Password: app password (not regular password!)

### Slack Setup

1. Add **"Slack"** node
2. Create Slack app: https://api.slack.com/apps
3. Add webhook URL
4. Configure channel and message

### Discord Setup

1. Add **"Discord"** node
2. Create webhook in Discord server:
   - Server Settings → Integrations → Webhooks
   - Copy webhook URL
3. Paste URL in n8n Discord node

### Google Sheets Setup

1. Add **"Google Sheets"** node
2. Click **"Create New Credential"**
3. Sign in with Google
4. Grant permissions
5. Select spreadsheet and sheet
6. Map your data columns

### Database Storage (PostgreSQL/MySQL)

1. Add **"PostgreSQL"** or **"MySQL"** node
2. Configure connection:
   - Host: `localhost`
   - Database: your database name
   - User & Password
3. Operation: Insert
4. Table: `predictions`
5. Map columns

---

## Troubleshooting

### Problem: "Connection Refused" or "ECONNREFUSED"

**Cause:** Flask server isn't running

**Solution:**
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
python app.py
```
Keep this terminal open!

**Verify it's running:**
```bash
curl http://localhost:5001
```

---

### Problem: "Team not found" Error

**Cause:** Team name doesn't match your `fbs.json` database

**Solution:**
- Use exact team names from `fbs.json`
- Examples:
  - ✅ "Ohio State" (correct)
  - ❌ "OSU" (wrong)
  - ✅ "Michigan" (correct)
  - ❌ "UM" (wrong)

**Check valid team names:**
```bash
cat /Users/davlenswain/Desktop/Gameday_Graphql_Model/fbs.json | grep '"school"'
```

---

### Problem: "Cannot read file" Error

**Cause:** File path is incorrect

**Solution:**
Use absolute path:
```
/Users/davlenswain/Desktop/Gameday_Graphql_Model/week15.json
```

**Verify file exists:**
```bash
ls -la /Users/davlenswain/Desktop/Gameday_Graphql_Model/week15.json
```

---

### Problem: Workflow Runs But No Output

**Solution:**
1. Click on each node
2. Check the **"Output"** tab on right panel
3. Look for error messages in red
4. Check execution logs at bottom

---

### Problem: "Timeout" Error

**Cause:** Prediction taking too long

**Solution:**
In HTTP Request node:
- Click **"Add Option"**
- Select **"Timeout"**
- Set to: `60000` (60 seconds)

---

### Problem: Too Many Requests / API Overload

**Solution:**
Add batching to HTTP Request node:
- Click **"Add Option"**
- Select **"Batching"**
- Batch Size: `1`
- Batch Interval: `3000` (3 seconds)

---

### Problem: JSON Parse Error

**Cause:** Response isn't valid JSON

**Solution:**
1. Check HTTP Request node output
2. Add Code node before parsing:
```javascript
const response = $input.first().json;
console.log('Response:', JSON.stringify(response, null, 2));
return { json: response };
```

---

### Problem: Schedule Not Triggering

**Solution:**
1. Check workflow is **ACTIVE** (blue toggle at top)
2. Verify timezone is correct
3. Check n8n is running (don't close n8n!)
4. View execution history: Executions tab

---

## Advanced Use Cases

### 1. Weekly Report with Accuracy Tracking

```
Schedule (Monday 8am)
  → Read last week's predictions from database
  → Fetch actual scores from API
  → Compare predictions vs actuals
  → Calculate accuracy metrics
  → Generate report
  → Email to subscribers
```

**Metrics to Track:**
- Win/Loss accuracy
- Spread accuracy (within 3 points)
- Over/Under accuracy
- High-confidence pick success rate
- ROI on value picks

### 2. Real-Time Betting Value Finder

```
Schedule (Every hour during gameday)
  → Fetch current betting lines
  → Run predictions
  → Compare predicted vs actual lines
  → Filter for positive EV (+5% or more)
  → Send alerts to Discord/SMS
```

### 3. Player Props Predictions

```
Manual/Schedule Trigger
  → Select game from dropdown
  → Call /enhanced-props endpoint
  → Format player predictions
  → Compare to betting markets
  → Highlight value props
  → Export to betting sheet
```

**API Endpoint:**
```bash
POST http://localhost:5001/enhanced-props
{
  "home_team": "Ohio State",
  "away_team": "Michigan"
}
```

### 4. Conference Championship Scenarios

```
Manual Trigger
  → Input conference name
  → Fetch all conference games
  → Run predictions for remaining games
  → Calculate tiebreaker scenarios
  → Generate championship probability matrix
  → Create visualization
  → Post to Twitter/Discord
```

### 5. Injury Impact Analysis

```
Webhook Trigger (injury news)
  → Parse player and team info
  → Re-run prediction with/without player
  → Calculate point differential
  → Update line projections
  → Alert if significant change (>3 points)
```

### 6. Parlay Builder

```
Manual Trigger
  → Get all high-confidence picks (>70%)
  → Filter by time slots (no overlaps)
  → Calculate combined odds
  → Generate optimal 3/5/7 game parlays
  → Display expected value
  → Format for betting slip
```

### 7. Live Game Monitoring

```
Webhook (from live score API)
  → Receive score update
  → Compare to prediction
  → Calculate win probability shift
  → Alert on large deviations
  → Track in-game betting opportunities
```

---

## Complete Workflow Examples

### Example 1: Saturday Morning Predictions

**Flow:**
```
1. Schedule Trigger (Saturday 9am)
2. Read week15.json
3. Parse games
4. Loop: Call /predict for each game
5. Aggregate results
6. Format HTML email
7. Send to email list
8. Post summary to Discord
9. Update Google Sheet
```

**Execution Time:** ~2-5 minutes for 30 games
**Frequency:** Weekly

---

### Example 2: Hourly Line Shopping

**Flow:**
```
1. Schedule Trigger (Every hour, 9am-11pm)
2. Fetch current lines from betting API
3. Run predictions
4. Compare: predicted line vs actual line
5. Calculate edge (%)
6. Filter: edge > 5%
7. If value found:
   → Send push notification
   → Post to Discord #betting-alerts
   → Log to database
8. End
```

**Execution Time:** ~30 seconds
**Frequency:** Hourly during game days

---

### Example 3: Results Tracker

**Flow:**
```
1. Schedule Trigger (Monday 8am)
2. Read last week's predictions from DB
3. Fetch actual scores from ESPN API
4. Compare predictions vs actuals
5. Calculate metrics:
   - Win % accuracy
   - Average point differential
   - Spread accuracy
   - High-confidence accuracy
6. Generate charts
7. Create weekly report
8. Email to subscribers
9. Update season stats
```

**Execution Time:** ~1 minute
**Frequency:** Weekly

---

## API Endpoints Reference

Your Flask app provides these endpoints:

### GET `/`
Health check - returns status

### GET `/teams`
Returns all FBS teams from `fbs.json`

### POST `/predict`
**Request:**
```json
{
  "home_team": "Ohio State",
  "away_team": "Michigan"
}
```

**Response:**
```json
{
  "home_team": "Ohio State",
  "away_team": "Michigan",
  "predicted_winner": "Ohio State",
  "predicted_home_score": 31,
  "predicted_away_score": 24,
  "confidence": 0.78,
  "spread_prediction": "Ohio State -7",
  "value_pick": "Ohio State -6.5 (+EV)",
  "home_win_probability": 0.78,
  "away_win_probability": 0.22,
  "key_factors": [
    "Home field advantage",
    "Superior offensive efficiency"
  ]
}
```

### POST `/enhanced-props`
Get player props predictions (if available)

**Request:**
```json
{
  "home_team": "Ohio State",
  "away_team": "Michigan"
}
```

---

## File Paths Reference

Important files in your project:

```
/Users/davlenswain/Desktop/Gameday_Graphql_Model/
├── app.py                          # Flask API server
├── graphqlpredictor.py             # Prediction engine
├── fbs.json                        # Team database
├── week15.json                     # Current week games
├── week15_with_lines.json          # Games with betting lines
├── Currentweekgames.json           # Current games
├── requirements.txt                # Python dependencies
└── data/                           # Historical data
```

---

## Performance Tips

### 1. Batch Requests
Always use batching when processing multiple games:
```yaml
Batch Size: 1
Batch Interval: 2000ms
```

### 2. Caching
Cache team data to avoid repeated reads:
```javascript
// In Code node
const teams = $node["Read Teams"].json;
// Use throughout workflow
```

### 3. Error Handling
Wrap API calls in try-catch:
```javascript
try {
  const response = await fetch(url);
  return { json: await response.json() };
} catch (error) {
  return { json: { error: error.message } };
}
```

### 4. Timeout Settings
Set appropriate timeouts:
- Simple predictions: 30 seconds
- Complex analysis: 60 seconds
- Batch operations: 120 seconds

---

## Security Notes

### 1. Don't Expose API Publicly
Your Flask server runs on `localhost` only:
```python
# Good (default)
app.run(host='127.0.0.1', port=5001)

# Bad - don't do this
app.run(host='0.0.0.0', port=5001)
```

### 2. Protect n8n Webhooks
If using webhooks, add authentication:
```yaml
Authentication: Header Auth
Header Name: X-API-Key
Header Value: your-secret-key
```

### 3. Secure Credentials
Use n8n's credential system - don't hardcode:
- Email passwords
- API keys
- Webhook URLs
- Database passwords

---

## Next Steps

### Beginner Level:
1. ✅ Set up single game prediction
2. ✅ Add email output
3. ✅ Test with manual trigger
4. ✅ Add schedule trigger

### Intermediate Level:
1. ✅ Process multiple games from JSON
2. ✅ Add Discord/Slack notifications
3. ✅ Store predictions in Google Sheets
4. ✅ Create weekly summary reports

### Advanced Level:
1. ✅ Build accuracy tracking system
2. ✅ Integrate live betting APIs
3. ✅ Create value betting alerts
4. ✅ Develop parlay builder
5. ✅ Add player props analysis

---

## Support Resources

### Your Project Documentation:
- `README.md` - Project overview
- `GRAPHQL_MIGRATION_GUIDE.md` - API details
- `DEBUGGING_GUIDE.md` - Troubleshooting

### n8n Documentation:
- https://docs.n8n.io
- https://docs.n8n.io/code-examples/
- https://community.n8n.io

### Need Help?
1. Check n8n execution logs
2. Test API with curl first
3. Verify Flask server is running
4. Check this guide's troubleshooting section

---

## Workflow JSON Files

Two complete workflow files are included in this guide:

1. **Simple Single Game Prediction**
   - File: `Gameday_Prediction_Workflow.json`
   - Use for: Testing, single game analysis

2. **Multiple Games Batch Prediction**
   - File: `Multi_Game_Predictions_Workflow.json`
   - Use for: Weekly predictions, automated reports

**To Import:**
1. Copy JSON content from artifacts section
2. In n8n: Menu → Import from File
3. Paste JSON
4. Click Import

---

## Checklist: Your First Workflow

Use this checklist to set up your first working workflow:

### Setup Phase:
- [ ] Flask server installed and tested
- [ ] n8n installed and running
- [ ] Verified API works with curl
- [ ] `week15.json` file exists and has data

### Build Phase:
- [ ] Created new workflow in n8n
- [ ] Added HTTP Request node
- [ ] Configured with correct URL and body
- [ ] Tested single prediction successfully
- [ ] Added Code node for formatting
- [ ] Added output node (email/Slack/etc)

### Test Phase:
- [ ] Clicked "Test workflow"
- [ ] All nodes show green checkmarks
- [ ] Received output (email/message/etc)
- [ ] Saved workflow with descriptive name

### Automation Phase:
- [ ] Replaced manual trigger with schedule
- [ ] Set correct day/time for execution
- [ ] Activated workflow (blue toggle)
- [ ] Verified first scheduled run works

### Done! 🎉
You now have automated college football predictions!

---

## Quick Reference Commands

### Start Flask Server:
```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
python app.py
```

### Test API:
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team":"Ohio State","away_team":"Michigan"}'
```

### Check if Server is Running:
```bash
curl http://localhost:5001
```

### View Team Names:
```bash
cat fbs.json | grep '"school"' | head -20
```

### Start n8n (if not running):
```bash
npx n8n
# or
n8n start
```

---

## Change Log

**Version 1.0** - Initial integration guide
- Single game prediction workflow
- Multiple games batch workflow  
- Email/Slack/Discord/Sheets outputs
- Scheduling and automation
- Troubleshooting guide

---

**Last Updated:** December 3, 2024

**Project:** Gameday_Graphql_Model  
**Integration:** n8n Automation Platform  
**Author:** Davlen

---

## Additional Notes

This guide assumes:
- macOS or Linux system
- Python 3.8+ installed
- n8n installed and running
- Basic familiarity with JSON and REST APIs

For Windows users, adjust file paths:
```
C:\Users\YourName\Desktop\Gameday_Graphql_Model\week15.json
```

---

**🏈 Happy Automating! Go get those winning predictions! 🎯**
