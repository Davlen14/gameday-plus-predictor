#!/usr/bin/env python3
"""
Test script for dynamic confidence calculations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass
from typing import Dict, Optional

# Mock prediction object for testing
@dataclass
class MockPrediction:
    predicted_spread: float
    predicted_total: float
    confidence: float
    market_spread: Optional[float] = None
    market_total: Optional[float] = None

def calculate_base_data_quality(prediction, details):
    """
    Calculate base data quality score (70-95 range) based on available data completeness
    Factors: market lines availability, player data completeness, recent game data
    """
    score = 70  # Base score
    
    # Market data availability (+8 points max)
    market_spread = getattr(prediction, 'market_spread', None)
    market_total = getattr(prediction, 'market_total', None)
    market_lines = details.get('market_lines', [])
    
    if market_spread and market_total:
        score += 4  # Both spread and total available
    elif market_spread or market_total:
        score += 2  # One market line available
        
    if len(market_lines) >= 3:
        score += 4  # Multiple sportsbooks
    elif len(market_lines) >= 1:
        score += 2  # At least one sportsbook
    
    # Player data completeness (+7 points max)
    player_analysis = details.get('enhanced_player_analysis', {})
    home_players = player_analysis.get('home', {})
    away_players = player_analysis.get('away', {})
    
    home_qb_count = len(home_players.get('quarterbacks', []))
    away_qb_count = len(away_players.get('quarterbacks', []))
    home_wr_count = len(home_players.get('receivers', []))
    away_wr_count = len(away_players.get('receivers', []))
    
    if home_qb_count > 0 and away_qb_count > 0:
        score += 3  # QB data for both teams
    if home_wr_count >= 3 and away_wr_count >= 3:
        score += 4  # Good receiver data coverage
    
    # Advanced metrics completeness (+10 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    # Check for key EPA metrics
    if home_metrics.get('epa') and away_metrics.get('epa'):
        score += 3
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        score += 2
    if home_metrics.get('explosiveness') and away_metrics.get('explosiveness'):
        score += 2
    
    # Weather data availability (+3 points max)
    weather = details.get('weather', {})
    if weather.get('temperature') is not None:
        score += 1
    if weather.get('wind_speed') is not None:
        score += 1
    if weather.get('precipitation') is not None:
        score += 1
    
    return min(95, max(70, score))

def calculate_consistency_factor(prediction, details):
    """
    Calculate consistency factor (-5 to +10 range) based on prediction model consistency
    Factors: model stability, data variance, historical accuracy patterns
    """
    factor = 0  # Base factor
    
    # Market consensus alignment (+5 points max)
    model_spread = prediction.predicted_spread
    market_spread = getattr(prediction, 'market_spread', None)
    
    if market_spread is not None:
        spread_diff = abs(model_spread - market_spread)
        if spread_diff <= 1.5:
            factor += 5  # Very close to market consensus
        elif spread_diff <= 3.0:
            factor += 3  # Reasonable alignment
        elif spread_diff <= 5.0:
            factor += 1  # Some alignment
        else:
            factor -= 2  # Significant divergence from market
    
    # EPA differential consistency (+3 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_diff = home_metrics['epa'] - away_metrics['epa']
        # Check if EPA differential supports the spread prediction
        if (model_spread > 0 and epa_diff > 0) or (model_spread < 0 and epa_diff < 0):
            factor += 3  # EPA supports prediction direction
        elif abs(epa_diff) < 0.1:  # Very close EPA values
            factor += 1
    
    # Talent rating consistency (+2 points max)
    ratings = details.get('ratings', {})
    home_talent = ratings.get('home', {}).get('talent', 0)
    away_talent = ratings.get('away', {}).get('talent', 0)
    
    if home_talent and away_talent:
        talent_diff = home_talent - away_talent
        spread_direction = 1 if model_spread > 0 else -1
        talent_direction = 1 if talent_diff > 0 else -1
        
        if spread_direction == talent_direction:
            factor += 2  # Talent ratings support prediction
    
    return max(-5, min(10, factor))

def calculate_differential_strength(prediction, details):
    """
    Calculate differential strength (0 to +15 range) based on statistical differentials
    Factors: EPA differentials, talent gaps, market consensus alignment
    """
    strength = 0  # Base strength
    
    # EPA differential strength (+6 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_diff = abs(home_metrics['epa'] - away_metrics['epa'])
        if epa_diff >= 0.4:
            strength += 6  # Very strong EPA differential
        elif epa_diff >= 0.2:
            strength += 4  # Strong EPA differential
        elif epa_diff >= 0.1:
            strength += 2  # Moderate EPA differential
    
    # Talent gap strength (+4 points max)
    ratings = details.get('ratings', {})
    home_talent = ratings.get('home', {}).get('talent', 0)
    away_talent = ratings.get('away', {}).get('talent', 0)
    
    if home_talent and away_talent:
        talent_gap = abs(home_talent - away_talent)
        if talent_gap >= 15:
            strength += 4  # Large talent gap
        elif talent_gap >= 8:
            strength += 3  # Significant talent gap
        elif talent_gap >= 4:
            strength += 1  # Moderate talent gap
    
    # Success rate differential (+3 points max)
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        success_diff = abs(home_metrics['success_rate'] - away_metrics['success_rate'])
        if success_diff >= 8:
            strength += 3  # Large success rate gap
        elif success_diff >= 4:
            strength += 2  # Significant success rate gap
        elif success_diff >= 2:
            strength += 1  # Moderate success rate gap
    
    # Multiple indicators agreement (+2 points max)
    agreement_count = 0
    model_spread = prediction.predicted_spread
    
    # Check if EPA, talent, and success rate all point in same direction
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_favors_home = home_metrics['epa'] > away_metrics['epa']
        if (model_spread > 0) == epa_favors_home:
            agreement_count += 1
    
    if home_talent and away_talent:
        talent_favors_home = home_talent > away_talent
        if (model_spread > 0) == talent_favors_home:
            agreement_count += 1
    
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        success_favors_home = home_metrics['success_rate'] > away_metrics['success_rate']
        if (model_spread > 0) == success_favors_home:
            agreement_count += 1
    
    if agreement_count >= 3:
        strength += 2  # All indicators agree
    elif agreement_count >= 2:
        strength += 1  # Most indicators agree
    
    return min(15, max(0, strength))

def test_dynamic_confidence():
    """Test the dynamic confidence calculations with various scenarios"""
    
    print("🧪 Testing Dynamic Confidence Calculations")
    print("=" * 50)
    
    # Test Scenario 1: Minimal data
    print("\n📊 Test 1: Minimal Data Scenario")
    prediction1 = MockPrediction(predicted_spread=-3.5, predicted_total=47.5, confidence=0.72)
    details1 = {}
    
    base_quality1 = calculate_base_data_quality(prediction1, details1)
    consistency1 = calculate_consistency_factor(prediction1, details1)
    differential1 = calculate_differential_strength(prediction1, details1)
    
    print(f"Base Data Quality: {base_quality1} (should be ~70)")
    print(f"Consistency Factor: {consistency1} (should be ~0)")
    print(f"Differential Strength: {differential1} (should be ~0)")
    
    # Test Scenario 2: Rich data with market alignment
    print("\n📊 Test 2: Rich Data with Market Alignment")
    prediction2 = MockPrediction(
        predicted_spread=-6.5, 
        predicted_total=52.0, 
        confidence=0.85,
        market_spread=-7.0,
        market_total=51.5
    )
    details2 = {
        'market_lines': [
            {'sportsbook': 'DraftKings', 'spread': -7.0, 'total': 51.5},
            {'sportsbook': 'FanDuel', 'spread': -6.5, 'total': 52.0},
            {'sportsbook': 'BetMGM', 'spread': -7.5, 'total': 51.0}
        ],
        'enhanced_player_analysis': {
            'home': {
                'quarterbacks': [{'name': 'QB1', 'rating': 85}],
                'receivers': [
                    {'name': 'WR1', 'rating': 90},
                    {'name': 'WR2', 'rating': 82},
                    {'name': 'WR3', 'rating': 78},
                    {'name': 'WR4', 'rating': 75}
                ]
            },
            'away': {
                'quarterbacks': [{'name': 'QB2', 'rating': 78}],
                'receivers': [
                    {'name': 'WR1', 'rating': 85},
                    {'name': 'WR2', 'rating': 80},
                    {'name': 'WR3', 'rating': 76}
                ]
            }
        },
        'team_metrics': {
            'home': {
                'epa': 0.35,
                'success_rate': 45.2,
                'explosiveness': 0.28
            },
            'away': {
                'epa': 0.15,
                'success_rate': 38.7,
                'explosiveness': 0.22
            }
        },
        'ratings': {
            'home': {'talent': 85.4},
            'away': {'talent': 72.1}
        },
        'weather': {
            'temperature': 72,
            'wind_speed': 8,
            'precipitation': 0
        }
    }
    
    base_quality2 = calculate_base_data_quality(prediction2, details2)
    consistency2 = calculate_consistency_factor(prediction2, details2)
    differential2 = calculate_differential_strength(prediction2, details2)
    
    print(f"Base Data Quality: {base_quality2} (should be ~90+)")
    print(f"Consistency Factor: {consistency2} (should be ~8+)")
    print(f"Differential Strength: {differential2} (should be ~12+)")
    
    # Test Scenario 3: Conflicting indicators
    print("\n📊 Test 3: Conflicting Indicators Scenario")
    prediction3 = MockPrediction(
        predicted_spread=10.5, 
        predicted_total=65.0, 
        confidence=0.60,
        market_spread=3.5,  # Large market disagreement
        market_total=64.0
    )
    details3 = {
        'market_lines': [
            {'sportsbook': 'DraftKings', 'spread': 3.5, 'total': 64.0}
        ],
        'team_metrics': {
            'home': {
                'epa': 0.10,  # Weak EPA for large spread
                'success_rate': 42.0,
                'explosiveness': 0.18
            },
            'away': {
                'epa': 0.08,  # Very close EPA values
                'success_rate': 40.5,
                'explosiveness': 0.16
            }
        },
        'ratings': {
            'home': {'talent': 78.0},
            'away': {'talent': 76.5}  # Close talent ratings
        }
    }
    
    base_quality3 = calculate_base_data_quality(prediction3, details3)
    consistency3 = calculate_consistency_factor(prediction3, details3)
    differential3 = calculate_differential_strength(prediction3, details3)
    
    print(f"Base Data Quality: {base_quality3} (should be ~75-80)")
    print(f"Consistency Factor: {consistency3} (should be negative due to market disagreement)")
    print(f"Differential Strength: {differential3} (should be low due to weak differentials)")
    
    # Summary
    print("\n✅ Dynamic Confidence Testing Complete")
    print("=" * 50)
    print("OLD SYSTEM: Always 88, +3, +8 (static)")
    print("NEW SYSTEM: Dynamic based on actual data quality")
    print(f"Test 1: {base_quality1}, {consistency1:+d}, {differential1}")
    print(f"Test 2: {base_quality2}, {consistency2:+d}, {differential2}")
    print(f"Test 3: {base_quality3}, {consistency3:+d}, {differential3}")

if __name__ == "__main__":
    test_dynamic_confidence()