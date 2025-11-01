#!/usr/bin/env python3
"""
🎯 Week 8 Backtesting Script
Tests spread and over/under predictions against actual Week 8 results
Generates HTML report with detailed analysis
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graphqlpredictor import LightningPredictor

@dataclass
class BacktestResult:
    """Individual game backtest result"""
    game_id: int
    home_team: str
    away_team: str

    # Actual results
    actual_home_score: int
    actual_away_score: int
    actual_spread: float  # home_score - away_score
    actual_total: float
    actual_winner: str

    # Predictions
    predicted_spread: float
    predicted_total: float
    predicted_home_win_prob: float
    predicted_winner: str

    # Market data (if available)
    market_spread: Optional[float] = None
    market_total: Optional[float] = None

    # Errors and accuracy
    spread_error: float = 0
    total_error: float = 0
    winner_correct: bool = False
    spread_hit: bool = False  # Within 2.5 points
    total_hit: bool = False   # Exact over/under

    # Context
    conference_game: bool = False
    neutral_site: bool = False

class Week8Backtester:
    """Backtests Week 8 predictions against actual results"""

    def __init__(self):
        self.predictor = None
        self.week8_data = self._load_week8_data()
        self.results: List[BacktestResult] = []

    def _load_week8_data(self) -> Dict:
        """Load Week 8 games data with actual results"""
        try:
            with open('/Users/davlenswain/Desktop/Gameday_Graphql_Model/week8.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading week8.json: {e}")
            return {'games': []}

    def _get_team_id(self, team_name: str) -> Optional[int]:
        """Get team ID from team name using fbs.json"""
        try:
            with open('/Users/davlenswain/Desktop/Gameday_Graphql_Model/fbs.json', 'r') as f:
                teams_data = json.load(f)

            # Try exact match first
            for team in teams_data:
                if team['school'].lower() == team_name.lower():
                    return team['id']

            # Try fuzzy matching
            team_name_lower = team_name.lower()
            for team in teams_data:
                if team_name_lower in team['school'].lower() or team['school'].lower() in team_name_lower:
                    return team['id']

            return None
        except Exception as e:
            print(f"❌ Error getting team ID for {team_name}: {e}")
            return None

    async def initialize_predictor(self):
        """Initialize the Lightning Predictor"""
        try:
            # API Key for College Football Data (same as used in run.py)
            api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
            self.predictor = LightningPredictor(api_key)
            print("✅ Predictor initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing predictor: {e}")
            raise

    async def backtest_all_games(self):
        """Run predictions on all Week 8 games (completed and future)"""
        print("\n" + "="*80)
        print("🎯 PREDICTING ALL WEEK 8 GAMES")
        print("="*80)

        all_games = self.week8_data.get('games', [])
        print(f"📊 Testing {len(all_games)} total games from Week 8")

        completed_games = [game for game in all_games if game.get('completed', False)]
        future_games = [game for game in all_games if not game.get('completed', False)]

        print(f"✅ Completed games: {len(completed_games)}")
        print(f"🔮 Future games: {len(future_games)}")

        # Test completed games first
        if completed_games:
            print(f"\n🏈 TESTING COMPLETED GAMES ({len(completed_games)})")
            for i, game in enumerate(completed_games, 1):
                try:
                    result = await self._backtest_single_game(game)
                    if result:
                        self.results.append(result)
                        self._print_game_result(result, i, len(completed_games), "COMPLETED")

                except Exception as e:
                    print(f"❌ Error testing completed game {game.get('id')}: {e}")
                    continue

        # Predict future games
        if future_games:
            print(f"\n🔮 PREDICTING FUTURE GAMES ({len(future_games)})")
            for i, game in enumerate(future_games, 1):
                try:
                    result = await self._predict_future_game(game)
                    if result:
                        self.results.append(result)
                        self._print_game_result(result, i, len(future_games), "FUTURE")

                except Exception as e:
                    print(f"❌ Error predicting future game {game.get('id')}: {e}")
                    continue

        return self.results

    async def _backtest_single_game(self, game: Dict) -> Optional[BacktestResult]:
        """Backtest a single game"""
        home_team = game.get('homeTeam', '')
        away_team = game.get('awayTeam', '')
        home_score = game.get('homePoints', 0)
        away_score = game.get('awayPoints', 0)

        # Skip if we don't have valid data
        if not home_team or not away_team or home_score is None or away_score is None:
            return None

        try:
            # Get team IDs from names
            home_team_id = self._get_team_id(home_team)
            away_team_id = self._get_team_id(away_team)

            if home_team_id is None or away_team_id is None:
                print(f"❌ Could not find team IDs for {home_team} or {away_team}")
                return None

            # Get prediction using team IDs (home, away order as per predictor function signature)
            prediction = await self.predictor.predict_game(home_team_id, away_team_id)

            # Calculate actual results
            actual_spread = home_score - away_score  # Positive = home won
            actual_total = home_score + away_score
            actual_winner = home_team if home_score > away_score else away_team

            # Extract predictions
            pred_spread = prediction.predicted_spread if hasattr(prediction, 'predicted_spread') else 0
            pred_total = prediction.predicted_total if hasattr(prediction, 'predicted_total') else 0
            pred_home_win_prob = prediction.home_win_prob if hasattr(prediction, 'home_win_prob') else 0.5
            pred_winner = home_team if pred_home_win_prob > 0.5 else away_team

            # Calculate errors
            spread_error = abs(pred_spread - actual_spread)
            total_error = abs(pred_total - actual_total)
            winner_correct = (pred_winner == actual_winner)

            # Determine hits (within acceptable ranges)
            spread_hit = spread_error <= 2.5  # Within 2.5 points
            total_hit = total_error <= 3.0    # Within 3 points of total

            return BacktestResult(
                game_id=game.get('id', 0),
                home_team=home_team,
                away_team=away_team,
                actual_home_score=home_score,
                actual_away_score=away_score,
                actual_spread=actual_spread,
                actual_total=actual_total,
                actual_winner=actual_winner,
                predicted_spread=pred_spread,
                predicted_total=pred_total,
                predicted_home_win_prob=pred_home_win_prob,
                predicted_winner=pred_winner,
                spread_error=spread_error,
                total_error=total_error,
                winner_correct=winner_correct,
                spread_hit=spread_hit,
                total_hit=total_hit,
                conference_game=game.get('conferenceGame', False),
                neutral_site=game.get('neutralSite', False)
            )

        except Exception as e:
            print(f"❌ Error predicting {away_team} @ {home_team}: {e}")
            return None

    async def _predict_future_game(self, game: Dict) -> Optional[BacktestResult]:
        """Predict a future game (no actual results available)"""
        home_team = game.get('homeTeam', '')
        away_team = game.get('awayTeam', '')

        # Skip if we don't have valid data
        if not home_team or not away_team:
            return None

        try:
            # Get team IDs from names
            home_team_id = self._get_team_id(home_team)
            away_team_id = self._get_team_id(away_team)

            if home_team_id is None or away_team_id is None:
                print(f"❌ Could not find team IDs for {home_team} or {away_team}")
                return None

            # Get prediction using team IDs (home, away order as per predictor function signature)
            prediction = await self.predictor.predict_game(home_team_id, away_team_id)

            # Extract predictions
            pred_spread = prediction.predicted_spread if hasattr(prediction, 'predicted_spread') else 0
            pred_total = prediction.predicted_total if hasattr(prediction, 'predicted_total') else 0
            pred_home_win_prob = prediction.home_win_prob if hasattr(prediction, 'home_win_prob') else 0.5
            pred_winner = home_team if pred_home_win_prob > 0.5 else away_team

            return BacktestResult(
                game_id=game.get('id', 0),
                home_team=home_team,
                away_team=away_team,
                actual_home_score=None,  # No actual results for future games
                actual_away_score=None,
                actual_spread=0,  # Placeholder
                actual_total=0,   # Placeholder
                actual_winner="TBD",  # To be determined
                predicted_spread=pred_spread,
                predicted_total=pred_total,
                predicted_home_win_prob=pred_home_win_prob,
                predicted_winner=pred_winner,
                spread_error=0,  # No error for future games
                total_error=0,   # No error for future games
                winner_correct=None,  # Cannot determine for future games
                spread_hit=None,   # Cannot determine for future games
                total_hit=None,    # Cannot determine for future games
                conference_game=game.get('conferenceGame', False),
                neutral_site=game.get('neutralSite', False)
            )

        except Exception as e:
            print(f"❌ Error predicting future game {away_team} @ {home_team}: {e}")
            return None

    def _print_game_result(self, result: BacktestResult, game_num: int, total_games: int, game_type: str = "COMPLETED"):
        """Print individual game result"""
        print(f"\n[{game_num}/{total_games}] {result.away_team} @ {result.home_team}")

        if game_type == "COMPLETED":
            print(f"   Actual: {result.home_team} {result.actual_home_score}, {result.away_team} {result.actual_away_score}")
            print(f"   Predicted Spread: {result.predicted_spread:+.1f} (Actual: {result.actual_spread:+.1f})")
            print(f"   Predicted Total: {result.predicted_total:.1f} (Actual: {result.actual_total:.1f})")
            print(f"   Winner: {'✅' if result.winner_correct else '❌'} | Spread: {'✅' if result.spread_hit else '❌'} | Total: {'✅' if result.total_hit else '❌'}")
        else:  # FUTURE
            print(f"   Predicted Spread: {result.predicted_spread:+.1f}")
            print(f"   Predicted Total: {result.predicted_total:.1f}")
            print(f"   Predicted Winner: {result.predicted_winner} ({result.predicted_home_win_prob:.1%})")

    def generate_summary_stats(self) -> Dict:
        """Generate comprehensive summary statistics for completed games only"""
        if not self.results:
            return {}

        # Only calculate stats for completed games (those with actual results)
        completed_results = [r for r in self.results if r.actual_home_score is not None]

        if not completed_results:
            return {
                'total_games': len(self.results),
                'completed_games': 0,
                'future_games': len(self.results),
                'winner_accuracy': 0,
                'spread_accuracy': 0,
                'total_accuracy': 0,
                'avg_spread_error': 0,
                'avg_total_error': 0,
                'spread_rmse': 0,
                'total_rmse': 0,
                'winners_correct': 0,
                'spread_hits': 0,
                'total_hits': 0
            }

        # Basic counts for completed games
        total_completed = len(completed_results)
        winners_correct = sum(1 for r in completed_results if r.winner_correct)
        spread_hits = sum(1 for r in completed_results if r.spread_hit)
        total_hits = sum(1 for r in completed_results if r.total_hit)

        # Accuracy percentages
        winner_accuracy = (winners_correct / total_completed) * 100
        spread_accuracy = (spread_hits / total_completed) * 100
        total_accuracy = (total_hits / total_completed) * 100

        # Average errors
        avg_spread_error = sum(r.spread_error for r in completed_results) / total_completed
        avg_total_error = sum(r.total_error for r in completed_results) / total_completed

        # RMSE calculations
        spread_rmse = (sum(r.spread_error ** 2 for r in completed_results) / total_completed) ** 0.5
        total_rmse = (sum(r.total_error ** 2 for r in completed_results) / total_completed) ** 0.5

        return {
            'total_games': len(self.results),
            'completed_games': total_completed,
            'future_games': len(self.results) - total_completed,
            'winner_accuracy': winner_accuracy,
            'spread_accuracy': spread_accuracy,
            'total_accuracy': total_accuracy,
            'avg_spread_error': avg_spread_error,
            'avg_total_error': avg_total_error,
            'spread_rmse': spread_rmse,
            'total_rmse': total_rmse,
            'winners_correct': winners_correct,
            'spread_hits': spread_hits,
            'total_hits': total_hits
        }

    def generate_html_report(self, stats: Dict) -> str:
        """Generate HTML report with results"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week 8 Backtest Results - Gameday+</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            background: linear-gradient(45deg, #fbbf24, #f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(30, 41, 59, 0.8);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            backdrop-filter: blur(10px);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #fbbf24;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #94a3b8;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .games-section {{
            background: rgba(30, 41, 59, 0.8);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        .game-card {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 20px;
            padding: 20px;
            margin: 15px 0;
            background: rgba(51, 65, 85, 0.5);
            border-radius: 10px;
            border-left: 4px solid;
        }}
        .completed-game {{
            border-left-color: #3b82f6;
        }}
        .future-game {{
            border-left-color: #f59e0b;
            grid-template-columns: 2fr 1fr 1fr;
        }}
        .game-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .game-type {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .completed-game .game-type {{
            background: #10b981;
            color: white;
        }}
        .future-game .game-type {{
            background: #f59e0b;
            color: black;
        }}
        .game-matchup {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .game-result {{
            text-align: center;
        }}
        .game-prediction {{
            text-align: center;
        }}
        .game-accuracy {{
            text-align: center;
        }}
        .game-note {{
            text-align: center;
            color: #94a3b8;
            font-style: italic;
            grid-column: span 3;
        }}
        .winner-correct {{ border-left-color: #10b981; }}
        .winner-wrong {{ border-left-color: #ef4444; }}
        .spread-hit {{ color: #10b981; font-weight: bold; }}
        .spread-miss {{ color: #ef4444; }}
        .total-hit {{ color: #10b981; font-weight: bold; }}
        .total-miss {{ color: #ef4444; }}
        .footer {{
            text-align: center;
            color: #64748b;
            font-size: 0.9em;
            margin-top: 40px;
        }}
        .accuracy-legend {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        .legend-correct {{ background: #10b981; }}
        .legend-wrong {{ background: #ef4444; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Week 8 Backtest Results</h1>
            <p>Generated on {timestamp}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Games</div>
                <div class="stat-value">{stats.get('total_games', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Completed Games</div>
                <div class="stat-value">{stats.get('completed_games', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Future Games</div>
                <div class="stat-value">{stats.get('future_games', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Winner Accuracy</div>
                <div class="stat-value">{stats.get('winner_accuracy', 0):.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Spread Accuracy (±2.5)</div>
                <div class="stat-value">{stats.get('spread_accuracy', 0):.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Accuracy (±3)</div>
                <div class="stat-value">{stats.get('total_accuracy', 0):.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Spread Error</div>
                <div class="stat-value">{stats.get('avg_spread_error', 0):.1f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Total Error</div>
                <div class="stat-value">{stats.get('avg_total_error', 0):.1f}</div>
            </div>
        </div>

        <div class="accuracy-legend">
            <div class="legend-item">
                <div class="legend-dot legend-correct"></div>
                <span>Hit (within range)</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot legend-wrong"></div>
                <span>Miss (outside range)</span>
            </div>
        </div>

        <div class="games-section">
            <h2 style="margin-bottom: 20px; color: #fbbf24;">📊 Individual Game Results</h2>
'''

        # Add individual game results
        for result in self.results:
            if result.actual_home_score is not None:  # Completed game
                winner_class = "winner-correct" if result.winner_correct else "winner-wrong"
                spread_class = "spread-hit" if result.spread_hit else "spread-miss"
                total_class = "total-hit" if result.total_hit else "total-miss"

                html += f'''
                <div class="game-card {winner_class} completed-game">
                    <div class="game-header">
                        <div class="game-matchup">
                            <strong>{result.away_team} @ {result.home_team}</strong>
                        </div>
                        <div class="game-type">Completed</div>
                    </div>
                    <div class="game-result">
                        <div>Actual: {result.actual_home_score}-{result.actual_away_score}</div>
                        <div>Spread: {result.actual_spread:+.1f}</div>
                        <div>Total: {result.actual_total:.1f}</div>
                    </div>
                    <div class="game-prediction">
                        <div>Pred: {result.predicted_spread:+.1f}</div>
                        <div>Total: {result.predicted_total:.1f}</div>
                        <div>Win%: {result.predicted_home_win_prob:.1%}</div>
                    </div>
                    <div class="game-accuracy">
                        <div>Winner: {'✅' if result.winner_correct else '❌'}</div>
                        <div class="{spread_class}">Spread: {'✅' if result.spread_hit else '❌'}</div>
                        <div class="{total_class}">Total: {'✅' if result.total_hit else '❌'}</div>
                    </div>
                </div>
'''
            else:  # Future game
                html += f'''
                <div class="game-card future-game">
                    <div class="game-header">
                        <div class="game-matchup">
                            <strong>{result.away_team} @ {result.home_team}</strong>
                        </div>
                        <div class="game-type">Future</div>
                    </div>
                    <div class="game-prediction">
                        <div>Pred: {result.predicted_spread:+.1f}</div>
                        <div>Total: {result.predicted_total:.1f}</div>
                        <div>Win%: {result.predicted_home_win_prob:.1%}</div>
                    </div>
                    <div class="game-note">
                        <em>Game has not been played yet</em>
                    </div>
                </div>
'''

        html += '''
        </div>

        <div class="footer">
            <p>Generated by Gameday+ Lightning Predictor | Week 8 Backtest</p>
            <p>Spread accuracy measured within ±2.5 points | Total accuracy measured within ±3 points</p>
        </div>
    </div>
</body>
</html>
'''

        return html

async def main():
    """Main backtesting function"""
    print("🏈 Starting Week 8 Backtest...")

    backtester = Week8Backtester()

    try:
        # Initialize predictor
        await backtester.initialize_predictor()

        # Run backtest
        results = await backtester.backtest_all_games()

        if not results:
            print("❌ No games were successfully backtested")
            return

        # Generate statistics
        stats = backtester.generate_summary_stats()

        # Print summary to console
        print("\n" + "="*80)
        print("📈 BACKTEST SUMMARY")
        print("="*80)
        print(f"Games Tested: {stats['total_games']}")
        print(f"Winner Accuracy: {stats['winner_accuracy']:.1f}% ({stats['winners_correct']}/{stats['total_games']})")
        print(f"Spread Accuracy (±2.5pts): {stats['spread_accuracy']:.1f}% ({stats['spread_hits']}/{stats['total_games']})")
        print(f"Total Accuracy (±3pts): {stats['total_accuracy']:.1f}% ({stats['total_hits']}/{stats['total_games']})")
        print(f"Average Spread Error: {stats['avg_spread_error']:.1f} points")
        print(f"Average Total Error: {stats['avg_total_error']:.1f} points")
        print(f"Spread RMSE: {stats['spread_rmse']:.1f} points")
        print(f"Total RMSE: {stats['total_rmse']:.1f} points")

        # Generate HTML report
        html_report = backtester.generate_html_report(stats)

        # Save HTML report
        report_path = "/Users/davlenswain/Desktop/Gameday_Graphql_Model/week8_backtest_results.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_report)

        print(f"\n✅ HTML report saved to: {report_path}")
        print("🎯 Open the HTML file in your browser to view detailed results!")

    except Exception as e:
        print(f"❌ Backtest failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())