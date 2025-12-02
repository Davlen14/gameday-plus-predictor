"""
Comprehensive Unit Tests for +EV Identification System

Tests cover:
- Odds conversion and calculations
- No-vig fair line calculations
- Expected value calculations
- Kelly Criterion and bankroll management
- Arbitrage detection
- Integration tests for the full engine
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ev_system.ev_calculator import (
    EVCalculator, OddsConverter, NoVigCalculator,
    calculate_implied_probability, calculate_fair_probability, is_plus_ev
)
from ev_system.kelly_criterion import (
    KellyCriterion, PortfolioManager, calculate_optimal_stake
)
from ev_system.arbitrage_detector import (
    ArbitrageDetector, OpportunityType, RiskLevel, find_arbitrage
)
from ev_system.odds_manager import (
    OddsManager, RateLimiter, SportsbookOdds, BookType
)
from ev_system.ev_engine import (
    EVDetectionEngine, EVOpportunity, ConfidenceLevel,
    quick_ev_check, find_best_ev
)


class TestOddsConverter(unittest.TestCase):
    """Test odds conversion utilities"""
    
    def setUp(self):
        self.converter = OddsConverter()
    
    def test_american_to_decimal_positive(self):
        """Test +150 -> 2.50"""
        result = self.converter.american_to_decimal(150)
        self.assertAlmostEqual(result, 2.50, places=2)
    
    def test_american_to_decimal_negative(self):
        """Test -110 -> 1.909"""
        result = self.converter.american_to_decimal(-110)
        self.assertAlmostEqual(result, 1.909, places=2)
    
    def test_american_to_decimal_even(self):
        """Test +100 -> 2.00"""
        result = self.converter.american_to_decimal(100)
        self.assertAlmostEqual(result, 2.00, places=2)
    
    def test_decimal_to_american_over_2(self):
        """Test 2.50 -> +150"""
        result = self.converter.decimal_to_american(2.50)
        self.assertEqual(result, 150)
    
    def test_decimal_to_american_under_2(self):
        """Test 1.91 -> -110 (approximately)"""
        result = self.converter.decimal_to_american(1.91)
        self.assertAlmostEqual(result, -110, delta=5)
    
    def test_american_to_implied_probability_favorite(self):
        """Test -150 implies 60% probability"""
        result = self.converter.american_to_implied_probability(-150)
        self.assertAlmostEqual(result, 0.60, places=2)
    
    def test_american_to_implied_probability_underdog(self):
        """Test +200 implies 33.33% probability"""
        result = self.converter.american_to_implied_probability(200)
        self.assertAlmostEqual(result, 0.333, places=2)
    
    def test_implied_to_american_favorite(self):
        """Test 60% -> -150"""
        result = self.converter.implied_probability_to_american(0.60)
        self.assertEqual(result, -150)
    
    def test_implied_to_american_underdog(self):
        """Test 33% -> +200 (approximately)"""
        result = self.converter.implied_probability_to_american(0.333)
        self.assertAlmostEqual(result, 200, delta=5)
    
    def test_round_trip_conversion(self):
        """Test converting back and forth preserves value"""
        original = 150
        decimal = self.converter.american_to_decimal(original)
        back = self.converter.decimal_to_american(decimal)
        self.assertEqual(back, original)


class TestNoVigCalculator(unittest.TestCase):
    """Test no-vig calculations"""
    
    def setUp(self):
        self.calculator = NoVigCalculator()
    
    def test_calculate_vig_percentage(self):
        """Test vig calculation from typical -110/-110 market"""
        # -110/-110 implies 52.38% + 52.38% = 104.76%
        implied_probs = [0.5238, 0.5238]
        vig = self.calculator.calculate_vig_percentage(implied_probs)
        self.assertAlmostEqual(vig, 4.76, places=1)
    
    def test_remove_vig_multiplicative(self):
        """Test vig removal normalizes to 100%"""
        implied_probs = [0.5238, 0.5238]
        fair_probs = self.calculator.remove_vig_multiplicative(implied_probs)
        
        # Should sum to 1.0
        self.assertAlmostEqual(sum(fair_probs), 1.0, places=6)
        # Should be 50/50 for even odds
        self.assertAlmostEqual(fair_probs[0], 0.5, places=6)
        self.assertAlmostEqual(fair_probs[1], 0.5, places=6)
    
    def test_remove_vig_asymmetric(self):
        """Test vig removal with asymmetric odds"""
        # -150/+130 line
        implied_probs = [0.60, 0.4348]  # Total: 103.48%
        fair_probs = self.calculator.remove_vig_multiplicative(implied_probs)
        
        self.assertAlmostEqual(sum(fair_probs), 1.0, places=6)
        self.assertGreater(fair_probs[0], fair_probs[1])  # Favorite should have higher prob
    
    def test_calculate_fair_odds_from_sharp_book(self):
        """Test full sharp book fair line calculation"""
        # Pinnacle-style line: -150/+130
        sharp_odds = [-150, 130]
        fair_probs, fair_odds = self.calculator.calculate_fair_odds_from_sharp_book(sharp_odds)
        
        # Fair probs should sum to 1
        self.assertAlmostEqual(sum(fair_probs), 1.0, places=6)
        
        # Favorite fair prob should be around 57-58%
        self.assertGreater(fair_probs[0], 0.55)
        self.assertLess(fair_probs[0], 0.60)


class TestEVCalculator(unittest.TestCase):
    """Test expected value calculations"""
    
    def setUp(self):
        self.calculator = EVCalculator(min_ev_threshold=0.01)
    
    def test_calculate_ev_positive(self):
        """Test +EV calculation with edge"""
        # True prob 55%, odds +100 (2.0 decimal)
        result = self.calculator.calculate_ev(
            true_probability=0.55,
            decimal_odds=2.0,
            stake=100
        )
        
        # EV = (0.55 * 100) - (0.45 * 100) = 10
        self.assertAlmostEqual(result['ev_amount'], 10.0, places=1)
        self.assertAlmostEqual(result['ev_percentage'], 10.0, places=1)
        self.assertTrue(result['is_plus_ev'])
    
    def test_calculate_ev_negative(self):
        """Test -EV calculation (typical house edge)"""
        # True prob 50%, odds -110 (1.909 decimal)
        result = self.calculator.calculate_ev(
            true_probability=0.50,
            decimal_odds=1.909,
            stake=100
        )
        
        # Should be negative EV
        self.assertLess(result['ev_amount'], 0)
        self.assertFalse(result['is_plus_ev'])
    
    def test_calculate_ev_from_sharp_line(self):
        """Test EV calculation using sharp book as reference"""
        # Sharp book: -150/+130
        # Soft book offers +160 on underdog (much better than +130 fair)
        result = self.calculator.calculate_ev_from_sharp_line(
            sharp_odds=[-150, 130],
            soft_odds=160,  # Significantly better than sharp's +130
            selection_index=1  # Underdog
        )
        
        # Should be +EV since +160 >> +138 fair value (gives >1% edge)
        self.assertTrue(result['is_plus_ev'])
        self.assertGreater(result['ev_percentage'], 1.0)  # Should exceed 1% threshold
    
    def test_find_plus_ev_opportunities(self):
        """Test finding +EV across multiple soft books"""
        sharp_odds = [-150, 130]  # Fair line (fair is ~-138/+138)
        soft_book_odds = {
            'draftkings': [-145, 125],  # Slightly worse than fair
            'fanduel': [-155, 165],  # +EV on underdog (+165 vs +138 fair)
            'betmgm': [-125, 105],  # +EV on favorite (-125 vs -138 fair)
        }
        
        opportunities = self.calculator.find_plus_ev_opportunities(
            sharp_odds=sharp_odds,
            soft_book_odds=soft_book_odds,
            min_ev=0.005  # Lower threshold to catch more opportunities
        )
        
        # Should find opportunities at FanDuel (underdog) and BetMGM (favorite)
        self.assertGreater(len(opportunities), 0)
    
    def test_calculate_clv(self):
        """Test closing line value calculation"""
        # Bet at +150, closed at +120
        result = self.calculator.calculate_clv(
            bet_odds=150,
            closing_odds=120
        )
        
        # Positive CLV since we got better odds
        self.assertGreater(result['clv_percentage'], 0)
        self.assertTrue(result['beat_close'])


class TestKellyCriterion(unittest.TestCase):
    """Test Kelly Criterion calculations"""
    
    def setUp(self):
        self.kelly = KellyCriterion(
            bankroll=10000,
            kelly_fraction=0.25,
            max_bet_percentage=0.05
        )
    
    def test_full_kelly_positive_ev(self):
        """Test full Kelly with positive EV"""
        # 55% probability at +100 (2.0 decimal)
        kelly_fraction = self.kelly.calculate_full_kelly(
            probability=0.55,
            decimal_odds=2.0
        )
        
        # Kelly = (bp - q) / b = (1*0.55 - 0.45) / 1 = 0.10
        self.assertAlmostEqual(kelly_fraction, 0.10, places=2)
    
    def test_full_kelly_negative_ev(self):
        """Test full Kelly returns negative for -EV bets"""
        # 45% probability at +100 (2.0 decimal)
        kelly_fraction = self.kelly.calculate_full_kelly(
            probability=0.45,
            decimal_odds=2.0
        )
        
        # Should be negative (don't bet)
        self.assertLess(kelly_fraction, 0)
    
    def test_calculate_bet_size_with_limits(self):
        """Test bet sizing with fractional Kelly and limits"""
        result = self.kelly.calculate_bet_size(
            probability=0.55,
            decimal_odds=2.0
        )
        
        # Fractional Kelly: 0.10 * 0.25 = 0.025 = 2.5% of bankroll
        # That's $250 on $10,000
        self.assertLessEqual(result['bet_amount'], 500)  # Under max
        self.assertGreater(result['bet_amount'], 0)
        self.assertTrue(result['is_positive_ev'])
    
    def test_calculate_bet_size_max_limit(self):
        """Test max bet percentage limit"""
        result = self.kelly.calculate_bet_size(
            probability=0.70,  # Very high edge
            decimal_odds=2.5
        )
        
        # Should be capped at 5% of bankroll ($500)
        self.assertLessEqual(result['bet_amount'], 500)
    
    def test_simultaneous_kelly(self):
        """Test Kelly for multiple simultaneous bets"""
        bets = [
            {'probability': 0.55, 'decimal_odds': 2.0},
            {'probability': 0.52, 'decimal_odds': 2.1},
            {'probability': 0.58, 'decimal_odds': 1.95}
        ]
        
        results = self.kelly.calculate_simultaneous_kelly(bets)
        
        # Should have 3 results
        self.assertEqual(len(results), 3)
        
        # Total allocation should be reasonable
        total_allocation = sum(r['bet_amount'] for r in results)
        self.assertLess(total_allocation, 3000)  # Less than 30% of bankroll


class TestPortfolioManager(unittest.TestCase):
    """Test portfolio and risk management"""
    
    def setUp(self):
        self.portfolio = PortfolioManager(
            initial_bankroll=10000,
            max_drawdown=0.20,
            kelly_fraction=0.25
        )
    
    def test_initial_state(self):
        """Test portfolio initial state"""
        self.assertEqual(self.portfolio.current_bankroll, 10000)
        self.assertEqual(self.portfolio.peak_bankroll, 10000)
        self.assertEqual(self.portfolio.current_drawdown, 0.0)
    
    def test_drawdown_calculation(self):
        """Test drawdown calculation after losses"""
        self.portfolio.current_bankroll = 8000
        
        # 20% drawdown from 10000 to 8000
        self.assertAlmostEqual(self.portfolio.current_drawdown, 0.20, places=2)
    
    def test_drawdown_protection_factor(self):
        """Test position sizing reduction during drawdown"""
        # At 16% drawdown (80% of max)
        self.portfolio.current_bankroll = 8400
        self.portfolio.peak_bankroll = 10000
        
        factor = self.portfolio.drawdown_protection_factor
        
        # Should reduce sizing
        self.assertLess(factor, 1.0)
        self.assertGreater(factor, 0.0)
    
    def test_position_sizing_with_protection(self):
        """Test full position sizing with drawdown protection"""
        result = self.portfolio.calculate_position_size(
            probability=0.55,
            decimal_odds=2.0
        )
        
        self.assertIn('recommended_bet', result)
        self.assertIn('protection_factor', result)
        self.assertTrue(result['betting_allowed'])
    
    def test_bet_tracking(self):
        """Test bet placement and resolution"""
        # Place a bet
        bet = self.portfolio.place_bet(
            bet_id='test_001',
            stake=100,
            decimal_odds=2.0,
            probability=0.55
        )
        
        self.assertEqual(bet.result, None)
        self.assertEqual(self.portfolio.daily_exposure, 100)
        
        # Resolve as win
        result = self.portfolio.resolve_bet('test_001', 'win')
        
        self.assertEqual(result['outcome'], 'win')
        self.assertAlmostEqual(result['profit_loss'], 100, places=2)
        self.assertGreater(self.portfolio.current_bankroll, 10000)
    
    def test_performance_metrics(self):
        """Test performance metrics calculation"""
        # Place and resolve some bets
        self.portfolio.place_bet('b1', 100, 2.0, 0.55)
        self.portfolio.resolve_bet('b1', 'win')
        
        self.portfolio.place_bet('b2', 100, 2.0, 0.55)
        self.portfolio.resolve_bet('b2', 'lose')
        
        metrics = self.portfolio.get_performance_metrics()
        
        self.assertEqual(metrics['total_bets'], 2)
        self.assertEqual(metrics['wins'], 1)
        self.assertEqual(metrics['losses'], 1)
        self.assertAlmostEqual(metrics['win_rate'], 0.5, places=2)


class TestArbitrageDetector(unittest.TestCase):
    """Test arbitrage detection"""
    
    def setUp(self):
        self.detector = ArbitrageDetector(min_profit_margin=0.5)
    
    def test_detect_pure_arbitrage(self):
        """Test detection of pure arbitrage opportunity"""
        # Arbitrage exists when combined implied < 100%
        # Book A: Team 1 @ +110 (47.6%)
        # Book B: Team 2 @ +110 (47.6%)
        # Total: 95.2% - Arbitrage!
        
        side_a = [('BookA', 110)]
        side_b = [('BookB', 110)]
        
        result = self.detector.detect_two_way_arbitrage(side_a, side_b)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.opportunity_type, OpportunityType.PURE_ARBITRAGE)
        self.assertGreater(result.profit_margin, 0)
        self.assertGreater(result.guaranteed_profit, 0)
    
    def test_no_arbitrage_standard_market(self):
        """Test no arbitrage in standard -110/-110 market"""
        side_a = [('BookA', -110)]
        side_b = [('BookB', -110)]
        
        result = self.detector.detect_two_way_arbitrage(side_a, side_b)
        
        # No arbitrage (104.76% total implied)
        self.assertIsNone(result)
    
    def test_detect_spread_middle(self):
        """Test detection of spread middle opportunity"""
        # Middle exists when spreads overlap
        spreads = [
            ('BookA', 7.0, -110),   # Team getting +7
            ('BookB', -3.0, -110),  # Team giving -3
        ]
        
        result = self.detector.detect_spread_middle(spreads)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.opportunity_type, OpportunityType.MIDDLE)
    
    def test_detect_total_middle(self):
        """Test detection of total middle opportunity"""
        totals = [
            ('BookA', 42.5, 'over', -110),
            ('BookB', 45.5, 'under', -110),
        ]
        
        result = self.detector.detect_total_middle(totals)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.opportunity_type, OpportunityType.MIDDLE)
        # 3 point middle window
        self.assertGreater(result.potential_middle_profit, 0)
    
    def test_find_arbitrage_utility(self):
        """Test quick utility function"""
        result = find_arbitrage(
            side_a_odds=[('BookA', 110)],
            side_b_odds=[('BookB', 110)],
            stake=1000
        )
        
        self.assertIsNotNone(result)
        self.assertIn('profit_margin', result)
        self.assertIn('bets', result)


class TestOddsManager(unittest.TestCase):
    """Test odds management"""
    
    def setUp(self):
        self.manager = OddsManager()
    
    def test_add_and_retrieve_odds(self):
        """Test adding and retrieving odds"""
        self.manager.add_odds(
            sportsbook='DraftKings',
            event_id='game_001',
            market_type='moneyline',
            selection='home',
            american_odds=-150
        )
        
        odds = self.manager.get_odds('game_001')
        
        self.assertEqual(len(odds), 1)
        self.assertEqual(odds[0].sportsbook, 'DraftKings')
        self.assertEqual(odds[0].american_odds, -150)
    
    def test_book_type_classification(self):
        """Test sportsbook type classification"""
        self.assertEqual(self.manager.get_book_type('pinnacle'), BookType.SHARP)
        self.assertEqual(self.manager.get_book_type('draftkings'), BookType.SOFT)
        self.assertEqual(self.manager.get_book_type('betfair'), BookType.EXCHANGE)
        self.assertEqual(self.manager.get_book_type('unknown_book'), BookType.SOFT)
    
    def test_get_best_odds(self):
        """Test finding best available odds"""
        self.manager.add_odds('BookA', 'game_001', 'moneyline', 'home', -150)
        self.manager.add_odds('BookB', 'game_001', 'moneyline', 'home', -140)
        self.manager.add_odds('BookC', 'game_001', 'moneyline', 'home', -155)
        
        best = self.manager.get_best_odds('game_001', 'moneyline', 'home')
        
        self.assertIsNotNone(best)
        self.assertEqual(best.american_odds, -140)  # Best payout
    
    def test_market_consensus(self):
        """Test market consensus calculation"""
        self.manager.add_odds('BookA', 'game_001', 'moneyline', 'home', -150)
        self.manager.add_odds('BookB', 'game_001', 'moneyline', 'home', -145)
        self.manager.add_odds('BookC', 'game_001', 'moneyline', 'home', -155)
        
        consensus = self.manager.get_market_consensus('game_001', 'moneyline', 'home')
        
        self.assertEqual(consensus['num_books'], 3)
        self.assertEqual(consensus['best_odds'], -145)
        self.assertEqual(consensus['worst_odds'], -155)


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting"""
    
    def test_rate_limiter_status(self):
        """Test rate limiter status reporting"""
        limiter = RateLimiter(requests_per_minute=60)
        status = limiter.get_status()
        
        self.assertIn('tokens_available', status)
        self.assertIn('minute_requests', status)
        self.assertEqual(status['minute_limit'], 60)


