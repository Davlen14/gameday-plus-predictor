"""
🗄️ MIGRATE JSON DATA TO PREDICTIONS.DB
=====================================
Imports all critical JSON files into predictions.db so the predictor
can read everything from the database instead of JSON files.
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DB_PATH = 'instance/predictions.db'
BASE_PATH = '/Users/davlenswain/Desktop/Gameday_Graphql_Model'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create new tables for JSON data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table for coaches ranking data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coaches_rankings_data (
            id INTEGER PRIMARY KEY,
            coach_id INTEGER,
            coach_name TEXT,
            current_team TEXT,
            conference TEXT,
            career_wins INTEGER,
            career_losses INTEGER,
            season_2025_wins INTEGER,
            season_2025_losses INTEGER,
            overall_rank INTEGER,
            data_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for FBS ratings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fbs_ratings_comprehensive (
            id INTEGER PRIMARY KEY,
            team_id INTEGER UNIQUE,
            team_name TEXT,
            conference TEXT,
            rating REAL,
            rank INTEGER,
            data_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for player metrics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_metrics_data (
            id INTEGER PRIMARY KEY,
            position TEXT,
            player_name TEXT,
            team TEXT,
            metric_type TEXT,
            metric_value REAL,
            data_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Tables created successfully")

def import_coaches_data():
    """Import coaches_simplified_ranked.json"""
    print("\n📥 Importing coaches data...")
    
    json_path = os.path.join(BASE_PATH, 'frontend/src/data/coaches_simplified_ranked.json')
    
    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        return
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM coaches_rankings_data')
    
    coaches = data.get('coaches', [])
    for coach in coaches:
        try:
            cursor.execute('''
                INSERT INTO coaches_rankings_data 
                (coach_id, coach_name, current_team, conference, career_wins, 
                 career_losses, season_2025_wins, season_2025_losses, overall_rank, data_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coach.get('id'),
                coach.get('name'),
                coach.get('currentTeam', {}).get('school'),
                coach.get('currentTeam', {}).get('conference'),
                coach.get('careerRecord', {}).get('wins'),
                coach.get('careerRecord', {}).get('losses'),
                coach.get('current2025Season', {}).get('wins'),
                coach.get('current2025Season', {}).get('losses'),
                coach.get('rankings', {}).get('overallRank'),
                json.dumps(coach)
            ))
        except Exception as e:
            print(f"⚠️  Error importing coach {coach.get('name')}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {len(coaches)} coaches")

def import_fbs_ratings():
    """Import all_fbs_ratings_comprehensive JSON"""
    print("\n📥 Importing FBS ratings...")
    
    # Find the latest FBS ratings file
    fbs_files = []
    for root, dirs, files in os.walk(os.path.join(BASE_PATH, 'weekly_updates')):
        for f in files:
            if 'all_fbs_ratings_comprehensive' in f and f.endswith('.json'):
                fbs_files.append(os.path.join(root, f))
    
    if not fbs_files:
        print("❌ No FBS ratings files found")
        return
    
    # Use the most recent file
    json_path = sorted(fbs_files)[-1]
    print(f"Using: {json_path}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM fbs_ratings_comprehensive')
    
    teams = data.get('teams', []) if isinstance(data, dict) else data
    count = 0
    
    for team in teams:
        try:
            cursor.execute('''
                INSERT INTO fbs_ratings_comprehensive 
                (team_id, team_name, conference, rating, rank, data_json)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                team.get('id') or team.get('team_id'),
                team.get('name') or team.get('team_name'),
                team.get('conference'),
                team.get('rating') or team.get('elo_rating'),
                team.get('rank') or team.get('ranking'),
                json.dumps(team)
            ))
            count += 1
        except Exception as e:
            print(f"⚠️  Error importing team {team.get('name')}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} FBS teams")

def import_player_metrics():
    """Import player metrics from all positions"""
    print("\n📥 Importing player metrics...")
    
    positions = ['qb', 'wr', 'rb', 'te', 'db', 'dl', 'lb']
    player_metrics_path = os.path.join(BASE_PATH, 'player_metrics')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM player_metrics_data')
    
    total_imported = 0
    
    for position in positions:
        pos_dir = os.path.join(player_metrics_path, position)
        
        if not os.path.exists(pos_dir):
            continue
        
        # Find the most recent comprehensive analysis file
        files = sorted([f for f in os.listdir(pos_dir) if 'comprehensive' in f and f.endswith('.json')])
        
        if not files:
            continue
        
        json_path = os.path.join(pos_dir, files[-1])
        print(f"  Importing {position.upper()}: {files[-1]}")
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            # Handle different data structures - player metrics use 'rankings' key
            players = data.get('rankings', []) if isinstance(data, dict) else data
            
            for player in players:
                try:
                    # Extract metrics from various possible field names
                    player_name = (player.get('name') or player.get('player_name') or 
                                  player.get('Player') or 'Unknown')
                    team = (player.get('team') or player.get('Team') or 
                           player.get('school') or player.get('School') or 'Unknown')
                    rating = (player.get('rating') or player.get('efficiency_score') or 
                             player.get('composite_score') or 0)
                    
                    cursor.execute('''
                        INSERT INTO player_metrics_data 
                        (position, player_name, team, metric_type, metric_value, data_json)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        position.upper(),
                        player_name,
                        team,
                        'comprehensive_ranking',
                        float(rating) if rating else 0,
                        json.dumps(player)
                    ))
                    total_imported += 1
                except Exception as e:
                    print(f"⚠️  Error importing {position} player: {e}")
        
        except Exception as e:
            print(f"❌ Error reading {position} file: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {total_imported} player metrics")

def verify_imports():
    """Verify data was imported"""
    print("\n🔍 Verifying imports...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM coaches_rankings_data')
    coaches_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM fbs_ratings_comprehensive')
    fbs_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM player_metrics_data')
    player_count = cursor.fetchone()['count']
    
    conn.close()
    
    print(f"\n📊 IMPORT SUMMARY:")
    print(f"  ✅ Coaches: {coaches_count}")
    print(f"  ✅ FBS Teams: {fbs_count}")
    print(f"  ✅ Player Metrics: {player_count}")
    print(f"\n✨ All data migrated to predictions.db!")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🗄️  MIGRATING JSON DATA TO PREDICTIONS.DB")
    print("="*60)
    
    create_tables()
    import_coaches_data()
    import_fbs_ratings()
    import_player_metrics()
    verify_imports()
    
    print("\n" + "="*60)
    print("✅ MIGRATION COMPLETE!")
    print("="*60)
