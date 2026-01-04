"""
Odds Manager Module

Manages odds data from multiple sportsbooks:
- Rate limiting for API calls
- Odds aggregation and normalization
- Sharp vs soft book classification
- Real-time odds tracking
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class BookType(Enum):
    """Classification of sportsbook types"""
    SHARP = "sharp"  # Market-making books with accurate lines
    SOFT = "soft"    # Recreational books with potential mispricings
    EXCHANGE = "exchange"  # Betting exchanges


@dataclass
class SportsbookOdds:
    """Represents odds from a single sportsbook"""
    sportsbook: str
    book_type: BookType
    event_id: str
    market_type: str  # 'moneyline', 'spread', 'total'
    selection: str
    american_odds: int
    decimal_odds: float
    spread_value: Optional[float] = None
    total_value: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    is_stale: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'sportsbook': self.sportsbook,
            'book_type': self.book_type.value,
            'event_id': self.event_id,
            'market_type': self.market_type,
            'selection': self.selection,
            'american_odds': self.american_odds,
            'decimal_odds': self.decimal_odds,
            'spread_value': self.spread_value,
            'total_value': self.total_value,
            'timestamp': self.timestamp.isoformat(),
            'is_stale': self.is_stale
        }


class RateLimiter:
    """
    Rate limiter for API calls with support for different time windows.
    
    Implements token bucket algorithm for smooth rate limiting.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_limit: int = 10
    ):
        """
        Initialize Rate Limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
            requests_per_hour: Maximum requests per hour
            burst_limit: Maximum burst of requests allowed
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_limit = burst_limit
        
        # Token bucket state
        self.tokens = burst_limit
        self.last_refill = time.time()
        
        # Request tracking
        self.minute_requests: List[float] = []
        self.hour_requests: List[float] = []
        
        # Lock for thread safety
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """
        Acquire permission to make a request.
        
        Returns:
            True if request is allowed, False if rate limited
        """
        async with self._lock:
            current_time = time.time()
            
            # Clean up old request timestamps
            self._cleanup_old_requests(current_time)
            
            # Check hourly limit
            if len(self.hour_requests) >= self.requests_per_hour:
                return False
            
            # Check minute limit
            if len(self.minute_requests) >= self.requests_per_minute:
                return False
            
            # Refill tokens
            self._refill_tokens(current_time)
            
            # Check burst limit
            if self.tokens <= 0:
                return False
            
            # Consume token and record request
            self.tokens -= 1
            self.minute_requests.append(current_time)
            self.hour_requests.append(current_time)
            
            return True
    
    async def wait_for_slot(self, timeout: float = 60.0) -> bool:
        """
        Wait until a request slot is available.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if slot acquired, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if await self.acquire():
                return True
            await asyncio.sleep(0.1)
        
        return False
    
    def get_wait_time(self) -> float:
        """
        Get estimated wait time until next available slot.
        
        Returns:
            Estimated wait time in seconds
        """
        if len(self.minute_requests) >= self.requests_per_minute:
            oldest = min(self.minute_requests)
            return max(0, 60 - (time.time() - oldest))
        return 0.0
    
    def _cleanup_old_requests(self, current_time: float):
        """Remove request timestamps older than their windows."""
        minute_cutoff = current_time - 60
        hour_cutoff = current_time - 3600
        
        self.minute_requests = [t for t in self.minute_requests if t > minute_cutoff]
        self.hour_requests = [t for t in self.hour_requests if t > hour_cutoff]
    
    def _refill_tokens(self, current_time: float):
        """Refill tokens based on time elapsed."""
        elapsed = current_time - self.last_refill
        refill_rate = self.requests_per_minute / 60  # Tokens per second
        
        new_tokens = elapsed * refill_rate
        self.tokens = min(self.burst_limit, self.tokens + new_tokens)
        self.last_refill = current_time
    
    def get_status(self) -> Dict:
        """Get current rate limiter status."""
        return {
            'tokens_available': round(self.tokens, 2),
            'minute_requests': len(self.minute_requests),
            'hour_requests': len(self.hour_requests),
            'minute_limit': self.requests_per_minute,
            'hour_limit': self.requests_per_hour,
            'wait_time': self.get_wait_time()
        }


