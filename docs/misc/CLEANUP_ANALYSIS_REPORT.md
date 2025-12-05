# Gameday+ Project Cleanup Analysis Report
**Generated:** 2025-11-26
**Current Project Size:** ~900MB
**Target Size:** <300MB (66% reduction)
**Estimated Savings:** ~600MB

---

## 📊 Storage Breakdown by Category

| Directory | Current Size | Status | Action |
|-----------|-------------|--------|--------|
| **frontend/node_modules** | 353MB | Build artifact | ✅ Add to .gitignore (already done) |
| **.venv** | 258MB | Python virtual env | ✅ Add to .gitignore (already done) |
| **weekly_updates/** | 109MB | Historical data | ⚠️ Archive old weeks |
| **backtesting 2/** | 40MB | Old analysis | 🗑️ Safe to delete |
| **data/** | 37MB | Mixed (current + old) | ⚠️ Remove old timestamped files |
| **player_metrics/** | 23MB | Current metrics | ✅ Keep recent, delete old |
| **weekly_update_scripts/** | 22MB | Old metrics | 🗑️ Safe to delete |
| **Root directory** | ~50MB | Mixed files | 🗑️ Clean up test/temp files |
| **__pycache__** (298 dirs) | ~5MB | Python cache | 🗑️ Delete all |
| **logs/** | 364KB + root logs | Log files | 🗑️ Delete old logs |

---

## 🔴 CRITICAL FILES - DO NOT DELETE

### Core Application Files
```
✅ graphqlpredictor.py (284K) - Main prediction engine
✅ app.py (68K) - Flask application
✅ run.py (80K) - Runner script
✅ fbs.json (48K) - Team data
✅ Coaches.json (48K) - Coaches data
✅ Currentweekgames.json (184K) - Current week data
✅ betting_lines_manager.py (20K) - Betting logic
✅ formatter.py (76K) - Data formatter
```

### Core Data Files (Keep Most Recent Only)
```
✅ data/react_power5_teams.json (16M) - KEEP LATEST
✅ data/power5_drives_only.json (6.6M) - KEEP LATEST
✅ data/fbs_teams_stats_only.json (688K) - Current stats
✅ data/fbs_offensive_stats.json (428K) - Current stats
✅ data/fbs_defensive_stats.json (376K) - Current stats
✅ frontend/src/data/* - Current frontend data
```

### Configuration & Deployment
```
✅ requirements.txt (4K)
✅ package.json (4K)
✅ Dockerfile (4K)
✅ nixpacks.toml (4K)
✅ railway.json (4K)
✅ Procfile (4K)
✅ build.sh (4K)
✅ runtime.txt (4K)
✅ start-fullstack.sh (8K)
✅ .gitignore (NEW - keep!)
```

### Frontend Application
```
✅ frontend/src/ - All source files
✅ frontend/public/ - Public assets
✅ frontend/package.json
✅ frontend/vite.config.js
✅ frontend/.env.development
⚠️ frontend/node_modules - Exclude from git (already in .gitignore)
```

### Predictor Engine
```
✅ predictor/core/lightning_predictor.py
✅ predictor_engine/ directory
```

---

## 🟢 SAFE TO DELETE - Old/Duplicate/Test Files

### 1. Duplicate OSU/Michigan Rivalry Files (~3MB)
**Pattern:** Multiple timestamped outputs from Nov 26
```bash
# Duplicate rivalry analysis files (keep only latest)
osu_michigan_rivalry_data_20251126_085814.json (112K)
osu_michigan_rivalry_data_20251126_090113.json (112K)
osu_michigan_rivalry_data_20251126_090350.json (112K)
osu_michigan_rivalry_data_20251126_090734.json (112K)
osu_michigan_rivalry_data_20251126_090813.json (112K)
osu_michigan_rivalry_data_20251126_090952.json (112K)
osu_michigan_rivalry_data_20251126_091041.json (112K)
osu_michigan_rivalry_data_20251126_091325.json (112K)
osu_michigan_rivalry_data_20251126_091408.json (112K) ← KEEP LATEST ONLY

# Duplicate reports
osu_michigan_rivalry_report_20251126_*.txt (10 files, ~160K total)
osu_michigan_rivalry_graphql_20251126_092017.json (28K)
osu_michigan_rivalry_graphql_20251126_092017.txt (16K)

# General rivalry analysis duplicates
rivalry_analysis_all_20251126_092646.json (4K)
rivalry_analysis_all_20251126_092646.txt (4K)
rivalry_analysis_all_20251126_092711.json (4K)
rivalry_analysis_all_20251126_092711.txt (4K)
rivalry_analysis_all_20251126_093100.json (456K)
rivalry_analysis_all_20251126_093100.txt (20K)
rivalry_analysis_all_20251126_094317.json (456K) ← KEEP LATEST ONLY
rivalry_analysis_all_20251126_094317.txt (28K)
```

### 2. Duplicate Player Props Files (~450KB)
**Pattern:** Multiple timestamps for same game
```bash
REAL_DATA_player_props_OSU_vs_Michigan_week14_1764157129.json (76K)
REAL_DATA_player_props_OSU_vs_Michigan_week14_1764157332.json (76K)
REAL_DATA_player_props_OSU_vs_Michigan_week14_1764157548.json (76K)
REAL_DATA_player_props_OSU_vs_Michigan_week14_1764157767.json (76K)
REAL_DATA_player_props_OSU_vs_Michigan_week14_1764158886.json (76K) ← KEEP LATEST
enhanced_player_props_OSU_vs_Michigan_week14_1764156667.json (24K)
enhanced_player_props_OSU_vs_Michigan_week14_1764156905.json (112K) ← KEEP LATEST
player_props_Ohio_State_vs_Michigan_week14.json (12K)
```

### 3. Duplicate Team High Usage Players (~64KB)
```bash
team_high_usage_players_2025_1764156132.json (16K)
team_high_usage_players_2025_1764156155.json (16K)
team_high_usage_players_2025_1764156183.json (16K)
team_high_usage_players_2025_1764156217.json (16K) ← KEEP LATEST
```

### 4. Old QB Rankings at Root Level (~40KB)
**Action:** These are duplicates of player_metrics/qb/* - DELETE
```bash
qb_passer_rating_rankings_2025_20251125_023208.json (8K)
qb_ball_security_score_rankings_2025_20251125_023208.json (8K)
qb_dual_threat_efficiency_rankings_2025_20251125_023208.json (8K)
qb_total_yards_rankings_2025_20251125_023208.json (8K)
qb_comprehensive_efficiency_score_rankings_2025_20251125_023208.json (8K)
comprehensive_qb_analysis_2025_20251125_023208.json (228K)
```

### 5. Old Week Data Files (~200KB)
```bash
week8.json (96K)
week8_fbs_weather_graphql_20251016_005225.json (32K)
week8_fbs_weather_graphql_20251016_012151.json (32K)
week9.json (80K)
week9_game_media.json (56K)
```

### 6. Test HTML Files (~300KB)
**1,192 test files found!** - HTML files in root:
```bash
test_betting_logic.html (8K)
test_integration.html (4K)
testingweek9.html (36K)
teampicks.html (16K)
test_all_week8_games.html (24K)
overview.html (32K)
debug_frontend_data.html (12K)
test.html (32K)
test_report.html (4K)
integration-demo.html (12K)
week8_backtest_results.html (72K)
```

### 7. Test Python Scripts (~200KB)
**Partial list of test_*.py files to delete:**
```bash
test_rivalry_graphql.py (4K)
test_week12_games.py (4K)
test_ui_update.py (4K)
test_texas_georgia.py (4K)
test_single_prediction.py (4K)
test_player_integration.py (4K)
test_optimized.py (4K)
test_modular_system.py (4K)
test_fix.py (4K)
test_enhancement_features.py (4K)
test_enhanced_players.py (4K)
test_enhanced_model.py (4K)
test_dashboard.py (4K)
test_corrected_betting_logic.py (4K)
test_batch_3games.py (4K)
test_async_player_flow.py (4K)
test_api.py (4K)
test_all_ranked_week12.py (4K)
test_18_sections.py (4K)
test_iowa_state_live.py (12K)
test_full_integration.py (12K)
test_additional_games.py (12K)
test_ohio_fix.py (8K)
test_ole_miss_wazzu.py (8K)
test_week8_weather.py (8K)
test_betting_fixes.py (8K)
test_elite_predictor.py (8K)
test_enhanced_prediction_system.py (8K)
testplayermetrics.py (36K)
```

### 8. Old Analysis/Debug Scripts (~150KB)
```bash
backtest_week8.py (28K)
batch_predict_week13.py (8K)
batch_rivalry_analyzer.py (16K)
check_full_schedule.py (4K)
component_mapping_analysis.py (12K)
debug_frontend_data.py (4K)
debug_michigan.py (4K)
debug_player_impact.py (8K)
debug_player_stats.py (8K)
debug_weeks.py (4K)
discover_schema_fields.py (8K)
enhanced_validation.py (8K)
fact_check.py (8K)
fetch_week10_game_media.py (8K)
fetch_week9_game_media.py (8K)
hardcoded_detection.py (12K)
integration_roadmap.py (12K)
prediction_validator.py (12K)
ratings_explorer.py (12K)
react_components_scan.py (12K)
schema_explorer.py (12K)
simple_validation.py (12K)
smart_component_analysis.py (12K)
update_components_dynamic_v2.py (24K)
update_components_to_dynamic.py (24K)
validate_enhanced_system.py (4K)
verify_fix.py (8K)
verify_new_weeks.py (4K)
verify_weeks.py (4K)
```

### 9. Utility Scripts (Potentially Old) (~100KB)
```bash
ap_poll_week7.py (8K)
ap_poll_week10.py (8K)
week8_fetcher.py (12K)
week9_fetcher.py (16K)
week10_fetcher.py (12K)
week11_fetcher.py (12K)
week11_graphql_fetcher.py (16K)
fix_dashboard.py (16K)
extract_js.py (4K)
```

### 10. Old JSON Response/Test Files (~150KB)
```bash
test_3_games.json (8K)
test_prediction_output.json (24K)
full_api_response_syracuse_gt.json (24K)
Response_Fixed.json (36K)
Resoponse.json (36K)
Structured_Analysis.json (16K)
live_data_Iowa_State_vs_BYU.json (8K)
ap_poll_week10_2025.json (4K)
Clean_UI_Components.json (4K)
ats_data_2025.json (52K) - May be needed, check if used in frontend
```

### 11. Log Files (~500KB)
```bash
backend.log (4K)
frontend.log (4K)
flask.log (12K)
flask_new.log (328K)
week13_predictions.log (12K)
server.log (4K)
vite.log (4K)
nohup.out (48K)
full_output_test.txt (32K)
```

### 12. Old Betting Picks/Reports (~150KB)
```bash
week13_betting_picks.txt (16K)
week13_betting_picks_CORRECTED.txt (24K)
week13_betting_picks_FINAL.txt (84K) ← KEEP if still relevant
week13_picks_comparison.txt (12K)
```

### 13. Backup/Old Shell Scripts (~20KB)
```bash
start-fullstack.sh.backup (4K)
start-fullstack-old.sh (4K)
temp-start-fullstack.sh (4K)
start.sh (4K)
```

### 14. Old Test Report Files (~50KB)
```bash
test_report.js (44K)
test.js (16K)
test_frontend_fix.js (4K)
```

### 15. Python Cache Files (~5MB)
```bash
__pycache__/ directories (298 total) - ~5MB
*.pyc files throughout project
```

### 16. Old/Duplicate Data Directory Files (~15MB)
**Note:** data/ has duplicates of files that exist in backtesting 2/ and frontend/src/data/
```bash
# Old timestamped analysis files (Oct/Nov)
data/comprehensive_db_analysis_2025_20251015_051747.json (980K) - DELETE
data/comprehensive_db_analysis_2025_20251103_005036.json (1.0M) - DELETE (have newer in player_metrics)
data/comprehensive_dl_analysis_2025_20251015_051056.json (736K) - DELETE
data/comprehensive_dl_analysis_2025_20251103_005326.json (816K) - DELETE
data/comprehensive_lb_analysis_2025_20251015_053156.json (520K) - DELETE
data/comprehensive_lb_analysis_2025_20251103_005148.json (568K) - DELETE
data/comprehensive_rb_analysis_2025_20251103_004639.json (472K) - DELETE
data/comprehensive_wr_analysis_2025_20251015_045922.json (396K) - DELETE
data/comprehensive_wr_analysis_2025_20251103_004752.json (448K) - DELETE
data/comprehensive_qb_analysis_2025_20251103_004118.json (204K) - DELETE
data/comprehensive_te_analysis_2025_20251103_004907.json (200K) - DELETE

# Old enhanced games data
data/all_fbs_games_2024_ENHANCED_20251015_002119.json (3.0M) - DELETE (old season)
data/all_fbs_games_2025_ENHANCED_20251015_083540.json (2.4M) - DELETE (outdated)
data/all_fbs_elo_progression_2025_20251015_020032.json (348K) - DELETE
```

### 17. Entire "backtesting 2/" Directory (~40MB)
**This is all old data from Oct/Nov - SAFE TO DELETE**
```bash
backtesting 2/react_power5_teams.json (16M)
backtesting 2/power5_drives_only.json (6.6M)
backtesting 2/all_fbs_games_2024_ENHANCED_20251015_002119.json (3.0M)
backtesting 2/all_fbs_games_2025_ENHANCED_20251015_083540.json (2.4M)
backtesting 2/all_fbs_teams_schedules_2025_20251113_042858.json (1.9M)
backtesting 2/comprehensive_db_analysis_2025_20251113_034921.json (1.1M)
backtesting 2/comprehensive_dl_analysis_2025_20251113_034920.json (828K)
backtesting 2/comprehensive_power_rankings_20251113_040210.json (812K)
backtesting 2/fbs_team_stats_complete.json (728K)
backtesting 2/fbs_teams_stats_only.json (688K)
... and many more old files
```

### 18. Old "weekly_update_scripts/" Directory (~22MB)
**Duplicate of current player_metrics/ - DELETE**
```bash
weekly_update_scripts/player_metrics/db/* (7+ files, ~7.7MB)
weekly_update_scripts/player_metrics/dl/* (7+ files, ~5.8MB)
weekly_update_scripts/player_metrics/lb/* (7+ files, ~4.3MB)
weekly_update_scripts/player_metrics/qb/* (7+ files, ~1.4MB)
weekly_update_scripts/player_metrics/rb/* (7+ files, ~1.4MB)
weekly_update_scripts/player_metrics/wr/* (7+ files, ~1.1MB)
weekly_update_scripts/player_metrics/te/* (7+ files, ~0.7MB)
```

---

## 🟡 QUESTIONABLE - Review Before Deleting

### Markdown Documentation Files (45 files, ~5MB)
**Action:** Review and consolidate, delete outdated
```bash
⚠️ Chat.md (612K) - Review if needed
⚠️ CHAT_HISTORY_FORMATTER_HARDCODING_ISSUE.md (292K) - Likely outdated
⚠️ COMPREHENSIVE_PROJECT_DOCUMENTATION.md (28K) - Keep
⚠️ README.md (8K) - Keep
⚠️ DEPLOYMENT_GUIDE.md (4K) - Keep
⚠️ College_Football_Data_GraphQL_Schema.md (28K) - Keep
⚠️ AAAcomprehensiveguide.md (28K) - Keep

# Review and potentially delete:
WEEKLY_UPDATE_CHECKLIST.md (48K)
WEEKLY_UPDATE_CHECKLIST_WEEK12.md (32K)
WEEK12_DATA_UPDATE_STATUS.md (8K)
WEEK_11_CFB_TRENDS_ANALYTICS.md (24K)
WEEK10_POWER_RANKINGS_INTEGRATION.md (24K)
COMPREHENSIVE_UI_INTEGRATION_PLAN.md (48K)
COMPREHENSIVE_ANALYSIS_STATUS.md (40K)
COMPONENT_INTEGRATION_PROGRESS.md (16K)
UI_Enhancement_Roadmap.md (28K)
UI_MODERNIZATION_ANALYSIS.md (32K)
SMART_REFACTORING_PLAN.md (8K)
REFACTORING_IMPLEMENTATION_GUIDE.md (12K)
REFACTORING_CHECKLIST.md (4K)
COMPLETE_INTEGRATION_ROADMAP.md (32K)
PREDICTION_RESULTS_FIX_ROADMAP.md (12K)
PREDICTION_SYSTEM_FIXES_SUMMARY.md (8K)
PREDICTION_ENGINE_OPTIMIZATION_v0.2.1.md (8K)
GamedayPlus_Lightning-Fast_Predictor_Roadmap.md (16K)
COMPREHENSIVE_DATA_SOURCES_MAPPING.md (20K)
IOS_INTEGRATION_GUIDE.md (64K)
REACT_VS_IOS_COMPLETE_COMPARISON.md (12K)
FIGMA_UI_DEVELOPMENT_PLAN.md (8K)
ADD_INSIGHTS_GUIDE.md (8K)
LIVE_GAME_FEATURE.md (20K)
LIVE_GAME_INTEGRATION_COMPLETE.md (16K)
RAILWAY_API_CONFIG_MIGRATION.md (12K)
OPTIMIZATION_SUMMARY.md (12K)
FINAL_ENHANCEMENT_SUMMARY.md (8K)
ENHANCEMENT_SUMMARY.md (4K)
BETTING_ANALYSIS_FIX_SUMMARY.md (8K)
STEP3_IMPLEMENTATION_CHECKLIST.md (8K)
STEP3_FINAL_IMPLEMENTATION_GUIDE.md (8K)
QUICK_REFERENCE.md (8K)
TROUBLESHOOTING_LOG.md (4K)
UI_RESET_COMPLETE.md (4K)
CORRECT_PLAYER_QUERIES.md (8K)
analysis_discrepancies.md (12K)
ENHANCED_UI_COMPONENTS.md (0B - empty)
```

### Current Generator Scripts (~60KB)
**Action:** Keep if actively used, delete if superseded
```bash
⚠️ player_props_generator.py (28K) - Check if still used
⚠️ enhanced_player_props_generator.py (28K) - Likely current version
⚠️ real_data_props_generator.py (32K) - Check which is current
⚠️ osu_michigan_rivalry_analysis.py (24K) - Keep for future rivalry games
⚠️ osu_michigan_rivalry_graphql.py (20K) - Keep
⚠️ batch_rivalry_analyzer.py (16K) - Keep
⚠️ rivalry_config.py (8K) - Keep
⚠️ fbs_players_extractor.py (20K) - Keep
⚠️ fetch_2025_players.py (8K) - Keep
⚠️ fetch_ats_data.py (4K) - Keep
⚠️ high_usage_players_rest.py (16K) - Keep
⚠️ fixed_betting_analyzer.py (28K) - Keep
⚠️ game_media_service.py (8K) - Keep
```

### SVG Logo Files (~24KB)
```bash
✅ Draftking.svg (8K) - Keep
✅ Bovada-Casino-Logo.svg (8K) - Keep
✅ espnbet.svg (4K) - Keep
```

### Weekly Updates Archives (~109MB)
**Action:** Keep week 13 & 14, archive older weeks
```bash
⚠️ weekly_updates/week_14/ (~55MB) - KEEP (current)
⚠️ weekly_updates/week_13/ (~54MB) - KEEP (recent)
⚠️ weekly_updates/week_12/ - Archive/delete if exists
⚠️ weekly_updates/week_11/ - Archive/delete if exists
... older weeks
```

### Root node_modules (~8KB)
```bash
⚠️ node_modules/ (8K) - Likely leftover, safe to delete
⚠️ package-lock.json (root) (4K) - Check if needed
```

---

## 💾 Estimated Storage Savings

| Category | Savings |
|----------|---------|
| .venv (already in .gitignore) | 258MB |
| frontend/node_modules (already in .gitignore) | 353MB |
| **backtesting 2/** | 40MB |
| **weekly_update_scripts/** | 22MB |
| **Old data/ files** | 15MB |
| **Duplicate rivalry files** | 3MB |
| **Test files (HTML/Python/JS)** | 5MB |
| **Python __pycache__** | 5MB |
| **Old week JSON files** | 1MB |
| **Player props duplicates** | 0.5MB |
| **Log files** | 0.5MB |
| **QB rankings root duplicates** | 0.3MB |
| **Backup scripts** | 0.02MB |
| **Old markdown docs** (after review) | 3MB |
| **Total Immediate Savings** | **~95MB** |
| **With .gitignore (node_modules/.venv)** | **~706MB** |

**After cleanup: ~194MB** (from 900MB)
**After first Railway deploy: ~194MB** (node_modules/venv rebuilt on server, not in git)

---

## 🚀 Single Cleanup Command

```bash
# BACKUP FIRST (just in case)
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
tar -czf ../gameday_backup_$(date +%Y%m%d).tar.gz .

# DELETE OLD FILES (safe cleanup - run from project root)
rm -rf "backtesting 2" \
  && rm -rf weekly_update_scripts \
  && rm -rf node_modules \
  && rm -f osu_michigan_rivalry_data_20251126_08*.json \
  && rm -f osu_michigan_rivalry_data_20251126_090*.json \
  && rm -f osu_michigan_rivalry_data_20251126_091[0-2]*.json \
  && rm -f osu_michigan_rivalry_report_20251126_*.txt \
  && rm -f osu_michigan_rivalry_graphql_20251126_*.{json,txt} \
  && rm -f rivalry_analysis_all_20251126_092*.json \
  && rm -f rivalry_analysis_all_20251126_092*.txt \
  && rm -f rivalry_analysis_all_20251126_093*.{json,txt} \
  && rm -f REAL_DATA_player_props_OSU_vs_Michigan_week14_176415[67]*.json \
  && rm -f enhanced_player_props_OSU_vs_Michigan_week14_1764156667.json \
  && rm -f player_props_Ohio_State_vs_Michigan_week14.json \
  && rm -f team_high_usage_players_2025_176415[0-1]*.json \
  && rm -f qb_*_rankings_2025_*.json \
  && rm -f comprehensive_qb_analysis_2025_20251125_*.json \
  && rm -f week[89]*.json \
  && rm -f *.html \
  && rm -f test_*.py \
  && rm -f test_*.js \
  && rm -f backend.log frontend.log flask.log flask_new.log week*.log server.log vite.log nohup.out \
  && rm -f week13_betting_picks.txt week13_betting_picks_CORRECTED.txt week13_picks_comparison.txt \
  && rm -f start-fullstack*.backup start-fullstack-old.sh temp-start-fullstack.sh start.sh \
  && rm -f test_report.js test.js test_frontend_fix.js \
  && rm -f test_3_games.json test_prediction_output.json full_api_response_*.json \
  && rm -f Response_Fixed.json Resoponse.json Structured_Analysis.json \
  && rm -f live_data_*.json ap_poll_week10_2025.json Clean_UI_Components.json \
  && rm -f full_output_test.txt \
  && rm -f data/comprehensive_*_analysis_2025_202510*.json \
  && rm -f data/comprehensive_*_analysis_2025_202511*.json \
  && rm -f data/all_fbs_games_202*_ENHANCED_*.json \
  && rm -f data/all_fbs_elo_progression_*.json \
  && rm -f backtest_week8.py \
  && rm -f batch_predict_week13.py \
  && rm -f check_full_schedule.py \
  && rm -f component_mapping_analysis.py \
  && rm -f debug_*.py \
  && rm -f discover_schema_fields.py \
  && rm -f enhanced_validation.py \
  && rm -f fact_check.py \
  && rm -f fetch_week*_game_media.py \
  && rm -f hardcoded_detection.py \
  && rm -f integration_roadmap.py \
  && rm -f prediction_validator.py \
  && rm -f ratings_explorer.py \
  && rm -f react_components_scan.py \
  && rm -f schema_explorer.py \
  && rm -f simple_validation.py \
  && rm -f smart_component_analysis.py \
  && rm -f update_components*.py \
  && rm -f validate_enhanced_system.py \
  && rm -f verify_*.py \
  && rm -f ap_poll_week*.py \
  && rm -f week*_fetcher.py \
  && rm -f fix_dashboard.py \
  && rm -f extract_js.py \
  && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null \
  && echo "✅ Cleanup complete!"
```

---

## 📋 Step-by-Step Safer Cleanup (Recommended)

### Phase 1: Remove Confirmed Duplicates (Safe)
```bash
# 1. Delete duplicate rivalry files (keep latest only)
rm -f osu_michigan_rivalry_data_20251126_08*.json
rm -f osu_michigan_rivalry_data_20251126_090*.json
rm -f osu_michigan_rivalry_data_20251126_091[0-2]*.json
rm -f osu_michigan_rivalry_report_20251126_*.txt
rm -f rivalry_analysis_all_20251126_09[0-2]*.{json,txt}

# 2. Delete duplicate player props (keep latest)
rm -f REAL_DATA_player_props_OSU_vs_Michigan_week14_176415[67]*.json
rm -f enhanced_player_props_OSU_vs_Michigan_week14_1764156667.json

# 3. Delete duplicate team usage files
rm -f team_high_usage_players_2025_176415[0-1]*.json

# 4. Delete QB rankings duplicates at root
rm -f qb_*_rankings_2025_*.json
rm -f comprehensive_qb_analysis_2025_20251125_*.json

echo "✅ Phase 1 complete: ~4MB freed"
```

### Phase 2: Remove Test Files (Safe)
```bash
# 1. Delete test HTML files
rm -f test_*.html testingweek9.html teampicks.html overview.html debug_frontend_data.html test.html integration-demo.html week8_backtest_results.html

# 2. Delete test Python scripts
rm -f test_*.py

# 3. Delete test JS files
rm -f test_*.js

echo "✅ Phase 2 complete: ~5MB freed"
```

### Phase 3: Remove Old Data Files (Safe)
```bash
# 1. Delete old week data
rm -f week[89]*.json

# 2. Delete old player props
rm -f player_props_Ohio_State_vs_Michigan_week14.json

# 3. Delete old test JSON
rm -f test_3_games.json test_prediction_output.json full_api_response_*.json
rm -f Response_Fixed.json Resoponse.json Structured_Analysis.json live_data_*.json
rm -f ap_poll_week10_2025.json Clean_UI_Components.json

echo "✅ Phase 3 complete: ~1MB freed"
```

### Phase 4: Remove Cache and Logs (Safe)
```bash
# 1. Delete all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 2. Delete log files
rm -f backend.log frontend.log flask.log flask_new.log week*.log server.log vite.log nohup.out full_output_test.txt

echo "✅ Phase 4 complete: ~6MB freed"
```

### Phase 5: Remove Old Scripts (Review First)
```bash
# Review these before deleting - some might be useful utilities
rm -f backtest_week8.py batch_predict_week13.py check_full_schedule.py
rm -f component_mapping_analysis.py debug_*.py discover_schema_fields.py
rm -f enhanced_validation.py fact_check.py fetch_week*_game_media.py
rm -f hardcoded_detection.py integration_roadmap.py prediction_validator.py
rm -f ratings_explorer.py react_components_scan.py schema_explorer.py
rm -f simple_validation.py smart_component_analysis.py update_components*.py
rm -f validate_enhanced_system.py verify_*.py ap_poll_week*.py week*_fetcher.py
rm -f fix_dashboard.py extract_js.py

echo "✅ Phase 5 complete: ~2MB freed"
```

### Phase 6: Remove Large Old Directories (VERIFY FIRST!)
```bash
# VERIFY: Make sure you have current data elsewhere before running
# Check that frontend/src/data/ and player_metrics/ have current files

# 1. Delete backtesting 2 directory (old Oct/Nov data)
rm -rf "backtesting 2"

# 2. Delete weekly_update_scripts (duplicate of player_metrics)
rm -rf weekly_update_scripts

# 3. Delete old data/ files
rm -f data/comprehensive_*_analysis_2025_202510*.json
rm -f data/comprehensive_*_analysis_2025_202511*.json
rm -f data/all_fbs_games_202*_ENHANCED_*.json
rm -f data/all_fbs_elo_progression_*.json

# 4. Delete root node_modules (not needed)
rm -rf node_modules

echo "✅ Phase 6 complete: ~77MB freed"
```

### Phase 7: Clean Up Backup Scripts
```bash
rm -f start-fullstack*.backup start-fullstack-old.sh temp-start-fullstack.sh start.sh

echo "✅ Phase 7 complete"
```

### Phase 8: Review Markdown Files (Manual)
```bash
# Review and delete outdated markdown files manually
# Keep: README.md, DEPLOYMENT_GUIDE.md, COMPREHENSIVE_PROJECT_DOCUMENTATION.md
# Consider deleting weekly status updates and old roadmaps

echo "⚠️ Phase 8: Manual review needed for .md files"
```

---

## 🔍 Verification Commands

### After Cleanup - Verify Project Still Works
```bash
# 1. Check Python dependencies
python3 -m pip list

# 2. Check if core files exist
ls -lh graphqlpredictor.py app.py fbs.json Coaches.json

# 3. Check frontend
cd frontend && npm install && npm run build

# 4. Test backend
python3 app.py

# 5. Check new size
cd /Users/davlenswain/Desktop/Gameday_Graphql_Model
du -sh .
```

### Check What's in .gitignore
```bash
cat .gitignore
```

Expected:
```
node_modules/
.venv/
__pycache__/
*.pyc
.env
*.log
```

---

## 🎯 Priority Actions

### HIGH PRIORITY (Do Now)
1. ✅ **Verify .gitignore includes:** `node_modules/`, `.venv/`, `__pycache__/`, `*.pyc`, `*.log`
2. 🗑️ **Delete "backtesting 2/"** - 40MB of old Oct/Nov data
3. 🗑️ **Delete "weekly_update_scripts/"** - 22MB duplicate of player_metrics
4. 🗑️ **Delete all test_*.py files** - No longer needed
5. 🗑️ **Delete all test HTML files** - No longer needed
6. 🗑️ **Delete __pycache__ directories** - Will be regenerated
7. 🗑️ **Delete duplicate rivalry/props files** - Keep only latest

### MEDIUM PRIORITY (This Week)
1. 📦 **Archive old weeks in weekly_updates/** - Keep only week 13 & 14
2. 📝 **Consolidate markdown docs** - Merge related docs, delete outdated
3. 🧹 **Clean data/ directory** - Remove Oct/Nov timestamped files
4. 🗑️ **Delete old log files** - Keep only current logs if needed

### LOW PRIORITY (When Time Allows)
1. 📚 **Review and update documentation** - Single source of truth
2. 🔄 **Evaluate generator scripts** - Which are current vs legacy
3. 📊 **Audit player_metrics/** - Ensure only current week data

---

## 📌 Notes

1. **Virtual Environment (.venv)**: Already in .gitignore - Railway will rebuild on deploy
2. **node_modules**: Already in .gitignore - Railway will run `npm install` on deploy
3. **Current Week Data**: Always keep the most recent weekly_updates/week_XX/
4. **Player Metrics**: Current data is in `player_metrics/` - weekly_update_scripts is old
5. **Frontend Data**: Keep `frontend/src/data/*` - it's the active data source
6. **Rivalry Analysis**: The Nov 26 files are duplicates from multiple test runs

---

## 🚨 DO NOT DELETE

- graphqlpredictor.py
- app.py, run.py
- fbs.json, Coaches.json
- Currentweekgames.json
- frontend/src/ directory
- predictor/ directory
- data/react_power5_teams.json (current)
- data/power5_drives_only.json (current)
- data/fbs_*_stats.json (current)
- requirements.txt, package.json
- Deployment configs (Dockerfile, railway.json, etc.)
- .gitignore
- weekly_updates/week_14/
- weekly_updates/week_13/
- player_metrics/ (current metrics)

---

## ✅ Expected Results After Cleanup

**Before:**
- Total size: ~900MB
- Files in git: ~300MB (rest is node_modules/.venv)
- Railway deploy: Times out

**After:**
- Total size: ~194MB
- Files in git: ~194MB
- Railway deploy: Fast and successful
- All functionality: Intact

---

## 📞 Questions Before Cleanup?

If uncertain about any file:
1. Check if it's imported/used: `grep -r "filename" .`
2. Check git history: `git log --all -- filename`
3. When in doubt, keep it for now
4. Create backup before mass deletion: `tar -czf backup.tar.gz .`

---

**Generated by Claude Code Analysis**
**Report Date:** November 26, 2025
**Project:** Gameday+ College Football Prediction System
