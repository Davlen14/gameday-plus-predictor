#!/usr/bin/env python3
"""
Import Comprehensive Power Rankings from JSON to Database
Creates table and imports all detailed offensive and defensive metrics
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = 'instance/predictions.db'
JSON_PATH = 'weekly_updates/week_15/comprehensive_power_rankings_20251203_053934.json'

def create_comprehensive_rankings_table(conn):
    """Create the comprehensive_power_rankings table with all individual columns"""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comprehensive_power_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            conference TEXT,
            season INTEGER NOT NULL,
            week INTEGER NOT NULL,
            
            -- Overall Rankings
            rank INTEGER,
            overall_score REAL,
            offensive_score REAL,
            defensive_score REAL,
            total_metrics_analyzed INTEGER,
            
            -- Offensive Normalized Metrics (40 columns)
            off_norm_avg_starting_field_position REAL,
            off_norm_rushing_success REAL,
            off_norm_completion_pct REAL,
            off_norm_passing_ppa REAL,
            off_norm_open_field_yards REAL,
            off_norm_offense_ppa REAL,
            off_norm_yards_per_game REAL,
            off_norm_yards_per_rush REAL,
            off_norm_passing_downs_success REAL,
            off_norm_power_success REAL,
            off_norm_possession_time_pct REAL,
            off_norm_rushing_ppa REAL,
            off_norm_offense_explosiveness REAL,
            off_norm_offense_havoc_front_seven REAL,
            off_norm_stuff_rate REAL,
            off_norm_rush_td_rate REAL,
            off_norm_fourth_down_pct REAL,
            off_norm_rushing_explosiveness REAL,
            off_norm_passing_explosiveness REAL,
            off_norm_standard_downs_success REAL,
            off_norm_passing_downs_ppa REAL,
            off_norm_first_downs_per_game REAL,
            off_norm_passing_success REAL,
            off_norm_penalty_yards_per_game REAL,
            off_norm_line_yards REAL,
            off_norm_offense_success_rate REAL,
            off_norm_interception_pct REAL,
            off_norm_yards_per_pass REAL,
            off_norm_pass_td_rate REAL,
            off_norm_third_down_pct REAL,
            off_norm_offense_havoc_db REAL,
            off_norm_offense_havoc_total REAL,
            off_norm_avg_predicted_points_start REAL,
            off_norm_second_level_yards REAL,
            off_norm_yards_per_play REAL,
            off_norm_standard_downs_ppa REAL,
            off_norm_points_per_opportunity REAL,
            off_norm_kick_return_avg REAL,
            off_norm_turnover_margin REAL,
            off_norm_punt_return_avg REAL,
            
            -- Defensive Normalized Metrics (40 columns)
            def_norm_second_level_yards REAL,
            def_norm_fourth_down_pct_allowed REAL,
            def_norm_takeaways_per_game REAL,
            def_norm_defense_ppa REAL,
            def_norm_rush_td_allowed_rate REAL,
            def_norm_defense_explosiveness REAL,
            def_norm_pass_td_allowed_rate REAL,
            def_norm_third_down_pct_allowed REAL,
            def_norm_stuff_rate REAL,
            def_norm_kick_return_avg_allowed REAL,
            def_norm_yards_allowed_per_play REAL,
            def_norm_defense_havoc_total REAL,
            def_norm_passing_success REAL,
            def_norm_tackles_for_loss_per_game REAL,
            def_norm_passing_explosiveness REAL,
            def_norm_punt_return_avg_allowed REAL,
            def_norm_sacks_per_game REAL,
            def_norm_power_success REAL,
            def_norm_completion_pct_allowed REAL,
            def_norm_rushing_ppa REAL,
            def_norm_points_per_opportunity REAL,
            def_norm_standard_downs_success REAL,
            def_norm_interceptions_per_game REAL,
            def_norm_open_field_yards REAL,
            def_norm_passing_downs_success REAL,
            def_norm_defense_havoc_front_seven REAL,
            def_norm_standard_downs_ppa REAL,
            def_norm_defense_havoc_db REAL,
            def_norm_rushing_explosiveness REAL,
            def_norm_yards_allowed_per_game REAL,
            def_norm_rushing_success REAL,
            def_norm_yards_per_rush_allowed REAL,
            def_norm_yards_per_pass_allowed REAL,
            def_norm_fumbles_recovered_per_game REAL,
            def_norm_sack_rate REAL,
            def_norm_defense_success_rate REAL,
            def_norm_passing_downs_ppa REAL,
            def_norm_passing_ppa REAL,
            def_norm_opponent_penalty_yards_per_game REAL,
            def_norm_line_yards REAL,
            
            -- Offensive Raw Metrics (40 columns)
            off_raw_yards_per_play REAL,
            off_raw_yards_per_game REAL,
            off_raw_completion_pct REAL,
            off_raw_yards_per_pass REAL,
            off_raw_pass_td_rate REAL,
            off_raw_interception_pct REAL,
            off_raw_yards_per_rush REAL,
            off_raw_rush_td_rate REAL,
            off_raw_third_down_pct REAL,
            off_raw_fourth_down_pct REAL,
            off_raw_first_downs_per_game REAL,
            off_raw_points_per_opportunity REAL,
            off_raw_turnover_margin REAL,
            off_raw_possession_time_pct REAL,
            off_raw_line_yards REAL,
            off_raw_second_level_yards REAL,
            off_raw_open_field_yards REAL,
            off_raw_power_success REAL,
            off_raw_stuff_rate REAL,
            off_raw_offense_ppa REAL,
            off_raw_offense_success_rate REAL,
            off_raw_offense_explosiveness REAL,
            off_raw_standard_downs_ppa REAL,
            off_raw_standard_downs_success REAL,
            off_raw_passing_downs_ppa REAL,
            off_raw_passing_downs_success REAL,
            off_raw_rushing_ppa REAL,
            off_raw_rushing_success REAL,
            off_raw_rushing_explosiveness REAL,
            off_raw_passing_ppa REAL,
            off_raw_passing_success REAL,
            off_raw_passing_explosiveness REAL,
            off_raw_avg_starting_field_position REAL,
            off_raw_avg_predicted_points_start REAL,
            off_raw_offense_havoc_total REAL,
            off_raw_offense_havoc_front_seven REAL,
            off_raw_offense_havoc_db REAL,
            off_raw_kick_return_avg REAL,
            off_raw_punt_return_avg REAL,
            off_raw_penalty_yards_per_game REAL,
            
            -- Defensive Raw Metrics (40 columns)
            def_raw_yards_allowed_per_play REAL,
            def_raw_yards_allowed_per_game REAL,
            def_raw_completion_pct_allowed REAL,
            def_raw_yards_per_pass_allowed REAL,
            def_raw_pass_td_allowed_rate REAL,
            def_raw_yards_per_rush_allowed REAL,
            def_raw_rush_td_allowed_rate REAL,
            def_raw_third_down_pct_allowed REAL,
            def_raw_fourth_down_pct_allowed REAL,
            def_raw_interceptions_per_game REAL,
            def_raw_fumbles_recovered_per_game REAL,
            def_raw_takeaways_per_game REAL,
            def_raw_sacks_per_game REAL,
            def_raw_tackles_for_loss_per_game REAL,
            def_raw_sack_rate REAL,
            def_raw_line_yards REAL,
            def_raw_second_level_yards REAL,
            def_raw_open_field_yards REAL,
            def_raw_power_success REAL,
            def_raw_stuff_rate REAL,
            def_raw_defense_ppa REAL,
            def_raw_defense_success_rate REAL,
            def_raw_defense_explosiveness REAL,
            def_raw_points_per_opportunity REAL,
            def_raw_standard_downs_ppa REAL,
            def_raw_standard_downs_success REAL,
            def_raw_passing_downs_ppa REAL,
            def_raw_passing_downs_success REAL,
            def_raw_rushing_ppa REAL,
            def_raw_rushing_success REAL,
            def_raw_rushing_explosiveness REAL,
            def_raw_passing_ppa REAL,
            def_raw_passing_success REAL,
            def_raw_passing_explosiveness REAL,
            def_raw_defense_havoc_total REAL,
            def_raw_defense_havoc_front_seven REAL,
            def_raw_defense_havoc_db REAL,
            def_raw_kick_return_avg_allowed REAL,
            def_raw_punt_return_avg_allowed REAL,
            def_raw_opponent_penalty_yards_per_game REAL,
            
            -- Metadata
            generated_at TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            UNIQUE(team_name, season, week)
        )
    """)
    
    conn.commit()
    print("✅ Created comprehensive_power_rankings table with 169 individual columns")

