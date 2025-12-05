"""
ESPN Player Headshot Service
Fetches player IDs and headshot URLs from ESPN API
"""

import requests
import json
from typing import Dict, Optional, List
from fuzzywuzzy import fuzz

class ESPNPlayerService:
    """Service to fetch player headshots from ESPN API"""
    
    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football"
    HEADSHOT_URL = "https://a.espncdn.com/i/headshots/college-football/players/full/{player_id}.png"
    HEADSHOT_FALLBACK = "https://a.espncdn.com/i/teamlogos/default-team-logo-500.png"
    
    def __init__(self):
        """Initialize with team ID mapping from fbs.json"""
        self.team_to_espn_id = {}
        self.player_cache = {}
        self._load_team_mapping()
    
    def _load_team_mapping(self):
        """Load ESPN team ID mapping"""
        # Common ESPN team IDs for major teams
        self.team_to_espn_id = {
            "Ohio State": 194,
            "Michigan": 130,
            "Alabama": 333,
            "Georgia": 61,
            "Texas": 251,
            "Oregon": 2483,
            "Penn State": 213,
            "Notre Dame": 87,
            "USC": 30,
            "LSU": 99,
            "Florida State": 52,
            "Clemson": 228,
            "Miami": 2390,
            "Oklahoma": 201,
            "Florida": 57,
            "Auburn": 2,
            "Tennessee": 2633,
            "Texas A&M": 245,
            "Washington": 264,
            "Wisconsin": 275,
            "Iowa": 2294,
            "Nebraska": 158,
            "Louisville": 97,
            "North Carolina": 153,
            "NC State": 152,
            "Virginia Tech": 259,
            "Pittsburgh": 221,
            "West Virginia": 277,
            "Ole Miss": 145,
            "Mississippi State": 344,
            "Arkansas": 8,
            "Kentucky": 96,
            "South Carolina": 2579,
            "Missouri": 142,
            "Vanderbilt": 238,
            "Indiana": 84,
            "Maryland": 120,
            "Rutgers": 164,
            "Northwestern": 77,
            "Purdue": 2509,
            "Minnesota": 135,
            "Illinois": 356,
            "Michigan State": 127,
            "UCLA": 26,
            "Stanford": 24,
            "California": 25,
            "Arizona": 12,
            "Arizona State": 9,
            "Colorado": 38,
            "Utah": 254,
            "Oklahoma State": 197,
            "Kansas": 2305,
            "Kansas State": 2306,
            "Baylor": 239,
            "TCU": 2628,
            "Iowa State": 66,
            "Texas Tech": 2641,
            "BYU": 252,
            "Cincinnati": 2132,
            "UCF": 2116,
            "Houston": 248,
            "SMU": 2567,
            "Memphis": 235,
            "Tulane": 2655,
            "Navy": 2426,
            "Army": 349,
            "Air Force": 2005,
            "Boise State": 68,
            "San Diego State": 21,
            "Fresno State": 278,
            "UNLV": 2439,
            "Wyoming": 2751,
            "Colorado State": 36,
            "New Mexico": 167,
            "Utah State": 328,
            "San Jose State": 23,
            "Nevada": 2440
        }
    
    def get_espn_team_id(self, team_name: str) -> Optional[int]:
        """
        Get ESPN team ID for a given team name
        Uses fuzzy matching to handle variations
        """
        # Direct match
        if team_name in self.team_to_espn_id:
            return self.team_to_espn_id[team_name]
        
        # Fuzzy match
        best_match = None
        best_score = 0
        for espn_team, espn_id in self.team_to_espn_id.items():
            score = fuzz.ratio(team_name.lower(), espn_team.lower())
            if score > best_score and score > 80:
                best_score = score
                best_match = espn_id
        
        return best_match
    
    def fetch_team_roster(self, team_name: str) -> Dict:
        """
        Fetch full roster for a team from ESPN
        Returns: {player_name: {id, position, headshot_url}}
        """
        espn_id = self.get_espn_team_id(team_name)
        if not espn_id:
            print(f"⚠️  No ESPN ID found for {team_name}")
            return {}
        
        # Check cache
        cache_key = f"roster_{espn_id}"
        if cache_key in self.player_cache:
            return self.player_cache[cache_key]
        
        try:
            url = f"{self.BASE_URL}/teams/{espn_id}/roster"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            roster = {}
            
            # Parse athletes from different position groups
            for position_group in data.get('athletes', []):
                for player in position_group.get('items', []):
                    player_name = player.get('displayName') or player.get('fullName')
                    player_id = player.get('id')
                    
                    if player_name and player_id:
                        roster[player_name] = {
                            'id': player_id,
                            'position': position_group.get('position', 'Unknown'),
                            'headshot_url': self.HEADSHOT_URL.format(player_id=player_id),
                            'first_name': player.get('firstName', ''),
                            'last_name': player.get('lastName', ''),
                            'short_name': player.get('shortName', player_name)
                        }
            
            # Cache the result
            self.player_cache[cache_key] = roster
            print(f"✅ Fetched {len(roster)} players for {team_name} (ESPN ID: {espn_id})")
            return roster
            
        except Exception as e:
            print(f"❌ Error fetching roster for {team_name}: {e}")
            return {}
    
    def get_player_headshot(self, player_name: str, team_name: str) -> str:
        """
        Get headshot URL for a specific player
        Returns headshot URL or fallback image
        """
        roster = self.fetch_team_roster(team_name)
        
        # Direct name match
        if player_name in roster:
            return roster[player_name]['headshot_url']
        
        # Fuzzy name match
        best_match = None
        best_score = 0
        for roster_name, player_data in roster.items():
            score = fuzz.ratio(player_name.lower(), roster_name.lower())
            if score > best_score and score > 85:
                best_score = score
                best_match = player_data['headshot_url']
        
        return best_match if best_match else self.HEADSHOT_FALLBACK
    
    def enrich_player_data(self, players_data: Dict, team_name: str) -> Dict:
        """
        Enrich player data with ESPN headshots
        Input: {position: [player_data_dicts]}
        Output: Same structure with headshot_url added to each player
        """
        roster = self.fetch_team_roster(team_name)
        
        for position, players in players_data.items():
            if isinstance(players, list):
                for player in players:
                    if isinstance(player, dict) and 'name' in player:
                        player_name = player['name']
                        
                        # Find matching player in roster
                        if player_name in roster:
                            player['headshot_url'] = roster[player_name]['headshot_url']
                            player['espn_player_id'] = roster[player_name]['id']
                        else:
                            # Fuzzy match
                            best_match = None
                            best_score = 0
                            for roster_name, player_data in roster.items():
                                score = fuzz.ratio(player_name.lower(), roster_name.lower())
                                if score > best_score and score > 85:
                                    best_score = score
                                    best_match = player_data
                            
                            if best_match:
                                player['headshot_url'] = best_match['headshot_url']
                                player['espn_player_id'] = best_match['id']
                            else:
                                player['headshot_url'] = self.HEADSHOT_FALLBACK
                                player['espn_player_id'] = None
            
            elif isinstance(players, dict) and 'name' in players:
                # Single player (like QB)
                player_name = players['name']
                if player_name in roster:
                    players['headshot_url'] = roster[player_name]['headshot_url']
                    players['espn_player_id'] = roster[player_name]['id']
                else:
                    players['headshot_url'] = self.HEADSHOT_FALLBACK
                    players['espn_player_id'] = None
        
        return players_data


# Test function
if __name__ == "__main__":
    service = ESPNPlayerService()
    
    # Test with Ohio State
    print("\n🏈 Testing ESPN Player Service")
    print("=" * 60)
    
    roster = service.fetch_team_roster("Ohio State")
    print(f"\nFound {len(roster)} players")
    
    # Show first 5 players
    print("\n📋 Sample Players:")
    for i, (name, data) in enumerate(list(roster.items())[:5]):
        print(f"{i+1}. {name} ({data['position']})")
        print(f"   Headshot: {data['headshot_url']}")
    
    # Test player lookup
    test_player = "Will Howard"  # Ohio State QB
    headshot = service.get_player_headshot(test_player, "Ohio State")
    print(f"\n🎯 Looking up: {test_player}")
    print(f"   Headshot URL: {headshot}")
