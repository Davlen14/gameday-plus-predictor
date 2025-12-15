#!/bin/bash
# Safe Gameday+ Project Cleanup Script
# Removes redundant JSON/CSV files that have been migrated to database
# Run from: /Users/davlenswain/Desktop/Gameday_Graphql_Model

set -e  # Exit on any error

echo "🧹 Gameday+ Safe Cleanup Script"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create backup
echo "📦 Step 1: Creating backup..."
BACKUP_DIR="backups/cleanup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup critical files
cp -r instance "$BACKUP_DIR/" 2>/dev/null || echo "No instance/ to backup"
cp -r frontend/src/data "$BACKUP_DIR/frontend_data" 2>/dev/null || echo "No frontend/src/data to backup"
cp -r data "$BACKUP_DIR/data" 2>/dev/null || echo "No data/ to backup"
cp -r weekly_updates "$BACKUP_DIR/weekly_updates" 2>/dev/null || echo "No weekly_updates/ to backup"

echo -e "${GREEN}✅ Backup created: $BACKUP_DIR${NC}"
echo ""

# Step 2: Calculate space to be freed
echo "📊 Step 2: Calculating space to be freed..."
BEFORE_SIZE=$(du -sh . 2>/dev/null | awk '{print $1}')
echo "Current project size: $BEFORE_SIZE"
echo ""

# Step 3: Delete frontend/src/data files (EXCEPT fbs.json)
echo "🗑️  Step 3: Cleaning frontend/src/data/ (keeping fbs.json only)..."

if [ -d "frontend/src/data" ]; then
  # Delete the big ones first
  rm -f frontend/src/data/react_power5_teams.json && echo "  ✓ Deleted react_power5_teams.json (16MB)"
  rm -f frontend/src/data/power5_drives_only.json && echo "  ✓ Deleted power5_drives_only.json (6.6MB)"
  
  # Delete coach files
  rm -f frontend/src/data/lane_kiffin_master.json && echo "  ✓ Deleted lane_kiffin_master.json"
  rm -f frontend/src/data/james_franklin_master.json && echo "  ✓ Deleted james_franklin_master.json"
  rm -f frontend/src/data/coaches_advanced_rankings.json && echo "  ✓ Deleted coaches_advanced_rankings.json"
  rm -f frontend/src/data/coaches_enhanced_stats.json && echo "  ✓ Deleted coaches_enhanced_stats.json"
  rm -f frontend/src/data/coaches_simplified_ranked.json && echo "  ✓ Deleted coaches_simplified_ranked.json"
  rm -f frontend/src/data/coaches_with_vsranked_stats.json && echo "  ✓ Deleted coaches_with_vsranked_stats.json"
  rm -rf frontend/src/data/coach_timelines/ && echo "  ✓ Deleted coach_timelines/ directory"
  
  # Delete team stats files
  rm -f frontend/src/data/fbs_defensive_stats.json && echo "  ✓ Deleted fbs_defensive_stats.json"
  rm -f frontend/src/data/fbs_offensive_stats.json && echo "  ✓ Deleted fbs_offensive_stats.json"
  rm -f frontend/src/data/fbs_team_stats_complete.json && echo "  ✓ Deleted fbs_team_stats_complete.json"
  rm -f frontend/src/data/fbs_teams_stats_only.json && echo "  ✓ Deleted fbs_teams_stats_only.json"
  rm -f frontend/src/data/react_fbs_team_rankings.json && echo "  ✓ Deleted react_fbs_team_rankings.json"
  rm -f frontend/src/data/react_power5_efficiency.json && echo "  ✓ Deleted react_power5_efficiency.json"
  rm -f frontend/src/data/team_season_summaries_clean.json && echo "  ✓ Deleted team_season_summaries_clean.json"
  rm -f frontend/src/data/complete_win_probabilities.json && echo "  ✓ Deleted complete_win_probabilities.json"
  
  # Delete misc files
  rm -f frontend/src/data/ap.json && echo "  ✓ Deleted ap.json"
  rm -f frontend/src/data/react_fbs_conferences.json && echo "  ✓ Deleted react_fbs_conferences.json"
  
  # Delete files with " 2" suffix (duplicates)
  find frontend/src/data -name "* 2.json" -delete && echo "  ✓ Deleted duplicate ' 2.json' files"
  
  echo -e "${GREEN}✅ Frontend data cleaned (kept fbs.json only)${NC}"
