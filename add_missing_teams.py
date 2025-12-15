#!/usr/bin/env python3
"""
Add missing teams from fbs.json to coaches_master.db
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / 'instance' / 'coaches_master.db'
FBS_JSON_PATH = Path(__file__).parent / 'fbs.json'

def load_fbs_json():
    """Load teams from fbs.json"""
    with open(FBS_JSON_PATH) as f:
        return json.load(f)

def get_existing_teams(conn):
    """Get set of existing team names in database"""
    cursor = conn.cursor()
    cursor.execute("SELECT school FROM teams")
    return {row[0] for row in cursor.fetchall()}

def add_teams(teams_to_add):
    """Add teams to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    created_at = datetime.now().isoformat()
    added = 0
    
    for team in teams_to_add:
        try:
            cursor.execute("""
                INSERT INTO teams (
                    id, school, mascot, abbreviation, conference,
                    color, alt_color, logo_url, location_name, capacity,
                    city, state, classification, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team['id'],
                team['school'],
                team.get('mascot', ''),
                team.get('abbreviation', ''),
                team.get('conference', ''),
                team.get('primary_color', ''),
                team.get('alt_color', ''),
                team['logos'][0] if team.get('logos') else None,
                team.get('location_name', ''),
                team.get('capacity', 0),
                team.get('city', ''),
                team.get('state', ''),
                team.get('classification', 'fbs'),
                created_at
            ))
            added += 1
        except sqlite3.IntegrityError as e:
            print(f"Error adding {team['school']}: {e}")
        except Exception as e:
            print(f"Unexpected error for {team['school']}: {e}")
    
    conn.commit()
    conn.close()
    return added

def main():
    print("Loading fbs.json...")
    all_teams = load_fbs_json()
    
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    
    existing = get_existing_teams(conn)
    conn.close()
    
    print(f"Found {len(existing)} existing teams in database")
    print(f"Found {len(all_teams)} teams in fbs.json")
    
    # Filter to teams with conferences that aren't in database
    teams_to_add = [
        t for t in all_teams 
        if t.get('conference') and t['school'] not in existing
    ]
    
    print(f"\nTeams to add: {len(teams_to_add)}")
    
    if teams_to_add:
        print(f"Adding {len(teams_to_add)} teams...")
        added = add_teams(teams_to_add)
        print(f"✅ Successfully added {added} teams!")
    else:
        print("No teams to add!")

if __name__ == '__main__':
    main()