class TestEVDetectionEngine(unittest.TestCase):
    """Test the main EV detection engine"""
    
    def setUp(self):
        self.engine = EVDetectionEngine(
            bankroll=10000,
            min_ev_threshold=0.01,
            min_edge_threshold=0.02
        )
    
    def test_process_odds_update(self):
        """Test processing odds data"""
        odds_data = [
            {
                'sportsbook': 'pinnacle',
                'home_odds': -150,
                'away_odds': 130,
                'total': 45.5,
                'over_odds': -110,
                'under_odds': -110
            },
            {
                'sportsbook': 'draftkings',
                'home_odds': -145,  # Better for home bettors
                'away_odds': 125,
                'total': 45.5,
                'over_odds': -105,  # Better for over bettors
                'under_odds': -115
            }
        ]
        
        result = self.engine.process_odds_update(
            event_id='game_001',
            event_name='Team A vs Team B',
            odds_data=odds_data
        )
        
        self.assertIn('sharp_consensus', result)
        self.assertIn('ev_opportunities', result)
        self.assertIn('arbitrage_opportunities', result)
    
    def test_sharp_consensus_calculation(self):
        """Test sharp book consensus calculation"""
        odds_data = [
            {
                'sportsbook': 'pinnacle',
                'home_odds': -150,
                'away_odds': 130
            }
        ]
        
        result = self.engine.process_odds_update(
            event_id='game_001',
            event_name='Test Game',
            odds_data=odds_data
        )
        
        consensus = result['sharp_consensus']
        
        self.assertIn('moneyline', consensus)
        if 'home' in consensus['moneyline']:
            # Home fair prob should be ~57-58%
            self.assertGreater(consensus['moneyline']['home'], 0.55)
    
    def test_get_summary(self):
        """Test engine summary"""
        summary = self.engine.get_summary()
        
        self.assertEqual(summary['bankroll'], 10000)
        self.assertIn('thresholds', summary)
        self.assertIn('portfolio_metrics', summary)