# Default sportsbook classifications
DEFAULT_BOOK_CLASSIFICATIONS = {
    # Sharp books - market makers with accurate lines
    'pinnacle': BookType.SHARP,
    'betcris': BookType.SHARP,
    'bookmaker': BookType.SHARP,
    'circa': BookType.SHARP,
    
    # Exchanges
    'betfair': BookType.EXCHANGE,
    'matchbook': BookType.EXCHANGE,
    'smarkets': BookType.EXCHANGE,
    
    # Soft books - recreational books
    'draftkings': BookType.SOFT,
    'fanduel': BookType.SOFT,
    'betmgm': BookType.SOFT,
    'caesars': BookType.SOFT,
    'bet365': BookType.SOFT,
    'bovada': BookType.SOFT,
    'betonline': BookType.SOFT,
    'espnbet': BookType.SOFT,
    'pointsbet': BookType.SOFT,
    'wynnbet': BookType.SOFT,
    'betrivers': BookType.SOFT,
    'unibet': BookType.SOFT,
    'superbook': BookType.SOFT,
    'barstool': BookType.SOFT,
    'hard_rock': BookType.SOFT,
    'tipico': BookType.SOFT,
}


class OddsManager:
    """
    Manages odds data from multiple sportsbooks with rate limiting
    and intelligent aggregation.
    """
    
    def __init__(
        self,
        book_classifications: Optional[Dict[str, BookType]] = None,
        stale_threshold_seconds: int = 60
    ):
        """
        Initialize Odds Manager.
        
        Args:
            book_classifications: Custom book type classifications
            stale_threshold_seconds: Seconds until odds considered stale
        """
        self.book_classifications = book_classifications or DEFAULT_BOOK_CLASSIFICATIONS
        self.stale_threshold = timedelta(seconds=stale_threshold_seconds)
        
        # Odds storage: event_id -> market_type -> selection -> [SportsbookOdds]
        self.odds_cache: Dict[str, Dict[str, Dict[str, List[SportsbookOdds]]]] = {}
        
        # Rate limiters per sportsbook
        self.rate_limiters: Dict[str, RateLimiter] = {}
        
        # Callbacks for odds updates
        self.update_callbacks: List[Callable] = []
    
    def get_book_type(self, sportsbook: str) -> BookType:
        """Get the classification for a sportsbook."""
        normalized = sportsbook.lower().replace(' ', '_').replace('-', '_')
        return self.book_classifications.get(normalized, BookType.SOFT)
    
    def add_odds(
        self,
        sportsbook: str,
        event_id: str,
        market_type: str,
        selection: str,
        american_odds: int,
        spread_value: Optional[float] = None,
        total_value: Optional[float] = None
    ) -> SportsbookOdds:
        """
        Add or update odds from a sportsbook.
        
        Args:
            sportsbook: Name of the sportsbook
            event_id: Unique event identifier
            market_type: Type of market (moneyline, spread, total)
            selection: Selection name (home, away, over, under)
            american_odds: American odds value
            spread_value: Spread value (for spread bets)
            total_value: Total value (for over/under bets)
            
        Returns:
            SportsbookOdds object created
        """
        book_type = self.get_book_type(sportsbook)
        decimal_odds = self._american_to_decimal(american_odds)
        
        odds_obj = SportsbookOdds(
            sportsbook=sportsbook,
            book_type=book_type,
            event_id=event_id,
            market_type=market_type,
            selection=selection,
            american_odds=american_odds,
            decimal_odds=decimal_odds,
            spread_value=spread_value,
            total_value=total_value
        )
        
        # Initialize nested dicts if needed
        if event_id not in self.odds_cache:
            self.odds_cache[event_id] = {}
        if market_type not in self.odds_cache[event_id]:
            self.odds_cache[event_id][market_type] = {}
        if selection not in self.odds_cache[event_id][market_type]:
            self.odds_cache[event_id][market_type][selection] = []
        
        # Update or add odds
        odds_list = self.odds_cache[event_id][market_type][selection]
        
        # Remove existing odds from same sportsbook
        odds_list[:] = [o for o in odds_list if o.sportsbook != sportsbook]
        odds_list.append(odds_obj)
        
        # Trigger callbacks
        for callback in self.update_callbacks:
            callback(odds_obj)
        
        return odds_obj
    
    def get_odds(
        self,
        event_id: str,
        market_type: Optional[str] = None,
        selection: Optional[str] = None,
        book_type: Optional[BookType] = None,
        exclude_stale: bool = True
    ) -> List[SportsbookOdds]:
        """
        Get odds from cache with optional filtering.
        
        Args:
            event_id: Event to get odds for
            market_type: Filter by market type
            selection: Filter by selection
            book_type: Filter by book type
            exclude_stale: Whether to exclude stale odds
            
        Returns:
            List of matching SportsbookOdds
        """
        if event_id not in self.odds_cache:
            return []
        
        results = []
        current_time = datetime.now()
        
        for mkt_type, selections in self.odds_cache[event_id].items():
            if market_type and mkt_type != market_type:
                continue
            
            for sel, odds_list in selections.items():
                if selection and sel != selection:
                    continue
                
                for odds in odds_list:
                    # Check staleness
                    if exclude_stale:
                        age = current_time - odds.timestamp
                        if age > self.stale_threshold:
                            odds.is_stale = True
                            continue
                    
                    # Check book type
                    if book_type and odds.book_type != book_type:
                        continue
                    
                    results.append(odds)
        
        return results
    
    def get_best_odds(
        self,
        event_id: str,
        market_type: str,
        selection: str,
        prefer_sharp: bool = False
    ) -> Optional[SportsbookOdds]:
        """
        Get the best available odds for a selection.
        
        Args:
            event_id: Event identifier
            market_type: Market type
            selection: Selection to find best odds for
            prefer_sharp: Prefer sharp book odds even if not highest
            
        Returns:
            Best SportsbookOdds or None
        """
        odds = self.get_odds(event_id, market_type, selection)
        
        if not odds:
            return None
        
        if prefer_sharp:
            sharp_odds = [o for o in odds if o.book_type == BookType.SHARP]
            if sharp_odds:
                return max(sharp_odds, key=lambda o: o.decimal_odds)
        
        return max(odds, key=lambda o: o.decimal_odds)
    
    def get_sharp_consensus(
        self,
        event_id: str,
        market_type: str
    ) -> Dict[str, float]:
        """
        Get consensus fair probabilities from sharp books.
        
        Args:
            event_id: Event identifier
            market_type: Market type (moneyline, spread, total)
            
        Returns:
            Dictionary mapping selection to fair probability
        """
        from .ev_calculator import NoVigCalculator
        
        sharp_odds = self.get_odds(
            event_id, market_type, book_type=BookType.SHARP
        )
        
        if not sharp_odds:
            return {}
        
        # Group by selection
        selection_odds: Dict[str, List[int]] = {}
        for odds in sharp_odds:
            if odds.selection not in selection_odds:
                selection_odds[odds.selection] = []
            selection_odds[odds.selection].append(odds.american_odds)
        
        if len(selection_odds) < 2:
            return {}
        
        # Average odds per selection
        avg_odds = {
            sel: sum(odds_list) // len(odds_list)
            for sel, odds_list in selection_odds.items()
        }
        
        # Calculate no-vig probabilities
        selections = list(avg_odds.keys())
        odds_list = [avg_odds[s] for s in selections]
        
        try:
            fair_probs, _ = NoVigCalculator.calculate_fair_odds_from_sharp_book(odds_list)
            return dict(zip(selections, fair_probs))
        except Exception:
            return {}
    
    def get_market_consensus(
        self,
        event_id: str,
        market_type: str,
        selection: str
    ) -> Dict[str, Any]:
        """
        Get market consensus for a selection across all books.
        
        Returns:
            Dictionary with consensus metrics
        """
        odds = self.get_odds(event_id, market_type, selection)
        
        if not odds:
            return {'error': 'No odds found'}
        
        american_odds = [o.american_odds for o in odds]
        decimal_odds = [o.decimal_odds for o in odds]
        
        # Separate by book type
        sharp_decimal = [o.decimal_odds for o in odds if o.book_type == BookType.SHARP]
        soft_decimal = [o.decimal_odds for o in odds if o.book_type == BookType.SOFT]
        
        return {
            'selection': selection,
            'num_books': len(odds),
            'best_odds': max(american_odds),
            'worst_odds': min(american_odds),
            'average_odds': sum(american_odds) // len(american_odds),
            'best_decimal': max(decimal_odds),
            'worst_decimal': min(decimal_odds),
            'average_decimal': sum(decimal_odds) / len(decimal_odds),
            'sharp_average': sum(sharp_decimal) / len(sharp_decimal) if sharp_decimal else None,
            'soft_average': sum(soft_decimal) / len(soft_decimal) if soft_decimal else None,
            'books': [
                {
                    'sportsbook': o.sportsbook,
                    'book_type': o.book_type.value,
                    'american_odds': o.american_odds,
                    'decimal_odds': o.decimal_odds
                }
                for o in sorted(odds, key=lambda x: x.decimal_odds, reverse=True)
            ]
        }
    
    def get_rate_limiter(
        self,
        sportsbook: str,
        requests_per_minute: int = 60
    ) -> RateLimiter:
        """
        Get or create rate limiter for a sportsbook.
        
        Args:
            sportsbook: Sportsbook name
            requests_per_minute: Rate limit if creating new
            
        Returns:
            RateLimiter for the sportsbook
        """
        normalized = sportsbook.lower().replace(' ', '_')
        
        if normalized not in self.rate_limiters:
            self.rate_limiters[normalized] = RateLimiter(
                requests_per_minute=requests_per_minute
            )
        
        return self.rate_limiters[normalized]
    
    def on_odds_update(self, callback: Callable[[SportsbookOdds], None]):
        """Register a callback for odds updates."""
        self.update_callbacks.append(callback)
    
    def clear_event(self, event_id: str):
        """Clear all odds for an event."""
        if event_id in self.odds_cache:
            del self.odds_cache[event_id]
    
    def clear_all(self):
        """Clear all cached odds."""
        self.odds_cache.clear()
    
    def export_odds(self, event_id: str) -> Dict:
        """
        Export all odds for an event as dictionary.
        
        Args:
            event_id: Event to export
            
        Returns:
            Dictionary of all odds data
        """
        odds = self.get_odds(event_id, exclude_stale=False)
        
        return {
            'event_id': event_id,
            'timestamp': datetime.now().isoformat(),
            'odds': [o.to_dict() for o in odds]
        }
    
    def _american_to_decimal(self, american: int) -> float:
        """Convert American odds to decimal."""
        if american > 0:
            return (american / 100) + 1
        else:
            return (100 / abs(american)) + 1


