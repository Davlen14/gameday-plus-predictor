#!/bin/bash
# Monitor Big Ten ingestion progress

echo "🔍 MONITORING BIG TEN INGESTION"
echo "================================"
echo ""

while true; do
    clear
    echo "🏈 BIG TEN INGESTION PROGRESS"
    echo "=============================="
    echo ""
    
    # Check if process is running
    if ps aux | grep "ingest_by_conference" | grep -v grep > /dev/null; then
        echo "✅ Process running (PID: $(ps aux | grep 'ingest_by_conference' | grep -v grep | awk '{print $2}' | head -1))"
    else
        echo "⚠️  Process not running"
    fi
    
    echo ""
    echo "📊 DATABASE STATS:"
    sqlite3 instance/coaches_master.db << EOF
SELECT 
    '  Coaches: ' || COUNT(*) || ' / 18'
FROM coaches;

SELECT 
    '  Total Games: ' || COUNT(*)
FROM games;

SELECT
    '  Recruiting Classes: ' || COUNT(*)
FROM recruiting_classes;

SELECT
    '  Draft Picks: ' || COUNT(*)
FROM draft_picks;
EOF

    echo ""
    echo "👥 COACHES INGESTED:"
    sqlite3 instance/coaches_master.db "SELECT '  ' || id || '. ' || name || ' (' || current_school || ') - ' || (SELECT COUNT(*) FROM games WHERE coach_id = coaches.id) || ' games' FROM coaches ORDER BY id"
    
    echo ""
    echo "🔄 Next update in 10 seconds... (Ctrl+C to stop)"
    sleep 10
done
