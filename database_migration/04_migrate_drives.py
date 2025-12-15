#!/usr/bin/env python3
"""
Phase 4: Migrate Drives Data (11,507+ drives from power5_drives_only.json)
This is the largest migration - may take 5-10 minutes
"""

import sqlite3
import json
import os
from datetime import datetime

# SAFE APPROACH: Use separate predictions database
DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'
DATA_DIR = 'data'

def get_team_id_from_name(cursor, team_name):
    """Helper to get team_id from team name"""
    # Check if teams table exists locally
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if cursor.fetchone():
        cursor.execute("SELECT id FROM teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
    
    # Try attached master database
    try:
        cursor.execute("SELECT id FROM master.teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except:
        return None

def migrate_drives():
    """Migrate power5_drives_only.json"""
    print("\n🚚 Migrating Drive Data (This may take a few minutes)...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB if needed for team lookups
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if not cursor.fetchone():
        print("  ⚠️  Teams table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    drives_file = os.path.join(DATA_DIR, 'power5_drives_only.json')
    if not os.path.exists(drives_file):
        print(f"  ⚠️  File not found: {drives_file}")
        conn.close()
        return
    
    print("  📖 Loading JSON file...")
    with open(drives_file, 'r') as f:
        drives_data = json.load(f)
    
    print(f"  📊 Found {len(drives_data):,} drives to migrate")
    
    # Batch insert for performance
    drives_to_insert = []
    errors = 0
    
    for i, drive in enumerate(drives_data):
        if i % 1000 == 0 and i > 0:
            print(f"    Processing drive {i:,}/{len(drives_data):,}...")
        
        # Get team_id
        team_name = drive.get('offense')
        team_id = get_team_id_from_name(cursor, team_name)
        
        # Extract timing info
        start_time = drive.get('startTime', {})
        end_time = drive.get('endTime', {})
        elapsed = drive.get('elapsed', {})
        
        try:
            drive_tuple = (
                drive.get('id'),
                drive.get('gameId'),
                team_id,
                drive.get('offense'),
                drive.get('offenseConference'),
                drive.get('defense'),
                drive.get('defenseConference'),
                drive.get('driveNumber'),
                drive.get('season'),
                drive.get('week'),
                1 if drive.get('scoring') else 0,
                drive.get('driveResult'),
                drive.get('startPeriod'),
                drive.get('startYardline'),
                drive.get('startYardsToGoal'),
                drive.get('endPeriod'),
                drive.get('endYardline'),
                drive.get('endYardsToGoal'),
                start_time.get('minutes'),
                start_time.get('seconds'),
                end_time.get('minutes'),
                end_time.get('seconds'),
                elapsed.get('minutes'),
                elapsed.get('seconds'),
                1 if drive.get('isHomeOffense') else 0,
                drive.get('startOffenseScore'),
                drive.get('startDefenseScore'),
                drive.get('endOffenseScore'),
                drive.get('endDefenseScore'),
                drive.get('plays'),
                drive.get('yards')
            )
            drives_to_insert.append(drive_tuple)
            
        except Exception as e:
            errors += 1
            if errors < 10:  # Only show first 10 errors
                print(f"  ⚠️  Error processing drive {drive.get('id')}: {e}")
    
    # Batch insert
    print(f"\n  💾 Inserting {len(drives_to_insert):,} drives into database...")
    try:
        cursor.executemany("""
            INSERT OR REPLACE INTO drives_complete 
            (id, game_id, team_id, offense, offense_conference, defense, defense_conference,
             drive_number, season, week, scoring, drive_result,
             start_period, start_yardline, start_yards_to_goal,
             end_period, end_yardline, end_yards_to_goal,
             start_time_minutes, start_time_seconds, end_time_minutes, end_time_seconds,
             elapsed_minutes, elapsed_seconds,
             is_home_offense, start_offense_score, start_defense_score,
             end_offense_score, end_defense_score, plays_count, yards)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, drives_to_insert)
        
        conn.commit()
        print(f"  ✅ Successfully migrated {len(drives_to_insert):,} drives")
        if errors > 0:
            print(f"  ⚠️  Skipped {errors} drives due to errors")
        
    except Exception as e:
        print(f"  ❌ Batch insert failed: {e}")
        conn.rollback()
    
    conn.close()

def create_drive_indexes():
    """Create indexes for fast querying"""
    print("\n🔍 Creating Indexes for Drive Queries...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_drives_team_season ON drives_complete(team_id, season)",
        "CREATE INDEX IF NOT EXISTS idx_drives_offense_season ON drives_complete(offense, season)",
        "CREATE INDEX IF NOT EXISTS idx_drives_scoring ON drives_complete(scoring, season)",
        "CREATE INDEX IF NOT EXISTS idx_drives_game ON drives_complete(game_id)",
        "CREATE INDEX IF NOT EXISTS idx_drives_week ON drives_complete(season, week)",
        "CREATE INDEX IF NOT EXISTS idx_drives_result ON drives_complete(drive_result)",
    ]
    
    for idx_sql in indexes:
        try:
            cursor.execute(idx_sql)
            print(f"  ✅ Created index")
        except Exception as e:
            print(f"  ⚠️  Index creation warning: {e}")
    
    conn.commit()
    conn.close()
    print("  ✅ All indexes created")

def analyze_drives():
    """Analyze migrated drive data"""
    print("\n📊 Analyzing Drive Data...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total drives
    cursor.execute("SELECT COUNT(*) FROM drives_complete")
    total = cursor.fetchone()[0]
    print(f"  📈 Total Drives: {total:,}")
    
    # Scoring drives
    cursor.execute("SELECT COUNT(*) FROM drives_complete WHERE scoring = 1")
    scoring = cursor.fetchone()[0]
    print(f"  🏈 Scoring Drives: {scoring:,} ({scoring/total*100:.1f}%)")
    
    # Drives by season
    cursor.execute("SELECT season, COUNT(*) FROM drives_complete GROUP BY season ORDER BY season")
    seasons = cursor.fetchall()
    print(f"\n  📅 Drives by Season:")
    for season, count in seasons:
        print(f"     {season}: {count:,} drives")
    
    # Top 10 teams by total drives
    cursor.execute("""
        SELECT offense, COUNT(*) as drive_count 
        FROM drives_complete 
        GROUP BY offense 
        ORDER BY drive_count DESC 
        LIMIT 10
    """)
    top_teams = cursor.fetchall()
    print(f"\n  🏆 Top 10 Teams by Drive Count:")
    for i, (team, count) in enumerate(top_teams, 1):
        print(f"     {i}. {team}: {count:,} drives")
    
    conn.close()

def verify_migration():
    """Verify drives migration"""
    print("\n🔍 Verifying Migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM drives_complete")
    count = cursor.fetchone()[0]
    
    # Expected ~11,507 drives
    expected_min = 10000
    expected_max = 12000
    
    if expected_min <= count <= expected_max:
        print(f"  ✅ Drive count looks good: {count:,} drives")
        status = True
    else:
        print(f"  ⚠️  Unexpected drive count: {count:,} (expected {expected_min:,}-{expected_max:,})")
        status = False
    
    conn.close()
    return status

if __name__ == '__main__':
    print("🚀 Phase 4: Migrating Drive Data")
    print("=" * 50)
    print("⏱️  This is the largest migration and may take 5-10 minutes")
    print("=" * 50)
    
    start_time = datetime.now()
    
    migrate_drives()
    create_drive_indexes()
    analyze_drives()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 50)
    print(f"⏱️  Migration completed in {duration:.1f} seconds")
    
    if verify_migration():
        print("✅ Phase 4 Complete!")
        print("Next: Run 05_migrate_players.py")
    else:
        print("⚠️  Verification failed. Check warnings above.")
