#!/usr/bin/env python3
"""
Retry failed Week 14 games with longer timeout and sequential processing
"""
import requests
import json
from datetime import datetime
import time

# Failed games from previous run
FAILED_GAMES = [
    {'away': 'Ohio State', 'home': 'Michigan'},
    {'away': 'Indiana', 'home': 'Purdue'},
    {'away': 'Georgia', 'home': 'Georgia Tech'},
    {'away': 'Alabama', 'home': 'Auburn'},
    {'away': 'Texas Tech', 'home': 'West Virginia'},
    {'away': 'UCF', 'home': 'BYU'},
    {'away': 'Virginia Tech', 'home': 'Virginia'},
    {'away': 'James Madison', 'home': 'Coastal Carolina'},
    {'away': 'Temple', 'home': 'North Texas'},
    {'away': 'Charlotte', 'home': 'Tulane'},
    {'away': 'Kennesaw State', 'home': 'Liberty'},
    {'away': 'Troy', 'home': 'Southern Miss'},
    {'away': 'Ball State', 'home': 'Miami (OH)'},
    {'away': 'Western Kentucky', 'home': 'Jacksonville State'},
    {'away': 'Wake Forest', 'home': 'Duke'},
    {'away': 'Western Michigan', 'home': 'Eastern Michigan'}
]

API_URL = "http://localhost:5002/predict"

def fetch_game_summary(game, index):
    """Fetch game summary for a single game with extended timeout"""
    payload = {
        "home_team": game['home'],
        "away_team": game['away'],
        "week": 14,
        "year": 2025
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=180)  # 3 minute timeout
        if response.status_code == 200:
            data = response.json()
            summary = data.get('ui_components', {}).get('game_summary_and_rationale', {})
            
            print(f"✅ [{index+1}/16] {game['away']} @ {game['home']}")
            
            return {
                'game': game,
                'summary': summary.get('summary', ''),
                'rationale': summary.get('rationale', [])
            }
        else:
            print(f"❌ [{index+1}/16] {game['away']} @ {game['home']} - Status {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏱️  [{index+1}/16] {game['away']} @ {game['home']} - Timeout")
        return None
    except Exception as e:
        print(f"❌ [{index+1}/16] {game['away']} @ {game['home']} - {str(e)}")
        return None

def main():
    print(f"🏈 Retrying {len(FAILED_GAMES)} failed Week 14 games...")
    print(f"⏱️  Started at {datetime.now().strftime('%H:%M:%S')}\n")
    
    results = []
    successful = 0
    failed = 0
    
    for index, game in enumerate(FAILED_GAMES):
        result = fetch_game_summary(game, index)
        if result:
            results.append(result)
            successful += 1
        else:
            failed += 1
        
        # Small delay between requests to avoid overwhelming the server
        if index < len(FAILED_GAMES) - 1:
            time.sleep(2)
    
    print(f"\n⏱️  Completed at {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n📊 Results: {successful} successful, {failed} failed")
    
    # Save results
    if results:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"week14_retry_summaries_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
        
        # Load original file and merge
        try:
            with open('week14_enhanced_summaries_20251130_052138.json', 'r') as f:
                original_data = json.load(f)
            
            # Add retry results to original
            original_data.extend(results)
            
            # Save merged results
            merged_filename = f"week14_complete_summaries_{timestamp}.json"
            with open(merged_filename, 'w') as f:
                json.dump(original_data, f, indent=2)
            
            print(f"💾 Merged results saved to: {merged_filename}")
            print(f"📊 Total games: {len(original_data)}")
        except FileNotFoundError:
            print("⚠️  Could not find original file to merge")

if __name__ == "__main__":
    main()
