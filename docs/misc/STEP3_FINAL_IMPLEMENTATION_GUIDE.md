# Step 3: Railway API Configuration - Final Implementation Guide

## 📋 QUICK RECAP

### What We're Doing
Converting hardcoded API URLs to environment-based configuration so the app works on both local development and Railway production.

### Current Problem
- `App.tsx` line 38: Hardcoded `http://127.0.0.1:5002/predict`
- `apiClient.js` line 2: Hardcoded `http://localhost:5002`
- Missing `.env.production` file for Railway deployment

### Solution
- Use existing `config.js` that already supports `VITE_API_URL` environment variable
- Update 2 files to import and use CONFIG
- Create 1 new `.env.production` file
- No breaking changes - all fallbacks in place

### Why It's Safe
- ✅ CONFIG has fallback: `import.meta.env.VITE_API_URL || 'http://127.0.0.1:5002'`
- ✅ `.env.development` already exists with correct URL
- ✅ Vite automatically loads correct .env file based on mode
- ✅ No logic changes, just URL source
- ✅ All 24 React components unaffected
- ✅ All API calls work exactly the same

---

## 🎯 EXACT CHANGES NEEDED

### Change 1: Update `frontend/src/App.tsx`

**Location**: Line 1-2 (add import) and Line 38 (update fetch)

**Current Code (Lines 1-2):**
```typescript
import { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
```

**Change To:**
```typescript
import { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import { CONFIG } from './config';
```

**Current Code (Line 38):**
```typescript
const response = await fetch('http://127.0.0.1:5002/predict', {
```

**Change To:**
```typescript
const response = await fetch(`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`, {
```

**Why This Works:**
- CONFIG.API.BASE_URL reads from `VITE_API_URL` env var
- Falls back to `http://127.0.0.1:5002` if env var not set
- CONFIG.API.ENDPOINTS.PREDICT = `/predict`
- Result: `http://127.0.0.1:5002/predict` (same as before locally)

---

### Change 2: Update `frontend/src/services/apiClient.js`

**Location**: Line 2 (replace hardcoded URL)

**Current Code (Line 2):**
```javascript
const API_BASE_URL = 'http://localhost:5002';
```

**Change To:**
```javascript
import { CONFIG } from '../config';
const API_BASE_URL = CONFIG.API.BASE_URL;
```

**Why This Works:**
- Same CONFIG system as App.tsx
- All 3 methods (getPrediction, healthCheck, getTeams) use API_BASE_URL
- Automatically uses correct URL based on environment

---

### Change 3: Create `frontend/.env.production`

**File**: NEW FILE at `frontend/.env.production`

**Content:**
```env
# Production Environment Configuration
VITE_API_URL=https://gameday-graphql-model.up.railway.app
VITE_API_TIMEOUT=10000
```

**Why This Works:**
- Vite automatically uses this file during `npm run build`
- Railway will use this URL for production
- Matches the Railway deployment URL

---

## 🧪 TESTING PLAN

### Test 1: Local Development (Should Still Work)
```bash
cd frontend
npm run dev
```
- Opens on `http://localhost:5173`
- Uses `.env.development`
- VITE_API_URL = `http://127.0.0.1:5002`
- Should connect to local Flask server ✅

### Test 2: Production Build Preview
```bash
cd frontend
npm run build
npm run preview
```
- Builds with `.env.production`
- VITE_API_URL = `https://gameday-graphql-model.up.railway.app`
- Shows what production will look like ✅

### Test 3: Railway Deployment
```bash
git push origin main
```
- Railway auto-deploys
- Uses production build
- Connects to Railway's Flask server ✅

---

## 📚 REFERENCE DOCUMENTATION

### Files Being Modified
1. **frontend/src/App.tsx** - Main React component
   - Line 1-2: Add import
   - Line 38: Update fetch URL
   - Reference: `handlePrediction` function

2. **frontend/src/services/apiClient.js** - API client service
   - Line 2: Replace hardcoded URL
   - Reference: Used by store.js and potentially other components

3. **frontend/.env.production** - NEW production environment file
   - Reference: Vite automatically loads this during build

