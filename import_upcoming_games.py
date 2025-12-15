#!/usr/bin/env python3
"""
Import Upcoming Games to Predictions Database
Imports all remaining 2025 games with comprehensive data
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = 'instance/predictions.db'
JSON_PATH = 'weekly_updates/week_15/remaining_games_complete_2025.json'

def create_table(conn):
    """Create upcoming_games table with all fields"""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS upcoming_games (
            -- Basic Game Info
            id INTEGER PRIMARY KEY,
            season INTEGER,
            week INTEGER,
            season_type TEXT,
            start_date TEXT,
            start_time_tbd BOOLEAN,
            completed BOOLEAN,
            neutral_site BOOLEAN,
            conference_game BOOLEAN,
            attendance INTEGER,
            venue_id INTEGER,
            venue TEXT,
            
            -- Home Team Basic
            home_id INTEGER,
            home_team TEXT,
            home_classification TEXT,
            home_conference TEXT,
            home_points INTEGER,
            
            -- Away Team Basic
            away_id INTEGER,
            away_team TEXT,
            away_classification TEXT,
            away_conference TEXT,
            away_points INTEGER,
            
            -- Records
            home_wins INTEGER,
            home_losses INTEGER,
            home_ties INTEGER,
            home_record TEXT,
            away_wins INTEGER,
            away_losses INTEGER,
            away_ties INTEGER,
            away_record TEXT,
            
            -- Rankings
            home_rank INTEGER,
            away_rank INTEGER,
            
            -- Betting Lines
            line_provider TEXT,
            spread REAL,
            formatted_spread TEXT,
            spread_open REAL,
            over_under REAL,
            over_under_open REAL,
            home_moneyline INTEGER,
            away_moneyline INTEGER,
            
            -- Team Info
            home_logo TEXT,
            home_color TEXT,
            home_alt_color TEXT,
            home_abbreviation TEXT,
            away_logo TEXT,
            away_color TEXT,
            away_alt_color TEXT,
            away_abbreviation TEXT,
            
            -- Season Stats - Home
            home_ppg_offense REAL,
            home_ppg_defense REAL,
            home_ypg_offense REAL,
            home_ypg_defense REAL,
            home_third_down_pct REAL,
            home_turnovers INTEGER,
            home_turnovers_forced INTEGER,
            home_turnover_margin INTEGER,
            home_sacks INTEGER,
            home_sacks_allowed INTEGER,
            
            -- Season Stats - Away
            away_ppg_offense REAL,
            away_ppg_defense REAL,
            away_ypg_offense REAL,
            away_ypg_defense REAL,
            away_third_down_pct REAL,
            away_turnovers INTEGER,
            away_turnovers_forced INTEGER,
            away_turnover_margin INTEGER,
            away_sacks INTEGER,
            away_sacks_allowed INTEGER,
            
            -- Leaders - Home
            home_qb_name TEXT,
            home_qb_stat REAL,
            home_qb_category TEXT,
            home_rb_name TEXT,
            home_rb_stat REAL,
            home_rb_category TEXT,
            home_wr_name TEXT,
            home_wr_stat REAL,
            home_wr_category TEXT,
            home_def_name TEXT,
            home_def_stat REAL,
            home_def_category TEXT,
            
            -- Leaders - Away
            away_qb_name TEXT,
            away_qb_stat REAL,
            away_qb_category TEXT,
            away_rb_name TEXT,
            away_rb_stat REAL,
            away_rb_category TEXT,
            away_wr_name TEXT,
            away_wr_stat REAL,
            away_wr_category TEXT,
            away_def_name TEXT,
            away_def_stat REAL,
            away_def_category TEXT,
            
            -- FPI Data - Home
            home_fpi REAL,
            home_fpi_rank INTEGER,
            home_sos_rank INTEGER,
            home_sor_rank INTEGER,
            home_efficiency_overall REAL,
            home_efficiency_offense REAL,
            home_efficiency_defense REAL,
            
            -- FPI Data - Away
            away_fpi REAL,
            away_fpi_rank INTEGER,
            away_sos_rank INTEGER,
            away_sor_rank INTEGER,
            away_efficiency_overall REAL,
            away_efficiency_offense REAL,
            away_efficiency_defense REAL,
            
            -- Weather
            temperature REAL,
            wind_speed REAL,
            wind_direction TEXT,
            weather_condition TEXT,
            weather_note TEXT,
            
            -- Metadata
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ Created upcoming_games table")

def import_games(conn, json_path):
    """Import games from JSON"""
    cursor = conn.cursor()
    
    with open(json_path) as f:
        games = json.load(f)
    
    print(f"Importing {len(games)} games...")
    
    imported = 0
    for game in games:
        try:
            # Extract betting lines
            lines = game.get('lines', [{}])[0] if game.get('lines') else {}
            
            # Extract home team info
            home_info = game.get('homeTeamInfo', {})
            home_record = game.get('homeRecord', {})
            home_stats = game.get('homeSeasonStats', {})
            home_leaders = game.get('homeLeaders', {})
            home_fpi = game.get('homeFPI', {})
            
            # Extract away team info
            away_info = game.get('awayTeamInfo', {})
            away_record = game.get('awayRecord', {})
            away_stats = game.get('awaySeasonStats', {})
            away_leaders = game.get('awayLeaders', {})
            away_fpi = game.get('awayFPI', {})
            
            # Extract weather
            weather = game.get('weather', {})
            
            # Extract leaders
            home_qb = home_leaders.get('qb') or {}
            home_rb = home_leaders.get('rb') or {}
            home_wr = home_leaders.get('wr') or {}
            home_def = home_leaders.get('def') or {}
            
            away_qb = away_leaders.get('qb') or {}
            away_rb = away_leaders.get('rb') or {}
            away_wr = away_leaders.get('wr') or {}
            away_def = away_leaders.get('def') or {}
            
            cursor.execute("""
                INSERT OR REPLACE INTO upcoming_games (
                    id, season, week, season_type, start_date, start_time_tbd, completed, neutral_site,
                    conference_game, attendance, venue_id, venue,
                    home_id, home_team, home_classification, home_conference, home_points,
                    away_id, away_team, away_classification, away_conference, away_points,
                    home_wins, home_losses, home_ties, home_record,
                    away_wins, away_losses, away_ties, away_record,
                    home_rank, away_rank,
                    line_provider, spread, formatted_spread, spread_open, over_under, over_under_open,
                    home_moneyline, away_moneyline,
                    home_logo, home_color, home_alt_color, home_abbreviation,
                    away_logo, away_color, away_alt_color, away_abbreviation,
                    home_ppg_offense, home_ppg_defense, home_ypg_offense, home_ypg_defense, home_third_down_pct,
                    home_turnovers, home_turnovers_forced, home_turnover_margin, home_sacks, home_sacks_allowed,
                    away_ppg_offense, away_ppg_defense, away_ypg_offense, away_ypg_defense, away_third_down_pct,
                    away_turnovers, away_turnovers_forced, away_turnover_margin, away_sacks, away_sacks_allowed,
                    home_qb_name, home_qb_stat, home_qb_category, home_rb_name, home_rb_stat, home_rb_category,
                    home_wr_name, home_wr_stat, home_wr_category, home_def_name, home_def_stat, home_def_category,
                    away_qb_name, away_qb_stat, away_qb_category, away_rb_name, away_rb_stat, away_rb_category,
                    away_wr_name, away_wr_stat, away_wr_category, away_def_name, away_def_stat, away_def_category,
                    home_fpi, home_fpi_rank, home_sos_rank, home_sor_rank, home_efficiency_overall,
                    home_efficiency_offense, home_efficiency_defense,
                    away_fpi, away_fpi_rank, away_sos_rank, away_sor_rank, away_efficiency_overall,
                    away_efficiency_offense, away_efficiency_defense,
                    temperature, wind_speed, wind_direction, weather_condition, weather_note
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?, ?
                )
            """, (
                # Basic Game Info
                game.get('id'),
                game.get('season'),
                game.get('week'),
                game.get('seasonType'),
                game.get('startDate'),
                game.get('startTimeTBD'),
                game.get('completed'),
                game.get('neutralSite'),
                game.get('conferenceGame'),
                game.get('attendance'),
                game.get('venueId'),
                game.get('venue'),
                
                # Home Team Basic
                game.get('homeId'),
                game.get('homeTeam'),
                game.get('homeClassification'),
                game.get('homeConference'),
                game.get('homePoints'),
                
                # Away Team Basic
                game.get('awayId'),
                game.get('awayTeam'),
                game.get('awayClassification'),
                game.get('awayConference'),
                game.get('awayPoints'),
                
                # Records
                home_record.get('wins'),
                home_record.get('losses'),
                home_record.get('ties'),
                home_record.get('record'),
                away_record.get('wins'),
                away_record.get('losses'),
                away_record.get('ties'),
                away_record.get('record'),
                
                # Rankings
                game.get('homeRank'),
                game.get('awayRank'),
                
                # Betting Lines
                lines.get('provider'),
                lines.get('spread'),
                lines.get('formattedSpread'),
                lines.get('spreadOpen'),
                lines.get('overUnder'),
                lines.get('overUnderOpen'),
                lines.get('homeMoneyline'),
                lines.get('awayMoneyline'),
                
                # Team Info
                home_info.get('logo'),
                home_info.get('color'),
                home_info.get('alt_color'),
                home_info.get('abbreviation'),
                away_info.get('logo'),
                away_info.get('color'),
                away_info.get('alt_color'),
                away_info.get('abbreviation'),
                
                # Season Stats - Home
                home_stats.get('ppg_offense'),
                home_stats.get('ppg_defense'),
                home_stats.get('ypg_offense'),
                home_stats.get('ypg_defense'),
                home_stats.get('third_down_pct'),
                home_stats.get('turnovers'),
                home_stats.get('turnovers_forced'),
                home_stats.get('turnover_margin'),
                home_stats.get('sacks'),
                home_stats.get('sacks_allowed'),
                
                # Season Stats - Away
                away_stats.get('ppg_offense'),
                away_stats.get('ppg_defense'),
                away_stats.get('ypg_offense'),
                away_stats.get('ypg_defense'),
                away_stats.get('third_down_pct'),
                away_stats.get('turnovers'),
                away_stats.get('turnovers_forced'),
                away_stats.get('turnover_margin'),
                away_stats.get('sacks'),
                away_stats.get('sacks_allowed'),
                
                # Leaders - Home
                home_qb.get('name'),
                home_qb.get('stat'),
                home_qb.get('category'),
                home_rb.get('name'),
                home_rb.get('stat'),
                home_rb.get('category'),
                home_wr.get('name'),
                home_wr.get('stat'),
                home_wr.get('category'),
                home_def.get('name'),
                home_def.get('stat'),
                home_def.get('category'),
                
                # Leaders - Away
                away_qb.get('name'),
                away_qb.get('stat'),
                away_qb.get('category'),
                away_rb.get('name'),
                away_rb.get('stat'),
                away_rb.get('category'),
                away_wr.get('name'),
                away_wr.get('stat'),
                away_wr.get('category'),
                away_def.get('name'),
                away_def.get('stat'),
                away_def.get('category'),
                
                # FPI Data - Home
                home_fpi.get('fpi'),
                home_fpi.get('fpi_rank'),
                home_fpi.get('sos_rank'),
                home_fpi.get('sor_rank'),
                home_fpi.get('efficiency_overall'),
                home_fpi.get('efficiency_offense'),
                home_fpi.get('efficiency_defense'),
                
                # FPI Data - Away
                away_fpi.get('fpi'),
                away_fpi.get('fpi_rank'),
                away_fpi.get('sos_rank'),
                away_fpi.get('sor_rank'),
                away_fpi.get('efficiency_overall'),
                away_fpi.get('efficiency_offense'),
                away_fpi.get('efficiency_defense'),
                
                # Weather
                weather.get('temperature'),
                weather.get('wind_speed'),
                weather.get('wind_direction'),
                weather.get('weather_condition'),
                weather.get('note')
            ))
            
            imported += 1
            
        except Exception as e:
            print(f"❌ Error importing game {game.get('id')}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Successfully imported {imported} games")

def verify(conn):
    """Verify the import"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM upcoming_games")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total games in database: {count}")
    
    cursor.execute("""
        SELECT 
            away_team, away_record, home_team, home_record,
            spread, over_under, home_fpi, away_fpi
        FROM upcoming_games 
        ORDER BY week, start_date
        LIMIT 5
    """)
    
    print("\n🏈 First 5 Upcoming Games:")
    for row in cursor.fetchall():
        print(f"  {row[0]} ({row[1]}) @ {row[2]} ({row[3]})")
        print(f"    Spread: {row[4]}, O/U: {row[5]}, FPI: {row[7]} vs {row[6]}")

def main():
    print("=" * 60)
    print("Import Upcoming Games to Predictions Database")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create table
        create_table(conn)
        
        # Import data
        import_games(conn, JSON_PATH)
        
        # Verify
        verify(conn)
        
        print("\n✅ Import completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
