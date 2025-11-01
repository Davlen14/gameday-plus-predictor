import json
import os
from typing import Dict, List, Any
import statistics
import math

# Import the dataclasses from the main module - we'll need to move these too
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class DataProcessor:
    """Handles processing and transformation of static data"""
    
    def __init__(self):
        pass
    
    def _process_team_stats(self, fbs_stats: List[Dict]) -> Dict[str, Any]:
        """Process FBS team stats into comprehensive team objects"""
        # For now, return the data as-is to avoid breaking changes
        # This will need the full implementation from the original file
        processed_stats = {}
        
        for team_data in fbs_stats:
            team_name = team_data['team']
            stats = team_data['stats']
            processed_stats[team_name] = stats
        
        return processed_stats
    
    def _process_drive_data(self, drive_data: Any) -> Any:
        """Process drive data"""
        return drive_data
    
    def _create_team_lookup(self, fbs_stats: List[Dict]) -> Dict[str, int]:
        """Create team name to ID lookup"""
        lookup = {}
        for team_data in fbs_stats:
            if 'team' in team_data and 'id' in team_data:
                lookup[team_data['team']] = team_data['id']
        return lookup
    
    def _extract_coaching_data(self, coaches_data: Any) -> Any:
        """Extract coaching data"""
        return coaches_data
    
    def _process_team_drives(self, power5_teams_drives: Any) -> Any:
        """Process team drives data"""
        return power5_teams_drives
    
    def _process_structured_offensive(self, structured_offensive_stats: Dict) -> Dict[str, Dict]:
        """Process structured offensive statistics with enhanced metadata"""
        if not structured_offensive_stats or 'offensive_stats' not in structured_offensive_stats:
            return {}
        
        processed = {}
        for team_stat in structured_offensive_stats['offensive_stats']:
            team_name = team_stat.get('team', '')
            if team_name:
                processed[team_name] = {
                    'passing_yards': team_stat.get('passing_yards', 0),
                    'rushing_yards': team_stat.get('rushing_yards', 0),
                    'total_yards': team_stat.get('total_yards', 0),
                    'points_per_game': team_stat.get('points_per_game', 0),
                    'plays_per_game': team_stat.get('plays_per_game', 0),
                    'yards_per_play': team_stat.get('yards_per_play', 0.0),
                    'third_down_conversion_pct': team_stat.get('third_down_conversion_pct', 0.0),
                    'red_zone_conversion_pct': team_stat.get('red_zone_conversion_pct', 0.0),
                    'turnovers_lost': team_stat.get('turnovers_lost', 0),
                    'fumbles_lost': team_stat.get('fumbles_lost', 0),
                    'interceptions_thrown': team_stat.get('interceptions_thrown', 0),
                    # Enhanced metadata
                    'efficiency_metrics': team_stat.get('efficiency_metrics', {}),
                    'situational_stats': team_stat.get('situational_stats', {}),
                    'advanced_metrics': team_stat.get('advanced_metrics', {})
                }
        
        return processed
    
    def _process_structured_defensive(self, structured_defensive_stats: Dict) -> Dict[str, Dict]:
        """Process structured defensive statistics with enhanced metadata"""
        if not structured_defensive_stats or 'defensive_stats' not in structured_defensive_stats:
            return {}
        
        processed = {}
        for team_stat in structured_defensive_stats['defensive_stats']:
            team_name = team_stat.get('team', '')
            if team_name:
                processed[team_name] = {
                    'points_allowed': team_stat.get('points_allowed', 0),
                    'yards_allowed': team_stat.get('yards_allowed', 0),
                    'passing_yards_allowed': team_stat.get('passing_yards_allowed', 0),
                    'rushing_yards_allowed': team_stat.get('rushing_yards_allowed', 0),
                    'yards_per_play_allowed': team_stat.get('yards_per_play_allowed', 0.0),
                    'third_down_defense_pct': team_stat.get('third_down_defense_pct', 0.0),
                    'red_zone_defense_pct': team_stat.get('red_zone_defense_pct', 0.0),
                    'turnovers_forced': team_stat.get('turnovers_forced', 0),
                    'fumbles_recovered': team_stat.get('fumbles_recovered', 0),
                    'interceptions': team_stat.get('interceptions', 0),
                    'sacks': team_stat.get('sacks', 0),
                    'tackles_for_loss': team_stat.get('tackles_for_loss', 0),
                    # Enhanced metadata
                    'efficiency_metrics': team_stat.get('efficiency_metrics', {}),
                    'situational_stats': team_stat.get('situational_stats', {}),
                    'advanced_metrics': team_stat.get('advanced_metrics', {})
                }
        
        return processed
    
    def _process_backtesting_data(self, backtesting_data: Dict) -> Dict[str, Dict]:
        """Process comprehensive backtesting ratings for enhanced model calibration"""
        if not backtesting_data or 'teams' not in backtesting_data:
            return {}
        
        processed_ratings = {}
        
        for team in backtesting_data['teams']:
            team_name = team.get('team', '')
            if not team_name:
                continue
            
            # Extract comprehensive ratings (using new field names from backtesting JSON)
            ratings = {
                'elo': team.get('elo', 1500),
                'fpi': team.get('fpi', 0.0),
                'sp_overall': team.get('sp_overall', 0.0),
                'sp_offense': team.get('sp_offense', 0.0),
                'sp_defense': team.get('sp_defense', 0.0),
                'srs': team.get('srs', 0.0),
                'sagarin': team.get('sagarin', 0.0),
                'massey': team.get('massey', 0.0),
                'colley': team.get('colley', 0.0),
                'ratings_available': True,
                
                # New field names (match backtesting JSON structure)
                'fpi_offensive_efficiency': team.get('fpi_components', {}).get('offensive_efficiency', 0.0),
                'fpi_defensive_efficiency': team.get('fpi_components', {}).get('defensive_efficiency', 0.0),
                'fpi_st_efficiency': team.get('fpi_components', {}).get('special_teams_efficiency', 0.0),
                
                # SP+ components
                'sp_offensive_rating': team.get('sp_components', {}).get('offensive_rating', 0.0),
                'sp_defensive_rating': team.get('sp_components', {}).get('defensive_rating', 0.0),
                'sp_special_teams_rating': team.get('sp_components', {}).get('special_teams_rating', 0.0),
                
                # Advanced metrics
                'power_rating': team.get('power_rating', 0.0),
                'consistency_rating': team.get('consistency_rating', 0.0),
                'recent_form_rating': team.get('recent_form_rating', 0.0),
                'sos_rating': team.get('sos_rating', 0.0)
            }
            
            processed_ratings[team_name] = ratings
        
        print(f"✅ Processed backtesting ratings for {len(processed_ratings)} teams")
        return processed_ratings