else
  echo -e "${YELLOW}⚠️  frontend/src/data not found${NC}"
fi
echo ""

# Step 4: Delete duplicate JSON files in project root and other directories
echo "🗑️  Step 4: Removing duplicate JSON files..."

# Remove react_power5_teams duplicates (keep NONE - all data in DB)
find . -name "react_power5_teams*.json" -type f ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" -delete && echo "  ✓ Deleted all react_power5_teams.json copies"

# Remove power5_drives duplicates (keep NONE - all data in DB)
find . -name "power5_drives*.json" -type f ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" -delete && echo "  ✓ Deleted all power5_drives*.json copies"

# Remove comprehensive team stats duplicates
find . -name "comprehensive_team_game_stats*.json" -type f ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" -delete && echo "  ✓ Deleted comprehensive_team_game_stats*.json"

# Remove clean team stats
find . -name "clean_team_game_stats*.json" -type f ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" -delete && echo "  ✓ Deleted clean_team_game_stats*.json"

echo -e "${GREEN}✅ Duplicates removed${NC}"
echo ""

# Step 5: Clean weekly_updates directory (old weekly snapshots)
echo "🗑️  Step 5: Cleaning weekly_updates/ directory..."

if [ -d "weekly_updates" ]; then
  # Delete player leader files (data in DB)
  find weekly_updates -name "defensive_leaders*.json" -delete && echo "  ✓ Deleted defensive_leaders*.json"
  find weekly_updates -name "receiving_leaders*.json" -delete && echo "  ✓ Deleted receiving_leaders*.json"
  find weekly_updates -name "rushing_leaders*.json" -delete && echo "  ✓ Deleted rushing_leaders*.json"
  find weekly_updates -name "passing_leaders*.json" -delete && echo "  ✓ Deleted passing_leaders*.json"
  
  # Delete team stats files
  find weekly_updates -name "team_season_stats*.json" -delete && echo "  ✓ Deleted team_season_stats*.json"
  find weekly_updates -name "fbs_team_stats_complete*.json" -delete && echo "  ✓ Deleted fbs_team_stats_complete*.json"
  
  # Delete " 2.json" duplicates
  find weekly_updates -name "* 2.json" -delete && echo "  ✓ Deleted duplicate ' 2.json' files"
  
  echo -e "${GREEN}✅ Weekly updates cleaned${NC}"
else
  echo -e "${YELLOW}⚠️  weekly_updates/ not found${NC}"
fi
echo ""

# Step 6: Clean data_generators directory
echo "🗑️  Step 6: Cleaning data_generators/ directory..."

if [ -d "data_generators" ]; then
  # Remove all the duplicate large files
  find data_generators -name "react_power5_teams*.json" -delete 2>/dev/null && echo "  ✓ Deleted react_power5_teams*.json"
  find data_generators -name "power5_drives*.json" -delete 2>/dev/null && echo "  ✓ Deleted power5_drives*.json"
  find data_generators -name "* 2.json" -delete 2>/dev/null && echo "  ✓ Deleted duplicate ' 2.json' files"
  
  echo -e "${GREEN}✅ Data generators cleaned${NC}"
else
  echo -e "${YELLOW}⚠️  data_generators/ not found${NC}"
fi
echo ""

