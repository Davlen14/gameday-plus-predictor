#!/usr/bin/env python3
"""
PARALLEL Team Metrics Ingestion - 6x faster with concurrent workers
"""

import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from ingest_all_team_metrics_rest import ComprehensiveTeamMetricsIngestor
import threading

# Thread-safe counter for progress tracking
class ProgressTracker:
    def __init__(self, total):
        self.lock = threading.Lock()
        self.completed = 0
        self.total = total
        self.errors = []
    
    def increment(self, team_name, success=True, error_msg=None):
        with self.lock:
            self.completed += 1
            if not success:
                self.errors.append((team_name, error_msg))
            print(f"[{self.completed}/{self.total}] {'✅' if success else '❌'} {team_name}")

def ingest_single_team(team_name, api_key, progress):
    """Ingest metrics for a single team"""
    try:
        ingestor = ComprehensiveTeamMetricsIngestor(api_key=api_key)
        ingestor.ingest_team_metrics(team_name, start_year=2000, end_year=2025)
        progress.increment(team_name, success=True)
        return True
    except Exception as e:
        progress.increment(team_name, success=False, error_msg=str(e))
        return False

if __name__ == "__main__":
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    # Get teams that DON'T have advanced metrics yet
    conn = sqlite3.connect("instance/coaches_master.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.school 
        FROM teams t
        LEFT JOIN team_seasons ts ON t.id = ts.team_id AND ts.off_ppa IS NOT NULL
        GROUP BY t.school
        HAVING COUNT(ts.team_id) = 0
        ORDER BY t.school
    """)
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print("🏈 PARALLEL TEAM METRICS INGESTION")
    print("=" * 80)
    print(f"📊 Teams to process: {len(teams)}")
    print(f"⚡ Parallel workers: 6")
    print(f"📅 Years: 2000-2025 (26 seasons per team)")
    print("=" * 80)
    print()
    
    progress = ProgressTracker(len(teams))
    
    # Process teams in parallel with 6 workers
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(ingest_single_team, team, api_key, progress): team 
            for team in teams
        }
        
        # Wait for all to complete
        for future in as_completed(futures):
            pass  # Progress is tracked in the callback
    
    print("\n" + "=" * 80)
    print("✅ PARALLEL INGESTION COMPLETE!")
    print("=" * 80)
    print(f"Successfully processed: {progress.total - len(progress.errors)} teams")
    
    if progress.errors:
        print(f"\n⚠️  Errors ({len(progress.errors)} teams):")
        for team, error in progress.errors[:10]:
            print(f"  - {team}: {error[:100]}")
    
    # Now batch update talent & recruiting for all teams
    print("\n" + "=" * 80)
    print("🎓 Updating talent & recruiting data...")
    ingestor = ComprehensiveTeamMetricsIngestor(api_key=api_key)
    ingestor.batch_update_talent_recruiting(start_year=2000, end_year=2025)
    
    print("\n✅ ALL DONE!")
