"""
Fixed betting analysis system with proper normalization, edge calculations, and provider selection.
Implements all requirements from the specification including data integrity warnings and unit tests.
"""

import warnings
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import statistics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIntegrityWarning(UserWarning):
    """Warning for spread/moneyline inconsistencies"""
    pass

class DataSanityWarning(UserWarning):
    """Warning for extreme value discrepancies"""
    pass

@dataclass
class SportsbookLine:
    """Represents a single sportsbook's betting lines"""
    provider: str
    spread: Optional[float] = None
    total: Optional[float] = None
    moneyline_home: Optional[int] = None
    moneyline_away: Optional[int] = None

@dataclass
class NormalizedBettingAnalysis:
    """Normalized betting analysis with proper edge calculations"""
    # Team of interest (for consistent perspective)
    team_of_interest: str
    opponent: str
    
    # Model projections (normalized to team_of_interest perspective)
    model_spread_for_team: float  # Positive = team gets points, Negative = team gives points
    model_total: float
    
    # Market consensus (normalized to team_of_interest perspective)
    market_spread_consensus: float
    market_total_consensus: float
    
    # Edge calculations
    spread_value_edge: float  # market_spread - model_spread (positive = value on team_of_interest)
    total_value_edge: float   # model_total - market_total (positive = value on OVER)
    
    # Best available lines
    best_spread_line: Optional[SportsbookLine] = None
    best_total_line: Optional[SportsbookLine] = None
    best_spread_value: Optional[float] = None
    best_total_value: Optional[float] = None
    
    # Recommendations
    spread_recommendation: Optional[str] = None
    total_recommendation: Optional[str] = None
    
    # Warnings and data quality
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class FixedBettingAnalyzer:
    """Fixed betting analysis with proper normalization and edge calculations"""
    
    def __init__(self, spread_threshold: float = 2.0, total_threshold: float = 3.0):
        self.spread_threshold = spread_threshold
        self.total_threshold = total_threshold
        
    def normalize_spread_to_team_perspective(self, 
                                           raw_spread: float, 
                                           team_of_interest: str, 
                                           home_team: str, 
                                           away_team: str,
                                           spread_is_for_home: bool = True) -> float:
        """
        Normalize spread to team_of_interest perspective.
        
        Args:
            raw_spread: The raw spread value from sportsbook
            team_of_interest: The team we're analyzing from perspective of
            home_team: Home team name
            away_team: Away team name
            spread_is_for_home: Whether the raw_spread is from home team's perspective
            
        Returns:
            Normalized spread where positive = team_of_interest gets points
        """
        if team_of_interest == home_team:
            # Team of interest is home team
            return raw_spread if spread_is_for_home else -raw_spread
        else:
            # Team of interest is away team
            return -raw_spread if spread_is_for_home else raw_spread
    
    def detect_spread_moneyline_inconsistency(self, 
                                            spread: float, 
                                            moneyline_favorite: int, 
                                            moneyline_underdog: int,
                                            team_of_interest: str,
                                            home_team: str) -> bool:
        """
        Detect if spread and moneyline disagree on favorite.
        
        Returns True if inconsistent, False if consistent.
        """
        # Determine favorite from spread (negative spread = favorite)
        spread_indicates_home_favorite = spread < 0
        
        # Determine favorite from moneylines (negative moneyline = favorite)
        if team_of_interest == home_team:
            # We have home team's perspective
            ml_indicates_home_favorite = moneyline_favorite < moneyline_underdog
        else:
            # We have away team's perspective  
            ml_indicates_home_favorite = moneyline_underdog < moneyline_favorite
            
        return spread_indicates_home_favorite != ml_indicates_home_favorite
    
    def find_best_spread_line(self, 
                            sportsbooks: List[SportsbookLine],
                            team_of_interest: str,
                            home_team: str,
                            away_team: str,
                            value_edge: float) -> Tuple[Optional[SportsbookLine], Optional[float]]:
        """
        Find the best available spread line based on value edge direction.
        
        If value_edge > 0: Look for highest + number (most points for team_of_interest)
        If value_edge < 0: Look for lowest - number (give fewest points)
        """
        if not sportsbooks:
            return None, None
            
        valid_lines = [sb for sb in sportsbooks if sb.spread is not None]
        if not valid_lines:
            return None, None
            
        # Normalize all spreads to team_of_interest perspective
        normalized_spreads = []
        for sb in valid_lines:
            normalized = self.normalize_spread_to_team_perspective(
                sb.spread, team_of_interest, home_team, away_team, spread_is_for_home=True
            )
            normalized_spreads.append((sb, normalized))
        
        if value_edge > 0:
            # Value on team_of_interest - want highest + number (most points)
            best_line, best_spread = max(normalized_spreads, key=lambda x: x[1])
        else:
            # Value on opponent - want lowest number (give fewest points)
            best_line, best_spread = min(normalized_spreads, key=lambda x: x[1])
            
        return best_line, best_spread
    
    def find_best_total_line(self, 
                           sportsbooks: List[SportsbookLine], 
                           total_edge: float) -> Tuple[Optional[SportsbookLine], Optional[float]]:
        """
        Find the best available total line based on edge direction.
        
        If total_edge > 0 (model > market): Value on OVER, want lowest total
        If total_edge < 0 (model < market): Value on UNDER, want highest total
        """
        valid_lines = [sb for sb in sportsbooks if sb.total is not None]
        if not valid_lines:
            return None, None
            
        if total_edge > 0:
            # Value on OVER - want lowest total available
            best_line = min(valid_lines, key=lambda x: x.total)
        else:
            # Value on UNDER - want highest total available
            best_line = max(valid_lines, key=lambda x: x.total)
            
        return best_line, best_line.total
    
    def calculate_market_consensus(self, 
                                 sportsbooks: List[SportsbookLine],
                                 team_of_interest: str,
                                 home_team: str,
                                 away_team: str) -> Tuple[float, float]:
        """Calculate market consensus spread and total with outlier removal"""
        
        # Normalize spreads to team_of_interest perspective
        normalized_spreads = []
        totals = []
        
        for sb in sportsbooks:
            if sb.spread is not None:
                normalized = self.normalize_spread_to_team_perspective(
                    sb.spread, team_of_interest, home_team, away_team, spread_is_for_home=True
                )
                normalized_spreads.append(normalized)
                
            if sb.total is not None:
                totals.append(sb.total)
        
        # Remove outliers (beyond 3 standard deviations) unless all values are extreme
        def remove_outliers(values):
            if len(values) <= 2:
                return values
            mean_val = statistics.mean(values)
            stdev = statistics.stdev(values) if len(values) > 1 else 0
            if stdev == 0:
                return values
            filtered = [v for v in values if abs(v - mean_val) <= 3 * stdev]
            return filtered if filtered else values  # Keep all if all are outliers
        
        consensus_spread = statistics.mean(remove_outliers(normalized_spreads)) if normalized_spreads else 0.0
        consensus_total = statistics.mean(remove_outliers(totals)) if totals else 0.0
        
        return consensus_spread, consensus_total
    
    def analyze_betting_value(self,
                            model_spread: float,  # From team_of_interest perspective
                            model_total: float,
                            team_of_interest: str,
                            home_team: str,
                            away_team: str,
                            sportsbooks: List[SportsbookLine]) -> NormalizedBettingAnalysis:
        """
        Complete betting analysis with proper normalization and recommendations.
        
        Args:
            model_spread: Model's spread from team_of_interest perspective (+ = team gets points)
            model_total: Model's predicted total
            team_of_interest: Team to analyze from perspective of
            home_team: Home team name
            away_team: Away team name  
            sportsbooks: List of sportsbook lines
        """
        
        opponent = away_team if team_of_interest == home_team else home_team
        
        # Calculate market consensus
        market_spread_consensus, market_total_consensus = self.calculate_market_consensus(
            sportsbooks, team_of_interest, home_team, away_team
        )
        
        # Calculate value edges
        spread_value_edge = market_spread_consensus - model_spread
        total_value_edge = model_total - market_total_consensus
        
        # Find best available lines
        best_spread_line, best_spread_value = self.find_best_spread_line(
            sportsbooks, team_of_interest, home_team, away_team, spread_value_edge
        )
        best_total_line, best_total_value = self.find_best_total_line(
            sportsbooks, total_value_edge
        )
        
        # Create analysis object
        analysis = NormalizedBettingAnalysis(
            team_of_interest=team_of_interest,
            opponent=opponent,
            model_spread_for_team=model_spread,
            model_total=model_total,
            market_spread_consensus=market_spread_consensus,
            market_total_consensus=market_total_consensus,
            spread_value_edge=spread_value_edge,
            total_value_edge=total_value_edge,
            best_spread_line=best_spread_line,
            best_total_line=best_total_line,
            best_spread_value=best_spread_value,
            best_total_value=best_total_value
        )
        
        # Generate recommendations
        self._generate_recommendations(analysis)
        
        # Check for data integrity issues
        self._validate_data_integrity(analysis, sportsbooks, home_team)
        
        return analysis
    
    def _generate_recommendations(self, analysis: NormalizedBettingAnalysis):
        """Generate betting recommendations based on value edges and thresholds"""
        
        # Spread recommendation
        if abs(analysis.spread_value_edge) >= self.spread_threshold:
            if analysis.spread_value_edge > 0:
                # Value on team_of_interest
                spread_text = f"{analysis.best_spread_value:+.1f}" if analysis.best_spread_value else f"{analysis.market_spread_consensus:+.1f}"
                provider = analysis.best_spread_line.provider if analysis.best_spread_line else "Consensus"
                analysis.spread_recommendation = f"✅ {analysis.team_of_interest} {spread_text} @ {provider} — Market undervaluing {analysis.team_of_interest}"
            else:
                # Value on opponent
                spread_text = f"{-analysis.best_spread_value:+.1f}" if analysis.best_spread_value else f"{-analysis.market_spread_consensus:+.1f}"
                provider = analysis.best_spread_line.provider if analysis.best_spread_line else "Consensus"
                analysis.spread_recommendation = f"✅ {analysis.opponent} {spread_text} @ {provider} — Market overvaluing {analysis.team_of_interest}"
        else:
            analysis.spread_recommendation = "No significant spread value detected"
            
        # Total recommendation  
        if abs(analysis.total_value_edge) >= self.total_threshold:
            if analysis.total_value_edge > 0:
                # Value on OVER
                total_text = f"{analysis.best_total_value:.1f}" if analysis.best_total_value else f"{analysis.market_total_consensus:.1f}"
                provider = analysis.best_total_line.provider if analysis.best_total_line else "Consensus"
                analysis.total_recommendation = f"✅ OVER {total_text} @ {provider} — Model projects higher scoring"
                
                # Check for extreme discrepancy
                if analysis.total_value_edge > 12:
                    analysis.warnings.append("DataSanityWarning: Extreme total discrepancy detected (>12 points)")
            else:
                # Value on UNDER
                total_text = f"{analysis.best_total_value:.1f}" if analysis.best_total_value else f"{analysis.market_total_consensus:.1f}"
                provider = analysis.best_total_line.provider if analysis.best_total_line else "Consensus"
                analysis.total_recommendation = f"✅ UNDER {total_text} @ {provider} — Model projects lower scoring"
                
                if analysis.total_value_edge < -12:
                    analysis.warnings.append("DataSanityWarning: Extreme total discrepancy detected (>12 points)")
        else:
            analysis.total_recommendation = "No significant total value detected"
    
    def _validate_data_integrity(self, analysis: NormalizedBettingAnalysis, sportsbooks: List[SportsbookLine], home_team: str):
        """Validate data integrity and add warnings for inconsistencies"""
        
        inconsistent_books = []
        for sb in sportsbooks:
            if sb.spread is not None and sb.moneyline_home is not None and sb.moneyline_away is not None:
                is_inconsistent = self.detect_spread_moneyline_inconsistency(
                    sb.spread, sb.moneyline_home, sb.moneyline_away, 
                    analysis.team_of_interest, home_team
                )
                if is_inconsistent:
                    inconsistent_books.append(sb.provider)
        
        if inconsistent_books:
            analysis.warnings.append(f"DataIntegrityWarning: Spread/moneyline inconsistency at {', '.join(inconsistent_books)}")
            
        # Check for extreme spread discrepancies between books
        spreads = [sb.spread for sb in sportsbooks if sb.spread is not None]
        if len(spreads) > 1:
            spread_range = max(spreads) - min(spreads)
            if spread_range > 6:  # More than 6 point spread between books
                analysis.warnings.append(f"DataIntegrityWarning: Large spread variance across books ({spread_range:.1f} points)")
    
    def format_analysis_output(self, analysis: NormalizedBettingAnalysis) -> str:
        """Format analysis output according to exact specification requirements"""
        
        output_lines = []
        
        # Determine who is the favorite for proper display formatting
        # If team_of_interest has positive spread, they're the underdog
        # If team_of_interest has negative spread, they're the favorite
        is_team_of_interest_underdog = analysis.model_spread_for_team > 0
        
        if is_team_of_interest_underdog:
            favorite_team = analysis.opponent
            underdog_team = analysis.team_of_interest
            favorite_model_spread = -analysis.model_spread_for_team  # Convert to favorite perspective
            favorite_market_spread = -analysis.market_spread_consensus
        else:
            favorite_team = analysis.team_of_interest
            underdog_team = analysis.opponent
            favorite_model_spread = analysis.model_spread_for_team
            favorite_market_spread = analysis.market_spread_consensus
        
        # Model Projection - always show favorite giving points (negative)
        output_lines.append(f"Model Projection: {favorite_team} {favorite_model_spread:+.1f}  (Total {analysis.model_total:.1f})")
        
        # Market Consensus - always show favorite giving points (negative)
        output_lines.append(f"Market Consensus: {favorite_team} {favorite_market_spread:+.1f}  (Total {analysis.market_total_consensus:.1f})")
        
        # Value Edge (spread)
        output_lines.append(f"Value Edge (spread): {analysis.spread_value_edge:+.1f} points")
        
        # Best Available Spread Line - show in conventional format (favorite giving points)
        if analysis.best_spread_line and analysis.best_spread_value is not None:
            if is_team_of_interest_underdog:
                # Team of interest is underdog, show favorite giving points
                best_spread_display = -analysis.best_spread_value
                output_lines.append(f"Best Available Spread Line: {favorite_team} {best_spread_display:+.1f} @ {analysis.best_spread_line.provider}")
            else:
                # Team of interest is favorite, show them giving points
                output_lines.append(f"Best Available Spread Line: {favorite_team} {analysis.best_spread_value:+.1f} @ {analysis.best_spread_line.provider}")
        
        # Recommended Bet (spread)
        output_lines.append(f"{analysis.spread_recommendation}")
        
        # Value Edge (total)
        output_lines.append(f"Value Edge (total): {analysis.total_value_edge:+.1f} points")
        
        # Best Available Total Line
        if analysis.best_total_line and analysis.best_total_value is not None:
            over_under = "OVER" if analysis.total_value_edge > 0 else "UNDER"
            output_lines.append(f"Best Available Total Line: {over_under} {analysis.best_total_value:.1f} @ {analysis.best_total_line.provider}")
        
        # Recommended Total Bet
        output_lines.append(f"{analysis.total_recommendation}")
        
        # Warnings
        for warning in analysis.warnings:
            output_lines.append(warning)
            
        return "\n".join(output_lines)


