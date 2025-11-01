"""
Game Media Service - Loads Week 9 game media data for accurate game information
"""
import json
from pathlib import Path
from typing import Dict, Optional

class GameMediaService:
    """Service to load and query game media information from week9_game_media.json"""
    
    def __init__(self, media_file_path: str = "week9_game_media.json"):
        self.media_file = Path(media_file_path)
        self.games_data = self._load_media_data()
    
    def _load_media_data(self) -> Dict:
        """Load game media data from JSON file"""
        try:
            if not self.media_file.exists():
                print(f"⚠️ Warning: Game media file not found at {self.media_file}")
                return {"games": []}
            
            with open(self.media_file, 'r') as f:
                data = json.load(f)
                print(f"✅ Loaded {len(data.get('games', []))} games from media file")
                return data
        except Exception as e:
            print(f"❌ Error loading game media data: {e}")
            return {"games": []}
    
    def _normalize_team_name(self, team_name: str) -> str:
        """Normalize team name for matching"""
        # Common variations
        replacements = {
            "Miami": "Miami (FL)",
            "Miami FL": "Miami (FL)",
            "Miami (Florida)": "Miami (FL)",
            "USC": "Southern California",
            "LSU": "Louisiana State",
            "UCF": "Central Florida",
            "BYU": "Brigham Young",
            "SMU": "Southern Methodist",
            "TCU": "Texas Christian",
            "UNLV": "Nevada-Las Vegas",
        }
        
        normalized = team_name.strip()
        return replacements.get(normalized, normalized)
    
    def get_game_info(self, home_team: str, away_team: str) -> Optional[Dict]:
        """
        Find game information by team matchup
        
        Args:
            home_team: Name of home team
            away_team: Name of away team
            
        Returns:
            Dict with game_id, scheduling, media, weather info or None if not found
        """
        home_normalized = self._normalize_team_name(home_team)
        away_normalized = self._normalize_team_name(away_team)
        
        for game in self.games_data.get('games', []):
            matchup = game.get('matchup', {})
            game_home = matchup.get('home', {}).get('team', '')
            game_away = matchup.get('away', {}).get('team', '')
            
            # Check if teams match (case-insensitive)
            if (game_home.lower() == home_normalized.lower() and 
                game_away.lower() == away_normalized.lower()):
                return {
                    'game_id': game.get('game_id'),
                    'date': game.get('scheduling', {}).get('date', 'TBD'),
                    'time': game.get('scheduling', {}).get('time', 'TBD'),
                    'network': game.get('media', {}).get('tv_network', 'TBD'),
                    'radio': game.get('media', {}).get('radio', []),
                    'streaming': game.get('media', {}).get('streaming', []),
                    'weather': game.get('weather'),
                    'venue': matchup.get('home', {}).get('team', '')  # Home team typically indicates venue
                }
        
        # Try reverse match (sometimes home/away can be swapped)
        for game in self.games_data.get('games', []):
            matchup = game.get('matchup', {})
            game_home = matchup.get('home', {}).get('team', '')
            game_away = matchup.get('away', {}).get('team', '')
            
            if (game_away.lower() == home_normalized.lower() and 
                game_home.lower() == away_normalized.lower()):
                print(f"⚠️ Found reverse match for {home_team} vs {away_team}")
                return {
                    'game_id': game.get('game_id'),
                    'date': game.get('scheduling', {}).get('date', 'TBD'),
                    'time': game.get('scheduling', {}).get('time', 'TBD'),
                    'network': game.get('media', {}).get('tv_network', 'TBD'),
                    'radio': game.get('media', {}).get('radio', []),
                    'streaming': game.get('media', {}).get('streaming', []),
                    'weather': game.get('weather'),
                    'venue': matchup.get('away', {}).get('team', '')
                }
        
        print(f"⚠️ No game media found for {home_team} vs {away_team}")
        return None
    
    def get_all_games(self) -> list:
        """Get all available games"""
        return self.games_data.get('games', [])
    
    def get_games_by_network(self, network: str) -> list:
        """Get all games on a specific network"""
        network_lower = network.lower()
        return [
            game for game in self.games_data.get('games', [])
            if game.get('media', {}).get('tv_network', '').lower() == network_lower
        ]


# Singleton instance
_game_media_service = None

def get_game_media_service() -> GameMediaService:
    """Get or create game media service instance"""
    global _game_media_service
    if _game_media_service is None:
        _game_media_service = GameMediaService()
    return _game_media_service
