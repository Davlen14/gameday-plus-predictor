"""
Batch Rivalry Analysis for All Rivalry Week Games
Analyzes all major college football rivalries with comprehensive historical data
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from rivalry_config import RIVALRY_GAMES

class BatchRivalryAnalyzer:
    def __init__(self):
        self.api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Load team IDs from fbs.json
        with open('fbs.json', 'r') as f:
            teams_data = json.load(f)
            self.team_ids = {team['school']: team['id'] for team in teams_data}
        
        # Track rivalries to analyze (unique pairs only)
        self.rivalries_to_analyze = []
        seen = set()
        for (team1, team2), info in RIVALRY_GAMES.items():
            pair = tuple(sorted([team1, team2]))
            if pair not in seen:
                seen.add(pair)
                self.rivalries_to_analyze.append({
                    'team1': team1,
                    'team2': team2,
                    'info': info
                })
    
    def get_rivalry_games(self, team1_name: str, team2_name: str, start_year: int = 2000) -> List[Dict]:
        """Get all games between two rivals since start_year"""
        team1_id = self.team_ids.get(team1_name)
        team2_id = self.team_ids.get(team2_name)
        
        if not team1_id or not team2_id:
            print(f"❌ Could not find team IDs for {team1_name} or {team2_name}")
            return []
        
        # GraphQL query to get all games between two teams
        query = """
        query GetRivalryGames($team1Id: Int!, $team2Id: Int!, $startYear: smallint!) {
          games: game(
            where: {
              _or: [
                {homeTeamId: {_eq: $team1Id}, awayTeamId: {_eq: $team2Id}},
                {homeTeamId: {_eq: $team2Id}, awayTeamId: {_eq: $team1Id}}
              ],
              season: {_gte: $startYear},
              seasonType: {_eq: "regular"}
            }
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
            }
            lines {
              provider {
                id
                name
              }
              spread
              overUnder
            }
          }
        }
        """
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json={
                    "query": query,
                    "variables": {
                        "team1Id": team1_id,
                        "team2Id": team2_id,
                        "startYear": start_year
                    }
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    print(f"❌ GraphQL errors: {data['errors']}")
                    return []
                games = data.get('data', {}).get('games', [])
                return games
            else:
                print(f"❌ API request failed: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching games: {e}")
            return []
    
    def get_rankings_for_games(self, games: List[Dict]) -> Dict:
        """Get AP Poll rankings for all games"""
        if not games:
            return {}
        
        # Get unique year-week combinations
        year_weeks = set()
        for game in games:
            year_weeks.add((game['season'], game['week']))
        
        rankings = {}
        
        for year, week in year_weeks:
            query = """
            query GetRankings($yearInt: Int!, $week: Int!) {
              pollRank(
                where: {
                  poll: {season: {_eq: $yearInt}},
                  week: {_eq: $week},
                  poll: {name: {_eq: "AP Top 25"}}
                }
              ) {
                rank
                teamId
                poll {
                  name
                  season
                }
                week
              }
            }
            """
            
            try:
                response = requests.post(
                    self.graphql_url,
                    headers=self.headers,
                    json={
                        "query": query,
                        "variables": {
                            "yearInt": int(year),
                            "week": int(week)
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        poll_ranks = data['data'].get('pollRank', [])
                        for rank in poll_ranks:
                            key = (year, week, rank['teamId'])
                            rankings[key] = rank['rank']
            except Exception as e:
                print(f"⚠️  Error fetching rankings for {year} Week {week}: {e}")
        
        return rankings
    
    def analyze_rivalry(self, team1_name: str, team2_name: str, games: List[Dict], rankings: Dict) -> Dict:
        """Analyze rivalry statistics"""
        if not games:
            return None
        
        team1_id = self.team_ids.get(team1_name)
        team2_id = self.team_ids.get(team2_name)
        
        stats = {
            'total_games': len(games),
            'team1_wins': 0,
            'team2_wins': 0,
            'team1_points': 0,
            'team2_points': 0,
            'ranked_matchups': 0,
            'top10_matchups': 0,
            'closest_game': None,
            'biggest_blowout': None,
            'home_wins': 0,
            'away_wins': 0
        }
        
        min_margin = float('inf')
        max_margin = 0
        
        for game in games:
            home_id = game['homeTeamId']
            away_id = game['awayTeamId']
            home_score = game['homePoints'] or 0
            away_score = game['awayPoints'] or 0
            
            # Get rankings
            home_rank = rankings.get((game['season'], game['week'], home_id))
            away_rank = rankings.get((game['season'], game['week'], away_id))
            
            if home_rank or away_rank:
                stats['ranked_matchups'] += 1
                if home_rank and home_rank <= 10 and away_rank and away_rank <= 10:
                    stats['top10_matchups'] += 1
            
            # Determine winner
            if home_score > away_score:
                winner_id = home_id
                stats['home_wins'] += 1
            elif away_score > home_score:
                winner_id = away_id
                stats['away_wins'] += 1
            else:
                continue
            
            # Track team-specific wins and points
            if home_id == team1_id:
                stats['team1_points'] += home_score
                stats['team2_points'] += away_score
                if winner_id == team1_id:
                    stats['team1_wins'] += 1
                else:
                    stats['team2_wins'] += 1
            else:
                stats['team1_points'] += away_score
                stats['team2_points'] += home_score
                if winner_id == team1_id:
                    stats['team1_wins'] += 1
                else:
                    stats['team2_wins'] += 1
            
            # Track margins
            margin = abs(home_score - away_score)
            if margin < min_margin:
                min_margin = margin
                stats['closest_game'] = game
            if margin > max_margin:
                max_margin = margin
                stats['biggest_blowout'] = game
        
        return stats
    
    def format_rivalry_summary(self, team1_name: str, team2_name: str, rivalry_info: Dict, 
                               stats: Dict, games: List[Dict], rankings: Dict) -> str:
        """Format a summary for a single rivalry"""
        if not stats:
            return f"\n{'='*80}\n{rivalry_info['name']}: {team1_name} vs {team2_name}\n{'='*80}\nNo games found since 2000\n"
        
        summary = f"\n{'='*80}\n"
        summary += f"{rivalry_info['name']}: {team1_name} vs {team2_name}\n"
        if rivalry_info.get('trophy'):
            summary += f"Trophy: {rivalry_info['trophy']}\n"
        summary += f"Established: {rivalry_info.get('established', 'Unknown')}\n"
        summary += f"{'='*80}\n\n"
        
        # Overall statistics
        summary += "📊 SERIES STATISTICS (Since 2000)\n"
        summary += f"Total Games: {stats['total_games']}\n"
        summary += f"{team1_name} Wins: {stats['team1_wins']} ({stats['team1_wins']/stats['total_games']*100:.1f}%)\n"
        summary += f"{team2_name} Wins: {stats['team2_wins']} ({stats['team2_wins']/stats['total_games']*100:.1f}%)\n"
        
        if stats['total_games'] > 0:
            team1_ppg = stats['team1_points'] / stats['total_games']
            team2_ppg = stats['team2_points'] / stats['total_games']
            summary += f"{team1_name} PPG: {team1_ppg:.1f}\n"
            summary += f"{team2_name} PPG: {team2_ppg:.1f}\n"
            summary += f"Average Margin: {abs(team1_ppg - team2_ppg):.1f} points\n"
        
        summary += f"Home Wins: {stats['home_wins']} ({stats['home_wins']/stats['total_games']*100:.1f}%)\n"
        summary += f"Away Wins: {stats['away_wins']} ({stats['away_wins']/stats['total_games']*100:.1f}%)\n"
        summary += f"Ranked Matchups: {stats['ranked_matchups']}\n"
        summary += f"Top 10 Matchups: {stats['top10_matchups']}\n\n"
        
        # Notable games
        if stats['closest_game']:
            game = stats['closest_game']
            home_rank = rankings.get((game['season'], game['week'], game['homeTeamId']))
            away_rank = rankings.get((game['season'], game['week'], game['awayTeamId']))
            home_rank_str = f"#{home_rank}" if home_rank else "NR"
            away_rank_str = f"#{away_rank}" if away_rank else "NR"
            margin = abs(game['homePoints'] - game['awayPoints'])
            summary += f"🔥 Closest Game: {game['season']} - {home_rank_str} {game['homeTeam']} {game['homePoints']}, "
            summary += f"{away_rank_str} {game['awayTeam']} {game['awayPoints']} ({margin} pt margin)\n"
        
        if stats['biggest_blowout']:
            game = stats['biggest_blowout']
            home_rank = rankings.get((game['season'], game['week'], game['homeTeamId']))
            away_rank = rankings.get((game['season'], game['week'], game['awayTeamId']))
            home_rank_str = f"#{home_rank}" if home_rank else "NR"
            away_rank_str = f"#{away_rank}" if away_rank else "NR"
            margin = abs(game['homePoints'] - game['awayPoints'])
            summary += f"💥 Biggest Blowout: {game['season']} - {home_rank_str} {game['homeTeam']} {game['homePoints']}, "
            summary += f"{away_rank_str} {game['awayTeam']} {game['awayPoints']} ({margin} pt margin)\n\n"
        
        # Last 10 games
        summary += "📅 LAST 10 MEETINGS\n"
        for game in games[-10:]:
            home_rank = rankings.get((game['season'], game['week'], game['homeTeamId']))
            away_rank = rankings.get((game['season'], game['week'], game['awayTeamId']))
            home_rank_str = f"#{home_rank}" if home_rank else "NR"
            away_rank_str = f"#{away_rank}" if away_rank else "NR"
            
            summary += f"  {game['season']} Week {game['week']}: "
            summary += f"{home_rank_str} {game['homeTeam']} {game['homePoints']} - "
            summary += f"{away_rank_str} {game['awayTeam']} {game['awayPoints']}"
            
            if game.get('weather'):
                weather = game['weather']
                if weather.get('temperature'):
                    summary += f" | {weather['temperature']}°F"
            
            if game.get('lines'):
                for line in game['lines'][:1]:  # Show first sportsbook
                    if line.get('spread'):
                        summary += f" | Spread: {line['spread']}"
            
            summary += "\n"
        
        return summary
    
    def analyze_all_rivalries(self):
        """Analyze all rivalry games"""
        print("🏈 ANALYZING ALL RIVALRY WEEK GAMES")
        print(f"Found {len(self.rivalries_to_analyze)} unique rivalries\n")
        
        all_results = {}
        all_summaries = []
        
        for idx, rivalry in enumerate(self.rivalries_to_analyze, 1):
            team1 = rivalry['team1']
            team2 = rivalry['team2']
            info = rivalry['info']
            
            print(f"[{idx}/{len(self.rivalries_to_analyze)}] Analyzing {info['name']}: {team1} vs {team2}")
            
            # Get games
            games = self.get_rivalry_games(team1, team2)
            print(f"  ✓ Found {len(games)} games")
            
            if not games:
                print(f"  ⚠️  No games found for this rivalry\n")
                continue
            
            # Get rankings
            print(f"  ✓ Fetching rankings...")
            rankings = self.get_rankings_for_games(games)
            
            # Analyze
            stats = self.analyze_rivalry(team1, team2, games, rankings)
            
            # Store results
            all_results[info['name']] = {
                'team1': team1,
                'team2': team2,
                'info': info,
                'stats': stats,
                'games': games,
                'rankings': rankings
            }
            
            # Generate summary
            summary = self.format_rivalry_summary(team1, team2, info, stats, games, rankings)
            all_summaries.append(summary)
            
            print(f"  ✓ Complete ({stats['team1_wins']}-{stats['team2_wins']} series)\n")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"rivalry_analysis_all_{timestamp}.json"
        txt_file = f"rivalry_analysis_all_{timestamp}.txt"
        
        with open(json_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        with open(txt_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("COLLEGE FOOTBALL RIVALRY WEEK COMPREHENSIVE ANALYSIS\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}\n")
            f.write(f"Total Rivalries Analyzed: {len(all_results)}\n")
            f.write("="*80 + "\n")
            for summary in all_summaries:
                f.write(summary)
        
        print(f"\n✅ Analysis complete!")
        print(f"📊 Results saved to: {json_file}")
        print(f"📄 Report saved to: {txt_file}")
        
        return all_results

if __name__ == "__main__":
    analyzer = BatchRivalryAnalyzer()
    analyzer.analyze_all_rivalries()
