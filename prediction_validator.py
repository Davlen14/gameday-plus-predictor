"""
Prediction Validation Module
Ensures mathematical consistency across all prediction components
"""

import math
from typing import Dict, Any, List, Tuple
import warnings

class PredictionConsistencyError(Exception):
    """Raised when prediction components are mathematically inconsistent"""
    pass

class PredictionValidator:
    """Validates that prediction components are mathematically consistent"""
    
    # Tolerance for floating-point comparisons
    TOLERANCE = 0.1
    
    @staticmethod
    def validate_spread_score_consistency(predicted_spread: float, predicted_total: float, 
                                        home_score: int, away_score: int) -> bool:
        """
        Validates that predicted scores align with spread and total
        
        Args:
            predicted_spread: Home team spread (positive = home favored)
            predicted_total: Combined points total
            home_score: Predicted home team score
            away_score: Predicted away team score
            
        Returns:
            True if consistent, raises PredictionConsistencyError if not
        """
        # Check total consistency
        actual_total = home_score + away_score
        if abs(actual_total - predicted_total) > PredictionValidator.TOLERANCE:
            raise PredictionConsistencyError(
                f"Score total mismatch: {home_score} + {away_score} = {actual_total}, "
                f"but predicted total is {predicted_total:.1f}"
            )
        
        # Check spread consistency
        actual_spread = home_score - away_score
        if abs(actual_spread - predicted_spread) > PredictionValidator.TOLERANCE:
            raise PredictionConsistencyError(
                f"Spread mismatch: {home_score} - {away_score} = {actual_spread}, "
                f"but predicted spread is {predicted_spread:.1f}"
            )
        
        return True
    
    @staticmethod
    def validate_probability_spread_alignment(win_probability: float, predicted_spread: float,
                                            conversion_factor: float = 2.4) -> bool:
        """
        Validates that win probability aligns with predicted spread using logistic conversion
        
        Args:
            win_probability: Home team win probability (0-1)
            predicted_spread: Home team spread (positive = home favored)
            conversion_factor: Logistic conversion factor (default 2.4 for CFB)
            
        Returns:
            True if consistent, raises PredictionConsistencyError if not
        """
        # Convert probability to implied spread
        if 0.01 <= win_probability <= 0.99:
            implied_spread = math.log(win_probability / (1 - win_probability)) * conversion_factor
        else:
            # Use larger factor for extreme probabilities
            implied_spread = math.log(win_probability / (1 - win_probability)) * 3.5
        
        # Allow for some tolerance in spread calculations
        spread_tolerance = 2.0  # 2-point tolerance for spread alignment
        if abs(implied_spread - predicted_spread) > spread_tolerance:
            raise PredictionConsistencyError(
                f"Win probability {win_probability:.1%} implies spread of {implied_spread:.1f}, "
                f"but predicted spread is {predicted_spread:.1f}"
            )
        
        return True
    
    @staticmethod
    def validate_market_alignment(model_spread: float, market_spread: float,
                                model_total: float, market_total: float) -> Dict[str, Any]:
        """
        Validates model predictions against market and calculates edges
        
        Returns:
            Dictionary with edge analysis and value recommendations
        """
        spread_edge = market_spread - model_spread if market_spread else 0
        total_edge = model_total - market_total if market_total else 0
        
        # Determine value picks based on edges
        value_picks = {
            'spread_pick': None,
            'total_pick': None,
            'spread_edge': spread_edge,
            'total_edge': total_edge
        }
        
        # Spread value analysis (need >2.5 point edge for value)
        if abs(spread_edge) >= 2.5:
            if spread_edge > 0:
                value_picks['spread_pick'] = f"Away team +{market_spread:.1f} (Model edge: +{spread_edge:.1f})"
            else:
                value_picks['spread_pick'] = f"Home team {market_spread:.1f} (Model edge: {spread_edge:.1f})"
        
        # Total value analysis (need >3.5 point edge for value)
        if abs(total_edge) >= 3.5:
            if total_edge > 0:
                value_picks['total_pick'] = f"OVER {market_total:.1f} (Model edge: +{total_edge:.1f})"
            else:
                value_picks['total_pick'] = f"UNDER {market_total:.1f} (Model edge: {total_edge:.1f})"
        
        return value_picks
    
    @staticmethod
    def validate_full_prediction(prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation of entire prediction structure
        
        Args:
            prediction_data: Complete prediction dictionary
            
        Returns:
            Validation results with any warnings or errors
        """
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'consistency_checks': {}
        }
        
        try:
            # Extract key values
            predicted_spread = prediction_data.get('predicted_spread', 0)
            predicted_total = prediction_data.get('predicted_total', 0)
            home_win_prob = prediction_data.get('home_win_prob', 0.5)
            
            # Get predicted scores from final_prediction
            final_pred = prediction_data.get('ui_components', {}).get('final_prediction', {})
            predicted_score = final_pred.get('predicted_score', {})
            home_score = predicted_score.get('home_score', 0)
            away_score = predicted_score.get('away_score', 0)
            
            # 1. Validate spread-score consistency
            try:
                PredictionValidator.validate_spread_score_consistency(
                    predicted_spread, predicted_total, home_score, away_score
                )
                validation_results['consistency_checks']['spread_score'] = 'PASS'
            except PredictionConsistencyError as e:
                validation_results['errors'].append(str(e))
                validation_results['is_valid'] = False
                validation_results['consistency_checks']['spread_score'] = 'FAIL'
            
            # 2. Validate probability-spread alignment
            try:
                PredictionValidator.validate_probability_spread_alignment(
                    home_win_prob, predicted_spread
                )
                validation_results['consistency_checks']['probability_spread'] = 'PASS'
            except PredictionConsistencyError as e:
                validation_results['warnings'].append(str(e))
                validation_results['consistency_checks']['probability_spread'] = 'WARNING'
            
            # 3. Check for extreme values
            if abs(predicted_spread) > 35:
                validation_results['warnings'].append(f"Extreme spread: {predicted_spread:.1f}")
            
            if predicted_total < 20 or predicted_total > 100:
                validation_results['warnings'].append(f"Unusual total: {predicted_total:.1f}")
            
            if home_win_prob < 0.05 or home_win_prob > 0.95:
                validation_results['warnings'].append(f"Extreme win probability: {home_win_prob:.1%}")
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['is_valid'] = False
        
        return validation_results

def apply_prediction_fixes(prediction):
    """
    Apply fixes to ensure prediction consistency across all teams
    
    Args:
        prediction: GamePrediction object
        
    Returns:
        Fixed prediction object
    """
    # Recalculate implied scores using correct formula
    if hasattr(prediction, 'predicted_spread') and hasattr(prediction, 'predicted_total'):
        home_implied_score = (prediction.predicted_total + prediction.predicted_spread) / 2
        away_implied_score = (prediction.predicted_total - prediction.predicted_spread) / 2
        
        # Ensure no negative scores
        if home_implied_score < 0:
            away_implied_score += abs(home_implied_score)
            home_implied_score = 0
        elif away_implied_score < 0:
            home_implied_score += abs(away_implied_score)
            away_implied_score = 0
        
        # Store the corrected implied scores
        if hasattr(prediction, 'detailed_analysis'):
            if 'implied_scores' not in prediction.detailed_analysis:
                prediction.detailed_analysis['implied_scores'] = {}
            
            prediction.detailed_analysis['implied_scores']['home'] = round(home_implied_score)
            prediction.detailed_analysis['implied_scores']['away'] = round(away_implied_score)
    
    return prediction