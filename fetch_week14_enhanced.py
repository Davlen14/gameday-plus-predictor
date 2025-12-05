#!/usr/bin/env python3
"""
Fetch game summary and rationale for all Week 14 games in parallel
"""
import asyncio
import aiohttp
import json
from datetime import datetime

# Week 14 games from TeamSelector.tsx
WEEK_14_GAMES = [
    # Top Ranked Matchups
    {'away': 'Ohio State', 'home': 'Michigan'},
    {'away': 'Indiana', 'home': 'Purdue'},
    {'away': 'Texas A&M', 'home': 'Texas'},
    {'away': 'Georgia', 'home': 'Georgia Tech'},
    {'away': 'Oregon', 'home': 'Washington'},
    {'away': 'Ole Miss', 'home': 'Mississippi State'},
    {'away': 'Texas Tech', 'home': 'West Virginia'},
    {'away': 'LSU', 'home': 'Oklahoma'},
    {'away': 'Notre Dame', 'home': 'Stanford'},
    {'away': 'Alabama', 'home': 'Auburn'},
    {'away': 'UCF', 'home': 'BYU'},
    {'away': 'Vanderbilt', 'home': 'Tennessee'},
    {'away': 'Miami', 'home': 'Pittsburgh'},
    {'away': 'Utah', 'home': 'Kansas'},
    {'away': 'Virginia Tech', 'home': 'Virginia'},
    {'away': 'UCLA', 'home': 'USC'},
    {'away': 'James Madison', 'home': 'Coastal Carolina'},
    {'away': 'Temple', 'home': 'North Texas'},
    {'away': 'Charlotte', 'home': 'Tulane'},
    {'away': 'SMU', 'home': 'California'},
    # Rest of Week 14 Games
    {'away': 'Cincinnati', 'home': 'TCU'},
    {'away': 'Kennesaw State', 'home': 'Liberty'},
    {'away': 'Troy', 'home': 'Southern Miss'},
    {'away': 'Florida State', 'home': 'Florida'},
    {'away': 'Oregon State', 'home': 'Washington State'},
    {'away': 'Maryland', 'home': 'Michigan State'},
    {'away': 'Rice', 'home': 'South Florida'},
    {'away': 'Northwestern', 'home': 'Illinois'},
    {'away': 'Navy', 'home': 'Memphis'},
    {'away': 'Ohio', 'home': 'Buffalo'},
    {'away': 'Kent State', 'home': 'Northern Illinois'},
    {'away': 'Air Force', 'home': 'Colorado State'},
    {'away': 'San Diego State', 'home': 'New Mexico'},
    {'away': 'Boise State', 'home': 'Utah State'},
    {'away': 'Arizona', 'home': 'Arizona State'},
    {'away': 'Houston', 'home': 'Baylor'},
    {'away': 'Kentucky', 'home': 'Louisville'},
    {'away': 'Clemson', 'home': 'South Carolina'},
    {'away': 'Colorado', 'home': 'Kansas State'},
    {'away': 'Iowa State', 'home': 'Oklahoma State'},
    {'away': 'East Carolina', 'home': 'Florida Atlantic'},
    {'away': 'Toledo', 'home': 'Central Michigan'},
    {'away': 'Ball State', 'home': 'Miami (OH)'},
    {'away': 'UTEP', 'home': 'Delaware'},
    {'away': 'Florida International', 'home': 'Sam Houston'},
    {'away': 'Georgia Southern', 'home': 'Marshall'},
    {'away': 'Western Kentucky', 'home': 'Jacksonville State'},
    {'away': 'Louisiana Tech', 'home': 'Missouri State'},
    {'away': 'Georgia State', 'home': 'Old Dominion'},
    {'away': 'Arkansas State', 'home': 'App State'},
    {'away': 'Boston College', 'home': 'Syracuse'},
    {'away': 'Middle Tennessee', 'home': 'New Mexico State'},
    {'away': 'UL Monroe', 'home': 'Louisiana'},
    {'away': 'South Alabama', 'home': 'Texas State'},
    {'away': 'Missouri', 'home': 'Arkansas'},
    {'away': 'Wisconsin', 'home': 'Minnesota'},
    {'away': 'Penn State', 'home': 'Rutgers'},
    {'away': 'Wake Forest', 'home': 'Duke'},
    {'away': 'North Carolina', 'home': 'NC State'},
    {'away': 'UAB', 'home': 'Tulsa'},
    {'away': 'Fresno State', 'home': 'San José State'},
    {'away': 'Bowling Green', 'home': 'Massachusetts'},
    {'away': 'Western Michigan', 'home': 'Eastern Michigan'},
    {'away': 'Army', 'home': 'UTSA'},
    {'away': 'Iowa', 'home': 'Nebraska'},
    {'away': 'UNLV', 'home': 'Nevada'},
    {'away': 'Wyoming', 'home': 'Hawai\'i'}
]

API_URL = "http://localhost:5002/predict"

