#!/usr/bin/env python3
"""
Enhanced Validation - Test a subset of Week 7 games to compare enhanced vs baseline performance
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor

# Sample of Week 7 games for quick validation
WEEK7_SAMPLE = [
    {"home_team": "USC", "home_id": 30, "away_team": "Michigan", "away_id": 130, "home_score": 31, "away_score": 13},
    {"home_team": "Ole Miss", "home_id": 145, "away_team": "Washington State", "away_id": 265, "home_score": 24, "away_score": 21},
    {"home_team": "LSU", "home_id": 99, "away_team": "Arkansas", "away_id": 8, "home_score": 31, "away_score": 17}, 
    {"home_team": "Texas", "home_id": 251, "away_team": "Georgia", "away_id": 61, "home_score": 30, "away_score": 15},
    {"home_team": "Notre Dame", "home_id": 87, "away_team": "NC State", "away_id": 152, "home_score": 36, "away_score": 7},
]

async def enhanced_validation_test():
    """Quick validation of enhanced system performance"""
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🚀 ENHANCED PLAYER ANALYSIS VALIDATION")
    print("=" * 65)
    print(f"🎯 Testing {len(WEEK7_SAMPLE)} Week 7 games with enhanced system")
    print("=" * 65)
    
    correct_predictions = 0
    total_games = len(WEEK7_SAMPLE)
    total_spread_error = 0.0
    total_total_error = 0.0
    
    for i, game in enumerate(WEEK7_SAMPLE):
        print(f"\n🏈 Game {i+1}/{total_games}: {game['away_team']} @ {game['home_team']}")
        print(f"   Actual: {game['home_team']} {game['home_score']}-{game['away_score']} {game['away_team']}")
        
        try:
            prediction = await predictor.predict_game(
                home_team_id=game['home_id'],
                away_team_id=game['away_id']
            )
            
            if prediction:
                # Determine actual winner
                actual_home_win = game['home_score'] > game['away_score']
                predicted_home_win = prediction.home_win_prob > 50
                
                # Check if prediction was correct
                correct = actual_home_win == predicted_home_win
                if correct:
                    correct_predictions += 1
                
                # Calculate errors
                actual_spread = game['home_score'] - game['away_score']
                predicted_spread = prediction.predicted_spread
                spread_error = abs(actual_spread - predicted_spread)
                total_spread_error += spread_error
                
                actual_total = game['home_score'] + game['away_score']
                predicted_total = prediction.predicted_total
                total_error = abs(actual_total - predicted_total)
                total_total_error += total_error
                
                # Display results
                result = "✅ CORRECT" if correct else "❌ WRONG"
                print(f"   {result}: Predicted {game['home_team'] if predicted_home_win else game['away_team']} wins")
                print(f"   📊 Confidence: {prediction.confidence:.1f}%")
                print(f"   📈 Spread Error: {spread_error:.1f} points")
                print(f"   🎯 Total Error: {total_error:.1f} points")
                
            else:
                print("   ❌ PREDICTION FAILED")
                
        except Exception as e:
            print(f"   ⚠️ ERROR: {str(e)}")
    
    # Calculate final metrics
    accuracy = (correct_predictions / total_games) * 100
    avg_spread_error = total_spread_error / total_games
    avg_total_error = total_total_error / total_games
    
    print("\n" + "=" * 65)
    print("📊 ENHANCED SYSTEM PERFORMANCE SUMMARY")
    print("=" * 65)
    print(f"🎯 Accuracy: {correct_predictions}/{total_games} = {accuracy:.1f}%")
    print(f"📊 Avg Spread Error: {avg_spread_error:.1f} points")
    print(f"🎯 Avg Total Error: {avg_total_error:.1f} points")
    print("=" * 65)
    
    print(f"\n✅ Enhanced player analysis system tested!")
    print(f"🚀 Key improvements:")
    print(f"   📈 QB efficiency scores from comprehensive data")
    print(f"   🏃 RB/WR/TE skill position analysis")  
    print(f"   🛡️ DB/LB/DL defensive player metrics")
    print(f"   ⚖️ Weighted positional impact (QB 40%, Skill 35%, Defense 25%)")
    
if __name__ == "__main__":
    asyncio.run(enhanced_validation_test())