def import_rankings_data(conn, json_path):
    """Import data from JSON file"""
    cursor = conn.cursor()
    
    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    rankings = data['rankings']
    
    # Assuming week 15 from directory
    week = 15
    season = 2025
    
    print(f"Importing {len(rankings)} teams for Season {season}, Week {week}")
    
    imported_count = 0
    for team_data in rankings:
        try:
            # Extract detailed metrics
            off_norm = team_data['detailed_metrics']['offensive_normalized']
            def_norm = team_data['detailed_metrics']['defensive_normalized']
            off_raw = team_data['detailed_metrics']['offensive_raw']
            def_raw = team_data['detailed_metrics']['defensive_raw']
            
            cursor.execute("""
                INSERT OR REPLACE INTO comprehensive_power_rankings (
                    team_name, conference, season, week,
                    rank, overall_score, offensive_score, defensive_score, total_metrics_analyzed,
                    
                    -- Offensive Normalized
                    off_norm_avg_starting_field_position, off_norm_rushing_success, off_norm_completion_pct,
                    off_norm_passing_ppa, off_norm_open_field_yards, off_norm_offense_ppa, off_norm_yards_per_game,
                    off_norm_yards_per_rush, off_norm_passing_downs_success, off_norm_power_success,
                    off_norm_possession_time_pct, off_norm_rushing_ppa, off_norm_offense_explosiveness,
                    off_norm_offense_havoc_front_seven, off_norm_stuff_rate, off_norm_rush_td_rate,
                    off_norm_fourth_down_pct, off_norm_rushing_explosiveness, off_norm_passing_explosiveness,
                    off_norm_standard_downs_success, off_norm_passing_downs_ppa, off_norm_first_downs_per_game,
                    off_norm_passing_success, off_norm_penalty_yards_per_game, off_norm_line_yards,
                    off_norm_offense_success_rate, off_norm_interception_pct, off_norm_yards_per_pass,
                    off_norm_pass_td_rate, off_norm_third_down_pct, off_norm_offense_havoc_db,
                    off_norm_offense_havoc_total, off_norm_avg_predicted_points_start, off_norm_second_level_yards,
                    off_norm_yards_per_play, off_norm_standard_downs_ppa, off_norm_points_per_opportunity,
                    off_norm_kick_return_avg, off_norm_turnover_margin, off_norm_punt_return_avg,
                    
                    -- Defensive Normalized
                    def_norm_second_level_yards, def_norm_fourth_down_pct_allowed, def_norm_takeaways_per_game,
                    def_norm_defense_ppa, def_norm_rush_td_allowed_rate, def_norm_defense_explosiveness,
                    def_norm_pass_td_allowed_rate, def_norm_third_down_pct_allowed, def_norm_stuff_rate,
                    def_norm_kick_return_avg_allowed, def_norm_yards_allowed_per_play, def_norm_defense_havoc_total,
                    def_norm_passing_success, def_norm_tackles_for_loss_per_game, def_norm_passing_explosiveness,
                    def_norm_punt_return_avg_allowed, def_norm_sacks_per_game, def_norm_power_success,
                    def_norm_completion_pct_allowed, def_norm_rushing_ppa, def_norm_points_per_opportunity,
                    def_norm_standard_downs_success, def_norm_interceptions_per_game, def_norm_open_field_yards,
                    def_norm_passing_downs_success, def_norm_defense_havoc_front_seven, def_norm_standard_downs_ppa,
                    def_norm_defense_havoc_db, def_norm_rushing_explosiveness, def_norm_yards_allowed_per_game,
                    def_norm_rushing_success, def_norm_yards_per_rush_allowed, def_norm_yards_per_pass_allowed,
                    def_norm_fumbles_recovered_per_game, def_norm_sack_rate, def_norm_defense_success_rate,
                    def_norm_passing_downs_ppa, def_norm_passing_ppa, def_norm_opponent_penalty_yards_per_game,
                    def_norm_line_yards,
                    
                    -- Offensive Raw
                    off_raw_yards_per_play, off_raw_yards_per_game, off_raw_completion_pct, off_raw_yards_per_pass,
                    off_raw_pass_td_rate, off_raw_interception_pct, off_raw_yards_per_rush, off_raw_rush_td_rate,
                    off_raw_third_down_pct, off_raw_fourth_down_pct, off_raw_first_downs_per_game,
                    off_raw_points_per_opportunity, off_raw_turnover_margin, off_raw_possession_time_pct,
                    off_raw_line_yards, off_raw_second_level_yards, off_raw_open_field_yards, off_raw_power_success,
                    off_raw_stuff_rate, off_raw_offense_ppa, off_raw_offense_success_rate, off_raw_offense_explosiveness,
                    off_raw_standard_downs_ppa, off_raw_standard_downs_success, off_raw_passing_downs_ppa,
                    off_raw_passing_downs_success, off_raw_rushing_ppa, off_raw_rushing_success,
                    off_raw_rushing_explosiveness, off_raw_passing_ppa, off_raw_passing_success,
                    off_raw_passing_explosiveness, off_raw_avg_starting_field_position, off_raw_avg_predicted_points_start,
                    off_raw_offense_havoc_total, off_raw_offense_havoc_front_seven, off_raw_offense_havoc_db,
                    off_raw_kick_return_avg, off_raw_punt_return_avg, off_raw_penalty_yards_per_game,
                    
                    -- Defensive Raw
                    def_raw_yards_allowed_per_play, def_raw_yards_allowed_per_game, def_raw_completion_pct_allowed,
                    def_raw_yards_per_pass_allowed, def_raw_pass_td_allowed_rate, def_raw_yards_per_rush_allowed,
                    def_raw_rush_td_allowed_rate, def_raw_third_down_pct_allowed, def_raw_fourth_down_pct_allowed,
                    def_raw_interceptions_per_game, def_raw_fumbles_recovered_per_game, def_raw_takeaways_per_game,
                    def_raw_sacks_per_game, def_raw_tackles_for_loss_per_game, def_raw_sack_rate, def_raw_line_yards,
                    def_raw_second_level_yards, def_raw_open_field_yards, def_raw_power_success, def_raw_stuff_rate,
                    def_raw_defense_ppa, def_raw_defense_success_rate, def_raw_defense_explosiveness,
                    def_raw_points_per_opportunity, def_raw_standard_downs_ppa, def_raw_standard_downs_success,
                    def_raw_passing_downs_ppa, def_raw_passing_downs_success, def_raw_rushing_ppa,
                    def_raw_rushing_success, def_raw_rushing_explosiveness, def_raw_passing_ppa,
                    def_raw_passing_success, def_raw_passing_explosiveness, def_raw_defense_havoc_total,
                    def_raw_defense_havoc_front_seven, def_raw_defense_havoc_db, def_raw_kick_return_avg_allowed,
                    def_raw_punt_return_avg_allowed, def_raw_opponent_penalty_yards_per_game,
                    
                    generated_at
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?
                )
            """, (
                team_data['team'], team_data['conference'], season, week,
                team_data['rank'], team_data['overall_score'], team_data['offensive_score'],
                team_data['defensive_score'], team_data['total_metrics_analyzed'],
                
                # Offensive Normalized (40)
                off_norm.get('avg_starting_field_position'), off_norm.get('rushing_success'),
                off_norm.get('completion_pct'), off_norm.get('passing_ppa'), off_norm.get('open_field_yards'),
                off_norm.get('offense_ppa'), off_norm.get('yards_per_game'), off_norm.get('yards_per_rush'),
                off_norm.get('passing_downs_success'), off_norm.get('power_success'), off_norm.get('possession_time_pct'),
                off_norm.get('rushing_ppa'), off_norm.get('offense_explosiveness'), off_norm.get('offense_havoc_front_seven'),
                off_norm.get('stuff_rate'), off_norm.get('rush_td_rate'), off_norm.get('fourth_down_pct'),
                off_norm.get('rushing_explosiveness'), off_norm.get('passing_explosiveness'), off_norm.get('standard_downs_success'),
                off_norm.get('passing_downs_ppa'), off_norm.get('first_downs_per_game'), off_norm.get('passing_success'),
                off_norm.get('penalty_yards_per_game'), off_norm.get('line_yards'), off_norm.get('offense_success_rate'),
                off_norm.get('interception_pct'), off_norm.get('yards_per_pass'), off_norm.get('pass_td_rate'),
                off_norm.get('third_down_pct'), off_norm.get('offense_havoc_db'), off_norm.get('offense_havoc_total'),
                off_norm.get('avg_predicted_points_start'), off_norm.get('second_level_yards'), off_norm.get('yards_per_play'),
                off_norm.get('standard_downs_ppa'), off_norm.get('points_per_opportunity'), off_norm.get('kick_return_avg'),
                off_norm.get('turnover_margin'), off_norm.get('punt_return_avg'),
                
                # Defensive Normalized (40)
                def_norm.get('def_second_level_yards'), def_norm.get('fourth_down_pct_allowed'),
                def_norm.get('takeaways_per_game'), def_norm.get('defense_ppa'), def_norm.get('rush_td_allowed_rate'),
                def_norm.get('defense_explosiveness'), def_norm.get('pass_td_allowed_rate'), def_norm.get('third_down_pct_allowed'),
                def_norm.get('def_stuff_rate'), def_norm.get('kick_return_avg_allowed'), def_norm.get('yards_allowed_per_play'),
                def_norm.get('defense_havoc_total'), def_norm.get('def_passing_success'), def_norm.get('tackles_for_loss_per_game'),
                def_norm.get('def_passing_explosiveness'), def_norm.get('punt_return_avg_allowed'), def_norm.get('sacks_per_game'),
                def_norm.get('def_power_success'), def_norm.get('completion_pct_allowed'), def_norm.get('def_rushing_ppa'),
                def_norm.get('def_points_per_opportunity'), def_norm.get('def_standard_downs_success'),
                def_norm.get('interceptions_per_game'), def_norm.get('def_open_field_yards'), def_norm.get('def_passing_downs_success'),
                def_norm.get('defense_havoc_front_seven'), def_norm.get('def_standard_downs_ppa'), def_norm.get('defense_havoc_db'),
                def_norm.get('def_rushing_explosiveness'), def_norm.get('yards_allowed_per_game'), def_norm.get('def_rushing_success'),
                def_norm.get('yards_per_rush_allowed'), def_norm.get('yards_per_pass_allowed'), def_norm.get('fumbles_recovered_per_game'),
                def_norm.get('sack_rate'), def_norm.get('defense_success_rate'), def_norm.get('def_passing_downs_ppa'),
                def_norm.get('def_passing_ppa'), def_norm.get('opponent_penalty_yards_per_game'), def_norm.get('def_line_yards'),
                
                # Offensive Raw (40)
                off_raw.get('yards_per_play'), off_raw.get('yards_per_game'), off_raw.get('completion_pct'),
                off_raw.get('yards_per_pass'), off_raw.get('pass_td_rate'), off_raw.get('interception_pct'),
                off_raw.get('yards_per_rush'), off_raw.get('rush_td_rate'), off_raw.get('third_down_pct'),
                off_raw.get('fourth_down_pct'), off_raw.get('first_downs_per_game'), off_raw.get('points_per_opportunity'),
                off_raw.get('turnover_margin'), off_raw.get('possession_time_pct'), off_raw.get('line_yards'),
                off_raw.get('second_level_yards'), off_raw.get('open_field_yards'), off_raw.get('power_success'),
                off_raw.get('stuff_rate'), off_raw.get('offense_ppa'), off_raw.get('offense_success_rate'),
                off_raw.get('offense_explosiveness'), off_raw.get('standard_downs_ppa'), off_raw.get('standard_downs_success'),
                off_raw.get('passing_downs_ppa'), off_raw.get('passing_downs_success'), off_raw.get('rushing_ppa'),
                off_raw.get('rushing_success'), off_raw.get('rushing_explosiveness'), off_raw.get('passing_ppa'),
                off_raw.get('passing_success'), off_raw.get('passing_explosiveness'), off_raw.get('avg_starting_field_position'),
                off_raw.get('avg_predicted_points_start'), off_raw.get('offense_havoc_total'), off_raw.get('offense_havoc_front_seven'),
                off_raw.get('offense_havoc_db'), off_raw.get('kick_return_avg'), off_raw.get('punt_return_avg'),
                off_raw.get('penalty_yards_per_game'),
                
                # Defensive Raw (40)
                def_raw.get('yards_allowed_per_play'), def_raw.get('yards_allowed_per_game'),
                def_raw.get('completion_pct_allowed'), def_raw.get('yards_per_pass_allowed'), def_raw.get('pass_td_allowed_rate'),
                def_raw.get('yards_per_rush_allowed'), def_raw.get('rush_td_allowed_rate'), def_raw.get('third_down_pct_allowed'),
                def_raw.get('fourth_down_pct_allowed'), def_raw.get('interceptions_per_game'), def_raw.get('fumbles_recovered_per_game'),
                def_raw.get('takeaways_per_game'), def_raw.get('sacks_per_game'), def_raw.get('tackles_for_loss_per_game'),
                def_raw.get('sack_rate'), def_raw.get('def_line_yards'), def_raw.get('second_level_yards'),
                def_raw.get('def_open_field_yards'), def_raw.get('def_power_success'), def_raw.get('def_stuff_rate'),
                def_raw.get('defense_ppa'), def_raw.get('defense_success_rate'), def_raw.get('defense_explosiveness'),
                def_raw.get('def_points_per_opportunity'), def_raw.get('def_standard_downs_ppa'),
                def_raw.get('def_standard_downs_success'), def_raw.get('def_passing_downs_ppa'),
                def_raw.get('def_passing_downs_success'), def_raw.get('def_rushing_ppa'), def_raw.get('def_rushing_success'),
                def_raw.get('def_rushing_explosiveness'), def_raw.get('def_passing_ppa'), def_raw.get('def_passing_success'),
                def_raw.get('def_passing_explosiveness'), def_raw.get('defense_havoc_total'), def_raw.get('defense_havoc_front_seven'),
                def_raw.get('defense_havoc_db'), def_raw.get('kick_return_avg_allowed'), def_raw.get('punt_return_avg_allowed'),
                def_raw.get('opponent_penalty_yards_per_game'),
                
                metadata['generated_at']
            ))
            
            imported_count += 1
            
        except Exception as e:
            print(f"❌ Error importing {team_data['team']}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    conn.commit()
    print(f"✅ Successfully imported {imported_count} teams")

def verify_import(conn):
    """Verify the import was successful"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM comprehensive_power_rankings WHERE season = 2025 AND week = 15")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total teams in database: {count}")
    
    cursor.execute("""
        SELECT team_name, rank, overall_score, offensive_score, defensive_score 
        FROM comprehensive_power_rankings 
        WHERE season = 2025 AND week = 15 
        ORDER BY rank 
        LIMIT 5
    """)
    
    print("\n🏆 Top 5 Teams:")
    for row in cursor.fetchall():
        print(f"  #{row[1]} {row[0]}: Overall={row[2]:.2f}, Off={row[3]:.2f}, Def={row[4]:.2f}")

def main():
    print("=" * 60)
    print("Comprehensive Power Rankings Import Tool")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create table
        create_comprehensive_rankings_table(conn)
        
        # Import data
        import_rankings_data(conn, JSON_PATH)
        
        # Verify
        verify_import(conn)
        
        print("\n✅ Import completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
