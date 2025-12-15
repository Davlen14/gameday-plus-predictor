# 🤖 AI Cleanup Prompt - Gameday+ Project

## Copy this prompt to give an AI agent:

---

**🎯 MISSION:** Perform a comprehensive audit of the Gameday+ project to identify and safely remove redundant JSON/CSV files after database migration.

**📍 Project Location:** `/Users/davlenswain/Desktop/Gameday_Graphql_Model`

---

## Phase 1: File Inventory & Analysis

### Task 1.1: JSON File Audit (489 files)
Analyze each JSON file and categorize:

1. **Identify large duplicates:**
   - Find all copies of `react_power5_teams.json` (6 copies, 21MB each)
   - Find all copies of `power5_drives_complete.json` (5 copies, 9.6MB each)
   - Find all copies of `comprehensive_team_game_stats.json`
   - List all duplicates with " 2.json" suffix (space-2 naming pattern)

2. **Map to database tables:**
   - Check which JSON files have equivalent data in `predictions.db`
   - Database tables to check: `drives_complete`, `player_metrics_data`, `team_offensive_stats`, `team_defensive_stats`, `comprehensive_power_rankings`, `upcoming_games`, `sportsbook_lines`, `historical_game_results`
   - Run: `sqlite3 instance/predictions.db ".tables"` to see all tables
   - Run: `sqlite3 instance/predictions.db "SELECT COUNT(*) FROM [table_name]"` to verify data exists

3. **Code dependency check:**
   - Search for each JSON file in Python code: `grep -r "filename.json" --include="*.py" .`
   - Search in JavaScript/TypeScript: `grep -r "filename.json" --include="*.ts" --include="*.tsx" --include="*.js" frontend/`
   - For each reference found, verify if it's:
     - ✅ SAFE: Loading from database instead (look for database_helper or sqlite3 calls)
     - ⚠️ ACTIVE: Still reading the JSON file
     - 🗑️ DEAD CODE: Commented out or unused imports

### Task 1.2: CSV File Audit (267 files)

1. **Check CSV sizes:**
   - Find empty CSV files: `find . -name "*.csv" -size 0 ! -path "*/node_modules/*" ! -path "*/.venv/*"`
   - Find large CSV files: `find . -name "*.csv" -type f ! -path "*/node_modules/*" ! -path "*/.venv/*" -exec du -sh {} \; | sort -rh | head -20`

2. **Map CSV references:**
   - Find all CSV reads: `grep -r "pd\.read_csv\|csv\.reader\|\.csv" --include="*.py" . | grep -v ".venv"`
   - For each reference, check if:
     - It's reading from CSV file
     - It's using database instead
     - It's generating/writing CSV (keep these)

---

## Phase 2: Critical Safety Checks

### Task 2.1: Verify graphqlpredictor.py is JSON-free
```bash
# Check graphqlpredictor.py for JSON imports
grep -n "\.json\|json\.load" graphqlpredictor.py

# Check for open() calls
grep -n "open(" graphqlpredictor.py

# Verify it only uses database_helper
grep -n "database_helper\|sqlite3" graphqlpredictor.py
```

**Expected Result:** graphqlpredictor.py should ONLY use `database_helper` for data access, NO JSON file reads.

### Task 2.2: Verify betting_lines_manager.py fallback chain
```bash
# Check betting_lines_manager.py data sources
grep -n "\.json\|sqlite3\|graphql" betting_lines_manager.py
```

**Expected Priority:** Database → GraphQL API → JSON files (fallback only)

### Task 2.3: Check frontend dependencies
```bash
# Find JSON imports in React
grep -r "import.*from.*\.json" frontend/src/

# Check which JSON files are in frontend/src/data/
ls -lh frontend/src/data/*.json
```

**✅ VERIFIED - React Component Audit Complete:**

**KEEP (Essential):**
- ✅ `fbs.json` (45KB) - Team metadata used by 7+ components

**DELETE (25MB savings in frontend/src/data/):**
- 🔴 `react_power5_teams.json` (16MB) - NOT USED, duplicate
- 🔴 `power5_drives_only.json` (6.6MB) - NOT USED, data in DB
- 🔴 Coach JSON files (280KB) - lane_kiffin_master.json, james_franklin_master.json, etc.
  * Used by `CoachAnalysisPage.tsx` but should fetch from API instead
  * API exists: `app_master.py` port 5555 `/api/coach/<id>`
- 🔴 Team stats files (2.6MB) - fbs_defensive_stats.json, fbs_offensive_stats.json, etc. - NOT USED

**Migration Needed:**
- Update `CoachAnalysisPage.tsx` to use API instead of hardcoded coach JSON imports

