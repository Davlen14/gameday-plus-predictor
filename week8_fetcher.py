#!/usr/bin/env python3
"""
Week 8 College Football Games and Lines Fetcher
Fetches all games and betting lines for Week 8 using College Football Data API
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class Week8DataFetcher:
    """Fetches Week 8 college football games and betting lines"""

    BASE_URL = "https://api.collegefootballdata.com"
    API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Gameday+ Predictor/1.0',
            'Authorization': f'Bearer {self.API_KEY}'
        })

    def get_week8_games(self) -> List[Dict[str, Any]]:
        """Get all games for Week 8 of the current season"""
        try:
            # Get current year
            current_year = datetime.now().year

            # Fetch games for Week 8
            games_url = f"{self.BASE_URL}/games"
            params = {
                'year': current_year,
                'week': 8,
                'seasonType': 'regular'
            }

            print(f"📡 Fetching Week 8 games for {current_year}...")
            response = self.session.get(games_url, params=params)
            response.raise_for_status()

            games = response.json()
            print(f"✅ Found {len(games)} games for Week 8")

            return games

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching games: {e}")
            return []

    def get_game_lines(self, game_id: int, home_team: str = None, away_team: str = None) -> Dict[str, Any]:
        """Get betting lines for a specific game"""
        try:
            lines_url = f"{self.BASE_URL}/lines"
            params = {
                'gameId': game_id
            }

            response = self.session.get(lines_url, params=params)
            response.raise_for_status()

            lines_data = response.json()

            if lines_data and isinstance(lines_data, list) and len(lines_data) > 0:
                game_lines = lines_data[0]
                lines = game_lines.get('lines', [])

                if lines:
                    # Get the first available line (usually the most recent)
                    latest_line = lines[0]
                    
                    # Get moneylines to determine favorite
                    home_moneyline = latest_line.get('homeMoneyline', 0)
                    away_moneyline = latest_line.get('awayMoneyline', 0)
                    
                    # Format the spread for display with team name
                    spread = latest_line.get('spread')
                    formatted_spread = 'N/A'
                    
                    if spread is not None and spread != 'N/A' and home_team and away_team:
                        try:
                            spread_float = float(spread)
                            
                            # Determine favorite based on moneyline (more negative = favorite)
                            # If home has negative moneyline (e.g., -200), they're favored
                            # If away has negative moneyline, they're favored
                            if home_moneyline and away_moneyline:
                                if home_moneyline < away_moneyline:
                                    # Home team is favorite
                                    favorite_team = home_team
                                    favorite_spread = spread_float
                                else:
                                    # Away team is favorite
                                    favorite_team = away_team
                                    favorite_spread = -spread_float
                                
                                # Format: "TeamName -7.5" (negative for favorite)
                                if favorite_spread < 0:
                                    formatted_spread = f"{favorite_team} {favorite_spread}"
                                else:
                                    formatted_spread = f"{favorite_team} +{favorite_spread}"
                            else:
                                # Fallback: use spread sign to determine
                                if spread_float < 0:
                                    # Negative spread = home team favored
                                    formatted_spread = f"{home_team} {spread_float}"
                                else:
                                    # Positive spread = home team underdog, so away is favored
                                    formatted_spread = f"{away_team} -{spread_float}"
                        except (ValueError, TypeError):
                            formatted_spread = 'N/A'
                    elif spread is not None and spread != 'N/A':
                        # No team names provided, just format the number
                        try:
                            spread_float = float(spread)
                            formatted_spread = f"{spread_float:+.1f}"
                        except (ValueError, TypeError):
                            formatted_spread = 'N/A'

                    return {
                        'game_id': game_id,
                        'lines_available': True,
                        'spread': spread,
                        'formatted_spread': formatted_spread,
                        'over_under': latest_line.get('overUnder', 'N/A'),
                        'home_moneyline': latest_line.get('homeMoneyline', 'N/A'),
                        'away_moneyline': latest_line.get('awayMoneyline', 'N/A'),
                        'provider': latest_line.get('provider', 'Unknown'),
                        'spread_open': latest_line.get('spreadOpen', 'N/A'),
                        'over_under_open': latest_line.get('overUnderOpen', 'N/A'),
                        'all_providers': [line.get('provider') for line in lines],
                        'last_updated': datetime.now().isoformat()
                    }

            return {
                'game_id': game_id,
                'lines_available': False,
                'spread': 'N/A',
                'formatted_spread': 'N/A',
                'over_under': 'N/A',
                'home_moneyline': 'N/A',
                'away_moneyline': 'N/A',
                'provider': 'No lines available',
                'spread_open': 'N/A',
                'over_under_open': 'N/A',
                'all_providers': [],
                'last_updated': datetime.now().isoformat()
            }

        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error fetching lines for game {game_id}: {e}")
            return {
                'game_id': game_id,
                'lines_available': False,
                'spread': 'N/A',
                'formatted_spread': 'N/A',
                'over_under': 'N/A',
                'home_moneyline': 'N/A',
                'away_moneyline': 'N/A',
                'provider': 'Error fetching lines',
                'spread_open': 'N/A',
                'over_under_open': 'N/A',
                'all_providers': [],
                'last_updated': datetime.now().isoformat()
            }

    def enrich_games_with_lines(self, games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add betting lines to each game, filtering for FBS only"""
        # Filter for FBS games only
        fbs_games = [
            game for game in games
            if game.get('homeClassification') == 'fbs' and game.get('awayClassification') == 'fbs'
        ]

        print(f"📊 Filtered to {len(fbs_games)} FBS games (out of {len(games)} total games)")

        enriched_games = []

        print("� Fetching betting lines for FBS games...")
        for i, game in enumerate(fbs_games, 1):
            home_team = game.get('homeTeam', 'Unknown')
            away_team = game.get('awayTeam', 'Unknown')
            print(f"  {i}/{len(fbs_games)}: {home_team} vs {away_team}")

            game_id = game.get('id')
            if game_id:
                lines = self.get_game_lines(game_id, home_team, away_team)
                enriched_game = {
                    **game,
                    'betting_lines': lines
                }
            else:
                enriched_game = {
                    **game,
                    'betting_lines': {
                        'game_id': None,
                        'lines_available': False,
                        'error': 'No game ID available'
                    }
                }

            enriched_games.append(enriched_game)

        return enriched_games

    def save_to_json(self, data: Dict[str, Any], filename: str = "week8.json"):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"💾 Data saved to {filename}")
            print(f"📊 Total games: {len(data.get('games', []))}")
            print(f"📈 Games with lines: {sum(1 for g in data.get('games', []) if g.get('betting_lines', {}).get('lines_available', False))}")

        except Exception as e:
            print(f"❌ Error saving to file: {e}")

    def run(self):
        """Main execution method"""
        print("🏈 Week 8 College Football Data Fetcher")
        print("=" * 50)

        # Get games
        games = self.get_week8_games()

        if not games:
            print("❌ No games found for Week 8")
            return

        # Enrich with betting lines
        enriched_games = self.enrich_games_with_lines(games)

        # Prepare final data structure
        data = {
            'metadata': {
                'week': 8,
                'season': datetime.now().year,
                'fetched_at': datetime.now().isoformat(),
                'total_games': len(enriched_games),
                'total_raw_games': len(games),
                'filter': 'FBS only',
                'api_source': 'College Football Data API'
            },
            'games': enriched_games
        }

        # Save to file
        self.save_to_json(data, "week8.json")

        print("\n🎉 Week 8 data fetch complete!")
        print("📁 File saved as: week8.json")

def main():
    """Main entry point"""
    try:
        fetcher = Week8DataFetcher()
        fetcher.run()
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()