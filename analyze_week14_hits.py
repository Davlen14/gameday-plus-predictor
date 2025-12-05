#!/usr/bin/env python3
"""
Analyze Week 14 predictions vs actual results
Determines which games we hit (correctly predicted the spread)
"""
import json
from datetime import datetime

def load_predictions():
    """Load prediction data"""
    with open('week14_game_summaries_20251129_203941.json', 'r') as f:
        return json.load(f)

def load_actual_scores():
    """Load actual game scores"""
    with open('week14_2025_scores.json', 'r') as f:
        return json.load(f)

def normalize_team_name(name):
    """Normalize team names for matching"""
    # Handle common variations
    mappings = {
        'Miami': 'Miami (FL)',
        'Miami (OH)': 'Miami (Ohio)',
        'App State': 'Appalachian State',
        'UL Monroe': 'ULM',
        'San José State': 'San Jose State',
        'Hawai\'i': 'Hawaii',
    }
    
    normalized = mappings.get(name, name)
    
    # Check if name contains the normalized version
    return normalized.lower().strip()

def find_actual_game(predictions_game, actual_games):
    """Find matching actual game for a prediction"""
    pred_away = normalize_team_name(predictions_game['away_team'])
    pred_home = normalize_team_name(predictions_game['home_team'])
    
    for game in actual_games:
        actual_away = normalize_team_name(game['away_team']['name'].split()[-1])  # Get mascot/main name
        actual_home = normalize_team_name(game['home_team']['name'].split()[-1])
        
        # Also check full name
        actual_away_full = normalize_team_name(game['away_team']['name'])
        actual_home_full = normalize_team_name(game['home_team']['name'])
        
        if ((pred_away in actual_away or pred_away in actual_away_full or actual_away in pred_away) and
            (pred_home in actual_home or pred_home in actual_home_full or actual_home in pred_home)):
            return game
    
    return None

def analyze_prediction(pred_game, actual_game):
    """Analyze if prediction was a hit"""
    if not actual_game or actual_game['status'] != 'Final':
        return None
    
    # Get actual scores
    away_score = int(actual_game['away_team']['score'])
    home_score = int(actual_game['home_team']['score'])
    actual_margin = away_score - home_score  # Positive = away won, negative = home won
    
    # Get prediction
    summary = pred_game['summary']
    predicted_spread = summary.get('spread_analysis', {}).get('predicted_spread', 0)
    predicted_winner = summary.get('predicted_winner', '')
    
    # Determine actual winner
    if actual_margin > 0:
        actual_winner = pred_game['away_team']
    elif actual_margin < 0:
        actual_winner = pred_game['home_team']
    else:
        actual_winner = 'Push'
    
    # Check if we predicted winner correctly
    winner_correct = (predicted_winner == actual_winner)
    
    # Check if spread was covered
    # Spread logic: If we predict -12.2 (favored by 12.2), we need to win by MORE than 12.2
    # actual_margin is (away - home), predicted_spread is from away team perspective
    # If predicted_spread is -12.2 (away favored), actual_margin needs to be < -12.2 (more negative = bigger win)
    # If predicted_spread is +5.0 (home favored), actual_margin needs to be > +5.0 (more positive = home covered)
    
    spread_covered = actual_margin < predicted_spread  # We beat the spread if actual is better than predicted
    
    return {
        'matchup': f"{pred_game['away_team']} @ {pred_game['home_team']}",
        'predicted_spread': predicted_spread,
        'predicted_winner': predicted_winner,
        'actual_score': f"{pred_game['away_team']} {away_score}, {pred_game['home_team']} {home_score}",
        'actual_margin': actual_margin,
        'actual_winner': actual_winner,
        'winner_correct': winner_correct,
        'spread_covered': spread_covered,
        'hit': spread_covered,
        'away_score': away_score,
        'home_score': home_score
    }

def main():
    print("🏈 Week 14 2025 Prediction Analysis")
    print("=" * 80)
    
    # Load data
    predictions_data = load_predictions()
    actual_data = load_actual_scores()
    
    predictions = predictions_data['games']
    actual_games = actual_data['games']
    
    print(f"\n📊 Loaded {len(predictions)} predictions and {actual_data['completed_games_count']} completed games\n")
    
    # Analyze each prediction
    hits = []
    misses = []
    no_result = []
    
    for pred in predictions:
        if not pred['success']:
            continue
            
        actual_game = find_actual_game(pred, actual_games)
        
        if not actual_game:
            no_result.append(pred)
            continue
        
        if actual_game['status'] != 'Final':
            no_result.append(pred)
            continue
            
        analysis = analyze_prediction(pred, actual_game)
        
        if analysis:
            if analysis['hit']:
                hits.append(analysis)
            else:
                misses.append(analysis)
    
    # Print results
    print(f"✅ HITS: {len(hits)}")
    print(f"❌ MISSES: {len(misses)}")
    print(f"⏳ NO RESULT YET: {len(no_result)}")
    
    if len(hits) + len(misses) > 0:
        hit_rate = (len(hits) / (len(hits) + len(misses))) * 100
        print(f"📈 HIT RATE: {hit_rate:.1f}%")
    
    # Show hits
    print("\n" + "=" * 80)
    print("✅ GAMES WE HIT (Spread Covered)")
    print("=" * 80)
    
    for hit in sorted(hits, key=lambda x: abs(x['predicted_spread']), reverse=True):
        print(f"\n{hit['matchup']}")
        print(f"  Predicted: {hit['predicted_winner']} {hit['predicted_spread']:+.1f}")
        print(f"  Actual: {hit['actual_score']} (margin: {hit['actual_margin']:+d})")
        print(f"  ✅ COVERED by {abs(hit['actual_margin'] - hit['predicted_spread']):.1f} points")
    
    # Show misses
    print("\n" + "=" * 80)
    print("❌ GAMES WE MISSED (Spread Not Covered)")
    print("=" * 80)
    
    for miss in sorted(misses, key=lambda x: abs(x['predicted_spread']), reverse=True):
        print(f"\n{miss['matchup']}")
        print(f"  Predicted: {miss['predicted_winner']} {miss['predicted_spread']:+.1f}")
        print(f"  Actual: {miss['actual_score']} (margin: {miss['actual_margin']:+d})")
        print(f"  ❌ MISSED by {abs(miss['actual_margin'] - miss['predicted_spread']):.1f} points")
    
    # Save detailed report
    report = {
        'generated_at': datetime.now().isoformat(),
        'week': 14,
        'season': 2025,
        'summary': {
            'total_predictions': len(predictions),
            'completed_games': len(hits) + len(misses),
            'hits': len(hits),
            'misses': len(misses),
            'pending': len(no_result),
            'hit_rate': round((len(hits) / (len(hits) + len(misses)) * 100), 1) if (len(hits) + len(misses)) > 0 else 0
        },
        'hits': hits,
        'misses': misses,
        'pending': [{'matchup': f"{p['away_team']} @ {p['home_team']}"} for p in no_result]
    }
    
    output_file = f"week14_prediction_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n\n💾 Detailed report saved to: {output_file}")

if __name__ == "__main__":
    main()
