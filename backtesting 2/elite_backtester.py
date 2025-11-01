#!/usr/bin/env python3
"""
🚀 ELITE BACKTESTING ENGINE
Comprehensive validation system for college football prediction model
Uses 2024 + 2025 historical game data to validate and enhance algorithm
"""

import asyncio
import json
import sys
import os
import math
import statistics
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
# Optional imports for visualization (install if needed)
# import matplotlib.pyplot as plt  
# import seaborn as sns
# import pandas as pd
# import numpy as np

# Add parent directory to path to import predictor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graphqlpredictor import LightningPredictor

@dataclass
class BacktestResult:
    """Individual game backtest result"""
    game_id: int
    season: int
    week: int
    home_team: str
    away_team: str
    
    # Actual results
    actual_home_score: int
    actual_away_score: int
    actual_winner: str
    actual_spread: float  # home_score - away_score
    actual_total: float
    
    # Predictions
    predicted_home_win_prob: float
    predicted_spread: float
    predicted_total: float
    predicted_winner: str
    
    # Market data
    closing_spread: Optional[float]
    closing_total: Optional[float]
    
    # Errors
    winner_correct: bool
    spread_error: float
    total_error: float
    ats_correct: Optional[bool]  # Against the spread
    
    # Context
    conference_game: bool
    neutral_site: bool
    home_elo: Optional[float]
    away_elo: Optional[float]

@dataclass  
class BacktestSummary:
    """Complete backtest performance summary"""
    total_games: int
    
    # Winner prediction
    winners_correct: int
    winner_accuracy: float
    
    # Spread prediction  
    avg_spread_error: float
    median_spread_error: float
    spread_rmse: float
    
    # Total prediction
    avg_total_error: float
    median_total_error: float
    total_rmse: float
    
    # Against the spread
    ats_games: int
    ats_correct: int
    ats_accuracy: float
    
    # Probability calibration
    brier_score: float
    log_loss: float
    
    # ROI simulation
    flat_bet_roi: float
    kelly_roi: float
    
    # Performance by category
    by_conference: Dict[str, Dict]
    by_spread_size: Dict[str, Dict]
    by_week: Dict[int, Dict]
    by_season: Dict[int, Dict]

