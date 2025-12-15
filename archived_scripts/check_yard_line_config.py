#!/usr/bin/env python3
"""
Yard Line Configuration Checker
Analyzes how yard lines are currently being calculated and displayed
"""

import requests
import json

def check_api_data():
    """Check the live game API data structure"""
    print("=" * 80)
    print("YARD LINE CONFIGURATION CHECK")
    print("=" * 80)
    
    url = "http://localhost:5002/api/live-game?home=Tulane&away=North%20Texas"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print("\n�� GAME INFO:")
        print(f"  Home: {data['game_info']['home_team']}")
        print(f"  Away: {data['game_info']['away_team']}")
        print(f"  Status: {data['game_info']['status']}")
        
        print("\n🏈 FIELD POSITION (Current/Last Known):")
        fp = data.get('field_position', {})
        print(f"  Yard Line: {fp.get('yard_line', 'N/A')}")
        print(f"  Down: {fp.get('down', 'N/A')}")
        print(f"  Distance: {fp.get('distance', 'N/A')}")
        
        print("\n🎯 SAMPLE PLAYS (First 5):")
        plays = data.get('plays', [])
        for i, play in enumerate(plays[:5]):
            print(f"\n  Play {i+1}:")
            print(f"    Text: {play.get('play_text', '')[:80]}...")
            print(f"    Offense: {play.get('offense')} ({play.get('team')})")
            print(f"    Yard Line: {play.get('yard_line')}")
            print(f"    Yards to Goal: {play.get('yards_to_goal')}")
            print(f"    Yards Gained: {play.get('yards_gained')}")
            print(f"    Down & Distance: {play.get('down')} & {play.get('distance')}")
        
        # Find the specific Mestemaker play
        print("\n🔍 SPECIFIC PLAY ANALYSIS (Mestemaker to Sides):")
        for play in plays:
            if 'D.Mestemaker' in play.get('play_text', '') and 'L.Sides' in play.get('play_text', ''):
                print(f"  Full Text: {play.get('play_text')}")
                print(f"  Offense Team: {play.get('offense')} ({play.get('team')})")
                print(f"  Yard Line (raw from ESPN): {play.get('yard_line')}")
                print(f"  Yards Gained: {play.get('yards_gained')}")
                
                # Analyze what this means
                yard_line = play.get('yard_line', 0)
                yards_gained = play.get('yards_gained', 0)
                offense = play.get('offense')
                
                print("\n  ❓ PROBLEM ANALYSIS:")
                print(f"    • ESPN gives us: yard_line = {yard_line} (yardsToEndzone)")
                print(f"    • This means: {yard_line} yards from the OFFENSE's endzone")
                print(f"    • Play text says: 'caught at TLN48'")
                
                if offense == 'away':
                    print(f"    • North Texas (away) has ball at {yard_line} yards to their own endzone")
                    print(f"    • Absolute field position should be: {100 - yard_line} (from home's perspective)")
                    print(f"    • After 11 yard gain: should move to {100 - yard_line + yards_gained}")
                else:
                    print(f"    • Tulane (home) has ball at {yard_line} yards to their own endzone")
                    print(f"    • Absolute field position should be: {yard_line}")
                
                print("\n  ✅ EXPECTED BEHAVIOR:")
                print("    1. START: Ball at North Texas 41 (59 yards to their endzone)")
                print("    2. PLAY: 11 yard completion")
                print("    3. END: Ball at North Texas 48 (48 yards to Tulane's endzone = TLN48)")
                print("    4. Visual should show ball moving from 41 → 52 on absolute 0-100 field")
                
                break
        
        print("\n" + "=" * 80)
        print("CURRENT ISSUES:")
        print("=" * 80)
        print("❌ Backend is sending 'yardsToEndzone' as yard_line")
        print("❌ This is relative to OFFENSE's goal line, not absolute field position")
        print("❌ Frontend needs absolute 0-100 position for visualization")
        print("❌ Play direction not being considered (home going right, away going left)")
        
        print("\n" + "=" * 80)
        print("REQUIRED FIXES:")
        print("=" * 80)
        print("1️⃣ Backend (app.py):")
        print("   Convert yardsToEndzone → absolute field position (0-100)")
        print("   Formula for AWAY team: absolute_pos = 100 - yardsToEndzone")
        print("   Formula for HOME team: absolute_pos = yardsToEndzone")
        print("")
        print("2️⃣ Animation (FieldVisualization.tsx):")
        print("   Use start_yard_line and end_yard_line for trajectory")
        print("   Calculate both positions using same conversion logic")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Flask backend is running on http://localhost:5002")

if __name__ == "__main__":
    check_api_data()
