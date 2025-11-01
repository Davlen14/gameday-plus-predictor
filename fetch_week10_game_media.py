"""
Fetch all Week 10 FBS game media information from College Football Data API
Outputs to: week10_game_media.json
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from pathlib import Path

# Use environment variable or default API key
API_KEY = os.getenv('CFBD_API_KEY', "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p")
GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"

WEEK = 10
YEAR = 2025

# Load FBS team IDs for filtering
SCRIPT_DIR = Path(__file__).parent
FBS_FILE = SCRIPT_DIR / "fbs.json"

def load_fbs_team_ids():
    """Load FBS team IDs from fbs.json"""
    try:
        with open(FBS_FILE, 'r') as f:
            fbs_teams = json.load(f)
            return {team['id'] for team in fbs_teams}
    except Exception as e:
        print(f"⚠️ Warning: Could not load FBS team IDs: {e}")
        return set()

# GraphQL Query for Week 10 games
WEEK_GAMES_QUERY = """
query Week10FBSGames($year: smallint!, $week: smallint!) {
  games(
    where: {
      season: {_eq: $year}
      week: {_eq: $week}
      seasonType: {_eq: "regular"}
    }
    order_by: {startDate: asc}
  ) {
    id
    season
    week
    seasonType
    startDate
    startTimeTBD
    neutralSite
    conferenceGame
    homeId
    homeTeam
    homeConference
    homePoints
    awayId
    awayTeam
    awayConference
    awayPoints
    excitement
    highlightsAvailable
    venue
    venueId
    attendance
    media {
      mediaType
      outlet
    }
  }
}
"""

async def fetch_week10_fbs_games():
    """Fetch all Week 10 FBS games with media information"""
    
    query_vars = {
        "year": YEAR,
        "week": WEEK
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": WEEK_GAMES_QUERY,
        "variables": query_vars
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPHQL_URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('data', {}).get('games', [])
                else:
                    error_text = await response.text()
                    print(f"❌ GraphQL Error: {response.status}")
                    print(f"Response: {error_text}")
                    return []
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

def filter_fbs_games(games, fbs_team_ids):
    """Filter games to include only FBS vs FBS matchups"""
    fbs_games = []
    
    for game in games:
        home_id = game.get('homeId')
        away_id = game.get('awayId')
        
        if home_id in fbs_team_ids and away_id in fbs_team_ids:
            fbs_games.append(game)
    
    return fbs_games

def format_game_data(games):
    """Format and enrich game data"""
    formatted_games = []
    
    for game in games:
        media_info = game.get('media', [])
        tv_broadcast = next((m for m in media_info if m.get('mediaType') == 'TV'), None)
        
        formatted_game = {
            'id': game.get('id'),
            'week': game.get('week'),
            'season': game.get('season'),
            'date': game.get('startDate'),
            'time_tbd': game.get('startTimeTBD', False),
            'home_team': game.get('homeTeam'),
            'home_id': game.get('homeId'),
            'home_conference': game.get('homeConference'),
            'away_team': game.get('awayTeam'),
            'away_id': game.get('awayId'),
            'away_conference': game.get('awayConference'),
            'neutral_site': game.get('neutralSite', False),
            'conference_game': game.get('conferenceGame', False),
            'venue': game.get('venue'),
            'venue_id': game.get('venueId'),
            'tv_network': tv_broadcast.get('outlet') if tv_broadcast else None,
            'media': media_info,
            'home_points': game.get('homePoints'),
            'away_points': game.get('awayPoints'),
            'completed': game.get('homePoints') is not None
        }
        
        formatted_games.append(formatted_game)
    
    return formatted_games

def print_game_summary(games):
    """Print formatted summary of games"""
    print(f"\n{'='*80}")
    print(f"📺 WEEK 10 FBS GAMES - {YEAR} SEASON")
    print(f"{'='*80}\n")
    
    conf_games = [g for g in games if g.get('conference_game')]
    non_conf_games = [g for g in games if not g.get('conference_game')]
    
    print(f"📊 SUMMARY:")
    print(f"   Total FBS Games: {len(games)}")
    print(f"   Conference Games: {len(conf_games)}")
    print(f"   Non-Conference Games: {len(non_conf_games)}")
    
    networks = {}
    for game in games:
        network = game.get('tv_network') or 'No TV'
        networks[network] = networks.get(network, 0) + 1
    
    print(f"\n📺 TV COVERAGE:")
    for network, count in sorted(networks.items(), key=lambda x: x[1], reverse=True):
        print(f"   {network}: {count} games")
    
    print(f"\n{'='*80}\n")
    
    for idx, game in enumerate(games, 1):
        date_obj = datetime.fromisoformat(game['date'].replace('Z', '+00:00'))
        date_str = date_obj.strftime('%a %b %d, %I:%M %p ET')
        
        network = game.get('tv_network') or 'No TV'
        conf_tag = "🏆 CONF" if game.get('conference_game') else "      "
        neutral_tag = "⚖️" if game.get('neutral_site') else ""
        
        print(f"{idx:2d}. {date_str}")
        print(f"    {game['away_team']} @ {game['home_team']} {neutral_tag}")
        print(f"    📺 {network:15s} {conf_tag}")
        print(f"    🏟️  {game['venue']}")
        print()

async def main():
    print(f"🏈 Fetching Week {WEEK} {YEAR} FBS Games...")
    
    fbs_team_ids = load_fbs_team_ids()
    print(f"✅ Loaded {len(fbs_team_ids)} FBS teams")
    
    games = await fetch_week10_fbs_games()
    
    if not games:
        print("❌ No games found!")
        return
    
    print(f"✅ Found {len(games)} total games")
    
    fbs_games = filter_fbs_games(games, fbs_team_ids)
    print(f"✅ Filtered to {len(fbs_games)} FBS vs FBS games")
    
    formatted_games = format_game_data(fbs_games)
    formatted_games.sort(key=lambda x: x['date'])
    
    print_game_summary(formatted_games)
    
    output_file = 'week10_game_media.json'
    output_data = {
        'week': WEEK,
        'season': YEAR,
        'fetched_at': datetime.utcnow().isoformat() + 'Z',
        'total_games': len(formatted_games),
        'games': formatted_games
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Data saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
