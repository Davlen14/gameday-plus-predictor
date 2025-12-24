# 🚀 Railway Deployment Fix - Gameday Live Links

## Problem Summary
Your Gameday Live links and other HTML pages weren't opening on Railway, showing either blank pages or errors. Only the `/predictor` React app was working.

## Root Cause
The `start.sh` script (used by Railway's Dockerfile) was starting the wrong Flask application:
- **Was running:** `app:app` (the full prediction stack with complex ML imports)
- **Should run:** `app_master:app` (the coach database API with all template routes)

This mismatch meant Railway was running `app.py` which doesn't properly serve all the HTML template pages, while `app_master.py` (which has all those routes) wasn't running at all.

## What Was Fixed

### 1. start.sh - Fixed App Selection ✅
**File:** `start.sh`

**Changed from:**
```bash
exec gunicorn app:app \
    --bind "0.0.0.0:$PORT" \
```

**Changed to:**
```bash
exec gunicorn app_master:app \
    --bind "0.0.0.0:$PORT" \
```

This now matches the `Procfile` configuration and ensures the correct Flask app runs on Railway.

### 2. .gitignore - Removed Database Block ✅
**File:** `.gitignore`

**Removed:** 
```
coaches_master.db
```

**Replaced with:**
```
# NOTE: coaches_master.db is required for deployment - DO NOT exclude
```

This ensures future database updates can be committed to git. Note: The database files **are already in the repository** with full data (19MB coaches_master.db + 8.4MB predictions.db), so no action needed there.

## Routes That Will Now Work 🎉

After deployment, these routes will load correctly on Railway:

| Route | Description | Status |
|-------|-------------|--------|
| `/` | API documentation homepage | ✅ Works |
| `/gamedaylive` | **Main game cards slider dashboard** | ✅ Fixed |
| `/coaches` | Coaches database list | ✅ Fixed |
| `/coach/<id>` | Individual coach profiles | ✅ Fixed |
| `/teams` | Teams list | ✅ Fixed |
| `/team/<id>` | Team profiles | ✅ Fixed |
| `/nil` | NIL valuations index | ✅ Fixed |
| `/master-dashboard` | Analytics dashboard | ✅ Fixed |
| `/drives-explorer` | Drive analytics explorer | ✅ Fixed |
| `/predictor` | React prediction app | ✅ Still works |
| `/health` | Health check endpoint | ✅ Works |

### API Endpoints Also Available
- `/api/upcoming-games` - Game data for sliders
- `/api/coaches` - All coaches
- `/api/teams` - All teams
- `/api/predictions/game/<id>` - Game predictions
- Many more (see `app_master.py` for full list)

## Testing After Deployment

### 1. Main Page Test
```bash
curl https://your-railway-app.railway.app/gamedaylive
# Should return HTML with game cards
```

### 2. Health Check Test
```bash
curl https://your-railway-app.railway.app/health
# Should return database status JSON
```

### 3. API Test
```bash
curl https://your-railway-app.railway.app/api/upcoming-games
# Should return JSON with games array
```

### 4. Browser Tests
Open in browser:
1. `https://your-railway-app.railway.app/gamedaylive` - Should show game cards slider
2. `https://your-railway-app.railway.app/coaches` - Should show coaches list
3. `https://your-railway-app.railway.app/predictor` - Should still work for predictions

## Architecture Reference

### Two Flask Apps in Project

#### app.py (Full Prediction Stack)
- **Port:** 5002 (local)
- **Purpose:** Complex ML prediction engine with GraphQL
- **Best for:** Local development with full feature set
- **Heavy imports:** graphqlpredictor.py, betting_lines_manager.py, etc.

#### app_master.py (Coach Database API) ✅ Now used on Railway
- **Port:** 5555 (local), 8080 (Railway)
- **Purpose:** Serve HTML templates + coach/team database API
- **Best for:** Railway deployment (lighter, faster startup)
- **Light imports:** Just Flask, sqlite3, pathlib
- **Databases:** 
  - `instance/coaches_master.db` (19MB) - Main data
  - `instance/predictions.db` (8.4MB) - Game predictions

### Deployment Config Files
- `railway.json` → Uses Dockerfile
- `Dockerfile` → Calls `start.sh`
- `start.sh` → Runs `gunicorn app_master:app` ✅
- `Procfile` → Also specifies `app_master:app` ✅

## Verification Checklist

After Railway deployment completes:

- [ ] Visit `/gamedaylive` - Game cards slider loads
- [ ] Visit `/coaches` - Coaches list loads
- [ ] Visit `/predictor` - Prediction tool still works
- [ ] Check `/health` - Shows database connected
- [ ] API call `/api/upcoming-games` - Returns JSON data
- [ ] Check Railway logs - No "FileNotFoundError" for databases
- [ ] Check Railway logs - Shows "app_master:app" in startup message

## If Issues Persist

### Check Railway Logs
```bash
railway logs
```

Look for:
- `✅ Found database at: instance/coaches_master.db` (Good)
- `❌ Database not found` (Bad - contact support)
- `Starting Gameday+ server on port 8080...` (Good)
- `gunicorn app_master:app` in startup (Good)

### Database Size Check
The databases should be ~27MB total. If Railway shows smaller sizes, the files may not have uploaded correctly. You can verify in Railway dashboard under "Files" section.

### Force Re-deployment
If the changes don't take effect:
```bash
git commit --allow-empty -m "Trigger Railway rebuild"
git push origin main
```

## Questions?

If you have issues:
1. Check Railway logs first
2. Verify `/health` endpoint shows database status
3. Check browser console for any JS errors
4. Verify Railway is using the latest commit with these fixes

---

**Last Updated:** December 16, 2024
**Fixed Issues:** Gameday Live links not opening, HTML pages showing errors
**Status:** ✅ Ready for deployment
