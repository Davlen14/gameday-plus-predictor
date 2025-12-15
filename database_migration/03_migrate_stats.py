#!/usr/bin/env python3
"""
Phase 3: Migrate Team Stats (EPA, Offensive, Defensive)
Migrates detailed team performance metrics from JSON files
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

def migrate_epa_metrics():
    """Migrate fbs_teams_stats_only.json"""
    print("\n📊 Migrating EPA Metrics...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB if needed for team lookups
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if not cursor.fetchone():
        print("  ⚠️  Teams table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    stats_file = os.path.join(DATA_DIR, 'fbs_teams_stats_only.json')
    if not os.path.exists(stats_file):
        print(f"  ⚠️  File not found: {stats_file}")
        conn.close()
        return
    
    with open(stats_file, 'r') as f:
        teams_data = json.load(f)
    
    migrated = 0
    for team_data in teams_data:
        team_name = team_data.get('team')
        team_id = get_team_id_from_name(cursor, team_name)
        
        if not team_id:
            print(f"  ⚠️  Team not found: {team_name}")
            continue
        
        stats = team_data.get('stats', {})
        season = team_data.get('season', 2025)
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO team_epa_metrics 
                (team_id, team_name, season, conference,
                 off_plays, off_ppa, off_success_rate, off_explosiveness, off_power_success, off_stuff_rate,
                 def_plays, def_ppa, def_success_rate, def_explosiveness, def_power_success, def_stuff_rate,
                 off_std_ppa, off_std_success_rate, off_std_explosiveness,
                 def_std_ppa, def_std_success_rate, def_std_explosiveness,
                 off_pass_down_ppa, off_pass_down_success_rate, off_pass_down_explosiveness,
                 def_pass_down_ppa, def_pass_down_success_rate, def_pass_down_explosiveness,
                 off_rush_ppa, off_rush_success_rate, off_rush_explosiveness,
                 def_rush_ppa, def_rush_success_rate, def_rush_explosiveness,
                 off_pass_ppa, off_pass_success_rate, off_pass_explosiveness,
                 def_pass_ppa, def_pass_success_rate, def_pass_explosiveness,
                 off_field_pos_avg_start, off_field_pos_avg_predicted_points,
                 def_field_pos_avg_start, def_field_pos_avg_predicted_points,
                 off_havoc_total, def_havoc_total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id, team_name, season, team_data.get('conference'),
                stats.get('offensivePlays'), stats.get('offensivePPA'), stats.get('offensiveSuccessRate'),
                stats.get('offensiveExplosiveness'), stats.get('offensivePowerSuccess'), stats.get('offensiveStuffRate'),
                stats.get('defensivePlays'), stats.get('defensivePPA'), stats.get('defensiveSuccessRate'),
                stats.get('defensiveExplosiveness'), stats.get('defensivePowerSuccess'), stats.get('defensiveStuffRate'),
                stats.get('offensiveStandardDownsPPA'), stats.get('offensiveStandardDownsSuccessRate'),
                stats.get('offensiveStandardDownsExplosiveness'),
                stats.get('defensiveStandardDownsPPA'), stats.get('defensiveStandardDownsSuccessRate'),
                stats.get('defensiveStandardDownsExplosiveness'),
                stats.get('offensivePassingDownsPPA'), stats.get('offensivePassingDownsSuccessRate'),
                stats.get('offensivePassingDownsExplosiveness'),
                stats.get('defensivePassingDownsPPA'), stats.get('defensivePassingDownsSuccessRate'),
                stats.get('defensivePassingDownsExplosiveness'),
                stats.get('offensiveRushingPPA'), stats.get('offensiveRushingSuccessRate'),
                stats.get('offensiveRushingExplosiveness'),
                stats.get('defensiveRushingPPA'), stats.get('defensiveRushingSuccessRate'),
                stats.get('defensiveRushingExplosiveness'),
                stats.get('offensivePassingPPA'), stats.get('offensivePassingSuccessRate'),
                stats.get('offensivePassingExplosiveness'),
                stats.get('defensivePassingPPA'), stats.get('defensivePassingSuccessRate'),
                stats.get('defensivePassingExplosiveness'),
                stats.get('offensiveFieldPosition'), stats.get('offensivePredictedPoints'),
                stats.get('defensiveFieldPosition'), stats.get('defensivePredictedPoints'),
                stats.get('offensiveHavoc'), stats.get('defensiveHavoc')
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {team_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} team EPA metrics")

def migrate_offensive_stats():
    """Migrate fbs_offensive_stats.json"""
    print("\n⚔️ Migrating Offensive Stats...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB if needed for team lookups
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if not cursor.fetchone():
        print("  ⚠️  Teams table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    stats_file = os.path.join(DATA_DIR, 'fbs_offensive_stats.json')
    if not os.path.exists(stats_file):
        print(f"  ⚠️  File not found: {stats_file}")
        conn.close()
        return
    
    with open(stats_file, 'r') as f:
        teams_data = json.load(f)
    
    migrated = 0
    for team_data in teams_data:
        team_name = team_data.get('team')
        team_id = get_team_id_from_name(cursor, team_name)
        
        if not team_id:
            continue
        
        stats = team_data.get('stats', {})
        season = team_data.get('season', 2025)
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO team_offensive_stats 
                (team_id, season, first_downs, third_down_conversions, third_downs, third_down_pct,
                 fourth_down_conversions, fourth_downs, fourth_down_pct,
                 total_yards, yards_per_game, yards_per_play,
                 passing_yards, passing_yards_per_game, rushing_yards, rushing_yards_per_game,
                 points, points_per_game, touchdowns,
                 fumbles_lost, interceptions_thrown, turnovers,
                 red_zone_attempts, red_zone_conversions, red_zone_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id, season,
                stats.get('firstDowns'), stats.get('thirdDownConversions'), stats.get('thirdDowns'),
                stats.get('thirdDownConversionPct'),
                stats.get('fourthDownConversions'), stats.get('fourthDowns'),
                stats.get('fourthDownConversionPct'),
                stats.get('totalYards'), stats.get('yardsPerGame'), stats.get('yardsPerPlay'),
                stats.get('passingYards'), stats.get('passingYardsPerGame'),
                stats.get('rushingYards'), stats.get('rushingYardsPerGame'),
                stats.get('points'), stats.get('pointsPerGame'), stats.get('touchdowns'),
                stats.get('fumblesLost'), stats.get('interceptions'), stats.get('turnovers'),
                stats.get('redZoneAttempts'), stats.get('redZoneConversions'), stats.get('redZonePct')
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {team_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} offensive stats")

def migrate_defensive_stats():
    """Migrate fbs_defensive_stats.json"""
    print("\n🛡️ Migrating Defensive Stats...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB if needed for team lookups
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    if not cursor.fetchone():
        print("  ⚠️  Teams table not found - attaching master database for lookups...")
        if os.path.exists(MASTER_DB_PATH):
            cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
            print("  ✅ Master database attached")
    
    stats_file = os.path.join(DATA_DIR, 'fbs_defensive_stats.json')
    if not os.path.exists(stats_file):
        print(f"  ⚠️  File not found: {stats_file}")
        conn.close()
        return
    
    with open(stats_file, 'r') as f:
        teams_data = json.load(f)
    
    migrated = 0
    for team_data in teams_data:
        team_name = team_data.get('team')
        team_id = get_team_id_from_name(cursor, team_name)
        
        if not team_id:
            continue
        
        stats = team_data.get('stats', {})
        season = team_data.get('season', 2025)
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO team_defensive_stats 
                (team_id, season, first_downs_allowed, third_down_conversions_allowed, 
                 third_downs_allowed, third_down_pct_allowed,
                 fourth_down_conversions_allowed, fourth_downs_allowed, fourth_down_pct_allowed,
                 total_yards_allowed, yards_per_game_allowed, yards_per_play_allowed,
                 passing_yards_allowed, passing_yards_per_game_allowed,
                 rushing_yards_allowed, rushing_yards_per_game_allowed,
                 points_allowed, points_per_game_allowed, touchdowns_allowed,
                 fumbles_recovered, interceptions, turnovers_gained,
                 sacks, tackles_for_loss,
                 red_zone_attempts_allowed, red_zone_conversions_allowed, red_zone_pct_allowed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id, season,
                stats.get('firstDownsAllowed'), stats.get('thirdDownConversionsAllowed'),
                stats.get('thirdDownsAllowed'), stats.get('thirdDownPctAllowed'),
                stats.get('fourthDownConversionsAllowed'), stats.get('fourthDownsAllowed'),
                stats.get('fourthDownPctAllowed'),
                stats.get('totalYardsAllowed'), stats.get('yardsPerGameAllowed'),
                stats.get('yardsPerPlayAllowed'),
                stats.get('passingYardsAllowed'), stats.get('passingYardsPerGameAllowed'),
                stats.get('rushingYardsAllowed'), stats.get('rushingYardsPerGameAllowed'),
                stats.get('pointsAllowed'), stats.get('pointsPerGameAllowed'),
                stats.get('touchdownsAllowed'),
                stats.get('fumblesRecovered'), stats.get('interceptions'), stats.get('turnoversGained'),
                stats.get('sacks'), stats.get('tacklesForLoss'),
                stats.get('redZoneAttemptsAllowed'), stats.get('redZoneConversionsAllowed'),
                stats.get('redZonePctAllowed')
            ))
            migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating {team_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ Migrated {migrated} defensive stats")

def verify_migration():
    """Verify stats migration"""
    print("\n🔍 Verifying Migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    checks = [
        ("team_epa_metrics", "SELECT COUNT(*) FROM team_epa_metrics"),
        ("team_offensive_stats", "SELECT COUNT(*) FROM team_offensive_stats"),
        ("team_defensive_stats", "SELECT COUNT(*) FROM team_defensive_stats"),
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
    print("🚀 Phase 3: Migrating Team Stats")
    print("=" * 50)
    
    migrate_epa_metrics()
    migrate_offensive_stats()
    migrate_defensive_stats()
    
    print("\n" + "=" * 50)
    if verify_migration():
        print("✅ Phase 3 Complete!")
        print("Next: Run 04_migrate_drives.py")
    else:
        print("⚠️  Some tables have no data. Check warnings above.")
