#!/bin/bash
# Archive migrated JSON files

echo "📦 Archiving migrated JSON files..."

# Create archive directory
mkdir -p data/archived_json_backup

# List of files to archive
files=(
    "data/power5_drives_only.json"
    "data/coaches_advanced_rankings.json"
    "data/react_fbs_team_rankings.json"
    "data/fbs_teams_stats_only.json"
    "data/fbs_offensive_stats.json"
    "data/fbs_defensive_stats.json"
    "data/team_season_summaries_clean.json"
    "data/react_power5_efficiency.json"
    "data/complete_win_probabilities.json"
    "data/ap.json"
    "data/react_power5_teams.json"
    "data/coaches_simplified_ranked.json"
)

# Move files
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  Moving $file..."
        mv "$file" data/archived_json_backup/
    else
        echo "  ⚠️  $file not found"
    fi
done

echo ""
echo "✅ Archive complete!"
echo "   Files moved to: data/archived_json_backup/"
echo ""
echo "📊 Summary:"
ls -1 data/archived_json_backup/ | wc -l | xargs echo "   Files archived:"
du -sh data/archived_json_backup/ | awk '{print "   Total size: " $1}'
