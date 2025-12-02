"""
Arbitrage Detection Module

Detects arbitrage and middle opportunities:
- Pure arbitrage (guaranteed profit)
- Middle opportunities (win both sides)
- Scalping opportunities
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class OpportunityType(Enum):
    """Types of betting opportunities"""
    PURE_ARBITRAGE = "pure_arbitrage"
    MIDDLE = "middle"
    SCALP = "scalp"
    MODEL_EDGE = "model_edge"
    HEDGE = "hedge"


class RiskLevel(Enum):
    """Risk levels for opportunities"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ArbitrageOpportunity:
    """Represents a detected arbitrage or edge opportunity"""
    opportunity_type: OpportunityType
    profit_margin: float  # Percentage profit or expected value
    risk_level: RiskLevel
    bets: List[Dict]  # List of required bets
    explanation: str
    confidence: float  # 0-100 confidence score
    total_stake_required: float
    guaranteed_profit: Optional[float] = None
    potential_middle_profit: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'opportunity_type': self.opportunity_type.value,
            'profit_margin': self.profit_margin,
            'risk_level': self.risk_level.value,
            'bets': self.bets,
            'explanation': self.explanation,
            'confidence': self.confidence,
            'total_stake_required': self.total_stake_required,
            'guaranteed_profit': self.guaranteed_profit,
            'potential_middle_profit': self.potential_middle_profit
        }


