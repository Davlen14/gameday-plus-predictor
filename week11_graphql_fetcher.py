#!/usr/bin/env python3
"""
Week 11 College Football Games Fetcher using GraphQL
Fetches all games and betting lines for Week 11 using College Football Data GraphQL API
Generates Currentweekgames.json format
"""

import requests
import json
from datetime import datetime, timezone
from typing import Dict, List, Any
from zoneinfo import ZoneInfo

class Week11GraphQLFetcher:
    """Fetches Week 11 college football games and betting lines using GraphQL"""

    BASE_URL = "https://api.collegefootballdata.com"
    GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
    API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Gameday+ Predictor/1.0',
            'Authorization': f'Bearer {self.API_KEY}'
        })

    def get_week11_games(self) -> List[Dict[str, Any]]:
        """Get all games for Week 11 with media info using GraphQL"""
        try:
            # GraphQL query to get games with media info
            query = """
            query GetWeek11Games {
              game(where: {
                season: {_eq: 2025},
                week: {_eq: 11},
                seasonType: {_eq: "regular"}
              }) {
                id
                season
                week
                homeTeam
                awayTeam
                homeConference
                awayConference
                homeClassification
                awayClassification
                startDate
                homePoints
                awayPoints
                neutralSite
                conferenceGame
                mediaInfo {
                  mediaType
                  name
                }
              }
            }
            """

            print(f"📡 Fetching Week 11 games via GraphQL...")
            response = self.session.post(
                self.GRAPHQL_URL,
                json={'query': query},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()
            games = data.get('data', {}).get('game', [])
            
            print(f"✅ Found {len(games)} total games for Week 11")
            
            # Filter to FBS only
            fbs_games = [g for g in games if g.get('homeClassification') == 'fbs' and g.get('awayClassification') == 'fbs']
            print(f"📊 Filtered to {len(fbs_games)} FBS games")
            
            return fbs_games

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching games: {e}")
            return []

    def get_rankings(self) -> List[tuple]:
        """Get current AP Poll rankings"""
        try:
            rankings_url = f"{self.BASE_URL}/rankings"
            params = {
                'year': 2025,
                'week': 11
            }

            response = self.session.get(rankings_url, params=params)
            response.raise_for_status()

            rankings_data = response.json()
            
            # Find AP Poll specifically
            for poll_week in rankings_data:
                for poll in poll_week.get('polls', []):
                    if poll.get('poll') == 'AP Top 25':
                        ranked_teams = [(team['school'], team['rank']) for team in poll.get('ranks', [])]
                        return ranked_teams[:25]
            
            return []

        except Exception as e:
            print(f"⚠️  Error fetching rankings: {e}")
            return []

    def get_game_lines(self, game_id: int) -> Dict[str, Any]:
        """Get betting lines for a specific game"""
        try:
            lines_url = f"{self.BASE_URL}/lines"
            params = {'gameId': game_id}

            response = self.session.get(lines_url, params=params)
            response.raise_for_status()

            lines_data = response.json()

            if lines_data and isinstance(lines_data, list) and len(lines_data) > 0:
                game_lines = lines_data[0]
                lines = game_lines.get('lines', [])

                if lines:
                    providers = {}
                    for line in lines:
                        provider = line.get('provider', 'Unknown')
                        if provider not in providers:
                            providers[provider] = {
                                'provider': provider,
                                'providerId': 888888 if provider == 'DraftKings' else 58,
                                'spread': line.get('spread'),
                                'spreadOpen': line.get('spreadOpen'),
                                'overUnder': line.get('overUnder'),
                                'overUnderOpen': line.get('overUnderOpen'),
                                'moneylineHome': line.get('homeMoneyline'),
                                'moneylineAway': line.get('awayMoneyline')
                            }

                    # Calculate consensus
                    spreads = [p['spread'] for p in providers.values() if p['spread'] is not None]
                    totals = [p['overUnder'] for p in providers.values() if p['overUnder'] is not None]

                    return {
                        'totalProviders': len(providers),
                        'consensus': {
                            'spread': sum(spreads) / len(spreads) if spreads else None,
                            'total': sum(totals) / len(totals) if totals else None,
                            'spreadRange': {
                                'min': min(spreads) if spreads else None,
                                'max': max(spreads) if spreads else None
                            },
                            'totalRange': {
                                'min': min(totals) if totals else None,
                                'max': max(totals) if totals else None
                            }
                        },
                        'allProviders': list(providers.values())
                    }

            return None

        except Exception as e:
            print(f"⚠️  Error fetching lines for game {game_id}: {e}")
            return None

    def format_game(self, game: Dict, rankings_dict: Dict) -> Dict:
        """Format game data to match Currentweekgames.json structure"""
        game_id = game.get('id')
        home_team = game.get('homeTeam', 'Unknown')
        away_team = game.get('awayTeam', 'Unknown')
        
        home_rank = rankings_dict.get(home_team)
        away_rank = rankings_dict.get(away_team)

        # Parse datetime - Convert from UTC to Eastern Time
        start_date = game.get('startDate', '')
        try:
            # Parse the UTC datetime from API (format: "2025-11-08T17:00:00")
            dt_utc = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
            
            # Convert to Eastern Time
            dt_et = dt_utc.astimezone(ZoneInfo("America/New_York"))
            
            formatted_date = dt_et.strftime("%B %d, %Y at %I:%M %p ET")
            date_only = dt_et.strftime("%Y-%m-%d")
            time_only = dt_et.strftime("%H:%M")
            day_of_week = dt_et.strftime("%A")
        except:
            formatted_date = "TBD"
            date_only = "TBD"
            time_only = "TBD"
            day_of_week = "TBD"
        
        # Extract media/network info from GraphQL response
        media_info = game.get('mediaInfo', [])
        network = "TBD"
        if media_info:
            # Find TV broadcast (prioritize over streaming)
            for media in media_info:
                if media.get('mediaType', '').lower() in ['tv', 'television']:
                    network = media.get('name', 'TBD')
                    break
            # If no TV, use first media source
            if network == "TBD" and media_info:
                network = media_info[0].get('name', 'TBD')

        # Get betting lines
        betting_lines = self.get_game_lines(game_id)

        return {
            'gameId': game_id,
            'datetime': {
                'raw': start_date,
                'formatted': formatted_date,
                'date': date_only,
                'time': time_only,
                'dayOfWeek': day_of_week,
                'timeZone': 'ET'
            },
            'homeTeam': {
                'name': home_team,
                'rank': home_rank,
                'conference': game.get('homeConference', 'Unknown'),
                'division': None,
                'mascot': None,
                'score': game.get('homePoints')
            },
            'awayTeam': {
                'name': away_team,
                'rank': away_rank,
                'conference': game.get('awayConference', 'Unknown'),
                'division': None,
                'mascot': None,
                'score': game.get('awayPoints')
            },
            'media': {
                'network': network,
                'mediaInfo': media_info
            },
            'venue': {
                'name': None,
                'city': None,
                'state': None
            },
            'gameInfo': {
                'neutralSite': game.get('neutralSite', False),
                'conferenceGame': game.get('conferenceGame', False),
                'attendance': None,
                'week': 11,
                'season': 2025,
                'seasonType': 'regular'
            },
            'bettingLines': betting_lines if betting_lines else {
                'totalProviders': 0,
                'consensus': None,
                'allProviders': []
            }
        }

    def generate_week11_data(self):
        """Main function to generate Currentweekgames.json"""
        print("🏈 Week 11 College Football Data Fetcher (GraphQL)")
        print("=" * 50)
        
        # Fetch games with media
        games = self.get_week11_games()
        
        if not games:
            print("❌ No games found!")
            return
        
        # Get rankings
        print("📊 Fetching AP Poll rankings...")
        rankings = self.get_rankings()
        rankings_dict = dict(rankings)
        print(f"✅ Found {len(rankings)} ranked teams")
        
        # Format all games
        print(f"🔄 Processing {len(games)} games...")
        formatted_games = []
        
        for game in games:
            formatted_game = self.format_game(game, rankings_dict)
            formatted_games.append(formatted_game)
        
        # Calculate summary stats
        ranked_matchups = sum(1 for g in formatted_games if g['homeTeam']['rank'] or g['awayTeam']['rank'])
        ranked_vs_ranked = sum(1 for g in formatted_games if g['homeTeam']['rank'] and g['awayTeam']['rank'])
        games_with_lines = sum(1 for g in formatted_games if g['bettingLines']['totalProviders'] > 0)
        
        # Get top ranked teams
        top_ranked = sorted(
            [(g['homeTeam']['name'], g['homeTeam']['rank']) for g in formatted_games if g['homeTeam']['rank']] +
            [(g['awayTeam']['name'], g['awayTeam']['rank']) for g in formatted_games if g['awayTeam']['rank']],
            key=lambda x: x[1]
        )[:10]
        
        # Build final output
        output = {
            'summary': {
                'generatedAt': datetime.now().isoformat(),
                'week': 11,
                'year': 2025,
                'seasonType': 'regular',
                'totalGames': len(formatted_games),
                'power5Games': sum(1 for g in formatted_games if g['homeTeam']['conference'] in ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12']),
                'rankedMatchups': ranked_matchups,
                'rankedVsRanked': ranked_vs_ranked,
                'topRankedTeams': top_ranked,
                'bettingLinesAvailable': games_with_lines,
                'totalBettingProviders': max([g['bettingLines']['totalProviders'] for g in formatted_games], default=0),
                'gamesWithConsensusLines': sum(1 for g in formatted_games if g['bettingLines'].get('consensus')),
                'gamesWithScores': sum(1 for g in formatted_games if g['homeTeam']['score'] is not None),
                'sortingInfo': 'Games sorted by highest rank (lowest rank number) then by conference alphabetically'
            },
            'games': {
                'all': formatted_games
            }
        }
        
        # Save to file
        with open('Currentweekgames.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Week 11 data saved to Currentweekgames.json")
        print(f"   Total games: {len(formatted_games)}")
        print(f"   Ranked matchups: {ranked_matchups}")
        print(f"   Ranked vs Ranked: {ranked_vs_ranked}")
        print(f"   Games with betting lines: {games_with_lines}")
        print(f"   Games with media info: {sum(1 for g in formatted_games if g['media']['network'] != 'TBD')}")

if __name__ == '__main__':
    fetcher = Week11GraphQLFetcher()
    fetcher.generate_week11_data()
