"""
Kelly Criterion Module

Optimal bankroll management using Kelly Criterion and portfolio theory:
- Full Kelly calculation
- Fractional Kelly for risk management
- Multi-bet portfolio optimization
- Drawdown protection
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import math


@dataclass
class BetRecord:
    """Record of a placed bet for tracking"""
    bet_id: str
    timestamp: datetime
    stake: float
    odds_decimal: float
    probability: float
    result: Optional[str] = None  # "win", "lose", "push", "pending"
    profit_loss: Optional[float] = None
    
    def resolve(self, outcome: str) -> float:
        """Resolve the bet and calculate P/L"""
        self.result = outcome
        if outcome == "win":
            self.profit_loss = self.stake * (self.odds_decimal - 1)
        elif outcome == "lose":
            self.profit_loss = -self.stake
        elif outcome == "push":
            self.profit_loss = 0.0
        else:
            self.profit_loss = None
        return self.profit_loss or 0.0


class KellyCriterion:
    """
    Kelly Criterion calculator for optimal bet sizing.
    
    The Kelly Criterion determines the optimal fraction of bankroll to bet
    to maximize long-term growth while managing risk.
    
    Formula: f* = (bp - q) / b
    Where:
        f* = fraction of bankroll to bet
        b = decimal odds - 1 (net odds)
        p = probability of winning
        q = probability of losing (1 - p)
    """
    
    def __init__(
        self,
        bankroll: float,
        kelly_fraction: float = 0.25,
        max_bet_percentage: float = 0.05,
        min_bet_amount: float = 10.0
    ):
        """
        Initialize Kelly Criterion calculator.
        
        Args:
            bankroll: Total bankroll amount
            kelly_fraction: Fraction of Kelly to use (0.25 = quarter Kelly)
            max_bet_percentage: Maximum percentage of bankroll per bet (default 5%)
            min_bet_amount: Minimum bet amount
        """
        self.bankroll = bankroll
        self.kelly_fraction = kelly_fraction
        self.max_bet_percentage = max_bet_percentage
        self.min_bet_amount = min_bet_amount
    
    def calculate_full_kelly(
        self,
        probability: float,
        decimal_odds: float
    ) -> float:
        """
        Calculate full Kelly fraction.
        
        Args:
            probability: True probability of winning (0-1)
            decimal_odds: Decimal odds offered
            
        Returns:
            Optimal fraction of bankroll to bet (can be negative for -EV bets)
        """
        if probability <= 0 or probability >= 1:
            raise ValueError("Probability must be between 0 and 1 (exclusive)")
        if decimal_odds <= 1:
            raise ValueError("Decimal odds must be greater than 1")
        
        b = decimal_odds - 1  # Net odds
        p = probability
        q = 1 - probability
        
        # Kelly formula: f* = (bp - q) / b
        kelly = (b * p - q) / b
        
        return kelly
    
    def calculate_bet_size(
        self,
        probability: float,
        decimal_odds: float,
        apply_fractional: bool = True,
        apply_limits: bool = True
    ) -> Dict[str, float]:
        """
        Calculate recommended bet size with risk management.
        
        Args:
            probability: True probability of winning
            decimal_odds: Decimal odds offered
            apply_fractional: Whether to apply fractional Kelly
            apply_limits: Whether to apply min/max limits
            
        Returns:
            Dictionary with bet sizing information
        """
        full_kelly = self.calculate_full_kelly(probability, decimal_odds)
        
        # Apply fractional Kelly
        if apply_fractional:
            kelly_fraction = full_kelly * self.kelly_fraction
        else:
            kelly_fraction = full_kelly
        
        # Calculate bet amount
        bet_amount = self.bankroll * max(0, kelly_fraction)
        
        # Apply limits
        if apply_limits:
            max_bet = self.bankroll * self.max_bet_percentage
            bet_amount = min(bet_amount, max_bet)
            bet_amount = max(bet_amount, 0)  # Can't bet negative
            
            # Apply minimum only if bet is > 0
            if 0 < bet_amount < self.min_bet_amount:
                bet_amount = 0  # Don't bet if below minimum
        
        # Calculate expected growth
        expected_growth = self._calculate_expected_growth(
            probability, decimal_odds, kelly_fraction
        )
        
        return {
            "bet_amount": round(bet_amount, 2),
            "full_kelly_fraction": round(full_kelly, 4),
            "adjusted_kelly_fraction": round(kelly_fraction, 4),
            "bet_percentage": round((bet_amount / self.bankroll) * 100, 2),
            "expected_growth_rate": round(expected_growth, 4),
            "is_positive_ev": full_kelly > 0,
            "bankroll": self.bankroll,
            "potential_profit": round(bet_amount * (decimal_odds - 1), 2),
            "potential_loss": round(bet_amount, 2)
        }
    
    def _calculate_expected_growth(
        self,
        probability: float,
        decimal_odds: float,
        kelly_fraction: float
    ) -> float:
        """
        Calculate expected logarithmic growth rate.
        
        The Kelly Criterion maximizes E[log(wealth)], which corresponds
        to maximizing the geometric growth rate.
        """
        if kelly_fraction <= 0:
            return 0.0
        
        b = decimal_odds - 1
        p = probability
        q = 1 - probability
        f = kelly_fraction
        
        # Expected log growth: p * log(1 + b*f) + q * log(1 - f)
        # Protect against log(0)
        if f >= 1:
            return float('-inf')
        
        growth = p * math.log(1 + b * f) + q * math.log(1 - f)
        return growth
    
    def update_bankroll(self, new_bankroll: float):
        """Update bankroll after wins/losses."""
        self.bankroll = max(0, new_bankroll)
    
    def calculate_simultaneous_kelly(
        self,
        bets: List[Dict]
    ) -> List[Dict]:
        """
        Calculate Kelly for multiple simultaneous independent bets.
        
        When placing multiple bets at once, we need to account for
        total capital allocation.
        
        Args:
            bets: List of dicts with 'probability' and 'decimal_odds'
            
        Returns:
            List of bet sizing recommendations
        """
        # Calculate individual Kelly fractions
        results = []
        total_kelly = 0
        
        for bet in bets:
            kelly = self.calculate_full_kelly(
                bet['probability'],
                bet['decimal_odds']
            )
            if kelly > 0:
                total_kelly += kelly * self.kelly_fraction
                results.append({
                    **bet,
                    'kelly_fraction': kelly * self.kelly_fraction
                })
        
        # If total exceeds max allocation, scale down proportionally
        max_total = self.max_bet_percentage * 3  # Allow 3x max for multiple bets
        
        if total_kelly > max_total:
            scale_factor = max_total / total_kelly
        else:
            scale_factor = 1.0
        
        # Calculate final bet amounts
        final_results = []
        for result in results:
            adjusted_kelly = result['kelly_fraction'] * scale_factor
            bet_amount = self.bankroll * adjusted_kelly
            
            final_results.append({
                'probability': result['probability'],
                'decimal_odds': result['decimal_odds'],
                'bet_amount': round(bet_amount, 2),
                'kelly_fraction': round(adjusted_kelly, 4),
                'scaled': scale_factor < 1.0
            })
        
        return final_results


class PortfolioManager:
    """
    Advanced portfolio management with drawdown protection and bet tracking.
    
    Features:
    - Real-time bankroll tracking
    - Drawdown monitoring and protection
    - Bet history and performance metrics
    - Risk-adjusted position sizing
    """
    
    def __init__(
        self,
        initial_bankroll: float,
        max_drawdown: float = 0.20,
        kelly_fraction: float = 0.25,
        max_single_bet: float = 0.02,
        max_daily_exposure: float = 0.10
    ):
        """
        Initialize Portfolio Manager.
        
        Args:
            initial_bankroll: Starting bankroll
            max_drawdown: Maximum acceptable drawdown (default 20%)
            kelly_fraction: Fractional Kelly to use
            max_single_bet: Maximum single bet as fraction of bankroll
            max_daily_exposure: Maximum total daily exposure
        """
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.peak_bankroll = initial_bankroll
        self.max_drawdown = max_drawdown
        self.kelly_fraction = kelly_fraction
        self.max_single_bet = max_single_bet
        self.max_daily_exposure = max_daily_exposure
        
        self.bet_history: List[BetRecord] = []
        self.daily_exposure: float = 0.0
        self.last_reset_date: datetime = datetime.now()
        
        self.kelly = KellyCriterion(
            bankroll=initial_bankroll,
            kelly_fraction=kelly_fraction,
            max_bet_percentage=max_single_bet
        )
    
    @property
    def current_drawdown(self) -> float:
        """Calculate current drawdown from peak."""
        if self.peak_bankroll <= 0:
            return 0.0
        return (self.peak_bankroll - self.current_bankroll) / self.peak_bankroll
    
    @property
    def drawdown_protection_factor(self) -> float:
        """
        Calculate position sizing reduction based on drawdown.
        
        As drawdown approaches max, reduce bet sizes to protect capital.
        """
        if self.current_drawdown >= self.max_drawdown:
            return 0.0  # Stop betting
        
        drawdown_ratio = self.current_drawdown / self.max_drawdown
        
        if drawdown_ratio < 0.5:
            return 1.0  # No reduction
        elif drawdown_ratio < 0.8:
            return 1.0 - (drawdown_ratio - 0.5) * 0.5  # Gradual reduction
        else:
            return 0.2  # Significant reduction
    
    def calculate_position_size(
        self,
        probability: float,
        decimal_odds: float,
        ev_percentage: Optional[float] = None
    ) -> Dict:
        """
        Calculate optimal position size with all risk controls.
        
        Args:
            probability: True probability of winning
            decimal_odds: Decimal odds offered
            ev_percentage: Optional pre-calculated EV percentage
            
        Returns:
            Position sizing recommendation with risk analysis
        """
        # Reset daily exposure if new day
        self._check_daily_reset()
        
        # Update Kelly calculator with current bankroll
        self.kelly.bankroll = self.current_bankroll
        
        # Get base Kelly sizing
        base_sizing = self.kelly.calculate_bet_size(probability, decimal_odds)
        
        if not base_sizing['is_positive_ev']:
            return {
                'recommended_bet': 0.0,
                'reason': 'Negative EV - no bet recommended',
                **base_sizing
            }
        
        # Apply drawdown protection
        protection_factor = self.drawdown_protection_factor
        adjusted_bet = base_sizing['bet_amount'] * protection_factor
        
        # Check daily exposure limit
        remaining_daily = (self.max_daily_exposure * self.current_bankroll) - self.daily_exposure
        adjusted_bet = min(adjusted_bet, max(0, remaining_daily))
        
        # Final position size
        final_bet = max(0, adjusted_bet)
        
        return {
            'recommended_bet': round(final_bet, 2),
            'base_kelly_bet': base_sizing['bet_amount'],
            'protection_factor': round(protection_factor, 2),
            'current_drawdown': round(self.current_drawdown * 100, 2),
            'daily_exposure_remaining': round(remaining_daily, 2),
            'current_bankroll': round(self.current_bankroll, 2),
            'peak_bankroll': round(self.peak_bankroll, 2),
            'betting_allowed': protection_factor > 0 and remaining_daily > 0,
            **base_sizing
        }
    
    def place_bet(
        self,
        bet_id: str,
        stake: float,
        decimal_odds: float,
        probability: float
    ) -> BetRecord:
        """
        Record a placed bet.
        
        Args:
            bet_id: Unique identifier for the bet
            stake: Amount wagered
            decimal_odds: Decimal odds
            probability: True probability estimate
            
        Returns:
            BetRecord object
        """
        bet = BetRecord(
            bet_id=bet_id,
            timestamp=datetime.now(),
            stake=stake,
            odds_decimal=decimal_odds,
            probability=probability
        )
        
        self.bet_history.append(bet)
        self.daily_exposure += stake
        
        return bet
    
    def resolve_bet(self, bet_id: str, outcome: str) -> Dict:
        """
        Resolve a bet and update bankroll.
        
        Args:
            bet_id: Unique identifier of bet to resolve
            outcome: "win", "lose", or "push"
            
        Returns:
            Resolution details
        """
        for bet in self.bet_history:
            if bet.bet_id == bet_id and bet.result is None:
                profit_loss = bet.resolve(outcome)
                
                # Update bankroll
                self.current_bankroll += profit_loss
                
                # Update peak if new high
                if self.current_bankroll > self.peak_bankroll:
                    self.peak_bankroll = self.current_bankroll
                
                return {
                    'bet_id': bet_id,
                    'outcome': outcome,
                    'profit_loss': profit_loss,
                    'new_bankroll': self.current_bankroll,
                    'drawdown': self.current_drawdown
                }
        
        raise ValueError(f"Bet {bet_id} not found or already resolved")
    
    def get_performance_metrics(self) -> Dict:
        """
        Calculate comprehensive performance metrics.
        
        Returns:
            Dictionary of performance statistics
        """
        resolved_bets = [b for b in self.bet_history if b.result is not None]
        
        if not resolved_bets:
            return {
                'total_bets': 0,
                'message': 'No resolved bets yet'
            }
        
        wins = [b for b in resolved_bets if b.result == 'win']
        losses = [b for b in resolved_bets if b.result == 'lose']
        
        total_wagered = sum(b.stake for b in resolved_bets)
        total_profit = sum(b.profit_loss or 0 for b in resolved_bets)
        
        return {
            'total_bets': len(resolved_bets),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': len(wins) / len(resolved_bets) if resolved_bets else 0,
            'total_wagered': round(total_wagered, 2),
            'total_profit_loss': round(total_profit, 2),
            'roi': round((total_profit / total_wagered) * 100, 2) if total_wagered > 0 else 0,
            'current_bankroll': round(self.current_bankroll, 2),
            'bankroll_growth': round(
                ((self.current_bankroll - self.initial_bankroll) / self.initial_bankroll) * 100, 2
            ),
            'peak_bankroll': round(self.peak_bankroll, 2),
            'max_drawdown_experienced': round(
                ((self.peak_bankroll - min(
                    self.current_bankroll, 
                    self.peak_bankroll
                )) / self.peak_bankroll) * 100, 2
            ) if self.peak_bankroll > 0 else 0
        }
    
    def _check_daily_reset(self):
        """Reset daily exposure if it's a new day."""
        now = datetime.now()
        if now.date() > self.last_reset_date.date():
            self.daily_exposure = 0.0
            self.last_reset_date = now


def calculate_optimal_stake(
    bankroll: float,
    probability: float,
    decimal_odds: float,
    kelly_fraction: float = 0.25
) -> float:
    """
    Quick utility function to calculate optimal stake.
    
    Args:
        bankroll: Total bankroll
        probability: True probability of winning
        decimal_odds: Decimal odds offered
        kelly_fraction: Fraction of Kelly to use
        
    Returns:
        Recommended stake amount
    """
    kelly = KellyCriterion(bankroll=bankroll, kelly_fraction=kelly_fraction)
    result = kelly.calculate_bet_size(probability, decimal_odds)
    return result['bet_amount']
