#!/usr/bin/env python3
"""
Migrate remaining JSON files to database
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'

def create_new_tables():
    """Create tables for remaining data"""
    print("🔨 Creating new tables...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for drive efficiency metrics (react_power5_efficiency.json)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_drive_efficiency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            season INTEGER DEFAULT 2025,
            offensive_drives INTEGER,
            defensive_drives INTEGER,
            offensive_scoring INTEGER,
            defensive_scoring_allowed INTEGER,
            offensive_scoring_pct REAL,
            defensive_stop_pct REAL,
            avg_yards_per_drive REAL,
            avg_points_per_drive REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(team_name, season)
        )
    """)
    
    # Table for AP poll rankings (ap.json)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ap_poll_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL,
            season_type TEXT DEFAULT 'regular',
            week INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            school TEXT NOT NULL,
            conference TEXT,
            first_place_votes INTEGER,
            points INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(season, week, rank)
        )
    """)
    
    # Table for coaches poll rankings (coaches_simplified_ranked.json)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coaches_poll_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            school TEXT NOT NULL,
            conference TEXT,
            points INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(season, week, rank)
        )
    """)
    
    # Update win_probability_curves if it exists (complete_win_probabilities.json)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            season_type TEXT,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            home_score INTEGER,
            away_score INTEGER,
            home_postgame_wp REAL,
            away_postgame_wp REAL,
            home_pregame_wp REAL,
            away_pregame_wp REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(game_id)
        )
    """)
    
    # Indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_drive_efficiency_team ON team_drive_efficiency(team_name, season)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ap_poll_week ON ap_poll_rankings(season, week)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_coaches_poll_week ON coaches_poll_rankings(season, week)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_historical_games ON historical_game_results(season, week)")
    
    conn.commit()
    conn.close()
    print("  ✅ Created 4 new tables with indexes")

def migrate_drive_efficiency():
    """Migrate react_power5_efficiency.json"""
    print("\n📊 Migrating drive efficiency data...")
    
    with open('data/react_power5_efficiency.json', 'r') as f:
        efficiency_data = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for team_name, team_data in efficiency_data.items():
        cursor.execute("""
            INSERT OR REPLACE INTO team_drive_efficiency
            (team_name, season, offensive_drives, defensive_drives, 
             offensive_scoring, defensive_scoring_allowed,
             offensive_scoring_pct, defensive_stop_pct,
             avg_yards_per_drive, avg_points_per_drive)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            team_name, 2025,
            team_data.get('offensive_drives'),
            team_data.get('defensive_drives'),
            team_data.get('offensive_scoring'),
            team_data.get('defensive_scoring_allowed'),
            team_data.get('offensive_scoring_pct'),
            team_data.get('defensive_stop_pct'),
            team_data.get('avg_yards_per_drive'),
            team_data.get('avg_points_per_drive')
        ))
        count += 1
    
    conn.commit()
    conn.close()
    print(f"  ✅ Migrated {count} teams drive efficiency")

def migrate_ap_polls():
    """Migrate ap.json"""
    print("\n📊 Migrating AP poll rankings...")
    
    with open('data/ap.json', 'r') as f:
        ap_data = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for week_key, week_data in ap_data.items():
        week = week_data.get('week')
        season = week_data.get('season', 2025)
        
        for rank_data in week_data.get('ranks', []):
            cursor.execute("""
                INSERT OR REPLACE INTO ap_poll_rankings
                (season, week, rank, school, conference, first_place_votes, points)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                season, week,
                rank_data.get('rank'),
                rank_data.get('school'),
                rank_data.get('conference'),
                rank_data.get('firstPlaceVotes'),
                rank_data.get('points')
            ))
            count += 1
    
    conn.commit()
    conn.close()
    print(f"  ✅ Migrated {count} AP poll rankings")

def migrate_coaches_polls():
    """Migrate coaches_simplified_ranked.json"""
    print("\n📊 Migrating Coaches poll rankings...")
    
    with open('data/coaches_simplified_ranked.json', 'r') as f:
        coaches_data = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # This file has a different structure - it's coaches info, not poll rankings
    # Skip this one as it duplicates coach_rankings table
    print("  ⚠️  Skipping - data already in coach_rankings table")
    
    conn.close()

def migrate_win_probabilities():
    """Migrate complete_win_probabilities.json"""
    print("\n📊 Migrating historical game results...")
    
    with open('data/complete_win_probabilities.json', 'r') as f:
        games_data = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for game in games_data:
        cursor.execute("""
            INSERT OR REPLACE INTO historical_game_results
            (game_id, season, week, season_type, home_team, away_team,
             home_score, away_score, home_postgame_wp, away_postgame_wp,
             home_pregame_wp, away_pregame_wp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game.get('gameId'),
            game.get('season'),
            game.get('week'),
            game.get('seasonType'),
            game.get('homeTeam'),
            game.get('awayTeam'),
            game.get('homeScore'),
            game.get('awayScore'),
            game.get('homePostgameWP'),
            game.get('awayPostgameWP'),
            game.get('homePregameWP'),
            game.get('awayPregameWP')
        ))
        count += 1
    
    conn.commit()
    conn.close()
    print(f"  ✅ Migrated {count} historical game results")

def migrate_power5_teams():
    """
    Skip react_power5_teams.json - this is duplicate drive data
    Already have drives_complete table with 11,507 drives
    """
    print("\n📊 Checking react_power5_teams.json...")
    print("  ⚠️  Skipping - duplicate drive data already in drives_complete table")

if __name__ == '__main__':
    print("🚀 Migrating Remaining Data to Database")
    print("=" * 50)
    
    create_new_tables()
    migrate_drive_efficiency()
    migrate_ap_polls()
    migrate_coaches_polls()
    migrate_win_probabilities()
    migrate_power5_teams()
    
    print("\n" + "=" * 50)
    print("✅ Migration Complete!")
    print("\nDatabase Summary:")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM team_drive_efficiency")
    print(f"  Drive Efficiency: {cursor.fetchone()[0]} teams")
    
    cursor.execute("SELECT COUNT(*) FROM ap_poll_rankings")
    print(f"  AP Poll Rankings: {cursor.fetchone()[0]} entries")
    
    cursor.execute("SELECT COUNT(*) FROM historical_game_results")
    print(f"  Historical Games: {cursor.fetchone()[0]} games")
    
    conn.close()