# Step 7: Clean empty CSV files
echo "🗑️  Step 7: Removing empty CSV files..."
EMPTY_CSV_COUNT=$(find . -name "*.csv" -size 0 ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" | wc -l | xargs)
find . -name "*.csv" -size 0 ! -path "*/node_modules/*" ! -path "*/.venv/*" ! -path "*/backups/*" -delete
echo -e "${GREEN}✅ Deleted $EMPTY_CSV_COUNT empty CSV files${NC}"
echo ""

# Step 8: Delete specific unused files
echo "🗑️  Step 8: Removing unused individual files..."
rm -f army_navy_matchup.json && echo "  ✓ Deleted army_navy_matchup.json"
rm -f washington_boise*.json && echo "  ✓ Deleted washington_boise*.json"
echo ""

# Step 9: Calculate space saved
echo "📊 Step 9: Calculating space saved..."
AFTER_SIZE=$(du -sh . 2>/dev/null | awk '{print $1}')
echo "Before: $BEFORE_SIZE"
echo "After:  $AFTER_SIZE"
echo ""

# Step 10: Verify database integrity
echo "🔍 Step 10: Verifying database integrity..."
python3 << 'PYEOF'
import sqlite3
import sys

try:
    conn = sqlite3.connect('instance/predictions.db')
    cursor = conn.cursor()
    
    # Check key tables
    tables_to_check = [
        ('drives_complete', 'Drive data'),
        ('player_metrics_data', 'Player metrics'),
        ('team_offensive_stats', 'Offensive stats'),
        ('team_defensive_stats', 'Defensive stats'),
        ('upcoming_games', 'Game schedule'),
        ('sportsbook_lines', 'Betting lines')
    ]
    
    print("Database verification:")
    all_good = True
    for table_name, description in tables_to_check:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            print(f"  ✓ {description}: {count:,} rows")
            if count == 0:
                print(f"    ⚠️  Warning: {table_name} is empty")
                all_good = False
        except Exception as e:
            print(f"  ✗ Error checking {table_name}: {e}")
            all_good = False
    
    conn.close()
    
    if all_good:
        print("\n✅ Database integrity verified!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tables may be empty - verify this is expected")
        sys.exit(0)
        
except Exception as e:
    print(f"\n❌ Database check failed: {e}")
    sys.exit(1)
PYEOF

DB_CHECK_RESULT=$?
if [ $DB_CHECK_RESULT -ne 0 ]; then
  echo -e "${RED}❌ Database verification failed!${NC}"
  echo "Your data is backed up in: $BACKUP_DIR"
  exit 1
fi
echo ""

# Step 11: Verify essential files still exist
echo "🔍 Step 11: Verifying essential files..."
ESSENTIAL_FILES=(
  "frontend/src/fbs.json"
  "package.json"
  "tsconfig.json"
  "railway.json"
  "instance/predictions.db"
)

ALL_ESSENTIAL_EXIST=true
for file in "${ESSENTIAL_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $file exists"
  else
    echo -e "  ${RED}✗ $file MISSING!${NC}"
    ALL_ESSENTIAL_EXIST=false
  fi
done

if [ "$ALL_ESSENTIAL_EXIST" = false ]; then
  echo -e "${RED}❌ Essential files missing! Restore from backup: $BACKUP_DIR${NC}"
  exit 1
fi
echo ""

# Step 12: Summary
echo "========================================="
echo -e "${GREEN}✅ CLEANUP COMPLETE!${NC}"
echo "========================================="
echo ""
echo "📦 Backup location: $BACKUP_DIR"
echo "📊 Space freed: Check 'du -sh .' to see new size"
echo ""
echo "✅ Safe to delete:"
echo "   - All coach JSON files (data in coaches_master.db)"
echo "   - All large team/drive JSON files (data in predictions.db)"
echo "   - Empty CSV files"
echo "   - Duplicate ' 2.json' files"
echo ""
echo "✅ Kept essential files:"
echo "   - fbs.json (team metadata for UI)"
echo "   - All database files"
echo "   - All config files (package.json, tsconfig.json, etc.)"
echo ""
echo "🧪 Next steps:"
echo "   1. Test your predictor: python graphqlpredictor.py"
echo "   2. Start frontend: cd frontend && npm run dev"
echo "   3. Verify UI loads correctly"
echo ""
echo "🔄 To rollback if issues:"
echo "   cp -r $BACKUP_DIR/instance instance"
echo "   cp -r $BACKUP_DIR/frontend_data frontend/src/data"
echo ""