### Files NOT Being Modified (But Important to Know)
- `frontend/src/config.js` - Already has correct CONFIG structure
- `frontend/.env.development` - Already has correct dev URL
- `frontend/vite.config.js` - Already configured correctly
- `frontend/src/store.js` - Uses ApiClient, will work automatically
- All 24 React components - No changes needed

### Environment Variable Flow
```
Development:
.env.development → VITE_API_URL=http://127.0.0.1:5002 → CONFIG.API.BASE_URL → App.tsx & apiClient.js

Production:
.env.production → VITE_API_URL=https://gameday-graphql-model.up.railway.app → CONFIG.API.BASE_URL → App.tsx & apiClient.js
```

---

## ⚠️ SAFETY CHECKLIST

Before implementing, verify:
- ✅ `frontend/src/config.js` exists and has CONFIG.API structure
- ✅ `frontend/.env.development` exists with correct URL
- ✅ `frontend/vite.config.js` exists and is configured
- ✅ `frontend/package.json` has build scripts
- ✅ No other files hardcode the API URL (checked via grep)

After implementing, verify:
- ✅ `npm run dev` still works locally
- ✅ `npm run build` completes without errors
- ✅ `npm run preview` shows the app
- ✅ No TypeScript errors in App.tsx
- ✅ No import errors in apiClient.js

---

## 🚀 DEPLOYMENT FLOW

### Local Development
```
1. npm run dev
2. Loads .env.development
3. VITE_API_URL = http://127.0.0.1:5002
4. App connects to local Flask (port 5002)
5. Everything works ✅
```

### Production on Railway
```
1. git push origin main
2. Railway detects changes
3. Runs: npm run build (uses .env.production)
4. VITE_API_URL = https://gameday-graphql-model.up.railway.app
5. App connects to Railway Flask server
6. Everything works ✅
```

---

## 📝 PROMPT FOR AI ASSISTANT

Use this prompt to ask an AI to implement these changes:

---

**PROMPT:**

I need you to implement Step 3 of my Railway API configuration migration. Here's exactly what to do:

**Context:**
- Project: Gameday+ college football prediction platform
- Current issue: 2 hardcoded API URLs that break on Railway
- Solution: Use existing CONFIG system with environment variables
- Reference: See STEP3_FINAL_IMPLEMENTATION_GUIDE.md for full details

**Changes Required:**

1. **Update frontend/src/App.tsx**
   - Add import at top: `import { CONFIG } from './config';`
   - Line 38: Replace `fetch('http://127.0.0.1:5002/predict', {` with `fetch(\`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}\`, {`
   - Reference: handlePrediction function, lines 33-61

2. **Update frontend/src/services/apiClient.js**
   - Line 2: Replace `const API_BASE_URL = 'http://localhost:5002';` with:
     ```javascript
     import { CONFIG } from '../config';
     const API_BASE_URL = CONFIG.API.BASE_URL;
     ```
   - Reference: All 3 methods use API_BASE_URL (getPrediction, healthCheck, getTeams)

3. **Create frontend/.env.production**
   - New file with content:
     ```env
     # Production Environment Configuration
     VITE_API_URL=https://gameday-graphql-model.up.railway.app
     VITE_API_TIMEOUT=10000
     ```

**Safety Checks:**
- CONFIG.API.BASE_URL has fallback to http://127.0.0.1:5002
- .env.development already exists with correct dev URL
- No breaking changes - just changing URL source
- All 24 React components unaffected
- No new dependencies needed

**After Implementation:**
- Test locally: `npm run dev` should work
- Test build: `npm run build` should complete
- Test preview: `npm run preview` should show app
- No TypeScript errors
- No import errors

**Reference Files:**
- frontend/src/config.js - CONFIG structure (don't modify)
- frontend/.env.development - Dev env (don't modify)
- frontend/vite.config.js - Vite config (don't modify)
- STEP3_FINAL_IMPLEMENTATION_GUIDE.md - Full documentation

Please implement these 3 changes carefully and verify nothing breaks.

---


