# Railway Deployment Guide for Gameday GraphQL Predictor

## 🚀 EASIEST Deployment Options (NO GitHub Required!)

### Option 1: Railway CLI (RECOMMENDED - Super Easy!)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy directly from your folder
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
railway deploy
```

### Option 2: Drag & Drop Deployment
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up** (can use email, no GitHub needed)
3. **Click "New Project"**
4. **Select "Empty Project"**
5. **Drag your entire project folder** into the Railway dashboard
6. **Railway auto-detects** and deploys!

### Option 3: ZIP Upload
1. **Compress your project folder** into a ZIP file
2. **Go to Railway dashboard**
3. **Upload the ZIP file**
4. **Deploy automatically**

## Quick Setup for Railway Deployment

### 1. Prepare Your Repository (SKIP THIS - NOT NEEDED!)
```bash
# IGNORE THIS SECTION - GitHub not required!
# You can use Railway CLI or drag & drop instead
```

### 2. Deploy to Railway (Multiple Easy Options)

1. **Go to [Railway.app](https://railway.app)**
2. **Sign in** with GitHub
3. **Click "New Project"**
4. **Choose "Deploy from GitHub repo"**
5. **Select your repository** (you'll need to push this to GitHub first)
6. **Railway will auto-detect** the Python app and deploy it

### 3. Set Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click **"Variables"** tab
3. Add these variables:
   ```
   CFB_API_KEY=your_actual_college_football_api_key_here
   PORT=8080
   ```

### 4. API Endpoints for Your iOS App

Once deployed, your Railway app will give you a URL like:
`https://your-app-name.railway.app`

**Endpoints:**
- Health Check: `GET /`
- Predict Game: `GET /predict/{home_team_id}/{away_team_id}`
- Predict Game: `POST /predict` with JSON body:
  ```json
  {
    "home_team_id": 356,
    "away_team_id": 194
  }
  ```

**Example Response:**
```json
{
  "success": true,
  "prediction": {
    "home_team": "Illinois",
    "away_team": "Ohio State", 
    "predicted_winner": "Ohio State",
    "home_score": 30,
    "away_score": 36,
    "spread": 6.5,
    "total": 66.0,
    "home_win_probability": 8.1,
    "confidence": 60.6,
    "key_factors": ["Talent disadvantage", "Strong away team superiority"]
  }
}
```

### 5. iOS App Integration

In your iOS app, make HTTP requests to:
```swift
let url = "https://your-app-name.railway.app/predict/356/194"
// Make GET request and parse JSON response
```

### 6. Alternative: GitHub Quick Deploy

If you want to deploy without setting up git:

1. Create a new repo on GitHub
2. Upload these files:
   - `app.py`
   - `graphqlpredictor.py` 
   - `requirements.txt`
   - `Procfile`
   - `railway.json`
   - `runtime.txt`
3. Connect to Railway and deploy

### Files Ready for Deployment:
✅ `app.py` - Flask API server
✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Railway startup command
✅ `railway.json` - Railway configuration
✅ `runtime.txt` - Python version
✅ `graphqlpredictor.py` - Your prediction engine

### Important Notes:
- Make sure to get a valid College Football Data API key
- The API includes CORS headers for iOS app compatibility
- Deployment typically takes 2-3 minutes on Railway
- Railway provides HTTPS automatically