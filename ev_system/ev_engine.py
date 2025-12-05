"""
EV Detection Engine Module

Main engine that combines all components for real-time +EV detection:
- Sharp book fair line calculation
- Soft book opportunity scanning
- Arbitrage detection
- Portfolio-aware recommendations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from enum import Enum

from .ev_calculator import EVCalculator, OddsConverter, NoVigCalculator
from .kelly_criterion import KellyCriterion, PortfolioManager
from .arbitrage_detector import ArbitrageDetector, ArbitrageOpportunity, OpportunityType, RiskLevel
from .odds_manager import OddsManager, SportsbookOdds, BookType


class ConfidenceLevel(Enum):
    """Confidence levels for +EV opportunities"""
    HIGH = "high"      # 90%+ confidence
    MEDIUM = "medium"  # 70-90% confidence
    LOW = "low"        # 50-70% confidence
    SPECULATIVE = "speculative"  # <50% confidence


@dataclass
class EVOpportunity:
    """Represents a detected +EV betting opportunity"""
    event_id: str
    event_name: str
    market_type: str
    selection: str
    
    # Odds information
    sportsbook: str
    american_odds: int
    decimal_odds: float
    
    # EV calculations
    true_probability: float
    implied_probability: float
    ev_percentage: float
    edge_percentage: float
    
    # Sharp book reference
    sharp_book: str
    sharp_odds: int
    fair_probability: float
    
    # Recommendations
    recommended_stake: float
    kelly_fraction: float
    confidence: ConfidenceLevel
    
    # Timing
    detected_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    
    # Additional context
    market_width: Optional[float] = None
    line_movement: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'market_type': self.market_type,
            'selection': self.selection,
            'sportsbook': self.sportsbook,
            'american_odds': self.american_odds,
            'decimal_odds': self.decimal_odds,
            'true_probability': round(self.true_probability * 100, 2),
            'implied_probability': round(self.implied_probability * 100, 2),
            'ev_percentage': round(self.ev_percentage, 2),
            'edge_percentage': round(self.edge_percentage, 2),
            'sharp_book': self.sharp_book,
            'sharp_odds': self.sharp_odds,
            'fair_probability': round(self.fair_probability * 100, 2),
            'recommended_stake': round(self.recommended_stake, 2),
            'kelly_fraction': round(self.kelly_fraction, 4),
            'confidence': self.confidence.value,
            'detected_at': self.detected_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'market_width': self.market_width,
            'line_movement': self.line_movement,
            'notes': self.notes
        }


class EVDetectionEngine:
    """
    Main engine for detecting +EV betting opportunities.
    
    Combines sharp book analysis, soft book scanning, and portfolio
    management for comprehensive +EV identification.
    """
    
    # Default sharp books for fair line calculation
    DEFAULT_SHARP_BOOKS = ['pinnacle', 'betcris', 'bookmaker', 'circa']
    
    # Default soft books to scan for +EV
    DEFAULT_SOFT_BOOKS = [
        'draftkings', 'fanduel', 'betmgm', 'caesars', 
        'bet365', 'bovada', 'pointsbet', 'espnbet'
    ]
    
    def __init__(
        self,
        bankroll: float = 10000.0,
        min_ev_threshold: float = 0.01,
        min_edge_threshold: float = 0.02,
        max_market_width: float = 0.25,
        kelly_fraction: float = 0.25,
        sharp_books: Optional[List[str]] = None,
        soft_books: Optional[List[str]] = None
    ):
        """
        Initialize EV Detection Engine.
        
        Args:
            bankroll: Total bankroll for position sizing
            min_ev_threshold: Minimum EV percentage to flag (1% default)
            min_edge_threshold: Minimum edge over fair line (2% default)
            max_market_width: Maximum acceptable market width (25 cents)
            kelly_fraction: Fraction of Kelly to use for sizing
            sharp_books: List of sharp book names
            soft_books: List of soft book names to scan
        """
        self.bankroll = bankroll
        self.min_ev_threshold = min_ev_threshold
        self.min_edge_threshold = min_edge_threshold
        self.max_market_width = max_market_width
        self.kelly_fraction = kelly_fraction
        
        self.sharp_books = [b.lower() for b in (sharp_books or self.DEFAULT_SHARP_BOOKS)]
        self.soft_books = [b.lower() for b in (soft_books or self.DEFAULT_SOFT_BOOKS)]
        
        # Initialize components
        self.ev_calculator = EVCalculator(min_ev_threshold=min_ev_threshold)
        self.odds_converter = OddsConverter()
        self.no_vig_calculator = NoVigCalculator()
        self.kelly = KellyCriterion(bankroll=bankroll, kelly_fraction=kelly_fraction)
        self.portfolio = PortfolioManager(
            initial_bankroll=bankroll,
            kelly_fraction=kelly_fraction
        )
        self.arbitrage_detector = ArbitrageDetector()
        self.odds_manager = OddsManager()
        
        # Detected opportunities
        self.opportunities: List[EVOpportunity] = []
        self.arbitrage_opportunities: List[ArbitrageOpportunity] = []
    
    def process_odds_update(
        self,
        event_id: str,
        event_name: str,
        odds_data: List[Dict]
    ) -> Dict[str, Any]:
        """
        Process incoming odds data and detect opportunities.
        
        Args:
            event_id: Unique event identifier
            event_name: Human-readable event name
            odds_data: List of odds from different sportsbooks:
                [
                    {
                        'sportsbook': 'pinnacle',
                        'market_type': 'moneyline',
                        'home_odds': -150,
                        'away_odds': 130,
                        'spread': -7.5,
                        'spread_odds': -110,
                        'total': 45.5,
                        'over_odds': -110,
                        'under_odds': -110
                    },
                    ...
                ]
                
        Returns:
            Dictionary with detected opportunities and analysis
        """
        # Store odds in manager
        self._store_odds(event_id, odds_data)
        
        # Get sharp book consensus
        sharp_consensus = self._calculate_sharp_consensus(event_id, odds_data)
        
        # Scan soft books for +EV
        ev_opps = self._scan_for_plus_ev(
            event_id, event_name, odds_data, sharp_consensus
        )
        
        # Detect arbitrage opportunities
        arb_opps = self._detect_arbitrage(event_id, event_name, odds_data)
        
        # Store opportunities
        self.opportunities.extend(ev_opps)
        self.arbitrage_opportunities.extend(arb_opps)
        
        return {
            'event_id': event_id,
            'event_name': event_name,
            'sharp_consensus': sharp_consensus,
            'ev_opportunities': [o.to_dict() for o in ev_opps],
            'arbitrage_opportunities': [o.to_dict() for o in arb_opps],
            'total_opportunities': len(ev_opps) + len(arb_opps)
        }
    
    def _store_odds(self, event_id: str, odds_data: List[Dict]):
        """Store odds in the odds manager."""
        for odds in odds_data:
            sportsbook = odds.get('sportsbook', 'unknown')
            
            # Moneyline
            if 'home_odds' in odds:
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='moneyline',
                    selection='home',
                    american_odds=odds['home_odds']
                )
            
            if 'away_odds' in odds:
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='moneyline',
                    selection='away',
                    american_odds=odds['away_odds']
                )
            
            # Spread
            if 'spread' in odds:
                spread_odds = odds.get('spread_odds', -110)
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='spread',
                    selection='home',
                    american_odds=spread_odds,
                    spread_value=odds['spread']
                )
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='spread',
                    selection='away',
                    american_odds=spread_odds,
                    spread_value=-odds['spread']
                )
            
            # Total
            if 'total' in odds:
                over_odds = odds.get('over_odds', -110)
                under_odds = odds.get('under_odds', -110)
                
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='total',
                    selection='over',
                    american_odds=over_odds,
                    total_value=odds['total']
                )
                self.odds_manager.add_odds(
                    sportsbook=sportsbook,
                    event_id=event_id,
                    market_type='total',
                    selection='under',
                    american_odds=under_odds,
                    total_value=odds['total']
                )
    
    def _calculate_sharp_consensus(
        self,
        event_id: str,
        odds_data: List[Dict]
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate fair probabilities from sharp book consensus.
        
        Returns:
            Dictionary mapping market_type -> selection -> fair_probability
        """
        consensus = {}
        
        # Filter sharp book odds
        sharp_odds = [
            o for o in odds_data 
            if o.get('sportsbook', '').lower() in self.sharp_books
        ]
        
        if not sharp_odds:
            # Use all odds if no sharp books available
            sharp_odds = odds_data
        
        # Calculate for each market type
        for market_type in ['moneyline', 'spread', 'total']:
            consensus[market_type] = {}
            
            if market_type == 'moneyline':
                home_odds = [o['home_odds'] for o in sharp_odds if 'home_odds' in o]
                away_odds = [o['away_odds'] for o in sharp_odds if 'away_odds' in o]
                
                if home_odds and away_odds:
                    avg_home = sum(home_odds) // len(home_odds)
                    avg_away = sum(away_odds) // len(away_odds)
                    
                    fair_probs, _ = NoVigCalculator.calculate_fair_odds_from_sharp_book(
                        [avg_home, avg_away]
                    )
                    
                    consensus[market_type]['home'] = fair_probs[0]
                    consensus[market_type]['away'] = fair_probs[1]
            
            elif market_type == 'total':
                over_odds = [o.get('over_odds', -110) for o in sharp_odds if 'total' in o]
                under_odds = [o.get('under_odds', -110) for o in sharp_odds if 'total' in o]
                
                if over_odds and under_odds:
                    avg_over = sum(over_odds) // len(over_odds)
                    avg_under = sum(under_odds) // len(under_odds)
                    
                    fair_probs, _ = NoVigCalculator.calculate_fair_odds_from_sharp_book(
                        [avg_over, avg_under]
                    )
                    
                    consensus[market_type]['over'] = fair_probs[0]
                    consensus[market_type]['under'] = fair_probs[1]
        
        return consensus
    
    def _scan_for_plus_ev(
        self,
        event_id: str,
        event_name: str,
        odds_data: List[Dict],
        sharp_consensus: Dict
    ) -> List[EVOpportunity]:
        """Scan soft books for +EV opportunities."""
        opportunities = []
        
        # Get sharp book reference
        sharp_ref = None
        for odds in odds_data:
            if odds.get('sportsbook', '').lower() in self.sharp_books:
                sharp_ref = odds
                break
        
        if not sharp_ref:
            sharp_ref = odds_data[0] if odds_data else {}
        
        # Scan moneyline
        if 'moneyline' in sharp_consensus and sharp_consensus['moneyline']:
            for selection in ['home', 'away']:
                if selection not in sharp_consensus['moneyline']:
                    continue
                    
                fair_prob = sharp_consensus['moneyline'][selection]
                odds_key = f'{selection}_odds'
                
                for odds in odds_data:
                    sportsbook = odds.get('sportsbook', '').lower()
                    
                    # Skip sharp books
                    if sportsbook in self.sharp_books:
                        continue
                    
                    if odds_key not in odds:
                        continue
                    
                    american_odds = odds[odds_key]
                    
                    opp = self._evaluate_opportunity(
                        event_id=event_id,
                        event_name=event_name,
                        market_type='moneyline',
                        selection=selection,
                        sportsbook=sportsbook,
                        american_odds=american_odds,
                        fair_probability=fair_prob,
                        sharp_book=sharp_ref.get('sportsbook', 'consensus'),
                        sharp_odds=sharp_ref.get(odds_key, american_odds)
                    )
                    
                    if opp:
                        opportunities.append(opp)
        
        # Scan totals
        if 'total' in sharp_consensus and sharp_consensus['total']:
            for selection in ['over', 'under']:
                if selection not in sharp_consensus['total']:
                    continue
                    
                fair_prob = sharp_consensus['total'][selection]
                odds_key = f'{selection}_odds'
                
                for odds in odds_data:
                    sportsbook = odds.get('sportsbook', '').lower()
                    
                    if sportsbook in self.sharp_books:
                        continue
                    
                    if odds_key not in odds:
                        continue
                    
                    american_odds = odds[odds_key]
                    
                    opp = self._evaluate_opportunity(
                        event_id=event_id,
                        event_name=event_name,
                        market_type='total',
                        selection=selection,
                        sportsbook=sportsbook,
                        american_odds=american_odds,
                        fair_probability=fair_prob,
                        sharp_book=sharp_ref.get('sportsbook', 'consensus'),
                        sharp_odds=sharp_ref.get(odds_key, american_odds)
                    )
                    
                    if opp:
                        opportunities.append(opp)
        
        # Sort by EV percentage
        opportunities.sort(key=lambda x: x.ev_percentage, reverse=True)
        
        return opportunities
    
    def _evaluate_opportunity(
        self,
        event_id: str,
        event_name: str,
        market_type: str,
        selection: str,
        sportsbook: str,
        american_odds: int,
        fair_probability: float,
        sharp_book: str,
        sharp_odds: int
    ) -> Optional[EVOpportunity]:
        """
        Evaluate if an opportunity meets +EV thresholds.
        
        Returns:
            EVOpportunity if +EV, None otherwise
        """
        # Calculate EV
        ev_result = self.ev_calculator.calculate_ev(
            true_probability=fair_probability,
            american_odds=american_odds
        )
        
        # Check thresholds
        if not ev_result['is_plus_ev']:
            return None
        
        if ev_result['edge_percentage'] / 100 < self.min_edge_threshold:
            return None
        
        # Calculate recommended stake
        decimal_odds = self.odds_converter.american_to_decimal(american_odds)
        sizing = self.portfolio.calculate_position_size(
            probability=fair_probability,
            decimal_odds=decimal_odds
        )
        
        # Determine confidence level
        ev_pct = ev_result['ev_percentage'] / 100
        edge_pct = ev_result['edge_percentage'] / 100
        
        if ev_pct >= 0.05 and edge_pct >= 0.04:
            confidence = ConfidenceLevel.HIGH
        elif ev_pct >= 0.03 and edge_pct >= 0.025:
            confidence = ConfidenceLevel.MEDIUM
        elif ev_pct >= 0.01:
            confidence = ConfidenceLevel.LOW
        else:
            confidence = ConfidenceLevel.SPECULATIVE
        
        return EVOpportunity(
            event_id=event_id,
            event_name=event_name,
            market_type=market_type,
            selection=selection,
            sportsbook=sportsbook,
            american_odds=american_odds,
            decimal_odds=decimal_odds,
            true_probability=fair_probability,
            implied_probability=ev_result['implied_probability'] / 100,
            ev_percentage=ev_result['ev_percentage'],
            edge_percentage=ev_result['edge_percentage'],
            sharp_book=sharp_book,
            sharp_odds=sharp_odds,
            fair_probability=fair_probability,
            recommended_stake=sizing['recommended_bet'],
            kelly_fraction=sizing.get('adjusted_kelly_fraction', 0),
            confidence=confidence,
            notes=[]
        )
    
    def _detect_arbitrage(
        self,
        event_id: str,
        event_name: str,
        odds_data: List[Dict]
    ) -> List[ArbitrageOpportunity]:
        """Detect arbitrage opportunities."""
        opportunities = []
        
        # Prepare data for arbitrage detector
        home_ml_odds = [(o['sportsbook'], o['home_odds']) for o in odds_data if 'home_odds' in o]
        away_ml_odds = [(o['sportsbook'], o['away_odds']) for o in odds_data if 'away_odds' in o]
        
        # Check moneyline arbitrage
        if home_ml_odds and away_ml_odds:
            arb = self.arbitrage_detector.detect_two_way_arbitrage(
                home_ml_odds, away_ml_odds
            )
            if arb:
                opportunities.append(arb)
        
        # Check total middles
        totals = []
        for odds in odds_data:
            if 'total' in odds:
                totals.append((odds['sportsbook'], odds['total'], 'over', odds.get('over_odds', -110)))
                totals.append((odds['sportsbook'], odds['total'], 'under', odds.get('under_odds', -110)))
        
        if len(totals) >= 2:
            middle = self.arbitrage_detector.detect_total_middle(totals)
            if middle:
                opportunities.append(middle)
        
        return opportunities
    
    def get_active_opportunities(
        self,
        min_ev: Optional[float] = None,
        max_age_seconds: int = 300
    ) -> List[EVOpportunity]:
        """
        Get currently active +EV opportunities.
        
        Args:
            min_ev: Minimum EV percentage filter
            max_age_seconds: Maximum age of opportunity
            
        Returns:
            List of active opportunities
        """
        current_time = datetime.now()
        active = []
        
        for opp in self.opportunities:
            # Check age
            age = (current_time - opp.detected_at).total_seconds()
            if age > max_age_seconds:
                continue
            
            # Check EV threshold
            if min_ev and opp.ev_percentage < min_ev:
                continue
            
            active.append(opp)
        
        return active
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of current state and opportunities."""
        return {
            'bankroll': self.bankroll,
            'total_ev_opportunities': len(self.opportunities),
            'total_arbitrage_opportunities': len(self.arbitrage_opportunities),
            'active_ev_opportunities': len(self.get_active_opportunities()),
            'portfolio_metrics': self.portfolio.get_performance_metrics(),
            'thresholds': {
                'min_ev': self.min_ev_threshold,
                'min_edge': self.min_edge_threshold,
                'kelly_fraction': self.kelly_fraction
            }
        }
    
    def clear_opportunities(self):
        """Clear all stored opportunities."""
        self.opportunities.clear()
        self.arbitrage_opportunities.clear()


# Example usage and quick calculation functions
def quick_ev_check(
    sharp_home: int,
    sharp_away: int,
    soft_odds: int,
    selection: str = 'home'
) -> Dict:
    """
    Quick EV check comparing sharp to soft book.
    
    Args:
        sharp_home: Sharp book home odds (American)
        sharp_away: Sharp book away odds (American)
        soft_odds: Soft book odds for selection (American)
        selection: 'home' or 'away'
        
    Returns:
        EV calculation results
    """
    calculator = EVCalculator()
    selection_idx = 0 if selection == 'home' else 1
    
    return calculator.calculate_ev_from_sharp_line(
        sharp_odds=[sharp_home, sharp_away],
        soft_odds=soft_odds,
        selection_index=selection_idx
    )


def find_best_ev(
    sharp_odds: Tuple[int, int],
    soft_books: Dict[str, Tuple[int, int]]
) -> List[Dict]:
    """
    Find best +EV opportunities across soft books.
    
    Args:
        sharp_odds: (home_odds, away_odds) from sharp book
        soft_books: {book_name: (home_odds, away_odds), ...}
        
    Returns:
        List of +EV opportunities sorted by EV
    """
    engine = EVDetectionEngine()
    
    odds_data = [
        {
            'sportsbook': 'pinnacle',
            'home_odds': sharp_odds[0],
            'away_odds': sharp_odds[1]
        }
    ]
    
    for book_name, (home, away) in soft_books.items():
        odds_data.append({
            'sportsbook': book_name,
            'home_odds': home,
            'away_odds': away
        })
    
    result = engine.process_odds_update(
        event_id='quick_check',
        event_name='Quick EV Check',
        odds_data=odds_data
    )
    
    return result['ev_opportunities']
