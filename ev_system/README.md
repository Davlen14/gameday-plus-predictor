# +EV (Positive Expected Value) Identification System

A comprehensive Python module for identifying positive expected value betting opportunities in sports betting markets through real-time odds analysis and mathematical modeling.

## Features

- **Odds Conversion**: Convert between American, Decimal, and Implied Probability formats
- **No-Vig Calculation**: Calculate fair probabilities by removing bookmaker vig
- **Expected Value (EV) Detection**: Identify +EV opportunities by comparing soft book odds to sharp book fair lines
- **Kelly Criterion**: Optimal bankroll management with fractional Kelly and risk controls
- **Arbitrage Detection**: Find pure arbitrage and middle opportunities across sportsbooks
- **Portfolio Management**: Track bets, manage drawdowns, and calculate performance metrics

## Installation

The module is included in the gameday-plus-predictor repository. No additional installation required.

```python
from ev_system import EVCalculator, KellyCriterion, EVDetectionEngine
```

## Quick Start

### Calculate Expected Value

```python
from ev_system import EVCalculator

calculator = EVCalculator(min_ev_threshold=0.01)  # 1% minimum

# Basic EV calculation
result = calculator.calculate_ev(
    true_probability=0.55,  # 55% true chance
    decimal_odds=2.0        # +100 American
)
print(f"EV: {result['ev_percentage']}%")
print(f"Is +EV: {result['is_plus_ev']}")

# Compare sharp vs soft book
result = calculator.calculate_ev_from_sharp_line(
    sharp_odds=[-150, 130],  # Pinnacle line
    soft_odds=140,           # DraftKings offering +140
    selection_index=1        # Underdog
)
```

### Calculate Optimal Bet Size

```python
from ev_system import KellyCriterion

kelly = KellyCriterion(
    bankroll=10000,
    kelly_fraction=0.25,    # Quarter Kelly for safety
    max_bet_percentage=0.05 # Max 5% per bet
)

result = kelly.calculate_bet_size(
    probability=0.55,
    decimal_odds=2.0
)
print(f"Recommended bet: ${result['bet_amount']}")
```

### Detect Arbitrage Opportunities

```python
from ev_system import ArbitrageDetector

detector = ArbitrageDetector()

# Check for pure arbitrage
arb = detector.detect_two_way_arbitrage(
    odds_side_a=[('BookA', 110)],  # Team A +110 at BookA
    odds_side_b=[('BookB', 110)],  # Team B +110 at BookB
    total_stake=1000
)

if arb:
    print(f"Arbitrage found! Profit: ${arb.guaranteed_profit}")
```

### Full Detection Engine

```python
from ev_system import EVDetectionEngine

engine = EVDetectionEngine(
    bankroll=10000,
    min_ev_threshold=0.01,
    min_edge_threshold=0.02
)

odds_data = [
    {'sportsbook': 'pinnacle', 'home_odds': -150, 'away_odds': 130},
    {'sportsbook': 'draftkings', 'home_odds': -140, 'away_odds': 125},
    {'sportsbook': 'fanduel', 'home_odds': -145, 'away_odds': 140},
]

result = engine.process_odds_update(
    event_id='game_001',
    event_name='Team A vs Team B',
    odds_data=odds_data
)

for opp in result['ev_opportunities']:
    print(f"+EV: {opp['sportsbook']} - {opp['ev_percentage']}%")
```

## Module Components

### ev_calculator.py

- `OddsConverter`: Convert between odds formats
- `NoVigCalculator`: Remove vig from betting lines
- `EVCalculator`: Calculate expected value

### kelly_criterion.py

- `KellyCriterion`: Optimal bet sizing
- `PortfolioManager`: Bankroll and risk management

### arbitrage_detector.py

- `ArbitrageDetector`: Find arbitrage and middle opportunities
- `ArbitrageOpportunity`: Dataclass for detected opportunities

### odds_manager.py

- `OddsManager`: Multi-sportsbook odds aggregation
- `RateLimiter`: API rate limiting
- `SportsbookOdds`: Dataclass for odds data

### ev_engine.py

- `EVDetectionEngine`: Main detection engine
- `EVOpportunity`: Dataclass for +EV opportunities

## Mathematical Foundation

### Expected Value Formula

```
EV = (True Probability × Potential Profit) - (Probability of Losing × Stake)
```

### No-Vig Fair Line Calculation

```
Implied Probability = 100 / (American Odds + 100)  [for positive odds]
Implied Probability = |American Odds| / (|American Odds| + 100)  [for negative odds]

Total Implied Probability = Sum of all market probabilities
Vig Rate = Total Implied Probability - 100%

True Probability = Individual Implied Probability / Total Implied Probability
```

### Kelly Criterion

```
f* = (bp - q) / b

Where:
  f* = optimal fraction of bankroll
  b = decimal odds - 1
  p = probability of winning
  q = probability of losing
```

## Running Tests

```bash
python -m ev_system.test_ev_system
```

## Running Demo

```bash
python -m ev_system.demo
```

## Sportsbook Classifications

The system classifies sportsbooks as:

- **Sharp**: Pinnacle, BetCris, Bookmaker, Circa
- **Soft**: DraftKings, FanDuel, BetMGM, Caesars, etc.
- **Exchange**: Betfair, Matchbook, Smarkets

Sharp books are used for fair line calculation, while soft books are scanned for +EV opportunities.

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_ev_threshold` | 0.01 (1%) | Minimum EV to flag as +EV |
| `min_edge_threshold` | 0.02 (2%) | Minimum edge over fair line |
| `kelly_fraction` | 0.25 | Fraction of full Kelly to use |
| `max_bet_percentage` | 0.05 (5%) | Maximum bet as % of bankroll |
| `max_drawdown` | 0.20 (20%) | Maximum acceptable drawdown |

## License

Part of the Gameday+ Predictor project.
