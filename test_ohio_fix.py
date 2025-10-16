#!/usr/bin/env python3
"""
Test script to verify Ohio State vs Ohio University player matching fix
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor

async def test_ohio_team_matching():
    """Test that Ohio State and Ohio University players are properly separated"""
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🔍 Testing Ohio Team Player Matching Fix")
    print("=" * 60)
    
    # Load comprehensive player data
    player_data = predictor._load_comprehensive_player_data()
    
    if not player_data:
        print("❌ Could not load player data")
        return
    
    print(f"📊 Loaded player data:")
    print(f"   QBs: {len(player_data.get('qbs', []))}")
    print(f"   WRs: {len(player_data.get('wrs', []))}")
    print(f"   RBs: {len(player_data.get('rbs', []))}")
    
    # Test Ohio State matching
    print(f"\n🏈 Testing 'Ohio State' player matching:")
    ohio_state_players = predictor._get_team_players("Ohio State", player_data)
    
    print(f"   QB: {ohio_state_players['qb']['name'] if ohio_state_players['qb'] else 'None'}")
    print(f"   WRs: {len(ohio_state_players['wrs'])}")
    print(f"   RBs: {len(ohio_state_players['rbs'])}")
    print(f"   TEs: {len(ohio_state_players['tes'])}")
    print(f"   Defense: {len(ohio_state_players['defense'])}")
    
    # Show all positions with their players
    if ohio_state_players['qb']:
        print(f"\n   🎯 Ohio State QB:")
        qb = ohio_state_players['qb']
        print(f"      • {qb.get('name', 'Unknown')} (Team: {qb.get('team', 'Unknown')})")
        
    if ohio_state_players['wrs']:
        print(f"\n   📡 Ohio State WRs ({len(ohio_state_players['wrs'])}):")
        for i, wr in enumerate(ohio_state_players['wrs'][:5]):
            team = wr.get('team', 'Unknown')
            print(f"      {i+1}. {wr.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_state_players['rbs']:
        print(f"\n   🏃 Ohio State RBs ({len(ohio_state_players['rbs'])}):")
        for i, rb in enumerate(ohio_state_players['rbs'][:3]):
            team = rb.get('team', 'Unknown')
            print(f"      {i+1}. {rb.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_state_players['tes']:
        print(f"\n   🎯 Ohio State TEs ({len(ohio_state_players['tes'])}):")
        for i, te in enumerate(ohio_state_players['tes'][:3]):
            team = te.get('team', 'Unknown')
            print(f"      {i+1}. {te.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_state_players['defense']:
        print(f"\n   🛡️  Ohio State Defense ({len(ohio_state_players['defense'])}):")
        for i, def_player in enumerate(ohio_state_players['defense'][:5]):
            team = def_player.get('team', 'Unknown')
            position = def_player.get('position_type', 'DEF')
            print(f"      {i+1}. {def_player.get('name', 'Unknown')} ({position}) (Team: {team})")
    
    # Test Ohio University matching (if exists in data)
    print(f"\n🏈 Testing 'Ohio University' player matching:")
    ohio_univ_players = predictor._get_team_players("Ohio University", player_data)
    
    print(f"   QB: {ohio_univ_players['qb']['name'] if ohio_univ_players['qb'] else 'None'}")
    print(f"   WRs: {len(ohio_univ_players['wrs'])}")
    print(f"   RBs: {len(ohio_univ_players['rbs'])}")
    print(f"   TEs: {len(ohio_univ_players['tes'])}")
    print(f"   Defense: {len(ohio_univ_players['defense'])}")
    
    # Show all positions with their players
    if ohio_univ_players['qb']:
        print(f"\n   🎯 Ohio University QB:")
        qb = ohio_univ_players['qb']
        print(f"      • {qb.get('name', 'Unknown')} (Team: {qb.get('team', 'Unknown')})")
        
    if ohio_univ_players['wrs']:
        print(f"\n   📡 Ohio University WRs ({len(ohio_univ_players['wrs'])}):")
        for i, wr in enumerate(ohio_univ_players['wrs'][:5]):
            team = wr.get('team', 'Unknown')
            print(f"      {i+1}. {wr.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_univ_players['rbs']:
        print(f"\n   🏃 Ohio University RBs ({len(ohio_univ_players['rbs'])}):")
        for i, rb in enumerate(ohio_univ_players['rbs'][:3]):
            team = rb.get('team', 'Unknown')
            print(f"      {i+1}. {rb.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_univ_players['tes']:
        print(f"\n   🎯 Ohio University TEs ({len(ohio_univ_players['tes'])}):")
        for i, te in enumerate(ohio_univ_players['tes'][:3]):
            team = te.get('team', 'Unknown')
            print(f"      {i+1}. {te.get('name', 'Unknown')} (Team: {team})")
            
    if ohio_univ_players['defense']:
        print(f"\n   �️  Ohio University Defense ({len(ohio_univ_players['defense'])}):")
        for i, def_player in enumerate(ohio_univ_players['defense'][:5]):
            team = def_player.get('team', 'Unknown')
            position = def_player.get('position_type', 'DEF')
            print(f"      {i+1}. {def_player.get('name', 'Unknown')} ({position}) (Team: {team})")
    
    # Test with just "Ohio" to see if it incorrectly matches both
    print(f"\n🏈 Testing 'Ohio' player matching:")
    ohio_players = predictor._get_team_players("Ohio", player_data)
    
    print(f"   QB: {ohio_players['qb']['name'] if ohio_players['qb'] else 'None'}")
    print(f"   WRs: {len(ohio_players['wrs'])}")
    print(f"   RBs: {len(ohio_players['rbs'])}")
    print(f"   Defense: {len(ohio_players['defense'])}")
    
    # Analysis
    print(f"\n📊 Analysis:")
    osu_total = len(ohio_state_players['wrs']) + len(ohio_state_players['rbs']) + len(ohio_state_players['tes']) + len(ohio_state_players['defense']) + (1 if ohio_state_players['qb'] else 0)
    ou_total = len(ohio_univ_players['wrs']) + len(ohio_univ_players['rbs']) + len(ohio_univ_players['tes']) + len(ohio_univ_players['defense']) + (1 if ohio_univ_players['qb'] else 0)
    ohio_total = len(ohio_players['wrs']) + len(ohio_players['rbs']) + len(ohio_players['tes']) + len(ohio_players['defense']) + (1 if ohio_players['qb'] else 0)
    
    print(f"   Ohio State players found: {osu_total}")
    print(f"   Ohio University players found: {ou_total}")
    print(f"   Ohio (generic) players found: {ohio_total}")
    
    # Check for team contamination in Ohio State results
    print(f"\n🔍 Checking for team contamination:")
    contaminated = False
    
    all_ohio_state = [ohio_state_players['qb']] + ohio_state_players['wrs'] + ohio_state_players['rbs'] + ohio_state_players['defense']
    all_ohio_state = [p for p in all_ohio_state if p]  # Remove None values
    
    for player in all_ohio_state:
        team = player.get('team', '').lower()
        if 'ohio' in team and ('university' in team or ('ohio' in team and 'state' not in team)):
            print(f"   ❌ Contamination found: {player.get('name', 'Unknown')} listed as Ohio State but team is '{player.get('team', 'Unknown')}'")
            contaminated = True
    
    if not contaminated and all_ohio_state:
        print(f"   ✅ No contamination found - all {len(all_ohio_state)} Ohio State players have correct team association")
    elif not all_ohio_state:
        print(f"   ⚠️  No Ohio State players found to check")
    
    print(f"\n{'✅ FIX VERIFIED' if not contaminated else '❌ FIX INCOMPLETE'}")

if __name__ == "__main__":
    asyncio.run(test_ohio_team_matching())