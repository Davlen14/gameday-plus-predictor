"""
EV Calculator Module

Core expected value calculations including:
- Odds conversion (American, Decimal, Fractional)
- Implied probability calculation
- No-vig fair line calculation
- Expected value computation
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Union
import math


@dataclass
class OddsData:
    """Represents odds data from a sportsbook"""
    american: Optional[int] = None
    decimal: Optional[float] = None
    fractional: Optional[Tuple[int, int]] = None
    implied_probability: Optional[float] = None


class OddsConverter:
    """
    Utility class for converting between different odds formats.
    
    Supports:
    - American odds (+150, -110, etc.)
    - Decimal odds (2.50, 1.91, etc.)
    - Fractional odds (3/2, 10/11, etc.)
    - Implied probability (0.40, 0.524, etc.)
    """
    
    @staticmethod
    def american_to_decimal(american_odds: int) -> float:
        """
        Convert American odds to decimal odds.
        
        Args:
            american_odds: American odds value (e.g., +150, -110)
            
        Returns:
            Decimal odds value
            
        Examples:
            >>> OddsConverter.american_to_decimal(150)
            2.5
            >>> OddsConverter.american_to_decimal(-110)
            1.909090909...
        """
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    
    @staticmethod
    def decimal_to_american(decimal_odds: float) -> int:
        """
        Convert decimal odds to American odds.
        
        Args:
            decimal_odds: Decimal odds value (e.g., 2.50)
            
        Returns:
            American odds value (rounded to integer)
        """
        if decimal_odds >= 2.0:
            return int(round((decimal_odds - 1) * 100))
        else:
            return int(round(-100 / (decimal_odds - 1)))
    
    @staticmethod
    def american_to_implied_probability(american_odds: int) -> float:
        """
        Convert American odds to implied probability.
        
        Args:
            american_odds: American odds value
            
        Returns:
            Implied probability as decimal (0-1)
            
        Examples:
            >>> OddsConverter.american_to_implied_probability(100)
            0.5
            >>> OddsConverter.american_to_implied_probability(-110)
            0.5238...
        """
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)
    
    @staticmethod
    def implied_probability_to_american(probability: float) -> int:
        """
        Convert implied probability to American odds.
        
        Args:
            probability: Probability as decimal (0-1)
            
        Returns:
            American odds value
        """
        if probability <= 0 or probability >= 1:
            raise ValueError("Probability must be between 0 and 1 (exclusive)")
        
        if probability < 0.5:
            return int(round((100 / probability) - 100))
        else:
            return int(round(-100 * probability / (1 - probability)))
    
    @staticmethod
    def decimal_to_implied_probability(decimal_odds: float) -> float:
        """
        Convert decimal odds to implied probability.
        
        Args:
            decimal_odds: Decimal odds value
            
        Returns:
            Implied probability as decimal (0-1)
        """
        if decimal_odds <= 1:
            raise ValueError("Decimal odds must be greater than 1")
        return 1 / decimal_odds
    
    @staticmethod
    def implied_probability_to_decimal(probability: float) -> float:
        """
        Convert implied probability to decimal odds.
        
        Args:
            probability: Probability as decimal (0-1)
            
        Returns:
            Decimal odds value
        """
        if probability <= 0 or probability >= 1:
            raise ValueError("Probability must be between 0 and 1 (exclusive)")
        return 1 / probability
    
    @staticmethod
    def fractional_to_decimal(numerator: int, denominator: int) -> float:
        """
        Convert fractional odds to decimal odds.
        
        Args:
            numerator: Top number of fraction
            denominator: Bottom number of fraction
            
        Returns:
            Decimal odds value
        """
        return (numerator / denominator) + 1
    
    @staticmethod
    def decimal_to_fractional(decimal_odds: float) -> Tuple[int, int]:
        """
        Convert decimal odds to fractional odds (approximate).
        
        Args:
            decimal_odds: Decimal odds value
            
        Returns:
            Tuple of (numerator, denominator)
        """
        from math import gcd
        
        fractional = decimal_odds - 1
        # Convert to fraction with reasonable denominator
        denominator = 100
        numerator = int(round(fractional * denominator))
        
        # Simplify fraction
        common_divisor = gcd(numerator, denominator)
        return (numerator // common_divisor, denominator // common_divisor)


class NoVigCalculator:
    """
    Calculator for removing vig (vigorish/juice) from betting lines
    to determine fair/true probabilities.
    """
    
    @staticmethod
    def calculate_total_implied_probability(implied_probs: List[float]) -> float:
        """
        Calculate total implied probability (includes vig).
        
        Args:
            implied_probs: List of implied probabilities for all outcomes
            
        Returns:
            Total implied probability (>1.0 indicates vig)
        """
        return sum(implied_probs)
    
    @staticmethod
    def calculate_vig_percentage(implied_probs: List[float]) -> float:
        """
        Calculate the vig percentage from implied probabilities.
        
        Args:
            implied_probs: List of implied probabilities for all outcomes
            
        Returns:
            Vig as percentage (e.g., 4.5 for 4.5% vig)
        """
        total = sum(implied_probs)
        return (total - 1.0) * 100
    
    @staticmethod
    def remove_vig_multiplicative(implied_probs: List[float]) -> List[float]:
        """
        Remove vig using multiplicative method (most common).
        
        Each probability is divided by the total to normalize to 100%.
        
        Args:
            implied_probs: List of implied probabilities with vig
            
        Returns:
            List of fair probabilities (sum to 1.0)
        """
        total = sum(implied_probs)
        if total == 0:
            raise ValueError("Total implied probability cannot be zero")
        return [prob / total for prob in implied_probs]
    
    @staticmethod
    def remove_vig_power_method(implied_probs: List[float], iterations: int = 100) -> List[float]:
        """
        Remove vig using the power method (more accurate for large vig).
        
        This method iteratively finds the exponent that makes probabilities sum to 1.
        
        Args:
            implied_probs: List of implied probabilities with vig
            iterations: Number of iterations for convergence
            
        Returns:
            List of fair probabilities
        """
        if len(implied_probs) != 2:
            # Fall back to multiplicative for non-binary outcomes
            return NoVigCalculator.remove_vig_multiplicative(implied_probs)
        
        # Binary search for the correct exponent
        low, high = 0.0, 2.0
        
        for _ in range(iterations):
            mid = (low + high) / 2
            adjusted = [p ** mid for p in implied_probs]
            total = sum(adjusted)
            
            if abs(total - 1.0) < 1e-10:
                break
            elif total > 1.0:
                low = mid
            else:
                high = mid
        
        return [p ** mid / sum([p ** mid for p in implied_probs]) for p in implied_probs]
    
    @staticmethod
    def calculate_fair_odds_from_sharp_book(
        sharp_odds: List[int],
        method: str = "multiplicative"
    ) -> Tuple[List[float], List[int]]:
        """
        Calculate fair odds from a sharp book's lines.
        
        Args:
            sharp_odds: List of American odds from sharp book
            method: Vig removal method ("multiplicative" or "power")
            
        Returns:
            Tuple of (fair_probabilities, fair_american_odds)
        """
        # Convert to implied probabilities
        converter = OddsConverter()
        implied_probs = [
            converter.american_to_implied_probability(odds)
            for odds in sharp_odds
        ]
        
        # Remove vig
        if method == "power":
            fair_probs = NoVigCalculator.remove_vig_power_method(implied_probs)
        else:
            fair_probs = NoVigCalculator.remove_vig_multiplicative(implied_probs)
        
        # Convert back to American odds
        fair_odds = [
            converter.implied_probability_to_american(prob)
            for prob in fair_probs
        ]
        
        return fair_probs, fair_odds


class EVCalculator:
    """
    Core Expected Value calculator for sports betting.
    
    Expected Value (EV) represents the average amount you can expect to win
    or lose per bet over the long run. Positive EV (+EV) bets have a
    mathematical edge over the sportsbook.
    """
    
    def __init__(self, min_ev_threshold: float = 0.01):
        """
        Initialize EV Calculator.
        
        Args:
            min_ev_threshold: Minimum EV percentage to consider a bet +EV (default 1%)
        """
        self.min_ev_threshold = min_ev_threshold
        self.converter = OddsConverter()
        self.no_vig = NoVigCalculator()
    
    def calculate_ev(
        self,
        true_probability: float,
        decimal_odds: Optional[float] = None,
        american_odds: Optional[int] = None,
        stake: float = 100.0
    ) -> Dict[str, float]:
        """
        Calculate Expected Value for a bet.
        
        EV = (True Probability × Potential Profit) - (Loss Probability × Stake)
        
        Args:
            true_probability: The true/fair probability of winning (0-1)
            decimal_odds: Decimal odds offered (provide this OR american_odds)
            american_odds: American odds offered (provide this OR decimal_odds)
            stake: Bet amount for calculation (default $100)
            
        Returns:
            Dictionary with EV calculations:
            - ev_amount: Expected value in dollars
            - ev_percentage: Expected value as percentage of stake
            - is_plus_ev: Boolean indicating if bet is +EV
            - edge_percentage: Your edge over the book
        """
        # Convert odds to decimal if needed
        if decimal_odds is None and american_odds is None:
            raise ValueError("Must provide either decimal_odds or american_odds")
        
        if decimal_odds is None:
            decimal_odds = self.converter.american_to_decimal(american_odds)
        
        # Calculate implied probability from odds
        implied_prob = self.converter.decimal_to_implied_probability(decimal_odds)
        
        # Calculate potential profit
        potential_profit = stake * (decimal_odds - 1)
        
        # Calculate EV
        # EV = (prob_win × profit) - (prob_lose × stake)
        prob_lose = 1 - true_probability
        ev_amount = (true_probability * potential_profit) - (prob_lose * stake)
        ev_percentage = ev_amount / stake
        
        # Calculate edge (true prob - implied prob)
        edge_percentage = true_probability - implied_prob
        
        return {
            "ev_amount": round(ev_amount, 2),
            "ev_percentage": round(ev_percentage * 100, 2),
            "is_plus_ev": ev_percentage > self.min_ev_threshold,
            "edge_percentage": round(edge_percentage * 100, 2),
            "true_probability": round(true_probability * 100, 2),
            "implied_probability": round(implied_prob * 100, 2),
            "decimal_odds": round(decimal_odds, 3),
            "potential_profit": round(potential_profit, 2),
            "stake": stake
        }
    
    def calculate_ev_from_sharp_line(
        self,
        sharp_odds: List[int],
        soft_odds: int,
        selection_index: int = 0,
        stake: float = 100.0,
        vig_removal_method: str = "multiplicative"
    ) -> Dict[str, float]:
        """
        Calculate EV by comparing soft book odds to sharp book fair line.
        
        This is the primary method used by professional bettors to identify +EV.
        
        Args:
            sharp_odds: List of American odds from sharp book for all outcomes
            soft_odds: American odds from soft book for the selection
            selection_index: Index of the selection in sharp_odds (0 or 1 for binary)
            stake: Bet amount
            vig_removal_method: Method to remove vig ("multiplicative" or "power")
            
        Returns:
            Dictionary with EV calculations
        """
        # Get fair probabilities from sharp book
        fair_probs, fair_odds = self.no_vig.calculate_fair_odds_from_sharp_book(
            sharp_odds, vig_removal_method
        )
        
        true_probability = fair_probs[selection_index]
        
        # Calculate EV using soft book odds
        return self.calculate_ev(
            true_probability=true_probability,
            american_odds=soft_odds,
            stake=stake
        )
    
    def find_plus_ev_opportunities(
        self,
        sharp_odds: List[int],
        soft_book_odds: Dict[str, List[int]],
        min_ev: Optional[float] = None,
        stake: float = 100.0
    ) -> List[Dict]:
        """
        Find all +EV opportunities across multiple soft books.
        
        Args:
            sharp_odds: List of American odds from sharp book
            soft_book_odds: Dict mapping book name to list of odds
            min_ev: Minimum EV percentage to include (default uses instance threshold)
            stake: Bet amount for calculations
            
        Returns:
            List of +EV opportunities sorted by EV percentage
        """
        if min_ev is None:
            min_ev = self.min_ev_threshold
        
        opportunities = []
        
        # Get fair probabilities
        fair_probs, _ = self.no_vig.calculate_fair_odds_from_sharp_book(sharp_odds)
        
        for book_name, odds_list in soft_book_odds.items():
            for i, soft_odds in enumerate(odds_list):
                ev_result = self.calculate_ev(
                    true_probability=fair_probs[i],
                    american_odds=soft_odds,
                    stake=stake
                )
                
                if ev_result["ev_percentage"] / 100 >= min_ev:
                    opportunities.append({
                        "sportsbook": book_name,
                        "selection": i,
                        "soft_odds": soft_odds,
                        "sharp_fair_prob": fair_probs[i],
                        **ev_result
                    })
        
        # Sort by EV percentage descending
        opportunities.sort(key=lambda x: x["ev_percentage"], reverse=True)
        
        return opportunities
    
    def calculate_clv(
        self,
        bet_odds: int,
        closing_odds: int
    ) -> Dict[str, float]:
        """
        Calculate Closing Line Value (CLV).
        
        CLV measures how much better your bet was compared to the closing line.
        Positive CLV indicates beating the market.
        
        Args:
            bet_odds: American odds at time of bet
            closing_odds: American odds at market close
            
        Returns:
            Dictionary with CLV calculations
        """
        bet_implied = self.converter.american_to_implied_probability(bet_odds)
        closing_implied = self.converter.american_to_implied_probability(closing_odds)
        
        clv_percentage = (closing_implied - bet_implied) * 100
        
        return {
            "clv_percentage": round(clv_percentage, 2),
            "bet_implied_prob": round(bet_implied * 100, 2),
            "closing_implied_prob": round(closing_implied * 100, 2),
            "beat_close": clv_percentage > 0
        }


# Standalone utility functions for quick calculations
def calculate_implied_probability(american_odds: int) -> float:
    """Quick utility to calculate implied probability from American odds."""
    return OddsConverter.american_to_implied_probability(american_odds)


def calculate_fair_probability(odds_list: List[int]) -> List[float]:
    """Quick utility to calculate fair probabilities from a list of American odds."""
    fair_probs, _ = NoVigCalculator.calculate_fair_odds_from_sharp_book(odds_list)
    return fair_probs


def is_plus_ev(sharp_odds: List[int], soft_odds: int, selection: int = 0, threshold: float = 0.01) -> bool:
    """Quick check if a bet is +EV based on sharp vs soft odds."""
    calc = EVCalculator(min_ev_threshold=threshold)
    result = calc.calculate_ev_from_sharp_line(sharp_odds, soft_odds, selection)
    return result["is_plus_ev"]
