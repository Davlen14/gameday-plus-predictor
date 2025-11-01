#!/usr/bin/env python3
"""Test player data integration in prediction pipeline"""

import sys
import os

# Add the project root to path
sys.path.insert(0, os.path.dirname(__file__))

from predictor.core.lightning_predictor import LightningPredictor

def test_player_data_flow():
    """Test that player data flows from PlayerAnalyzer to prediction output"""
    print("=" * 80)
    print("Testing Player Data Integration")
    print("=" * 80)
    
    # Initialize predictor
    predictor = LightningPredictor()
    
    # Make a prediction
    print("\n🏈 Testing with Syracuse vs Georgia Tech...")
    prediction = predictor.predict_game("Syracuse", "Georgia Tech")
    
    # Check if player_analysis exists in detailed_analysis
    print("\n" + "=" * 80)
    print("Checking prediction.detailed_analysis...")
    print("=" * 80)
    
    if hasattr(prediction, 'detailed_analysis'):
        player_analysis = prediction.detailed_analysis.get('player_analysis', {})
        
        if player_analysis:
            print("✅ SUCCESS: player_analysis found in prediction!")
            
            # Check home team players
            home_players = player_analysis.get('home_team_players', {})
            away_players = player_analysis.get('away_team_players', {})
            
            print(f"\n📊 Home Team (Syracuse) Players:")
            print(f"   QBs: {len(home_players.get('qbs', []))}")
            print(f"   WRs: {len(home_players.get('wrs', []))}")
            print(f"   RBs: {len(home_players.get('rbs', []))}")
            
            if home_players.get('qbs'):
                print(f"\n   Top QB: {home_players['qbs'][0].get('player', 'Unknown')}")
            
            print(f"\n📊 Away Team (Georgia Tech) Players:")
            print(f"   QBs: {len(away_players.get('qbs', []))}")
            print(f"   WRs: {len(away_players.get('wrs', []))}")
            print(f"   RBs: {len(away_players.get('rbs', []))}")
            
            if away_players.get('qbs'):
                print(f"\n   Top QB: {away_players['qbs'][0].get('player', 'Unknown')}")
            
            # Check player differential
            player_diff = player_analysis.get('player_differential', {})
            if player_diff:
                print(f"\n📈 Player Differentials:")
                print(f"   QB: {player_diff.get('qb_differential', 0.0):+.3f}")
                print(f"   WR: {player_diff.get('wr_differential', 0.0):+.3f}")
                print(f"   RB: {player_diff.get('rb_differential', 0.0):+.3f}")
                print(f"   Total: {player_diff.get('total_impact', 0.0):+.3f}")
        else:
            print("❌ ERROR: player_analysis is empty in prediction.detailed_analysis")
            print(f"   Available keys: {list(prediction.detailed_analysis.keys())}")
    else:
        print("❌ ERROR: prediction has no detailed_analysis attribute")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_player_data_flow()