async def fetch_game_summary(session, game, index):
    """Fetch comprehensive game prediction data including all 3 UI sections"""
    payload = {
        "home_team": game['home'],
        "away_team": game['away'],
        "week": 14,
        "year": 2025
    }
    
    try:
        async with session.post(API_URL, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                ui = data.get('ui_components', {})
                summary = ui.get('game_summary_and_rationale', {})
                
                # Extract all three key sections
                prediction_cards = ui.get('prediction_cards', {})
                final_prediction = ui.get('final_prediction', {})
                ats_comparison = ui.get('ats_comparison', {})
                market_comparison = ui.get('detailed_analysis', {}).get('betting_analysis', {})
                header = ui.get('header', {})
                
                # Extract key data points
                win_prob = prediction_cards.get('win_probability', {})
                spread = prediction_cards.get('predicted_spread', {})
                total = prediction_cards.get('predicted_total', {})
                score = final_prediction.get('predicted_score', {})
                
                print(f"✅ [{index+1}/67] {game['away']} @ {game['home']} - {win_prob.get('favored_team', '')} {max(win_prob.get('home_team_prob', 0), win_prob.get('away_team_prob', 0)):.1f}%")
                
                return {
                    'matchup': f"{game['away']} @ {game['home']}",
                    'away_team': game['away'],
                    'home_team': game['home'],
                    'summary': summary,
                    
                    # Section 1: Win Probability & Prediction Cards
                    'win_probability': {
                        'favored_team': win_prob.get('favored_team', ''),
                        'home_prob': win_prob.get('home_team_prob', 0),
                        'away_prob': win_prob.get('away_team_prob', 0)
                    },
                    'predicted_spread': {
                        'model_spread': spread.get('model_spread', 0),
                        'model_spread_display': spread.get('model_spread_display', ''),
                        'market_spread': spread.get('market_spread', 0),
                        'edge': spread.get('edge', 0)
                    },
                    'predicted_total': {
                        'model_total': total.get('model_total', 0),
                        'market_total': total.get('market_total', 0),
                        'edge': total.get('edge', 0)
                    },
                    
                    # Section 2: Final Prediction Summary
                    'final_score': {
                        'away_score': score.get('away_score', 0),
                        'home_score': score.get('home_score', 0),
                        'total': score.get('total', 0)
                    },
                    'key_factors': final_prediction.get('key_factors', []),
                    
                    # Section 3: ATS Comparison
                    'ats_performance': {
                        'away_team': {
                            'ats_record': ats_comparison.get('away_team', {}).get('ats_record', 'N/A'),
                            'cover_rate': ats_comparison.get('away_team', {}).get('cover_rate', 0),
                            'avg_margin': ats_comparison.get('away_team', {}).get('avg_cover_margin', 0),
                            'rating': ats_comparison.get('away_team', {}).get('rating', 'N/A')
                        },
                        'home_team': {
                            'ats_record': ats_comparison.get('home_team', {}).get('ats_record', 'N/A'),
                            'cover_rate': ats_comparison.get('home_team', {}).get('cover_rate', 0),
                            'avg_margin': ats_comparison.get('home_team', {}).get('avg_cover_margin', 0),
                            'rating': ats_comparison.get('home_team', {}).get('rating', 'N/A')
                        },
                        'betting_intelligence': ats_comparison.get('betting_intelligence', '')
                    },
                    
                    # Section 4: Market Analysis
                    'market_analysis': {
                        'spread_recommendation': market_comparison.get('spread_recommendation', ''),
                        'total_recommendation': market_comparison.get('total_recommendation', ''),
                        'spread_edge': market_comparison.get('spread_edge', 0),
                        'total_edge': market_comparison.get('total_edge', 0),
                        'formatted_spread': market_comparison.get('formatted_spread', '')
                    },
                    
                    # Game info
                    'game_info': header.get('game_info', {}),
                    
                    'success': True
                }
            else:
                print(f"❌ [{index+1}/67] {game['away']} @ {game['home']} - Status {response.status}")
                return {
                    'matchup': f"{game['away']} @ {game['home']}",
                    'success': False,
                    'error': f"HTTP {response.status}"
                }
    except Exception as e:
        print(f"❌ [{index+1}/67] {game['away']} @ {game['home']} - Error: {str(e)}")
        return {
            'matchup': f"{game['away']} @ {game['home']}",
            'success': False,
            'error': str(e)
        }

async def fetch_all_summaries():
    """Fetch all game summaries in parallel with controlled concurrency"""
    print(f"🏈 Fetching summaries for {len(WEEK_14_GAMES)} Week 14 games...")
    print(f"⏱️  Started at {datetime.now().strftime('%H:%M:%S')}\n")
    
    # Limit concurrent requests to avoid overwhelming the server
    connector = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=300)  # 5 minute timeout
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_game_summary(session, game, i) for i, game in enumerate(WEEK_14_GAMES)]
        results = await asyncio.gather(*tasks)
    
    print(f"\n⏱️  Completed at {datetime.now().strftime('%H:%M:%S')}")
    
    # Summary statistics
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\n📊 Results: {successful} successful, {failed} failed")
    
    # Save results
    output_file = f"week14_enhanced_summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'total_games': len(results),
            'successful': successful,
            'failed': failed,
            'games': results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(fetch_all_summaries())
