"""
🏗️ COACH DATABASE FACTORY - Master Database Setup
==================================================
Creates the universal coaches_master.db with the complete 11-table schema
that can hold all 134 FBS coaches.

Schema mirrors the validated Campbell prototype:
- coaches: Core metadata + headshots
- stints: Coaching history by school
- games: Game-by-game results with advanced metrics
- rankings: AP Poll history
- draft_picks: NFL talent produced
- situational_stats: Home/away, blowouts, vs ranked
- vs_coaches: Head-to-head records
- season_analytics: Offensive/defensive/advanced metrics
- recruiting_classes: 247Sports class rankings
- talent_composite: Team talent ratings
- transfer_portal: Portal activity

Usage:
    python setup_master_db.py
"""

import sqlite3
from pathlib import Path

def create_master_database():
    """Create the universal coaches database with complete schema"""
    
    db_path = Path('instance/coaches_master.db')
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing database for clean slate
    if db_path.exists():
        print(f"⚠️  Removing existing {db_path}")
        db_path.unlink()
    
    print(f"🏗️  Creating {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # TABLE 1: COACHES - Core metadata
    cursor.execute("""
        CREATE TABLE coaches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            current_school VARCHAR(100) NOT NULL,
            headshot_url TEXT,
            career_record VARCHAR(20) NOT NULL,
            career_win_pct FLOAT NOT NULL,
            total_games INTEGER NOT NULL,
            espn_id TEXT,
            cfbd_id INTEGER,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Table created: coaches")
    
    # TABLE 2: STINTS - Coaching history
    cursor.execute("""
        CREATE TABLE stints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            start_year INTEGER NOT NULL,
            end_year INTEGER NOT NULL,
            record VARCHAR(20) NOT NULL,
            win_pct FLOAT,
            games_coached INTEGER,
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: stints")
    
    # TABLE 3: GAMES - Full game history with metrics
    cursor.execute("""
        CREATE TABLE games (
            id INTEGER PRIMARY KEY,
            coach_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            season_type VARCHAR(20),
            school VARCHAR(100) NOT NULL,
            opponent VARCHAR(100) NOT NULL,
            opponent_logo TEXT,
            result VARCHAR(1) NOT NULL,
            coach_score INTEGER NOT NULL,
            opponent_score INTEGER NOT NULL,
            opponent_sp_overall FLOAT,
            opponent_sp_offense FLOAT,
            opponent_sp_defense FLOAT,
            opponent_fpi FLOAT,
            opponent_srs FLOAT,
            excitement_index FLOAT,
            is_home BOOLEAN NOT NULL DEFAULT 0,
            is_neutral BOOLEAN NOT NULL DEFAULT 0,
            is_conference BOOLEAN NOT NULL DEFAULT 0,
            is_signature BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: games")
    
    # TABLE 4: RANKINGS - AP Poll history
    cursor.execute("""
        CREATE TABLE rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: rankings")
    
    # TABLE 5: DRAFT PICKS - NFL talent
    cursor.execute("""
        CREATE TABLE draft_picks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            player_name VARCHAR(100) NOT NULL,
            year INTEGER NOT NULL,
            round INTEGER NOT NULL,
            pick INTEGER,
            nfl_team VARCHAR(100) NOT NULL,
            college_school VARCHAR(100),
            position VARCHAR(10),
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: draft_picks")
    
    # TABLE 6: SITUATIONAL STATS - Context performance
    cursor.execute("""
        CREATE TABLE situational_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            stint_id INTEGER,
            school VARCHAR(100),
            
            -- vs Ranked Performance
            vs_ranked_record VARCHAR(10),
            vs_top_10_record VARCHAR(10),
            vs_top_25_record VARCHAR(10),
            
            -- Home/Away/Neutral
            home_record VARCHAR(10),
            away_record VARCHAR(10),
            neutral_record VARCHAR(10),
            
            -- Margin Performance
            blowout_wins INTEGER DEFAULT 0,
            blowout_losses INTEGER DEFAULT 0,
            one_score_wins INTEGER DEFAULT 0,
            one_score_losses INTEGER DEFAULT 0,
            comeback_wins INTEGER DEFAULT 0,
            
            -- Conference Performance
            conference_record VARCHAR(10),
            conference_championship_appearances INTEGER DEFAULT 0,
            bowl_record VARCHAR(10),
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE,
            FOREIGN KEY(stint_id) REFERENCES stints(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: situational_stats")
    
    # TABLE 7: VS COACHES - Head-to-head records
    cursor.execute("""
        CREATE TABLE vs_coaches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            opponent_coach VARCHAR(100) NOT NULL,
            opponent_school VARCHAR(100),
            
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            record VARCHAR(10),
            
            avg_point_differential FLOAT,
            biggest_win_margin INTEGER,
            biggest_loss_margin INTEGER,
            
            first_meeting_year INTEGER,
            last_meeting_year INTEGER,
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: vs_coaches")
    
    # TABLE 8: SEASON ANALYTICS - Offensive/Defensive metrics
    cursor.execute("""
        CREATE TABLE season_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            
            -- Offensive Stats
            points_per_game FLOAT,
            yards_per_game FLOAT,
            yards_per_play FLOAT,
            passing_yards_pg FLOAT,
            rushing_yards_pg FLOAT,
            third_down_pct FLOAT,
            fourth_down_pct FLOAT,
            red_zone_pct FLOAT,
            
            -- Defensive Stats
            points_allowed_pg FLOAT,
            yards_allowed_pg FLOAT,
            yards_per_play_allowed FLOAT,
            passing_yards_allowed_pg FLOAT,
            rushing_yards_allowed_pg FLOAT,
            sacks_per_game FLOAT,
            tackles_for_loss_pg FLOAT,
            turnovers_gained_pg FLOAT,
            
            -- Advanced Metrics
            sp_overall FLOAT,
            sp_offense FLOAT,
            sp_defense FLOAT,
            fpi FLOAT,
            srs FLOAT,
            elo_rating FLOAT,
            
            -- Game Control
            avg_time_of_possession FLOAT,
            pace_plays_per_game FLOAT,
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: season_analytics")
    
    # TABLE 9: RECRUITING CLASSES - 247Sports data
    cursor.execute("""
        CREATE TABLE recruiting_classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            year INTEGER NOT NULL,
            
            -- Class Rankings (247 Composite)
            class_rank INTEGER,
            total_commits INTEGER,
            avg_rating FLOAT,
            total_rating FLOAT,
            
            -- Position Breakdown
            five_stars INTEGER DEFAULT 0,
            four_stars INTEGER DEFAULT 0,
            three_stars INTEGER DEFAULT 0,
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: recruiting_classes")
    
    # TABLE 10: TALENT COMPOSITE - Team talent ratings
    cursor.execute("""
        CREATE TABLE talent_composite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            year INTEGER NOT NULL,
            
            talent_rating FLOAT,
            talent_rank INTEGER,
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: talent_composite")
    
    # TABLE 11: TRANSFER PORTAL - Portal activity
    cursor.execute("""
        CREATE TABLE transfer_portal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            school VARCHAR(100) NOT NULL,
            season INTEGER NOT NULL,
            
            transfers_in INTEGER DEFAULT 0,
            transfers_out INTEGER DEFAULT 0,
            net_transfers INTEGER DEFAULT 0,
            
            avg_rating_in FLOAT,
            avg_rating_out FLOAT,
            
            FOREIGN KEY(coach_id) REFERENCES coaches(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table created: transfer_portal")
    
    # Create indexes for performance
    indexes = [
        "CREATE INDEX idx_games_coach_season ON games(coach_id, season)",
        "CREATE INDEX idx_games_opponent ON games(opponent)",
        "CREATE INDEX idx_stints_coach ON stints(coach_id)",
        "CREATE INDEX idx_rankings_coach_season ON rankings(coach_id, season)",
        "CREATE INDEX idx_recruiting_coach_year ON recruiting_classes(coach_id, year)",
        "CREATE INDEX idx_talent_coach_year ON talent_composite(coach_id, year)",
        "CREATE INDEX idx_portal_coach_season ON transfer_portal(coach_id, season)",
    ]
    
    for idx_sql in indexes:
        cursor.execute(idx_sql)
    
    print("✅ Performance indexes created")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ MASTER DATABASE CREATED SUCCESSFULLY!")
    print(f"📁 Location: {db_path.absolute()}")
    print(f"📊 Tables: 11")
    print(f"🎯 Ready for: 134 FBS coaches")
    print("=" * 80)

if __name__ == "__main__":
    create_master_database()