---

## Phase 3: Create Deletion Plan

### Task 3.1: Categorize ALL files into:

**🔴 SAFE_TO_DELETE** (Generate list with space savings)
- Duplicate files (" 2.json" suffix)
- Files with data now in database tables
- Empty CSV files (0 bytes)
- Old weekly snapshot directories

**🟡 NEEDS_REVIEW** (Flag for manual inspection)
- Files with active code references but unclear usage
- Large files without obvious database equivalent
- Configuration/workflow JSON files

**🟢 KEEP_ESSENTIAL** (Must preserve)
- `fbs.json` - Frontend team data
- `package.json`, `package-lock.json` - npm
- `tsconfig.json` - TypeScript config
- `railway.json` - Deployment
- `n8n_gameday_workflow.json` - Automation

**🔵 KEEP_FALLBACK** (Keep for backup/fallback)
- `week15.json` - Betting lines fallback
- `Currentweekgames.json` - Betting lines fallback

### Task 3.2: Calculate Savings
For each category, sum file sizes and show:
```
SAFE_TO_DELETE: XXX MB (YYY files)
NEEDS_REVIEW: XXX MB (YYY files)
KEEP_ESSENTIAL: XXX MB (YYY files)
KEEP_FALLBACK: XXX MB (YYY files)
```

---

## Phase 4: Generate Cleanup Script

Create `cleanup.sh` with:

1. **Backup section:**
```bash
#!/bin/bash
echo "🔄 Creating backup..."
mkdir -p backups/cleanup_$(date +%Y%m%d)
cp -r instance backups/cleanup_$(date +%Y%m%d)/
```

2. **Safe deletion section:**
```bash
echo "🗑️ Removing duplicate JSON files..."
# Remove all " 2.json" files
find . -name "* 2.json" -type f ! -path "*/node_modules/*" -delete

echo "🗑️ Removing drive data files (now in DB)..."
# Remove power5_drives files
rm -f data_generators/team_stats/power5_drives*.json
rm -f weekly_updates/week_15/power5_drives*.json
# etc...
```

3. **Verification section:**
```bash
echo "✅ Verifying database integrity..."
python -c "
import sqlite3
conn = sqlite3.connect('instance/predictions.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM drives_complete')
print(f'Drives in DB: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM player_metrics_data')
print(f'Players in DB: {cursor.fetchone()[0]}')
"
```

4. **Test suite:**
```bash
echo "🧪 Testing app startup..."
# Start backend briefly to verify no import errors
timeout 10s python app.py || echo "Backend started successfully"
```

---

## Phase 5: Deliver Report

Create a markdown report with:

### Section 1: Executive Summary
- Total files analyzed
- Total space that can be reclaimed
- Risk assessment (LOW/MEDIUM/HIGH)
- Recommended next steps

### Section 2: Detailed Findings
**For each file in SAFE_TO_DELETE:**
- File path
- Size
- Database equivalent table
- Code references (with line numbers)
- Why it's safe to delete

**For each file in NEEDS_REVIEW:**
- File path
- Size
- Active code references
- Reason it needs review

### Section 3: Migration Verification
- ✅ List of database tables with row counts
- ✅ Confirmation graphqlpredictor.py is JSON-free
- ✅ Confirmation betting lines use database first
- ⚠️ Any remaining JSON dependencies found

### Section 4: Cleanup Commands
- Provide `cleanup.sh` script
- Step-by-step manual deletion commands
- Rollback procedure if issues occur

---

## 🎯 Success Criteria

1. ✅ All 489 JSON files categorized
2. ✅ All 267 CSV files categorized
3. ✅ Total space savings calculated
4. ✅ graphqlpredictor.py verified JSON-free
5. ✅ Zero breaking changes confirmed
6. ✅ Cleanup script provided
7. ✅ Rollback procedure documented

---

## 🚨 Safety Rules

**DO NOT DELETE:**
- Any file in `frontend/public/`
- Any file in `instance/` (databases)
- `fbs.json` (used by React)
- Configuration files (package.json, tsconfig.json, railway.json)
- N8N workflow files

**ALWAYS:**
- Create backups before deletion
- Test app after cleanup
- Verify database has equivalent data before deleting JSON
- Keep at least one copy of each unique data file until verified

---

## 📤 Deliverables

Please provide:
1. **CLEANUP_REPORT.md** - Full analysis with categorized file lists
2. **cleanup.sh** - Automated cleanup script
3. **ROLLBACK.md** - How to restore if issues occur
4. **SPACE_SAVINGS.txt** - Before/after disk usage

