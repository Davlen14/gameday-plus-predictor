#!/usr/bin/env python3
"""
Simple stats migration - just migrate the essential fields that predictor uses
"""

import sqlite3
import json
import os

DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'

def migrate_essential_stats():
    """Migrate just the essential team stats that the predictor uses"""
    print("🚀 Migrating Essential Team Stats...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Attach master DB for team lookups
    cursor.execute(f"ATTACH DATABASE '{MASTER_DB_PATH}' AS master")
    
    # 1. Migrate EPA metrics (fbs_teams_stats_only.json)
    print("\n📊 Migrating EPA metrics...")
    with open('data/fbs_teams_stats_only.json', 'r') as f:
        epa_data = json.load(f)
    
    epa_count = 0
    for team in epa_data:
        team_name = team.get('team')
        cursor.execute("SELECT id FROM master.teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        if not result:
            continue
        
        team_id = result[0]
        stats = team.get('stats', {})
        
        # Insert with NULL for columns we don't have data for
        cursor.execute("""
            INSERT OR REPLACE INTO team_epa_metrics 
            (team_id, team_name, season, conference, off_plays, off_ppa, off_success_rate, 
             off_explosiveness, def_plays, def_ppa, def_success_rate, def_explosiveness)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            team_id, team_name, 2025, team.get('conference'),
            stats.get('offensivePlays'), stats.get('offensivePPA'), stats.get('offensiveSuccessRate'),
            stats.get('offensiveExplosiveness'),
            stats.get('defensivePlays'), stats.get('defensivePPA'), stats.get('defensiveSuccessRate'),
            stats.get('defensiveExplosiveness')
        ))
        epa_count += 1
    
    print(f"  ✅ Migrated {epa_count} teams EPA metrics")
    
    # 2. Migrate offensive stats (fbs_offensive_stats.json)
    print("\n📊 Migrating Offensive stats...")
    with open('data/fbs_offensive_stats.json', 'r') as f:
        off_file = json.load(f)
    
    off_data = off_file.get('offensive_stats', [])
    off_count = 0
    for team in off_data:
        team_name = team.get('team')
        cursor.execute("SELECT id FROM master.teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        if not result:
            continue
        
        team_id = result[0]
        
        cursor.execute("""
            INSERT OR REPLACE INTO team_offensive_stats 
            (team_id, season, yards_per_play, yards_per_game, points_per_game)
            VALUES (?, ?, ?, ?, ?)
        """, (
            team_id, 2025, 
            team.get('yardsPerPlay'), 
            team.get('yardsPerGame'), team.get('pointsPerGame')
        ))
        off_count += 1
    
    print(f"  ✅ Migrated {off_count} teams offensive stats")
    
    # 3. Migrate defensive stats (fbs_defensive_stats.json)
    print("\n📊 Migrating Defensive stats...")
    with open('data/fbs_defensive_stats.json', 'r') as f:
        def_file = json.load(f)
    
    def_data = def_file.get('defensive_stats', [])
    def_count = 0
    for team in def_data:
        team_name = team.get('team')
        cursor.execute("SELECT id FROM master.teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        if not result:
            continue
        
        team_id = result[0]
        
        cursor.execute("""
            INSERT OR REPLACE INTO team_defensive_stats 
            (team_id, season, yards_per_play_allowed, yards_per_game_allowed, points_per_game_allowed)
            VALUES (?, ?, ?, ?, ?)
        """, (
            team_id, 2025,
            team.get('yardsPerPlay'),
            team.get('yardsPerGame'), team.get('pointsPerGame')
        ))
        def_count += 1
    
    print(f"  ✅ Migrated {def_count} teams defensive stats")
    
    # 4. Migrate season summaries (team_season_summaries_clean.json)
    print("\n📊 Migrating Season summaries...")
    with open('data/team_season_summaries_clean.json', 'r') as f:
        summary_data = json.load(f)
    
    summary_count = 0
    for team in summary_data:
        team_name = team.get('team')
        cursor.execute("SELECT id FROM master.teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        if not result:
            continue
        
        team_id = result[0]
        
        cursor.execute("""
            INSERT OR REPLACE INTO team_season_summaries
            (team_id, team_name, season, wins, losses, win_pct)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            team_id, team_name, 2025,
            team.get('wins'), team.get('losses'), team.get('winPercent')
        ))
        summary_count += 1
    
    print(f"  ✅ Migrated {summary_count} teams season summaries")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Migration complete!")
    print(f"   EPA: {epa_count} teams")
    print(f"   Offensive: {off_count} teams")
    print(f"   Defensive: {def_count} teams")
    print(f"   Summaries: {summary_count} teams")

if __name__ == '__main__':
    migrate_essential_stats()
