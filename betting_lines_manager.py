#!/usr/bin/env python3
"""
Betting Lines Integration Module
Loads and processes betting lines from week8.json for Flask API integration
"""

import json
import os
from typing import Dict, List, Any, Optional

class BettingLinesManager:
    """Manages betting lines data from week8.json"""
    
    def __init__(self, lines_file: str = "week8.json"):
        self.lines_file = lines_file
        self.games_data = self._load_games_data()
        
    def _load_games_data(self) -> Dict[str, Any]:
        """Load games and betting lines data from JSON file"""
        try:
            if os.path.exists(self.lines_file):
                with open(self.lines_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            else:
                print(f"⚠️  Betting lines file {self.lines_file} not found")
                return {'games': []}
        except Exception as e:
            print(f"❌ Error loading betting lines: {e}")
            return {'games': []}
    
    def find_game_by_teams(self, home_team: str, away_team: str) -> Optional[Dict[str, Any]]:
        """Find a game by team names"""
        home_team_clean = self._clean_team_name(home_team)
        away_team_clean = self._clean_team_name(away_team)
        
        for game in self.games_data.get('games', []):
            game_home = self._clean_team_name(game.get('homeTeam', ''))
            game_away = self._clean_team_name(game.get('awayTeam', ''))
            
            if game_home == home_team_clean and game_away == away_team_clean:
                return game
                
        return None
    
    def _clean_team_name(self, team_name: str) -> str:
        """Normalize team name for matching"""
        if not team_name:
            return ""
            
        # Common team name normalizations
        normalizations = {
            'miami (fl)': 'miami',
            'miami (oh)': 'miami (oh)',
            'usc': 'usc',
            'tcu': 'tcu',
            'ucf': 'ucf',
            'smu': 'smu',
            'byu': 'byu',
            'uab': 'uab',
            'utep': 'utep',
            'utsa': 'utsa',
            'unlv': 'unlv',
            'ul monroe': 'ul monroe',
            'ul lafayette': 'louisiana',
            'louisiana': 'louisiana'
        }
        
        clean_name = team_name.lower().strip()
        return normalizations.get(clean_name, clean_name)
    
    def get_betting_analysis(self, home_team: str, away_team: str, model_spread: float = None, model_total: float = None) -> Dict[str, Any]:
        """Get detailed betting analysis for a game"""
        game = self.find_game_by_teams(home_team, away_team)
        
        if not game or not game.get('betting_lines', {}).get('lines_available'):
            return self._get_empty_betting_analysis()
            
        betting_lines = game['betting_lines']
        
        # Extract market data
        market_spread = betting_lines.get('spread', 0)
        market_total = betting_lines.get('over_under', 0)
        formatted_spread = betting_lines.get('formatted_spread', 'N/A')
        
        # Calculate value edges if model data provided
        spread_edge = 0
        total_edge = 0
        is_upset_alert = False
        model_favorite = None
        market_favorite = None
        
        if model_spread is not None and market_spread:
            # Determine who each system thinks will win
            # Model spread: NEGATIVE = away team favored, POSITIVE = home team favored
            # Market spread: NEGATIVE = home team favored, POSITIVE = away team favored (from API)
            
            if model_spread < 0:
                model_favorite = away_team
                model_spread_abs = abs(model_spread)
            else:
                model_favorite = home_team
                model_spread_abs = abs(model_spread)
                
            if market_spread < 0:
                market_favorite = home_team
                market_spread_abs = abs(market_spread)
            else:
                market_favorite = away_team
                market_spread_abs = abs(market_spread)
            
            # Check if model and market disagree on favorite (UPSET ALERT!)
            if model_favorite != market_favorite:
                is_upset_alert = True
                # When favorites differ, edge is sum of spreads (you get points on team model thinks wins!)
                spread_edge = model_spread_abs + market_spread_abs
                print(f"⚠️ UPSET ALERT: Model favors {model_favorite} by {model_spread_abs:.1f}, Market favors {market_favorite} by {market_spread_abs:.1f}")
                print(f"🔍 UPSET Edge: {model_spread_abs} + {market_spread_abs} = {spread_edge:.1f} points")
            else:
                # Same favorite - calculate normal edge
                spread_edge = market_spread_abs - model_spread_abs
                print(f"🔍 Same favorite ({market_favorite}): Market {market_spread_abs} - Model {model_spread_abs} = {spread_edge:.1f}")
            
            print(f"🔍 Model spread raw: {model_spread}, Market spread raw: {market_spread}")
            
        if model_total is not None and market_total:
            total_edge = model_total - market_total
        
        # Generate sportsbook recommendations
        spread_recommendation = self._get_spread_recommendation(
            formatted_spread, spread_edge, home_team, away_team, model_spread, market_spread, 
            is_upset_alert, model_favorite, market_favorite
        )
        
        total_recommendation = self._get_total_recommendation(
            market_total, total_edge, model_total
        )
        
        return {
            'market_spread': market_spread,
            'market_total': market_total,
            'formatted_spread': formatted_spread,
            'spread_edge': spread_edge,
            'total_edge': total_edge,
            'spread_recommendation': spread_recommendation,
            'total_recommendation': total_recommendation,
            'is_upset_alert': is_upset_alert,
            'model_favorite': model_favorite,
            'market_favorite': market_favorite,
            'sportsbooks': {
                'primary_provider': betting_lines.get('provider', 'Unknown'),
                'all_providers': betting_lines.get('all_providers', []),
                'home_moneyline': betting_lines.get('home_moneyline', 'N/A'),
                'away_moneyline': betting_lines.get('away_moneyline', 'N/A'),
                'spread_open': betting_lines.get('spread_open', 'N/A'),
                'total_open': betting_lines.get('over_under_open', 'N/A')
            },
            'data_source': 'College Football Data API',
            'last_updated': betting_lines.get('last_updated', 'Unknown')
        }
    
    def _get_spread_recommendation(self, formatted_spread: str, edge: float, home_team: str, away_team: str,
                                   model_spread: float = None, market_spread: float = None,
                                   is_upset_alert: bool = False, model_favorite: str = None, 
                                   market_favorite: str = None) -> str:
        """Generate spread betting recommendation with proper logic"""
        
        if abs(edge) < 2 and not is_upset_alert:
            return "No significant edge detected"
        
        # Parse formatted spread to get market favorite and line
        parts = formatted_spread.split()
        if len(parts) >= 2:
            spread_value = float(parts[-1])
            market_fav_team = ' '.join(parts[:-1])
            market_underdog = away_team if market_fav_team == home_team else home_team
            market_line = abs(spread_value)
            
            # CASE 1: UPSET ALERT - Model and market disagree on favorite
            if is_upset_alert and model_favorite and market_favorite:
                # Bet the model's favorite getting points as underdog
                return f"UPSET ALERT: {model_favorite} +{market_line:.1f} (model predicts {model_favorite} wins, market gives them points!)"
            
            # CASE 2: Same favorite - bet based on who's getting better value
            elif model_spread is not None and market_spread is not None:
                model_spread_abs = abs(model_spread)
                market_spread_abs = abs(market_spread)
                
                if model_spread_abs > market_spread_abs:
                    # Model thinks favorite wins by MORE than market - bet the favorite
                    return f"{market_fav_team} {spread_value:.1f} (model projects {market_fav_team} wins by {model_spread_abs:.1f}, only need {market_spread_abs:.1f})"
                else:
                    # Model thinks it will be closer - bet the underdog
                    return f"{market_underdog} +{market_line:.1f} (model projects closer game, {edge:.1f}pt cushion)"
            
            # Fallback logic
            if edge >= 2:
                return f"{market_underdog} +{market_line:.1f} ({edge:.1f}pt edge)"
            else:
                return f"{market_fav_team} {spread_value:.1f} ({abs(edge):.1f}pt edge)"
        
        # Fallback if parsing fails
        if is_upset_alert:
            return f"UPSET ALERT: Model predicts upset ({edge:.1f}pt edge)"
        return f"Value detected ({edge:.1f}pt edge)"
    
    def _get_total_recommendation(self, market_total: float, edge: float, model_total: float = None) -> str:
        """Generate total betting recommendation"""
        if not market_total or abs(edge) < 3:
            return "No significant edge detected"
            
        if edge >= 3:
            return f"Value: OVER {market_total} (model projects {edge:.1f}pts higher)"
        else:
            return f"Value: UNDER {market_total} (model projects {abs(edge):.1f}pts lower)"
    
    def _get_empty_betting_analysis(self) -> Dict[str, Any]:
        """Return empty betting analysis structure"""
        return {
            'market_spread': 0,
            'market_total': 0,
            'formatted_spread': 'N/A',
            'spread_edge': 0,
            'total_edge': 0,
            'spread_recommendation': 'No market data available',
            'total_recommendation': 'No market data available',
            'sportsbooks': {
                'primary_provider': 'No data',
                'all_providers': [],
                'home_moneyline': 'N/A',
                'away_moneyline': 'N/A',
                'spread_open': 'N/A',
                'total_open': 'N/A'
            },
            'data_source': 'No data available',
            'last_updated': 'N/A'
        }

# Global instance for use in Flask app
betting_manager = BettingLinesManager()