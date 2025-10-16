#!/usr/bin/env python3
"""
Test to see all 18 sections output from run.py directly
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor
from run import format_prediction_output

async def test_all_18_sections():
    """Test that all 18 sections are generated"""
    
    print("🎯 TESTING ALL 18 SECTIONS OUTPUT")
    print("=" * 80)
    
    # Initialize predictor
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    # Test with Minnesota vs Nebraska
    home_team_id = 135   # Minnesota  
    away_team_id = 158   # Nebraska
    
    # Load team data
    with open('fbs.json', 'r') as f:
        fbs_teams = json.load(f)
    
    home_team_fbs = next((team for team in fbs_teams if team['id'] == home_team_id), None)
    away_team_fbs = next((team for team in fbs_teams if team['id'] == away_team_id), None)
    
    home_team_data = {
        'id': home_team_id,
        'name': home_team_fbs['school'],
        'logo_url': home_team_fbs['logos'][0],
    }
    
    away_team_data = {
        'id': away_team_id,
        'name': away_team_fbs['school'], 
        'logo_url': away_team_fbs['logos'][0],
    }
    
    print(f"Testing: {away_team_data['name']} @ {home_team_data['name']}")
    
    # Make real prediction
    prediction = await predictor.predict_game(home_team_id, away_team_id)
    
    print("\n🔍 CALLING format_prediction_output DIRECTLY:")
    print("=" * 80)
    
    # Call the function directly and count sections
    output_lines = []
    import sys
    import io
    
    # Capture output
    original_stdout = sys.stdout
    captured = io.StringIO()
    sys.stdout = captured
    
    try:
        format_prediction_output(prediction, home_team_data, away_team_data)
    finally:
        sys.stdout = original_stdout
    
    full_output = captured.getvalue()
    lines = full_output.split('\n')
    
    # Count sections (look for both � and 🎯 emojis)
    sections_found = []
    for i, line in enumerate(lines):
        if '[' in line and ']' in line and ('🎯' in line or '�' in line or '📺' in line):
            # Extract section number
            import re
            match = re.search(r'\[(\d+(?:\.\d+)?)\]', line)
            if match:
                sections_found.append((match.group(1), line.strip()))
    
    print(f"📊 SECTIONS ANALYSIS:")
    print(f"   Total output lines: {len(lines)}")
    print(f"   Total characters: {len(full_output)}")
    print(f"   Sections found: {len(sections_found)}")
    print()
    
    print("🔍 SECTIONS DETECTED:")
    for section_num, section_line in sections_found:
        print(f"   [{section_num}] - {section_line}")
    
    if len(sections_found) >= 18:
        print(f"\n✅ SUCCESS: Found {len(sections_found)} sections (≥18 expected)")
    else:
        print(f"\n❌ MISSING SECTIONS: Only {len(sections_found)} found, expected ≥18")
        
        # Show where output might be truncated
        print(f"\n📄 LAST 10 LINES OF OUTPUT:")
        for line in lines[-10:]:
            if line.strip():
                print(f"   {line}")
    
    # Save full output for inspection
    with open('full_output_test.txt', 'w') as f:
        f.write(full_output)
    print(f"\n💾 Full output saved to 'full_output_test.txt' for inspection")
    
    return len(sections_found) >= 18

if __name__ == "__main__":
    success = asyncio.run(test_all_18_sections())
    if success:
        print("\n✅ ALL SECTIONS ARE WORKING!")
    else:
        print("\n❌ SECTIONS ARE MISSING - NEED TO DEBUG")