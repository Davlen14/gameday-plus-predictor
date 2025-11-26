#!/usr/bin/env python3
"""
OSU vs Michigan Rivalry Analysis (2000-2024)
Pure GraphQL implementation - no REST API
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import statistics

class RivalryAnalyzerGraphQL:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Load team IDs
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
    
    def get_all_rivalry_games(self, team1: str = "Ohio State", team2: str = "Michigan",
                               start_year: int = 2000, end_year: int = 2024) -> List[Dict]:
        """Fetch ALL rivalry games using pure GraphQL"""
        team1_id = self.team_ids.get(team1)
        team2_id = self.team_ids.get(team2)
        
        if not team1_id or not team2_id:
            print(f"❌ Could not find team IDs: {team1}={team1_id}, {team2}={team2_id}")
            return []
        
        print(f"📥 Fetching rivalry games: {team1} (ID: {team1_id}) vs {team2} (ID: {team2_id})")
        print(f"   Years: {start_year}-{end_year}")
        
        query = """
        query RivalryGames($team1Id: Int!, $team2Id: Int!, $startYear: smallint!, $endYear: smallint!) {
            games: game(
                where: {
                    _or: [
                        {homeTeamId: {_eq: $team1Id}, awayTeamId: {_eq: $team2Id}},
                        {homeTeamId: {_eq: $team2Id}, awayTeamId: {_eq: $team1Id}}
                    ],
                    season: {_gte: $startYear, _lte: $endYear},
                    seasonType: {_eq: "regular"}
                },
                orderBy: {season: ASC, week: ASC}
            ) {
                id
                season
                week
                startDate
                homeTeam
                awayTeam
                homeTeamId
                awayTeamId
                homePoints
                awayPoints
                venueId
                neutralSite
                weather {
                    temperature
                    windSpeed
                    windDirection
                    precipitation
                    humidity
                    pressure
                    weatherConditionCode
                }
                lines {
                    spread
                    spreadOpen
                    overUnder
                    overUnderOpen
                    moneylineHome
                    moneylineAway
                    provider {
                        id
                        name
                    }
                }
            }
        }
        """
        
        variables = {
            "team1Id": team1_id,
            "team2Id": team2_id,
            "startYear": start_year,
            "endYear": end_year
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                print(f"❌ GraphQL errors: {data['errors']}")
                return []
            
            games = data.get('data', {}).get('games', [])
            print(f"✅ Found {len(games)} rivalry games")
            
            for game in games:
                year = game.get('season')
                week = game.get('week')
                home = game.get('homeTeam')
                away = game.get('awayTeam')
                print(f"  ✓ {year} Week {week}: {home} vs {away}")
            
            return games
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def get_rankings_for_games(self, games: List[Dict]) -> Dict[tuple, Dict]:
        """Fetch rankings for all games in batch"""
        rankings_map = {}
        
        print("\n📊 Fetching rankings data...")
        
        # Group games by year/week for efficient querying
        game_periods = set()
        for game in games:
            year = game.get('season')
            week = game.get('week')
            if year and week:
                game_periods.add((year, week))
        
        for year, week in sorted(game_periods):
            query = """
            query GetRankings($year: Int!, $week: smallint!, $teamIds: [Int!]) {
                pollRank(
                    where: {
                        poll: {season: {_eq: $year}, week: {_eq: $week}},
                        team: {teamId: {_in: $teamIds}}
                    }
                ) {
                    rank
                    team {
                        teamId
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
            
            # Get team IDs for this game
            game_for_period = next(g for g in games if g['season'] == year and g['week'] == week)
            team_ids = [game_for_period['homeTeamId'], game_for_period['awayTeamId']]
            
            variables = {
                "year": year,
                "week": week,
                "teamIds": team_ids
            }
            
            try:
                response = requests.post(
                    self.graphql_url,
                    headers=self.headers,
                    json={"query": query, "variables": variables}
                )
                data = response.json()
                
                if 'errors' not in data:
                    ranks = data.get('data', {}).get('pollRank', [])
                    
                    # Extract AP Poll rankings
                    home_rank = None
                    away_rank = None
                    
                    for rank_data in ranks:
                        if rank_data['poll']['pollType']['name'] == 'AP Top 25':
                            team_id = rank_data['team']['teamId']
                            rank = rank_data['rank']
                            
                            if team_id == game_for_period['homeTeamId']:
                                home_rank = rank
                            elif team_id == game_for_period['awayTeamId']:
                                away_rank = rank
                    
                    rankings_map[(year, week)] = {
                        'home_rank': home_rank,
                        'away_rank': away_rank
                    }
                    
                    if home_rank or away_rank:
                        print(f"  ✓ {year} Week {week}: Home=#{home_rank or 'NR'}, Away=#{away_rank or 'NR'}")
                
            except Exception as e:
                print(f"  ⚠ {year} Week {week}: {str(e)}")
        
        return rankings_map
    
    def get_sp_ratings(self, games: List[Dict]) -> Dict[tuple, Dict]:
        """Fetch SP+ ratings for all games"""
        sp_map = {}
        
        print("\n📈 Fetching SP+ ratings...")
        
        years = set(g['season'] for g in games)
        
        for year in sorted(years):
            query = """
            query GetSPRatings($year: smallint!, $teamIds: [Int!]) {
                spRating(
                    where: {
                        year: {_eq: $year},
                        teamId: {_in: $teamIds}
                    }
                ) {
                    teamId
                    year
                    rating
                    ranking
                    team {
                        school
                    }
                }
            }
            """
            
            # Get unique team IDs for this year
            team_ids = list(set([
                g['homeTeamId'] for g in games if g['season'] == year
            ] + [
                g['awayTeamId'] for g in games if g['season'] == year
            ]))
            
            variables = {
                "year": year,
                "teamIds": team_ids
            }
            
            try:
                response = requests.post(
                    self.graphql_url,
                    headers=self.headers,
                    json={"query": query, "variables": variables}
                )
                data = response.json()
                
                if 'errors' not in data:
                    ratings = data.get('data', {}).get('spRating', [])
                    
                    for rating in ratings:
                        team_id = rating['teamId']
                        sp_map[(year, team_id)] = {
                            'rating': rating.get('rating'),
                            'ranking': rating.get('ranking'),
                            'school': rating['team']['school']
                        }
                    
                    print(f"  ✓ {year}: Found {len(ratings)} SP+ ratings")
                
            except Exception as e:
                print(f"  ⚠ {year}: {str(e)}")
        
        return sp_map
    
    def analyze_rivalry(self, games: List[Dict], rankings: Dict, sp_ratings: Dict) -> Dict:
        """Analyze the rivalry statistics"""
        osu_wins = 0
        michigan_wins = 0
        total_points_osu = 0
        total_points_michigan = 0
        home_team_wins = 0
        ranked_matchups = 0
        top10_matchups = 0
        margins = []
        
        for game in games:
            home_team = game['homeTeam']
            away_team = game['awayTeam']
            home_points = game['homePoints'] or 0
            away_points = game['awayPoints'] or 0
            
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
            year_week = (game['season'], game['week'])
            if year_week in rankings:
                ranks = rankings[year_week]
                if ranks['home_rank'] and ranks['away_rank']:
                    ranked_matchups += 1
                    if ranks['home_rank'] <= 10 and ranks['away_rank'] <= 10:
                        top10_matchups += 1
        
        total_games = len(games)
        
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
    
    def format_game_summary(self, game: Dict, rankings: Dict, sp_ratings: Dict) -> str:
        """Format a single game summary"""
        year = game['season']
        week = game['week']
        home_team = game['homeTeam']
        away_team = game['awayTeam']
        home_points = game['homePoints'] or 0
        away_points = game['awayPoints'] or 0
        
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
        
        # Get rankings
        year_week = (year, week)
        ranks = rankings.get(year_week, {})
        home_rank_str = f"#{ranks.get('home_rank')}" if ranks.get('home_rank') else "Unranked"
        away_rank_str = f"#{ranks.get('away_rank')}" if ranks.get('away_rank') else "Unranked"
        
        # Get SP+ ratings
        home_sp = sp_ratings.get((year, game['homeTeamId']))
        away_sp = sp_ratings.get((year, game['awayTeamId']))
        home_sp_str = f"SP+: {home_sp['rating']:.1f}" if home_sp and home_sp.get('rating') else "SP+: N/A"
        away_sp_str = f"SP+: {away_sp['rating']:.1f}" if away_sp and away_sp.get('rating') else "SP+: N/A"
        
        # Format betting lines
        lines = game.get('lines', [])
        line_str = "N/A"
        if lines:
            providers_info = []
            for line in lines:
                provider = line['provider']['name']
                spread = line.get('spread')
                ou = line.get('overUnder')
                line_info = f"{provider}"
                if spread is not None:
                    line_info += f" ({spread:+.1f})"
                if ou is not None:
                    line_info += f" O/U: {ou}"
                providers_info.append(line_info)
            line_str = " | ".join(providers_info)
        
        # Format weather
        weather = game.get('weather')
        weather_str = "N/A"
        if weather:
            temp = weather.get('temperature')
            wind = weather.get('windSpeed')
            precip = weather.get('precipitation')
            
            parts = []
            if temp is not None:
                parts.append(f"{temp:.1f}°F")
            if wind is not None:
                parts.append(f"Wind: {wind:.1f}mph")
            if precip is not None and precip > 0:
                parts.append(f"Precip: {precip:.2f}\"")
            
            weather_str = ", ".join(parts) if parts else "N/A"
        
        summary = f"""
{'='*80}
{result_emoji} {year} - Week {week}
{'='*80}
📍 Location: {"Neutral Site" if game.get('neutralSite') else (home_team + " (Home)")}
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
    
    def generate_report(self, games: List[Dict], rankings: Dict, sp_ratings: Dict, output_file: str = None):
        """Generate comprehensive rivalry report"""
        report = []
        report.append("="*80)
        report.append("🏈 OHIO STATE vs MICHIGAN RIVALRY ANALYSIS (2000-2024)")
        report.append("   Pure GraphQL Implementation")
        report.append("="*80)
        report.append("")
        
        # Overall statistics
        stats = self.analyze_rivalry(games, rankings, sp_ratings)
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
        
        for game in games:
            report.append(self.format_game_summary(game, rankings, sp_ratings))
        
        report_text = "\n".join(report)
        
        # Print to console
        print(report_text)
        
        # Save to file
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"\n✅ Report saved to: {output_file}")
        
        return report_text


def main():
    """Main execution function"""
    print("🏈 Starting OSU vs Michigan Rivalry Analysis (Pure GraphQL)...")
    print("="*80)
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    analyzer = RivalryAnalyzerGraphQL(api_key)
    
    # Fetch all games in one query
    games = analyzer.get_all_rivalry_games(start_year=2000, end_year=2024)
    
    if not games:
        print("❌ No games found!")
        return
    
    # Fetch rankings for all games
    rankings = analyzer.get_rankings_for_games(games)
    
    # Fetch SP+ ratings
    sp_ratings = analyzer.get_sp_ratings(games)
    
    # Save raw data
    output_json = f"osu_michigan_rivalry_graphql_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_json, 'w') as f:
        json.dump({
            'games': games,
            'rankings': {f"{k[0]}_week{k[1]}": v for k, v in rankings.items()},
            'sp_ratings': {f"{k[0]}_team{k[1]}": v for k, v in sp_ratings.items()}
        }, f, indent=2, default=str)
    print(f"\n✅ Raw data saved to: {output_json}")
    
    # Generate report
    print("\n" + "="*80)
    print("📝 GENERATING COMPREHENSIVE REPORT")
    print("="*80 + "\n")
    
    output_txt = f"osu_michigan_rivalry_graphql_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    analyzer.generate_report(games, rankings, sp_ratings, output_txt)
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
