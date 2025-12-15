#!/usr/bin/env python3
"""
Import all team drives and plays from CSV files into gameday_analytics.db
"""

import sqlite3
import csv
import os
import re
from collections import defaultdict

DB_PATH = 'gameday_analytics.db'
DRIVES_FOLDER = 'drives'

def parse_time_dict(time_str):
    """Parse time dictionary string like "{'minutes': 15, 'seconds': 0}" """
    if not time_str or time_str == '':
        return 0, 0
    try:
        # Extract minutes and seconds using regex
        minutes_match = re.search(r"'minutes':\s*(\d+)", time_str)
        seconds_match = re.search(r"'seconds':\s*(\d+)", time_str)
        
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0
        
        return minutes, seconds
    except:
        return 0, 0

def get_or_create_team(cursor, team_name, conference=None):
    """Get team ID or create if doesn't exist"""
    cursor.execute("SELECT id FROM teams WHERE team_name = ?", (team_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute("""
            INSERT INTO teams (team_name, conference, abbreviation)
            VALUES (?, ?, ?)
        """, (team_name, conference, team_name.replace('_', '').replace(' ', '')[:10]))
        return cursor.lastrowid

def get_or_create_game(cursor, game_id, home_team_id, away_team_id):
    """Get game ID or create if doesn't exist"""
    cursor.execute("SELECT id FROM games WHERE game_id = ?", (game_id,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute("""
            INSERT INTO games (game_id, home_team_id, away_team_id)
            VALUES (?, ?, ?)
        """, (game_id, home_team_id, away_team_id))
        return cursor.lastrowid

def import_drives(conn, csv_path, team_name):
    """Import drives from CSV file"""
    cursor = conn.cursor()
    drives_imported = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Get or create teams
                    offense_team_id = get_or_create_team(cursor, row['offense'], row.get('offenseConference'))
                    defense_team_id = get_or_create_team(cursor, row['defense'], row.get('defenseConference'))
                    
                    # Determine home/away teams
                    is_home_offense = row.get('isHomeOffense', 'False') == 'True'
                    if is_home_offense:
                        home_team_id = offense_team_id
                        away_team_id = defense_team_id
                    else:
                        home_team_id = defense_team_id
                        away_team_id = offense_team_id
                    
                    # Get or create game
                    game_id = int(row['gameId'])
                    get_or_create_game(cursor, game_id, home_team_id, away_team_id)
                    
                    # Parse time fields
                    start_min, start_sec = parse_time_dict(row.get('startTime', ''))
                    end_min, end_sec = parse_time_dict(row.get('endTime', ''))
                    elapsed_min, elapsed_sec = parse_time_dict(row.get('elapsed', ''))
                    
                    # Insert drive
                    cursor.execute("""
                        INSERT OR IGNORE INTO drives (
                            drive_id, game_id, offense_team_id, defense_team_id,
                            drive_number, scoring, start_period, start_yardline, 
                            start_yards_to_goal, start_minutes, start_seconds,
                            end_period, end_yardline, end_yards_to_goal,
                            end_minutes, end_seconds, elapsed_minutes, elapsed_seconds,
                            plays, yards, drive_result, is_home_offense,
                            start_offense_score, start_defense_score,
                            end_offense_score, end_defense_score,
                            offense_conference, defense_conference
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        int(row['id']),
                        game_id,
                        offense_team_id,
                        defense_team_id,
                        int(row.get('driveNumber', 0)),
                        row.get('scoring', 'False') == 'True',
                        int(row.get('startPeriod', 0)),
                        int(row.get('startYardline', 0)),
                        int(row.get('startYardsToGoal', 0)),
                        start_min,
                        start_sec,
                        int(row.get('endPeriod', 0)),
                        int(row.get('endYardline', 0)),
                        int(row.get('endYardsToGoal', 0)),
                        end_min,
                        end_sec,
                        elapsed_min,
                        elapsed_sec,
                        int(row.get('plays', 0)),
                        int(row.get('yards', 0)),
                        row.get('driveResult', ''),
                        is_home_offense,
                        int(row.get('startOffenseScore', 0)),
                        int(row.get('startDefenseScore', 0)),
                        int(row.get('endOffenseScore', 0)),
                        int(row.get('endDefenseScore', 0)),
                        row.get('offenseConference', ''),
                        row.get('defenseConference', '')
                    ))
                    drives_imported += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Error importing drive {row.get('id', 'unknown')}: {str(e)}")
                    continue
        
        conn.commit()
        return drives_imported
        
    except Exception as e:
        print(f"    ❌ Error reading drives file: {str(e)}")
        return 0

def import_plays(conn, csv_path, team_name):
    """Import plays from CSV file"""
    cursor = conn.cursor()
    plays_imported = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Parse time
                    clock_min, clock_sec = parse_time_dict(row.get('clock', ''))
                    
                    # Insert play
                    cursor.execute("""
                        INSERT OR IGNORE INTO plays (
                            play_id, drive_id, game_id, play_number, period,
                            clock_minutes, clock_seconds, offense, offense_conference,
                            offense_score, defense, defense_conference, defense_score,
                            home, away, offense_timeouts, defense_timeouts,
                            yardline, yards_to_goal, down, distance, yards_gained,
                            scoring, play_type, play_text, ppa, wallclock
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        int(row['id']),
                        int(row['driveId']),
                        int(row['gameId']),
                        int(row.get('playNumber', 0)),
                        int(row.get('period', 0)),
                        clock_min,
                        clock_sec,
                        row.get('offense', ''),
                        row.get('offenseConference', ''),
                        int(row.get('offenseScore', 0)),
                        row.get('defense', ''),
                        row.get('defenseConference', ''),
                        int(row.get('defenseScore', 0)),
                        row.get('home', ''),
                        row.get('away', ''),
                        int(row.get('offenseTimeouts', 0)),
                        int(row.get('defenseTimeouts', 0)),
                        int(row.get('yardline', 0)) if row.get('yardline') else None,
                        int(row.get('yardsToGoal', 0)) if row.get('yardsToGoal') else None,
                        int(row.get('down', 0)) if row.get('down') else None,
                        int(row.get('distance', 0)) if row.get('distance') else None,
                        int(row.get('yardsGained', 0)) if row.get('yardsGained') else None,
                        row.get('scoring', 'False') == 'True',
                        row.get('playType', ''),
                        row.get('playText', ''),
                        float(row.get('ppa', 0)) if row.get('ppa') else None,
                        row.get('wallclock', '')
                    ))
                    plays_imported += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Error importing play {row.get('id', 'unknown')}: {str(e)}")
                    continue
        
        conn.commit()
        return plays_imported
        
    except Exception as e:
        print(f"    ❌ Error reading plays file: {str(e)}")
        return 0

def main():
    """Main import function"""
    
    print("🏈 GAMEDAY ANALYTICS DATABASE IMPORT")
    print("=" * 60)
    
    # Connect to database
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        print("Run create_analytics_db.py first!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    # Find all CSV files
    drives_folder = DRIVES_FOLDER
    if not os.path.exists(drives_folder):
        print(f"❌ Drives folder not found: {drives_folder}")
        return
    
    # Group files by team
    teams = defaultdict(dict)
    for filename in os.listdir(drives_folder):
        if filename.endswith('.csv'):
            if '_Drives.csv' in filename:
                team_name = filename.replace('_Drives.csv', '')
                teams[team_name]['drives'] = os.path.join(drives_folder, filename)
            elif '_Plays.csv' in filename:
                team_name = filename.replace('_Plays.csv', '')
                teams[team_name]['plays'] = os.path.join(drives_folder, filename)
    
    print(f"\n📁 Found {len(teams)} teams with CSV files")
    print(f"🚀 Starting import...\n")
    
    total_drives = 0
    total_plays = 0
    teams_processed = 0
    
    for team_name, files in sorted(teams.items()):
        if 'drives' in files and 'plays' in files:
            print(f"[{teams_processed + 1}/{len(teams)}] {team_name.replace('_', ' ')}")
            
            # Import drives
            drives_count = import_drives(conn, files['drives'], team_name)
            print(f"    ✅ Drives: {drives_count}")
            
            # Import plays
            plays_count = import_plays(conn, files['plays'], team_name)
            print(f"    ✅ Plays: {plays_count}")
            
            total_drives += drives_count
            total_plays += plays_count
            teams_processed += 1
        else:
            print(f"⚠️  {team_name}: Missing drives or plays file")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("📊 IMPORT COMPLETE!")
    print(f"✅ Teams processed: {teams_processed}")
    print(f"✅ Total drives: {total_drives:,}")
    print(f"✅ Total plays: {total_plays:,}")
    print(f"💾 Database: {DB_PATH}")

if __name__ == "__main__":
    main()
