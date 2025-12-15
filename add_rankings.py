#!/usr/bin/env python3
"""
Add ranking columns to team_seasons table for all key metrics
This script calculates and populates rankings for each season and metric
"""

import sqlite3
from collections import defaultdict

DB_PATH = 'instance/coaches_master.db'

# New ranking columns to add
NEW_RANKING_COLS = {
    'fpi_offense_efficiency_rank': 'fpi_offense_efficiency',
    'fpi_defense_efficiency_rank': 'fpi_defense_efficiency',
    'sp_offense_rank': 'sp_offense',
    'sp_defense_rank': 'sp_defense',
    'off_ppa_rank': 'off_ppa',
    'def_ppa_rank': 'def_ppa',
    'recruiting_points_rank': 'recruiting_points',
    'talent_composite_rank': 'talent_composite',
}

def add_ranking_columns():
    """Add new ranking columns to team_seasons table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(team_seasons)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    
    # Add missing columns
    for col_name in NEW_RANKING_COLS.keys():
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE team_seasons ADD COLUMN {col_name} INTEGER DEFAULT NULL")
            print(f"✓ Added column: {col_name}")
        else:
            print(f"✓ Column already exists: {col_name}")
    
    conn.commit()
    conn.close()

def calculate_rankings():
    """Calculate rankings for each season and metric"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all seasons
    cursor.execute("SELECT DISTINCT season FROM team_seasons ORDER BY season DESC")
    seasons = [row[0] for row in cursor.fetchall()]
    
    print(f"\nCalculating rankings for {len(seasons)} seasons...")
    
    for season in seasons:
        print(f"\nSeason {season}:")
        
        for rank_col, metric_col in NEW_RANKING_COLS.items():
            # Get all teams with this metric for this season (sorted by metric value DESC)
            cursor.execute(f"""
                SELECT id, team_id, {metric_col}
                FROM team_seasons
                WHERE season = ? AND {metric_col} IS NOT NULL
                ORDER BY {metric_col} DESC
            """, (season,))
            
            teams = cursor.fetchall()
            
            # Assign rankings
            for rank, (ts_id, team_id, value) in enumerate(teams, 1):
                cursor.execute(f"""
                    UPDATE team_seasons
                    SET {rank_col} = ?
                    WHERE id = ?
                """, (rank, ts_id))
            
            if teams:
                print(f"  ✓ {rank_col}: {len(teams)} teams ranked")
    
    conn.commit()
    conn.close()

def display_rankings_sample():
    """Display sample ranking data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get a sample team with all rankings
    cursor.execute("""
        SELECT ts.season, ts.team_id,
               ts.fpi_ranking, ts.fpi_offense_efficiency_rank, ts.fpi_defense_efficiency_rank,
               ts.sp_ranking, ts.sp_offense_rank, ts.sp_defense_rank,
               ts.recruiting_rank, ts.talent_composite_rank
        FROM team_seasons ts
        WHERE ts.season = 2025
        ORDER BY ts.fpi_ranking ASC
        LIMIT 5
    """)
    
    print("\n\nSample Rankings (2025 Season, Top 5 by FPI):")
    print("-" * 120)
    print(f"{'Team ID':<10} {'FPI':<8} {'FPI Off':<10} {'FPI Def':<10} {'SP+':<8} {'SP+ Off':<10} {'SP+ Def':<10} {'Recruit':<10} {'Talent':<10}")
    print("-" * 120)
    
    for row in cursor.fetchall():
        season, team_id, fpi_r, fpi_off, fpi_def, sp_r, sp_off, sp_def, rec_r, tal_r = row
        print(f"{team_id:<10} {fpi_r or '-':<8} {fpi_off or '-':<10} {fpi_def or '-':<10} {sp_r or '-':<8} {sp_off or '-':<10} {sp_def or '-':<10} {rec_r or '-':<10} {tal_r or '-':<10}")
    
    conn.close()

if __name__ == '__main__':
    print("=" * 120)
    print("GAMEDAY+ RANKING GENERATOR")
    print("=" * 120)
    
    print("\n1. Adding ranking columns to team_seasons table...")
    add_ranking_columns()
    
    print("\n2. Calculating rankings for all seasons and metrics...")
    calculate_rankings()
    
    print("\n3. Displaying sample rankings...")
    display_rankings_sample()
    
    print("\n" + "=" * 120)
    print("✓ Rankings successfully added and calculated!")
    print("=" * 120)
