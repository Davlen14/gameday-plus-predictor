#!/usr/bin/env python3
"""
Debug script to check Michigan team mapping and data issues
"""

import json
from app import get_team_id

def test_michigan_mapping():
    """Test Michigan team mapping"""
    print("🔍 Testing Michigan Team Mapping...")
    
    try:
        michigan_id = get_team_id("Michigan")
        print(f"✅ Michigan ID: {michigan_id}")
    except Exception as e:
        print(f"❌ Michigan mapping failed: {e}")
        return False
    
    try:
        washington_id = get_team_id("Washington")
        print(f"✅ Washington ID: {washington_id}")
    except Exception as e:
        print(f"❌ Washington mapping failed: {e}")
        return False
    
    # Check fbs.json directly
    try:
        with open('fbs.json', 'r') as f:
            teams_data = json.load(f)
        
        michigan_data = next((team for team in teams_data if team['id'] == michigan_id), None)
        washington_data = next((team for team in teams_data if team['id'] == washington_id), None)
        
        print(f"📊 Michigan data: {michigan_data}")
        print(f"📊 Washington data: {washington_data}")
        
        if michigan_data and washington_data:
            print("✅ Both teams found in fbs.json")
            return True
        else:
            print("❌ Missing team data in fbs.json")
            return False
            
    except Exception as e:
        print(f"❌ Error reading fbs.json: {e}")
        return False

if __name__ == "__main__":
    test_michigan_mapping()