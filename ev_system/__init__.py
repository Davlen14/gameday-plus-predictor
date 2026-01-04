"""
+EV (Positive Expected Value) Identification System

A comprehensive system for identifying positive expected value betting opportunities
in sports betting markets through real-time odds analysis and mathematical modeling.

Components:
- EVCalculator: Core expected value and no-vig calculations
- KellyCriterion: Optimal bankroll management
- ArbitrageDetector: Pure arbitrage and middle opportunity detection
- OddsManager: Multi-sportsbook odds aggregation and rate limiting
- PortfolioManager: Risk management and position sizing

Usage:
    from ev_system import EVCalculator, KellyCriterion, ArbitrageDetector
    
    # Calculate EV for a bet
    calculator = EVCalculator()
    ev = calculator.calculate_ev(true_probability=0.55, decimal_odds=2.10)
    
    # Calculate optimal bet size
    kelly = KellyCriterion(bankroll=10000)
    bet_size = kelly.calculate_bet_size(probability=0.55, decimal_odds=2.10)
"""

from .ev_calculator import EVCalculator, OddsConverter, NoVigCalculator
from .kelly_criterion import KellyCriterion, PortfolioManager
from .arbitrage_detector import ArbitrageDetector, ArbitrageOpportunity, OpportunityType, RiskLevel
from .odds_manager import OddsManager, RateLimiter, SportsbookOdds, BookType
from .ev_engine import EVDetectionEngine, EVOpportunity, ConfidenceLevel

__version__ = "1.0.0"
__all__ = [
    "EVCalculator",
    "OddsConverter", 
    "NoVigCalculator",
    "KellyCriterion",
    "PortfolioManager",
    "ArbitrageDetector",
    "ArbitrageOpportunity",
    "OpportunityType",
    "RiskLevel",
    "OddsManager",
    "RateLimiter",
    "SportsbookOdds",
    "BookType",
    "EVDetectionEngine",
    "EVOpportunity",
    "ConfidenceLevel",
]