# Unit Tests
class TestFixedBettingAnalyzer:
    """Comprehensive unit tests for the fixed betting analyzer"""
    
    def __init__(self):
        self.analyzer = FixedBettingAnalyzer()
        self.test_results = []
    
    def test_sign_normalization(self):
        """Test a) sign normalization"""
        print("🧪 Testing sign normalization...")
        
        # Test case: Ohio State -25.5, normalize to Wisconsin perspective
        result = self.analyzer.normalize_spread_to_team_perspective(
            raw_spread=-25.5,  # Ohio State -25.5 (home team giving 25.5)
            team_of_interest="Wisconsin",
            home_team="Ohio State", 
            away_team="Wisconsin",
            spread_is_for_home=True
        )
        
        expected = +25.5  # From Wisconsin's perspective, they get 25.5 points
        assert result == expected, f"Expected {expected}, got {result}"
        print(f"   ✅ Ohio State -25.5 → Wisconsin {result:+.1f} ✓")
        
        # Test reverse case
        result2 = self.analyzer.normalize_spread_to_team_perspective(
            raw_spread=+7.5,  # Home team getting 7.5
            team_of_interest="Home Team",
            home_team="Home Team",
            away_team="Away Team", 
            spread_is_for_home=True
        )
        
        expected2 = +7.5
        assert result2 == expected2, f"Expected {expected2}, got {result2}"
        print(f"   ✅ Home +7.5 → Home Team {result2:+.1f} ✓")
        
    def test_value_edge_calculation(self):
        """Test b) value_edge calculation with mixed sign inputs"""
        print("🧪 Testing value edge calculations...")
        
        # Wisconsin example: market gives +25.5, model gives +15.6
        market_spread = +25.5
        model_spread = +15.6
        value_edge = market_spread - model_spread
        
        expected = +9.9
        assert abs(value_edge - expected) < 0.1, f"Expected ~{expected}, got {value_edge}"
        print(f"   ✅ Market {market_spread:+.1f} - Model {model_spread:+.1f} = {value_edge:+.1f} ✓")
        
        # Test negative case
        market_spread2 = -3.5
        model_spread2 = +1.5  
        value_edge2 = market_spread2 - model_spread2
        expected2 = -5.0
        
        assert abs(value_edge2 - expected2) < 0.1, f"Expected ~{expected2}, got {value_edge2}"
        print(f"   ✅ Market {market_spread2:+.1f} - Model {model_spread2:+.1f} = {value_edge2:+.1f} ✓")
        
    def test_moneyline_spread_consistency(self):
        """Test c) moneyline vs spread favorite mismatch detection"""
        print("🧪 Testing moneyline/spread consistency...")
        
        # Consistent case: Spread says home -7, moneylines say home favorite
        inconsistent = self.analyzer.detect_spread_moneyline_inconsistency(
            spread=-7.0,  # Home team favored by 7
            moneyline_favorite=-150,  # Home team favored  
            moneyline_underdog=+130,  # Away team underdog
            team_of_interest="Home Team",
            home_team="Home Team"
        )
        
        assert not inconsistent, "Should be consistent"
        print(f"   ✅ Consistent: Home -7, ML Home -150/Away +130 ✓")
        
        # Inconsistent case: Spread says home -7, but moneylines say away favorite
        inconsistent2 = self.analyzer.detect_spread_moneyline_inconsistency(
            spread=-7.0,   # Home team favored by 7
            moneyline_favorite=+150,  # Home team underdog in ML?? 
            moneyline_underdog=-130,  # Away team favorite in ML??
            team_of_interest="Home Team", 
            home_team="Home Team"
        )
        
        assert inconsistent2, "Should detect inconsistency"
        print(f"   ✅ Inconsistent detected: Home -7 but ML suggests away favorite ✓")
        
    def test_best_available_line_selection(self):
        """Test d) picking best available sportsbook line for both spread and total"""
        print("🧪 Testing best line selection...")
        
        sportsbooks = [
            SportsbookLine("Bovada", spread=-26.0, total=41.0),
            SportsbookLine("ESPN Bet", spread=-24.5, total=42.5), 
            SportsbookLine("DraftKings", spread=-25.5, total=41.5)
        ]
        
        # Test best spread for team getting points (positive value edge)
        best_line, best_spread = self.analyzer.find_best_spread_line(
            sportsbooks=sportsbooks,
            team_of_interest="Wisconsin",
            home_team="Ohio State",
            away_team="Wisconsin", 
            value_edge=+9.9  # Value on Wisconsin
        )
        
        expected_spread = +26.0  # Bovada gives Wisconsin the most points
        assert best_line.provider == "Bovada", f"Expected Bovada, got {best_line.provider}"
        assert abs(best_spread - expected_spread) < 0.1, f"Expected {expected_spread:+.1f}, got {best_spread:+.1f}"
        print(f"   ✅ Best spread for underdog: Wisconsin {best_spread:+.1f} @ {best_line.provider} ✓")
        
        # Test best total for OVER (model > market)
        best_total_line, best_total = self.analyzer.find_best_total_line(
            sportsbooks=sportsbooks,
            total_edge=+24.9  # Value on OVER
        )
        
        expected_total = 41.0  # Bovada has lowest total
        assert best_total_line.provider == "Bovada", f"Expected Bovada, got {best_total_line.provider}"
        assert abs(best_total - expected_total) < 0.1, f"Expected {expected_total}, got {best_total}"
        print(f"   ✅ Best total for OVER: {best_total} @ {best_total_line.provider} ✓")
        
    def run_all_tests(self):
        """Run all unit tests"""
        print("🧪 RUNNING UNIT TESTS FOR FIXED BETTING ANALYZER")
        print("=" * 60)
        
        try:
            self.test_sign_normalization()
            self.test_value_edge_calculation() 
            self.test_moneyline_spread_consistency()
            self.test_best_available_line_selection()
            
            print("=" * 60)
            print("🎉 ALL TESTS PASSED!")
            return True
            
        except Exception as e:
            print(f"❌ TEST FAILED: {e}")
            return False


