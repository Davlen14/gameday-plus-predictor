#!/usr/bin/env python3
"""
Add coach headshots from JSON file to database
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent / 'instance' / 'coaches_master.db'

# JSON headshots file path
HEADSHOTS_JSON = Path(__file__).parent / 'frontend' / 'src' / 'data' / 'power5_coaches_headshots.json'

def load_headshots_from_json():
    """Load all coach headshots from JSON file"""
    with open(HEADSHOTS_JSON, 'r') as f:
        data = json.load(f)
    
    # Flatten all coaches from different conferences
    all_coaches = []
    for conference, coaches in data.items():
        all_coaches.extend(coaches)
    
    return all_coaches

def add_headshots_to_db(headshots):
    """Add headshots to database, matching by coach name and school"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updated_count = 0
    not_found = []
    
    for headshot_data in headshots:
        coach_name = headshot_data.get('coach')
        school = headshot_data.get('school')
        headshot_url = headshot_data.get('headshot_url')
        
        if not coach_name or not school or not headshot_url:
            print(f"⚠️  Skipping incomplete entry: {coach_name} at {school}")
            continue
        
        # Try to find coach by name and school
        cursor.execute(
            "SELECT id FROM coaches WHERE name = ? AND current_school = ?",
            (coach_name, school)
        )
        result = cursor.fetchone()
        
        if result:
            coach_id = result[0]
            # Update the headshot URL
            cursor.execute(
                "UPDATE coaches SET headshot_url = ?, updated_at = ? WHERE id = ?",
                (headshot_url, datetime.now().isoformat(), coach_id)
            )
            updated_count += 1
            print(f"✅ Updated: {coach_name} ({school})")
        else:
            not_found.append(f"{coach_name} ({school})")
            print(f"❌ Not found: {coach_name} ({school})")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully updated: {updated_count} coaches")
    print(f"❌ Not found in database: {len(not_found)}")
    
    if not_found:
        print(f"\nMissing coaches:")
        for coach in not_found:
            print(f"  - {coach}")

if __name__ == '__main__':
    print(f"Loading headshots from {HEADSHOTS_JSON.name}...")
    headshots = load_headshots_from_json()
    print(f"Loaded {len(headshots)} coach headshots\n")
    
    print(f"Adding headshots to database ({DB_PATH})...\n")
    add_headshots_to_db(headshots)
