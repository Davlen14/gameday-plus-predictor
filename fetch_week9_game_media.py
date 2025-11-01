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

FBS_TEAM_IDS = load_fbs_team_ids()

async def fetch_week10_fbs_games():
    """Fetch all Week 10 FBS games with media information"""
    
    query = """
query Week10FBSGames($year: smallint!, $week: smallint!) {
        games: game(
            where: {
                season: {_eq: $year},
                week: {_eq: $week},
                seasonType: {_eq: "regular"}
            },
            orderBy: {startDate: ASC}
        ) {
            id
            season
            week
            seasonType
            startDate
            homeTeam
            awayTeam
            homeTeamId
            awayTeamId
            homePoints
            awayPoints
            weather {
                gameId
                temperature
                windSpeed
                precipitation
                humidity
                dewpoint
                pressure
                weatherConditionCode
                windDirection
                windGust
            }
            mediaInfo {
                mediaType
                name
            }
        }
    }
    """
    
    variables = {
        "year": YEAR,
        "week": WEEK
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    print(f"🏈 Fetching Week {WEEK} FBS games for {YEAR}...")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GRAPHQL_URL, headers=headers, json=payload) as response:
            result = await response.json()
            
            if 'errors' in result:
                print(f"❌ GraphQL errors: {result['errors']}")
                return None
            
            return result.get('data', {}).get('games', [])

async def main():
    """Main execution function"""
    
    games = await fetch_week10_fbs_games()
    
    if not games:
        print("❌ No games found or error occurred")
        return
    
    # Filter for FBS games only (both teams must be FBS)
    fbs_games = []
    for game in games:
        home_team_id = game.get('homeTeamId')
        away_team_id = game.get('awayTeamId')
        
        # Check if both teams are in the FBS team ID set
        if home_team_id in FBS_TEAM_IDS and away_team_id in FBS_TEAM_IDS:
            fbs_games.append(game)
    
    print(f"✅ Found {len(fbs_games)} FBS games for Week {WEEK}")
    
    # Format the output
    output = {
        "meta": {
            "season": YEAR,
            "week": WEEK,
            "total_games": len(fbs_games),
            "fetched_at": datetime.now().isoformat(),
            "description": f"Week {WEEK} FBS game media and scheduling information"
        },
        "games": []
    }
    
    for game in fbs_games:
        # Parse start date
        start_date_raw = game.get('startDate', '')
        game_date = "TBD"
        game_time = "TBD"
        
        if start_date_raw:
            try:
                # Parse UTC time and convert to Eastern Time
                from datetime import timezone, timedelta
                
                dt = datetime.fromisoformat(start_date_raw.replace('Z', '+00:00'))
                # Convert from UTC to Eastern Time (UTC-5 for EST, UTC-4 for EDT)
                # October 2025 is still EDT (daylight saving)
                eastern_offset = timedelta(hours=-4)
                dt_eastern = dt + eastern_offset
                
                game_date = dt_eastern.strftime('%B %d, %Y')
                game_time = dt_eastern.strftime('%I:%M %p ET')
                raw_start_date = dt_eastern.strftime('%Y-%m-%dT%H:%M:%S')
            except Exception as e:
                print(f"⚠️ Error parsing date {start_date_raw}: {e}")
                game_date = start_date_raw
                raw_start_date = start_date_raw
        else:
            raw_start_date = None
        
        # Extract TV network
        tv_network = "TBD"
        radio_info = []
        streaming_info = []
        
        media_info = game.get('mediaInfo', [])
        for media in media_info:
            media_type = media.get('mediaType', '').lower()
            if media_type in ['tv', 'television']:
                tv_network = media.get('name', 'TBD')
            elif media_type == 'radio':
                radio_info.append({
                    'name': media.get('name', 'Unknown')
                })
            elif media_type in ['web', 'streaming', 'internet']:
                streaming_info.append({
                    'name': media.get('name', 'Unknown')
                })
        
        # Build game object
        game_obj = {
            "game_id": game.get('id'),
            "matchup": {
                "away": {
                    "team": game.get('awayTeam'),
                    "team_id": game.get('awayTeamId'),
                    "conference": game.get('awayTeamInfo', {}).get('conference'),
                    "points": game.get('awayPoints')
                },
                "home": {
                    "team": game.get('homeTeam'),
                    "team_id": game.get('homeTeamId'),
                    "conference": game.get('homeTeamInfo', {}).get('conference'),
                    "points": game.get('homePoints')
                }
            },
            "scheduling": {
                "date": game_date,
                "time": game_time,
                "raw_start_date": raw_start_date
            },
            "media": {
                "tv_network": tv_network,
                "radio": radio_info,
                "streaming": streaming_info,
                "all_media": media_info
            },
            "weather": game.get('weather', {})
        }
        
        output['games'].append(game_obj)
    
    # Write to JSON file
    output_file = 'week9_game_media.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Successfully saved {len(fbs_games)} games to {output_file}")
    
    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   Total FBS Games: {len(fbs_games)}")
    
    tv_games = sum(1 for g in output['games'] if g['media']['tv_network'] != 'TBD')
    print(f"   Games with TV coverage: {tv_games}")
    
    # Count games by network
    networks = {}
    for game in output['games']:
        network = game['media']['tv_network']
        networks[network] = networks.get(network, 0) + 1
    
    print(f"\n📺 TV NETWORKS:")
    for network, count in sorted(networks.items(), key=lambda x: x[1], reverse=True):
        print(f"   {network}: {count} game(s)")
    
    # Show sample games
    print(f"\n🎮 SAMPLE GAMES:")
    for i, game in enumerate(output['games'][:5]):
        away = game['matchup']['away']['team']
        home = game['matchup']['home']['team']
        network = game['media']['tv_network']
        date = game['scheduling']['date']
        time = game['scheduling']['time']
        print(f"   {i+1}. {away} @ {home}")
        print(f"      {date} at {time} on {network}")

if __name__ == "__main__":
    asyncio.run(main())
