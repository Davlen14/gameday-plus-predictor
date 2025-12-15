#!/usr/bin/env python3
"""
Script to add all G5 coaches to headshots JSON and database
"""

import json
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

# Read the G5 coaches CSV
csv_file = Path("frontend/src/components/figma/g5_head_coaches_2025_COMPLETE.csv")
headshots_file = Path("frontend/src/data/power5_coaches_headshots.json")
db_file = Path("instance/coaches_master.db")

print("Reading G5 coaches from CSV...")
g5_coaches = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        g5_coaches.append({
            "conference": row["Conference"],
            "school": row["School"],
            "coach": row["Head Coach"],
            "headshot_url": row["Headshot URL"],
            "profile_link": row["Profile Link"]
        })

print(f"Found {len(g5_coaches)} G5 coaches")

# Read existing headshots JSON
print("\nReading existing headshots JSON...")
with open(headshots_file, 'r', encoding='utf-8') as f:
    headshots_data = json.load(f)

# Group G5 coaches by conference
g5_by_conference = {}
for coach in g5_coaches:
    conf = coach["conference"].lower()
    if conf not in g5_by_conference:
        g5_by_conference[conf] = []
    g5_by_conference[conf].append({
        "coach": coach["coach"],
        "school": coach["school"],
        "headshot_url": coach["headshot_url"]
    })

# Add G5 conferences to headshots
for conf, coaches in g5_by_conference.items():
    if conf not in headshots_data:
        headshots_data[conf] = []
    headshots_data[conf] = coaches

print(f"Updated headshots JSON with {len(g5_by_conference)} G5 conferences")

# Save updated headshots JSON
print("Saving updated headshots JSON...")
with open(headshots_file, 'w', encoding='utf-8') as f:
    json.dump(headshots_data, f, indent=2, ensure_ascii=False)

print(f"✓ Saved to {headshots_file}")

# Now add coaches to database
print("\n" + "="*60)
print("Adding coaches to database...")
print("="*60)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get existing coach schools
cursor.execute("SELECT DISTINCT LOWER(current_school) FROM coaches")
existing_schools = set([row[0] for row in cursor.fetchall()])

added_count = 0
skipped_count = 0

for coach_data in g5_coaches:
    school = coach_data["school"]
    coach_name = coach_data["coach"]
    headshot = coach_data["headshot_url"]
    
    # Check if coach already exists
    if school.lower() in existing_schools:
        print(f"  ⊙ Skipping {coach_name} ({school}) - already exists")
        skipped_count += 1
        continue
    
    # Insert coach with basic data
    # We'll set placeholders that can be updated later with comprehensive data
    cursor.execute("""
        INSERT INTO coaches (
            name,
            current_school,
            headshot_url,
            career_record,
            career_win_pct,
            total_games,
            created_at,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coach_name,
        school,
        headshot,
        "0-0",  # Placeholder - will be updated
        0.0,    # Placeholder - will be updated
        0,      # Placeholder - will be updated
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    print(f"  ✓ Added {coach_name} ({school})")
    added_count += 1

conn.commit()

# Now fetch comprehensive data for the new coaches
print("\n" + "="*60)
print("Fetching comprehensive data for new coaches...")
print("="*60)

# Get all new coach IDs
cursor.execute("""
    SELECT id, name, current_school 
    FROM coaches 
    WHERE career_record = '0-0' OR total_games = 0
""")
new_coaches = cursor.fetchall()

print(f"Found {len(new_coaches)} coaches needing comprehensive data\n")

# For now, we'll just mark them as needing data
# In a real implementation, you would call CFBD API here
for coach_id, coach_name, school in new_coaches:
    print(f"  → {coach_name} ({school}) - needs CFBD data fetch")
    # TODO: Call CFBD API to get:
    # - career_record
    # - career_win_pct  
    # - total_games
    # - espn_id
    # - cfbd_id
    # And populate related tables:
    # - stints
    # - games
    # - rankings
    # - season_analytics
    # - situational_stats
    # - vs_coaches

conn.close()

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"✓ Added {added_count} new coaches to database")
print(f"⊙ Skipped {skipped_count} existing coaches")
print(f"✓ Updated headshots JSON with all G5 coaches")
print(f"\n⚠️  Note: New coaches need comprehensive data from CFBD API")
print("Run the CFBD data fetch script to populate full coach stats")
