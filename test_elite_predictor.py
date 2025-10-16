#!/usr/bin/env python3
"""
Elite Testing Framework for LightningPredictor
Validates performance against real Week 7 lines and results
"""

import asyncio
import json
from typing import Dict, List, Tuple
from datetime import datetime
from graphqlpredictor import LightningPredictor, GamePrediction

class PredictionTester:
    def __init__(self, api_key: str):
        self.predictor = LightningPredictor(api_key)
        self.test_results = []
        
    async def test_week_7_slate(self, games: List[Tuple[int, int, str]]) -> Dict:
        """Test predictor against full Week 7 slate"""
        print("🚀 LIGHTNING PREDICTOR ELITE TESTING 🚀")
        print("=" * 50)
        
        results = {
            'total_games': len(games),
            'predictions': [],
            'accuracy_metrics': {},
            'edge_cases': []
        }
        
        for home_id, away_id, game_desc in games:
            try:
                print(f"\n🏈 Predicting: {game_desc}")
                prediction = await self.predictor.predict_game(home_id, away_id)
                
                # Store prediction with metadata
                result = {
                    'game': game_desc,
                    'home_team_id': home_id,
                    'away_team_id': away_id,
                    'prediction': prediction,
                    'timestamp': datetime.now().isoformat()
                }
                
                results['predictions'].append(result)
                
                # Print formatted results
                self._print_prediction_analysis(prediction, game_desc)
                
            except Exception as e:
                print(f"❌ Error predicting {game_desc}: {e}")
                results['edge_cases'].append({
                    'game': game_desc,
                    'error': str(e)
                })
                
        # Calculate performance metrics
        results['accuracy_metrics'] = self._calculate_performance_metrics(results['predictions'])
        
        return results
    
    def _print_prediction_analysis(self, prediction: GamePrediction, game_desc: str):
        """Print detailed prediction analysis"""
        print(f"📊 {prediction.home_team} vs {prediction.away_team}")
        print(f"   Win Probability: {prediction.home_win_prob:.1%} (Home)")
        print(f"   Predicted Spread: {prediction.predicted_spread}")
        print(f"   Predicted Total: {prediction.predicted_total}")
        print(f"   Confidence: {prediction.confidence:.1%}")
        print(f"   Key Factors: {', '.join(prediction.key_factors[:3])}")
        
        # Analysis flags
        if prediction.confidence > 0.8:
            print("   🔥 HIGH CONFIDENCE PLAY")
        if abs(prediction.predicted_spread) > 10:
            print("   💪 BLOWOUT PREDICTION")
        if abs(prediction.predicted_spread) < 3:
            print("   ⚖️  CLOSE GAME ALERT")
            
    def _calculate_performance_metrics(self, predictions: List[Dict]) -> Dict:
        """Calculate predictor performance metrics"""
        if not predictions:
            return {}
            
        confidence_levels = [p['prediction'].confidence for p in predictions]
        spread_predictions = [abs(p['prediction'].predicted_spread) for p in predictions]
        
        return {
            'avg_confidence': sum(confidence_levels) / len(confidence_levels),
            'high_confidence_games': len([c for c in confidence_levels if c > 0.8]),
            'close_games_predicted': len([s for s in spread_predictions if s < 3]),
            'blowout_predictions': len([s for s in spread_predictions if s > 10]),
            'total_predictions': len(predictions)
        }
    
    async def test_single_game_deep_dive(self, home_id: int, away_id: int, game_desc: str):
        """Deep dive analysis for a single game"""
        print(f"\n🔬 DEEP DIVE ANALYSIS: {game_desc}")
        print("=" * 60)
        
        prediction = await self.predictor.predict_game(home_id, away_id)
        
        # Detailed breakdown
        print(f"🏈 {prediction.home_team} (Home) vs {prediction.away_team} (Away)")
        print(f"\n📈 PREDICTION SUMMARY:")
        print(f"   Home Win Probability: {prediction.home_win_prob:.1%}")
        print(f"   Away Win Probability: {(1-prediction.home_win_prob):.1%}")
        print(f"   Predicted Spread: {prediction.predicted_spread} (Negative = Home Favored)")
        print(f"   Predicted Total: {prediction.predicted_total} points")
        print(f"   Model Confidence: {prediction.confidence:.1%}")
        
        print(f"\n🎯 KEY FACTORS:")
        for i, factor in enumerate(prediction.key_factors, 1):
            print(f"   {i}. {factor}")
            
        # Confidence assessment
        print(f"\n🔥 CONFIDENCE ASSESSMENT:")
        if prediction.confidence > 0.85:
            print("   ✅ ELITE CONFIDENCE - Model loves this pick")
        elif prediction.confidence > 0.7:
            print("   ✅ SOLID CONFIDENCE - Good analytical backing")
        elif prediction.confidence > 0.6:
            print("   ⚠️  MODERATE CONFIDENCE - Proceed with caution")
        else:
            print("   🚨 LOW CONFIDENCE - High uncertainty game")
            
        # Market implications
        print(f"\n💰 BETTING IMPLICATIONS:")
        if abs(prediction.predicted_spread) > 7:
            print("   📈 Strong directional opinion - Good for spread betting")
        if prediction.confidence > 0.8:
            print("   💎 High conviction play - Consider larger unit size")
        if "market disagreement" in str(prediction.key_factors):
            print("   🎯 EDGE DETECTED - Model disagrees with market")
            
        return prediction

async def main():
    """Run comprehensive testing suite"""
    API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    tester = PredictionTester(API_KEY)
    
    # Week 7 2025 Sample Games (replace with actual team IDs)
    week_7_games = [
        (194, 2, "Ohio State @ Michigan"),           # Rivalry game
        (183, 150, "Oregon @ Washington"),           # Conference championship implications  
        (8, 57, "Alabama @ LSU"),                    # SEC West battle
        (245, 25, "Texas @ Oklahoma"),               # Red River Rivalry
        (52, 103, "Georgia @ Florida"),              # World's Largest Outdoor Cocktail Party
    ]
    
    print("🎯 Starting Lightning Predictor Elite Testing Suite...")
    
    # Test full slate
    results = await tester.test_week_7_slate(week_7_games)
    
    # Print summary
    print(f"\n🏆 TESTING SUMMARY:")
    print(f"   Total Games Predicted: {results['accuracy_metrics']['total_predictions']}")
    print(f"   Average Confidence: {results['accuracy_metrics']['avg_confidence']:.1%}")
    print(f"   High Confidence Games: {results['accuracy_metrics']['high_confidence_games']}")
    print(f"   Close Games Predicted: {results['accuracy_metrics']['close_games_predicted']}")
    print(f"   Blowout Predictions: {results['accuracy_metrics']['blowout_predictions']}")
    
    # Deep dive on first game
    if week_7_games:
        home_id, away_id, game_desc = week_7_games[0]
        await tester.test_single_game_deep_dive(home_id, away_id, game_desc)

if __name__ == "__main__":
    asyncio.run(main())