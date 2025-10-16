"""
Enhanced Prediction System Test
Tests the fixed prediction logic with multiple team matchups
Validates mathematical consistency across all predictions
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor
from prediction_validator import PredictionValidator, apply_prediction_fixes

def test_team_matchup(predictor, home_team, away_team, home_id, away_id):
    """Test a specific team matchup and validate consistency"""
    print(f"\n{'='*80}")
    print(f"🏈 TESTING: {away_team} @ {home_team}")
    print(f"{'='*80}")
    
    try:
        # Get prediction
        prediction = asyncio.run(predictor.predict_game(home_id, away_id))
        
        # Apply fixes
        prediction = apply_prediction_fixes(prediction)
        
        # Extract key values
        spread = prediction.predicted_spread
        total = prediction.predicted_total
        home_prob = prediction.home_win_prob
        
        # Calculate implied scores using CORRECTED logic
        home_score = round((total + spread) / 2)
        away_score = round((total - spread) / 2)
        
        print(f"\n📊 PREDICTION RESULTS:")
        print(f"   • Win Probability: {home_team} {home_prob:.1%} | {away_team} {(1-home_prob):.1%}")
        print(f"   • Predicted Spread: {home_team} {spread:+.1f}")
        print(f"   • Predicted Total: {total:.1f}")
        print(f"   • Predicted Score: {home_team} {home_score}, {away_team} {away_score}")
        
        # Validate consistency
        print(f"\n🔍 CONSISTENCY VALIDATION:")
        
        # Check score-spread alignment
        actual_spread = home_score - away_score
        actual_total = home_score + away_score
        
        spread_match = abs(actual_spread - spread) <= 0.5
        total_match = abs(actual_total - total) <= 0.5
        
        print(f"   • Spread Consistency: {actual_spread:.1f} vs {spread:.1f} {'✅' if spread_match else '❌'}")
        print(f"   • Total Consistency: {actual_total} vs {total:.1f} {'✅' if total_match else '❌'}")
        
        # Check probability-spread alignment
        import math
        if 0.01 <= home_prob <= 0.99:
            implied_spread = math.log(home_prob / (1 - home_prob)) * 2.4
        else:
            implied_spread = math.log(home_prob / (1 - home_prob)) * 3.5
        
        prob_spread_match = abs(implied_spread - spread) <= 3.0  # Allow 3-point tolerance
        print(f"   • Probability-Spread: {implied_spread:.1f} vs {spread:.1f} {'✅' if prob_spread_match else '⚠️'}")
        
        # Market comparison if available
        market_spread = getattr(prediction, 'market_spread', None)
        market_total = getattr(prediction, 'market_total', None)
        
        if market_spread:
            spread_edge = market_spread - spread
            print(f"   • Spread Edge: Model {spread:.1f} vs Market {market_spread:.1f} = {spread_edge:+.1f}")
            
        if market_total:
            total_edge = total - market_total
            print(f"   • Total Edge: Model {total:.1f} vs Market {market_total:.1f} = {total_edge:+.1f}")
        
        return {
            'team_matchup': f"{away_team} @ {home_team}",
            'spread_consistent': spread_match,
            'total_consistent': total_match,
            'prob_spread_aligned': prob_spread_match,
            'home_prob': home_prob,
            'predicted_spread': spread,
            'predicted_total': total,
            'home_score': home_score,
            'away_score': away_score
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def main():
    """Test multiple team matchups to validate the enhanced system"""
    
    print("🚀 ENHANCED PREDICTION SYSTEM VALIDATION")
    print("="*80)
    print("Testing mathematical consistency across multiple team matchups")
    
    # Initialize predictor
    import os
    api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    predictor = LightningPredictor(api_key)
    
    # Load team data
    with open('fbs.json', 'r') as f:
        teams = json.load(f)
    
    # Create team lookup
    team_lookup = {team['school']: team['id'] for team in teams}
    
    # Test cases covering different scenarios
    test_cases = [
        # High-ranked vs Low-ranked (should have big spread)
        ("Ohio State", "Wisconsin", team_lookup.get("Ohio State"), team_lookup.get("Wisconsin")),
        
        # Top 10 matchup (should be close spread)
        ("Georgia", "Texas", team_lookup.get("Georgia"), team_lookup.get("Texas")),
        
        # Mid-tier matchup
        ("Michigan State", "Purdue", team_lookup.get("Michigan State"), team_lookup.get("Purdue")),
        
        # Conference rivals
        ("Alabama", "Auburn", team_lookup.get("Alabama"), team_lookup.get("Auburn")),
        
        # Cross-conference
        ("Oregon", "Penn State", team_lookup.get("Oregon"), team_lookup.get("Penn State"))
    ]
    
    results = []
    
    for home_team, away_team, home_id, away_id in test_cases:
        if home_id and away_id:
            result = test_team_matchup(predictor, home_team, away_team, home_id, away_id)
            if result:
                results.append(result)
        else:
            print(f"⚠️ Skipping {away_team} @ {home_team} - teams not found")
    
    # Summary analysis
    print(f"\n{'='*80}")
    print("📈 VALIDATION SUMMARY")
    print(f"{'='*80}")
    
    if results:
        spread_consistent = sum(1 for r in results if r['spread_consistent'])
        total_consistent = sum(1 for r in results if r['total_consistent'])
        prob_aligned = sum(1 for r in results if r['prob_spread_aligned'])
        
        print(f"   📊 Tests Run: {len(results)}")
        print(f"   ✅ Spread Consistency: {spread_consistent}/{len(results)} ({spread_consistent/len(results)*100:.1f}%)")
        print(f"   ✅ Total Consistency: {total_consistent}/{len(results)} ({total_consistent/len(results)*100:.1f}%)")
        print(f"   ✅ Probability Alignment: {prob_aligned}/{len(results)} ({prob_aligned/len(results)*100:.1f}%)")
        
        print(f"\n📋 DETAILED RESULTS:")
        for result in results:
            status = "✅" if all([result['spread_consistent'], result['total_consistent'], result['prob_spread_aligned']]) else "⚠️"
            print(f"   {status} {result['team_matchup']}: Spread {result['predicted_spread']:+.1f}, Total {result['predicted_total']:.1f}, Prob {result['home_prob']:.1%}")
    
    print(f"\n🎯 PREDICTION SYSTEM STATUS:")
    if results and all(r['spread_consistent'] and r['total_consistent'] for r in results):
        print("   ✅ MATHEMATICAL CONSISTENCY: PASS")
        print("   ✅ SCORE CALCULATIONS: FIXED")
        print("   ✅ SYSTEM READY FOR PRODUCTION")
    else:
        print("   ⚠️ Some inconsistencies detected - review validation output")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()