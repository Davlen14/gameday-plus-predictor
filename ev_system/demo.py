#!/usr/bin/env python3
"""
+EV Identification System Demo

This demo showcases all the capabilities of the +EV identification system:
1. Odds conversion and probability calculations
2. No-vig fair line calculation from sharp books
3. Expected Value (EV) detection
4. Kelly Criterion bet sizing
5. Arbitrage and middle opportunity detection
6. Portfolio management with drawdown protection

Run this demo to see the system in action!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ev_system import (
    EVCalculator, OddsConverter, NoVigCalculator,
    KellyCriterion, PortfolioManager,
    ArbitrageDetector,
    OddsManager, BookType,
    EVDetectionEngine
)


def print_header(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"📊 {title}")
    print("=" * 70)


def demo_odds_conversion():
    """Demonstrate odds conversion utilities"""
    print_header("ODDS CONVERSION DEMO")
    
    converter = OddsConverter()
    
    # American to Decimal
    examples = [150, -110, 100, -200, 250]
    print("\n🔄 American to Decimal Conversion:")
    for american in examples:
        decimal = converter.american_to_decimal(american)
        implied = converter.american_to_implied_probability(american)
        print(f"   {american:+4d} → {decimal:.3f} decimal → {implied*100:.1f}% implied prob")
    
    # Decimal to American
    print("\n🔄 Decimal to American Conversion:")
    decimals = [1.50, 1.91, 2.00, 2.50, 3.00]
    for decimal in decimals:
        american = converter.decimal_to_american(decimal)
        implied = converter.decimal_to_implied_probability(decimal)
        print(f"   {decimal:.2f} → {american:+4d} American → {implied*100:.1f}% implied prob")


def demo_no_vig_calculation():
    """Demonstrate no-vig fair line calculation"""
    print_header("NO-VIG FAIR LINE CALCULATION")
    
    no_vig = NoVigCalculator()
    
    # Standard -110/-110 line
    print("\n📉 Standard -110/-110 Market:")
    implied_probs = [0.5238, 0.5238]  # -110 each side
    print(f"   Implied probabilities: {implied_probs[0]*100:.2f}% + {implied_probs[1]*100:.2f}%")
    print(f"   Total: {sum(implied_probs)*100:.2f}%")
    print(f"   Vig: {no_vig.calculate_vig_percentage(implied_probs):.2f}%")
    
    fair_probs = no_vig.remove_vig_multiplicative(implied_probs)
    print(f"   Fair probabilities: {fair_probs[0]*100:.2f}% + {fair_probs[1]*100:.2f}%")
    
    # Sharp book line
    print("\n📈 Sharp Book Line (-150/+130):")
    sharp_odds = [-150, 130]
    fair_probs, fair_odds = no_vig.calculate_fair_odds_from_sharp_book(sharp_odds)
    
    print(f"   Sharp odds: Home {sharp_odds[0]}, Away {sharp_odds[1]}")
    print(f"   Fair probabilities: {fair_probs[0]*100:.2f}% vs {fair_probs[1]*100:.2f}%")
    print(f"   Fair odds: {fair_odds[0]:+d} vs {fair_odds[1]:+d}")


def demo_ev_calculation():
    """Demonstrate Expected Value calculations"""
    print_header("+EV DETECTION DEMO")
    
    calculator = EVCalculator(min_ev_threshold=0.01)
    
    # Example 1: Coin flip at +100
    print("\n🎲 Example 1: Fair coin at +100 odds")
    result = calculator.calculate_ev(true_probability=0.50, american_odds=100)
    print(f"   True probability: {result['true_probability']}%")
    print(f"   Implied probability: {result['implied_probability']}%")
    print(f"   EV: ${result['ev_amount']} ({result['ev_percentage']}%)")
    print(f"   Is +EV: {result['is_plus_ev']}")
    
    # Example 2: Edge on a bet
    print("\n🎯 Example 2: 55% edge at +100 odds")
    result = calculator.calculate_ev(true_probability=0.55, american_odds=100)
    print(f"   True probability: {result['true_probability']}%")
    print(f"   Implied probability: {result['implied_probability']}%")
    print(f"   EV: ${result['ev_amount']} ({result['ev_percentage']}%)")
    print(f"   Edge: {result['edge_percentage']}%")
    print(f"   Is +EV: {result['is_plus_ev']}")
    
    # Example 3: Sharp vs Soft book comparison
    print("\n🏈 Example 3: NFL Game - Sharp vs Soft Book")
    print("   Sharp Book (Pinnacle): Cowboys +105, Eagles -115")
    print("   Soft Book (DraftKings): Cowboys +120")
    
    result = calculator.calculate_ev_from_sharp_line(
        sharp_odds=[105, -115],
        soft_odds=120,
        selection_index=0
    )
    
    print(f"\n   True probability (from sharp): {result['true_probability']}%")
    print(f"   Implied probability (at +120): {result['implied_probability']}%")
    print(f"   EV: ${result['ev_amount']} ({result['ev_percentage']}%)")
    print(f"   Edge: {result['edge_percentage']}%")
    print(f"   ✅ +EV BET!" if result['is_plus_ev'] else "   ❌ Not +EV")


def demo_kelly_criterion():
    """Demonstrate Kelly Criterion bet sizing"""
    print_header("KELLY CRITERION BET SIZING")
    
    kelly = KellyCriterion(
        bankroll=10000,
        kelly_fraction=0.25,
        max_bet_percentage=0.05
    )
    
    # Example 1: Moderate edge
    print("\n💰 Example 1: 55% probability at +100 odds")
    print(f"   Bankroll: $10,000")
    result = kelly.calculate_bet_size(probability=0.55, decimal_odds=2.0)
    
    print(f"   Full Kelly: {result['full_kelly_fraction']*100:.2f}%")
    print(f"   Quarter Kelly: {result['adjusted_kelly_fraction']*100:.2f}%")
    print(f"   Recommended bet: ${result['bet_amount']:.2f}")
    print(f"   Potential profit: ${result['potential_profit']:.2f}")
    
    # Example 2: Large edge
    print("\n💰 Example 2: 60% probability at +110 odds (large edge)")
    result = kelly.calculate_bet_size(probability=0.60, decimal_odds=2.10)
    
    print(f"   Full Kelly: {result['full_kelly_fraction']*100:.2f}%")
    print(f"   Quarter Kelly: {result['adjusted_kelly_fraction']*100:.2f}%")
    print(f"   Recommended bet: ${result['bet_amount']:.2f}")
    print(f"   (Capped at max bet limit: {kelly.max_bet_percentage*100}%)")


def demo_arbitrage_detection():
    """Demonstrate arbitrage and middle detection"""
    print_header("ARBITRAGE & MIDDLE DETECTION")
    
    detector = ArbitrageDetector(min_profit_margin=0.5)
    
    # Pure Arbitrage Example
    print("\n⚡ Pure Arbitrage Example:")
    print("   Book A: Team 1 @ +110 (47.6%)")
    print("   Book B: Team 2 @ +110 (47.6%)")
    print("   Total implied: 95.2% (< 100%)")
    
    side_a = [('BookA', 110)]
    side_b = [('BookB', 110)]
    
    arb = detector.detect_two_way_arbitrage(side_a, side_b, total_stake=1000)
    
    if arb:
        print(f"\n   ✅ ARBITRAGE FOUND!")
        print(f"   Profit margin: {arb.profit_margin:.2f}%")
        print(f"   Guaranteed profit: ${arb.guaranteed_profit:.2f}")
        print(f"   Bets required:")
        for bet in arb.bets:
            print(f"      - {bet['sportsbook']}: ${bet['stake']:.2f} at {bet['american_odds']:+d}")
    
    # Total Middle Example
    print("\n📊 Total Middle Example:")
    print("   Book A: Over 42.5 @ -110")
    print("   Book B: Under 45.5 @ -110")
    print("   Middle window: 3 points")
    
    totals = [
        ('BookA', 42.5, 'over', -110),
        ('BookB', 45.5, 'under', -110),
    ]
    
    middle = detector.detect_total_middle(totals, total_stake=1000)
    
    if middle:
        print(f"\n   ✅ MIDDLE OPPORTUNITY!")
        print(f"   Expected profit: {middle.profit_margin:.2f}%")
        print(f"   If middle hits: ${middle.potential_middle_profit:.2f}")
        print(f"   {middle.explanation}")


def demo_portfolio_management():
    """Demonstrate portfolio management with drawdown protection"""
    print_header("PORTFOLIO MANAGEMENT")
    
    portfolio = PortfolioManager(
        initial_bankroll=10000,
        max_drawdown=0.20,
        kelly_fraction=0.25
    )
    
    print(f"\n💼 Initial Setup:")
    print(f"   Starting bankroll: ${portfolio.initial_bankroll:,.2f}")
    print(f"   Max drawdown limit: {portfolio.max_drawdown*100:.0f}%")
    
    # Simulate some bets
    print("\n📝 Simulating bet history...")
    
    # Win
    bet1 = portfolio.place_bet('bet_001', 200, 2.0, 0.55)
    result1 = portfolio.resolve_bet('bet_001', 'win')
    print(f"   Bet 1: $200 @ 2.0x - WIN (+${result1['profit_loss']:.2f})")
    
    # Win
    bet2 = portfolio.place_bet('bet_002', 250, 1.91, 0.53)
    result2 = portfolio.resolve_bet('bet_002', 'win')
    print(f"   Bet 2: $250 @ 1.91x - WIN (+${result2['profit_loss']:.2f})")
    
    # Lose
    bet3 = portfolio.place_bet('bet_003', 300, 2.10, 0.52)
    result3 = portfolio.resolve_bet('bet_003', 'lose')
    print(f"   Bet 3: $300 @ 2.10x - LOSE (${result3['profit_loss']:.2f})")
    
    metrics = portfolio.get_performance_metrics()
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Total bets: {metrics['total_bets']}")
    print(f"   Win rate: {metrics['win_rate']*100:.1f}%")
    print(f"   Total wagered: ${metrics['total_wagered']:,.2f}")
    print(f"   Total P/L: ${metrics['total_profit_loss']:,.2f}")
    print(f"   ROI: {metrics['roi']:.1f}%")
    print(f"   Current bankroll: ${metrics['current_bankroll']:,.2f}")
    print(f"   Bankroll growth: {metrics['bankroll_growth']:.1f}%")
    
    # Show drawdown protection
    print("\n🛡️  Drawdown Protection:")
    print(f"   Current drawdown: {portfolio.current_drawdown*100:.1f}%")
    print(f"   Protection factor: {portfolio.drawdown_protection_factor:.2f}")


def demo_full_engine():
    """Demonstrate the full EV detection engine"""
    print_header("FULL EV DETECTION ENGINE")
    
    engine = EVDetectionEngine(
        bankroll=10000,
        min_ev_threshold=0.01,
        min_edge_threshold=0.02,
        kelly_fraction=0.25
    )
    
    print("\n🔍 Processing odds from multiple sportsbooks...")
    
    # Simulate a college football game
    odds_data = [
        {
            'sportsbook': 'pinnacle',
            'home_odds': -180,
            'away_odds': 155,
            'total': 52.5,
            'over_odds': -108,
            'under_odds': -112
        },
        {
            'sportsbook': 'draftkings',
            'home_odds': -170,  # Better for home bettors
            'away_odds': 145,
            'total': 52.5,
            'over_odds': -105,
            'under_odds': -115
        },
        {
            'sportsbook': 'fanduel',
            'home_odds': -175,
            'away_odds': 165,  # Better for away bettors
            'total': 53.0,
            'over_odds': -110,
            'under_odds': -110
        },
        {
            'sportsbook': 'betmgm',
            'home_odds': -165,  # Best for home bettors
            'away_odds': 140,
            'total': 52.0,
            'over_odds': -108,
            'under_odds': -112
        }
    ]
    
    result = engine.process_odds_update(
        event_id='cfb_001',
        event_name='Ohio State vs Michigan',
        odds_data=odds_data
    )
    
    print(f"\n📈 Sharp Consensus (from Pinnacle):")
    consensus = result['sharp_consensus']
    if 'moneyline' in consensus and consensus['moneyline']:
        print(f"   Home fair probability: {consensus['moneyline'].get('home', 0)*100:.1f}%")
        print(f"   Away fair probability: {consensus['moneyline'].get('away', 0)*100:.1f}%")
    
    print(f"\n🎯 +EV Opportunities Found: {len(result['ev_opportunities'])}")
    for opp in result['ev_opportunities'][:5]:  # Show top 5
        print(f"   • {opp['sportsbook']}: {opp['selection']} @ {opp['american_odds']:+d}")
        print(f"     EV: {opp['ev_percentage']:.2f}%, Edge: {opp['edge_percentage']:.2f}%")
        print(f"     Recommended bet: ${opp['recommended_stake']:.2f}")
        print(f"     Confidence: {opp['confidence']}")
    
    if not result['ev_opportunities']:
        print("   No +EV opportunities above threshold found")
    
    print(f"\n⚡ Arbitrage Opportunities: {len(result['arbitrage_opportunities'])}")
    for arb in result['arbitrage_opportunities']:
        print(f"   • Type: {arb['opportunity_type']}")
        print(f"     Profit margin: {arb['profit_margin']:.2f}%")
    
    # Summary
    summary = engine.get_summary()
    print(f"\n📊 Engine Summary:")
    print(f"   Bankroll: ${summary['bankroll']:,.2f}")
    print(f"   Min EV threshold: {summary['thresholds']['min_ev']*100:.1f}%")
    print(f"   Min edge threshold: {summary['thresholds']['min_edge']*100:.1f}%")


def main():
    """Run all demos"""
    print("\n" + "🎰" * 35)
    print("\n   +EV IDENTIFICATION SYSTEM - COMPREHENSIVE DEMO")
    print("\n" + "🎰" * 35)
    
    demo_odds_conversion()
    demo_no_vig_calculation()
    demo_ev_calculation()
    demo_kelly_criterion()
    demo_arbitrage_detection()
    demo_portfolio_management()
    demo_full_engine()
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print("\nThe +EV system is ready for use. Key features:")
    print("  • Odds conversion between American, Decimal, and Implied Probability")
    print("  • No-vig fair line calculation from sharp books")
    print("  • Expected Value detection with configurable thresholds")
    print("  • Kelly Criterion bet sizing with risk management")
    print("  • Arbitrage and middle opportunity detection")
    print("  • Portfolio management with drawdown protection")
    print("\nTo use in your code:")
    print("  from ev_system import EVDetectionEngine, EVCalculator, KellyCriterion")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
