# 🏈 Gameday+ AI Development Guide

> **🤖 Essential Knowledge for AI Coding Agents**  
> Complete architectural understanding and development patterns for the Gameday+ college football prediction platform.

## 🎯 Architecture Overview

Gameday+ is a **sophisticated prediction engine** with a modern React frontend:
- **Core Engine**: `LightningPredictor` class in `graphqlpredictor.py` (3,549 lines of advanced ML)
- **API Layer**: Flask server (`app.py`) that wraps the engine for web consumption  
- **Frontend**: React TypeScript app with 24+ glassmorphism UI components
- **Data Sources**: College Football Data GraphQL API, EPA metrics, sportsbook lines, weather data

## � Development Workflow

### **Starting the Full Stack**
```bash
./start-fullstack.sh  # Launches both servers in macOS Terminal tabs
```
- **Backend**: Flask on `http://localhost:5002` 
- **Frontend**: React on `http://localhost:5173`
- **Script validates**: `app.py` exists, `frontend/` directory, `.venv` virtual environment

### **Critical Development Patterns**

#### **1. Data Flow Architecture**
```
React UI → Flask /predict → LightningPredictor → GraphQL APIs → JSON Response → UI Components
```

#### **2. Team Data Management** 
- **Source**: `fbs.json` (130+ FBS teams with IDs, names, logos, colors)
- **Conversion**: `get_team_id()` function handles name→ID mapping with fuzzy matching
- **Frontend**: `teamService.js` loads teams locally (no API calls needed)

#### **3. Prediction Engine Integration**
- **Core**: `LightningPredictor.predict_game()` method processes all analysis
- **Output**: 18 comprehensive analysis sections (EPA, market comparison, confidence, etc.)
- **API Wrapper**: Flask formats engine output as structured JSON for React consumption

## � Key Data Patterns

### **API Response Structure**
The `/predict` endpoint returns structured JSON matching these UI components:
```json
{
  "confidence": { "overall_confidence": 85.2, "breakdown": {...} },
  "contextual_analysis": { "weather": {...}, "rankings": {...} },
  "final_prediction": { "spread": -7.5, "total": 67.0 },
  "market_comparison": { "sportsbooks": [...] }
}
```

### **Known Hardcoded Data Issues** ⚠️
**Priority fixes needed:**
- **Weather data**: Always shows 73.2°F, 8.1mph wind, 0.0 precipitation (`app.py` lines 271-274)
- **Confidence breakdown**: Static base values of 88%, +3%, +8% (`app.py` lines 257-261)  
- **API endpoint**: Frontend hardcoded to `localhost:5002` (needs environment config)

### **Component Integration Pattern**
React components expect prediction data via props:
```tsx
interface ComponentProps {
  predictionData?: {
    confidence?: { overall_confidence: number; breakdown: {...} };
    // 18+ other analysis sections
  };
}
```

## 🔧 Development Guidelines

### **When Working with Predictions**
1. **Use Flask `/predict` endpoint** - never call GraphQL directly from frontend
2. **Test with both formats**: `POST /predict` (JSON) and `GET /predict/home/away` (URL params)  
3. **Debug with `run.py`** - shows detailed terminal output of same prediction logic
4. **Validate team names** with `fbs.json` - supports fuzzy matching and aliases

### **Debugging Tools**
- **`debug_frontend_data.html`**: Test frontend data flow in browser
- **`test_api.py`**: Validate Flask API endpoints  
- **`run.py`**: See detailed prediction analysis in terminal
- **`python app.py`**: Start backend only for API testing

### **Component Architecture**
- **24 Figma components** in `frontend/src/components/figma/`
- **Glassmorphism styling** with Tailwind + custom CSS
- **Real-time data binding** via Zustand store (`store.js`)
- **TypeScript interfaces** for prediction data types

### **Deployment Configuration**
- **Railway**: Uses `Procfile`, `railway.json`, `build.sh`  
- **Gunicorn**: Production WSGI server with 120s timeout
- **Environment**: Python 3.11+ (specified in `runtime.txt`)

## 🎯 Common Tasks

### **Adding New Analysis Sections**
1. Extend `LightningPredictor` class in `graphqlpredictor.py`
2. Update JSON formatter in `app.py` 
3. Create React component in `frontend/src/components/figma/`
4. Add component to main `App.tsx`

### **Fixing Data Integration**
1. Check data structure in browser DevTools Network tab
2. Verify API response matches component props interface
3. Use fallback/demo data while debugging live integration

### **Performance Optimization** 
- GraphQL queries are batched in single call (`predict_game()` method)
- Frontend team data loaded once from `fbs.json` 
- Heavy computation cached in prediction engine

## 🎯 **Current Project Status & Known Issues**

