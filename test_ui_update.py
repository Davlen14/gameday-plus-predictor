#!/usr/bin/env python3
"""
Test the updated KeyPlayerImpact component with all positions
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor

async def test_full_prediction():
    """Test a full prediction to see all player positions"""
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🏈 Testing Full Prediction with All Player Positions")
    print("=" * 60)
    
    # Test with Ohio State vs Illinois 
    home_team_id = 356  # Illinois
    away_team_id = 194  # Ohio State
    
    print(f"🎯 Predicting: Ohio State @ Illinois")
    
    try:
        prediction = await predictor.predict_game(home_team_id, away_team_id)
        
        if prediction and hasattr(prediction, 'detailed_analysis'):
            player_analysis = prediction.detailed_analysis.get('enhanced_player_analysis', {})
            
            print(f"\n📊 Player Analysis Found:")
            print(f"   Away Players (Ohio State): {len(player_analysis.get('away_players', {}))}")
            print(f"   Home Players (Illinois): {len(player_analysis.get('home_players', {}))}")
            
            # Show what positions we have data for
            away_players = player_analysis.get('away_players', {})
            home_players = player_analysis.get('home_players', {})
            
            print(f"\n🏈 Ohio State Roster:")
            for position, players in away_players.items():
                if isinstance(players, list):
                    print(f"   {position.upper()}: {len(players)} players")
                elif players:
                    print(f"   {position.upper()}: 1 player")
                else:
                    print(f"   {position.upper()}: 0 players")
            
            print(f"\n🏈 Illinois Roster:")
            for position, players in home_players.items():
                if isinstance(players, list):
                    print(f"   {position.upper()}: {len(players)} players")
                elif players:
                    print(f"   {position.upper()}: 1 player")
                else:
                    print(f"   {position.upper()}: 0 players")
            
            # Calculate total players for UI display
            osu_total = 0
            ill_total = 0
            
            for pos, players in away_players.items():
                if isinstance(players, list):
                    osu_total += len(players)
                elif players:
                    osu_total += 1
                    
            for pos, players in home_players.items():
                if isinstance(players, list):
                    ill_total += len(players)
                elif players:
                    ill_total += 1
            
            print(f"\n📊 UI Display Totals:")
            print(f"   Ohio State: {osu_total} total players")
            print(f"   Illinois: {ill_total} total players")
            
            print(f"\n✅ Prediction completed successfully!")
            print(f"   Winner: {prediction.predicted_winner}")
            print(f"   Confidence: {prediction.confidence:.1%}")
            
        else:
            print("❌ No detailed player analysis found in prediction")
            
    except Exception as e:
        print(f"❌ Error running prediction: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_prediction())