#!/usr/bin/env python3
"""
MASTER MIGRATION SCRIPT
Runs all phases in sequence with progress tracking
"""

import sys
import os
import subprocess
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# SAFE APPROACH: Create separate predictions database
DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def run_phase(phase_num, script_name, description):
    """Run a migration phase"""
    print_header(f"PHASE {phase_num}: {description}")
    
    script_path = os.path.join('database_migration', script_name)
    
    try:
        result = subprocess.run(
            ['python3', script_path],
            capture_output=False,
            text=True,
            check=True
        )
        print(f"\n✅ Phase {phase_num} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Phase {phase_num} failed with error code {e.returncode}")
        print("Check the output above for details.")
        return False
    except FileNotFoundError:
        print(f"\n❌ Script not found: {script_path}")
        return False

def check_safe_mode():
    """Verify safe mode setup"""
    print_header("SAFE MODE VERIFICATION")
    
    print(f"✅ Master Database: {MASTER_DB_PATH}")
    if os.path.exists(MASTER_DB_PATH):
        size = os.path.getsize(MASTER_DB_PATH) / (1024*1024)
        print(f"   📊 Size: {size:.1f} MB (WILL NOT BE TOUCHED)")
    else:
        print(f"   ⚠️  Not found (will use for merge later)")
    
    print(f"\n📊 New Predictions Database: {DB_PATH}")
    if os.path.exists(DB_PATH):
        print(f"   ⚠️  Already exists - will be overwritten")
        response = input("\n   Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            return False
        os.remove(DB_PATH)
        print(f"   🗑️  Deleted old {DB_PATH}")
    else:
        print(f"   ✅ Will be created fresh")
    
    return True

def estimate_time():
    """Estimate total migration time"""
    print_header("MIGRATION TIME ESTIMATE")
    
    print("Phase 1: Schema Creation      ~  30 seconds")
    print("Phase 2: Core Data            ~  1 minute")
    print("Phase 3: Team Stats           ~  2 minutes")
    print("Phase 4: Drives (LARGE)       ~  5-10 minutes")
    print("Phase 5: Validation           ~  1 minute")
    print("-" * 50)
    print("TOTAL ESTIMATED TIME:         ~  10-15 minutes")
    print("\n☕ Grab a coffee - this will take a bit!")

def show_final_stats():
    """Show final database statistics"""
    print_header("FINAL DATABASE STATISTICS")
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get table counts
    tables = [
        'teams', 'coaches', 'games', 
        'team_epa_metrics', 'team_offensive_stats', 'team_defensive_stats',
        'drives_complete', 'player_efficiency', 'coach_rankings',
        'team_power_rankings', 'conferences'
    ]
    
    print("\n📊 Record Counts:")
    total_records = 0
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"  {table:.<35} {count:>10,}")
        except:
            pass
    
    print(f"\n{'TOTAL RECORDS':.<35} {total_records:>10,}")
    
    # Database size
    db_size = os.path.getsize(DB_PATH) / (1024*1024)
    print(f"\n💾 Database Size: {db_size:.1f} MB")
    
    conn.close()

def main():
    """Run complete migration"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🏈 GAMEDAY+ COMPLETE DATABASE MIGRATION 🏈            ║
    ║                                                               ║
    ║     Migrating 22 JSON Files → Single Database               ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"📅 Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Estimate time
    estimate_time()
    
    # Confirm
    response = input("\n🚀 Ready to begin migration? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Migration cancelled")
        return
    
    start_time = datetime.now()
    
    # Safe mode check
    if not check_safe_mode():
        print("❌ Aborted by user")
        return
    
    # Phase 1: Schema
    if not run_phase(1, '01_create_schema.py', 'Create Database Schema'):
        return
    
    # Phase 2: Core Data
    if not run_phase(2, '02_migrate_core_data.py', 'Migrate Core Data'):
        return
    
    # Phase 3: Stats
    if not run_phase(3, '03_migrate_stats.py', 'Migrate Team Stats'):
        return
    
    # Phase 4: Drives (BIG ONE)
    print("\n⚠️  PHASE 4 IS LARGE - This will take 5-10 minutes...")
    if not run_phase(4, '04_migrate_drives.py', 'Migrate Drive Data'):
        return
    
    # Validation
    print_header("VALIDATION")
    validation_result = subprocess.run(
        ['python3', 'database_migration/validate_migration.py'],
        capture_output=False
    )
    
    if validation_result.returncode != 0:
        print("\n⚠️  Validation failed! Review errors above.")
        print("Database has been created but may have issues.")
        return
    
    # Show stats
    show_final_stats()
    
    # Calculate duration
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Success message
    print_header("MIGRATION COMPLETE!")
    print(f"""
    ✅ All phases completed successfully!
    
    ⏱️  Total Time: {duration/60:.1f} minutes
    📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
    
    🛡️  SAFE MODE: All data in predictions.db
    ✅ Your coaches_master.db was NOT modified
    
    🎯 NEXT STEPS:
    
    1. Test predictor with predictions.db:
       python run.py "Ohio State" "Michigan"
    
    2. Verify accuracy (compare to JSON baseline)
    
    3. MERGE into master database (when confident):
       python database_migration/merge_databases.py
    
    4. After merge, update predictor code to use coaches_master.db
    
    5. Archive JSON files:
       mkdir -p data/archived_json_backup
       mv data/*.json data/archived_json_backup/
    
    🏆 Zero risk approach - your production DB stays safe! 🏆
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration interrupted by user")
        print("Database may be in incomplete state")
        print("Restore from backup if needed")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
