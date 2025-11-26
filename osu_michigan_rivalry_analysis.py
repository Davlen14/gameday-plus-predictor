#!/usr/bin/env python3
"""
OSU vs Michigan Rivalry Analysis (2000-2024)
Comprehensive historical analysis using College Football Data API
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import statistics

class RivalryAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.collegefootballdata.com"
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        self.graphql_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Load team ID mappings
        self.team_ids = self._load_team_ids()
    
    def _load_team_ids(self) -> Dict[str, int]:
        """Load team name to ID mappings from fbs.json"""
        try:
            with open('fbs.json', 'r') as f:
                teams = json.load(f)
                return {team['school']: team['id'] for team in teams}
        except Exception as e:
            print(f"⚠️  Could not load team IDs: {e}")
            return {}
        
    def get_game_data_graphql(self, year: int, week: int, home_team: str, away_team: str) -> Dict:
        """Fetch comprehensive game data using GraphQL API"""
        home_id = self.team_ids.get(home_team)
        away_id = self.team_ids.get(away_team)
        
        if not home_id or not away_id:
            return {}
        
        query = """
        query RivalryGameData($homeTeamId: Int!, $awayTeamId: Int!, $year: smallint!, $week: smallint!, $yearInt: Int!) {
            currentGame: game(
                where: {
                    homeTeamId: {_eq: $homeTeamId},
                    awayTeamId: {_eq: $awayTeamId},
                    season: {_eq: $year},
                    week: {_eq: $week}
                }
            ) {
                id
                weather {
                    temperature
                    windSpeed
                    precipitation
                    humidity
                    pressure
                    weatherConditionCode
                    windDirection
                }
                lines {
                    spread
                    overUnder
                    spreadOpen
                    overUnderOpen
                    moneylineHome
                    moneylineAway
                    provider {
                        id
                        name
                    }
                }
            }
            
            # Poll rankings
            homeRank: pollRank(
                where: {
                    poll: {
                        season: {_eq: $yearInt},
                        week: {_eq: $week}
                    },
                    team: {teamId: {_eq: $homeTeamId}}
                }
            ) {
                rank
                team {
                    school
                }
                poll {
                    pollType {
                        name
                    }
                }
            }
            
            awayRank: pollRank(
                where: {
                    poll: {
                        season: {_eq: $yearInt},
                        week: {_eq: $week}
                    },
                    team: {teamId: {_eq: $awayTeamId}}
                }
            ) {
                rank
                team {
                    school
                }
                poll {
                    pollType {
                        name
                    }
                }
            }
        }
        """
        
        variables = {
            "homeTeamId": home_id,
            "awayTeamId": away_id,
            "year": year,
            "yearInt": year,
            "week": week
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=self.graphql_headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                print(f"  ⚠ GraphQL errors: {data['errors'][0].get('message', 'Unknown error')}")
                return {}
            
            result = data.get('data', {})
            game_data = result.get('currentGame', [])
            home_ranks = result.get('homeRank', [])
            away_ranks = result.get('awayRank', [])
            
            # Get AP Poll ranks
            home_rank = None
            away_rank = None
            
            for rank_data in home_ranks:
                if rank_data.get('poll', {}).get('pollType', {}).get('name') == 'AP Top 25':
                    home_rank = rank_data.get('rank')
                    break
            
            for rank_data in away_ranks:
                if rank_data.get('poll', {}).get('pollType', {}).get('name') == 'AP Top 25':
                    away_rank = rank_data.get('rank')
                    break
            
            if game_data and len(game_data) > 0:
                game = game_data[0]
                return {
                    'rankings': {
                        'home_rank': home_rank,
                        'away_rank': away_rank
                    },
                    'weather': game.get('weather'),
                    'betting_lines': game.get('lines', [])
                }
            
            return {
                'rankings': {
                    'home_rank': home_rank,
                    'away_rank': away_rank
                },
                'weather': None,
                'betting_lines': []
            }
            
        except Exception as e:
            print(f"  ⚠ GraphQL error for {year} Week {week}: {str(e)}")
            return {}
    
    def get_rivalry_games(self, team1: str = "Ohio State", team2: str = "Michigan", 
                          start_year: int = 2000, end_year: int = 2024) -> List[Dict]:
        """Fetch all games between OSU and Michigan using matchup endpoint"""
        url = f"{self.base_url}/teams/matchup"
        params = {
            "team1": team1,
            "team2": team2,
            "minYear": start_year,
            "maxYear": end_year
        }
        
        try:
            print(f"Fetching matchup data: {team1} vs {team2} ({start_year}-{end_year})")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            all_games = data.get('games', [])
            print(f"✅ Found {len(all_games)} games in the rivalry")
            
            for game in all_games:
                year = game.get('season')
                week = game.get('week')
                home = game.get('homeTeam')
                away = game.get('awayTeam')
                print(f"  ✓ {year} Week {week}: {home} vs {away}")
            
            return all_games
            
        except Exception as e:
            print(f"✗ Error fetching matchup data: {str(e)}")
            return []
    
    def enrich_game_data(self, game: Dict) -> Dict:
        """Enrich game with additional data: SP+, weather, rankings, betting lines"""
        year = game.get('season')
        week = game.get('week')
        game_id = game.get('id')
        home_team = game.get('homeTeam') or game.get('home_team')
        away_team = game.get('awayTeam') or game.get('away_team')
        
        # Get comprehensive game data via GraphQL
        graphql_data = self.get_game_data_graphql(year, week, home_team, away_team)
        
        enriched = {
            'basic_info': game,
            'sp_ratings': self.get_sp_ratings(year, home_team, away_team),
            'rankings': graphql_data.get('rankings', self.get_rankings(year, week, home_team, away_team)),
            'weather': graphql_data.get('weather'),
            'betting_lines': graphql_data.get('betting_lines', []),
            'team_records': self.get_team_records(year, week, home_team, away_team)
        }
        
        return enriched
    
    def get_sp_ratings(self, year: int, home_team: str, away_team: str) -> Dict:
        """Get SP+ ratings for both teams"""
        url = f"{self.base_url}/ratings/sp"
        params = {"year": year}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            ratings = response.json()
            
            home_rating = next((r for r in ratings if r.get('team') == home_team), None)
            away_rating = next((r for r in ratings if r.get('team') == away_team), None)
            
            return {
                'home': home_rating,
                'away': away_rating
            }
        except Exception as e:
            print(f"  ⚠ SP+ ratings unavailable for {year}: {str(e)}")
            return {'home': None, 'away': None}
    
    def get_rankings(self, year: int, week: int, home_team: str, away_team: str) -> Dict:
        """Get AP Poll rankings for both teams"""
        url = f"{self.base_url}/rankings"
        params = {
            "year": year,
            "week": week,
            "seasonType": "regular"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            rankings = response.json()
            
            home_rank = None
            away_rank = None
            
            for poll in rankings:
                if poll.get('poll') == 'AP Top 25':
                    for rank in poll.get('ranks', []):
                        if rank.get('school') == home_team:
                            home_rank = rank.get('rank')
                        if rank.get('school') == away_team:
                            away_rank = rank.get('rank')
            
            return {
                'home_rank': home_rank,
                'away_rank': away_rank
            }
        except Exception as e:
            print(f"  ⚠ Rankings unavailable for {year} Week {week}: {str(e)}")
            return {'home_rank': None, 'away_rank': None}
    
    def get_weather(self, game_id: int) -> Dict:
        """Get weather data for the game"""
        if not game_id:
            return None
            
        url = f"{self.base_url}/games/weather"
        params = {"gameId": game_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            weather_data = response.json()
            return weather_data[0] if weather_data else None
        except Exception as e:
            return None
    
    def get_betting_lines(self, game_id: int) -> List[Dict]:
        """Get betting lines for the game"""
        if not game_id:
            return []
            
        url = f"{self.base_url}/lines"
        params = {"gameId": game_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            lines = response.json()
            return lines if lines else []
        except Exception as e:
            return []
    
    def get_team_records(self, year: int, week: int, home_team: str, away_team: str) -> Dict:
        """Get team records before the game"""
        url = f"{self.base_url}/records"
        params = {
            "year": year,
            "team": home_team
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            home_record = response.json()
            
            params['team'] = away_team
            response = requests.get(url, headers=self.headers, params=params)
            away_record = response.json()
            
            return {
                'home': home_record[0] if home_record else None,
                'away': away_record[0] if away_record else None
            }
        except Exception as e:
            return {'home': None, 'away': None}
    
    def analyze_rivalry(self, enriched_games: List[Dict]) -> Dict:
        """Analyze the rivalry statistics"""
        osu_wins = 0
        michigan_wins = 0
        total_points_osu = 0
        total_points_michigan = 0
        home_team_wins = 0
        ranked_matchups = 0
        top10_matchups = 0
        margins = []
        
        for game_data in enriched_games:
            game = game_data['basic_info']
            home_team = game.get('homeTeam') or game.get('home_team')
            away_team = game.get('awayTeam') or game.get('away_team')
            home_points = game.get('homeScore') or game.get('homePoints') or game.get('home_points', 0)
            away_points = game.get('awayScore') or game.get('awayPoints') or game.get('away_points', 0)
            
            # Determine winner
            if home_team == "Ohio State":
                osu_points = home_points
                mich_points = away_points
                if home_points > away_points:
                    osu_wins += 1
                    home_team_wins += 1
                else:
                    michigan_wins += 1
            else:
                osu_points = away_points
                mich_points = home_points
                if away_points > home_points:
                    osu_wins += 1
                else:
                    michigan_wins += 1
                    home_team_wins += 1
            
            total_points_osu += osu_points
            total_points_michigan += mich_points
            margins.append(abs(osu_points - mich_points))
            
            # Check rankings
            rankings = game_data.get('rankings', {})
            if rankings.get('home_rank') and rankings.get('away_rank'):
                ranked_matchups += 1
                if rankings.get('home_rank', 26) <= 10 and rankings.get('away_rank', 26) <= 10:
                    top10_matchups += 1
        
        total_games = len(enriched_games)
        
        return {
            'total_games': total_games,
            'osu_wins': osu_wins,
            'michigan_wins': michigan_wins,
            'osu_win_pct': (osu_wins / total_games * 100) if total_games > 0 else 0,
            'avg_points_osu': total_points_osu / total_games if total_games > 0 else 0,
            'avg_points_michigan': total_points_michigan / total_games if total_games > 0 else 0,
            'home_team_wins': home_team_wins,
            'home_win_pct': (home_team_wins / total_games * 100) if total_games > 0 else 0,
            'ranked_matchups': ranked_matchups,
            'top10_matchups': top10_matchups,
            'avg_margin': statistics.mean(margins) if margins else 0,
            'median_margin': statistics.median(margins) if margins else 0,
            'closest_game': min(margins) if margins else 0,
            'biggest_blowout': max(margins) if margins else 0
        }
    
    def format_game_summary(self, game_data: Dict) -> str:
        """Format a single game summary"""
        game = game_data['basic_info']
        rankings = game_data.get('rankings', {})
        sp = game_data.get('sp_ratings', {})
        weather = game_data.get('weather')
        lines = game_data.get('betting_lines')
        
        year = game.get('season')
        week = game.get('week')
        home_team = game.get('homeTeam') or game.get('home_team')
        away_team = game.get('awayTeam') or game.get('away_team')
        home_points = game.get('homeScore') or game.get('homePoints') or game.get('home_points', 0)
        away_points = game.get('awayScore') or game.get('awayPoints') or game.get('away_points', 0)
        
        # Determine if OSU won
        if home_team == "Ohio State":
            osu_won = home_points > away_points
            osu_points = home_points
            mich_points = away_points
        else:
            osu_won = away_points > home_points
            osu_points = away_points
            mich_points = home_points
        
        result_emoji = "🏆" if osu_won else "❌"
        
        # Format rankings
        home_rank_str = f"#{rankings.get('home_rank')}" if rankings.get('home_rank') else "Unranked"
        away_rank_str = f"#{rankings.get('away_rank')}" if rankings.get('away_rank') else "Unranked"
        
        # Format SP+ ratings
        home_sp = sp.get('home')
        away_sp = sp.get('away')
        home_sp_str = f"SP+: {home_sp.get('rating', 'N/A'):.1f}" if home_sp else "SP+: N/A"
        away_sp_str = f"SP+: {away_sp.get('rating', 'N/A'):.1f}" if away_sp else "SP+: N/A"
        
        # Format betting lines - combine all providers
        line_str = "N/A"
        if lines and len(lines) > 0:
            providers_info = []
            for line in lines:
                provider_obj = line.get('provider', {})
                provider = provider_obj.get('name', 'Unknown') if isinstance(provider_obj, dict) else str(provider_obj)
                spread = line.get('spread')
                ou = line.get('overUnder')
                line_info = f"{provider}"
                if spread is not None:
                    line_info += f" ({spread:+.1f})"
                if ou is not None:
                    line_info += f" O/U: {ou}"
                providers_info.append(line_info)
            line_str = " | ".join(providers_info) if providers_info else "N/A"
        
        # Format weather
        weather_str = "N/A"
        if weather:
            temp = weather.get('temperature')
            wind_speed = weather.get('windSpeed') or weather.get('wind_speed')
            conditions = weather.get('description') or weather.get('weatherConditionCode')
            
            parts = []
            if temp is not None:
                parts.append(f"{temp:.1f}°F")
            if wind_speed is not None:
                parts.append(f"Wind: {wind_speed:.1f}mph")
            if conditions and isinstance(conditions, str):
                parts.append(conditions)
                
            weather_str = ", ".join(parts) if parts else "N/A"
        
        summary = f"""
{'='*80}
{result_emoji} {year} - Week {week}
{'='*80}
📍 Location: {game.get('venue', 'N/A')}
🏠 {home_rank_str} {home_team} vs 🚌 {away_rank_str} {away_team}

