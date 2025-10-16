#!/usr/bin/env python3
"""
Test script to validate the fixed betting analysis logic in the main predictor.
Tests the Wisconsin vs Ohio State example to ensure correct outputs.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graphqlpredictor import LightningPredictor, GamePrediction, SportsbookLine

def test_wisconsin_ohio_state_integration():
    """Test the Wisconsin vs Ohio State example using the integrated predictor"""
    print("🏈 TESTING WISCONSIN vs OHIO STATE WITH INTEGRATED PREDICTOR")
    print("=" * 60)
    
    # Create a mock prediction that matches the example
    prediction = GamePrediction(
        home_team="Ohio State",
        away_team="Wisconsin", 
        home_win_prob=0.95,
        predicted_spread=-15.6,  # Ohio State -15.6 (home team giving 15.6)
        predicted_total=65.9,
        confidence=0.85,
        key_factors=[]
    )
    
    # Mock market lines data (as would come from GraphQL API)
    market_lines = [
        {
            'provider': {'name': 'Bovada'},
            'spread': -26.0,  # Ohio State -26
            'overUnder': 41.0,
            'moneylineHome': -2500,  # Ohio State heavily favored
            'moneylineAway': +1100   # Wisconsin big underdog
        },
        {
            'provider': {'name': 'ESPN Bet'},
            'spread': -24.5,  # Ohio State -24.5
            'overUnder': 42.5,
            'moneylineHome': -2200,
            'moneylineAway': +1050
        },
        {
            'provider': {'name': 'DraftKings'},
            'spread': -25.5,  # Ohio State -25.5
            'overUnder': 41.5,
            'moneylineHome': -2300,
            'moneylineAway': +1080
        }
    ]
    
    # Create predictor instance and test the fixed betting analysis
    predictor = LightningPredictor("test_api_key")  # Use dummy API key for testing
    
    print("📊 ORIGINAL PREDICTION:")
    print(f"   Model: {prediction.home_team} {prediction.predicted_spread:+.1f} (Total {prediction.predicted_total:.1f})")
    print(f"   Confidence: {prediction.confidence:.1%}")
    
    print(f"\n📈 MARKET LINES INPUT:")
    for line in market_lines:
        provider = line['provider']['name']
        spread = line['spread']
        total = line['overUnder']
        print(f"   {provider}: {prediction.home_team} {spread:+.1f}, Total {total:.1f}")
    
    # Run the fixed betting analysis
    updated_prediction = predictor._validate_against_market(prediction, market_lines)
    
    print(f"\n✅ FIXED ANALYSIS RESULTS:")
    print("=" * 40)
    if hasattr(updated_prediction, 'detailed_analysis') and updated_prediction.detailed_analysis:
        betting_analysis = updated_prediction.detailed_analysis.get('betting_analysis', {})
        if 'formatted_output' in betting_analysis:
            print(betting_analysis['formatted_output'])
        
        if 'warnings' in betting_analysis and betting_analysis['warnings']:
            print(f"\n⚠️  WARNINGS:")
            for warning in betting_analysis['warnings']:
                print(f"   {warning}")
    else:
        print("❌ No detailed betting analysis found")
    
    print(f"\n📋 PREDICTION UPDATES:")
    print(f"   Market Spread: {updated_prediction.market_spread:+.1f}")
    print(f"   Market Total: {updated_prediction.market_total:.1f}")
    print(f"   Spread Edge: {updated_prediction.spread_edge:.1f}")
    print(f"   Total Edge: {updated_prediction.total_edge:.1f}")
    print(f"   Spread Pick: {updated_prediction.value_spread_pick}")
    print(f"   Total Pick: {updated_prediction.value_total_pick}")
    print(f"   Updated Confidence: {updated_prediction.confidence:.1%}")
    
    return updated_prediction

def test_validation_results():
    """Validate that our results match the expected outputs from requirements"""
    print(f"\n🔍 VALIDATION AGAINST REQUIREMENTS:")
    print("=" * 40)
    
    expected_results = {
        'spread_value_edge': 9.9,  # Market +25.5 - Model +15.6
        'total_value_edge': 24.2,  # Model 65.9 - Market 41.7 (consensus)
        'best_spread_provider': 'Bovada',  # Highest points for Wisconsin
        'best_total_provider': 'Bovada',   # Lowest total for OVER bet
        'spread_recommendation_contains': 'Wisconsin +26.0 @ Bovada',
        'total_recommendation_contains': 'OVER 41.0 @ Bovada',
        'extreme_total_warning': True  # Should warn about >12 point discrepancy
    }
    
    prediction = test_wisconsin_ohio_state_integration()
    
    if hasattr(prediction, 'detailed_analysis') and prediction.detailed_analysis:
        betting_analysis = prediction.detailed_analysis.get('betting_analysis', {})
        
        # Check spread edge (within tolerance)
        actual_spread_edge = betting_analysis.get('spread_value_edge', 0)
        spread_edge_ok = abs(actual_spread_edge - expected_results['spread_value_edge']) < 1.0
        print(f"   ✅ Spread Edge: {actual_spread_edge:+.1f} (expected ~{expected_results['spread_value_edge']:+.1f}) {'✓' if spread_edge_ok else '✗'}")
        
        # Check total edge (within tolerance)
        actual_total_edge = betting_analysis.get('total_value_edge', 0)
        total_edge_ok = abs(actual_total_edge - expected_results['total_value_edge']) < 2.0
        print(f"   ✅ Total Edge: {actual_total_edge:+.1f} (expected ~{expected_results['total_value_edge']:+.1f}) {'✓' if total_edge_ok else '✗'}")
        
        # Check best providers
        spread_provider_ok = betting_analysis.get('best_spread_provider') == expected_results['best_spread_provider']
        total_provider_ok = betting_analysis.get('best_total_provider') == expected_results['best_total_provider']
        print(f"   ✅ Best Spread Provider: {betting_analysis.get('best_spread_provider')} {'✓' if spread_provider_ok else '✗'}")
        print(f"   ✅ Best Total Provider: {betting_analysis.get('best_total_provider')} {'✓' if total_provider_ok else '✗'}")
        
        # Check recommendations
        formatted_output = betting_analysis.get('formatted_output', '')
        spread_rec_ok = expected_results['spread_recommendation_contains'] in formatted_output
        total_rec_ok = expected_results['total_recommendation_contains'] in formatted_output
        print(f"   ✅ Spread Recommendation: {'✓' if spread_rec_ok else '✗'}")
        print(f"   ✅ Total Recommendation: {'✓' if total_rec_ok else '✗'}")
        
        # Check extreme discrepancy warning
        warnings = betting_analysis.get('warnings', [])
        extreme_warning_ok = any('Extreme total discrepancy' in warning for warning in warnings)
        print(f"   ✅ Extreme Total Warning: {'✓' if extreme_warning_ok else '✗'}")
        
        # Overall validation
        all_checks = [spread_edge_ok, total_edge_ok, spread_provider_ok, total_provider_ok, 
                     spread_rec_ok, total_rec_ok, extreme_warning_ok]
        if all(all_checks):
            print(f"\n🎉 ALL VALIDATION CHECKS PASSED!")
            return True
        else:
            print(f"\n❌ Some validation checks failed")
            return False
    else:
        print(f"❌ No betting analysis data found")
        return False

if __name__ == "__main__":
    try:
        validation_passed = test_validation_results()
        exit_code = 0 if validation_passed else 1
        print(f"\n{'🎯 TESTING COMPLETE - ALL FIXES WORKING!' if validation_passed else '❌ TESTING FAILED - FIXES NEED ADJUSTMENT'}")
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)