### **✅ What's Working Perfectly**
- ✅ **React Frontend**: 24 sophisticated glassmorphism components with real data
- ✅ **Flask Backend**: Comprehensive prediction engine with 18 analysis sections  
- ✅ **Data Integration**: Teams, players, EPA, coaching records, AP polls all dynamic
- ✅ **Market Analysis**: Live sportsbook integration with value betting recommendations
- ✅ **Railway Deployment**: Configured with Procfile, railway.json, build.sh
- ✅ **UI Components**: All 24 Figma components displaying real prediction data
- ✅ **Team Selection**: Dynamic team dropdowns with real FBS data
- ✅ **Player Impact**: Enhanced player analysis with efficiency scores
- ✅ **Advanced Metrics**: EPA comparisons, field position, drive efficiency

### **🔍 Current Issues Identified**

#### **1. ✅ Weather Data System (COMPLETED - STEP 2 ✓)**
**Solution Implemented**: Weather system now uses real API data from College Football Data GraphQL API:
- Temperature: Uses actual game weather (e.g., 81.3°F for Miami vs Louisville)
- Wind Speed: Uses actual conditions (e.g., 6.9 mph for Miami vs Louisville)  
- Precipitation: Real weather data from API
- All weather data now dynamic and game-specific instead of hardcoded values

**Files Fixed**:
- ✅ `graphqlpredictor.py`: Enhanced weather data capture from currentGame API
- ✅ `app.py`: Updated Flask API to serve real weather data
- ✅ **Status**: Production ready with 4 core weather fields displaying correctly

#### **2. ✅ Confidence Calculations (COMPLETED - STEP 2 ✓)**
**Solution Implemented**: Model confidence breakdown now uses dynamic calculations:
- Base Data Quality: Calculated from actual data quality metrics
- Consistency Factor: Dynamic based on prediction consistency
- Differential Strength: Calculated from team differential analysis

**Files Fixed**:
- ✅ `app.py`: Updated confidence calculations with dynamic values
- ✅ **Status**: Production ready with real confidence metrics

#### **3. ✅ Advanced Coach Rankings System (COMPLETED - STEP 2.5 ✓)**
**Solution Implemented**: Comprehensive 9-factor coaching analysis emphasizing 2025 performance:
- **Data-Driven vs Reputation**: See `ESPN_vs_DATA_RANKINGS.md` for comparison with ESPN's May 2025 subjective rankings
- **Talent Context**: Penalizes coaches who underachieve with elite rosters (Kirby Smart #37 despite ESPN #1)
- **2025 Heavy Weighting**: 25% current season + 15% weighted recent (2025=50%, 2024=30%, 2023=15%, 2022=5%)
- **9 Factors**: Season performance, recent trend, career win%, talent context, big games, recruiting, NFL development, betting, consistency
- **Normalization**: Top coach = 99/100 with proportional scaling

**Key Rankings**:
- #1 Ryan Day (99.0/100): 12-0 in 2025, meeting elite expectations
- #2 Kalen DeBoer (81.0/100): 10-2 at Alabama, solid post-Saban transition
- #3 Lane Kiffin (75.7/100): 11-1 at Ole Miss, elite 2025 season
- #7 Curt Cignetti (63.8/100): 12-0 at Indiana, +59% hottest trend

**Files**:
- ✅ `advanced_coach_rankings.py`: Main ranking engine
- ✅ `data/coaches_advanced_rankings.json`: Output with enhanced_analysis
- ✅ `frontend/src/data/coaches_advanced_rankings.json`: Frontend copy
- ✅ `ESPN_vs_DATA_RANKINGS.md`: Detailed comparison explaining differences
- ✅ `graphqlpredictor.py`: Updated to use coaches_advanced_rankings.json
- ✅ **Status**: Production ready, dramatically different from ESPN's reputation-based rankings

#### **3. Railway API Configuration (Enhancement - STEP 3 ⏳)**
**Problem**: React app currently points to localhost for API calls
**File to Fix**: `frontend/src/App.tsx` has hardcoded localhost URL
**Solution**: Use config system for dynamic API endpoint based on environment

### **🚀 Project Transformation Achievement**
**Before**: 3,000+ line HTML file with basic styling and hardcoded data
**After**: Professional React application with:
- 24 sophisticated UI components
- TypeScript for type safety
- Glassmorphism design with animations
- Environment-based configuration
- Zustand state management
- Real-time prediction engine integration

### **📊 Technical Excellence**
- **Database**: 155 QBs, 616 WRs analyzed per prediction
- **Market Integration**: 3+ sportsbooks with live line comparisons
- **Advanced Analytics**: EPA, success rates, field position metrics
- **Coaching Analysis**: Historical performance vs ranked teams
- **Player Impact**: Individual efficiency scores and team differentials

---

*⚡ Focus on the prediction engine (`graphqlpredictor.py`) and API wrapper (`app.py`) - these contain the core business logic. The React frontend is primarily a beautiful interface to display the engine's sophisticated analysis.*