📊 FINAL SCORE: {home_team} {home_points} - {away_team} {away_points}
   Margin: {abs(home_points - away_points)} points

📈 SP+ RATINGS:
   {home_team}: {home_sp_str}
   {away_team}: {away_sp_str}

🎲 BETTING:
   {line_str}

🌤️  WEATHER:
   {weather_str}

🏆 RESULT: {"Ohio State wins" if osu_won else "Michigan wins"} {osu_points}-{mich_points}
"""
        return summary
    
    def generate_report(self, enriched_games: List[Dict], output_file: str = None):
        """Generate comprehensive rivalry report"""
        # Sort games by year
        enriched_games.sort(key=lambda x: x['basic_info'].get('season'))
        
        report = []
        report.append("="*80)
        report.append("🏈 OHIO STATE vs MICHIGAN RIVALRY ANALYSIS (2000-2024)")
        report.append("="*80)
        report.append("")
        
        # Overall statistics
        stats = self.analyze_rivalry(enriched_games)
        report.append("📊 OVERALL SERIES STATISTICS")
        report.append("-"*80)
        report.append(f"Total Games: {stats['total_games']}")
        report.append(f"Ohio State Wins: {stats['osu_wins']} ({stats['osu_win_pct']:.1f}%)")
        report.append(f"Michigan Wins: {stats['michigan_wins']} ({100-stats['osu_win_pct']:.1f}%)")
        report.append(f"Home Team Wins: {stats['home_team_wins']} ({stats['home_win_pct']:.1f}%)")
        report.append(f"")
        report.append(f"Average Points:")
        report.append(f"  Ohio State: {stats['avg_points_osu']:.1f} PPG")
        report.append(f"  Michigan: {stats['avg_points_michigan']:.1f} PPG")
        report.append(f"")
        report.append(f"Game Margins:")
        report.append(f"  Average Margin: {stats['avg_margin']:.1f} points")
        report.append(f"  Median Margin: {stats['median_margin']:.1f} points")
        report.append(f"  Closest Game: {stats['closest_game']} points")
        report.append(f"  Biggest Blowout: {stats['biggest_blowout']} points")
        report.append(f"")
        report.append(f"Ranked Matchups: {stats['ranked_matchups']}")
        report.append(f"Top 10 Matchups: {stats['top10_matchups']}")
        report.append("")
        
        # Individual game summaries
        report.append("="*80)
        report.append("📅 GAME-BY-GAME BREAKDOWN")
        report.append("="*80)
        
        for game_data in enriched_games:
            report.append(self.format_game_summary(game_data))
        
        report_text = "\n".join(report)
        
        # Print to console
        print(report_text)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"\n✅ Report saved to: {output_file}")
        
        return report_text

def main():
    """Main execution function"""
    print("🏈 Starting OSU vs Michigan Rivalry Analysis...")
    print("="*80)
    
    # API key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    analyzer = RivalryAnalyzer(api_key)
    
    # Fetch all rivalry games
    print("\n📥 Fetching rivalry games from 2000-2024...")
    games = analyzer.get_rivalry_games(start_year=2000, end_year=2024)
    print(f"\n✅ Found {len(games)} games\n")
    
    # Enrich each game with additional data
    print("📊 Enriching games with SP+, rankings, weather, betting lines...")
    enriched_games = []
    for i, game in enumerate(games, 1):
        year = game.get('season')
        print(f"\n[{i}/{len(games)}] Processing {year} game...")
        enriched = analyzer.enrich_game_data(game)
        enriched_games.append(enriched)
    
    # Save raw data
    output_json = f"osu_michigan_rivalry_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_json, 'w') as f:
        json.dump(enriched_games, f, indent=2, default=str)
    print(f"\n✅ Raw data saved to: {output_json}")
    
    # Generate and save report
    print("\n" + "="*80)
    print("📝 GENERATING COMPREHENSIVE REPORT")
    print("="*80 + "\n")
    
    output_txt = f"osu_michigan_rivalry_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    analyzer.generate_report(enriched_games, output_txt)
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
