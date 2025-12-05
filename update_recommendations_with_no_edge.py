#!/usr/bin/env python3
"""
Update week14_recommendations_analysis.json to include "No Strong Edge" games
"""
import json
from datetime import datetime

def main():
    # Load current recommendations analysis
    with open('week14_recommendations_analysis.json', 'r') as f:
        analysis = json.load(f)
    
    # Load complete games for model spreads
    with open('week14_complete_all_games.json', 'r') as f:
        complete = json.load(f)
    
    # No edge games with actual results
    no_edge_games = {
        'Charlotte @ Tulane': {'actual': '13-35', 'margin': -22},
        'Florida State @ Florida': {'actual': '31-24', 'margin': 7},
        'San Diego State @ New Mexico': {'actual': '28-21', 'margin': 7},
        'Arizona @ Arizona State': {'actual': '21-35', 'margin': -14},
        'UTEP @ Delaware': {'actual': '14-21', 'margin': -7},
        'Louisiana Tech @ Missouri State': {'actual': '29-27', 'margin': 2},
        'Boston College @ Syracuse': {'actual': '17-45', 'margin': -28},
        'Wisconsin @ Minnesota': {'actual': '17-13', 'margin': 4},
        'Wake Forest @ Duke': {'actual': '14-23', 'margin': -9},
        'North Carolina @ NC State': {'actual': '29-35', 'margin': -6}
    }
    
    # Add no-edge games to results
    no_edge_hits = 0
    for game in complete['games']:
        matchup = game['matchup']
        if matchup in no_edge_games:
            model_spread_str = game['summary']['bottom_line']['model_spread']
            actual_data = no_edge_games[matchup]
            actual_result = actual_data['actual']
            actual_margin = actual_data['margin']
            
            # Parse model spread
            parts = model_spread_str.split()
            predicted_team = ' '.join(parts[:-1])
            predicted_spread = float(parts[-1])
            
            away_team = matchup.split(' @ ')[0]
            
            # Check if model predicted the right winner
            if predicted_team == away_team:
                model_predicted_away_win = predicted_spread < 0
            else:
                model_predicted_away_win = predicted_spread > 0
            
            actual_away_win = actual_margin > 0
            won = model_predicted_away_win == actual_away_win
            
            if won:
                no_edge_hits += 1
            
            # Add to results
            analysis['results'].append({
                'matchup': matchup,
                'recommendation': f"No strong edge ({model_spread_str})",
                'grade': 'NO EDGE',
                'edge': 0.0,
                'model_spread': model_spread_str,
                'actual_result': actual_result,
                'actual_margin': actual_margin,
                'bet_spread': 0.0,
                'won': won,
                'result_icon': '✅' if won else '❌'
            })
    
    # Update totals
    old_hits = analysis['hits']
    old_total = analysis['total_recommendations']
    
    analysis['total_recommendations'] = 67  # All games
    analysis['hits'] = old_hits + no_edge_hits
    analysis['misses'] = 67 - analysis['hits']
    analysis['no_result'] = 0
    analysis['win_rate'] = round((analysis['hits'] / 67) * 100, 1)
    analysis['generated_at'] = datetime.now().isoformat()
    
    # Save updated analysis
    with open('week14_recommendations_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"✅ Updated recommendations analysis!")
    print(f"\n📊 New Stats:")
    print(f"   Total Games: 67")
    print(f"   Betting Recommendations: 57 ({old_hits}/57 won = {(old_hits/57)*100:.1f}%)")
    print(f"   No Edge Games: 10 ({no_edge_hits}/10 won = {(no_edge_hits/10)*100:.1f}%)")
    print(f"   Combined: {analysis['hits']}/67 = {analysis['win_rate']}%")

if __name__ == "__main__":
    main()
