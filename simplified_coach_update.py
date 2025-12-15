#!/usr/bin/env python3
"""
Simplified approach: Update coaches with ESPN/CFBD IDs and basic records
Then we can pull game-by-game data later
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_FILE = Path("instance/coaches_master.db")

# Manual G5 coach records (current school only - 2024-25 season)
G5_COACH_RECORDS = {
    # MAC
    "Joe Moorhead": {"school": "Akron", "record": "4-8", "cfbd_id": None},
    "Mike Uremovich": {"school": "Ball State", "record": "3-9", "cfbd_id": None},
    "Eddie George": {"school": "Bowling Green", "record": "7-6", "cfbd_id": None},
    "Pete Lembo": {"school": "Buffalo", "record": "7-5", "cfbd_id": None},
    "Matt Drinkall": {"school": "Central Michigan", "record": "4-8", "cfbd_id": None},
    "Chris Creighton": {"school": "Eastern Michigan", "record": "6-6", "cfbd_id": None},
    "Mark Carney": {"school": "Kent State", "record": "0-12", "cfbd_id": None},
    "Chuck Martin": {"school": "Miami (OH)", "record": "7-5", "cfbd_id": None},
    "Thomas Hammock": {"school": "Northern Illinois", "record": "7-5", "cfbd_id": None},
    "Brian Smith": {"school": "Ohio", "record": "9-4", "cfbd_id": None},
    "Jason Candle": {"school": "Toledo", "record": "7-5", "cfbd_id": None},
    "Joe Harasymiak": {"school": "UMass", "record": "2-10", "cfbd_id": None},
    "Lance Taylor": {"school": "Western Michigan", "record": "4-8", "cfbd_id": None},
    
    # AAC
    "Jeff Monken": {"school": "Army", "record": "11-2", "cfbd_id": None},
    "Tim Albin": {"school": "Charlotte", "record": "5-7", "cfbd_id": None},
    "Blake Harrell": {"school": "East Carolina", "record": "8-5", "cfbd_id": None},
    "Zach Kittley": {"school": "Florida Atlantic", "record": "3-9", "cfbd_id": None},
    "Ryan Silverfield": {"school": "Memphis", "record": "10-3", "cfbd_id": None},
    "Brian Newberry": {"school": "Navy", "record": "9-3", "cfbd_id": None},
    "Scott Abell": {"school": "Rice", "record": "4-8", "cfbd_id": None},
    "Alex Golesh": {"school": "South Florida", "record": "6-6", "cfbd_id": None},
    "K.C. Keeler": {"school": "Temple", "record": "3-9", "cfbd_id": None},
    "Tre Lamb": {"school": "Tulsa", "record": "3-9", "cfbd_id": None},
    "Trent Dilfer": {"school": "UAB", "record": "3-9", "cfbd_id": None},
    "Jeff Traylor": {"school": "UTSA", "record": "6-6", "cfbd_id": None},
    
    # CUSA
    "Ryan Carty": {"school": "Delaware", "record": "5-7", "cfbd_id": None},
    "Willie Simmons": {"school": "FIU", "record": "4-8", "cfbd_id": None},
    "Charles Kelly": {"school": "Jacksonville State", "record": "8-4", "cfbd_id": None},
    "Jerry Mack": {"school": "Kennesaw State", "record": "1-11", "cfbd_id": None},
    "Jamey Chadwell": {"school": "Liberty", "record": "8-3", "cfbd_id": None},
    "Sonny Cumbie": {"school": "Louisiana Tech", "record": "4-8", "cfbd_id": None},
    "Derek Mason": {"school": "Middle Tennessee", "record": "3-9", "cfbd_id": None},
    "Ryan Beard": {"school": "Missouri State", "record": "6-6", "cfbd_id": None},
    "Tony Sanchez": {"school": "New Mexico State", "record": "3-9", "cfbd_id": None},
    "Phil Longo": {"school": "Sam Houston", "record": "8-5", "cfbd_id": None},
    "Scotty Walden": {"school": "UTEP", "record": "3-10", "cfbd_id": None},
    "Tyson Helton": {"school": "Western Kentucky", "record": "8-5", "cfbd_id": None},
    
    # Sun Belt
    "Dowell Loggains": {"school": "Appalachian State", "record": "5-7", "cfbd_id": None},
    "Butch Jones": {"school": "Arkansas State", "record": "7-5", "cfbd_id": None},
    "Tim Beck": {"school": "Coastal Carolina", "record": "5-7", "cfbd_id": None},
    "Clay Helton": {"school": "Georgia Southern", "record": "8-5", "cfbd_id": None},
    "Dell McGee": {"school": "Georgia State", "record": "3-9", "cfbd_id": None},
    "Bob Chesney": {"school": "James Madison", "record": "8-4", "cfbd_id": None},
    "Michael Desormeaux": {"school": "Louisiana", "record": "10-3", "cfbd_id": None},
    "Bryant Vincent": {"school": "Louisiana-Monroe", "record": "5-7", "cfbd_id": None},
    "Tony Gibson": {"school": "Marshall", "record": "10-3", "cfbd_id": None},
    "Ricky Rahne": {"school": "Old Dominion", "record": "4-8", "cfbd_id": None},
    "Major Applewhite": {"school": "South Alabama", "record": "6-6", "cfbd_id": None},
    "Charles Huff": {"school": "Southern Miss", "record": "9-4", "cfbd_id": None},
    "G.J. Kinne": {"school": "Texas State", "record": "7-5", "cfbd_id": None},
    "Gerad Parker": {"school": "Troy", "record": "3-9", "cfbd_id": None},
    
    # Mountain West
    "Troy Calhoun": {"school": "Air Force", "record": "4-8", "cfbd_id": None},
    "Spencer Danielson": {"school": "Boise State", "record": "12-2", "cfbd_id": None},
    "Jay Norvell": {"school": "Colorado State", "record": "8-5", "cfbd_id": None},
    "Matt Entz": {"school": "Fresno State", "record": "6-7", "cfbd_id": None},
    "Timmy Chang": {"school": "Hawaii", "record": "5-8", "cfbd_id": None},
    "Jeff Choate": {"school": "Nevada", "record": "3-10", "cfbd_id": None},
    "Jason Eck": {"school": "New Mexico", "record": "5-7", "cfbd_id": None},
    "Sean Lewis": {"school": "San Diego State", "record": "3-9", "cfbd_id": None},
    "Ken Niumatalolo": {"school": "San Jose State", "record": "3-9", "cfbd_id": None},
    "Dan Mullen": {"school": "UNLV", "record": "11-3", "cfbd_id": None},
    "Bronco Mendenhall": {"school": "Utah State", "record": "4-8", "cfbd_id": None},
    "Jay Sawvel": {"school": "Wyoming", "record": "2-10", "cfbd_id": None},
}

def update_coach_records():
    print("="*60)
    print("UPDATING G5 COACH RECORDS (2024-25 Season)")
    print("="*60)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    updated = 0
    not_found = 0
    
    for coach_name, data in G5_COACH_RECORDS.items():
        school = data["school"]
        record = data["record"]
        
        # Parse record
        parts = record.split("-")
        wins = int(parts[0])
        losses = int(parts[1])
        total_games = wins + losses
        win_pct = wins / total_games if total_games > 0 else 0.0
        
        # Update database
        cursor.execute("""
            UPDATE coaches 
            SET career_record = ?,
                career_win_pct = ?,
                total_games = ?,
                updated_at = ?
            WHERE name = ? AND current_school = ?
        """, (
            record,
            round(win_pct, 3),
            total_games,
            datetime.now().isoformat(),
            coach_name,
            school
        ))
        
        if cursor.rowcount > 0:
            print(f"  ✓ {coach_name} ({school}): {record}")
            updated += 1
        else:
            print(f"  ⊙ {coach_name} ({school}): Not found in DB")
            not_found += 1
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✓ Updated: {updated} coaches")
    print(f"⊙ Not found: {not_found} coaches")
    
    # Final count
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM coaches")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM coaches WHERE total_games > 0")
    with_data = cursor.fetchone()[0]
    conn.close()
    
    print(f"\nDatabase status:")
    print(f"  Total coaches: {total}")
    print(f"  With data: {with_data}")
    print(f"  Missing data: {total - with_data}")

if __name__ == "__main__":
    update_coach_records()
