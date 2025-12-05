# 🏈 Sportsbook Lines Display Fix - December 2, 2025

## Problem Summary
Sportsbook betting lines were showing "N/A" instead of actual spread/total/moneyline data in the frontend MarketComparison component.

---

## Root Causes Identified

### 1. **Field Name Mismatch** ❌
**File**: `betting_lines_manager.py` (lines 167-168)

**Problem**: API field names were reversed
```python
# WRONG CODE (what we had):
'moneylineHome': provider.get('homeMoneyline', 'N/A'),  # Field doesn't exist!
'moneylineAway': provider.get('awayMoneyline', 'N/A')   # Field doesn't exist!

# CORRECT CODE (what we fixed):
'moneylineHome': provider.get('moneylineHome', 'N/A'),  # ✅ Matches API
'moneylineAway': provider.get('moneylineAway', 'N/A')   # ✅ Matches API
```

**Impact**: All moneyline data showed as "N/A" because we were looking for fields that don't exist in the API response.

---

### 2. **GraphQL Data Structure Not Supported** ❌
**File**: `betting_lines_manager.py` (lines 362-380)

**Problem**: Code only handled `Currentweekgames.json` format, not live GraphQL API format

**Old Code** (only worked with JSON file):
```python
if 'bettingLines' in game:
    betting_lines = game['bettingLines']
    providers_data = betting_lines.get('allProviders', [])
```

**New Code** (handles both formats):
```python
# Handle GraphQL live data format (lines array)
if 'lines' in game:
    lines_data = game['lines']
    
    # Calculate consensus from lines
    spreads = [line.get('spread') for line in lines_data if line.get('spread') is not None]
    totals = [line.get('overUnder') for line in lines_data if line.get('overUnder') is not None]
    
    avg_spread = sum(spreads) / len(spreads) if spreads else 0
    avg_total = sum(totals) / len(totals) if totals else 0
    
    # Format spread display
    if avg_spread > 0:
        formatted_spread = f"{game['awayTeam']} -{avg_spread:.1f}"
    elif avg_spread < 0:
        formatted_spread = f"{game['homeTeam']} {abs(avg_spread):.1f}"
    else:
        formatted_spread = "Pick'em"
    
    # Use lines directly as providers
    providers_data = lines_data
    providers_list = lines_data
    
    # Use first provider for specific line info
    first_provider = providers_data[0] if providers_data else {}
    
# Handle Currentweekgames.json format (fallback)
elif 'bettingLines' in game:
    # ... existing code
```

**Impact**: System was fetching live Week 15 data from GraphQL but couldn't parse it, resulting in crashes.

---

### 3. **Missing Variable Assignments** ❌
**File**: `betting_lines_manager.py`

**Problem**: When GraphQL format was added, forgot to set critical variables:
- `formatted_spread` - caused `UnboundLocalError`
- `first_provider` - caused `UnboundLocalError`

**Error in Logs**:
```
UnboundLocalError: local variable 'first_provider' referenced before assignment
```

**Impact**: Backend crashed silently and returned simplified API response without betting analysis.

---

### 4. **Week Data Mismatch** ⚠️
**Files**: `Currentweekgames.json` vs GraphQL API

**Problem**: 
- JSON file had **Week 14** data (Ohio State vs Michigan - Nov 29, 2025)
- Current week is **Week 15** (Dec 6, 2025)
- Frontend defaulted to Ohio State vs Michigan (outdated game)

**Fix**: 
- Updated `TeamSelector.tsx` default teams from Ohio State/Michigan → Georgia/Alabama
- GraphQL API now fetches live Week 15 data (32 games)

---

## Data Structure Comparison

### GraphQL API Format (Week 15 - Live Data)
```json
{
  "id": 401777351,
  "homeTeam": "Alabama",
  "awayTeam": "Georgia",
  "lines": [
    {
      "provider": "ESPN Bet",
      "spread": 2.5,
      "overUnder": 47.5
    },
    {
      "provider": "DraftKings",
      "spread": 2.5,
      "overUnder": null
    },
    {
      "provider": "Bovada",
      "spread": 2.5,
      "overUnder": 48
    }
  ]
}
```

### Currentweekgames.json Format (Week 14 - Cached Data)
```json
{
  "gameId": 401756967,
  "homeTeam": { "name": "TCU" },
  "awayTeam": { "name": "Cincinnati" },
  "bettingLines": {
    "consensus": {
      "spread": -3.83,
      "total": 56.5
    },
    "allProviders": [
      {
        "provider": "Bovada",
        "spread": -3.5,
        "overUnder": 56.5,
        "moneylineHome": -185,
        "moneylineAway": 160
      }
    ]
  }
}
```

