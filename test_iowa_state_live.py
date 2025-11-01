#!/usr/bin/env python3
"""
Live Game Data Fetcher - Iowa State vs BYU Test
Fetches real-time game data, win probability, field position, and plays
Output: JSON format for UI integration
"""

import requests
import json
import os
from datetime import datetime

# API Configuration
CFBD_API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
HEADERS = {
    'Authorization': f'Bearer {CFBD_API_KEY}',
    'Accept': 'application/json'
}

GRAPHQL_ENDPOINT = "https://graphql.collegefootballdata.com/v1/graphql"
REST_BASE = "https://api.collegefootballdata.com"

# Game Configuration
WEEK = 10
YEAR = 2025
HOME_TEAM = "Iowa State"
AWAY_TEAM = "BYU"


def find_game_id(home_team, away_team, week=WEEK, year=YEAR):
    """Find game ID using scoreboard API"""
    url = f"{REST_BASE}/scoreboard"
    params = {'year': year, 'week': week, 'classification': 'fbs'}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        games = response.json()
        
        for game in games:
            home_match = home_team.lower() in game['homeTeam']['name'].lower()
            away_match = away_team.lower() in game['awayTeam']['name'].lower()
            
            if home_match and away_match:
                return {
                    'game_id': game['id'],
                    'status': game.get('status', 'scheduled'),
                    'home_team': game['homeTeam']['name'],
                    'away_team': game['awayTeam']['name']
                }
        
        print(f"❌ Game not found: {home_team} vs {away_team}")
        return None
        
    except Exception as e:
        print(f"❌ Error finding game: {e}")
        return None


def get_scoreboard_data(game_id):
    """Fetch live scoreboard data including win probability"""
    url = f"{REST_BASE}/scoreboard"
    params = {'year': YEAR, 'week': WEEK, 'classification': 'fbs'}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        games = response.json()
        
        game = next((g for g in games if g['id'] == game_id), None)
        
        if not game:
            return None
        
        return {
            'game_id': game['id'],
            'status': game.get('status', 'scheduled'),
            'period': game.get('period'),
            'clock': game.get('clock'),
            'situation': game.get('situation'),
            'possession': game.get('possession'),
            'last_play': game.get('lastPlay'),
            'home_team': {
                'name': game['homeTeam']['name'],
                'points': game['homeTeam'].get('points', 0),
                'line_scores': game['homeTeam'].get('lineScores', []),
                'win_probability': game['homeTeam'].get('winProbability')
            },
            'away_team': {
                'name': game['awayTeam']['name'],
                'points': game['awayTeam'].get('points', 0),
                'line_scores': game['awayTeam'].get('lineScores', []),
                'win_probability': game['awayTeam'].get('winProbability')
            }
        }
        
    except Exception as e:
        print(f"❌ Error fetching scoreboard: {e}")
        return None


def get_live_plays(game_id, limit=10):
    """Fetch live play-by-play data"""
    url = f"{REST_BASE}/live/plays"
    params = {'gameId': game_id}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        plays_data = response.json()
        
        # Extract all plays from drives
        all_plays = []
        
        for drive in plays_data.get('drives', []):
            for play in drive.get('plays', []):
                all_plays.append({
                    'id': play.get('id'),
                    'period': play.get('period'),
                    'clock': play.get('clock'),
                    'team': play.get('team'),
                    'down': play.get('down'),
                    'distance': play.get('distance'),
                    'yards_to_goal': play.get('yardsToGoal'),
                    'yards_gained': play.get('yardsGained'),
                    'play_type': play.get('playType'),
                    'play_text': play.get('playText'),
                    'home_score': play.get('homeScore'),
                    'away_score': play.get('awayScore'),
                    'epa': play.get('epa'),
                    'success': play.get('success')
                })
        
        # Sort by most recent (assuming later plays have higher IDs)
        all_plays.sort(key=lambda x: x.get('id', ''), reverse=True)
        
        return {
            'total_plays': len(all_plays),
            'recent_plays': all_plays,  # Return ALL plays, not limited
            'team_stats': plays_data.get('teams', [])
        }
        
    except Exception as e:
        print(f"❌ Error fetching plays: {e}")
        return None


def calculate_field_position(situation, possession):
    """
    Calculate field position from situation string
    Returns position as 0-100 (0 = offense's own goal line, 100 = opponent's goal line)
    """
    if not situation:
        return None
    
    import re
    match = re.search(r'at (\w+) (\d+)', situation)
    
    if match:
        team_abbr = match.group(1)
        yard_line = int(match.group(2))
        
        # Convert to 0-100 field position
        # If possession team matches yard_line team, they're on their own side
        return {
            'yard_line': yard_line,
            'team_abbr': team_abbr,
            'field_position': yard_line  # Simplified - would need team matching for accuracy
        }
    
    return None


