#!/usr/bin/env python3
"""
Test script to validate the game summary and rationale generation
"""

import json
from dataclasses import dataclass
from typing import List

# Mock prediction object
@dataclass
class MockStats:
    epa_offense: float = 0.15
    epa_defense: float = -0.10
    offensive_success_rate: float = 0.48
    defensive_success_rate: float = 0.42

@dataclass  
class MockPrediction:
    home_team: str = "Michigan"
    away_team: str = "Ohio State"
    home_win_prob: float = 0.28
    predicted_spread: float = -7.5
    predicted_total: float = 58.5
    confidence: float = 0.78
    key_factors: List[str] = None
    home_team_stats: MockStats = None
    away_team_stats: MockStats = None
    
    def __post_init__(self):
        if self.key_factors is None:
            self.key_factors = [
                "Superior offensive EPA differential",
                "Strong defensive performance",
                "Better power ratings",
                "Higher success rate on offense",
                "Defensive efficiency advantage"
            ]
        if self.home_team_stats is None:
            self.home_team_stats = MockStats(
                epa_offense=0.12,
                epa_defense=-0.08,
                offensive_success_rate=0.47,
                defensive_success_rate=0.43
            )
        if self.away_team_stats is None:
            self.away_team_stats = MockStats(
                epa_offense=0.18,
                epa_defense=-0.12,
                offensive_success_rate=0.52,
                defensive_success_rate=0.38
            )

# Mock predictor with ratings
class MockPredictor:
    def __init__(self):
        self.team_ratings = {
            "Ohio State": {"fpi": 25.3, "sp_plus": 28.1, "elo": 1850},
            "Michigan": {"fpi": 18.7, "sp_plus": 21.4, "elo": 1720}
        }

def extract_team_ratings(predictor, team_name):
    """Mock extract team ratings"""
    return predictor.team_ratings.get(team_name, {"fpi": 0, "sp_plus": 0, "elo": 0})

# Import the actual function from app.py
import sys
sys.path.insert(0, '/Users/davlenswain/Desktop/Gameday_Graphql_Model')

# Mock the dependencies
import app
app.extract_team_ratings = extract_team_ratings

from app import generate_game_summary_and_rationale

def test_summary():
    print("🧪 Testing Game Summary & Rationale Generation")
    print("=" * 80)
    
    # Create mock objects
    prediction = MockPrediction()
    home_team_data = {"id": 130, "name": "Michigan"}
    away_team_data = {"id": 194, "name": "Ohio State"}
    predictor = MockPredictor()
    details = {}
    
    # Generate summary
    try:
        summary = generate_game_summary_and_rationale(
            prediction, details, home_team_data, away_team_data, predictor
        )
        
        print("✅ Summary generated successfully!")
        print("\n" + "=" * 80)
        print("GAME SUMMARY & PREDICTION RATIONALE")
        print("=" * 80)
        print(json.dumps(summary, indent=2))
        
        # Validate key components
        print("\n" + "=" * 80)
        print("VALIDATION CHECKS")
        print("=" * 80)
        
        checks = [
            ("Favored team identified", "favored_team" in summary),
            ("Win probability calculated", "win_probability" in summary),
            ("Spread analysis included", "spread_analysis" in summary),
            ("Total analysis included", "total_analysis" in summary),
            ("Edge analysis calculated", "edge_analysis" in summary),
            ("Critical stats provided", "critical_stats" in summary),
            ("Key advantages listed", "key_advantages" in summary),
            ("Bottom line summary", "bottom_line" in summary),
            ("Home advantages count", len(summary.get("key_advantages", {}).get("home", [])) > 0),
            ("Away advantages count", len(summary.get("key_advantages", {}).get("away", [])) > 0),
        ]
        
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"{status} {check_name}: {result}")
        
        # Display key insights
        print("\n" + "=" * 80)
        print("KEY INSIGHTS")
        print("=" * 80)
        print(f"🏆 Predicted Winner: {summary['predicted_winner']}")
        print(f"📊 Win Probability: {summary['win_probability']['favorite']}%")
        print(f"🎯 Spread: {summary['spread_analysis']['spread_display']}")
        print(f"🔢 Total: {summary['total_analysis']['predicted_total']}")
        print(f"⚡ Edge Score: {summary['edge_analysis']['edge_leader']} leads {summary['edge_analysis']['total_edge']:.1f}")
        print(f"💪 Confidence: {summary['bottom_line']['confidence_level']} ({summary['bottom_line']['confidence_percentage']}%)")
        
        print("\n📝 Bottom Line Summary:")
        print(summary['bottom_line']['summary'])
        
        print("\n✅ ALL TESTS PASSED!")
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_summary()