# Utility functions
def create_odds_manager_from_api_data(
    api_data: List[Dict],
    event_id: str
) -> OddsManager:
    """
    Create and populate OddsManager from API response data.
    
    Args:
        api_data: List of odds dictionaries from API
        event_id: Event identifier
        
    Returns:
        Populated OddsManager
    """
    manager = OddsManager()
    
    for odds_data in api_data:
        sportsbook = odds_data.get('sportsbook', odds_data.get('provider', 'unknown'))
        
        # Add moneyline odds
        if 'moneyline_home' in odds_data:
            manager.add_odds(
                sportsbook=sportsbook,
                event_id=event_id,
                market_type='moneyline',
                selection='home',
                american_odds=odds_data['moneyline_home']
            )
        
        if 'moneyline_away' in odds_data:
            manager.add_odds(
                sportsbook=sportsbook,
                event_id=event_id,
                market_type='moneyline',
                selection='away',
                american_odds=odds_data['moneyline_away']
            )
        
        # Add spread odds
        if 'spread' in odds_data:
            spread = odds_data['spread']
            spread_odds = odds_data.get('spread_odds', -110)
            
            manager.add_odds(
                sportsbook=sportsbook,
                event_id=event_id,
                market_type='spread',
                selection='home',
                american_odds=spread_odds,
                spread_value=spread
            )
        
        # Add total odds
        if 'total' in odds_data or 'over_under' in odds_data:
            total = odds_data.get('total', odds_data.get('over_under'))
            over_odds = odds_data.get('over_odds', -110)
            under_odds = odds_data.get('under_odds', -110)
            
            manager.add_odds(
                sportsbook=sportsbook,
                event_id=event_id,
                market_type='total',
                selection='over',
                american_odds=over_odds,
                total_value=total
            )
            
            manager.add_odds(
                sportsbook=sportsbook,
                event_id=event_id,
                market_type='total',
                selection='under',
                american_odds=under_odds,
                total_value=total
            )
    
    return manager
