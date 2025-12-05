#!/usr/bin/env python3
"""
Regenerate Week 14 game summaries JSON with complete market analysis
"""

import json
import asyncio
import os
from datetime import datetime
from graphqlpredictor import LightningPredictor
from app import generate_game_summary_and_rationale

def get_team_id(team_name):
    """Convert team name to team ID using fbs.json data"""
    if isinstance(team_name, int):
        return team_name
    
    team_name_lower = team_name.lower().strip()
    
    with open('fbs.json', 'r') as f:
        teams_data = json.load(f)
    
    # Exact matches
    for team in teams_data:
        if team['school'].lower() == team_name_lower:
            return team['id']
        if team['mascot'].lower() == team_name_lower:
            return team['id']
    
    # Word matches
    for team in teams_data:
        school_words = team['school'].lower().split()
        if team_name_lower in school_words:
            return team['id']
    
    # Partial matches
    for team in teams_data:
        if team_name_lower in team['school'].lower():
            return team['id']
    
    raise ValueError(f"Team '{team_name}' not found in fbs.json")

async def regenerate_json():
    """Regenerate JSON with complete market analysis"""
    
    print("📊 Loading Week 14 games...")
    with open('Currentweekgames.json', 'r') as f:
        games_data = json.load(f)
    
    all_games = games_data['games']['all']
    print(f"Found {len(all_games)} games to analyze\n")
    
    print("⚡ Initializing LightningPredictor...")
    api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    predictor = LightningPredictor(api_key)
    
    results = []
    successful = 0
    failed = 0
    
    for idx, game in enumerate(all_games, 1):
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        
        print(f"\n[{idx}/{len(all_games)}] Analyzing {away_team} @ {home_team}...")
        
        try:
            home_team_id = get_team_id(home_team)
            away_team_id = get_team_id(away_team)
            
            # Run prediction
            prediction = await predictor.predict_game(home_team_id, away_team_id)
            
            # Extract betting lines from game data
            betting_lines = game.get('bettingLines', {})
            consensus = betting_lines.get('consensus', {})
            providers = betting_lines.get('allProviders', [])
            
            # Format betting analysis for the summary generator
            betting_analysis = None
            if providers:
                betting_analysis = {
                    'sportsbooks': {
                        'individual_books': []
                    }
                }
                
                for provider in providers:
                    book_data = {
                        'provider': provider.get('provider', 'Unknown'),
                        'spread': provider.get('spread'),
                        'over_under': provider.get('overUnder'),
                        'spread_odds': -110  # Default odds
                    }
                    betting_analysis['sportsbooks']['individual_books'].append(book_data)
            
            # Generate comprehensive summary with market analysis
            summary = generate_game_summary_and_rationale(
                prediction,
                {},  # details
                {},  # home_team_data
                {},  # away_team_data
                predictor,
                betting_analysis
            )
            
            results.append({
                'matchup': f"{away_team} @ {home_team}",
                'away_team': away_team,
                'home_team': home_team,
                'summary': summary,
                'success': True
            })
            
            successful += 1
            winner = summary['predicted_winner']
            win_prob = summary['win_probability']['favorite']
            spread = summary['spread_analysis']['spread_display']
            print(f"✅ Complete: {winner} {win_prob:.1f}% ({spread})")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'matchup': f"{away_team} @ {home_team}",
                'away_team': away_team,
                'home_team': home_team,
                'error': str(e),
                'success': False
            })
            failed += 1
    
    # Build output
    output = {
        'generated_at': datetime.now().isoformat(),
        'total_games': len(all_games),
        'successful': successful,
        'failed': failed,
        'games': results
    }
    
    # Write to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'week14_game_summaries_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Complete! Output saved to {output_file}")
    print(f"📊 Successful: {successful}/{len(all_games)}")
    print(f"❌ Failed: {failed}/{len(all_games)}")

if __name__ == "__main__":
    asyncio.run(regenerate_json())
