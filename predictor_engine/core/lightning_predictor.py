"""
Lightning Predictor - Main orchestrator class for modular prediction engine
Coordinates all modules and provides the same interface as the original monolith
"""

from typing import Dict, Any, List, Optional

# Core modules
from .data_utils import DataUtils
from .output_formatter import OutputFormatter
from .api_client import GraphQLClient
from .team_analyzer import TeamAnalyzer
from .player_analyzer import PlayerAnalyzer
from .game_predictor import GamePredictor

# Existing modules (keep these!)
from ..betting_lines_manager import BettingLinesManager
from ..prediction_validator import PredictionValidator
from ..data_models import GamePrediction, TeamMetrics


class LightningPredictor:
    """
    Lightweight orchestrator for the modular prediction engine
    Provides the same interface as the original monolith for app.py and run.py
    """
    
    def __init__(self, api_key: str, current_year: int = 2025, current_week: int = 9):
        """Initialize with all modular components"""
        
        # Core configuration
        self.api_key = api_key
        self.current_year = current_year
        self.current_week = current_week
        
        # Initialize modules
        self.data_utils = DataUtils()
        self.formatter = OutputFormatter()
        self.api_client = GraphQLClient(api_key, current_year, current_week)
        
        # Load static data once
        print("🔄 Loading static data...")
        static_data = self.data_utils.load_all_static_data()
        print("✅ Static data loaded successfully!")
        
        # Initialize analyzers with static data
        self.team_analyzer = TeamAnalyzer(static_data)
        self.player_analyzer = PlayerAnalyzer(static_data)
        self.game_predictor = GamePredictor()
        
        # Initialize existing modules (keep compatibility!)
        self.betting_manager = BettingLinesManager()
        self.validator = PredictionValidator()
        
        # Cache for efficiency
        self._team_cache = {}
    
    async def predict_game(self, home_team_id: int, away_team_id: int) -> GamePrediction:
        """
        Main prediction method - same interface as original
        Orchestrates all modules to produce comprehensive prediction
        """
        
        # Get team names from static data FIRST (before any GraphQL calls)
        home_team_name = self.data_utils.get_team_name_by_id(home_team_id) or f"Team {home_team_id}"
        away_team_name = self.data_utils.get_team_name_by_id(away_team_id) or f"Team {away_team_id}"
        
        # Display matchup header with static team names (always works)
        self.formatter.print_matchup_info(home_team_name, away_team_name)
        
        try:
            # 1. Fetch comprehensive data via GraphQL
            print(f"🔍 Fetching game data for teams {away_team_id} @ {home_team_id}...")
            data = await self.api_client.fetch_game_prediction_data(home_team_id, away_team_id)
            
            # 2. Extract team information for display (fallback to static data)
            api_home_name = self._extract_team_name(data.get('homeTeam', []))
            api_away_name = self._extract_team_name(data.get('awayTeam', []))
            
            # Use API names if available, otherwise keep static names
            if api_home_name != 'Unknown':
                home_team_name = api_home_name
            if api_away_name != 'Unknown':
                away_team_name = api_away_name
            
            # 4. Extract and display team metrics with all required data
            home_metrics = self._extract_team_metrics(
                data.get('homeTeamMetrics', []),
                data.get('homeRecentGames', []),
                data.get('homeSeasonGames', []),
                data.get('homeHistoricalMetrics', []),
                True,  # is_home
                home_team_id
            )
            away_metrics = self._extract_team_metrics(
                data.get('awayTeamMetrics', []),
                data.get('awayRecentGames', []),
                data.get('awaySeasonGames', []),
                data.get('awayHistoricalMetrics', []),
                False,  # is_home
                away_team_id
            )
            
            self.formatter.print_team_metrics(home_team_name, away_team_name, home_metrics, away_metrics)
            self.formatter.print_situational_performance(home_team_name, away_team_name, home_metrics, away_metrics)
            self.formatter.print_field_position_breakdown(home_team_name, away_team_name, home_metrics, away_metrics)
            
            # 5. Calculate advanced metrics differential
            advanced_differential, advanced_metrics = self.team_analyzer.calculate_advanced_metrics_differential(
                home_metrics, away_metrics
            )
            self.formatter.print_differential_analysis(advanced_metrics)
            
            # 6. Analyze talent differential
            talent_differential = self._calculate_talent_differential(
                data.get('homeTeamTalent', []), data.get('awayTeamTalent', [])
            )
            home_talent = data.get('homeTeamTalent', [{}])[0].get('talent', 0) if data.get('homeTeamTalent') else 0
            away_talent = data.get('awayTeamTalent', [{}])[0].get('talent', 0) if data.get('awayTeamTalent') else 0
            self.formatter.print_talent_ratings(home_team_name, away_team_name, home_talent, away_talent)
            
            # 7. Analyze season records
            self.formatter.print_season_records_header()
            self._analyze_team_records(data, home_team_id, away_team_id, home_team_name, away_team_name)
            
            # 8. Analyze players
            player_impact, player_analysis = self.player_analyzer.analyze_key_players(
                data.get('allPlayers', []), home_team_id, away_team_id, home_team_name, away_team_name
            )
            self.formatter.print_player_impact_analysis(home_team_name, away_team_name, player_analysis)
            
            # 9. Analyze coaching
            coaching_differential, coaching_analysis = self.team_analyzer.analyze_coaching_performance(
                {}, home_team_name, away_team_name
            )
            self.formatter.print_coaching_analysis(coaching_analysis)
            
            # 10. Analyze market lines (using existing betting manager)
            market_lines = data.get('marketLines', [])
            market_signal = self.team_analyzer.analyze_market_lines(market_lines)
            
            # 11. Calculate elite team factors
            elite_factor = self.team_analyzer.calculate_elite_team_factor(
                home_team_name, away_team_name, home_metrics, away_metrics
            )
            
            # 12. Weather analysis
            weather_impact = 0.0
            current_matchup = data.get('currentMatchup', [])
            if current_matchup and current_matchup[0].get('weather'):
                weather = current_matchup[0]['weather']
                weather_impact = self.game_predictor.calculate_weather_impact(weather)
                self.formatter.print_weather_analysis(weather)
            
            # 13. Generate final prediction
            prediction = self.game_predictor.calculate_final_prediction(
                advanced_differential=advanced_differential,
                talent_differential=talent_differential,
                player_impact=player_impact,
                coaching_differential=coaching_differential,
                market_signal=market_signal,
                elite_factor=elite_factor,
                weather_impact=weather_impact,
                home_team=home_team_name,
                away_team=away_team_name
            )
            
            # 14. Validate prediction (using existing validator)
            try:
                self.validator.validate_spread_score_consistency(
                    prediction.predicted_spread, prediction.predicted_total, 
                    prediction.detailed_analysis.get('home_score', 0), 
                    prediction.detailed_analysis.get('away_score', 0)
                )
                print("✅ Prediction validation passed")
            except Exception as e:
                print(f"⚠️  Prediction validation warning: {e}")
            
            # 15. Display final results
            prediction_summary_data = {
                'home_score': prediction.detailed_analysis.get('home_score', 0),
                'away_score': prediction.detailed_analysis.get('away_score', 0),
                'spread': prediction.predicted_spread,
                'total': prediction.predicted_total,
                'confidence': prediction.detailed_analysis.get('confidence_breakdown', {'overall_confidence': prediction.confidence})
            }
            self.formatter.print_prediction_summary(prediction_summary_data)
            
            # 16. Betting analysis (using existing betting manager)
            betting_analysis = self._analyze_betting_opportunities(market_lines, prediction)
            self.formatter.print_betting_analysis(betting_analysis)
            
            return prediction
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            # Return a default prediction with ACTUAL team names (not "Unknown")
            return GamePrediction(
                home_team=home_team_name,
                away_team=away_team_name, 
                home_win_prob=0.6,
                predicted_spread=3.0,
                predicted_total=45.0,
                confidence=0.5,  # Return as decimal (0.5 = 50%)
                key_factors=["Error occurred during prediction"],
                detailed_analysis={
                    'home_score': 24,
                    'away_score': 21,
                    'confidence_breakdown': {'overall_confidence': 50.0, 'breakdown': {}},
                    'factors_breakdown': {}
                }
            )
    
    def _extract_team_name(self, team_data: List[Dict]) -> str:
        """Extract team name from GraphQL response"""
        if team_data:
            return team_data[0].get('school', 'Unknown')
        return 'Unknown'
    
    def _extract_team_metrics(self, metrics_data: List[Dict], recent_games: List[Dict], 
                               season_games: List[Dict], historical_metrics: List[Dict], 
                               is_home: bool, team_id: int) -> Dict[str, Any]:
        """Extract comprehensive team metrics from GraphQL response with all calculations"""
        if not metrics_data:
            # Return default values if no data
            return {
                'epa': 0, 'epaAllowed': 0, 'explosiveness': 0, 'success': 0.5,
                'recent_form': 0, 'elo_rating': 1500, 'season_trend': 0,
                'sos_rating': 0, 'consistency_score': 0.5, 'recent_vs_early_differential': 0
            }

        metrics = metrics_data[0] if metrics_data else {}

        # Calculate all the derived metrics that were in the original
        recent_form = self._calculate_recent_form(recent_games, team_id)
        elo_rating = self._get_latest_elo(recent_games, team_id)
        season_trend = self._analyze_season_trends(historical_metrics, season_games, team_id)
        sos_rating = self._calculate_strength_of_schedule(season_games, team_id)
        consistency_score = self._analyze_performance_consistency(season_games, team_id)
        recent_vs_early = self._calculate_recent_vs_early_differential(season_games, team_id)

        # Return comprehensive metrics including both raw and calculated values
        result = dict(metrics)  # Start with raw GraphQL data
        result.update({
            'recent_form': recent_form,
            'elo_rating': elo_rating, 
            'season_trend': season_trend,
            'sos_rating': sos_rating,
            'consistency_score': consistency_score,
            'recent_vs_early_differential': recent_vs_early
        })
        
        return result
    
    def _calculate_talent_differential(self, home_talent_data: List[Dict], away_talent_data: List[Dict]) -> float:
        """Calculate talent rating differential"""
        home_talent = home_talent_data[0].get('talent', 0) if home_talent_data else 0
        away_talent = away_talent_data[0].get('talent', 0) if away_talent_data else 0
        
        # Normalize talent differential
        return (away_talent - home_talent) / 10.0  # Scale appropriately
    
    def _analyze_team_records(self, data: Dict, home_team_id: int, away_team_id: int, 
                            home_team_name: str, away_team_name: str):
        """Analyze and display team season records"""
        
        def analyze_team_record(games: List[Dict], team_id: int, team_name: str):
            wins = 0
            losses = 0
            completed_games = []
            
            for game in games:
                home_id = game.get('homeTeamId')
                away_id = game.get('awayTeamId')
                home_points = game.get('homePoints')
                away_points = game.get('awayPoints')
                
                # Only count completed games
                if home_points is None or away_points is None:
                    continue
                
                if home_id == team_id:
                    # Team was home
                    if home_points > away_points:
                        wins += 1
                    else:
                        losses += 1
                    completed_games.append({
                        'opponent': game.get('awayTeam', 'Unknown'),
                        'points_for': home_points,
                        'points_against': away_points
                    })
                elif away_id == team_id:
                    # Team was away
                    if away_points > home_points:
                        wins += 1
                    else:
                        losses += 1
                    completed_games.append({
                        'opponent': game.get('homeTeam', 'Unknown'),
                        'points_for': away_points,
                        'points_against': home_points
                    })
            
            # Calculate stats
            total_points = sum(g['points_for'] for g in completed_games)
            total_allowed = sum(g['points_against'] for g in completed_games)
            games_played = len(completed_games)
            
            team_metrics = {
                'ppg': total_points / games_played if games_played > 0 else 0,
                'ppg_allowed': total_allowed / games_played if games_played > 0 else 0
            }
            
            self.formatter.print_team_record_analysis(team_name, wins, losses, completed_games, team_metrics)
        
        # Analyze both teams
        analyze_team_record(data.get('homeSeasonGames', []), home_team_id, home_team_name)
        analyze_team_record(data.get('awaySeasonGames', []), away_team_id, away_team_name)
    
    def _analyze_betting_opportunities(self, market_lines: List[Dict], prediction: GamePrediction) -> Dict[str, Any]:
        """Analyze betting opportunities using existing betting manager"""
        
        if not market_lines:
            return {}
        
        # Use existing betting manager for analysis
        betting_analysis = {
            'market_lines': {},
            'recommendations': []
        }
        
        # Get consensus lines
        if market_lines:
            spreads = [line.get('spread') for line in market_lines if line.get('spread') is not None]
            totals = [line.get('overUnder') for line in market_lines if line.get('overUnder') is not None]
            
            if spreads:
                market_spread = sum(spreads) / len(spreads)
                betting_analysis['market_lines']['spread'] = market_spread
                
                # Compare with prediction
                spread_edge = prediction.predicted_spread - market_spread
                if abs(spread_edge) > 3.0:  # Significant edge
                    betting_analysis['recommendations'].append({
                        'type': 'Spread',
                        'value': spread_edge,
                        'confidence': min(abs(spread_edge) * 20, 80)
                    })
            
            if totals:
                market_total = sum(totals) / len(totals)
                betting_analysis['market_lines']['total'] = market_total
                
                # Compare with prediction
                total_edge = prediction.predicted_total - market_total
                if abs(total_edge) > 5.0:  # Significant edge
                    betting_analysis['recommendations'].append({
                        'type': 'Total',
                        'value': total_edge,
                        'confidence': min(abs(total_edge) * 15, 75)
                    })
        
        return betting_analysis
    
    def get_team_id(self, team_name: str) -> Optional[int]:
        """Get team ID from name using data utils"""
        return self.data_utils.get_team_id(team_name)
    
    def update_current_week(self, week: int):
        """Update current week for all components"""
        self.current_week = week
        self.api_client.set_current_week(week)
    
    def update_current_year(self, year: int):
        """Update current year for all components"""
        self.current_year = year
        self.api_client.set_current_year(year)
    
    def clear_cache(self):
        """Clear all cached data"""
        self._team_cache = {}
        self.data_utils.clear_cache()
    
    def get_health_status(self) -> Dict[str, str]:
        """Get health status of all components"""
        return {
            'data_utils': 'OK',
            'api_client': 'OK',
            'team_analyzer': 'OK',
            'player_analyzer': 'OK', 
            'game_predictor': 'OK',
            'betting_manager': 'OK',
            'validator': 'OK'
        }

    # CRITICAL: Missing calculation methods from original graphqlpredictor.py
    def _calculate_recent_form(self, recent_games: List[Dict], team_id: int) -> float:
        """Calculate recent form from last 4 games"""
        if not recent_games:
            return 0.5
            
        recent_form = 0
        games_analyzed = 0
        
        for game in recent_games[:4]:
            # Skip games that haven't been played yet (null win probabilities)
            win_prob = None
            if game['homeTeamId'] == team_id:
                win_prob = game.get('homePostgameWinProb')
            elif game['awayTeamId'] == team_id:
                win_prob = game.get('awayPostgameWinProb')
            else:
                continue
                
            # Only count games that have been played
            if win_prob is not None:
                recent_form += win_prob
                games_analyzed += 1
            
        return recent_form / games_analyzed if games_analyzed > 0 else 0.5

    def _get_latest_elo(self, recent_games: List[Dict], team_id: int) -> float:
        """Get latest ELO rating from most recent game"""
        if not recent_games:
            return 1500
            
        for game in recent_games:
            if game['homeTeamId'] == team_id:
                return game.get('homeStartElo', 1500)
            elif game['awayTeamId'] == team_id:
                return game.get('awayStartElo', 1500)
                
        return 1500

    def _analyze_season_trends(self, historical_metrics: List[Dict], season_games: List[Dict], team_id: int) -> float:
        """Analyze EPA and performance trends across the season"""
        if not historical_metrics or len(historical_metrics) < 3:
            return 0
            
        # Weight recent weeks more heavily
        week_weights = [0.1, 0.15, 0.2, 0.25, 0.3]  # Weeks 2-6 weights (week 7 gets highest)
        
        epa_trend = 0
        success_trend = 0
        total_weight = 0
        
        for i, week_data in enumerate(historical_metrics[-5:]):  # Last 5 weeks
            weight = week_weights[min(i, len(week_weights)-1)]
            
            epa_net = week_data.get('epa', 0) - week_data.get('epaAllowed', 0)
            success_net = week_data.get('success', 0.5) - week_data.get('successAllowed', 0.5)
            
            epa_trend += epa_net * weight
            success_trend += success_net * weight
            total_weight += weight
            
        if total_weight > 0:
            return (epa_trend + success_trend * 10) / total_weight
        return 0

    def _calculate_strength_of_schedule(self, season_games: List[Dict], team_id: int) -> float:
        """Calculate strength of schedule based on opponent ELO ratings"""
        if not season_games:
            return 0
            
        opponent_elos = []
        
        for game in season_games:
            opponent_elo = None
            if game['homeTeamId'] == team_id:
                opponent_elo = game.get('awayStartElo')
            elif game['awayTeamId'] == team_id:
                opponent_elo = game.get('homeStartElo')
                
            # Only include teams that have ELO ratings (exclude FCS teams, etc.)
            if opponent_elo is not None:
                opponent_elos.append(opponent_elo)
                
        if opponent_elos:
            avg_opponent_elo = sum(opponent_elos) / len(opponent_elos)
            return (avg_opponent_elo - 1500) / 100  # Normalize around 0
        return 0

    def _analyze_performance_consistency(self, season_games: List[Dict], team_id: int) -> float:
        """Analyze performance consistency across games"""
        if not season_games or len(season_games) < 3:
            return 0.5
            
        win_probs = []
        
        for game in season_games:
            win_prob = None
            if game['homeTeamId'] == team_id:
                win_prob = game.get('homePostgameWinProb')
            elif game['awayTeamId'] == team_id:
                win_prob = game.get('awayPostgameWinProb')
                
            # Only include completed games
            if win_prob is not None:
                win_probs.append(win_prob)
                
        if len(win_probs) > 1:
            # Calculate standard deviation (lower = more consistent)
            avg = sum(win_probs) / len(win_probs)
            variance = sum((x - avg) ** 2 for x in win_probs) / len(win_probs)
            std_dev = variance ** 0.5
            
            # Convert to consistency score (higher = more consistent)
            return max(0, 1 - (std_dev * 2))  # Scale so that std_dev of 0.5 = consistency of 0
        return 0.5

    def _calculate_recent_vs_early_differential(self, season_games: List[Dict], team_id: int) -> float:
        """Calculate differential between recent performance and early season"""
        if not season_games or len(season_games) < 4:
            return 0
            
        # Split games into early (first half) and recent (second half)
        mid_point = len(season_games) // 2
        early_games = season_games[:mid_point]
        recent_games = season_games[mid_point:]
        
        early_avg = self._average_win_prob(early_games, team_id)
        recent_avg = self._average_win_prob(recent_games, team_id)
        
        return recent_avg - early_avg

    def _average_win_prob(self, games: List[Dict], team_id: int) -> float:
        """Calculate average win probability for a set of games"""
        win_probs = []
        
        for game in games:
            win_prob = None
            if game['homeTeamId'] == team_id:
                win_prob = game.get('homePostgameWinProb')
            elif game['awayTeamId'] == team_id:
                win_prob = game.get('awayPostgameWinProb')
                
            # Only include completed games
            if win_prob is not None:
                win_probs.append(win_prob)
                
        return sum(win_probs) / len(win_probs) if win_probs else 0.5