---

## Files Modified

### 1. `betting_lines_manager.py`
- **Lines 167-168**: Fixed field name mapping (`homeMoneyline` → `moneylineHome`)
- **Lines 362-385**: Added GraphQL `lines` format support
- **Lines 155-162**: Added provider name handling for nested objects

### 2. `frontend/src/components/figma/TeamSelector.tsx`
- **Lines 75-77**: Changed default teams from Ohio State/Michigan → Georgia/Alabama

### 3. `test_sportsbook_display.html` (Created)
- New standalone HTML test page to debug API responses
- Shows raw JSON and formatted display
- Helpful for future debugging

---

## Testing Results

### Before Fix:
```
Live Sportsbook Lines

Bovada
├── Spread: N/A
├── Total: 56.5
└── Moneyline: N/A / N/A

ESPN Bet
├── Spread: N/A
├── Total: 58
└── Moneyline: N/A / N/A
```

### After Fix:
```
Live Sportsbook Lines

ESPN Bet
├── Spread: Georgia -2.5
├── Total: 47.5
└── Moneyline: N/A / N/A (GraphQL doesn't provide)

DraftKings
├── Spread: Georgia -2.5
├── Total: N/A
└── Moneyline: N/A / N/A

Bovada
├── Spread: Georgia -2.5
├── Total: 48.0
└── Moneyline: N/A / N/A
```

**Note**: Moneylines still show "N/A" because the GraphQL API doesn't include moneyline data in the `lines` query. This would require a different API endpoint or the cached JSON data.

---

## Why This Took 2 Days to Fix

### 1. **Silent Errors** 🤫
Flask error handling was catching exceptions and returning simplified responses without betting analysis. No visible error messages in the frontend.

### 2. **Python Module Caching** 💾
Even after code fixes, Python was loading old code from `__pycache__` directories. Had to:
- Clear cache: `find . -name "*.pyc" -delete`
- Force restart: `killall python`
- Multiple server restarts to get fresh code loaded

### 3. **Multiple Data Sources** 🔄
System uses 3 different data sources:
- Live GraphQL API (Week 15)
- `Currentweekgames.json` (Week 14)
- `week15.json` (backup)

Had to trace through code to find which source was active.

### 4. **Hidden Stack Traces** 📚
The actual error was buried in backend logs:
```
UnboundLocalError: local variable 'first_provider' referenced before assignment
```

Frontend just showed empty data, no indication of backend crash.

### 5. **Backwards Field Names** 🔄
The field name swap (`homeMoneyline` vs `moneylineHome`) was subtle and easy to miss. Required careful comparison of:
- API response structure (actual JSON)
- Code expectations (what we were querying)
- Data flow (where values were used)

---

## Prevention Checklist for Future

- [ ] **Add logging**: Print API response structure when parsing betting lines
- [ ] **Add validation**: Check if required fields exist before accessing
- [ ] **Better error handling**: Return error details to frontend instead of silent fallback
- [ ] **API response schema**: Document expected structure for each data source
- [ ] **Integration tests**: Automated tests that verify betting lines display correctly
- [ ] **Clear cache script**: Add `make clean` or similar to clear Python cache

---

## API Data Source

**Primary**: College Football Data GraphQL API
- **URL**: `https://graphql.collegefootballdata.com/v1/graphql`
- **Auth**: Bearer token in `betting_lines_manager.py`
- **Query**: Fetches games with `lines` field for Week 15, 2025

**Fallback**: `Currentweekgames.json` (Week 14 data)
- Contains full betting lines with moneylines
- Used when GraphQL API is unavailable

---

## Current Limitations

1. **No Moneyline Data from GraphQL**: The live API doesn't return moneyline odds in the `lines` query
2. **Limited Sportsbooks**: Only 3 books (ESPN Bet, DraftKings, Bovada) available for most games
3. **Null Values**: Some books don't have `overUnder` data (shows as `null`)

---

## Summary

**Lines Changed**: ~50 lines across 2 files  
**Time to Fix**: 2 days (due to caching, silent errors, debugging)  
**Complexity**: Medium (4 interconnected issues)  
**Status**: ✅ **FIXED** - Sportsbook lines now display correctly with live Week 15 data

---

**Fixed by**: AI Assistant (Claude Sonnet 4.5)  
**Date**: December 2, 2025  
**Commit**: Update `betting_lines_manager.py` and `TeamSelector.tsx` to support GraphQL betting lines