def get_complete_live_data(home_team=HOME_TEAM, away_team=AWAY_TEAM):
    """
    Main function to fetch all live game data
    Returns comprehensive JSON structure for UI
    """
    
    print(f"\n🏈 FETCHING LIVE DATA: {away_team} @ {home_team}")
    print("=" * 60)
    
    # Step 1: Find game
    print("\n[1/3] Finding game...")
    game_info = find_game_id(home_team, away_team)
    
    if not game_info:
        return {'error': 'Game not found'}
    
    game_id = game_info['game_id']
    print(f"✅ Game ID: {game_id}")
    print(f"   Status: {game_info['status']}")
    
    # Step 2: Get scoreboard data
    print("\n[2/3] Fetching scoreboard data...")
    scoreboard = get_scoreboard_data(game_id)
    
    if not scoreboard:
        return {'error': 'Failed to fetch scoreboard data'}
    
    print(f"✅ Score: {scoreboard['away_team']['name']} {scoreboard['away_team']['points']} - {scoreboard['home_team']['points']} {scoreboard['home_team']['name']}")
    if scoreboard.get('situation'):
        print(f"   Situation: {scoreboard['situation']}")
    
    # Step 3: Get plays data (only if game is in progress)
    plays = None
    if scoreboard['status'] == 'in_progress':
        print("\n[3/3] Fetching live plays...")
        plays = get_live_plays(game_id, limit=10)
        
        if plays:
            print(f"✅ Total plays: {plays['total_plays']}")
            print(f"   Showing most recent {len(plays['recent_plays'])} plays")
    else:
        print(f"\n[3/3] Skipping plays (game status: {scoreboard['status']})")
    
    # Calculate field position
    field_position = None
    if scoreboard.get('situation') and scoreboard.get('possession'):
        field_position = calculate_field_position(
            scoreboard['situation'],
            scoreboard['possession']
        )
    
    # Construct final JSON
    live_data = {
        'game_info': {
            'game_id': game_id,
            'home_team': scoreboard['home_team']['name'],
            'away_team': scoreboard['away_team']['name'],
            'week': WEEK,
            'year': YEAR,
            'status': scoreboard['status'],
            'is_live': scoreboard['status'] == 'in_progress'
        },
        'game_state': {
            'period': scoreboard.get('period'),
            'clock': scoreboard.get('clock'),
            'situation': scoreboard.get('situation'),
            'possession': scoreboard.get('possession'),
            'last_play': scoreboard.get('last_play')
        },
        'score': {
            'home': {
                'team': scoreboard['home_team']['name'],
                'points': scoreboard['home_team']['points'],
                'line_scores': scoreboard['home_team']['line_scores']
            },
            'away': {
                'team': scoreboard['away_team']['name'],
                'points': scoreboard['away_team']['points'],
                'line_scores': scoreboard['away_team']['line_scores']
            }
        },
        'win_probability': {
            'home': scoreboard['home_team']['win_probability'],
            'away': scoreboard['away_team']['win_probability'],
            'home_percentage': round(scoreboard['home_team']['win_probability'] * 100, 1) if scoreboard['home_team']['win_probability'] else None,
            'away_percentage': round(scoreboard['away_team']['win_probability'] * 100, 1) if scoreboard['away_team']['win_probability'] else None
        },
        'field_position': field_position,
        'plays': plays,
        'timestamp': datetime.now().isoformat()
    }
    
    return live_data


def main():
    """Main execution"""
    
    # Fetch live data
    data = get_complete_live_data()
    
    # Save to JSON file
    output_file = f"live_data_{HOME_TEAM.replace(' ', '_')}_vs_{AWAY_TEAM.replace(' ', '_')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Data saved to: {output_file}")
    print("=" * 60)
    
    # Pretty print summary
    if 'error' not in data:
        print("\n📊 LIVE GAME SUMMARY")
        print("=" * 60)
        print(f"Game: {data['game_info']['away_team']} @ {data['game_info']['home_team']}")
        print(f"Status: {data['game_info']['status']}")
        print(f"\nScore:")
        print(f"  {data['score']['away']['team']}: {data['score']['away']['points']}")
        print(f"  {data['score']['home']['team']}: {data['score']['home']['points']}")
        
        if data['win_probability']['home_percentage']:
            print(f"\nWin Probability:")
            print(f"  {data['score']['home']['team']}: {data['win_probability']['home_percentage']}%")
            print(f"  {data['score']['away']['team']}: {data['win_probability']['away_percentage']}%")
        
        if data['game_state']['situation']:
            print(f"\nCurrent Situation: {data['game_state']['situation']}")
        
        if data['plays']:
            print(f"\nMost Recent Play:")
            recent = data['plays']['recent_plays'][0] if data['plays']['recent_plays'] else None
            if recent:
                print(f"  Q{recent['period']} {recent['clock']} - {recent['play_text'][:80]}...")
    
    print("\n")


if __name__ == "__main__":
    main()
