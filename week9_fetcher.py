#!/usr/bin/env python3
"""
Week 11 College Football Games and Lines Fetcher
Fetches all games and betting lines for Week 11 using College Football Data API
Generates Currentweekgames.json format
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

class Week10DataFetcher:
    """Fetches Week 11 college football games and betting lines"""

    BASE_URL = "https://api.collegefootballdata.com"
    API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Gameday+ Predictor/1.0',
            'Authorization': f'Bearer {self.API_KEY}'
        })

    def get_week10_games(self) -> List[Dict[str, Any]]:
        """Get all games for Week 11 with media info"""
        try:
            current_year = 2025
            games_url = f"{self.BASE_URL}/games"
            params = {
                'year': current_year,
                'week': 11,
                'seasonType': 'regular'
            }

            print(f"📡 Fetching Week 11 games for {current_year}...")
            response = self.session.get(games_url, params=params)
            response.raise_for_status()

            games = response.json()
            print(f"✅ Found {len(games)} games for Week 11")
            
            # Enhance games with media info
            print(f"📺 Fetching media info for games...")
            for game in games:
                game['mediaInfo'] = self.get_game_media(game['id'])
            
            return games

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching games: {e}")
            return []
    
    def get_game_media(self, game_id: int) -> List[Dict[str, str]]:
        """Get media info (TV network) for a specific game using GraphQL"""
        try:
            # GraphQL endpoint for College Football Data API
            graphql_url = "https://apiv2.collegefootballdata.com/graphql"
            
            query = """
            query GetGameMedia($gameId: Int!) {
              game(where: {id: {_eq: $gameId}}) {
                id
                mediaInfo {
                  mediaType
                  name
                }
              }
            }
            """
            
            payload = {
                "query": query,
                "variables": {
                    "gameId": game_id
                }
            }
            
            response = self.session.post(graphql_url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract media info from GraphQL response
            if data.get('data') and data['data'].get('game'):
                games = data['data']['game']
                if games and len(games) > 0:
                    return games[0].get('mediaInfo', [])
            
            return []

        except Exception as e:
            # Don't fail if media not available
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
            
            # Find AP Poll specifically (not Coaches Poll)
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

                    all_providers = list(providers.values())
                    spreads = [p['spread'] for p in all_providers if p['spread']]
                    overs = [p['overUnder'] for p in all_providers if p['overUnder']]

                    return {
                        'totalProviders': len(all_providers),
                        'consensus': None,
                        'allProviders': all_providers,
                        'summary': {
                            'avgSpread': sum(spreads) / len(spreads) if spreads else None,
                            'avgOverUnder': sum(overs) / len(overs) if overs else None,
                            'spreadRange': {
                                'min': min(spreads) if spreads else None,
                                'max': max(spreads) if spreads else None
                            },
                            'overUnderRange': {
                                'min': min(overs) if overs else None,
                                'max': max(overs) if overs else None
                            }
                        }
                    }

            return None

        except Exception as e:
            print(f"⚠️  Error fetching lines for game {game_id}: {e}")
            return None

    def determine_matchup_type(self, home_rank, away_rank) -> str:
        """Determine matchup type based on rankings"""
        home_ranked = home_rank is not None
        away_ranked = away_rank is not None

        if home_ranked and away_ranked:
            return "ranked_vs_ranked"
        elif home_ranked:
            return "ranked_vs_unranked"
        elif away_ranked:
            return "unranked_vs_ranked"
        else:
            return "unranked_vs_unranked"

    def format_game(self, game: Dict, rankings_dict: Dict) -> Dict:
        """Format game data to match Currentweekgames.json structure"""
        game_id = game.get('id')
        home_team = game.get('homeTeam', 'Unknown')
        away_team = game.get('awayTeam', 'Unknown')
        
        home_rank = rankings_dict.get(home_team)
        away_rank = rankings_dict.get(away_team)

        # Parse datetime
        start_date = game.get('startDate', '')
        try:
            dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            formatted_date = dt.strftime("%B %d, %Y at %I:%M %p %Z")
            date_only = dt.strftime("%Y-%m-%d")
            time_only = dt.strftime("%H:%M")
            day_of_week = dt.strftime("%A")
        except:
            formatted_date = "TBD"
            date_only = "TBD"
            time_only = "TBD"
            day_of_week = "TBD"
        
        # Extract media/network info
        media_info = game.get('mediaInfo', [])
        network = "TBD"
        if media_info:
            # Find TV broadcast (prioritize over streaming)
            for media in media_info:
                if media.get('mediaType') in ['TV', 'television', 'tv']:
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
                'score': None
            },
            'awayTeam': {
                'name': away_team,
                'rank': away_rank,
                'conference': game.get('awayConference', 'Unknown'),
                'division': None,
                'mascot': None,
                'score': None
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
            'bettingLines': betting_lines,
            'matchupType': self.determine_matchup_type(home_rank, away_rank)
        }

    def run(self):
        """Main execution"""
        print("🏈 Week 11 College Football Data Fetcher")
        print("=" * 50)

        # Get games
        games = self.get_week10_games()
        if not games:
            print("❌ No games found for Week 11")
            return

        # Filter FBS only
        fbs_games = [g for g in games 
                     if g.get('homeClassification') == 'fbs' and g.get('awayClassification') == 'fbs']
        print(f"📊 Filtered to {len(fbs_games)} FBS games")

        # Get rankings
        rankings = self.get_rankings()
        rankings_dict = {team: rank for team, rank in rankings}

        # Count ranked matchups
        ranked_games = [g for g in fbs_games 
                       if rankings_dict.get(g.get('homeTeam')) or rankings_dict.get(g.get('awayTeam'))]
        ranked_vs_ranked = [g for g in fbs_games 
                           if rankings_dict.get(g.get('homeTeam')) and rankings_dict.get(g.get('awayTeam'))]

        # Format games
        formatted_games = [self.format_game(g, rankings_dict) for g in fbs_games]

        # Count betting lines
        games_with_lines = sum(1 for g in formatted_games if g.get('bettingLines'))

        # Build output
        output = {
            'summary': {
                'generatedAt': datetime.now().isoformat(),
                'week': 11,
                'year': datetime.now().year,
                'seasonType': 'regular',
                'totalGames': len(fbs_games),
                'power5Games': len([g for g in fbs_games if g.get('homeConference') in ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12']]),
                'rankedMatchups': len(ranked_games),
                'rankedVsRanked': len(ranked_vs_ranked),
                'topRankedTeams': rankings[:10],
                'bettingLinesAvailable': games_with_lines,
                'totalBettingProviders': 9,
                'gamesWithConsensusLines': 0,
                'gamesWithScores': 0,
                'sortingInfo': 'Games sorted by highest rank (lowest rank number) then by conference alphabetically'
            },
            'games': {
                'all': formatted_games
            }
        }

        # Save to file
        with open('Currentweekgames.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✅ Week 11 data saved to Currentweekgames.json")
        print(f"   Total games: {len(fbs_games)}")


def main():
    fetcher = Week10DataFetcher()
    fetcher.run()

if __name__ == "__main__":
    main()