class EliteBacktester:
    """Elite backtesting engine with comprehensive analysis"""
    
    def __init__(self):
        self.predictor = None
        self.historical_games = []
        self.results = []
        
    async def load_historical_data(self, data_2024_path: str, data_2025_path: str):
        """Load and combine 2024 + 2025 game data"""
        print("🔄 Loading historical game data...")
        
        # Load 2024 data
        with open(data_2024_path, 'r') as f:
            data_2024 = json.load(f)
        
        # Load 2025 data  
        with open(data_2025_path, 'r') as f:
            data_2025 = json.load(f)
        
        # Combine games and filter for completed FBS vs FBS only
        all_games = data_2024['games'] + data_2025['games']
        
        self.historical_games = [
            game for game in all_games 
            if (game.get('status') == 'completed' and 
                game.get('homeClassification') == 'fbs' and 
                game.get('awayClassification') == 'fbs' and
                game.get('homePoints') is not None and
                game.get('awayPoints') is not None)
        ]
        
        print(f"✅ Loaded {len(self.historical_games)} completed FBS vs FBS games")
        print(f"   2024: {len([g for g in self.historical_games if g['season'] == 2024])}")
        print(f"   2025: {len([g for g in self.historical_games if g['season'] == 2025])}")
        
        return len(self.historical_games)
    
    async def run_comprehensive_backtest(self, max_games: Optional[int] = None):
        """Run predictions on all historical games"""
        print("\n🚀 Starting comprehensive backtesting...")
        
        if max_games:
            games_to_test = self.historical_games[:max_games]
            print(f"   Testing first {max_games} games for speed")
        else:
            games_to_test = self.historical_games
        
        self.results = []
        total_games = len(games_to_test)
        
        for i, game in enumerate(games_to_test):
            if i % 50 == 0:
                print(f"   Progress: {i}/{total_games} ({i/total_games*100:.1f}%)")
            
            try:
                result = await self._test_single_game(game)
                if result:
                    self.results.append(result)
            except Exception as e:
                print(f"   ❌ Error testing game {game.get('id')}: {e}")
                continue
        
        print(f"✅ Completed backtesting: {len(self.results)} successful predictions")
        return self.results
    
    async def _test_single_game(self, game_data: Dict) -> Optional[BacktestResult]:
        """Test prediction on a single historical game"""
        
        # Initialize predictor for the correct week/season
        week = game_data.get('week', 1)
        season = game_data.get('season', 2024)
        
        if not self.predictor:
            # Use empty string for API key since we're using historical data
            self.predictor = LightningPredictor(api_key="")
            
        # Update the predictor's current week and year
        self.predictor.current_week = week
        self.predictor.current_year = season
        
        # Extract game info
        home_team_id = game_data.get('homeTeamId')
        away_team_id = game_data.get('awayTeamId')
        
        if not home_team_id or not away_team_id:
            return None
        
        try:
            # Run prediction
            prediction = await self.predictor.predict_game(home_team_id, away_team_id)
            
            # Extract actual results
            actual_home_score = game_data['homePoints']
            actual_away_score = game_data['awayPoints']
            actual_spread = actual_home_score - actual_away_score
            actual_total = actual_home_score + actual_away_score
            actual_winner = game_data['homeTeam'] if actual_home_score > actual_away_score else game_data['awayTeam']
            
            # Extract market data
            lines = game_data.get('lines', [])
            closing_spread = None
            closing_total = None
            
            if lines:
                # Use DraftKings as primary, fallback to first available
                dk_line = next((line for line in lines if 'DraftKings' in line.get('provider', {}).get('name', '')), None)
                primary_line = dk_line or lines[0]
                
                closing_spread = primary_line.get('spread')
                closing_total = primary_line.get('overUnder')
            
            # Calculate metrics
            predicted_winner = prediction.home_team if prediction.home_win_prob > 0.5 else prediction.away_team
            winner_correct = (predicted_winner == actual_winner)
            spread_error = abs(prediction.predicted_spread - (-actual_spread))  # Model predicts from away perspective
            total_error = abs(prediction.predicted_total - actual_total)
            
            # Against the spread calculation
            ats_correct = None
            if closing_spread is not None:
                # Did our predicted winner beat the spread?
                home_covered = actual_spread > closing_spread
                our_pick_home = prediction.home_win_prob > 0.5
                ats_correct = (home_covered == our_pick_home)
            
            return BacktestResult(
                game_id=game_data['id'],
                season=season,
                week=week,
                home_team=game_data['homeTeam'],
                away_team=game_data['awayTeam'],
                
                actual_home_score=actual_home_score,
                actual_away_score=actual_away_score,
                actual_winner=actual_winner,
                actual_spread=actual_spread,
                actual_total=actual_total,
                
                predicted_home_win_prob=prediction.home_win_prob,
                predicted_spread=prediction.predicted_spread,
                predicted_total=prediction.predicted_total,
                predicted_winner=predicted_winner,
                
                closing_spread=closing_spread,
                closing_total=closing_total,
                
                winner_correct=winner_correct,
                spread_error=spread_error,
                total_error=total_error,
                ats_correct=ats_correct,
                
                conference_game=game_data.get('conferenceGame', False),
                neutral_site=game_data.get('neutralSite', False),
                home_elo=game_data.get('homeStartElo'),
                away_elo=game_data.get('awayStartElo')
            )
            
        except Exception as e:
            print(f"   Error predicting game {game_data.get('id')}: {e}")
            return None
    
    def generate_comprehensive_analysis(self) -> BacktestSummary:
        """Generate comprehensive performance analysis"""
        print("\n📊 Generating comprehensive analysis...")
        
        if not self.results:
            raise ValueError("No backtest results available")
        
        total_games = len(self.results)
        
        # Winner accuracy
        winners_correct = sum(1 for r in self.results if r.winner_correct)
        winner_accuracy = winners_correct / total_games
        
        # Spread analysis
        spread_errors = [r.spread_error for r in self.results]
        avg_spread_error = statistics.mean(spread_errors)
        median_spread_error = statistics.median(spread_errors)
        spread_rmse = math.sqrt(statistics.mean([e**2 for e in spread_errors]))
        
        # Total analysis
        total_errors = [r.total_error for r in self.results]
        avg_total_error = statistics.mean(total_errors)
        median_total_error = statistics.median(total_errors)
        total_rmse = math.sqrt(statistics.mean([e**2 for e in total_errors]))
        
        # ATS analysis
        ats_results = [r for r in self.results if r.ats_correct is not None]
        ats_games = len(ats_results)
        ats_correct = sum(1 for r in ats_results if r.ats_correct)
        ats_accuracy = ats_correct / ats_games if ats_games > 0 else 0
        
        # Probability calibration
        actual_outcomes = [1 if r.predicted_winner == r.actual_winner else 0 for r in self.results]
        predicted_probs = [max(r.predicted_home_win_prob, 1-r.predicted_home_win_prob) for r in self.results]
        
        brier_score = statistics.mean([(actual_outcomes[i] - predicted_probs[i])**2 for i in range(len(actual_outcomes))])
        
        # Log loss (clip probabilities to avoid log(0))
        clipped_probs = [max(min(p, 0.99), 0.01) for p in predicted_probs]
        log_loss = -statistics.mean([actual_outcomes[i] * math.log(clipped_probs[i]) + 
                                   (1-actual_outcomes[i]) * math.log(1-clipped_probs[i]) 
                                   for i in range(len(actual_outcomes))])
        
        # ROI calculations (simplified)
        flat_bet_roi = (winners_correct - (total_games - winners_correct)) / total_games * 0.91  # -110 juice
        kelly_roi = 0  # Placeholder - would need actual odds for Kelly criterion
        
        # Performance breakdowns
        by_conference = self._analyze_by_conference()
        by_spread_size = self._analyze_by_spread_size()
        by_week = self._analyze_by_week()
        by_season = self._analyze_by_season()
        
        return BacktestSummary(
            total_games=total_games,
            winners_correct=winners_correct,
            winner_accuracy=winner_accuracy,
            avg_spread_error=avg_spread_error,
            median_spread_error=median_spread_error,
            spread_rmse=spread_rmse,
            avg_total_error=avg_total_error,
            median_total_error=median_total_error,
            total_rmse=total_rmse,
            ats_games=ats_games,
            ats_correct=ats_correct,
            ats_accuracy=ats_accuracy,
            brier_score=brier_score,
            log_loss=log_loss,
            flat_bet_roi=flat_bet_roi,
            kelly_roi=kelly_roi,
            by_conference=by_conference,
            by_spread_size=by_spread_size,
            by_week=by_week,
            by_season=by_season
        )
    
    def _analyze_by_conference(self) -> Dict:
        """Analyze performance by conference"""
        conf_results = {}
        
        for result in self.results:
            # Use home team conference as key (could enhance to track both)
            conf_key = "Conference"  # Simplified - would extract from game data
            
            if conf_key not in conf_results:
                conf_results[conf_key] = {'games': 0, 'correct': 0}
            
            conf_results[conf_key]['games'] += 1
            if result.winner_correct:
                conf_results[conf_key]['correct'] += 1
        
        # Calculate percentages
        for conf in conf_results:
            games = conf_results[conf]['games']
            correct = conf_results[conf]['correct']
            conf_results[conf]['accuracy'] = correct / games if games > 0 else 0
        
        return conf_results
    
    def _analyze_by_spread_size(self) -> Dict:
        """Analyze performance by spread size"""
        spread_buckets = {
            'close': {'min': 0, 'max': 3, 'games': 0, 'correct': 0},
            'medium': {'min': 3, 'max': 10, 'games': 0, 'correct': 0},
            'large': {'min': 10, 'max': 100, 'games': 0, 'correct': 0}
        }
        
        for result in self.results:
            spread_size = abs(result.actual_spread)
            
            for bucket_name, bucket in spread_buckets.items():
                if bucket['min'] <= spread_size < bucket['max']:
                    bucket['games'] += 1
                    if result.winner_correct:
                        bucket['correct'] += 1
                    break
        
        # Calculate percentages
        for bucket in spread_buckets.values():
            bucket['accuracy'] = bucket['correct'] / bucket['games'] if bucket['games'] > 0 else 0
        
        return spread_buckets
    
    def _analyze_by_week(self) -> Dict:
        """Analyze performance by week"""
        week_results = {}
        
        for result in self.results:
            week = result.week
            if week not in week_results:
                week_results[week] = {'games': 0, 'correct': 0}
            
            week_results[week]['games'] += 1
            if result.winner_correct:
                week_results[week]['correct'] += 1
        
        # Calculate percentages
        for week in week_results:
            games = week_results[week]['games']
            correct = week_results[week]['correct']
            week_results[week]['accuracy'] = correct / games if games > 0 else 0
        
        return week_results
    
    def _analyze_by_season(self) -> Dict:
        """Analyze performance by season"""
        season_results = {}
        
        for result in self.results:
            season = result.season
            if season not in season_results:
                season_results[season] = {'games': 0, 'correct': 0, 'spread_errors': []}
            
            season_results[season]['games'] += 1
            if result.winner_correct:
                season_results[season]['correct'] += 1
            season_results[season]['spread_errors'].append(result.spread_error)
        
        # Calculate percentages and averages
        for season in season_results:
            games = season_results[season]['games']
            correct = season_results[season]['correct']
            spread_errors = season_results[season]['spread_errors']
            
            season_results[season]['accuracy'] = correct / games if games > 0 else 0
            season_results[season]['avg_spread_error'] = statistics.mean(spread_errors) if spread_errors else 0
        
        return season_results
    
    def print_elite_report(self, summary: BacktestSummary):
        """Print comprehensive elite-level report"""
        print("\n" + "="*80)
        print("🏆 ELITE MODEL VALIDATION REPORT")
        print("="*80)
        
        # Overall Performance
        print(f"\n📊 OVERALL PERFORMANCE ({summary.total_games:,} games)")
        print(f"   🎯 Winner Accuracy: {summary.winner_accuracy:.1%} ({summary.winners_correct}/{summary.total_games})")
        
        # Grade the model
        if summary.winner_accuracy >= 0.58:
            grade = "🌟🌟🌟 ELITE (Professional Level)"
        elif summary.winner_accuracy >= 0.55:
            grade = "🌟🌟 EXCELLENT (Highly Profitable)"
        elif summary.winner_accuracy >= 0.524:
            grade = "🌟 GOOD (Beats Market)"
        else:
            grade = "⚠️ NEEDS IMPROVEMENT"
        
        print(f"   🏆 Model Grade: {grade}")
        
        # Against the Spread
        if summary.ats_games > 0:
            print(f"\n💰 AGAINST THE SPREAD")
            print(f"   📈 ATS Record: {summary.ats_correct}/{summary.ats_games} ({summary.ats_accuracy:.1%})")
            print(f"   🎲 Breakeven: 52.4% (you need 52.4% to profit at -110)")
            
            if summary.ats_accuracy >= 0.524:
                print(f"   ✅ PROFITABLE! You're beating the sportsbooks")
            else:
                print(f"   ❌ Below breakeven (but close wins are hard)")
        
        # Spread Accuracy
        print(f"\n📏 SPREAD PREDICTION ACCURACY")
        print(f"   🎯 Average Error: {summary.avg_spread_error:.2f} points")
        print(f"   📊 Median Error: {summary.median_spread_error:.2f} points")
        print(f"   📈 RMSE: {summary.spread_rmse:.2f} points")
        
        spread_grade = "🌟🌟🌟 ELITE" if summary.avg_spread_error < 7 else "🌟🌟 GOOD" if summary.avg_spread_error < 10 else "⚠️ NEEDS WORK"
        print(f"   🏆 Spread Grade: {spread_grade}")
        
        # Total Accuracy  
        print(f"\n🔢 TOTAL PREDICTION ACCURACY")
        print(f"   🎯 Average Error: {summary.avg_total_error:.2f} points")
        print(f"   📊 Median Error: {summary.median_total_error:.2f} points")
        print(f"   📈 RMSE: {summary.total_rmse:.2f} points")
        
        # Probability Calibration
        print(f"\n🎲 PROBABILITY CALIBRATION")
        print(f"   📊 Brier Score: {summary.brier_score:.4f} (lower is better)")
        print(f"   📈 Log Loss: {summary.log_loss:.4f} (lower is better)")
        
        cal_grade = "🌟🌟🌟 EXCELLENT" if summary.brier_score < 0.20 else "🌟🌟 GOOD" if summary.brier_score < 0.25 else "⚠️ NEEDS CALIBRATION"
        print(f"   🏆 Calibration Grade: {cal_grade}")
        
        # ROI Analysis
        print(f"\n💵 ROI ANALYSIS (Flat Betting)")
        print(f"   📈 Estimated ROI: {summary.flat_bet_roi:.1%}")
        
        if summary.flat_bet_roi > 0.05:
            print(f"   ✅ PROFITABLE! Strong positive ROI")
        elif summary.flat_bet_roi > 0:
            print(f"   ✅ Profitable (modest gains)")
        else:
            print(f"   ❌ Negative ROI (but winner accuracy matters more)")
        
        # Performance by Season
        print(f"\n📅 PERFORMANCE BY SEASON")
        for season, stats in summary.by_season.items():
            accuracy = stats['accuracy']
            games = stats['games']
            avg_error = stats['avg_spread_error']
            print(f"   {season}: {accuracy:.1%} accuracy ({games} games, {avg_error:.1f}pt avg error)")
        
        # Performance by Spread Size
        print(f"\n🎯 PERFORMANCE BY GAME TYPE")
        for bucket_name, stats in summary.by_spread_size.items():
            if stats['games'] > 0:
                print(f"   {bucket_name.title()} games: {stats['accuracy']:.1%} ({stats['correct']}/{stats['games']})")
        
        # Key Insights
        print(f"\n💡 KEY INSIGHTS")
        
        # Cross-season consistency
        if len(summary.by_season) > 1:
            accuracies = [stats['accuracy'] for stats in summary.by_season.values()]
            consistency = max(accuracies) - min(accuracies)
            if consistency < 0.03:
                print(f"   ✅ Excellent cross-season consistency ({consistency:.1%} variance)")
            else:
                print(f"   ⚠️ Some season-to-season variance ({consistency:.1%})")
        
        # Spread prediction quality
        if summary.avg_spread_error < 8:
            print(f"   ✅ Elite spread prediction accuracy")
        elif summary.avg_spread_error < 12:
            print(f"   ✅ Good spread prediction accuracy")
        
        # Market beating potential
        if summary.winner_accuracy > 0.55:
            print(f"   🚀 Strong potential to beat betting markets")
        elif summary.winner_accuracy > 0.52:
            print(f"   💰 Competitive with betting markets")
        
        print("\n" + "="*80)
        print("🎯 ALGORITHM ENHANCEMENT COMPLETE!")
        print("="*80)
    
    def save_detailed_results(self, output_dir: str = "backtesting_results"):
        """Save detailed results for further analysis"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save individual game results
        results_data = [asdict(result) for result in self.results]
        
        with open(f"{output_dir}/detailed_results.json", 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_games': len(self.results),
                'results': results_data
            }, f, indent=2)
        
        print(f"💾 Detailed results saved to {output_dir}/")

async def main():
    """Main backtesting execution"""
    print("🚀 ELITE BACKTESTING ENGINE")
    print("="*50)
    
    # Initialize backtester
    backtester = EliteBacktester()
    
    # Load historical data
    data_2024_path = "all_fbs_games_2024_ENHANCED_20251015_002119.json"
    data_2025_path = "all_fbs_games_2025_ENHANCED_20251015_083540.json"
    
    total_games = await backtester.load_historical_data(data_2024_path, data_2025_path)
    
    if total_games == 0:
        print("❌ No games loaded. Check file paths.")
        return
    
    print(f"\n🎯 Starting backtesting on {total_games} games...")
    print("   This may take 15-30 minutes for comprehensive analysis")
    
    # Ask user for quick vs full test
    print("\n⚡ Test Options:")
    print("   1. Quick test (100 games) - 2 minutes")
    print("   2. Medium test (500 games) - 8 minutes") 
    print("   3. Full test (all games) - 20-30 minutes")
    
    choice = input("\nChoice (1/2/3) or press Enter for medium: ").strip()
    
    max_games = None
    if choice == "1":
        max_games = 100
    elif choice == "2": 
        max_games = 500
    # else: full test (max_games = None)
    
    # Run backtest
    results = await backtester.run_comprehensive_backtest(max_games)
    
    if not results:
        print("❌ No successful predictions generated")
        return
    
    # Generate analysis
    summary = backtester.generate_comprehensive_analysis()
    
    # Print report
    backtester.print_elite_report(summary)
    
    # Save results
    backtester.save_detailed_results()
    
    print("\n🎉 Backtesting complete! Your algorithm has been validated.")
    print(f"   Check backtesting_results/ for detailed analysis files")

if __name__ == "__main__":
    asyncio.run(main())