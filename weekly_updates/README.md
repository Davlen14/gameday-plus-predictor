# 📅 Weekly Updates System

**Purpose**: Centralized location for all weekly data update files to keep the prediction engine current.

---

## 📂 What Goes in This Folder

### **Every Monday (New Week):**

1. **`ap_poll_week{N}.json`** - Current week's AP Top 25 rankings
   - Fetch from: https://api.collegefootballdata.com/rankings
   - Format: Standard AP Poll JSON with rank, school, conference, votes, points

2. **`week{N}_games.json`** - Current week's game schedule with betting lines
   - Generate using: `weekly_update_scripts/week11_graphql_fetcher.py` (update week number)
   - Contains: Games, betting lines, media info, rankings embedded
   - Replaces: Root `Currentweekgames.json` (copy this file there after generation)

3. **Player Analysis Files (Optional - if fresh data needed):**
   - `comprehensive_qb_analysis_2025_week{N}.json`
   - `comprehensive_rb_analysis_2025_week{N}.json`
   - `comprehensive_wr_analysis_2025_week{N}.json`
   - `comprehensive_te_analysis_2025_week{N}.json`
   - `comprehensive_db_analysis_2025_week{N}.json`
   - `comprehensive_lb_analysis_2025_week{N}.json`
   - `comprehensive_dl_analysis_2025_week{N}.json`
   - Generate using: Scripts in `weekly_update_scripts/`
   - Copy to: `backtesting 2/` directory after generation

---

## 🔄 Weekly Update Workflow

### **Step 1: Generate Fresh Data (Monday Morning)**
```bash
cd ~/Desktop/Gameday_Graphql_Model/weekly_update_scripts

# Update week number in fetcher script first
# Then run it
python week11_graphql_fetcher.py  # Update to current week

# Move generated file
mv Currentweekgames.json ../weekly_updates/week{N}_games.json
cp ../weekly_updates/week{N}_games.json ../Currentweekgames.json
```

### **Step 2: Fetch AP Poll**
```bash
# Using curl (replace week number)
curl -s "https://api.collegefootballdata.com/rankings?year=2025&seasonType=regular" \
  -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
  | jq '.[-1].polls[] | select(.poll == "AP Top 25")' \
  > weekly_updates/ap_poll_week{N}.json
```

### **Step 3: Update Frontend AP Data**
```bash
# Manually add week_{N} node to frontend/src/data/ap.json
# Use the data from ap_poll_week{N}.json
```

### **Step 4: Update Code Constants**
Edit `predictor/core/lightning_predictor.py`:
- Line 319: `self.current_week = {N}`
- Line 933: `$currentWeek: smallint = {N}`
- Lines 425-431: Update player file timestamps if regenerated

### **Step 5: Update Frontend Components**
- `frontend/src/components/figma/TeamSelector.tsx` - Update week, default teams, quick games
- `frontend/src/components/figma/Header.tsx` - Update demo data to featured game
- `frontend/src/components/figma/APPollRankings.tsx` - Update week fallback

---

## 📋 Quick Reference Checklist

**Files That MUST Update Weekly:**
- [ ] `Currentweekgames.json` (root) - Generated from fetcher script
- [ ] `frontend/src/data/ap.json` - Add new week_{N} node
- [ ] `predictor/core/lightning_predictor.py` - Lines 319, 933 (week constants)
- [ ] Frontend components - Week references and featured games

**Files That CAN Update Weekly (Optional):**
- [ ] Player analysis files (7 files) - Only if running fresh analysis
- [ ] `predictor/core/lightning_predictor.py` lines 425-431 - Only if player files updated

**Files That NEVER Update Weekly:**
- ✅ `fbs_teams_stats_only.json` - Season stats
- ✅ `react_power5_efficiency.json` - Season efficiency
- ✅ `power5_drives_only.json` - Historical drives
- ✅ `complete_win_probabilities.json` - Historical probabilities
- ✅ `coaches_with_vsranked_stats.json` - Season coaching stats
- ✅ `fbs_offensive_stats.json` - Season offensive stats
- ✅ `fbs_defensive_stats.json` - Season defensive stats
- ✅ All other frontend/src/data/*.json files

---

## 🎯 Expected Folder Structure After Week 13 Update

```
weekly_updates/
├── README.md (this file)
├── ap_poll_week12.json
├── ap_poll_week13.json
├── week12_games.json
├── week13_games.json
└── (player analysis files if regenerated)
```

---

## 💡 Pro Tips

1. **Keep old week files** - Useful for historical reference and debugging
2. **Always backup** - Copy `Currentweekgames.json` before replacing
3. **Verify data** - Use `jq` to check JSON structure before copying
4. **Test after updates** - Run prediction on featured game to verify
5. **Git commit after each week** - Track changes systematically

---

## 🚨 Common Mistakes to Avoid

❌ Forgetting to update BOTH week constants (line 319 AND 933)  
❌ Not copying generated games file to root `Currentweekgames.json`  
❌ Adding AP poll data without proper week_{N} node structure  
❌ Updating static season files unnecessarily  
❌ Forgetting to update frontend component week references  

---

**Last Updated**: Week 12 (November 13, 2025)  
**Next Update Due**: Week 13 (November 18-20, 2025)
