#!/usr/bin/env python3
"""
Create gameday_analytics.db - Central database for all team drives and plays data
"""

import sqlite3
import os

DB_PATH = 'gameday_analytics.db'

def create_database():
    """Create database with optimized schema for teams, games, drives, and plays"""
    
    # Remove old database if it exists
    if os.path.exists(DB_PATH):
        print(f"⚠️  Removing existing {DB_PATH}...")
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🏗️  Creating database schema...")
    
    # Teams table - Central hub, everything references this
    cursor.execute("""
        CREATE TABLE teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT UNIQUE NOT NULL,
            abbreviation TEXT,
            conference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created teams table")
    
    # Games table - Matchup information
    cursor.execute("""
        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER UNIQUE NOT NULL,
            home_team_id INTEGER,
            away_team_id INTEGER,
            season INTEGER DEFAULT 2025,
            week INTEGER,
            game_date TEXT,
            home_score INTEGER,
            away_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (home_team_id) REFERENCES teams(id),
            FOREIGN KEY (away_team_id) REFERENCES teams(id)
        )
    """)
    cursor.execute("CREATE INDEX idx_game_id ON games(game_id)")
    cursor.execute("CREATE INDEX idx_season_week ON games(season, week)")
    print("✅ Created games table with indexes")
    
    # Drives table - Drive-level data
    cursor.execute("""
        CREATE TABLE drives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drive_id INTEGER UNIQUE NOT NULL,
            game_id INTEGER NOT NULL,
            offense_team_id INTEGER NOT NULL,
            defense_team_id INTEGER NOT NULL,
            drive_number INTEGER,
            scoring BOOLEAN DEFAULT 0,
            start_period INTEGER,
            start_yardline INTEGER,
            start_yards_to_goal INTEGER,
            start_minutes INTEGER,
            start_seconds INTEGER,
            end_period INTEGER,
            end_yardline INTEGER,
            end_yards_to_goal INTEGER,
            end_minutes INTEGER,
            end_seconds INTEGER,
            elapsed_minutes INTEGER,
            elapsed_seconds INTEGER,
            plays INTEGER,
            yards INTEGER,
            drive_result TEXT,
            is_home_offense BOOLEAN,
            start_offense_score INTEGER,
            start_defense_score INTEGER,
            end_offense_score INTEGER,
            end_defense_score INTEGER,
            offense_conference TEXT,
            defense_conference TEXT,
            FOREIGN KEY (game_id) REFERENCES games(game_id),
            FOREIGN KEY (offense_team_id) REFERENCES teams(id),
            FOREIGN KEY (defense_team_id) REFERENCES teams(id)
        )
    """)
    cursor.execute("CREATE INDEX idx_drive_game ON drives(game_id)")
    cursor.execute("CREATE INDEX idx_drive_offense ON drives(offense_team_id)")
    cursor.execute("CREATE INDEX idx_drive_defense ON drives(defense_team_id)")
    cursor.execute("CREATE INDEX idx_drive_result ON drives(drive_result)")
    print("✅ Created drives table with indexes")
    
    # Plays table - Individual play data
    cursor.execute("""
        CREATE TABLE plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            play_id INTEGER UNIQUE NOT NULL,
            drive_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            play_number INTEGER,
            period INTEGER,
            clock_minutes INTEGER,
            clock_seconds INTEGER,
            offense TEXT,
            offense_conference TEXT,
            offense_score INTEGER,
            defense TEXT,
            defense_conference TEXT,
            defense_score INTEGER,
            home TEXT,
            away TEXT,
            offense_timeouts INTEGER,
            defense_timeouts INTEGER,
            yardline INTEGER,
            yards_to_goal INTEGER,
            down INTEGER,
            distance INTEGER,
            yards_gained INTEGER,
            scoring BOOLEAN DEFAULT 0,
            play_type TEXT,
            play_text TEXT,
            ppa REAL,
            wallclock TEXT,
            FOREIGN KEY (drive_id) REFERENCES drives(drive_id),
            FOREIGN KEY (game_id) REFERENCES games(game_id)
        )
    """)
    cursor.execute("CREATE INDEX idx_play_drive ON plays(drive_id)")
    cursor.execute("CREATE INDEX idx_play_game ON plays(game_id)")
    cursor.execute("CREATE INDEX idx_play_type ON plays(play_type)")
    cursor.execute("CREATE INDEX idx_play_down ON plays(down)")
    print("✅ Created plays table with indexes")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database created successfully: {DB_PATH}")
    print(f"📊 Tables: teams, games, drives, plays")
    print(f"🔗 All foreign keys and indexes configured")
    
    return DB_PATH

if __name__ == "__main__":
    create_database()
