#!/usr/bin/env python3
"""
Phase 1: Create Database Schema for Full Migration
Creates all new tables needed to replace JSON files
"""

import sqlite3
import os
from datetime import datetime

# SAFE APPROACH: Create separate predictions database
DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'

def create_schema():
    """Create all new tables for migration"""
    
    print("🏗️  Phase 1: Creating Predictions Database Schema...")
    print(f"📊 NEW Database: {DB_PATH}")
    print(f"🔒 SAFE Database: {MASTER_DB_PATH} (untouched)")
    print("\n⚡ Strategy: Build separate predictions.db, merge after validation")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Drives Complete (replaces power5_drives_only.json)
    print("Creating drives_complete table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drives_complete (
            id TEXT PRIMARY KEY,
            game_id INTEGER NOT NULL,
            team_id INTEGER,
            offense TEXT NOT NULL,
            offense_conference TEXT,
            defense TEXT NOT NULL,
            defense_conference TEXT,
            drive_number INTEGER,
            season INTEGER NOT NULL,
            week INTEGER,
            
            -- Scoring
            scoring BOOLEAN DEFAULT 0,
            drive_result TEXT,
            
            -- Field Position
            start_period INTEGER,
            start_yardline INTEGER,
            start_yards_to_goal INTEGER,
            end_period INTEGER,
            end_yardline INTEGER,
            end_yards_to_goal INTEGER,
            
            -- Timing
            start_time_minutes INTEGER,
            start_time_seconds INTEGER,
            end_time_minutes INTEGER,
            end_time_seconds INTEGER,
            elapsed_minutes INTEGER,
            elapsed_seconds INTEGER,
            
            -- Game Context
            is_home_offense BOOLEAN,
            start_offense_score INTEGER,
            start_defense_score INTEGER,
            end_offense_score INTEGER,
            end_defense_score INTEGER,
            
            -- Drive Stats
            plays_count INTEGER,
            yards INTEGER,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_drives_complete_team_season ON drives_complete(team_id, season)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_drives_complete_offense ON drives_complete(offense, season)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_drives_complete_scoring ON drives_complete(scoring)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_drives_complete_game ON drives_complete(game_id)")
    
    # 2. Team EPA Metrics (replaces fbs_teams_stats_only.json EPA data)
    print("Creating team_epa_metrics table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_epa_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            team_name TEXT NOT NULL,
            season INTEGER NOT NULL,
            conference TEXT,
            
            -- Overall Metrics
            overall_ppa REAL,
            overall_success_rate REAL,
            overall_explosiveness REAL,
            overall_power_success REAL,
            overall_stuff_rate REAL,
            
            -- Offensive EPA
            off_plays INTEGER,
            off_drives INTEGER,
            off_ppa REAL,
            off_total_ppa REAL,
            off_success_rate REAL,
            off_explosiveness REAL,
            off_power_success REAL,
            off_stuff_rate REAL,
            
            -- Defensive EPA
            def_plays INTEGER,
            def_drives INTEGER,
            def_ppa REAL,
            def_total_ppa REAL,
            def_success_rate REAL,
            def_explosiveness REAL,
            def_power_success REAL,
            def_stuff_rate REAL,
            
            -- Standard Downs
            off_std_rate REAL,
            off_std_ppa REAL,
            off_std_success_rate REAL,
            off_std_explosiveness REAL,
            def_std_rate REAL,
            def_std_ppa REAL,
            def_std_success_rate REAL,
            def_std_explosiveness REAL,
            
            -- Passing Downs
            off_pass_down_rate REAL,
            off_pass_down_ppa REAL,
            off_pass_down_success_rate REAL,
            off_pass_down_explosiveness REAL,
            def_pass_down_rate REAL,
            def_pass_down_ppa REAL,
            def_pass_down_success_rate REAL,
            def_pass_down_explosiveness REAL,
            
            -- Rush vs Pass
            off_rush_rate REAL,
            off_rush_ppa REAL,
            off_rush_success_rate REAL,
            off_rush_explosiveness REAL,
            def_rush_rate REAL,
            def_rush_ppa REAL,
            def_rush_success_rate REAL,
            def_rush_explosiveness REAL,
            
            off_pass_rate REAL,
            off_pass_ppa REAL,
            off_pass_success_rate REAL,
            off_pass_explosiveness REAL,
            def_pass_rate REAL,
            def_pass_ppa REAL,
            def_pass_success_rate REAL,
            def_pass_explosiveness REAL,
            
            -- Field Position
            off_field_pos_avg_start REAL,
            off_field_pos_avg_predicted_points REAL,
            def_field_pos_avg_start REAL,
            def_field_pos_avg_predicted_points REAL,
            
            -- Havoc
            off_havoc_total REAL,
            off_havoc_front_seven REAL,
            off_havoc_db REAL,
            def_havoc_total REAL,
            def_havoc_front_seven REAL,
            def_havoc_db REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_epa_team_season ON team_epa_metrics(team_id, season)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_epa_team_name ON team_epa_metrics(team_name, season)")
    
    # 3. Player Efficiency (replaces comprehensive_*_analysis.json files)
    print("Creating player_efficiency table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_efficiency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            team_name TEXT NOT NULL,
            player_name TEXT NOT NULL,
            position TEXT NOT NULL,
            season INTEGER NOT NULL,
            
            -- Core Efficiency Metrics
            efficiency_1 REAL,
            sigma_1 REAL,
            efficiency_2 REAL,
            sigma_2 REAL,
            weight_2025 REAL,
            
            -- Performance Stats
            games_played INTEGER,
            total_plays INTEGER,
            success_rate REAL,
            
            -- Ranking
            position_rank INTEGER,
            overall_rank INTEGER,
            conference_rank INTEGER,
            
            -- Position-Specific JSON (flexible storage)
            position_stats TEXT,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_eff_team_pos ON player_efficiency(team_id, position, season)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_eff_name ON player_efficiency(player_name)")
    
    # 4. Win Probability Models (replaces complete_win_probabilities.json)
    print("Creating win_probability_curves table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS win_probability_curves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            team_name TEXT NOT NULL,
            season INTEGER NOT NULL,
            
            -- Base probability
            baseline_win_prob REAL,
            
            -- Score differential probabilities
            prob_down_21_plus REAL,
            prob_down_14_to_20 REAL,
            prob_down_10_to_13 REAL,
            prob_down_7_to_9 REAL,
            prob_down_4_to_6 REAL,
            prob_down_1_to_3 REAL,
            prob_tied REAL,
            prob_up_1_to_3 REAL,
            prob_up_4_to_6 REAL,
            prob_up_7_to_9 REAL,
            prob_up_10_to_13 REAL,
            prob_up_14_to_20 REAL,
            prob_up_21_plus REAL,
            
            -- Context modifiers
            home_advantage_factor REAL,
            underdog_factor REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season)
        )
    """)
    
    # 5. Conferences (replaces react_fbs_conferences.json)
    print("Creating conferences table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            abbreviation TEXT,
            division TEXT,
            classification TEXT,
            
            -- Conference Stats
            total_teams INTEGER DEFAULT 0,
            avg_sp_rating REAL,
            avg_fpi REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 6. Team Offensive Stats Detail (enhance existing team_seasons)
    print("Creating team_offensive_stats table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_offensive_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            
            -- Basic Stats
            first_downs INTEGER,
            third_down_conversions INTEGER,
            third_downs INTEGER,
            third_down_pct REAL,
            fourth_down_conversions INTEGER,
            fourth_downs INTEGER,
            fourth_down_pct REAL,
            
            -- Yardage
            total_yards INTEGER,
            yards_per_game REAL,
            yards_per_play REAL,
            passing_yards INTEGER,
            passing_yards_per_game REAL,
            rushing_yards INTEGER,
            rushing_yards_per_game REAL,
            
            -- Scoring
            points INTEGER,
            points_per_game REAL,
            touchdowns INTEGER,
            field_goals_made INTEGER,
            field_goals_attempted INTEGER,
            
            -- Turnovers
            fumbles_lost INTEGER,
            interceptions_thrown INTEGER,
            turnovers INTEGER,
            turnover_margin INTEGER,
            
            -- Red Zone
            red_zone_attempts INTEGER,
            red_zone_conversions INTEGER,
            red_zone_pct REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season)
        )
    """)
    
    # 7. Team Defensive Stats Detail
    print("Creating team_defensive_stats table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_defensive_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            
            -- Basic Stats
            first_downs_allowed INTEGER,
            third_down_conversions_allowed INTEGER,
            third_downs_allowed INTEGER,
            third_down_pct_allowed REAL,
            fourth_down_conversions_allowed INTEGER,
            fourth_downs_allowed INTEGER,
            fourth_down_pct_allowed REAL,
            
            -- Yardage
            total_yards_allowed INTEGER,
            yards_per_game_allowed REAL,
            yards_per_play_allowed REAL,
            passing_yards_allowed INTEGER,
            passing_yards_per_game_allowed REAL,
            rushing_yards_allowed INTEGER,
            rushing_yards_per_game_allowed REAL,
            
            -- Scoring
            points_allowed INTEGER,
            points_per_game_allowed REAL,
            touchdowns_allowed INTEGER,
            
            -- Turnovers Created
            fumbles_recovered INTEGER,
            interceptions INTEGER,
            turnovers_gained INTEGER,
            
            -- Pressure
            sacks REAL,
            tackles_for_loss REAL,
            
            -- Red Zone
            red_zone_attempts_allowed INTEGER,
            red_zone_conversions_allowed INTEGER,
            red_zone_pct_allowed REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season)
        )
    """)
    
    # 8. Team Summary Stats (replaces team_season_summaries_clean.json)
    print("Creating team_season_summaries table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_season_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            team_name TEXT NOT NULL,
            season INTEGER NOT NULL,
            
            -- Record
            wins INTEGER,
            losses INTEGER,
            win_pct REAL,
            
            -- Rankings Summary
            final_ap_rank INTEGER,
            final_cfp_rank INTEGER,
            highest_rank INTEGER,
            weeks_ranked INTEGER,
            
            -- Performance Summary
            avg_margin_of_victory REAL,
            avg_margin_of_defeat REAL,
            largest_win_margin INTEGER,
            largest_loss_margin INTEGER,
            
            -- Notable Games
            wins_vs_ranked INTEGER,
            losses_vs_ranked INTEGER,
            wins_vs_top_10 INTEGER,
            losses_vs_top_10 INTEGER,
            
            -- Bowl/Playoff
            bowl_game TEXT,
            bowl_result TEXT,
            playoff_appearance BOOLEAN DEFAULT 0,
            national_championship BOOLEAN DEFAULT 0,
            
            -- Season Narrative (text summary)
            season_summary TEXT,
            key_wins TEXT,
            key_losses TEXT,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season)
        )
    """)
    
    # 9. Coach Rankings (consolidate multiple coach JSON files)
    print("Creating coach_rankings table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coach_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            
            -- Overall Rankings
            overall_rank INTEGER,
            win_pct_rank INTEGER,
            total_wins_rank INTEGER,
            
            -- Current Season
            current_season_rank INTEGER,
            current_season_record TEXT,
            current_season_wins INTEGER,
            current_season_losses INTEGER,
            
            -- vs Ranked
            vs_ranked_record TEXT,
            vs_ranked_win_pct REAL,
            vs_top_10_record TEXT,
            vs_top_25_record TEXT,
            
            -- Advanced Scores
            data_driven_score REAL,
            talent_context_score REAL,
            big_game_score REAL,
            recruiting_score REAL,
            nfl_development_score REAL,
            betting_performance_score REAL,
            consistency_score REAL,
            
            -- Composite Score
            composite_score REAL,
            composite_rank INTEGER,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(coach_id) REFERENCES coaches(id),
            UNIQUE(coach_id, season)
        )
    """)
    
    # 10. Team Power Rankings (replaces react_fbs_team_rankings.json)
    print("Creating team_power_rankings table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_power_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            team_name TEXT NOT NULL,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            
            -- Poll Rankings
            ap_rank INTEGER,
            coaches_rank INTEGER,
            cfp_rank INTEGER,
            
            -- Computer Rankings
            sp_rank INTEGER,
            fpi_rank INTEGER,
            srs_rank INTEGER,
            elo_rank INTEGER,
            
            -- Composite
            composite_rank INTEGER,
            power_rating REAL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            UNIQUE(team_id, season, week)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_power_rankings_week ON team_power_rankings(season, week)")
    
    conn.commit()
    
    # Verify tables created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n✅ Schema created successfully!")
    print(f"📊 Total tables in database: {len(tables)}")
    print("\nNew tables created:")
    new_tables = [
        'drives_complete', 'team_epa_metrics', 'player_efficiency',
        'win_probability_curves', 'conferences', 'team_offensive_stats',
        'team_defensive_stats', 'team_season_summaries', 'coach_rankings',
        'team_power_rankings'
    ]
    for table in new_tables:
        print(f"  ✓ {table}")
    
    conn.close()
    
    print(f"\n🎯 Phase 1 Complete!")
    print(f"Next: Run 02_migrate_core_data.py")

if __name__ == '__main__':
    print("🛡️  SAFE MODE: Creating separate predictions.db")
    print("=" * 70)
    print("✅ Your coaches_master.db will NOT be touched")
    print("✅ All predictor data goes into predictions.db")
    print("✅ Merge databases later after validation")
    print("=" * 70 + "\n")
    
    # No backup needed - we're creating a NEW database
    if os.path.exists(DB_PATH):
        print(f"⚠️  {DB_PATH} already exists")
        response = input("Delete and recreate? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Aborted")
            exit(1)
        os.remove(DB_PATH)
        print(f"🗑️  Deleted old {DB_PATH}\n")
    
    create_schema()
