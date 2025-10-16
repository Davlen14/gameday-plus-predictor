#!/usr/bin/env python3
"""
Test script for additional games: Ole Miss at Georgia and Tennessee at Alabama
Demonstrates the fixed betting analysis with different market scenarios.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graphqlpredictor import LightningPredictor, GamePrediction, SportsbookLine

def test_ole_miss_at_georgia():
    """Test Ole Miss at Georgia - closer spread scenario"""
    print("🏈 OLE MISS AT GEORGIA")
    print("=" * 50)
    
    # Create prediction - Georgia favored by 6.5
    prediction = GamePrediction(
        home_team="Georgia",
        away_team="Ole Miss",
        home_win_prob=0.72,
        predicted_spread=-6.5,  # Georgia -6.5
        predicted_total=58.5,
        confidence=0.78,
        key_factors=[]
    )
    
    # Market lines - tighter market with some disagreement
    market_lines = [
        {
            'provider': {'name': 'DraftKings'},
            'spread': -4.5,  # Georgia -4.5 (market thinks it's closer)
            'overUnder': 61.0,
            'moneylineHome': -200,
            'moneylineAway': +165
        },
        {
            'provider': {'name': 'FanDuel'},
            'spread': -5.0,  # Georgia -5.0
            'overUnder': 60.5,
            'moneylineHome': -210,
            'moneylineAway': +175
        },
        {
            'provider': {'name': 'Caesars'},
            'spread': -4.0,  # Georgia -4.0 (most generous to Ole Miss)
            'overUnder': 62.0,
            'moneylineHome': -190,
            'moneylineAway': +160
        }
    ]
    
    return run_game_analysis(prediction, market_lines, "Ole Miss at Georgia")

def test_tennessee_at_alabama():
    """Test Tennessee at Alabama - high total, tight spread"""
    print("\n🏈 TENNESSEE AT ALABAMA")
    print("=" * 50)
    
    # Create prediction - Alabama slight home favorite
    prediction = GamePrediction(
        home_team="Alabama",
        away_team="Tennessee", 
        home_win_prob=0.58,
        predicted_spread=-2.5,  # Alabama -2.5 (tight game)
        predicted_total=72.0,   # High-scoring game expected
        confidence=0.65,        # Lower confidence due to tight spread
        key_factors=[]
    )
    
    # Market lines - market sees it as essentially a pick'em
    market_lines = [
        {
            'provider': {'name': 'Bovada'},
            'spread': -1.0,  # Alabama -1.0 (almost pick'em)
            'overUnder': 69.5,
            'moneylineHome': -115,
            'moneylineAway': -105
        },
        {
            'provider': {'name': 'ESPN Bet'},
            'spread': -1.5,  # Alabama -1.5
            'overUnder': 70.0,
            'moneylineHome': -120,
            'moneylineAway': +100
        },
        {
            'provider': {'name': 'BetMGM'},
            'spread': -0.5,  # Alabama -0.5 (basically pick'em)
            'overUnder': 68.5,
            'moneylineHome': -110,
            'moneylineAway': -110
        }
    ]
    
    return run_game_analysis(prediction, market_lines, "Tennessee at Alabama")

def run_game_analysis(prediction, market_lines, game_name):
    """Run betting analysis for a given game"""
    predictor = LightningPredictor("test_api_key")
    
    print(f"📊 MODEL PREDICTION:")
    print(f"   {prediction.home_team} {prediction.predicted_spread:+.1f} (Total {prediction.predicted_total:.1f})")
    print(f"   Win Probability: {prediction.home_win_prob:.1%}")
    print(f"   Confidence: {prediction.confidence:.1%}")
    
    print(f"\n📈 MARKET LINES:")
    for line in market_lines:
        provider = line['provider']['name']
        spread = line['spread']
        total = line['overUnder']
        ml_home = line.get('moneylineHome', 'N/A')
        ml_away = line.get('moneylineAway', 'N/A')
        print(f"   {provider}: {prediction.home_team} {spread:+.1f}, Total {total:.1f}, ML {ml_home}/{ml_away}")
    
    # Run the analysis
    updated_prediction = predictor._validate_against_market(prediction, market_lines)
    
    print(f"\n💰 BETTING ANALYSIS RESULTS:")
    print("-" * 40)
    if hasattr(updated_prediction, 'detailed_analysis') and updated_prediction.detailed_analysis:
        betting_analysis = updated_prediction.detailed_analysis.get('betting_analysis', {})
        if 'formatted_output' in betting_analysis:
            print(betting_analysis['formatted_output'])
            
        # Show additional metrics
        spread_edge = betting_analysis.get('spread_value_edge', 0)
        total_edge = betting_analysis.get('total_value_edge', 0)
        
        print(f"\n📊 KEY METRICS:")
        print(f"   Spread Value Edge: {spread_edge:+.1f} points")
        print(f"   Total Value Edge: {total_edge:+.1f} points")
        print(f"   Best Spread Book: {betting_analysis.get('best_spread_provider', 'N/A')}")
        print(f"   Best Total Book: {betting_analysis.get('best_total_provider', 'N/A')}")
        
        if betting_analysis.get('warnings'):
            print(f"\n⚠️  WARNINGS:")
            for warning in betting_analysis['warnings']:
                print(f"   {warning}")
    
    return updated_prediction

def analyze_betting_scenarios():
    """Analyze different betting scenarios and provide insights"""
    print("\n🎯 COMPREHENSIVE BETTING ANALYSIS")
    print("=" * 60)
    
    # Run both games
    ole_miss_prediction = test_ole_miss_at_georgia()
    tennessee_prediction = test_tennessee_at_alabama()
    
    print(f"\n📈 SCENARIO COMPARISON:")
    print("=" * 40)
    
    # Extract betting analysis for comparison
    ole_miss_analysis = ole_miss_prediction.detailed_analysis.get('betting_analysis', {})
    tennessee_analysis = tennessee_prediction.detailed_analysis.get('betting_analysis', {})
    
    ole_miss_spread_edge = ole_miss_analysis.get('spread_value_edge', 0)
    ole_miss_total_edge = ole_miss_analysis.get('total_value_edge', 0)
    
    tennessee_spread_edge = tennessee_analysis.get('spread_value_edge', 0)
    tennessee_total_edge = tennessee_analysis.get('total_value_edge', 0)
    
    print(f"🏈 Ole Miss @ Georgia:")
    print(f"   Spread Edge: {ole_miss_spread_edge:+.1f} points")
    print(f"   Total Edge: {ole_miss_total_edge:+.1f} points")
    print(f"   Scenario: {'Strong Value' if abs(ole_miss_spread_edge) > 2 else 'Marginal Value'}")
    
    print(f"\n🏈 Tennessee @ Alabama:")
    print(f"   Spread Edge: {tennessee_spread_edge:+.1f} points")
    print(f"   Total Edge: {tennessee_total_edge:+.1f} points")
    print(f"   Scenario: {'Strong Value' if abs(tennessee_spread_edge) > 2 else 'Marginal Value'}")
    
    # Provide betting insights
    print(f"\n💡 BETTING INSIGHTS:")
    print("=" * 30)
    
    if abs(ole_miss_spread_edge) > abs(tennessee_spread_edge):
        print(f"   🎯 Better Spread Value: Ole Miss @ Georgia ({ole_miss_spread_edge:+.1f} vs {tennessee_spread_edge:+.1f})")
    else:
        print(f"   🎯 Better Spread Value: Tennessee @ Alabama ({tennessee_spread_edge:+.1f} vs {ole_miss_spread_edge:+.1f})")
    
    if abs(ole_miss_total_edge) > abs(tennessee_total_edge):
        print(f"   🎯 Better Total Value: Ole Miss @ Georgia ({ole_miss_total_edge:+.1f} vs {tennessee_total_edge:+.1f})")
    else:
        print(f"   🎯 Better Total Value: Tennessee @ Alabama ({tennessee_total_edge:+.1f} vs {ole_miss_total_edge:+.1f})")
    
    # Risk assessment
    ole_miss_risk = "High" if abs(ole_miss_spread_edge) < 1 else "Medium" if abs(ole_miss_spread_edge) < 3 else "Low"
    tennessee_risk = "High" if abs(tennessee_spread_edge) < 1 else "Medium" if abs(tennessee_spread_edge) < 3 else "Low"
    
    print(f"\n⚖️  RISK ASSESSMENT:")
    print(f"   Ole Miss @ Georgia: {ole_miss_risk} Risk")
    print(f"   Tennessee @ Alabama: {tennessee_risk} Risk")
    
    # Portfolio recommendations
    print(f"\n📋 PORTFOLIO RECOMMENDATIONS:")
    
    strong_values = []
    if abs(ole_miss_spread_edge) >= 2:
        direction = "Ole Miss" if ole_miss_spread_edge > 0 else "Georgia"
        strong_values.append(f"Spread: {direction} (Edge: {ole_miss_spread_edge:+.1f})")
    
    if abs(tennessee_spread_edge) >= 2:
        direction = "Tennessee" if tennessee_spread_edge > 0 else "Alabama"
        strong_values.append(f"Spread: {direction} (Edge: {tennessee_spread_edge:+.1f})")
    
    if abs(ole_miss_total_edge) >= 3:
        direction = "OVER" if ole_miss_total_edge > 0 else "UNDER"
        strong_values.append(f"Total: Ole Miss/Georgia {direction} (Edge: {ole_miss_total_edge:+.1f})")
    
    if abs(tennessee_total_edge) >= 3:
        direction = "OVER" if tennessee_total_edge > 0 else "UNDER"
        strong_values.append(f"Total: Tennessee/Alabama {direction} (Edge: {tennessee_total_edge:+.1f})")
    
    if strong_values:
        print(f"   🎯 Strong Value Plays:")
        for value in strong_values:
            print(f"      • {value}")
    else:
        print(f"   ⚠️  No strong value plays detected (edges below thresholds)")
    
    return ole_miss_prediction, tennessee_prediction

if __name__ == "__main__":
    try:
        print("🏈 MULTI-GAME BETTING ANALYSIS TEST")
        print("Testing fixed betting logic with Ole Miss @ Georgia and Tennessee @ Alabama")
        print("=" * 80)
        
        ole_miss_pred, tennessee_pred = analyze_betting_scenarios()
        
        print(f"\n✅ MULTI-GAME ANALYSIS COMPLETE!")
        print(f"   - Ole Miss @ Georgia: Market vs Model analysis complete")
        print(f"   - Tennessee @ Alabama: Market vs Model analysis complete")
        print(f"   - Betting recommendations generated for both games")
        print(f"   - Risk assessment and portfolio recommendations provided")
        
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)