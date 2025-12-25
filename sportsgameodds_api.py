#!/usr/bin/env python3
"""
Sports Game Odds API Integration for College Football (CFB)
Provides real-time odds, EV calculations, and betting analysis for CFB games.

API Documentation: https://sportsgameodds.com/docs/
Features:
- 3k+ odds markets including spreads, moneylines, over/unders, player props
- 80+ sportsbooks with unified odds formats
- Sub-minute updates for live data
- EV (Expected Value) calculations for CFB betting
"""

import os
import time
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_DELAY = 1.0  # seconds between requests


@dataclass
class OddsLine:
    """Represents a single betting line from a sportsbook"""
    bookmaker: str
    market_type: str  # 'spread', 'moneyline', 'total'
    line: Optional[float] = None  # spread or total line
    odds: int = 0  # American odds
    side: str = ""  # 'home', 'away', 'over', 'under'
    timestamp: Optional[datetime] = None


@dataclass
class PlayerProp:
    """Represents a player prop betting line"""
    player_name: str
    player_id: str
    prop_type: str  # 'passing_yards', 'rushing_yards', 'receiving_yards', etc.
    line: float
    over_odds: int
    under_odds: int
    bookmaker: str
    game_id: str
    team: Optional[str] = None


@dataclass
class EVBet:
    """Represents a bet with calculated Expected Value"""
    game_id: str
    bet_type: str  # 'spread', 'moneyline', 'total', 'player_prop'
    selection: str  # team name or over/under
    line: Optional[float] = None
    odds: int = 0
    bookmaker: str = ""
    model_probability: float = 0.0  # from our prediction engine
    implied_probability: float = 0.0  # from odds
    ev_percentage: float = 0.0  # Expected Value as percentage
    kelly_fraction: float = 0.0  # Kelly Criterion stake suggestion
    edge: float = 0.0  # absolute edge
    confidence: str = "Low"  # Low, Medium, High, Very High


@dataclass
class CFBGame:
    """Represents a College Football game with odds data"""
    event_id: str
    home_team: str
    away_team: str
    start_time: datetime
    home_team_id: Optional[str] = None
    away_team_id: Optional[str] = None
    spread_lines: List[OddsLine] = field(default_factory=list)
    moneyline_lines: List[OddsLine] = field(default_factory=list)
    total_lines: List[OddsLine] = field(default_factory=list)
    player_props: List[PlayerProp] = field(default_factory=list)
    consensus_spread: Optional[float] = None
    consensus_total: Optional[float] = None
    consensus_home_ml: Optional[int] = None
    consensus_away_ml: Optional[int] = None


