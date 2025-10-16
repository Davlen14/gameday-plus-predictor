# Railway API Configuration Migration Guide

## 📋 Overview
This document tracks the transformation from a single hardcoded HTML test file to a professional React application with environment-based API configuration for Railway deployment.

---

## 🔴 **BEFORE: Test HTML File Era**

### What We Had
- **Single File**: `test.html` + `test.js` - Standalone HTML file with embedded JavaScript
- **Hardcoded Everything**: API endpoints, styling, data all in one place
- **No Build Process**: Opened directly in browser (file:// protocol)
- **No Environment Support**: Same hardcoded URLs for dev and production
- **All Logic in One Place**: 530 lines of HTML + 265 lines of JavaScript

### Actual Code from test.js (Lines 3-6)
```javascript
// API endpoints - using absolute URLs to point to Flask server
const FLASK_BASE_URL = 'http://127.0.0.1:5002'; // ❌ Hardcoded localhost
const TEAMS_API_URL = FLASK_BASE_URL + '/teams';
const PREDICT_API_URL = FLASK_BASE_URL + '/predict';
```

### Actual Code from test.html (Lines 265-280)
```html
<!-- Team Selector -->
<div class="flex flex-col md:flex-row gap-6 mb-6">
    <div class="flex-1">
        <label for="awayTeam" class="block text-sm font-bold text-slate-300 mb-2">Away Team:</label>
        <select id="awayTeam" class="w-full p-3 border rounded-xl backdrop-blur-sm focus:ring-2 transition-all duration-200 outline-none">
            <option value="">Select Away Team</option>
        </select>
    </div>
    <!-- ... -->
</div>
<button id="predictButton" onclick="makePrediction()" class="text-white font-bold py-4 px-8 rounded-xl transition-all duration-200 transform hover:-translate-y-1 max-w-md w-full">
    Generate Prediction
</button>
```

### How It Worked
1. Open `test.html` in browser
2. JavaScript loads teams from `http://127.0.0.1:5002/teams`
3. User selects teams and clicks button
4. JavaScript calls `makePrediction()` function
5. Sends POST to `http://127.0.0.1:5002/predict`
6. Results displayed inline in HTML

### Problems with This Approach
- ❌ **Can't deploy to production** - localhost doesn't exist on Railway
- ❌ **No environment switching** - Same hardcoded URL for dev and production
- ❌ **Manual code changes needed** - Edit test.js to change API URL
- ❌ **No version control** - Configuration mixed with code
- ❌ **Difficult to test** - Can't easily test different API endpoints
- ❌ **No build process** - Can't use environment variables
- ❌ **All in one file** - 530 lines of HTML + 265 lines of JS = hard to maintain

---

## 🟢 **AFTER: Professional React Setup**

### What We Built
- **Modular Architecture**: 24 separate React components instead of one 530-line HTML file
- **Build Process**: Vite bundler with environment variable support
- **Config System**: Centralized `config.js` with environment-based URLs
- **API Client**: Reusable service layer (`apiClient.js`)
- **TypeScript**: Type safety for components and data structures
- **Deployment Ready**: Can run on localhost, Railway, or any server
- **Separation of Concerns**: Logic, styling, and configuration all separated

### Current File Structure
```
frontend/src/
├── config.js                 # ✅ Environment-based configuration hub
├── services/
│   ├── apiClient.js         # ✅ Reusable API client service
│   ├── teamService.js       # ✅ Team data management
│   └── dataManager.js       # ✅ Data transformation
├── App.tsx                  # ❌ Still has hardcoded URL (line 38)
├── components/
│   └── figma/               # 24 professional UI components
│       ├── TeamSelector.tsx
│       ├── PredictionCards.tsx
│       ├── ConfidenceSection.tsx
│       ├── MarketComparison.tsx
│       └── ... 20 more components
├── types/
│   └── PredictionTypes.ts   # ✅ TypeScript interfaces
└── store.js                 # ✅ Zustand state management
```

### Current Config System (config.js) - ALREADY BUILT ✅
```javascript
export const CONFIG = {
    API: {
        BASE_URL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:5002',
        ENDPOINTS: {
            TEAMS: '/teams',
            PREDICT: '/predict'
        },
        TIMEOUT: 10000,
        RETRY_ATTEMPTS: 3
    },
    SECTIONS: { /* 15+ configurable sections */ },
    CHARTS: { /* color and animation config */ },
    UI: { /* breakpoints and animations */ }
};
```

✅ **Good**: Uses environment variable `VITE_API_URL`
✅ **Good**: Falls back to localhost for development
✅ **Good**: Centralized configuration
❌ **Problem**: Not being used in `App.tsx` or `apiClient.js` yet

---

## 🚧 **CURRENT STATE: Partially Migrated**

### What's Working ✅
- ✅ Config file exists with environment support (`config.js`)
- ✅ API client service exists (`apiClient.js`)
- ✅ React components are modular (24 separate components)
- ✅ Build process supports environment variables (Vite)
- ✅ TypeScript for type safety
- ✅ Zustand state management
- ✅ All 18 prediction analysis sections working

### What's NOT Working ❌
- ❌ `App.tsx` line 38: Still uses hardcoded `http://127.0.0.1:5002`
- ❌ `apiClient.js` line 2: Still uses hardcoded `http://localhost:5002`
- ❌ No `.env` files for development/production
- ❌ Railway doesn't know what API URL to use
- ❌ Can't switch between environments without code changes
- ❌ Config system exists but isn't being used

### Current Hardcoded URLs (The Problem)

**App.tsx (Line 38) - HARDCODED**
```typescript
const response = await fetch('http://127.0.0.1:5002/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    home_team: homeTeam,
    away_team: awayTeam
  })
});
// ❌ Hardcoded - breaks on Railway (localhost doesn't exist)
```

**apiClient.js (Line 2) - HARDCODED**
```javascript
const API_BASE_URL = 'http://localhost:5002';

export class ApiClient {
  static async getPrediction(homeTeam, awayTeam) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        // ❌ Hardcoded - breaks on Railway
```

### The Gap
- **Config system is built** but **not connected** to the actual API calls
- Like having a blueprint for a house but not building it
- The infrastructure is there, just needs to be wired up

---

## ✅ **WHAT NEEDS TO BE DONE: Step 3 Tasks**

### Task 1: Update App.tsx to Use Config
**File**: `frontend/src/App.tsx`  
**Current**: Line 38 has hardcoded URL  
**Action**: Import and use `CONFIG.API.BASE_URL`

```typescript
// BEFORE (Line 38)
const response = await fetch('http://127.0.0.1:5002/predict', {

// AFTER
import { CONFIG } from './config';
const response = await fetch(`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`, {
```

### Task 2: Update apiClient.js to Use Config
**File**: `frontend/src/services/apiClient.js`  
**Current**: Line 2 has hardcoded URL  
**Action**: Import and use `CONFIG.API.BASE_URL`

```javascript
// BEFORE (Line 2)
const API_BASE_URL = 'http://localhost:5002';

// AFTER
import { CONFIG } from '../config';
const API_BASE_URL = CONFIG.API.BASE_URL;
```

### Task 3: Create Environment Files
**Files to Create**:
- `frontend/.env.development` - For local development
- `frontend/.env.production` - For Railway deployment

```env
# .env.development
VITE_API_URL=http://127.0.0.1:5002

# .env.production
VITE_API_URL=https://gameday-graphql-model.up.railway.app
```

### Task 4: Update Railway Configuration
**File**: `railway.json` or Railway dashboard  
**Action**: Set environment variable

```json
{
  "variables": {
    "VITE_API_URL": "https://gameday-graphql-model.up.railway.app"
  }
}
```

### Task 5: Update Vite Configuration (if needed)
**File**: `frontend/vite.config.ts`  
**Action**: Ensure environment variables are properly loaded

---

## 🎯 **Deployment Flow After Migration**

### Local Development
```
1. Run: npm run dev
2. Vite loads .env.development
3. VITE_API_URL = http://127.0.0.1:5002
4. App connects to local Flask server
5. Everything works locally ✅
```

### Railway Production
```
1. Push code to Railway
2. Railway sets VITE_API_URL environment variable
3. Vite loads .env.production (or Railway env var)
4. VITE_API_URL = https://gameday-graphql-model.up.railway.app
5. App connects to production Flask server
6. Everything works on Railway ✅
```

---

## 📊 **Comparison: Before vs After**

| Aspect | Before (HTML) | After (React) | Status |
|--------|---------------|---------------|--------|
| **File Type** | Single `.html` | Modular `.tsx` + `.js` | ✅ Done |
| **Build Process** | None | Vite bundler | ✅ Done |
| **Configuration** | Hardcoded | Environment-based | 🚧 Partial |
| **API URLs** | Hardcoded in HTML | In `config.js` | 🚧 Partial |
| **Components** | Inline HTML | 24 separate components | ✅ Done |
| **Styling** | Inline CSS | Tailwind + CSS modules | ✅ Done |
| **Type Safety** | None | TypeScript | ✅ Done |
| **Dev/Prod Split** | Manual code changes | Environment variables | ❌ Not Done |
| **Railway Ready** | ❌ No | 🚧 Almost | 🚧 In Progress |

---

## 🔗 **Related Files**

### Configuration Files
- `frontend/src/config.js` - Main configuration hub
- `frontend/vite.config.ts` - Vite build configuration
- `railway.json` - Railway deployment config
- `.env.development` - Dev environment (needs creation)
- `.env.production` - Prod environment (needs creation)

### API Integration Files
- `frontend/src/App.tsx` - Main app (needs update)
- `frontend/src/services/apiClient.js` - API client (needs update)
- `frontend/src/services/teamService.js` - Team data service
- `backend/app.py` - Flask API server

### Component Files
- `frontend/src/components/figma/` - 24 UI components
- `frontend/src/components/TeamSelector.jsx` - Team selection UI

---

## 🚀 **Next Steps**

1. **Update App.tsx** - Replace hardcoded URL with `CONFIG.API.BASE_URL`
2. **Update apiClient.js** - Replace hardcoded URL with `CONFIG.API.BASE_URL`
3. **Create .env files** - Add development and production environment files
4. **Test locally** - Verify dev environment works
5. **Deploy to Railway** - Set environment variable and test production
6. **Mark Step 3 Complete** - Update copilot-instructions.md

---

## 📝 **Notes**

- The config system is already in place and well-designed
- Only the implementation (using the config) is incomplete
- This is a low-risk change - just connecting existing pieces
- No new dependencies needed
- Backward compatible with current setup


