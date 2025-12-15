#!/usr/bin/env python3
"""
Update coaches_master.db with headshots and team logos
"""

import json
import sqlite3

def load_headshots():
    """Load headshots from power5_coaches_headshots.json"""
    with open('power5_coaches_headshots.json', 'r') as f:
        data = json.load(f)
    
    # Flatten all conferences into single dict
    headshots = {}
    for conference, coaches in data.items():
        for coach_info in coaches:
            coach_name = coach_info['coach']
            headshot_url = coach_info.get('headshot_url', '')
            if headshot_url:
                headshots[coach_name] = headshot_url
    
    return headshots

def load_team_logos():
    """Load team logos from fbs.json"""
    with open('fbs.json', 'r') as f:
        teams = json.load(f)
    
    # Create dict of school -> logo
    logos = {}
    for team in teams:
        school = team['school']
        logo_list = team.get('logos', [])
        if logo_list:
            logos[school] = logo_list[0]  # Use primary logo
    
    return logos

def update_database():
    """Update coaches_master.db with headshots and logos"""
    print("🔄 Loading headshots and team logos...")
    headshots = load_headshots()
    team_logos = load_team_logos()
    
    print(f"✅ Loaded {len(headshots)} headshots")
    print(f"✅ Loaded {len(team_logos)} team logos")
    
    # Connect to database
    conn = sqlite3.connect('instance/coaches_master.db')
    cursor = conn.cursor()
    
    # First, add team_logo column to stints if it doesn't exist
    try:
        cursor.execute("ALTER TABLE stints ADD COLUMN team_logo TEXT")
        print("✅ Added team_logo column to stints table")
    except sqlite3.OperationalError:
        print("ℹ️  team_logo column already exists in stints table")
    
    # Update coach headshots
    updated_headshots = 0
    for coach_name, headshot_url in headshots.items():
        cursor.execute("""
            UPDATE coaches 
            SET headshot_url = ? 
            WHERE name = ?
        """, (headshot_url, coach_name))
        if cursor.rowcount > 0:
            updated_headshots += 1
    
    print(f"✅ Updated {updated_headshots} coach headshots")
    
    # Update team logos in stints
    updated_logos = 0
    cursor.execute("SELECT id, school FROM stints")
    stints = cursor.fetchall()
    
    for stint_id, school in stints:
        logo = team_logos.get(school)
        if logo:
            cursor.execute("""
                UPDATE stints 
                SET team_logo = ? 
                WHERE id = ?
            """, (logo, stint_id))
            updated_logos += 1
    
    print(f"✅ Updated {updated_logos} team logos in stints")
    
    # Commit changes
    conn.commit()
    
    # Verify updates
    cursor.execute("SELECT COUNT(*) FROM coaches WHERE headshot_url IS NOT NULL AND headshot_url != ''")
    headshot_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stints WHERE team_logo IS NOT NULL AND team_logo != ''")
    logo_count = cursor.fetchone()[0]
    
    print("\n" + "="*80)
    print("📊 DATABASE UPDATE COMPLETE")
    print("="*80)
    print(f"🎯 Coaches with headshots: {headshot_count}")
    print(f"🏫 Stints with team logos: {logo_count}")
    print("="*80)
    
    conn.close()

if __name__ == '__main__':
    update_database()