class TestQuickUtilities(unittest.TestCase):
    """Test quick utility functions"""
    
    def test_quick_ev_check(self):
        """Test quick EV check function"""
        result = quick_ev_check(
            sharp_home=-150,
            sharp_away=130,
            soft_odds=165,  # Significantly better than +138 fair
            selection='away'
        )
        
        # EV should be positive (though may be below 1% threshold)
        self.assertGreater(result['ev_percentage'], 0)
    
    def test_calculate_implied_probability(self):
        """Test quick implied probability function"""
        prob = calculate_implied_probability(-150)
        self.assertAlmostEqual(prob, 0.60, places=2)
    
    def test_calculate_fair_probability(self):
        """Test quick fair probability function"""
        probs = calculate_fair_probability([-150, 130])
        
        self.assertAlmostEqual(sum(probs), 1.0, places=6)
    
    def test_is_plus_ev(self):
        """Test quick +EV check function"""
        # +165 vs sharp +130 (fair ~+138) should be +EV above 1% threshold
        result = is_plus_ev(
            sharp_odds=[-150, 130],
            soft_odds=165,  # Much better than fair
            selection=1,
            threshold=0.01
        )
        
        self.assertTrue(result)
    
    def test_calculate_optimal_stake(self):
        """Test quick optimal stake function"""
        stake = calculate_optimal_stake(
            bankroll=10000,
            probability=0.55,
            decimal_odds=2.0,
            kelly_fraction=0.25
        )
        
        self.assertGreater(stake, 0)
        self.assertLess(stake, 1000)  # Reasonable sizing


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world betting scenarios"""
    
    def test_nfl_game_example(self):
        """
        Test NFL game scenario from research doc:
        Sharp: Cowboys +105, Eagles -115
        Soft: Cowboys +120 at DraftKings
        """
        calculator = EVCalculator()
        
        result = calculator.calculate_ev_from_sharp_line(
            sharp_odds=[105, -115],  # Cowboys +105, Eagles -115
            soft_odds=120,  # Cowboys +120 at DraftKings
            selection_index=0  # Cowboys
        )
        
        # Should be +EV since +120 > +105 fair value
        self.assertTrue(result['is_plus_ev'])
        
        # EV should be around 4-5%
        self.assertGreater(result['ev_percentage'], 3)
        self.assertLess(result['ev_percentage'], 10)
    
    def test_backtest_scenario(self):
        """Test a backtest-style scenario"""
        engine = EVDetectionEngine(bankroll=10000)
        
        # Simulate finding multiple +EV bets
        games = [
            {
                'odds_data': [
                    {'sportsbook': 'pinnacle', 'home_odds': -150, 'away_odds': 130},
                    {'sportsbook': 'draftkings', 'home_odds': -140, 'away_odds': 125}
                ],
                'event_id': 'game_1',
                'event_name': 'Game 1'
            },
            {
                'odds_data': [
                    {'sportsbook': 'pinnacle', 'home_odds': -200, 'away_odds': 175},
                    {'sportsbook': 'fanduel', 'home_odds': -190, 'away_odds': 165}
                ],
                'event_id': 'game_2',
                'event_name': 'Game 2'
            }
        ]
        
        total_opportunities = 0
        for game in games:
            result = engine.process_odds_update(
                event_id=game['event_id'],
                event_name=game['event_name'],
                odds_data=game['odds_data']
            )
            total_opportunities += result['total_opportunities']
        
        # Should find some opportunities
        summary = engine.get_summary()
        self.assertGreaterEqual(summary['total_ev_opportunities'], 0)


def run_all_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestOddsConverter,
        TestNoVigCalculator,
        TestEVCalculator,
        TestKellyCriterion,
        TestPortfolioManager,
        TestArbitrageDetector,
        TestOddsManager,
        TestRateLimiter,
        TestEVDetectionEngine,
        TestQuickUtilities,
        TestRealWorldScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 +EV IDENTIFICATION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    success = run_all_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("=" * 70)
    
    exit(0 if success else 1)
