"""
Prediction Engine - Core calculation logic for college football game predictions
Separated from data fetching and API logic for better maintainability
"""

from typing import Dict, Tuple, List
from dataclasses import dataclass
import statistics
import math


@dataclass
class TeamMetrics:
    """Team performance metrics"""
    epa: float
    epa_allowed: float
    explosiveness: float
    success_rate: float
    talent_rating: float
    recent_form: float
    elo_rating: float
    season_trend: float
    sos_rating: float
    consistency_score: float
    recent_vs_early_differential: float


@dataclass
class GamePrediction:
    """Game prediction result"""
    home_team: str
    away_team: str
    predicted_spread: float
    predicted_total: float
    home_win_probability: float
    confidence: float
    reasoning: Dict


class PredictionEngine:
    """Core calculation engine for game predictions"""
    
    def __init__(self):
        """Initialize prediction engine with default parameters"""
        self.base_home_field_advantage = 2.5
        self.neutral_site_advantage = 0.0  # Bowl games are neutral site
        self.min_total_points = 40.0
        self.max_total_points = 85.0
        
        # Normalization ranges for component scaling
        self.normalization_ranges = {
            'epa_differential': (-0.5, 0.5),
            'composite_ratings': (-3.0, 3.0), 
            'market_consensus': (-10.0, 10.0),
            'player_impact': (-2.0, 2.0),
            'contextual_factors': (-5.0, 5.0)
        }
        
    def calculate_advanced_metrics_differential(
        self, 
        home_metrics, 
        away_metrics
    ) -> Tuple[float, Dict]:
        """
        Calculate comprehensive metrics differential between teams
        
        Returns:
            - Overall differential score
            - Dictionary of individual metric differentials
        """
        # Handle both dict and TeamMetrics objects
        def safe_get(obj, key, default=0):
            if hasattr(obj, key):
                return getattr(obj, key, default)
            elif isinstance(obj, dict):
                return obj.get(key, default)
            return default
        
        # EPA differentials (offense)
        overall_epa_diff = safe_get(home_metrics, 'epa') - safe_get(away_metrics, 'epa')
        passing_epa_diff = safe_get(home_metrics, 'passingEpa') - safe_get(away_metrics, 'passingEpa')
        rushing_epa_diff = safe_get(home_metrics, 'rushingEpa') - safe_get(away_metrics, 'rushingEpa')
        
        # Performance metrics
        success_rate_diff = safe_get(home_metrics, 'success') - safe_get(away_metrics, 'success')
        explosiveness_diff = safe_get(home_metrics, 'explosiveness') - safe_get(away_metrics, 'explosiveness')
        
        # Situational success
        passing_downs_diff = safe_get(home_metrics, 'passingDownsSuccess') - safe_get(away_metrics, 'passingDownsSuccess')
        standard_downs_diff = safe_get(home_metrics, 'standardDownsSuccess') - safe_get(away_metrics, 'standardDownsSuccess')
        
        # Field position control
        line_yards_diff = safe_get(home_metrics, 'lineYards') - safe_get(away_metrics, 'lineYards')
        second_level_diff = safe_get(home_metrics, 'secondLevelYards') - safe_get(away_metrics, 'secondLevelYards')
        open_field_diff = safe_get(home_metrics, 'openFieldYards') - safe_get(away_metrics, 'openFieldYards')
        highlight_yards_diff = safe_get(home_metrics, 'highlightYards') - safe_get(away_metrics, 'highlightYards')
        
        # Defensive edge (away defense - home defense, so positive = home advantage)
        epa_defense_diff = safe_get(away_metrics, 'epaAllowed') - safe_get(home_metrics, 'epaAllowed')
        passing_defense_diff = safe_get(away_metrics, 'passingEpaAllowed') - safe_get(home_metrics, 'passingEpaAllowed')
        rushing_defense_diff = safe_get(away_metrics, 'rushingEpaAllowed') - safe_get(home_metrics, 'rushingEpaAllowed')
        success_defense_diff = safe_get(away_metrics, 'successAllowed') - safe_get(home_metrics, 'successAllowed')
        explosiveness_defense_diff = safe_get(away_metrics, 'explosivenessAllowed') - safe_get(home_metrics, 'explosivenessAllowed')
        
        # Situational defense
        passing_downs_defense = safe_get(away_metrics, 'passingDownsSuccessAllowed') - safe_get(home_metrics, 'passingDownsSuccessAllowed')
        standard_downs_defense = safe_get(away_metrics, 'standardDownsSuccessAllowed') - safe_get(home_metrics, 'standardDownsSuccessAllowed')
        situational_defense_diff = (passing_downs_defense + standard_downs_defense) / 2
        
        # Weights for each metric category
        weights = {
            'overall_epa': 3.0,
            'passing_epa': 2.5,
            'rushing_epa': 2.0,
            'success_rate': 2.0,
            'explosiveness': 1.5,
            'passing_downs': 1.5,
            'standard_downs': 1.0,
            'line_yards': 1.0,
            'second_level': 0.8,
            'open_field': 0.8,
            'highlight_yards': 0.5,
            'epa_defense': 2.5,
            'passing_defense': 2.0,
            'rushing_defense': 2.0,
            'success_defense': 1.5,
            'explosiveness_defense': 1.0,
            'situational_defense': 1.5
        }
        
        # Calculate weighted differential
        weighted_sum = (
            overall_epa_diff * weights['overall_epa'] +
            passing_epa_diff * weights['passing_epa'] +
            rushing_epa_diff * weights['rushing_epa'] +
            success_rate_diff * weights['success_rate'] +
            explosiveness_diff * weights['explosiveness'] +
            passing_downs_diff * weights['passing_downs'] +
            standard_downs_diff * weights['standard_downs'] +
            line_yards_diff * weights['line_yards'] +
            second_level_diff * weights['second_level'] +
            open_field_diff * weights['open_field'] +
            highlight_yards_diff * weights['highlight_yards'] +
            epa_defense_diff * weights['epa_defense'] +
            passing_defense_diff * weights['passing_defense'] +
            rushing_defense_diff * weights['rushing_defense'] +
            success_defense_diff * weights['success_defense'] +
            explosiveness_defense_diff * weights['explosiveness_defense'] +
            situational_defense_diff * weights['situational_defense']
        )
        
        total_weight = sum(weights.values())
        overall_differential = (weighted_sum / total_weight) * 100  # Scale to point spread
        
        # Return both overall differential and component details
        metrics_detail = {
            'overall_epa_diff': overall_epa_diff,
            'passing_epa_diff': passing_epa_diff,
            'rushing_epa_diff': rushing_epa_diff,
            'success_rate_diff': success_rate_diff,
            'explosiveness_diff': explosiveness_diff,
            'passing_downs_diff': passing_downs_diff,
            'standard_downs_diff': standard_downs_diff,
            'line_yards_diff': line_yards_diff,
            'second_level_diff': second_level_diff,
            'open_field_diff': open_field_diff,
            'highlight_yards_diff': highlight_yards_diff,
            'epa_defense_diff': epa_defense_diff,
            'passing_defense_diff': passing_defense_diff,
            'rushing_defense_diff': rushing_defense_diff,
            'success_defense_diff': success_defense_diff,
            'explosiveness_defense_diff': explosiveness_defense_diff,
            'situational_defense_diff': situational_defense_diff
        }
        
        return overall_differential, metrics_detail
    
    def calculate_spread(
        self,
        home_metrics: TeamMetrics,
        away_metrics: TeamMetrics,
        advanced_differential: float,
        talent_gap: float
    ) -> float:
        """
        Calculate predicted point spread
        
        Args:
            home_metrics: Home team performance metrics
            away_metrics: Away team performance metrics
            advanced_differential: Pre-calculated advanced metrics differential
            talent_gap: Talent rating difference
            
        Returns:
            Predicted spread (positive = home favored)
        """
        # Start with advanced metrics differential
        base_spread = advanced_differential
        
        # Add home field advantage
        base_spread += self.base_home_field_advantage
        
        # Factor in talent gap (moderate weight)
        talent_factor = talent_gap * 0.15
        base_spread += talent_factor
        
        # Recent form adjustment
        form_diff = home_metrics.recent_form - away_metrics.recent_form
        base_spread += form_diff * 0.5
        
        # Season trend adjustment
        trend_diff = home_metrics.season_trend - away_metrics.season_trend
        base_spread += trend_diff * 0.3
        
        # ELO rating adjustment
        elo_diff = (home_metrics.elo_rating - away_metrics.elo_rating) / 25
        base_spread += elo_diff
        
        return round(base_spread, 1)
    
    def calculate_enhanced_prediction(self, home_team: str, away_team: str, 
                                   home_metrics, away_metrics,
                                   game_data: Dict) -> Dict:
        """Enhanced prediction calculation with all new data sources"""
        
        # Load additional data
        situational_data = self.load_situational_performance(home_team, away_team)
        analytics_data = self.load_season_analytics(home_team, away_team)
        drive_data = self.load_drive_efficiency(home_team, away_team)
        
        # Detect neutral site
        is_neutral_site = self.detect_neutral_site(game_data)
        home_field_advantage = self.neutral_site_advantage if is_neutral_site else self.base_home_field_advantage
        
        # Calculate advanced metrics differential
        advanced_diff, _ = self.calculate_advanced_metrics_differential(home_metrics, away_metrics)
        
        # Enhanced situational factors
        situational_edge = self._calculate_situational_edge(situational_data, home_team, away_team, is_neutral_site)
        
        # Drive efficiency differential
        drive_efficiency_edge = self._calculate_drive_efficiency_edge(drive_data, home_team, away_team)
        
        # Season analytics edge
        analytics_edge = self._calculate_analytics_edge(analytics_data, home_team, away_team)
        
        # Normalize all components 
        normalized_advanced = self.normalize_component(advanced_diff, 'epa_differential')
        normalized_situational = self.normalize_component(situational_edge, 'contextual_factors')
        normalized_drive = self.normalize_component(drive_efficiency_edge, 'player_impact')
        normalized_analytics = self.normalize_component(analytics_edge, 'composite_ratings')
        
        # Enhanced weights with proper normalization
        enhanced_weights = {
            'advanced_metrics': 0.35,  # EPA, success rates, etc.
            'drive_efficiency': 0.25,   # Scoring rate, yards/play from drives
            'season_analytics': 0.20,   # Red zone, third down efficiency
            'situational_performance': 0.20  # Neutral site, vs ranked, clutch
        }
        
        # Calculate weighted prediction
        raw_prediction = (
            normalized_advanced * enhanced_weights['advanced_metrics'] +
            normalized_drive * enhanced_weights['drive_efficiency'] +
            normalized_analytics * enhanced_weights['season_analytics'] +
            normalized_situational * enhanced_weights['situational_performance']
        )
        
        # Scale to point spread range and add home field
        final_spread = (raw_prediction * 7.0) + home_field_advantage
        
        # Calculate total using enhanced data
        predicted_total = self._calculate_enhanced_total(analytics_data, drive_data, home_team, away_team)
        
        return {
            'predicted_spread': round(final_spread, 1),
            'predicted_total': round(predicted_total, 1),
            'is_neutral_site': is_neutral_site,
            'home_field_advantage': home_field_advantage,
            'component_contributions': {
                'advanced_metrics': normalized_advanced * enhanced_weights['advanced_metrics'],
                'drive_efficiency': normalized_drive * enhanced_weights['drive_efficiency'],
                'season_analytics': normalized_analytics * enhanced_weights['season_analytics'],
                'situational_performance': normalized_situational * enhanced_weights['situational_performance']
            },
            'raw_prediction': raw_prediction
        }
        
    def normalize_component(self, value: float, component_type: str) -> float:
        """Normalize component values to -1.0 to +1.0 range for proper weighting"""
        if component_type not in self.normalization_ranges:
            return value
            
        min_val, max_val = self.normalization_ranges[component_type]
        
        # Clamp to range first
        clamped = max(min_val, min(max_val, value))
        
        # Normalize to -1.0 to +1.0
        if max_val == min_val:
            return 0.0
            
        normalized = 2.0 * (clamped - min_val) / (max_val - min_val) - 1.0
        return normalized
        
    def detect_neutral_site(self, game_data: Dict) -> bool:
        """Detect if game is played on neutral site (bowl games, playoffs)"""
        # Check for postseason games from database
        season_type = game_data.get('season_type', '')
        if season_type and 'postseason' in season_type.lower():
            return True
            
        # Check game title/venue for bowl game indicators
        game_title = game_data.get('title', '').lower()
        bowl_indicators = ['bowl', 'championship', 'playoff', 'semifinal', 'final']
        
        if any(indicator in game_title for indicator in bowl_indicators):
            return True
            
        # Check venue location vs team locations
        venue = game_data.get('venue', {}).get('name', '').lower()
        home_team = game_data.get('homeTeam', [{}])[0].get('school', '').lower()
        
        # If venue doesn't contain home team name, likely neutral
        if home_team and home_team not in venue:
            venue_indicators = ['stadium', 'dome', 'center', 'arena']
            if any(indicator in venue for indicator in venue_indicators):
                return True
                
        return False
        
    def load_situational_performance(self, home_team: str, away_team: str) -> Dict:
        """Load situational performance data from coaches_master.db"""
        import sqlite3
        from pathlib import Path
        
        try:
            db_path = Path(__file__).parent / 'instance' / 'coaches_master.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get situational stats for both teams
            query = """
            SELECT school, neutral_record, vs_ranked_record, vs_top_10_record,
                   one_score_wins, one_score_losses, comeback_wins,
                   home_record, away_record
            FROM situational_stats 
            WHERE school IN (?, ?)
            """
            
            cursor.execute(query, (home_team, away_team))
            results = cursor.fetchall()
            
            situational_data = {}
            for row in results:
                school = row[0]
                situational_data[school] = {
                    'neutral_record': row[1],
                    'vs_ranked_record': row[2], 
                    'vs_top_10_record': row[3],
                    'one_score_wins': row[4] or 0,
                    'one_score_losses': row[5] or 0,
                    'comeback_wins': row[6] or 0,
                    'home_record': row[7],
                    'away_record': row[8]
                }
            
            conn.close()
            return situational_data
            
        except Exception as e:
            print(f"Warning: Could not load situational data: {e}")
            return {}
    
    def load_season_analytics(self, home_team: str, away_team: str, season: int = 2025) -> Dict:
        """Load advanced season analytics from coaches_master.db"""
        import sqlite3
        from pathlib import Path
        
        try:
            db_path = Path(__file__).parent / 'instance' / 'coaches_master.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = """
            SELECT school, red_zone_pct, third_down_pct, fourth_down_pct,
                   points_per_game, points_allowed_pg, yards_per_play, yards_per_play_allowed,
                   sp_overall, sp_offense, sp_defense
            FROM season_analytics 
            WHERE school IN (?, ?) AND season = ?
            ORDER BY season DESC
            """
            
            cursor.execute(query, (home_team, away_team, season))
            results = cursor.fetchall()
            
            analytics_data = {}
            for row in results:
                school = row[0]
                analytics_data[school] = {
                    'red_zone_pct': row[1] or 0.0,
                    'third_down_pct': row[2] or 0.0,
                    'fourth_down_pct': row[3] or 0.0,
                    'points_per_game': row[4] or 0.0,
                    'points_allowed_pg': row[5] or 0.0,
                    'yards_per_play': row[6] or 0.0,
                    'yards_per_play_allowed': row[7] or 0.0,
                    'sp_overall': row[8] or 0.0,
                    'sp_offense': row[9] or 0.0,
                    'sp_defense': row[10] or 0.0
                }
            
            conn.close()
            return analytics_data
            
        except Exception as e:
            print(f"Warning: Could not load season analytics: {e}")
            return {}
    
    def load_drive_efficiency(self, home_team: str, away_team: str) -> Dict:
        """Load drive efficiency metrics from coaches_master.db"""
        import sqlite3
        from pathlib import Path
        
        try:
            db_path = Path(__file__).parent / 'instance' / 'coaches_master.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = """
            SELECT t.school,
                   AVG(CAST(d.yards as FLOAT) / d.plays_count) as yards_per_play,
                   100.0 * COUNT(CASE WHEN d.result IN ('TD', 'FG') THEN 1 END) / COUNT(*) as scoring_rate,
                   100.0 * COUNT(CASE WHEN d.result IN ('INT', 'FUMBLE') THEN 1 END) / COUNT(*) as turnover_rate,
                   AVG(d.yards) as avg_drive_yards,
                   AVG(d.plays_count) as avg_plays_per_drive
            FROM teams t 
            JOIN drives d ON t.id = d.team_id 
            WHERE t.school IN (?, ?)
            GROUP BY t.school
            """
            
            cursor.execute(query, (home_team, away_team))
            results = cursor.fetchall()
            
            drive_data = {}
            for row in results:
                school = row[0]
                drive_data[school] = {
                    'yards_per_play': row[1] or 0.0,
                    'scoring_rate': row[2] or 0.0,
                    'turnover_rate': row[3] or 0.0,
                    'avg_drive_yards': row[4] or 0.0,
                    'avg_plays_per_drive': row[5] or 0.0
                }
            
            conn.close()
            return drive_data
            
        except Exception as e:
            print(f"Warning: Could not load drive efficiency data: {e}")
            return {}
            
    def _calculate_situational_edge(self, situational_data: Dict, home_team: str, 
                                  away_team: str, is_neutral_site: bool) -> float:
        """Calculate edge from situational performance data"""
        if not situational_data:
            return 0.0
            
        home_data = situational_data.get(home_team, {})
        away_data = situational_data.get(away_team, {})
        
        edge = 0.0
        
        # Neutral site record (critical for bowl games)
        if is_neutral_site:
            home_neutral = self._parse_record(home_data.get('neutral_record', '0-0'))
            away_neutral = self._parse_record(away_data.get('neutral_record', '0-0'))
            if home_neutral['games'] > 0 and away_neutral['games'] > 0:
                edge += (home_neutral['win_pct'] - away_neutral['win_pct']) * 3.0
        
        # Clutch performance
        home_clutch_pct = 0.0
        away_clutch_pct = 0.0
        
        home_one_score = home_data.get('one_score_wins', 0) + home_data.get('one_score_losses', 0)
        if home_one_score > 0:
            home_clutch_pct = home_data.get('one_score_wins', 0) / home_one_score
            
        away_one_score = away_data.get('one_score_wins', 0) + away_data.get('one_score_losses', 0) 
        if away_one_score > 0:
            away_clutch_pct = away_data.get('one_score_wins', 0) / away_one_score
            
        edge += (home_clutch_pct - away_clutch_pct) * 2.0
        
        # Comeback ability 
        home_comebacks = home_data.get('comeback_wins', 0)
        away_comebacks = away_data.get('comeback_wins', 0)
        edge += (home_comebacks - away_comebacks) * 0.5
        
        return edge
    
    def _calculate_drive_efficiency_edge(self, drive_data: Dict, home_team: str, away_team: str) -> float:
        """Calculate edge from drive efficiency metrics"""
        if not drive_data:
            return 0.0
            
        home_data = drive_data.get(home_team, {})
        away_data = drive_data.get(away_team, {})
        
        # Yards per play differential (most predictive)
        ypp_diff = home_data.get('yards_per_play', 0.0) - away_data.get('yards_per_play', 0.0)
        
        # Scoring rate differential
        scoring_diff = home_data.get('scoring_rate', 0.0) - away_data.get('scoring_rate', 0.0)
        
        # Turnover rate differential (lower is better)
        turnover_diff = away_data.get('turnover_rate', 0.0) - home_data.get('turnover_rate', 0.0)
        
        # Weight yards per play most heavily
        edge = (ypp_diff * 2.0) + (scoring_diff * 0.05) + (turnover_diff * 0.1)
        
        return edge
    
    def _calculate_analytics_edge(self, analytics_data: Dict, home_team: str, away_team: str) -> float:
        """Calculate edge from season analytics"""
        if not analytics_data:
            return 0.0
            
        home_data = analytics_data.get(home_team, {})
        away_data = analytics_data.get(away_team, {})
        
        edge = 0.0
        
        # Red zone efficiency (critical for scoring)
        rz_diff = home_data.get('red_zone_pct', 0.0) - away_data.get('red_zone_pct', 0.0)
        edge += rz_diff * 0.02  # 10% red zone diff = 0.2 points
        
        # Third down efficiency
        third_down_diff = home_data.get('third_down_pct', 0.0) - away_data.get('third_down_pct', 0.0)
        edge += third_down_diff * 0.015
        
        # Overall SP+ differential
        sp_diff = home_data.get('sp_overall', 0.0) - away_data.get('sp_overall', 0.0)
        edge += sp_diff * 0.1
        
        return edge
    
    def _calculate_enhanced_total(self, analytics_data: Dict, drive_data: Dict, 
                                home_team: str, away_team: str) -> float:
        """Calculate predicted total using enhanced data"""
        base_total = 50.0  # Starting point
        
        # Points per game from analytics
        if analytics_data:
            home_ppg = analytics_data.get(home_team, {}).get('points_per_game', 25.0)
            away_ppg = analytics_data.get(away_team, {}).get('points_per_game', 25.0)
            if home_ppg > 0 and away_ppg > 0:
                base_total = (home_ppg + away_ppg) * 0.85  # Slight regression
        
        # Drive efficiency adjustment
        if drive_data:
            home_drive = drive_data.get(home_team, {})
            away_drive = drive_data.get(away_team, {})
            
            avg_scoring_rate = (home_drive.get('scoring_rate', 20.0) + 
                              away_drive.get('scoring_rate', 20.0)) / 2
            
            # Higher scoring rates = higher totals
            base_total += (avg_scoring_rate - 20.0) * 0.3
        
        return max(self.min_total_points, min(self.max_total_points, base_total))
    
    def _parse_record(self, record_str: str) -> Dict:
        """Parse win-loss record string into wins, losses, win percentage"""
        try:
            if '-' in record_str:
                wins, losses = map(int, record_str.split('-'))
                games = wins + losses
                win_pct = wins / games if games > 0 else 0.0
                return {'wins': wins, 'losses': losses, 'games': games, 'win_pct': win_pct}
        except:
            pass
        return {'wins': 0, 'losses': 0, 'games': 0, 'win_pct': 0.0}
        
    def ensure_prediction_consistency(self, spread: float, win_probability: float, 
                                    total: float, home_team: str, away_team: str) -> Dict:
        """Ensure win probability, spread, and final score are all consistent"""
        
        # Convert win probability to implied spread
        if win_probability > 0.01 and win_probability < 0.99:
            prob_implied_spread = math.log(win_probability / (1 - win_probability)) * 11.0
        else:
            prob_implied_spread = spread  # Use provided spread for extreme probabilities
            
        # Check for consistency
        spread_discrepancy = abs(spread - prob_implied_spread)
        
        # Use the spread that's most consistent with win probability
        consistent_spread = prob_implied_spread if spread_discrepancy > 2.0 else spread
        
        # Calculate final scores
        home_score = (total + consistent_spread) / 2
        away_score = (total - consistent_spread) / 2
        
        # Ensure the team with higher win probability actually wins the game
        if win_probability > 0.5 and home_score <= away_score:
            # Home team should win but doesn't - fix it
            margin = max(1.0, abs(consistent_spread))
            home_score = (total + margin) / 2
            away_score = (total - margin) / 2
            consistent_spread = margin
        elif win_probability < 0.5 and away_score <= home_score:
            # Away team should win but doesn't - fix it  
            margin = max(1.0, abs(consistent_spread))
            home_score = (total - margin) / 2
            away_score = (total + margin) / 2
            consistent_spread = -margin
            
        # Handle negative scores
        if home_score < 0:
            home_score = 0
            away_score = total
        elif away_score < 0:
            away_score = 0
            home_score = total
            
        return {
            'consistent_spread': round(consistent_spread, 1),
            'home_score': round(home_score, 0),
            'away_score': round(away_score, 0),
            'spread_discrepancy': spread_discrepancy,
            'was_adjusted': spread_discrepancy > 2.0 or 
                           (win_probability > 0.5 and spread <= 0) or
                           (win_probability < 0.5 and spread >= 0)
        }
    
    def calculate_total(
        self,
        home_metrics: TeamMetrics,
        away_metrics: TeamMetrics
    ) -> float:
        """
        Calculate predicted total points
        
        Args:
            home_metrics: Home team performance metrics
            away_metrics: Away team performance metrics
            
        Returns:
            Predicted total points
        """
        # Base total for college football
        base_total = 50.0
        
        # Offensive contributions
        home_offensive_rating = (
            home_metrics.epa + 
            home_metrics.explosiveness + 
            home_metrics.success_rate
        ) / 3
        away_offensive_rating = (
            away_metrics.epa + 
            away_metrics.explosiveness + 
            away_metrics.success_rate
        ) / 3
        
        # Defensive contributions (lower is better)
        home_defensive_rating = home_metrics.epa_allowed
        away_defensive_rating = away_metrics.epa_allowed
        
        # Calculate expected points for each team
        home_expected_points = (
            base_total / 2 + 
            (home_offensive_rating * 15) - 
            (away_defensive_rating * 10) + 
            2.5  # home field advantage
        )
        away_expected_points = (
            base_total / 2 + 
            (away_offensive_rating * 15) - 
            (home_defensive_rating * 10)
        )
        
        # Ensure minimum realistic scores
        home_expected_points = max(home_expected_points, 10)
        away_expected_points = max(away_expected_points, 10)
        
        total = home_expected_points + away_expected_points
        
        # Bound total within realistic range
        return max(min(total, self.max_total_points), self.min_total_points)
    
    def calculate_win_probability(
        self,
        predicted_spread: float,
        confidence: float
    ) -> float:
        """
        Calculate win probability from spread
        
        Args:
            predicted_spread: Predicted point spread
            confidence: Prediction confidence (0-1)
            
        Returns:
            Home team win probability (0-1)
        """
        # Use logistic function to convert spread to probability
        # Standard deviation for college football ~ 13 points
        import math
        std_dev = 13.0
        
        # Logistic function: P = 1 / (1 + e^(-spread/std_dev))
        try:
            probability = 1 / (1 + math.exp(-predicted_spread / std_dev))
        except OverflowError:
            probability = 1.0 if predicted_spread > 0 else 0.0
        
        # Adjust by confidence (reduce certainty for low confidence)
        # When confidence is low, pull probability toward 50%
        adjusted_probability = 0.5 + (probability - 0.5) * confidence
        
        return round(adjusted_probability, 3)
    
    def calculate_confidence(
        self,
        data_completeness: Dict,
        home_metrics: TeamMetrics,
        away_metrics: TeamMetrics,
        spread_magnitude: float
    ) -> float:
        """
        Calculate prediction confidence based on data quality and consistency
        
        Args:
            data_completeness: Dictionary indicating which data sources are available
            home_metrics: Home team metrics
            away_metrics: Away team metrics
            spread_magnitude: Absolute value of predicted spread
            
        Returns:
            Confidence score (0-1)
        """
        # Base confidence from data availability
        base_confidence = 0.4
        
        if data_completeness.get('has_metrics'):
            base_confidence += 0.15
        if data_completeness.get('has_recent_games'):
            base_confidence += 0.1
        if data_completeness.get('has_historical'):
            base_confidence += 0.1
        if data_completeness.get('has_season_games'):
            base_confidence += 0.1
        if data_completeness.get('has_ratings'):
            base_confidence += 0.08
        if data_completeness.get('has_weather'):
            base_confidence += 0.03
        
        # Boost for team consistency
        consistency_boost = (
            home_metrics.consistency_score + 
            away_metrics.consistency_score
        ) / 2 * 0.1
        
        # Boost for larger spreads (more confident in blowouts)
        differential_boost = min(abs(spread_magnitude) / 20, 0.15)
        
        # Reduce confidence if trends are conflicting
        trend_consistency = 1 - abs(
            home_metrics.season_trend - away_metrics.season_trend
        ) / 2
        trend_factor = trend_consistency * 0.05
        
        total_confidence = (
            base_confidence + 
            consistency_boost + 
            differential_boost + 
            trend_factor
        )
        
        return min(total_confidence, 1.0)
