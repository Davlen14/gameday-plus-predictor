#!/usr/bin/env python3
"""
Test the Ole Miss vs Washington State game - the exact matchup from the research paper!
This is the game with a 24-point model vs market discrepancy that the framework analyzed.
"""

import asyncio
from graphqlpredictor import LightningPredictor

async def main():
    # API Key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    # Initialize predictor
    predictor = LightningPredictor(api_key)
    
    print("=" * 80)
    print("🎓 RESEARCH PAPER TEST CASE")
    print("=" * 80)
    print("\n📚 Framework Analysis:")
    print("   - Market Line: Ole Miss -32.5")
    print("   - Old Model: Likely predicted ~8-10 point spread")
    print("   - Discrepancy: ~24 points")
    print("\n🔬 Key Issues Identified:")
    print("   - Ole Miss SoS: 16th (SEC) | Wazzu SoS: 78th")
    print("   - Market consensus severely underweighted (5%)")
    print("   - Opponent adjustment insufficient")
    print("   - Player impact (missing Ole Miss transfers) undervalued")
    print("\n✅ NEW MODEL SHOULD:")
    print("   - Weight market consensus properly (20%)")
    print("   - Apply rigorous SoS adjustment (50% component)")
    print("   - Account for player impact (10%)")
    print("\n" + "=" * 80)
    
    # Ole Miss ID: 145
    # Washington State ID: 265
    
    home_team_id = 145  # Ole Miss
    away_team_id = 265  # Washington State
    
    print("\n🏈 PREDICTING: Washington State @ Ole Miss (Week 7)")
    print("=" * 80 + "\n")
    
    try:
        # Run prediction
        prediction = await predictor.predict_game(home_team_id, away_team_id)
        
        print("\n" + "=" * 80)
        print("🏆 OPTIMIZED MODEL RESULTS vs MARKET")
        print("=" * 80)
        print(f"\n📊 Matchup: {prediction.away_team} @ {prediction.home_team}")
        
        print(f"\n💰 MARKET LINE:")
        print(f"   Spread: Ole Miss -32.5")
        print(f"   This means: Ole Miss favored by 32.5 points")
        
        print(f"\n🤖 OPTIMIZED MODEL PREDICTION:")
        print(f"   Spread: {prediction.home_team} {prediction.predicted_spread:+.1f}")
        if prediction.predicted_spread < 0:
            print(f"   This means: {prediction.home_team} favored by {abs(prediction.predicted_spread):.1f} points")
        else:
            print(f"   This means: {prediction.away_team} favored by {prediction.predicted_spread:.1f} points")
        
        # Calculate discrepancy
        market_spread = -32.5  # Ole Miss -32.5
        model_spread = prediction.predicted_spread
        discrepancy = abs(market_spread - model_spread)
        
        print(f"\n📊 DISCREPANCY ANALYSIS:")
        print(f"   Market: Ole Miss -{32.5}")
        print(f"   Model: Ole Miss -{abs(model_spread):.1f}" if model_spread < 0 else f"   Model: Washington State -{model_spread:.1f}")
        print(f"   Difference: {discrepancy:.1f} points")
        
        if discrepancy < 5:
            print(f"   ✅ EXCELLENT! Model closely matches market (within 5 points)")
            print(f"   🎯 This indicates proper weighting of market consensus")
        elif discrepancy < 10:
            print(f"   ✅ GOOD! Model reasonably close to market")
            print(f"   🎯 Small disagreement - model may have edge")
        elif discrepancy < 15:
            print(f"   ⚠️  MODERATE disagreement with market")
            print(f"   🔍 Model sees different factors than market")
        else:
            print(f"   ⚠️  SIGNIFICANT disagreement with market ({discrepancy:.1f} points)")
            print(f"   🚨 Large discrepancy - review needed")
        
        print(f"\n🎯 Win Probability:")
        print(f"   {prediction.home_team}: {prediction.home_win_prob:.1%}")
        print(f"   {prediction.away_team}: {(1 - prediction.home_win_prob):.1%}")
        
        print(f"\n🎯 Total: {prediction.predicted_total:.1f} points")
        print(f"\n💪 Model Confidence: {prediction.confidence:.1%}")
        
        print(f"\n🔑 Key Factors Identified:")
        for i, factor in enumerate(prediction.key_factors, 1):
            print(f"   {i}. {factor}")
        
        print("\n" + "=" * 80)
        print("📚 FRAMEWORK VALIDATION")
        print("=" * 80)
        print("\n✅ Improvements Applied:")
        print("   1. Market Consensus: 5% → 20% (4x increase)")
        print("   2. Opponent-Adjusted Metrics: 50% (with SoS)")
        print("   3. Key Player Impact: 3% → 10% (3x increase)")
        print("   4. Dixon-Coles temporal weighting")
        print("   5. Platt Scaling calibration")
        
        print(f"\n🎯 Expected Outcome:")
        if discrepancy < 10:
            print("   ✅ Model properly weighs market consensus")
            print("   ✅ Should be more accurate than old 24-point discrepancy")
        else:
            print("   ⚠️  Model still finding significant inefficiency")
            print("   💡 Could indicate genuine edge or data limitations")
        
        print("\n" + "=" * 80)
        print("✅ Analysis Complete!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
