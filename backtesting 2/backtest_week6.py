#!/usr/bin/env python3
"""
Simple backtesting script for Week 6 (Oct 5-12, 2025)
Tests your predictor against games that already happened
"""

import asyncio
from graphqlpredictor import LightningPredictor
import json

# Week 6 games that already happened (Oct 5-12, 2025)
WEEK_6_GAMES = [
    # Format: (home_team_id, away_team_id, actual_home_score, actual_away_score, home_team_name, away_team_name)
    # Add real games from Week 6 here - you can get team IDs from fbs.json
    # Example format:
    # (61, 194, 31, 24, "Georgia", "Auburn"),  # Georgia won 31-24 at home
]

async def backtest_week_6():
    """Run predictions on Week 6 games and compare to actual results"""
    predictor = LightningPredictor(week=6)
    
    results = {
        'correct_winners': 0,
        'total_games': 0,
        'spread_errors': [],
        'total_errors': [],
        'win_prob_accuracy': []
    }
    
    print("="*80)
    print("🔮 BACKTESTING WEEK 6 PREDICTIONS")
    print("="*80)
    
    for home_id, away_id, actual_home, actual_away, home_name, away_name in WEEK_6_GAMES:
        print(f"\n📊 Testing: {away_name} @ {home_name}")
        print(f"   Actual Result: {home_name} {actual_home}, {away_name} {actual_away}")
        
        try:
            # Run your prediction
            prediction = await predictor.predict_game(home_id, away_id)
            
            # Extract predictions
            pred_spread = prediction.predicted_spread
            pred_total = prediction.predicted_total
            home_win_prob = prediction.home_win_prob
            
            # Calculate actuals
            actual_spread = actual_home - actual_away  # Positive = home won
            actual_total = actual_home + actual_away
            actual_home_won = actual_home > actual_away
            
            # Check winner prediction
            predicted_home_win = home_win_prob > 0.5
            correct_winner = (predicted_home_win == actual_home_won)
            
            if correct_winner:
                results['correct_winners'] += 1
            
            # Calculate errors
            spread_error = abs(pred_spread - (-actual_spread))  # Your spread is from away perspective
            total_error = abs(pred_total - actual_total)
            
            results['spread_errors'].append(spread_error)
            results['total_errors'].append(total_error)
            results['total_games'] += 1
            
            # Win probability accuracy (Brier score component)
            if actual_home_won:
                prob_error = (1 - home_win_prob) ** 2
            else:
                prob_error = home_win_prob ** 2
            results['win_prob_accuracy'].append(prob_error)
            
            # Display results
            print(f"   Prediction: {home_name} {pred_spread:+.1f}")
            print(f"   Win Prob: {home_win_prob:.1%}")
            print(f"   Total: {pred_total:.1f}")
            print(f"   ")
            print(f"   ✅ Winner: {'CORRECT' if correct_winner else '❌ WRONG'}")
            print(f"   Spread Error: {spread_error:.1f} points")
            print(f"   Total Error: {total_error:.1f} points")
            
        except Exception as e:
            print(f"   ❌ Error running prediction: {e}")
            continue
    
    # Calculate summary statistics
    print("\n" + "="*80)
    print("📈 BACKTEST RESULTS SUMMARY")
    print("="*80)
    
    if results['total_games'] > 0:
        win_pct = (results['correct_winners'] / results['total_games']) * 100
        avg_spread_error = sum(results['spread_errors']) / len(results['spread_errors'])
        avg_total_error = sum(results['total_errors']) / len(results['total_errors'])
        brier_score = sum(results['win_prob_accuracy']) / len(results['win_prob_accuracy'])
        
        print(f"Games Tested: {results['total_games']}")
        print(f"")
        print(f"🎯 Winner Accuracy: {results['correct_winners']}/{results['total_games']} ({win_pct:.1f}%)")
        print(f"   Target: >52.4% to beat betting market")
        print(f"   ")
        print(f"📊 Average Spread Error: {avg_spread_error:.2f} points")
        print(f"   (Lower is better, <7 is good)")
        print(f"   ")
        print(f"📈 Average Total Error: {avg_total_error:.2f} points")
        print(f"   (Lower is better, <10 is good)")
        print(f"   ")
        print(f"🎲 Brier Score: {brier_score:.4f}")
        print(f"   (Lower is better, <0.20 is excellent)")
        print(f"   ")
        
        # Grade the model
        print("\n🏆 MODEL GRADE:")
        if win_pct >= 60:
            print("   🌟🌟🌟 ELITE (Vegas level)")
        elif win_pct >= 55:
            print("   🌟🌟 EXCELLENT (Profitable)")
        elif win_pct >= 52.4:
            print("   🌟 GOOD (Beats break-even)")
        else:
            print("   ⚠️  NEEDS IMPROVEMENT")
    else:
        print("⚠️  No games to test! Add Week 6 games to WEEK_6_GAMES list.")
        print("\nTo add games:")
        print("1. Check your fbs.json for team IDs")
        print("2. Look up actual scores from Week 6")
        print("3. Add to WEEK_6_GAMES list at top of this file")
    
    print("="*80)
    
    return results

if __name__ == "__main__":
    print("\n🏈 College Football Predictor - Week 6 Backtest\n")
    asyncio.run(backtest_week_6())