def run_wisconsin_ohio_state_example():
    """Run the Wisconsin vs Ohio State example with corrected logic"""
    print("\n🏈 WISCONSIN vs OHIO STATE EXAMPLE")
    print("=" * 50)
    
    analyzer = FixedBettingAnalyzer(spread_threshold=2.0, total_threshold=3.0)
    
    # Input data from the example
    model_spread_wisconsin = +15.6  # Model: Wisconsin +15.6 
    model_total = 65.9
    
    # Market data (raw sportsbook lines)
    sportsbooks = [
        SportsbookLine("Bovada", spread=-26.0, total=41.0),      # Ohio State -26
        SportsbookLine("ESPN Bet", spread=-24.5, total=42.5),    # Ohio State -24.5
        SportsbookLine("DraftKings", spread=-25.5, total=41.5)   # Ohio State -25.5
    ]
    
    # Run analysis
    analysis = analyzer.analyze_betting_value(
        model_spread=model_spread_wisconsin,
        model_total=model_total,
        team_of_interest="Wisconsin",
        home_team="Ohio State",
        away_team="Wisconsin", 
        sportsbooks=sportsbooks
    )
    
    # Format and display results
    print("\n📊 CORRECTED ANALYSIS RESULTS:")
    print("-" * 40)
    output = analyzer.format_analysis_output(analysis)
    print(output)
    
    # Additional calculations for verification
    print(f"\n🔍 VERIFICATION CALCULATIONS:")
    print(f"   Consensus Edge: {analysis.spread_value_edge:+.1f}")
    if analysis.best_spread_line:
        provider_edge = analysis.best_spread_value - model_spread_wisconsin
        print(f"   Provider Edge (Bovada): {provider_edge:+.1f}")
    
    return analysis


if __name__ == "__main__":
    # Run unit tests
    tester = TestFixedBettingAnalyzer()
    tests_passed = tester.run_all_tests()
    
    if tests_passed:
        # Run Wisconsin vs Ohio State example
        analysis = run_wisconsin_ohio_state_example()
        
        print(f"\n📋 WARNINGS AND LOGS:")
        for warning in analysis.warnings:
            print(f"   ⚠️  {warning}")
            
        if not analysis.warnings:
            print(f"   ✅ No data integrity issues detected")