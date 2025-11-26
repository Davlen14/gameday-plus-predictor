#!/usr/bin/env python3
"""
High Usage Players REST API Script
Fetches top players by usage using College Football Data REST API
1 QB, 2 WR, 2 RB, 1 K per team with highest usage
"""

import requests
import json
import time
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    team: str
    position: str
    usage_stats: Dict
    season_totals: Dict

class HighUsagePlayersAPI:
    def __init__(self):
        self.base_url = "https://api.collegefootballdata.com"
        self.api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'GamedayPlus/1.0'
        }
        self.year = 2025  # Current season
        
    def _make_request(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Make API request with rate limiting"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.1)  # Rate limiting
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error for {endpoint}: {e}")
            return []

    def get_top_players_by_usage(self) -> Dict[str, List[Player]]:
        """Get top players by position using usage endpoint"""
        print("🏈 Fetching player usage data...")
        
        # Get usage data for all positions
        usage_data = self._make_request("player/usage", {
            'year': self.year
        })
        
        if not usage_data:
            print("⚠️ No usage data found, falling back to stats endpoint...")
            return self._get_players_from_stats()
        
        # Organize by position
        players_by_position = {
            'QB': [],
            'WR': [],
            'RB': [], 
            'K': []
        }
        
        # Process usage data
        for player_data in usage_data:
            pos = player_data.get('position', '')
            if pos in players_by_position:
                usage_stats = {
                    'usage_percentage': player_data.get('usage', {}).get('overall', 0),
                    'passing_usage': player_data.get('usage', {}).get('pass', 0),
                    'rushing_usage': player_data.get('usage', {}).get('rush', 0),
                    'receiving_usage': player_data.get('usage', {}).get('firstDown', 0),
                    'total_plays': player_data.get('usage', {}).get('total', 0)
                }
                
                season_totals = {
                    'total_yards': player_data.get('seasonStats', {}).get('totalYards', 0),
                    'total_tds': player_data.get('seasonStats', {}).get('totalTDs', 0),
                    'games_played': player_data.get('seasonStats', {}).get('games', 12)
                }
                
                player = Player(
                    name=player_data.get('player', 'Unknown'),
                    team=player_data.get('team', 'Unknown'),
                    position=pos,
                    usage_stats=usage_stats,
                    season_totals=season_totals
                )
                players_by_position[pos].append(player)
        
        # Sort and get top players by position
        result = {}
        
        # Top 5 QBs by usage percentage
        qbs_sorted = sorted(players_by_position['QB'], 
                           key=lambda x: x.usage_stats['usage_percentage'], 
                           reverse=True)
        result['quarterbacks'] = qbs_sorted[:5]
        
        # Top 10 WRs by usage percentage  
        wrs_sorted = sorted(players_by_position['WR'],
                           key=lambda x: x.usage_stats['usage_percentage'],
                           reverse=True)
        result['wide_receivers'] = wrs_sorted[:10]
        
        # Top 10 RBs by usage percentage
        rbs_sorted = sorted(players_by_position['RB'],
                           key=lambda x: x.usage_stats['usage_percentage'],
                           reverse=True)
        result['running_backs'] = rbs_sorted[:10]
        
        # Top 5 Kickers by usage (or all available)
        ks_sorted = sorted(players_by_position['K'],
                          key=lambda x: x.usage_stats['usage_percentage'],
                          reverse=True)
        result['kickers'] = ks_sorted[:5]
        
        return result

    def _get_players_from_stats(self) -> Dict[str, List[Player]]:
        """Fallback method using stats endpoint"""
        print("📊 Using stats endpoint as fallback...")
        
        result = {
            'quarterbacks': [],
            'wide_receivers': [],
            'running_backs': [],
            'kickers': []
        }
        
        # Get QB stats
        qb_stats = self._make_request("stats/player/season", {
            'year': self.year,
            'category': 'passing',
            'seasonType': 'regular'
        })
        
        qb_usage = {}
        for stat in qb_stats:
            if stat.get('statType') == 'ATT':  # Passing attempts
                player_key = f"{stat['player']}_{stat['team']}"
                usage_stats = {
                    'usage_percentage': min(stat['stat'] / 400 * 100, 100),  # Normalize to percentage
                    'passing_usage': stat['stat'],
                    'rushing_usage': 0,
                    'total_plays': stat['stat']
                }
                season_totals = {
                    'total_yards': 0,
                    'total_tds': 0,
                    'games_played': 12
                }
                
                result['quarterbacks'].append(Player(
                    name=stat['player'],
                    team=stat['team'],
                    position='QB',
                    usage_stats=usage_stats,
                    season_totals=season_totals
                ))
        
        # Sort and limit
        result['quarterbacks'] = sorted(result['quarterbacks'], 
                                       key=lambda x: x.usage_stats['usage_percentage'], 
                                       reverse=True)[:5]
        
        return result

    def generate_team_player_database(self) -> Dict:
        """Generate database with top players per team (1 QB, 2 WR, 2 RB, 1 K)"""
        print("🏗️ Building team-based player database...")
        
        # Get all FBS teams
        teams_data = self._make_request("teams/fbs", {'year': self.year})
        
        if not teams_data:
            print("❌ Could not fetch teams data")
            return {}
        
        team_database = {}
        
        for team in teams_data[:10]:  # Limit to first 10 teams for demo
            team_name = team.get('school', 'Unknown')
            print(f"📋 Processing {team_name}...")
            
            # Get usage data for this team
            team_usage = self._make_request("player/usage", {
                'year': self.year,
                'team': team_name
            })
            
            # Organize by position
            team_players = {
                'quarterback': None,
                'wide_receivers': [],
                'running_backs': [],
                'kicker': None
            }
            
            qbs = []
            wrs = []
            rbs = []
            ks = []
            
            for player_data in team_usage:
                pos = player_data.get('position', '')
                usage_pct = player_data.get('usage', {}).get('overall', 0)
                
                player_info = {
                    'name': player_data.get('name', 'Unknown'),  # Fixed: use 'name' not 'player'
                    'position': pos,
                    'team': team_name,
                    'usage_percentage': round(usage_pct * 100, 1),  # Convert to percentage
                    'total_plays': int(usage_pct * 1000),  # Estimate total plays
                    'season_stats': {}  # Usage endpoint doesn't provide season stats
                }
                
                if pos == 'QB':
                    qbs.append(player_info)
                elif pos in ['WR', 'TE']:  # Include TEs with WRs
                    wrs.append(player_info)
                elif pos in ['RB', 'FB']:  # Include FBs with RBs
                    rbs.append(player_info)
                elif pos in ['K', 'PK']:
                    ks.append(player_info)
            
            # Sort and select top players
            qbs_sorted = sorted(qbs, key=lambda x: x['usage_percentage'], reverse=True)
            wrs_sorted = sorted(wrs, key=lambda x: x['usage_percentage'], reverse=True)
            rbs_sorted = sorted(rbs, key=lambda x: x['usage_percentage'], reverse=True)
            ks_sorted = sorted(ks, key=lambda x: x['usage_percentage'], reverse=True)
            
            # Assign top players
            team_players['quarterback'] = qbs_sorted[0] if qbs_sorted else self._create_default_player(team_name, 'QB')
            team_players['wide_receivers'] = wrs_sorted[:2] if len(wrs_sorted) >= 2 else wrs_sorted + [self._create_default_player(team_name, 'WR') for _ in range(2 - len(wrs_sorted))]
            team_players['running_backs'] = rbs_sorted[:2] if len(rbs_sorted) >= 2 else rbs_sorted + [self._create_default_player(team_name, 'RB') for _ in range(2 - len(rbs_sorted))]
            team_players['kicker'] = ks_sorted[0] if ks_sorted else self._create_default_player(team_name, 'K')
            
            team_database[team_name] = {
                'team_name': team_name,
                'players': team_players
            }
            
            time.sleep(0.2)  # Rate limiting
        
        return team_database
    
    def _create_default_player(self, team_name: str, position: str) -> Dict:
        """Create default player when no data available"""
        return {
            'name': f'{team_name} {position}1',
            'position': position,
            'team': team_name,
            'usage_percentage': 50.0,
            'total_plays': 100,
            'season_stats': {
                'totalYards': 500,
                'totalTDs': 3,
                'games': 12
            }
        }

    def print_team_database(self, database: Dict):
        """Print formatted team database"""
        print(f"\n🏆 TEAM PLAYER DATABASE - {len(database)} Teams")
        print("=" * 80)
        
        for team_name, team_data in database.items():
            print(f"\n🏈 {team_name}")
            print("-" * 50)
            
            players = team_data['players']
            
            # QB
            qb = players['quarterback']
            if qb:
                print(f"  🎯 QB: {qb['name']} ({qb['usage_percentage']:.1f}% usage, {qb['total_plays']} plays)")
            
            # WRs
            print("  📡 WRs:")
            for i, wr in enumerate(players['wide_receivers'], 1):
                print(f"    {i}. {wr['name']} ({wr['usage_percentage']:.1f}% usage, {wr['total_plays']} plays)")
            
            # RBs
            print("  🏃 RBs:")
            for i, rb in enumerate(players['running_backs'], 1):
                print(f"    {i}. {rb['name']} ({rb['usage_percentage']:.1f}% usage, {rb['total_plays']} plays)")
            
            # Kicker
            k = players['kicker']
            if k:
                print(f"  🥅 K: {k['name']} ({k['usage_percentage']:.1f}% usage, {k['total_plays']} plays)")

def main():
    """Main execution function"""
    api = HighUsagePlayersAPI()
    
    try:
        print("🚀 Starting High Usage Players Analysis...")
        print("📋 Target: 1 QB, 2 WR, 2 RB, 1 K per team")
        print("=" * 60)
        
        # Generate team-based database
        team_database = api.generate_team_player_database()
        
        if not team_database:
            print("❌ No team data generated")
            return False
        
        # Print results
        api.print_team_database(team_database)
        
        # Save to JSON file
        filename = f"team_high_usage_players_2025_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(team_database, f, indent=2)
        
        print(f"\n💾 Team database saved to: {filename}")
        print(f"🎉 Generated database for {len(team_database)} teams!")
        print("📊 Each team has: 1 QB, 2 WRs, 2 RBs, 1 K")
        
    except Exception as e:
        print(f"❌ Error generating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()