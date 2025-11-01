import json
import os
from typing import Dict, Any, List

class PlayerAnalyzer:
    """Handles player-specific analysis and metrics"""
    
    def __init__(self, static_data: Dict = None):
        self.static_data = static_data or {}
        self.player_data = {}
    
    def _load_comprehensive_player_data(self) -> Dict[str, Any]:
        """Load comprehensive player analysis files from data/ directory"""
        # Player data file paths - all in data/ folder now
        player_files = {
            'qbs': 'data/comprehensive_qb_analysis_2025_20251015_034259.json',
            'rbs': 'data/comprehensive_rb_analysis_2025_20251015_043434.json', 
            'wrs': 'data/comprehensive_wr_analysis_2025_20251015_045922.json',
            'tes': 'data/comprehensive_te_analysis_2025_20251015_050510.json',
            'dbs': 'data/comprehensive_db_analysis_2025_20251015_051747.json',
            'lbs': 'data/comprehensive_lb_analysis_2025_20251015_053156.json',
            'dls': 'data/comprehensive_dl_analysis_2025_20251015_051056.json'
        }
        
        player_data = {}
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        
        for position, filename in player_files.items():
            try:
                file_path = os.path.join(base_dir, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    player_data[position] = data
                    print(f"✅ Loaded {position.upper()} data: {len(data.get('players', []))} players")
                else:
                    print(f"⚠️  Player file not found: {filename}")
                    player_data[position] = {'players': []}
            except Exception as e:
                print(f"❌ Error loading {position} data: {e}")
                player_data[position] = {'players': []}
        
        return player_data
    
    def _analyze_player_impact(self, home_team_name: str, away_team_name: str) -> Dict[str, Any]:
        """Analyze player impact for both teams"""
        if not self.player_data:
            self.player_data = self._load_comprehensive_player_data()
        
        home_players = self._get_team_players(home_team_name)
        away_players = self._get_team_players(away_team_name)
        
        return {
            'home_team_players': home_players,
            'away_team_players': away_players,
            'player_differential': self._calculate_player_differential(home_players, away_players)
        }
    
    def _get_team_players(self, team_name: str) -> Dict[str, List[Dict]]:
        """Get all players for a specific team"""
        team_players = {}
        
        for position, data in self.player_data.items():
            players = data.get('players', [])
            team_players[position] = []
            
            for player in players:
                if player.get('team', '').lower() == team_name.lower():
                    # Extract efficiency score safely
                    efficiency_score = 0.0
                    if 'efficiency_metrics' in player:
                        efficiency_metrics = player['efficiency_metrics']
                        if isinstance(efficiency_metrics, dict):
                            efficiency_score = efficiency_metrics.get('comprehensive_efficiency_score', 0.0)
                    
                    team_players[position].append({
                        'name': player.get('name', 'Unknown'),
                        'efficiency_score': efficiency_score,
                        'stats': player.get('stats', {}),
                        'position': position
                    })
        
        return team_players
    
    def _calculate_player_differential(self, home_players: Dict, away_players: Dict) -> Dict[str, float]:
        """Calculate player differential between teams"""
        differentials = {}
        
        for position in home_players.keys():
            home_avg = self._calculate_position_average(home_players.get(position, []))
            away_avg = self._calculate_position_average(away_players.get(position, []))
            differentials[position] = home_avg - away_avg
        
        return differentials
    
    def _calculate_position_average(self, players: List[Dict]) -> float:
        """Calculate average efficiency for a position group"""
        if not players:
            return 0.0
        
        total_efficiency = sum(player.get('efficiency_score', 0.0) for player in players)
        return total_efficiency / len(players)