#!/usr/bin/env python3
"""
Phase 2: Migrate Core Data (Coaches, Teams, Conferences, Rankings)
Migrates data from JSON files that are 100% redundant
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
    # Try local teams table first
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

def migrate_conferences():
    """Migrate react_fbs_conferences.json"""
    print("\n📊 Migrating Conferences...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    conf_file = os.path.join(DATA_DIR, 'react_fbs_conferences.json')
    if not os.path.exists(conf_file):
        print(f"  ⚠️  File not found: {conf_file}")
        conn.close()
        return
    
    with open(conf_file, 'r') as f:
        conferences = json.load(f)
    
    migrated = 0
    for conf_name, conf_data in conferences.items():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO conferences (name, abbreviation, division, classification, total_teams)
                VALUES (?, ?, ?, ?, ?)
            """, (
                conf_name,
                conf_data.get('abbreviation', conf_name[:3].upper()),
                conf_data.get('division', 'FBS'),
                'FBS',
                len(conf_data.get('teams', []))
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {conf_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} conferences")

def migrate_team_power_rankings():
    """Migrate react_fbs_team_rankings.json"""
    print("\n📊 Migrating Team Power Rankings...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if teams table exists, if not attach master DB
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if not cursor.fetchone():
        print("  ⚠️  Teams table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    rankings_file = os.path.join(DATA_DIR, 'react_fbs_team_rankings.json')
    if not os.path.exists(rankings_file):
        print(f"  ⚠️  File not found: {rankings_file}")
        conn.close()
        return
    
    with open(rankings_file, 'r') as f:
        rankings_data = json.load(f)
    
    migrated = 0
    season = 2025  # Current season
    week = 15  # Week 15 data
    
    # Handle both dict and array formats
    teams_list = rankings_data.values() if isinstance(rankings_data, dict) else rankings_data
    
    for team_data in teams_list:
        team_name = team_data.get('team')
        team_id = get_team_id_from_name(cursor, team_name)
        
        if not team_id:
            print(f"  ⚠️  Team not found: {team_name}")
            continue
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO team_power_rankings 
                (team_id, team_name, season, week, ap_rank, sp_rank, fpi_rank, 
                 srs_rank, elo_rank, composite_rank, power_rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id,
                team_name,
                season,
                week,
                team_data.get('apRank'),
                team_data.get('spRank'),
                team_data.get('fpiRank'),
                team_data.get('srsRank'),
                team_data.get('eloRank'),
                team_data.get('rank'),
                team_data.get('rating', 0.0)
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {team_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} team rankings")

def migrate_coach_rankings():
    """Migrate coaches_advanced_rankings.json"""
    print("\n📊 Migrating Coach Rankings...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB if needed for coach lookups
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coaches'")
    if not cursor.fetchone():
        print("  ⚠️  Coaches table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    coach_file = os.path.join(DATA_DIR, 'coaches_advanced_rankings.json')
    if not os.path.exists(coach_file):
        print(f"  ⚠️  File not found: {coach_file}")
        conn.close()
        return
    
    with open(coach_file, 'r') as f:
        coaches_data = json.load(f)
    
    migrated = 0
    season = 2025
    
    for coach_data in coaches_data:
        coach_name = coach_data.get('name')
        
        # Find coach_id from master database
        try:
            cursor.execute("SELECT id FROM master.coaches WHERE name = ?", (coach_name,))
            result = cursor.fetchone()
            if not result:
                # Skip coaches not in master DB
                continue
            coach_id = result[0]
        except:
            print(f"  ⚠️  Coach not found: {coach_name}")
            continue
        
        # Parse current season record
        current_record = coach_data.get('2025Record', '0-0')
        try:
            wins, losses = map(int, current_record.split('-'))
        except:
            wins, losses = 0, 0
        
        # Parse vs ranked record
        vs_ranked = coach_data.get('vsRanked', {})
        vs_ranked_record = vs_ranked.get('record', '0-0-0')
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO coach_rankings 
                (coach_id, season, overall_rank, win_pct_rank, total_wins_rank,
                 current_season_rank, current_season_record, current_season_wins, current_season_losses,
                 vs_ranked_record, vs_ranked_win_pct, vs_top_10_record, vs_top_25_record,
                 data_driven_score, talent_context_score, big_game_score, 
                 recruiting_score, nfl_development_score, betting_performance_score,
                 consistency_score, composite_score, composite_rank)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coach_id,
                season,
                coach_data.get('overallRank'),
                coach_data.get('winPctRank'),
                coach_data.get('totalWinsRank'),
                coach_data.get('current2025Rank'),
                current_record,
                wins,
                losses,
                vs_ranked_record,
                vs_ranked.get('winPct', 0.0),
                vs_ranked.get('vsTop10', {}).get('record', '0-0-0') if isinstance(vs_ranked.get('vsTop10'), dict) else vs_ranked.get('vsTop10', '0-0-0'),
                vs_ranked.get('vsTop5', {}).get('record', '0-0-0') if isinstance(vs_ranked.get('vsTop5'), dict) else vs_ranked.get('vsTop5', '0-0-0'),
                0.0,  # data_driven_score - not in JSON
                0.0,  # talent_context_score - not in JSON
                0.0,  # big_game_score - not in JSON
                0.0,  # recruiting_score - not in JSON
                0.0,  # nfl_development_score - not in JSON
                0.0,  # betting_performance_score - not in JSON
                0.0,  # consistency_score - not in JSON
                coach_data.get('composite_score', 0.0),
                coach_data.get('composite_rank', 0)
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {coach_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} coach rankings")

def verify_migration():
    """Verify core data migration"""
    print("\n🔍 Verifying Migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    checks = [
        ("conferences", "SELECT COUNT(*) FROM conferences"),
        ("team_power_rankings", "SELECT COUNT(*) FROM team_power_rankings"),
        ("coach_rankings", "SELECT COUNT(*) FROM coach_rankings"),
    ]
    
    all_passed = True
    for table, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        status = "✅" if count > 0 else "❌"
        print(f"  {status} {table}: {count} records")
        if count == 0:
            all_passed = False
    
    conn.close()
    
    return all_passed

if __name__ == '__main__':
    print("🚀 Phase 2: Migrating Core Data")
    print("=" * 50)
    
    migrate_conferences()
    migrate_team_power_rankings()
    migrate_coach_rankings()
    
    print("\n" + "=" * 50)
    if verify_migration():
        print("✅ Phase 2 Complete!")
        print("Next: Run 03_migrate_stats.py")
    else:
        print("⚠️  Some tables have no data. Check warnings above.")
