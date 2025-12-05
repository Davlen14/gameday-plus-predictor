# 🚀 N8N Quick Start - Get Running in 2 Minutes

## Step 1️⃣: Start Your API Server

```bash
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
python app.py
```

Wait for: `* Running on http://0.0.0.0:5002`

---

## Step 2️⃣: Open N8N

Go to your n8n instance (usually `http://localhost:5678`)

---

## Step 3️⃣: Import the Workflow

1. Click **"+ Add workflow"** (top right)
2. Click the **3 dots menu** → **"Import from File"**
3. Select: `n8n_gameday_workflow.json` (in this folder)
4. Click **"Save"**

---

## Step 4️⃣: Run It

1. Click **"Execute Workflow"** button (top right)
2. Wait 30-60 seconds (prediction takes time)
3. Click **"Format Results"** node to see the prediction

---

## 🎯 What You'll Get

```json
{
  "game": "Ohio State vs Michigan",
  "prediction": "Spread: -7.5",
  "total": "Total: 67.0",
  "win_probability": "Win Prob: 78.0%",
  "confidence": "Confidence: 85.0%",
  "recommendation": "Bet Ohio State -7.5"
}
```

---

## 🔧 Change the Teams

1. Click **"Get Game Prediction"** node
2. Under **"Body Parameters"**:
   - Change `home_team` value (e.g., "Alabama")
   - Change `away_team` value (e.g., "Georgia")
3. Click **"Execute Workflow"** again

---

## 🎲 Valid Team Names

Use **exact** school names:
- ✅ "Ohio State" (not "OSU")
- ✅ "Michigan" (not "U of M")
- ✅ "Alabama", "Georgia", "Texas", etc.

Get full list: `http://localhost:5002/teams`

---

## 🔥 Next Steps

### Add Discord/Slack Output
1. Add **Discord** or **Slack** node after "Format Results"
2. Configure webhook/credentials
3. Send prediction notifications

### Automate Weekly Predictions
1. Replace "Manual Trigger" with **"Schedule Trigger"**
2. Set to run: **"Every Saturday at 9:00 AM"**
3. Add **"Code"** node to loop through week's games

### Batch Multiple Games
1. Add **"Code"** node with game list:
```javascript
return [
  { json: { home_team: "Ohio State", away_team: "Michigan" } },
  { json: { home_team: "Alabama", away_team: "Georgia" } },
  { json: { home_team: "Texas", away_team: "Oklahoma" } }
];
```
2. Add **"Split In Batches"** node
3. Connect to "Get Game Prediction"

---

## ⚠️ Troubleshooting

**"Connection refused" error?**
→ Make sure `python app.py` is running

**"Team not found" error?**
→ Check team name spelling: `http://localhost:5002/teams`

**Takes too long?**
→ Normal! Predictions analyze 155 QBs + 616 WRs. Wait 60 seconds.

**Want to see raw data?**
→ Click "Get Game Prediction" node to see full 18-section analysis

---

## 📚 More Examples

Check `N8N_INTEGRATION_GUIDE.md` for:
- Weekly accuracy tracking
- Betting value finder
- Player props predictions
- Parlay builder
- Live game monitoring
