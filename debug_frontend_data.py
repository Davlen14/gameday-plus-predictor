#!/usr/bin/env python3
"""
Debug the player data structure being sent to frontend
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor

async def debug_player_structure():
    """Debug what's actually being sent to the frontend"""
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🔍 Debugging Player Data Structure")
    print("=" * 60)
    
    # Test with Ohio State vs Wisconsin (the same matchup from your screenshot)
    home_team_id = 275   # Wisconsin  
    away_team_id = 194   # Ohio State
    
    print(f"🎯 Testing: Ohio State @ Wisconsin")
    
    try:
        prediction = await predictor.predict_game(home_team_id, away_team_id)
        
        if prediction and hasattr(prediction, 'detailed_analysis'):
            enhanced_player_analysis = prediction.detailed_analysis.get('enhanced_player_analysis', {})
            
            print(f"\n📊 Enhanced Player Analysis Structure:")
            print(f"Keys: {list(enhanced_player_analysis.keys())}")
            
            if 'away_players' in enhanced_player_analysis:
                away_players = enhanced_player_analysis['away_players']
                print(f"\n🏈 Away Players (Ohio State) Structure:")
                print(f"Keys: {list(away_players.keys())}")
                
                for pos, players in away_players.items():
                    if isinstance(players, list):
                        print(f"   {pos}: {len(players)} players")
                        if players and len(players) > 0:
                            print(f"      Sample: {players[0].get('name', 'Unknown')}")
                    elif players:
                        print(f"   {pos}: 1 player - {players.get('name', 'Unknown')}")
                    else:
                        print(f"   {pos}: None/Empty")
            
            if 'home_players' in enhanced_player_analysis:
                home_players = enhanced_player_analysis['home_players']
                print(f"\n🏈 Home Players (Wisconsin) Structure:")
                print(f"Keys: {list(home_players.keys())}")
                
                for pos, players in home_players.items():
                    if isinstance(players, list):
                        print(f"   {pos}: {len(players)} players")
                        if players and len(players) > 0:
                            print(f"      Sample: {players[0].get('name', 'Unknown')}")
                    elif players:
                        print(f"   {pos}: 1 player - {players.get('name', 'Unknown')}")
                    else:
                        print(f"   {pos}: None/Empty")
                        
            # Also show the raw JSON structure for frontend debugging
            print(f"\n📄 Raw JSON Structure (first 500 chars):")
            json_str = json.dumps(enhanced_player_analysis, indent=2)[:500]
            print(json_str + "...")
            
        else:
            print("❌ No enhanced player analysis found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_player_structure())