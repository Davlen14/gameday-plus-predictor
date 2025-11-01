#!/usr/bin/env python3
"""Test async prediction with proper player data flow"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from predictor.core.lightning_predictor import LightningPredictor

async def test_player_flow():
    """Test player data flows through prediction"""
    print("=" * 80)
    print("Testing Async Prediction with Player Data")
    print("=" * 80)
    
    # Use the same API key as app.py
    api_key = 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p'
    predictor = LightningPredictor(api_key)
    
    # Georgia Tech ID: 59, Syracuse ID: 183
    print("\n🏈 Predicting Georgia Tech (59) @ Syracuse (183)...")
    prediction = await predictor.predict_game(59, 183)
    
    print("\n" + "=" * 80)
    print("Checking prediction object...")
    print("=" * 80)
    
    print(f"Prediction type: {type(prediction)}")
    print(f"Has detailed_analysis: {hasattr(prediction, 'detailed_analysis')}")
    
    if hasattr(prediction, 'detailed_analysis') and prediction.detailed_analysis:
        print(f"detailed_analysis type: {type(prediction.detailed_analysis)}")
        print(f"detailed_analysis keys: {list(prediction.detailed_analysis.keys())}")
        
        player_analysis = prediction.detailed_analysis.get('player_analysis', {})
        print(f"\nplayer_analysis exists: {bool(player_analysis)}")
        
        if player_analysis:
            print(f"player_analysis type: {type(player_analysis)}")
            print(f"player_analysis keys: {list(player_analysis.keys())}")
            
            home_players = player_analysis.get('home_team_players', {})
            away_players = player_analysis.get('away_team_players', {})
            
            print(f"\n✅ Home team (Syracuse) QBs: {len(home_players.get('qbs', []))}")
            if home_players.get('qbs'):
                print(f"   Top QB: {home_players['qbs'][0].get('player', 'Unknown')}")
            
            print(f"\n✅ Away team (Georgia Tech) QBs: {len(away_players.get('qbs', []))}")
            if away_players.get('qbs'):
                print(f"   Top QB: {away_players['qbs'][0].get('player', 'Unknown')}")
        else:
            print("\n❌ player_analysis is empty!")
            print(f"   Available in detailed_analysis: {list(prediction.detailed_analysis.keys())}")
    else:
        print("\n❌ No detailed_analysis attribute or it's empty")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(test_player_flow())
