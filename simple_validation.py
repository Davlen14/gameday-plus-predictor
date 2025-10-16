#!/usr/bin/env python3
"""
Simple validation script to test predictions against historical results
"""

import json
import sys
import os
import asyncio
from datetime import datetime

# Add the current directory to path to import our predictor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graphqlpredictor import LightningPredictor

def load_historical_games(json_file):
    """Load historical games from JSON file"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data['games']
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return []

def load_team_mappings():
    """Load team name to ID mappings from fbs.json"""
    try:
        with open('fbs.json', 'r') as f:
            teams = json.load(f)
        
        # Create mapping from school name to ID
        name_to_id = {}
        for team in teams:
            name_to_id[team['school']] = team['id']
        
        return name_to_id
    except Exception as e:
        print(f"Error loading team mappings: {e}")
        return {}

def get_team_id(team_name, mappings):
    """Get team ID from name"""
    if team_name in mappings:
        return mappings[team_name]
    
    # Try some common variations
    variations = [
        team_name,
        team_name.replace('State', 'St.'),
        team_name.replace('St.', 'State'),
    ]
    
    for variation in variations:
        if variation in mappings:
            return mappings[variation]
    
    return None

def extract_pre_game_info(game):
    """Extract the information that would be available before the game"""
    pre_game_data = {
        'id': game['id'],
        'season': game['season'],
        'week': game['week'],
        'homeTeam': game['homeTeam'],
        'awayTeam': game['awayTeam'],
        'homeConference': game['homeConference'],
        'awayConference': game['awayConference'],
        'startDate': game['startDate'],
        'neutralSite': game['neutralSite'],
        'conferenceGame': game['conferenceGame'],
        # Actual results (for comparison)
        'actual_home_score': game['homePoints'],
        'actual_away_score': game['awayPoints'],
        'actual_winner': 'home' if game['homePoints'] > game['awayPoints'] else 'away'
    }
    
    # Add betting lines if available
    if 'lines' in game and game['lines']:
        for line in game['lines']:
            if line.get('provider') == 'DraftKings':  # Prefer DraftKings
                pre_game_data['spread'] = line.get('spread')
                pre_game_data['overUnder'] = line.get('overUnder')
                break
        else:
            # Fallback to first available line
            line = game['lines'][0]
            pre_game_data['spread'] = line.get('spread')
            pre_game_data['overUnder'] = line.get('overUnder')
    
    # Add weather if available
    if 'weather' in game:
        pre_game_data['weather'] = game['weather']
    
    return pre_game_data

async def run_single_prediction_test(game_data, team_mappings):
    """Run a prediction test on a single game"""
    try:
        # Initialize the predictor with API key
        api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
        predictor = LightningPredictor(api_key)
        
        # Get team IDs
        home_team_id = get_team_id(game_data['homeTeam'], team_mappings)
        away_team_id = get_team_id(game_data['awayTeam'], team_mappings)
        
        if not home_team_id or not away_team_id:
            print(f"❌ Could not find team IDs for {game_data['awayTeam']} @ {game_data['homeTeam']}")
            print(f"   Home: {game_data['homeTeam']} -> {home_team_id}")
            print(f"   Away: {game_data['awayTeam']} -> {away_team_id}")
            return None
        
        # Get prediction (this will use the GraphQL API)
        print(f"\n{'='*60}")
        print(f"TESTING: {game_data['awayTeam']} @ {game_data['homeTeam']}")
        print(f"Date: {game_data['startDate']}")
        print(f"Week {game_data['week']}, {game_data['season']}")
        print(f"Team IDs: {away_team_id} @ {home_team_id}")
        print(f"{'='*60}")
        
        # Run the prediction
        prediction = await predictor.predict_game(
            home_team_id=home_team_id,
            away_team_id=away_team_id
        )
        
        if not prediction:
            print("❌ Prediction failed")
            return None
        
        # Extract prediction results
        predicted_winner = 'home' if prediction.home_win_prob > 50 else 'away'
        
        # Calculate scores from spread and total
        home_implied_score = (prediction.predicted_total - prediction.predicted_spread) / 2
        away_implied_score = (prediction.predicted_total + prediction.predicted_spread) / 2
        
        # Handle extreme cases where a team would have negative points
        if home_implied_score < 0:
            predicted_home_score = 0
            predicted_away_score = prediction.predicted_total
        elif away_implied_score < 0:
            predicted_away_score = 0
            predicted_home_score = prediction.predicted_total
        else:
            predicted_home_score = home_implied_score
            predicted_away_score = away_implied_score
            
        confidence = prediction.home_win_prob
        if predicted_winner == 'away':
            confidence = 100 - confidence
        
        # Show results
        print(f"\n📊 PREDICTION RESULTS:")
        print(f"Predicted Winner: {game_data['homeTeam'] if predicted_winner == 'home' else game_data['awayTeam']}")
        print(f"Predicted Score: {game_data['homeTeam']} {predicted_home_score:.1f} - {predicted_away_score:.1f} {game_data['awayTeam']}")
        print(f"Confidence: {confidence:.1f}%")
        
        print(f"\n🏆 ACTUAL RESULTS:")
        print(f"Actual Winner: {game_data['homeTeam'] if game_data['actual_winner'] == 'home' else game_data['awayTeam']}")
        print(f"Actual Score: {game_data['homeTeam']} {game_data['actual_home_score']} - {game_data['actual_away_score']} {game_data['awayTeam']}")
        
        # Check accuracy
        winner_correct = predicted_winner == game_data['actual_winner']
        score_diff_home = abs(predicted_home_score - game_data['actual_home_score'])
        score_diff_away = abs(predicted_away_score - game_data['actual_away_score'])
        
        print(f"\n✅ VALIDATION:")
        print(f"Winner Prediction: {'✅ CORRECT' if winner_correct else '❌ WRONG'}")
        print(f"Home Score Diff: {score_diff_home:.1f} points")
        print(f"Away Score Diff: {score_diff_away:.1f} points")
        print(f"Total Score Diff: {score_diff_home + score_diff_away:.1f} points")
        
        return {
            'game_id': game_data['id'],
            'teams': f"{game_data['awayTeam']} @ {game_data['homeTeam']}",
            'winner_correct': winner_correct,
            'score_diff_total': score_diff_home + score_diff_away,
            'confidence': confidence,
            'prediction': prediction.__dict__ if hasattr(prediction, '__dict__') else prediction
        }
        
    except Exception as e:
        print(f"❌ Error running prediction: {e}")
        return None

async def main():
    """Main function to run the validation"""
    print("🏈 College Football Prediction Validation - Week 7 2025")
    print("=" * 60)
    
    # Load team mappings
    team_mappings = load_team_mappings()
    if not team_mappings:
        print("❌ Could not load team mappings")
        return
    
    print(f"📚 Loaded {len(team_mappings)} team mappings")
    
    # Load 2024 games
    games_2024 = load_historical_games('backtesting/all_fbs_games_2024_ENHANCED_20251015_002119.json')
    
    if not games_2024:
        print("❌ Could not load 2024 games")
        return
    
    print(f"📂 Loaded {len(games_2024)} games from 2024")
    
    # Filter for completed games only
    completed_games = [g for g in games_2024 if g.get('status') == 'completed']
    print(f"✅ Found {len(completed_games)} completed games")
    
    # Load 2025 games for Week 7 analysis
    games_2025 = load_historical_games('backtesting/all_fbs_games_2025_ENHANCED_20251015_083540.json')
    
    if not games_2025:
        print("❌ Could not load 2025 games")
        return
    
    print(f"📂 Loaded {len(games_2025)} games from 2025")
    
    # Filter for Week 7 completed games only
    week7_games = [g for g in games_2025 if g.get('week') == 7 and g.get('status') == 'completed']
    print(f"🎯 Found {len(week7_games)} completed Week 7 games")
    
    if not week7_games:
        print("❌ No Week 7 completed games found")
        return
    
    # Test all Week 7 games
    test_games = week7_games
    
    print(f"\n🎯 Testing all {len(test_games)} Week 7 games...")
    
    results = []
    for i, game in enumerate(test_games, 1):
        print(f"\n🏈 Game {i}/{len(test_games)} - Week 7, 2025")
        pre_game_data = extract_pre_game_info(game)
        result = await run_single_prediction_test(pre_game_data, team_mappings)
        
        if result:
            results.append(result)
        
        # Add a small delay to be nice to the API
        await asyncio.sleep(1)
    
    # Summary
    if results:
        correct_predictions = sum(1 for r in results if r['winner_correct'])
        avg_score_diff = sum(r['score_diff_total'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        print(f"\n{'='*60}")
        print(f"📈 VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Games Tested: {len(results)}")
        print(f"Correct Winner Predictions: {correct_predictions}/{len(results)} ({correct_predictions/len(results)*100:.1f}%)")
        print(f"Average Score Difference: {avg_score_diff:.1f} points")
        print(f"Average Confidence: {avg_confidence:.1f}%")
        print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())