class SportsGameOddsClient:
    """
    Client for SportsGameOdds API to fetch CFB odds and calculate EV.
    
    API Features Used:
    - /v2/events - Get CFB games and events
    - /v2/odds - Get odds for specific events
    - /v2/teams - Get CFB team data
    - /v2/players - Get player data for props
    """
    
    BASE_URL = "https://api.sportsgameodds.com/v2"
    LEAGUE_ID = "NCAAF"  # College Football
    SPORT_ID = "FOOTBALL"
    
    # Standard vig assumption for fair odds calculation
    STANDARD_VIG = 0.0435  # 4.35% per side (typical -110/-110)
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Sports Game Odds API client.
        
        Args:
            api_key: API key from SportsGameOdds (or from env var SPORTSGAMEODDS_API_KEY)
        """
        self.api_key = api_key or os.getenv("SPORTSGAMEODDS_API_KEY")
        if not self.api_key:
            logger.warning("SPORTSGAMEODDS_API_KEY not set - using demo mode")
            self.demo_mode = True
        else:
            self.demo_mode = False
            
        self.last_request_time = 0
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
            
    async def _rate_limit_async(self):
        """Enforce rate limiting between requests (async version)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < RATE_LIMIT_DELAY:
            await asyncio.sleep(RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make API request with rate limiting and error handling.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dict
        """
        if self.demo_mode:
            return self._get_demo_data(endpoint, params)
            
        await self._rate_limit_async()
        await self._ensure_session()
        
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.get(url, headers=headers, params=params or {}) as response:
                if response.status == 401:
                    raise ValueError("Invalid API key for SportsGameOdds")
                elif response.status == 429:
                    raise ValueError("Rate limit exceeded. Wait before making more requests.")
                elif response.status >= 400:
                    text = await response.text()
                    raise ValueError(f"API error {response.status}: {text}")
                    
                data = await response.json()
                return data
                
        except aiohttp.ClientError as e:
            raise ValueError(f"Request failed: {str(e)}")
            
    def _get_demo_data(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Return demo data when no API key is available"""
        if "events" in endpoint:
            return {
                "success": True,
                "data": [
                    {
                        "eventID": "demo_event_1",
                        "homeTeam": {"teamID": "OHIO_STATE_NCAAF", "name": "Ohio State"},
                        "awayTeam": {"teamID": "MICHIGAN_NCAAF", "name": "Michigan"},
                        "startTime": datetime.now(timezone.utc).isoformat(),
                        "leagueID": "NCAAF",
                        "status": "scheduled"
                    }
                ]
            }
        elif "odds" in endpoint:
            return {
                "success": True,
                "data": {
                    "event": {
                        "eventID": "demo_event_1",
                        "homeTeam": {"name": "Ohio State"},
                        "awayTeam": {"name": "Michigan"}
                    },
                    "odds": {
                        "spread-home-game": {
                            "oddID": "spread-home-game",
                            "closeSpread": -7.5,
                            "closeOdds": -110,
                            "bookmakerID": "draftkings"
                        },
                        "spread-away-game": {
                            "oddID": "spread-away-game",
                            "closeSpread": 7.5,
                            "closeOdds": -110,
                            "bookmakerID": "draftkings"
                        },
                        "total-over-game": {
                            "oddID": "total-over-game",
                            "closeOverUnder": 47.5,
                            "closeOdds": -110,
                            "bookmakerID": "draftkings"
                        },
                        "total-under-game": {
                            "oddID": "total-under-game",
                            "closeOverUnder": 47.5,
                            "closeOdds": -110,
                            "bookmakerID": "draftkings"
                        },
                        "moneyline-home-game": {
                            "oddID": "moneyline-home-game",
                            "closeOdds": -280,
                            "bookmakerID": "draftkings"
                        },
                        "moneyline-away-game": {
                            "oddID": "moneyline-away-game",
                            "closeOdds": +240,
                            "bookmakerID": "draftkings"
                        }
                    }
                }
            }
        return {"success": True, "data": []}
        
    # ============================================
    # Core API Methods
    # ============================================
    
    async def get_cfb_events(
        self,
        starts_after: Optional[str] = None,
        starts_before: Optional[str] = None,
        include_odds: bool = True,
        limit: int = 50
    ) -> List[CFBGame]:
        """
        Get upcoming CFB games with odds.
        
        Args:
            starts_after: ISO date string for earliest start time
            starts_before: ISO date string for latest start time
            include_odds: Whether to fetch odds for each game
            limit: Maximum number of games to return
            
        Returns:
            List of CFBGame objects with odds data
        """
        params = {
            "leagueID": self.LEAGUE_ID,
            "limit": min(limit, 100)
        }
        
        if starts_after:
            params["startsAfter"] = starts_after
        if starts_before:
            params["startsBefore"] = starts_before
            
        try:
            response = await self._make_request("events", params)
            events = response.get("data", [])
            
            games = []
            for event in events:
                game = self._parse_event(event)
                if game:
                    # Fetch odds for this game if requested
                    if include_odds:
                        try:
                            odds_data = await self._make_request(f"odds/event/{game.event_id}")
                            self._parse_odds_into_game(game, odds_data)
                        except Exception as e:
                            logger.warning(f"Could not fetch odds for {game.event_id}: {e}")
                    games.append(game)
                    
            return games
            
        except Exception as e:
            logger.error(f"Error fetching CFB events: {e}")
            return []
            
    def _parse_event(self, event: Dict) -> Optional[CFBGame]:
        """Parse raw event data into CFBGame object"""
        try:
            home_team_data = event.get("homeTeam", {})
            away_team_data = event.get("awayTeam", {})
            
            start_time_str = event.get("startTime", "")
            try:
                start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                start_time = datetime.now(timezone.utc)
                
            return CFBGame(
                event_id=event.get("eventID", ""),
                home_team=home_team_data.get("name", "Unknown"),
                away_team=away_team_data.get("name", "Unknown"),
                start_time=start_time,
                home_team_id=home_team_data.get("teamID"),
                away_team_id=away_team_data.get("teamID")
            )
        except Exception as e:
            logger.warning(f"Error parsing event: {e}")
            return None
            
    def _parse_odds_into_game(self, game: CFBGame, odds_data: Dict):
        """Parse odds data and add to game object"""
        data = odds_data.get("data", {})
        odds = data.get("odds", {})
        
        if not odds:
            return
            
        spreads = []
        moneylines = []
        totals = []
        
        for odd_id, odd_obj in odds.items():
            bookmaker = odd_obj.get("bookmakerID", "unknown")
            
            # Parse spread lines
            if "spread" in odd_id.lower():
                spread_val = odd_obj.get("closeSpread") or odd_obj.get("openSpread")
                odds_val = odd_obj.get("closeOdds") or odd_obj.get("openOdds", -110)
                if spread_val is not None:
                    side = "home" if "home" in odd_id.lower() else "away"
                    spreads.append(OddsLine(
                        bookmaker=bookmaker,
                        market_type="spread",
                        line=spread_val,
                        odds=odds_val,
                        side=side
                    ))
                    
            # Parse moneyline lines
            elif "moneyline" in odd_id.lower():
                odds_val = odd_obj.get("closeOdds") or odd_obj.get("openOdds")
                if odds_val is not None:
                    side = "home" if "home" in odd_id.lower() else "away"
                    moneylines.append(OddsLine(
                        bookmaker=bookmaker,
                        market_type="moneyline",
                        odds=odds_val,
                        side=side
                    ))
                    
            # Parse total lines
            elif "total" in odd_id.lower() or "over" in odd_id.lower() or "under" in odd_id.lower():
                total_val = odd_obj.get("closeOverUnder") or odd_obj.get("openOverUnder")
                odds_val = odd_obj.get("closeOdds") or odd_obj.get("openOdds", -110)
                if total_val is not None:
                    side = "over" if "over" in odd_id.lower() else "under"
                    totals.append(OddsLine(
                        bookmaker=bookmaker,
                        market_type="total",
                        line=total_val,
                        odds=odds_val,
                        side=side
                    ))
                    
        game.spread_lines = spreads
        game.moneyline_lines = moneylines
        game.total_lines = totals
        
        # Calculate consensus lines
        if spreads:
            home_spreads = [s.line for s in spreads if s.side == "home" and s.line is not None]
            if home_spreads:
                game.consensus_spread = sum(home_spreads) / len(home_spreads)
                
        if totals:
            total_vals = [t.line for t in totals if t.line is not None]
            if total_vals:
                game.consensus_total = sum(total_vals) / len(total_vals)
                
        if moneylines:
            home_mls = [m.odds for m in moneylines if m.side == "home"]
            away_mls = [m.odds for m in moneylines if m.side == "away"]
            if home_mls:
                game.consensus_home_ml = int(sum(home_mls) / len(home_mls))
            if away_mls:
                game.consensus_away_ml = int(sum(away_mls) / len(away_mls))
                
    # ============================================
    # EV Calculation Methods
    # ============================================
    
    @staticmethod
    def american_to_implied_probability(american_odds: int) -> float:
        """
        Convert American odds to implied probability.
        
        Args:
            american_odds: American format odds (e.g., -110, +150)
            
        Returns:
            Implied probability as decimal (0-1)
        """
        if american_odds < 0:
            return abs(american_odds) / (abs(american_odds) + 100)
        else:
            return 100 / (american_odds + 100)
            
    @staticmethod
    def american_to_decimal(american_odds: int) -> float:
        """
        Convert American odds to decimal odds.
        
        Args:
            american_odds: American format odds
            
        Returns:
            Decimal odds
        """
        if american_odds < 0:
            return 1 + (100 / abs(american_odds))
        else:
            return 1 + (american_odds / 100)
            
    @staticmethod
    def remove_vig(implied_prob: float, opposing_implied: float) -> float:
        """
        Remove vig from implied probability to get fair probability.
        
        Args:
            implied_prob: Implied probability from odds
            opposing_implied: Implied probability of the opposing outcome
            
        Returns:
            Fair (no-vig) probability
        """
        total_implied = implied_prob + opposing_implied
        if total_implied == 0:
            return 0.5
        return implied_prob / total_implied
        
    def calculate_ev(
        self,
        model_probability: float,
        american_odds: int,
        stake: float = 100
    ) -> Tuple[float, float]:
        """
        Calculate Expected Value for a bet.
        
        Args:
            model_probability: Your model's estimated true probability (0-1)
            american_odds: The betting odds offered
            stake: Amount wagered (default $100)
            
        Returns:
            Tuple of (EV amount, EV percentage)
        """
        decimal_odds = self.american_to_decimal(american_odds)
        
        # Expected Value = (Probability of Win * Potential Profit) - (Probability of Loss * Stake)
        potential_profit = stake * (decimal_odds - 1)
        ev_amount = (model_probability * potential_profit) - ((1 - model_probability) * stake)
        ev_percentage = (ev_amount / stake) * 100
        
        return ev_amount, ev_percentage
        
    def calculate_kelly_fraction(
        self,
        model_probability: float,
        american_odds: int,
        bankroll_fraction: float = 0.25  # Quarter Kelly for safety
    ) -> float:
        """
        Calculate Kelly Criterion optimal bet size.
        
        Args:
            model_probability: Your model's estimated true probability
            american_odds: The betting odds offered
            bankroll_fraction: Fraction of full Kelly to use (0.25 = Quarter Kelly)
            
        Returns:
            Optimal bet size as fraction of bankroll
        """
        decimal_odds = self.american_to_decimal(american_odds)
        b = decimal_odds - 1  # Net odds received on a win
        p = model_probability
        q = 1 - p
        
        # Kelly formula: f* = (bp - q) / b
        if b <= 0:
            return 0
            
        kelly = (b * p - q) / b
        
        # Apply fraction and ensure non-negative
        return max(0, kelly * bankroll_fraction)
        
    def find_ev_bets(
        self,
        game: CFBGame,
        model_spread: float,
        model_total: float,
        model_home_win_prob: float,
        min_ev_threshold: float = 2.0  # Minimum EV% to consider
    ) -> List[EVBet]:
        """
        Find positive EV bets for a CFB game.
        
        Args:
            game: CFBGame object with odds data
            model_spread: Your model's predicted spread (positive = home favored)
            model_total: Your model's predicted total
            model_home_win_prob: Your model's probability that home team wins (0-1)
            min_ev_threshold: Minimum EV% to include in results
            
        Returns:
            List of EVBet objects sorted by EV% descending
        """
        ev_bets = []
        
        # Analyze spread bets
        for spread_line in game.spread_lines:
            # Calculate model probability of covering
            if spread_line.side == "home":
                # Home team covers if they win by more than the spread
                # If spread is -7.5, home needs to win by 8+
                points_needed = -spread_line.line if spread_line.line else 0
                model_margin = model_spread
                cover_prob = self._spread_cover_probability(model_margin, points_needed)
            else:
                # Away team covers if they lose by less than spread or win
                points_buffer = spread_line.line if spread_line.line else 0
                model_margin = -model_spread
                cover_prob = self._spread_cover_probability(model_margin, -points_buffer)
                
            ev_amount, ev_pct = self.calculate_ev(cover_prob, spread_line.odds)
            
            if ev_pct >= min_ev_threshold:
                kelly = self.calculate_kelly_fraction(cover_prob, spread_line.odds)
                implied_prob = self.american_to_implied_probability(spread_line.odds)
                
                ev_bets.append(EVBet(
                    game_id=game.event_id,
                    bet_type="spread",
                    selection=f"{game.home_team if spread_line.side == 'home' else game.away_team} {spread_line.line:+.1f}",
                    line=spread_line.line,
                    odds=spread_line.odds,
                    bookmaker=spread_line.bookmaker,
                    model_probability=cover_prob,
                    implied_probability=implied_prob,
                    ev_percentage=ev_pct,
                    kelly_fraction=kelly,
                    edge=cover_prob - implied_prob,
                    confidence=self._get_confidence_level(ev_pct)
                ))
                
        # Analyze moneyline bets
        for ml_line in game.moneyline_lines:
            if ml_line.side == "home":
                win_prob = model_home_win_prob
                team_name = game.home_team
            else:
                win_prob = 1 - model_home_win_prob
                team_name = game.away_team
                
            ev_amount, ev_pct = self.calculate_ev(win_prob, ml_line.odds)
            
            if ev_pct >= min_ev_threshold:
                kelly = self.calculate_kelly_fraction(win_prob, ml_line.odds)
                implied_prob = self.american_to_implied_probability(ml_line.odds)
                
                ev_bets.append(EVBet(
                    game_id=game.event_id,
                    bet_type="moneyline",
                    selection=f"{team_name} ML",
                    odds=ml_line.odds,
                    bookmaker=ml_line.bookmaker,
                    model_probability=win_prob,
                    implied_probability=implied_prob,
                    ev_percentage=ev_pct,
                    kelly_fraction=kelly,
                    edge=win_prob - implied_prob,
                    confidence=self._get_confidence_level(ev_pct)
                ))
                
        # Analyze total bets
        for total_line in game.total_lines:
            if total_line.line is None:
                continue
                
            if total_line.side == "over":
                # Model probability that total goes over
                over_prob = self._total_probability(model_total, total_line.line, "over")
                selection = f"OVER {total_line.line}"
            else:
                # Model probability that total goes under
                over_prob = self._total_probability(model_total, total_line.line, "under")
                selection = f"UNDER {total_line.line}"
                
            ev_amount, ev_pct = self.calculate_ev(over_prob, total_line.odds)
            
            if ev_pct >= min_ev_threshold:
                kelly = self.calculate_kelly_fraction(over_prob, total_line.odds)
                implied_prob = self.american_to_implied_probability(total_line.odds)
                
                ev_bets.append(EVBet(
                    game_id=game.event_id,
                    bet_type="total",
                    selection=selection,
                    line=total_line.line,
                    odds=total_line.odds,
                    bookmaker=total_line.bookmaker,
                    model_probability=over_prob,
                    implied_probability=implied_prob,
                    ev_percentage=ev_pct,
                    kelly_fraction=kelly,
                    edge=over_prob - implied_prob,
                    confidence=self._get_confidence_level(ev_pct)
                ))
                
        # Sort by EV% descending
        ev_bets.sort(key=lambda x: x.ev_percentage, reverse=True)
        
        return ev_bets
        
    def _spread_cover_probability(
        self,
        predicted_margin: float,
        points_needed: float,
        std_dev: float = 13.5  # Historical CFB spread standard deviation
    ) -> float:
        """
        Calculate probability of covering a spread using normal distribution.
        
        Args:
            predicted_margin: Model's predicted margin (positive = team wins by X)
            points_needed: Points team needs to win by to cover
            std_dev: Standard deviation of prediction error
            
        Returns:
            Probability of covering (0-1)
        """
        # Z-score: how many standard deviations away from covering
        z = (predicted_margin - points_needed) / std_dev
        
        # CDF of standard normal distribution
        return self._normal_cdf(z)
        
    def _total_probability(
        self,
        predicted_total: float,
        line: float,
        direction: str,  # "over" or "under"
        std_dev: float = 10.0  # Historical CFB total standard deviation
    ) -> float:
        """
        Calculate probability of over/under hitting.
        
        Args:
            predicted_total: Model's predicted total
            line: Sportsbook's total line
            direction: "over" or "under"
            std_dev: Standard deviation of prediction error
            
        Returns:
            Probability of hitting (0-1)
        """
        z = (predicted_total - line) / std_dev
        
        if direction == "over":
            return self._normal_cdf(z)
        else:
            return 1 - self._normal_cdf(z)
            
    @staticmethod
    def _normal_cdf(z: float) -> float:
        """Standard normal cumulative distribution function"""
        return (1 + math.erf(z / math.sqrt(2))) / 2
        
    @staticmethod
    def _get_confidence_level(ev_pct: float) -> str:
        """Determine confidence level based on EV percentage"""
        if ev_pct >= 10:
            return "Very High"
        elif ev_pct >= 5:
            return "High"
        elif ev_pct >= 3:
            return "Medium"
        else:
            return "Low"
            
    # ============================================
    # Utility Methods
    # ============================================
    
    async def get_cfb_teams(self) -> List[Dict]:
        """Get all CFB teams from API"""
        try:
            response = await self._make_request("teams", {"leagueID": self.LEAGUE_ID})
            return response.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching CFB teams: {e}")
            return []
            
    async def get_api_usage(self) -> Dict:
        """Get current API usage and rate limit info"""
        try:
            response = await self._make_request("account/usage")
            return response.get("data", {})
        except Exception as e:
            logger.error(f"Error fetching API usage: {e}")
            return {}
            
    def game_to_dict(self, game: CFBGame) -> Dict:
        """Convert CFBGame to dictionary for JSON serialization"""
        return {
            "event_id": game.event_id,
            "home_team": game.home_team,
            "away_team": game.away_team,
            "start_time": game.start_time.isoformat() if game.start_time else None,
            "consensus_spread": game.consensus_spread,
            "consensus_total": game.consensus_total,
            "consensus_home_ml": game.consensus_home_ml,
            "consensus_away_ml": game.consensus_away_ml,
            "spread_lines": [
                {
                    "bookmaker": s.bookmaker,
                    "line": s.line,
                    "odds": s.odds,
                    "side": s.side
                } for s in game.spread_lines
            ],
            "moneyline_lines": [
                {
                    "bookmaker": m.bookmaker,
                    "odds": m.odds,
                    "side": m.side
                } for m in game.moneyline_lines
            ],
            "total_lines": [
                {
                    "bookmaker": t.bookmaker,
                    "line": t.line,
                    "odds": t.odds,
                    "side": t.side
                } for t in game.total_lines
            ]
        }
        
    def ev_bet_to_dict(self, ev_bet: EVBet) -> Dict:
        """Convert EVBet to dictionary for JSON serialization"""
        return {
            "game_id": ev_bet.game_id,
            "bet_type": ev_bet.bet_type,
            "selection": ev_bet.selection,
            "line": ev_bet.line,
            "odds": ev_bet.odds,
            "bookmaker": ev_bet.bookmaker,
            "model_probability": round(ev_bet.model_probability * 100, 1),
            "implied_probability": round(ev_bet.implied_probability * 100, 1),
            "ev_percentage": round(ev_bet.ev_percentage, 2),
            "kelly_fraction": round(ev_bet.kelly_fraction * 100, 2),
            "edge": round(ev_bet.edge * 100, 2),
            "confidence": ev_bet.confidence
        }


# Global instance for use in Flask app
_client: Optional[SportsGameOddsClient] = None


def get_sportsgameodds_client() -> SportsGameOddsClient:
    """Get or create singleton Sports Game Odds client"""
    global _client
    if _client is None:
        _client = SportsGameOddsClient()
    return _client


async def find_ev_opportunities(
    home_team: str,
    away_team: str,
    model_spread: float,
    model_total: float,
    model_home_win_prob: float,
    min_ev: float = 2.0
) -> List[Dict]:
    """
    Convenience function to find EV opportunities for a matchup.
    
    Args:
        home_team: Home team name
        away_team: Away team name
        model_spread: Model's predicted spread (positive = home favored)
        model_total: Model's predicted total
        model_home_win_prob: Model's home win probability (0-1)
        min_ev: Minimum EV% threshold
        
    Returns:
        List of EV bet opportunities as dictionaries
    """
    client = get_sportsgameodds_client()
    
    try:
        games = await client.get_cfb_events(include_odds=True)
        
        # Find the matching game
        target_game = None
        for game in games:
            if (home_team.lower() in game.home_team.lower() and 
                away_team.lower() in game.away_team.lower()):
                target_game = game
                break
                
        if not target_game:
            logger.warning(f"Game not found: {away_team} @ {home_team}")
            return []
            
        # Find EV bets
        ev_bets = client.find_ev_bets(
            target_game,
            model_spread,
            model_total,
            model_home_win_prob,
            min_ev
        )
        
        return [client.ev_bet_to_dict(bet) for bet in ev_bets]
        
    except Exception as e:
        logger.error(f"Error finding EV opportunities: {e}")
        return []


# Test function
async def test_api_connection() -> Dict:
    """Test Sports Game Odds API connection"""
    client = SportsGameOddsClient()
    
    try:
        usage = await client.get_api_usage()
        await client.close()
        
        if client.demo_mode:
            return {
                "status": "demo",
                "message": "Running in demo mode - set SPORTSGAMEODDS_API_KEY for live data",
                "usage": {}
            }
        
        return {
            "status": "connected",
            "message": "Successfully connected to Sports Game Odds API",
            "usage": usage
        }
        
    except Exception as e:
        await client.close()
        return {
            "status": "error",
            "message": str(e),
            "usage": {}
        }


if __name__ == "__main__":
    # Run test
    import asyncio
    
    async def main():
        print("Testing Sports Game Odds API connection...")
        result = await test_api_connection()
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        
        # Test EV calculation
        client = SportsGameOddsClient()
        
        print("\n--- EV Calculation Examples ---")
        
        # Example: You think a bet has 55% chance to hit at -110 odds
        ev_amt, ev_pct = client.calculate_ev(0.55, -110)
        print(f"55% win prob at -110 odds: EV = ${ev_amt:.2f} ({ev_pct:+.1f}%)")
        
        # Example: 60% chance at +100 odds
        ev_amt, ev_pct = client.calculate_ev(0.60, 100)
        print(f"60% win prob at +100 odds: EV = ${ev_amt:.2f} ({ev_pct:+.1f}%)")
        
        # Example: 40% chance at +200 odds
        ev_amt, ev_pct = client.calculate_ev(0.40, 200)
        print(f"40% win prob at +200 odds: EV = ${ev_amt:.2f} ({ev_pct:+.1f}%)")
        
        await client.close()
        
    asyncio.run(main())