class ArbitrageDetector:
    """
    Detects arbitrage and middle betting opportunities across sportsbooks.
    
    Pure Arbitrage: When the combined implied probability < 100%, 
    guaranteed profit regardless of outcome.
    
    Middle: When spread differences create opportunity to win both sides.
    """
    
    def __init__(
        self,
        min_profit_margin: float = 0.5,
        max_market_width: float = 0.25
    ):
        """
        Initialize Arbitrage Detector.
        
        Args:
            min_profit_margin: Minimum profit percentage to report (default 0.5%)
            max_market_width: Maximum acceptable market width for middles (25 cents)
        """
        self.min_profit_margin = min_profit_margin
        self.max_market_width = max_market_width
    
    def detect_two_way_arbitrage(
        self,
        odds_side_a: List[Tuple[str, int]],  # [(book_name, american_odds), ...]
        odds_side_b: List[Tuple[str, int]],
        total_stake: float = 1000.0
    ) -> Optional[ArbitrageOpportunity]:
        """
        Detect pure arbitrage opportunity on a two-way market.
        
        Args:
            odds_side_a: List of (sportsbook, american_odds) for side A
            odds_side_b: List of (sportsbook, american_odds) for side B
            total_stake: Total amount to distribute across bets
            
        Returns:
            ArbitrageOpportunity if found, None otherwise
        """
        best_a = self._find_best_odds(odds_side_a)
        best_b = self._find_best_odds(odds_side_b)
        
        if not best_a or not best_b:
            return None
        
        # Calculate implied probabilities
        prob_a = self._american_to_implied(best_a[1])
        prob_b = self._american_to_implied(best_b[1])
        
        total_implied = prob_a + prob_b
        
        # Arbitrage exists if total implied < 100%
        if total_implied >= 1.0:
            return None
        
        # Calculate profit margin
        profit_margin = (1 / total_implied - 1) * 100
        
        if profit_margin < self.min_profit_margin:
            return None
        
        # Calculate optimal stake distribution
        stake_a = total_stake * prob_a / total_implied
        stake_b = total_stake * prob_b / total_implied
        
        # Calculate guaranteed profit
        decimal_a = self._american_to_decimal(best_a[1])
        decimal_b = self._american_to_decimal(best_b[1])
        
        payout_a = stake_a * decimal_a
        payout_b = stake_b * decimal_b
        
        guaranteed_profit = min(payout_a, payout_b) - total_stake
        
        return ArbitrageOpportunity(
            opportunity_type=OpportunityType.PURE_ARBITRAGE,
            profit_margin=round(profit_margin, 2),
            risk_level=RiskLevel.LOW,
            bets=[
                {
                    'sportsbook': best_a[0],
                    'selection': 'Side A',
                    'american_odds': best_a[1],
                    'decimal_odds': round(decimal_a, 3),
                    'stake': round(stake_a, 2),
                    'potential_return': round(payout_a, 2)
                },
                {
                    'sportsbook': best_b[0],
                    'selection': 'Side B',
                    'american_odds': best_b[1],
                    'decimal_odds': round(decimal_b, 3),
                    'stake': round(stake_b, 2),
                    'potential_return': round(payout_b, 2)
                }
            ],
            explanation=f"Arbitrage opportunity: {best_a[0]} vs {best_b[0]}. "
                       f"Combined implied probability: {total_implied:.2%}",
            confidence=95.0,
            total_stake_required=total_stake,
            guaranteed_profit=round(guaranteed_profit, 2)
        )
    
    def detect_spread_middle(
        self,
        spreads: List[Tuple[str, float, int]],  # [(book, spread, odds), ...]
        total_stake: float = 1000.0
    ) -> Optional[ArbitrageOpportunity]:
        """
        Detect middle opportunity on spread markets.
        
        A middle exists when you can bet both sides with a gap where
        both bets could win.
        
        Args:
            spreads: List of (sportsbook, spread_value, american_odds)
            total_stake: Total amount to distribute
            
        Returns:
            ArbitrageOpportunity if middle found
        """
        if len(spreads) < 2:
            return None
        
        # Separate into positive and negative spreads (relative to same team)
        # Find the best spread on each side
        positive_spreads = [(b, s, o) for b, s, o in spreads if s > 0]
        negative_spreads = [(b, s, o) for b, s, o in spreads if s < 0]
        
        if not positive_spreads or not negative_spreads:
            return None
        
        # Find best positive spread (highest number getting points)
        best_positive = max(positive_spreads, key=lambda x: x[1])
        # Find best negative spread (smallest number giving points)
        best_negative = max(negative_spreads, key=lambda x: x[1])  # -3 > -7
        
        # Calculate middle width
        middle_width = best_positive[1] + best_negative[1]  # e.g., +7 + (-3) = 4
        
        if middle_width <= 0:
            return None  # No middle exists
        
        # Check market width constraint
        market_width = abs(best_positive[1]) - abs(best_negative[1])
        if market_width > self.max_market_width * 100:  # Convert to points
            # Market is too wide, middle might be low quality
            pass  # Still report but with lower confidence
        
        # Calculate stakes (equal distribution for middles)
        stake_each = total_stake / 2
        
        # Calculate potential outcomes
        decimal_pos = self._american_to_decimal(best_positive[2])
        decimal_neg = self._american_to_decimal(best_negative[2])
        
        # If both win (middle hits)
        profit_both_win = (stake_each * decimal_pos) + (stake_each * decimal_neg) - total_stake
        
        # If one wins
        profit_pos_wins = (stake_each * decimal_pos) - stake_each  # Win pos, lose neg
        profit_neg_wins = (stake_each * decimal_neg) - stake_each
        
        # Expected value depends on middle probability
        # Rough estimate: middle width in points / 10 = middle probability
        middle_probability = min(0.3, middle_width / 20)
        
        expected_value = (
            middle_probability * profit_both_win +
            (1 - middle_probability) * max(profit_pos_wins, profit_neg_wins)
        )
        
        return ArbitrageOpportunity(
            opportunity_type=OpportunityType.MIDDLE,
            profit_margin=round((expected_value / total_stake) * 100, 2),
            risk_level=RiskLevel.MEDIUM,
            bets=[
                {
                    'sportsbook': best_positive[0],
                    'selection': f'+{best_positive[1]}',
                    'spread': best_positive[1],
                    'american_odds': best_positive[2],
                    'stake': round(stake_each, 2)
                },
                {
                    'sportsbook': best_negative[0],
                    'selection': f'{best_negative[1]}',
                    'spread': best_negative[1],
                    'american_odds': best_negative[2],
                    'stake': round(stake_each, 2)
                }
            ],
            explanation=f"Middle opportunity: {middle_width} point window. "
                       f"If score lands between spreads, both bets win.",
            confidence=70.0 + (middle_width * 2),  # Higher confidence with wider middle
            total_stake_required=total_stake,
            potential_middle_profit=round(profit_both_win, 2)
        )
    
    def detect_total_middle(
        self,
        totals: List[Tuple[str, float, str, int]],  # [(book, total, over/under, odds), ...]
        total_stake: float = 1000.0
    ) -> Optional[ArbitrageOpportunity]:
        """
        Detect middle opportunity on totals (over/under) markets.
        
        Args:
            totals: List of (sportsbook, total_line, 'over'/'under', american_odds)
            total_stake: Total amount to distribute
            
        Returns:
            ArbitrageOpportunity if middle found
        """
        overs = [(b, t, o) for b, t, ou, o in totals if ou.lower() == 'over']
        unders = [(b, t, o) for b, t, ou, o in totals if ou.lower() == 'under']
        
        if not overs or not unders:
            return None
        
        # Best over is lowest total (e.g., O 42.5 better than O 44.5)
        best_over = min(overs, key=lambda x: x[1])
        # Best under is highest total (e.g., U 44.5 better than U 42.5)
        best_under = max(unders, key=lambda x: x[1])
        
        # Middle width
        middle_width = best_under[1] - best_over[1]
        
        if middle_width <= 0:
            return None
        
        stake_each = total_stake / 2
        
        decimal_over = self._american_to_decimal(best_over[2])
        decimal_under = self._american_to_decimal(best_under[2])
        
        profit_both_win = (stake_each * decimal_over) + (stake_each * decimal_under) - total_stake
        
        # Estimate middle probability
        middle_probability = min(0.25, middle_width / 10)
        
        expected_value = (
            middle_probability * profit_both_win +
            (1 - middle_probability) * ((stake_each * max(decimal_over, decimal_under) - stake_each) - stake_each)
        )
        
        return ArbitrageOpportunity(
            opportunity_type=OpportunityType.MIDDLE,
            profit_margin=round((expected_value / total_stake) * 100, 2),
            risk_level=RiskLevel.MEDIUM,
            bets=[
                {
                    'sportsbook': best_over[0],
                    'selection': f'Over {best_over[1]}',
                    'total': best_over[1],
                    'direction': 'over',
                    'american_odds': best_over[2],
                    'stake': round(stake_each, 2)
                },
                {
                    'sportsbook': best_under[0],
                    'selection': f'Under {best_under[1]}',
                    'total': best_under[1],
                    'direction': 'under',
                    'american_odds': best_under[2],
                    'stake': round(stake_each, 2)
                }
            ],
            explanation=f"Total middle: {middle_width} point window between "
                       f"O {best_over[1]} and U {best_under[1]}",
            confidence=65.0 + (middle_width * 3),
            total_stake_required=total_stake,
            potential_middle_profit=round(profit_both_win, 2)
        )
    
    def detect_all_opportunities(
        self,
        market_data: Dict,
        total_stake: float = 1000.0
    ) -> List[ArbitrageOpportunity]:
        """
        Detect all arbitrage and middle opportunities from market data.
        
        Args:
            market_data: Dictionary containing odds from multiple books:
                {
                    'moneyline': {
                        'home': [(book, odds), ...],
                        'away': [(book, odds), ...]
                    },
                    'spread': {
                        'home': [(book, spread, odds), ...],
                        'away': [(book, spread, odds), ...]
                    },
                    'total': [(book, total, over/under, odds), ...]
                }
            total_stake: Total stake for calculations
            
        Returns:
            List of all detected opportunities
        """
        opportunities = []
        
        # Check moneyline arbitrage
        if 'moneyline' in market_data:
            ml = market_data['moneyline']
            if 'home' in ml and 'away' in ml:
                arb = self.detect_two_way_arbitrage(
                    ml['home'], ml['away'], total_stake
                )
                if arb:
                    opportunities.append(arb)
        
        # Check spread middles
        if 'spread' in market_data:
            sp = market_data['spread']
            all_spreads = []
            if 'home' in sp:
                all_spreads.extend(sp['home'])
            if 'away' in sp:
                all_spreads.extend([(b, -s, o) for b, s, o in sp['away']])
            
            if len(all_spreads) >= 2:
                middle = self.detect_spread_middle(all_spreads, total_stake)
                if middle:
                    opportunities.append(middle)
        
        # Check total middles
        if 'total' in market_data:
            middle = self.detect_total_middle(market_data['total'], total_stake)
            if middle:
                opportunities.append(middle)
        
        # Sort by profit margin
        opportunities.sort(key=lambda x: x.profit_margin, reverse=True)
        
        return opportunities
    
    def _find_best_odds(self, odds_list: List[Tuple[str, int]]) -> Optional[Tuple[str, int]]:
        """Find the best (highest payout) odds from a list."""
        if not odds_list:
            return None
        
        # Convert to decimal for comparison
        best = max(odds_list, key=lambda x: self._american_to_decimal(x[1]))
        return best
    
    def _american_to_decimal(self, american: int) -> float:
        """Convert American odds to decimal."""
        if american > 0:
            return (american / 100) + 1
        else:
            return (100 / abs(american)) + 1
    
    def _american_to_implied(self, american: int) -> float:
        """Convert American odds to implied probability."""
        if american > 0:
            return 100 / (american + 100)
        else:
            return abs(american) / (abs(american) + 100)


def find_arbitrage(
    side_a_odds: List[Tuple[str, int]],
    side_b_odds: List[Tuple[str, int]],
    stake: float = 1000.0
) -> Optional[Dict]:
    """
    Quick utility to find arbitrage opportunity.
    
    Args:
        side_a_odds: List of (sportsbook, american_odds) for side A
        side_b_odds: List of (sportsbook, american_odds) for side B
        stake: Total stake amount
        
    Returns:
        Arbitrage opportunity dict or None
    """
    detector = ArbitrageDetector()
    result = detector.detect_two_way_arbitrage(side_a_odds, side_b_odds, stake)
    return result.to_dict() if result else None
