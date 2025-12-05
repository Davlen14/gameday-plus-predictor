# Step 3: Railway API Configuration - Implementation Checklist

## ✅ CURRENT STATE (What's Already Done)

### Infrastructure Already in Place
- ✅ `frontend/src/config.js` - Config system with `VITE_API_URL` support
- ✅ `frontend/.env.development` - Dev environment file exists with `VITE_API_URL=http://127.0.0.1:5002`
- ✅ `frontend/vite.config.js` - Vite properly configured
- ✅ `frontend/src/services/apiClient.js` - API client service exists
- ✅ `frontend/src/store.js` - Zustand store using ApiClient
- ✅ `frontend/src/App.tsx` - Main app component

### What's Working
- ✅ Config system reads environment variables
- ✅ Dev environment file set up correctly
- ✅ Vite build process supports env vars
- ✅ All 24 React components working
- ✅ API client service exists and functional

---

## ❌ WHAT'S BROKEN (The Problem)

### Two Hardcoded URLs That Need Fixing

**1. App.tsx (Line 38) - HARDCODED**
```typescript
const response = await fetch('http://127.0.0.1:5002/predict', {
```
- This is the main prediction fetch call
- Breaks on Railway (localhost doesn't exist)
- Needs to use `CONFIG.API.BASE_URL`

**2. apiClient.js (Line 2) - HARDCODED**
```javascript
const API_BASE_URL = 'http://localhost:5002';
```
- This is the fallback API client
- Also breaks on Railway
- Needs to use `CONFIG.API.BASE_URL`

### Missing File
- ❌ `frontend/.env.production` - Production environment file doesn't exist
- Needed for Railway deployment

---

## 🚀 WHAT TO DO (3 Simple Changes)

### Change 1: Update App.tsx (Line 38)
**File**: `frontend/src/App.tsx`

**Replace this:**
```typescript
const response = await fetch('http://127.0.0.1:5002/predict', {
```

**With this:**
```typescript
import { CONFIG } from './config';
// ... then in handlePrediction function:
const response = await fetch(`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`, {
```

**Why it won't break**: CONFIG has fallback to localhost, so dev still works

---

### Change 2: Update apiClient.js (Line 2)
**File**: `frontend/src/services/apiClient.js`

**Replace this:**
```javascript
const API_BASE_URL = 'http://localhost:5002';
```

**With this:**
```javascript
import { CONFIG } from '../config';
const API_BASE_URL = CONFIG.API.BASE_URL;
```

**Why it won't break**: CONFIG has fallback to localhost, so dev still works

---

### Change 3: Create .env.production
**File**: `frontend/.env.production` (NEW FILE)

**Add this:**
```env
# Production Environment Configuration
VITE_API_URL=https://gameday-graphql-model.up.railway.app
VITE_API_TIMEOUT=10000
```

**Why it won't break**: Only used during production build, dev uses .env.development

---

## 🛡️ SAFETY CHECKS

### Will This Break Development?
- ✅ **NO** - CONFIG has fallback: `import.meta.env.VITE_API_URL || 'http://127.0.0.1:5002'`
- ✅ `.env.development` already has correct URL
- ✅ `npm run dev` will use .env.development automatically

### Will This Break Production?
- ✅ **NO** - `.env.production` will be used during `npm run build`
- ✅ Railway will use the production URL
- ✅ Vite automatically loads correct .env file based on mode

### Will This Break Existing Code?
- ✅ **NO** - Only changing where URLs come from, not the logic
- ✅ All components still work the same
- ✅ API calls still work the same
- ✅ No dependencies to add
- ✅ No breaking changes

---

## 📋 IMPLEMENTATION ORDER

1. **Update App.tsx** - Add import and use CONFIG
2. **Update apiClient.js** - Add import and use CONFIG  
3. **Create .env.production** - Add production environment file
4. **Test locally** - `npm run dev` should still work
5. **Test build** - `npm run build` should work
6. **Mark Step 3 Complete** - Update copilot-instructions.md

---

## ✨ AFTER IMPLEMENTATION

### Local Development (npm run dev)
```
1. Vite loads .env.development
2. VITE_API_URL = http://127.0.0.1:5002
3. App uses CONFIG.API.BASE_URL = http://127.0.0.1:5002
4. Connects to local Flask server ✅
```

### Production Build (npm run build)
```
1. Vite loads .env.production
2. VITE_API_URL = https://gameday-graphql-model.up.railway.app
3. App uses CONFIG.API.BASE_URL = https://gameday-graphql-model.up.railway.app
4. Connects to Railway Flask server ✅
```

---

## 🎯 SUMMARY

**What's broken**: 2 hardcoded URLs + missing production env file
**What to do**: 3 simple changes (2 imports + 1 new file)
**Risk level**: VERY LOW - just connecting existing pieces
**Time to implement**: ~5 minutes
**Chance of breaking**: ~0% - all fallbacks in place


