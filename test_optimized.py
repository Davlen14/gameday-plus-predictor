#!/usr/bin/env python3
"""
Quick test of the optimized predictor with new weights
"""

import asyncio
from graphqlpredictor import LightningPredictor

async def main():
    # API Key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    # Initialize predictor
    predictor = LightningPredictor(api_key)
    
    print("=" * 80)
    print("🚀 OPTIMIZED COLLEGE FOOTBALL PREDICTOR - v2.0")
    print("=" * 80)
    print("\n📊 NEW FEATURES:")
    print("   ✅ Optimal Research-Based Weights")
    print("   ✅ Dixon-Coles Temporal Weighting")
    print("   ✅ Platt Scaling Probability Calibration")
    print("   ✅ Market Consensus: 5% → 20% (4x increase!)")
    print("   ✅ Key Player Impact: 3% → 10% (3x increase!)")
    print("\n" + "=" * 80)
    
    # Test game: Illinois (Fighting Illini) vs Ohio State (Buckeyes)
    # Illinois ID: 356
    # Ohio State ID: 194
    
    home_team_id = 356  # Illinois
    away_team_id = 194  # Ohio State
    
    print("\n🏈 PREDICTING: Ohio State @ Illinois (Week 7)")
    print("=" * 80 + "\n")
    
    try:
        # Run prediction
        prediction = await predictor.predict_game(home_team_id, away_team_id)
        
        print("\n" + "=" * 80)
        print("🏆 FINAL RESULTS")
        print("=" * 80)
        print(f"\n📊 Matchup: {prediction.away_team} @ {prediction.home_team}")
        print(f"\n🎯 Win Probability:")
        print(f"   {prediction.home_team}: {prediction.home_win_prob:.1%}")
        print(f"   {prediction.away_team}: {(1 - prediction.home_win_prob):.1%}")
        print(f"\n📈 Spread: {prediction.home_team} {prediction.predicted_spread:+.1f}")
        print(f"   (If negative, {prediction.home_team} is favored)")
        print(f"\n🎯 Total: {prediction.predicted_total:.1f} points")
        print(f"\n💪 Confidence: {prediction.confidence:.1%}")
        
        print(f"\n🔑 Key Factors:")
        for i, factor in enumerate(prediction.key_factors, 1):
            print(f"   {i}. {factor}")
        
        print("\n" + "=" * 80)
        print("✅ Prediction Complete!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
