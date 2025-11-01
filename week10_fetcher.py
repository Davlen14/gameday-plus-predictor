#!/usr/bin/env python3
"""
Week 10 College Football Games and Lines Fetcher
Fetches all games and betting lines for Week 10 using College Football Data API
Updates: Currentweekgames.json, week10.json
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

class Week10DataFetcher:
    """Fetches Week 10 college football games and betting lines"""

    BASE_URL = "https://api.collegefootballdata.com"
    API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Gameday+ Predictor/1.0',
            'Authorization': f'Bearer {self.API_KEY}'
        })

    def get_week10_games(self) -> List[Dict[str, Any]]:
        """Get all games for Week 10"""
        try:
            current_year = 2025
            games_url = f"{self.BASE_URL}/games"
            params = {
                'year': current_year,
                'week': 10,
                'seasonType': 'regular'
            }

            print(f"📡 Fetching Week 10 games for {current_year}...")
            response = self.session.get(games_url, params=params)
            response.raise_for_status()

            games = response.json()
            print(f"✅ Found {len(games)} games for Week 10")
            return games

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching games: {e}")
            return []

    def get_rankings(self) -> List[tuple]:
        """Get current AP Poll rankings"""
        try:
            rankings_url = f"{self.BASE_URL}/rankings"
            params = {
                'year': 2025,
                'week': 10
            }

            response = self.session.get(rankings_url, params=params)
            response.raise_for_status()

            rankings_data = response.json()

            # Extract AP Poll rankings
            rankings = []
            for poll_week in rankings_data:
                for poll in poll_week.get('polls', []):
                    if poll.get('poll') == 'AP Top 25':
                        for rank in poll.get('ranks', []):
                            rankings.append((rank['rank'], rank['school']))

            print(f"✅ Found {len(rankings)} ranked teams")
            return rankings

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching rankings: {e}")
            return []

    def get_betting_lines(self, game_id: int) -> Dict[str, Any]:
        """Get betting lines for a specific game"""
        try:
            lines_url = f"{self.BASE_URL}/lines"
            params = {
                'gameId': game_id
            }

            response = self.session.get(lines_url, params=params)
            response.raise_for_status()

            lines = response.json()

            if not lines:
                return {}

            # Get the most recent lines
            latest_line = lines[0]
            betting_data = {
                'spread': latest_line.get('spread'),
                'formattedSpread': latest_line.get('formattedSpread'),
                'overUnder': latest_line.get('overUnder'),
                'provider': latest_line.get('provider', 'Unknown')
            }

            return betting_data

        except requests.exceptions.RequestException as e:
            print(f"⚠️  No betting lines for game {game_id}")
            return {}

    def format_game_for_output(self, game: Dict[str, Any], rankings: List[tuple]) -> Dict[str, Any]:
        """Format a game with all required data"""
        # Get team rankings
        home_rank = None
        away_rank = None
        for rank, school in rankings:
            if school == game.get('home_team'):
                home_rank = rank
            if school == game.get('away_team'):
                away_rank = rank

        # Get betting lines
        betting = self.get_betting_lines(game.get('id'))

        formatted_game = {
            'id': game.get('id'),
            'season': game.get('season'),
            'week': game.get('week'),
            'season_type': game.get('season_type', 'regular'),
            'start_date': game.get('start_date'),
            'start_time_tbd': game.get('start_time_tbd', False),
            'neutral_site': game.get('neutral_site', False),
            'conference_game': game.get('conference_game', False),
            'attendance': game.get('attendance'),
            'venue_id': game.get('venue_id'),
            'venue': game.get('venue'),
            'home_id': game.get('home_id'),
            'home_team': game.get('home_team'),
            'home_conference': game.get('home_conference'),
            'home_division': game.get('home_division'),
            'home_points': game.get('home_points'),
            'home_line_scores': game.get('home_line_scores', []),
            'home_post_win_prob': game.get('home_post_win_prob'),
            'home_pregame_elo': game.get('home_pregame_elo'),
            'home_postgame_elo': game.get('home_postgame_elo'),
            'away_id': game.get('away_id'),
            'away_team': game.get('away_team'),
            'away_conference': game.get('away_conference'),
            'away_division': game.get('away_division'),
            'away_points': game.get('away_points'),
            'away_line_scores': game.get('away_line_scores', []),
            'away_post_win_prob': game.get('away_post_win_prob'),
            'away_pregame_elo': game.get('away_pregame_elo'),
            'away_postgame_elo': game.get('away_postgame_elo'),
            'excitement_index': game.get('excitement_index'),
            'highlights': game.get('highlights'),
            'notes': game.get('notes'),
            # Add rankings
            'home_rank': home_rank,
            'away_rank': away_rank,
            # Add betting lines
            'spread': betting.get('spread'),
            'formatted_spread': betting.get('formattedSpread'),
            'over_under': betting.get('overUnder'),
            'betting_provider': betting.get('provider')
        }

        return formatted_game

    def fetch_and_save_week10_data(self):
        """Main method to fetch all Week 10 data and save to files"""
        print("\n" + "="*80)
        print("🏈 WEEK 10 DATA FETCHER - 2025 SEASON")
        print("="*80 + "\n")

        # Get games
        games = self.get_week10_games()
        if not games:
            print("❌ No games found for Week 10!")
            return

        # Get rankings
        rankings = self.get_rankings()

        # Format all games
        print(f"\n📝 Formatting {len(games)} games with betting lines...")
        formatted_games = []
        for idx, game in enumerate(games, 1):
            print(f"   Processing game {idx}/{len(games)}: {game.get('away_team')} @ {game.get('home_team')}")
            formatted_game = self.format_game_for_output(game, rankings)
            formatted_games.append(formatted_game)

        # Prepare output data
        output_data = {
            'week': 10,
            'season': 2025,
            'season_type': 'regular',
            'fetched_at': datetime.utcnow().isoformat() + 'Z',
            'total_games': len(formatted_games),
            'games': formatted_games
        }

        # Save to week10.json
        week10_file = 'week10.json'
        with open(week10_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\n✅ Saved to {week10_file}")

        # Also save to Currentweekgames.json (for backward compatibility)
        current_week_file = 'Currentweekgames.json'
        with open(current_week_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ Updated {current_week_file}")

        # Print summary
        print("\n" + "="*80)
        print("📊 SUMMARY")
        print("="*80)
        print(f"   Total Games: {len(formatted_games)}")
        
        conf_games = sum(1 for g in formatted_games if g.get('conference_game'))
        print(f"   Conference Games: {conf_games}")
        print(f"   Non-Conference Games: {len(formatted_games) - conf_games}")
        
        games_with_lines = sum(1 for g in formatted_games if g.get('spread') is not None)
        print(f"   Games with Betting Lines: {games_with_lines}")
        
        ranked_matchups = sum(1 for g in formatted_games if g.get('home_rank') and g.get('away_rank'))
        print(f"   Ranked vs Ranked: {ranked_matchups}")
        
        print("\n✅ Week 10 data ready for predictions!")
        print("="*80 + "\n")


def main():
    fetcher = Week10DataFetcher()
    fetcher.fetch_and_save_week10_data()


if __name__ == "__main__":
    main()
