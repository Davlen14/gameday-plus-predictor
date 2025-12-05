#!/usr/bin/env python3
"""
Betting Lines Integration Module
Loads and processes betting lines from week8.json for Flask API integration
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional

class BettingLinesManager:
    """Manages betting lines data from GraphQL API"""
    
    def __init__(self, lines_file: str = "week15.json", current_week_file: str = "Currentweekgames.json"):
        self.lines_file = lines_file
        self.current_week_file = current_week_file
        self.api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.games_data = self._load_games_data()
        self.current_week_data = self._load_current_week_data()
    
    def _fetch_live_betting_lines(self, week: int = 15, year: int = 2025) -> List[Dict[str, Any]]:
        """Fetch live betting lines from GraphQL API"""
        import requests
        
        query = """
        query {
          game(where: {season: {_eq: %d}, week: {_eq: %d}}) {
            id
            homeTeam
            awayTeam
            lines {
              provider { name }
              spread
              overUnder
            }
          }
        }
        """ % (year, week)
        
        try:
            print(f"🔍 DEBUG: Calling GraphQL with week={week}, year={year}")
            response = requests.post(
                self.graphql_url,
                json={"query": query},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🔍 DEBUG: GraphQL response status: {response.status_code}")
                print(f"🔍 DEBUG: Response keys: {list(data.keys())}")
                
                # Check for errors
                if 'errors' in data:
                    import json as json_lib
                    print(f"❌ GraphQL errors: {json_lib.dumps(data['errors'], indent=2)}")
                    return {}
                
                games = data.get('data', {}).get('game', [])
                print(f"🔍 DEBUG: Found {len(games)} games in response")
                
                # Transform to expected format
                formatted_games = []
                for game in games:
                    formatted_lines = []
                    for line in game.get('lines', []):
                        formatted_lines.append({
                            'provider': line.get('provider', {}).get('name', 'Unknown'),
                            'spread': line.get('spread'),
                            'overUnder': line.get('overUnder')
                        })
                    
                    formatted_games.append({
                        'id': game.get('id'),
                        'homeTeam': game.get('homeTeam'),
                        'awayTeam': game.get('awayTeam'),
                        'lines': formatted_lines
                    })
                
                print(f"✅ Fetched {len(formatted_games)} games with live betting lines from GraphQL")
                return {'games': formatted_games}  # Return dict format to match expected structure
            else:
                print(f"⚠️  GraphQL API returned status {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching live betting lines: {e}")
            return {}  # Return empty dict instead of list
        
    def _load_games_data(self) -> Dict[str, Any]:
        """Load games data from GraphQL API (live) or fallback to JSON file"""
        
        # First try to fetch live data from GraphQL
        live_data = self._fetch_live_betting_lines()
        if live_data:
            print(f"✅ Using live data from GraphQL API")
            return live_data
        
        # Fallback to JSON file
        try:
            if os.path.exists(self.lines_file):
                with open(self.lines_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"⚠️  Using cached data from {self.lines_file}")
                    return data
            else:
                print(f"⚠️  Betting lines file {self.lines_file} not found")
                return {'games': []}
        except Exception as e:
            print(f"❌ Error loading betting lines: {e}")
            return {'games': []}
    
    def _load_current_week_data(self) -> Dict[str, Any]:
        """Load current week games data with enhanced formatting"""
        try:
            if os.path.exists(self.current_week_file):
                with open(self.current_week_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded {len(data.get('games', []))} games from {self.current_week_file}")
                    return data
            else:
                print(f"⚠️  Current week file {self.current_week_file} not found")
                return {'games': []}
        except Exception as e:
            print(f"❌ Error loading current week data: {e}")
            return {'games': []}
    
    def find_game_by_teams(self, home_team: str, away_team: str) -> Optional[Dict[str, Any]]:
        """Find a game by team names"""
        home_team_clean = self._clean_team_name(home_team)
        away_team_clean = self._clean_team_name(away_team)
        
        # First try current week data (has better formatting)
        games_list = self.current_week_data.get('games', [])
        # Handle both direct list and nested {"all": []} format
        if isinstance(games_list, dict):
            games_list = games_list.get('all', [])
            
        for game in games_list:
            game_home = self._clean_team_name(game.get('homeTeam', {}).get('name', ''))
            game_away = self._clean_team_name(game.get('awayTeam', {}).get('name', ''))
            
            if game_home == home_team_clean and game_away == away_team_clean:
                return game
        
        # Fallback to week15.json format (can be list or dict)
        if isinstance(self.games_data, list):
            games_list = self.games_data
        else:
            games_list = self.games_data.get('games', [])
            
        for game in games_list:
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
    
    def get_game_metadata(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Get game metadata including date, time, network info, and rankings"""
        game = self.find_game_by_teams(home_team, away_team)
        
        if not game:
            return {
                'date': 'October 25, 2025',
                'time': '4:00 PM ET',
                'network': 'TBD',
                'excitement_index': 4.2,
                'home_rank': None,
                'away_rank': None
            }
        
        # Handle Currentweekgames.json format
        if 'datetime' in game:
            datetime_info = game['datetime']
            date = datetime_info.get('date', '2025-10-25')
            time_24h = datetime_info.get('time', '16:00')
            day_of_week = datetime_info.get('dayOfWeek', 'Saturday')
            
            # Get rankings from current week data
            home_rank = game.get('homeTeam', {}).get('rank')
            away_rank = game.get('awayTeam', {}).get('rank')
            
            # Convert 24h to 12h format with ET
            try:
                hour = int(time_24h.split(':')[0])
                minute = time_24h.split(':')[1]
                if hour == 0:
                    time_12h = f"12:{minute} AM ET"
                elif hour < 12:
                    time_12h = f"{hour}:{minute} AM ET"
                elif hour == 12:
                    time_12h = f"12:{minute} PM ET"
                else:
                    time_12h = f"{hour - 12}:{minute} PM ET"
            except:
                time_12h = "4:00 PM ET"
            
            # Format date as "October 25, 2025"
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            except:
                formatted_date = "October 25, 2025"
            
            # Extract network from media info or infer from time/matchup
            network = 'TBD'
            if 'media' in game:
                media_data = game['media']
                network = media_data.get('network', 'TBD')
            else:
                # Infer network from time slot and ranked matchups
                try:
                    hour = int(time_24h.split(':')[0])
                    home_rank = game.get('homeTeam', {}).get('rank')
                    away_rank = game.get('awayTeam', {}).get('rank')
                    is_ranked_matchup = home_rank or away_rank
                    
                    # Prime time games
                    if hour >= 19:  # 7pm ET or later
                        if is_ranked_matchup:
                            network = 'NBC' if hour >= 20 else 'ABC'
                        else:
                            network = 'ESPN'
                    elif hour >= 15:  # 3pm - 7pm
                        network = 'CBS' if is_ranked_matchup else 'ESPN2'
                    else:  # Noon or earlier
                        network = 'FOX' if is_ranked_matchup else 'FS1'
                except:
                    network = 'TBD'
            
            return {
                'date': formatted_date,
                'time': time_12h,
                'network': network,
                'excitement_index': 4.2,
                'day_of_week': day_of_week,
                'home_rank': home_rank,
                'away_rank': away_rank
            }
        
        # Handle week9.json format (fallback)
        try:
            start_date = game.get('startDate', '2025-10-25T16:00:00.000Z')
            from datetime import datetime
            date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%B %d, %Y')
            time_12h = date_obj.strftime('%I:%M %p ET')
            
            return {
                'date': formatted_date,
                'time': time_12h,
                'network': 'TBD',
                'excitement_index': 4.2,
                'home_rank': None,
                'away_rank': None
            }
        except:
            return {
                'date': 'October 25, 2025',
                'time': '4:00 PM ET',
                'network': 'TBD',
                'excitement_index': 4.2,
                'home_rank': None,
                'away_rank': None
            }
    
    def get_betting_analysis(self, home_team: str, away_team: str, model_spread: float = None, model_total: float = None) -> Dict[str, Any]:
        """Get detailed betting analysis for a game"""
        game = self.find_game_by_teams(home_team, away_team)
        
        if not game:
            return self._get_empty_betting_analysis()
        
        # Handle GraphQL live data format (lines array)
        if 'lines' in game:
            lines_data = game['lines']
            
            # Calculate consensus from lines
            spreads = [line.get('spread') for line in lines_data if line.get('spread') is not None]
            totals = [line.get('overUnder') for line in lines_data if line.get('overUnder') is not None]
            
            avg_spread = sum(spreads) / len(spreads) if spreads else 0
            avg_total = sum(totals) / len(totals) if totals else 0
            
            # Format spread display
            if avg_spread > 0:
                formatted_spread = f"{game['awayTeam']} -{avg_spread:.1f}"
            elif avg_spread < 0:
                formatted_spread = f"{game['homeTeam']} {abs(avg_spread):.1f}"
            else:
                formatted_spread = "Pick'em"
            
            # Use lines directly as providers
            providers_data = lines_data
            providers_list = lines_data
            
            # Use first provider for specific line info
            first_provider = providers_data[0] if providers_data else {}
            
        # Handle Currentweekgames.json format (fallback)
        elif 'bettingLines' in game:
            betting_lines = game['bettingLines']
            
            # Get consensus data (already calculated in JSON)
            consensus = betting_lines.get('consensus', {})
            avg_spread = consensus.get('spread', 0)
            avg_total = consensus.get('overUnder', 0)
            
            # Get provider data from providers list
            providers_data = betting_lines.get('allProviders', [])
            providers_list = betting_lines.get('allProviders', [])
            
            # Format spread display
            if avg_spread > 0:
                formatted_spread = f"{game['awayTeam']['name']} -{avg_spread:.1f}"
            elif avg_spread < 0:
                formatted_spread = f"{game['homeTeam']['name']} {abs(avg_spread):.1f}"
            else:
                formatted_spread = "Pick'em"
            
            # Use first provider for specific line info
            first_provider = providers_data[0] if providers_data else {}
            
        # Handle week9.json format (fallback)
        elif 'betting_lines' in game and game.get('betting_lines', {}).get('lines_available'):
            betting_lines = game['betting_lines']
            avg_spread = betting_lines.get('spread', 0)
            avg_total = betting_lines.get('over_under', 0)
            formatted_spread = betting_lines.get('formatted_spread', 'N/A')
            providers_list = betting_lines.get('all_providers', [])
            first_provider = {
                'provider': betting_lines.get('provider', 'Unknown'),
                'moneylineHome': betting_lines.get('home_moneyline', 'N/A'),
                'moneylineAway': betting_lines.get('away_moneyline', 'N/A')
            }
        else:
            return self._get_empty_betting_analysis()
        
        # Extract market data
        market_spread = avg_spread
        market_total = avg_total
        
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
        
        # Build individual sportsbook lines for UI display
        individual_sportsbooks = []
        for provider in providers_data:
            # Handle both GraphQL format (lines) and JSON format (allProviders)
            provider_name = provider.get('provider', {}).get('name') if isinstance(provider.get('provider'), dict) else provider.get('provider', 'Unknown')
            
            individual_sportsbooks.append({
                'provider': provider_name,
                'spread': provider.get('spread', 0),
                'spreadOpen': provider.get('spreadOpen', 0),
                'overUnder': provider.get('overUnder', 0),
                'overUnderOpen': provider.get('overUnderOpen', 0),
                'moneylineHome': provider.get('moneylineHome', 'N/A'),
                'moneylineAway': provider.get('moneylineAway', 'N/A')
            })
        
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
                'primary_provider': first_provider.get('provider', 'Unknown'),
                'all_providers': providers_list,
                'home_moneyline': first_provider.get('homeMoneyline', 'N/A'),
                'away_moneyline': first_provider.get('awayMoneyline', 'N/A'),
                'spread_open': first_provider.get('spreadOpen', 'N/A'),
                'total_open': first_provider.get('overUnderOpen', 'N/A'),
                'individual_books': individual_sportsbooks  # NEW: Individual sportsbook lines
            },
            'data_source': 'College Football Data API',
            'last_updated': 'Current Week Data'
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
                'individual_books': [],  # Fix: Frontend expects this field
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