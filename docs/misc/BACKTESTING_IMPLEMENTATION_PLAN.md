# 🔬 **COMPREHENSIVE BACKTESTING SYSTEM - 48 HOUR IMPLEMENTATION**

## 🎯 **GOAL: Test Model Performance Using Historical Weekly Data**

Your model already has **weekly snapshots** stored in `weekly_updates/week_N/`. This is PERFECT for proper backtesting because each week's data only contains information available **at that time**.

---

## 📊 **YOUR CURRENT WEEKLY DATA STRUCTURE**

```
weekly_updates/
├── week_13/
│   ├── all_fbs_ratings_comprehensive_2025_20251117_204708.json  ← ELO/FPI/S&P+/SRS ratings
│   ├── fbs_teams_stats_only.json  ← Team statistics (EPA, yards, etc.)
│   ├── react_power5_efficiency.json  ← Efficiency metrics
│   ├── power5_drives_only.json  ← Drive-level data
│   ├── ap.json  ← AP Poll rankings
│   ├── coaches_simplified_ranked.json  ← Coaching data
│   ├── react_fbs_conferences.json  ← Conference info
│   ├── react_fbs_team_rankings.json  ← Team rankings
│   ├── team_season_summaries_clean.json  ← Season summaries
│   ├── fbs_defensive_stats.json  ← Defensive metrics
│   ├── fbs_offensive_stats.json  ← Offensive metrics
│   ├── react_power5_teams.json  ← Power 5 team drive data
│   ├── complete_win_probabilities.json  ← Historical probabilities
│   └── week13_2025_games_20251117_205550.json  ← Games for that week
│
└── week_14/
    ├── all_fbs_ratings_comprehensive_2025_20251125_021912.json
    ├── fbs_teams_stats_only.json
    ├── ... (same structure)
```

---

## 🚨 **CRITICAL INSIGHT: Time-Travel Backtesting**

**THE PROBLEM WITH NAIVE BACKTESTING:**
```python
# ❌ WRONG: Using Week 14 data to predict Week 7
predictor = LightningPredictor(api_key)  # Loads week_14 data!
prediction = predictor.predict_game(home_id, away_id)  # Week 7 game
# This is CHEATING - model has future information!
```

**THE CORRECT APPROACH:**
```python
# ✅ RIGHT: Load Week 6 data to predict Week 7
predictor = LightningPredictor(api_key, data_week=6)  # Only week 6 data
prediction = predictor.predict_game(home_id, away_id)  # Week 7 game
# Model only knows what was available before Week 7!
```

---

## 🏗️ **IMPLEMENTATION STRATEGY**

### **Phase 1: Make Predictor "Time-Aware"** (4 hours)
Modify `graphqlpredictor.py` to accept a `data_week` parameter that loads historical data from specific weeks.

### **Phase 2: Fetch Historical Game Results** (2 hours)
Create scripts to fetch actual scores for Weeks 1-14 from GraphQL API.

### **Phase 3: Build Backtesting Engine** (6 hours)
Create a system that:
1. Loads Week N-1 data
2. Predicts Week N games
3. Compares against actual results
4. Calculates accuracy metrics

### **Phase 4: Generate Reports** (4 hours)
Build comprehensive reports showing:
- Week-by-week performance
- Spread accuracy trends
- Betting ROI over time
- Model calibration analysis

---

## 📋 **DETAILED IMPLEMENTATION**

### **STEP 1: Modify LightningPredictor for Time-Travel** ⏰

**File: `graphqlpredictor.py`**

**Changes Required:**

```python
# OLD (Line 1278-1282):
def __init__(self, api_key: str):
    self.api_key = api_key
    self.base_url = "https://graphql.collegefootballdata.com/v1/graphql"
    self.current_week = 8
    self.current_year = 2025

# NEW:
def __init__(self, api_key: str, data_week: Optional[int] = None, prediction_week: Optional[int] = None):
    """
    Initialize predictor with time-travel capability
    
    Args:
        api_key: College Football Data API key
        data_week: Week number to load static data from (default: latest available)
        prediction_week: Week number to set for predictions (default: data_week + 1)
    """
    self.api_key = api_key
    self.base_url = "https://graphql.collegefootballdata.com/v1/graphql"
    
    # Determine which week's data to load
    self.data_week = data_week or self._get_latest_week()
    self.prediction_week = prediction_week or (self.data_week + 1)
    self.current_week = self.prediction_week
    self.current_year = 2025
    
    print(f"🕐 TIME-TRAVEL MODE:")
    print(f"   Loading data from: Week {self.data_week}")
    print(f"   Predicting for: Week {self.prediction_week}")
```

**Update _load_all_static_data() method (Line ~1321):**

```python
def _load_all_static_data(self) -> Dict:
    """Load all static JSON data files for comprehensive team analysis"""
    try:
        # DYNAMIC PATH BASED ON data_week
        week_folder = f'week_{self.data_week}'
        base_path = os.path.join(os.path.dirname(__file__), 'weekly_updates', week_folder)
        
        # Check if week folder exists
        if not os.path.exists(base_path):
            print(f"⚠️  Warning: {week_folder} folder not found, using latest available")
            # Fallback to latest week
            base_path = os.path.join(os.path.dirname(__file__), 'weekly_updates', 'week_14')
        
        print(f"📂 Loading static data from: {base_path}")
        
        # Rest of loading logic stays the same...
```

---

### **STEP 2: Create Historical Results Fetcher** 📥

**New File: `fetch_historical_results.py`**

```python
#!/usr/bin/env python3
"""
Fetch actual game results for all weeks (1-14) from GraphQL API
Saves to backtesting/week_N_results.json
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://graphql.collegefootballdata.com/v1/graphql"

async def fetch_week_results(session, week: int):
    """Fetch all completed games for a specific week"""
    query = """
    query GetWeekResults($week: smallint!, $year: smallint!) {
      game(where: {
        season: {_eq: $year},
        week: {_eq: $week},
        seasonType: {_eq: "regular"},
        homePoints: {_is_null: false},
        awayPoints: {_is_null: false}
      }) {
        id
        startDate
        week
        season
        seasonType
        homeTeamId
        homeTeam
        homeConference
        homePoints
        awayTeamId
        awayTeam
        awayConference
        awayPoints
        neutralSite
      }
    }
    """
    
    variables = {"week": week, "year": 2025}
    
    async with session.post(
        BASE_URL,
        json={"query": query, "variables": variables},
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    ) as response:
        result = await response.json()
        
        if 'errors' in result:
            print(f"❌ Week {week}: GraphQL errors - {result['errors']}")
            return None
        
        games = result.get('data', {}).get('game', [])
        
        # Filter for FBS games only
        fbs_games = [g for g in games if g.get('homeConference') and g.get('awayConference')]
        
        print(f"✅ Week {week}: {len(fbs_games)} FBS games completed")
        
        return {
            'week': week,
            'total_games': len(fbs_games),
            'fetched_at': datetime.now().isoformat(),
            'games': fbs_games
        }

async def fetch_all_weeks():
    """Fetch results for all weeks"""
    print("🏈 Fetching Historical Game Results (Weeks 1-14)")
    print("=" * 60)
    
    # Create backtesting directory
    os.makedirs('backtesting', exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        for week in range(1, 15):  # Weeks 1-14
            print(f"\n📊 Fetching Week {week}...")
            
            result = await fetch_week_results(session, week)
            
            if result:
                # Save to file
                output_file = f"backtesting/week_{week}_results.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"   💾 Saved to: {output_file}")
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
    
    print("\n✅ All historical results fetched!")

if __name__ == "__main__":
    asyncio.run(fetch_all_weeks())
```

---

### **STEP 3: Build Progressive Backtesting Engine** 🔬

**New File: `progressive_backtest.py`**

```python
#!/usr/bin/env python3
"""
Progressive Backtesting System
Tests model performance week-by-week using only data available at prediction time
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List
from graphqlpredictor import LightningPredictor
import pandas as pd

API_KEY = "YOUR_API_KEY_HERE"

def load_week_results(week: int) -> Dict:
    """Load actual results for a specific week"""
    results_file = f"backtesting/week_{week}_results.json"
    
    if not os.path.exists(results_file):
        print(f"⚠️  Warning: {results_file} not found")
        return None
    
    with open(results_file, 'r') as f:
        return json.load(f)

def get_team_id(team_name: str) -> int:
    """Convert team name to ID"""
    # Load fbs.json for team ID mapping
    with open('fbs.json', 'r') as f:
        teams = json.load(f)
    
    # Direct match
    for team in teams:
        if team['school'].lower() == team_name.lower():
            return team['id']
    
    # Fuzzy match
    team_words = set(team_name.lower().split())
    for team in teams:
        school_words = set(team['school'].lower().split())
        if team_words & school_words:
            return team['id']
    
    print(f"⚠️  Could not find ID for: {team_name}")
    return None

async def backtest_week(data_week: int, prediction_week: int) -> Dict:
    """
    Backtest a single week using only data available before that week
    
    Args:
        data_week: Week to load data from (e.g., 6)
        prediction_week: Week to predict (e.g., 7)
    """
    print(f"\n{'='*80}")
    print(f"🔬 BACKTESTING WEEK {prediction_week}")
    print(f"   Using data from: Week {data_week}")
    print(f"{'='*80}\n")
    
    # Load actual results for the prediction week
    actual_results = load_week_results(prediction_week)
    
    if not actual_results:
        print(f"❌ No results found for Week {prediction_week}")
        return None
    
    games = actual_results['games']
    print(f"📊 Testing against {len(games)} completed games\n")
    
    # Initialize predictor with historical data
    predictor = LightningPredictor(
        api_key=API_KEY,
        data_week=data_week,
        prediction_week=prediction_week
    )
    
    results = {
        'data_week': data_week,
        'prediction_week': prediction_week,
        'total_games': 0,
        'successful_predictions': 0,
        'failed_predictions': 0,
        'winner_correct': 0,
        'spread_within_7': 0,
        'spread_within_14': 0,
        'spread_errors': [],
        'total_errors': [],
        'game_details': []
    }
    
    for idx, game in enumerate(games, 1):
        home_team = game['homeTeam']
        away_team = game['awayTeam']
        home_points = game['homePoints']
        away_points = game['awayPoints']
        actual_margin = home_points - away_points
        
        home_id = game['homeTeamId']
        away_id = game['awayTeamId']
        
        if not home_id or not away_id:
            print(f"[{idx}/{len(games)}] ⚠️  Skipping {away_team} @ {home_team} - Missing IDs")
            results['failed_predictions'] += 1
            continue
        
        print(f"[{idx}/{len(games)}] {away_team} @ {home_team}")
        print(f"   Actual: {away_team} {away_points}, {home_team} {home_points} (Margin: {actual_margin:+.1f})")
        
        try:
            # Generate prediction using historical data
            prediction = await predictor.predict_game(home_id, away_id)
            
            # Extract prediction details
            predicted_spread = prediction.predicted_spread
            predicted_total = prediction.predicted_total
            
            # Calculate accuracy metrics
            spread_error = abs(predicted_spread - actual_margin)
            total_error = abs(predicted_total - (home_points + away_points))
            
            # Determine winners
            predicted_winner = home_team if predicted_spread < 0 else away_team
            actual_winner = home_team if actual_margin > 0 else away_team
            winner_correct = (predicted_winner == actual_winner)
            
            print(f"   Predicted: Spread {predicted_spread:+.1f}, Total {predicted_total:.1f}")
            print(f"   Errors: Spread {spread_error:.1f}, Total {total_error:.1f}")
            print(f"   Winner: {'✅ CORRECT' if winner_correct else '❌ WRONG'}")
            
            # Update statistics
            results['total_games'] += 1
            results['successful_predictions'] += 1
            
            if winner_correct:
                results['winner_correct'] += 1
            
            if spread_error <= 7:
                results['spread_within_7'] += 1
            
            if spread_error <= 14:
                results['spread_within_14'] += 1
            
            results['spread_errors'].append(spread_error)
            results['total_errors'].append(total_error)
            
            # Store game details
            results['game_details'].append({
                'matchup': f"{away_team} @ {home_team}",
                'actual_score': f"{away_points}-{home_points}",
                'actual_margin': actual_margin,
                'predicted_spread': predicted_spread,
                'predicted_total': predicted_total,
                'spread_error': spread_error,
                'total_error': total_error,
                'winner_correct': winner_correct
            })
            
        except Exception as e:
            print(f"   ❌ Prediction failed: {str(e)}")
            results['failed_predictions'] += 1
        
        print()
    
    # Calculate summary statistics
    if results['total_games'] > 0:
        results['winner_accuracy'] = (results['winner_correct'] / results['total_games']) * 100
        results['spread_accuracy_7'] = (results['spread_within_7'] / results['total_games']) * 100
        results['spread_accuracy_14'] = (results['spread_within_14'] / results['total_games']) * 100
        results['avg_spread_error'] = sum(results['spread_errors']) / len(results['spread_errors'])
        results['avg_total_error'] = sum(results['total_errors']) / len(results['total_errors'])
    
    return results

async def run_full_backtest(start_week: int = 2, end_week: int = 14):
    """
    Run complete progressive backtest from start_week to end_week
    
    Args:
        start_week: First week to predict (need week 1 data to predict week 2)
        end_week: Last week to predict
    """
    print("🏈 PROGRESSIVE BACKTESTING SYSTEM")
    print("=" * 80)
    print(f"Testing Weeks {start_week} to {end_week}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    all_results = []
    
    for prediction_week in range(start_week, end_week + 1):
        data_week = prediction_week - 1
        
        # Check if we have the necessary data
        data_folder = f"weekly_updates/week_{data_week}"
        if not os.path.exists(data_folder):
            print(f"\n⚠️  Skipping Week {prediction_week} - No Week {data_week} data available")
            continue
        
        # Run backtest for this week
        result = await backtest_week(data_week, prediction_week)
        
        if result:
            all_results.append(result)
            
            # Print week summary
            print(f"\n📊 WEEK {prediction_week} SUMMARY:")
            print(f"   Games Tested: {result['total_games']}")
            print(f"   Winner Accuracy: {result.get('winner_accuracy', 0):.1f}%")
            print(f"   Spread Accuracy (±7): {result.get('spread_accuracy_7', 0):.1f}%")
            print(f"   Avg Spread Error: {result.get('avg_spread_error', 0):.2f} points")
        
        # Small delay between weeks
        await asyncio.sleep(1)
    
    # Save comprehensive results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"backtesting/progressive_backtest_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump({
            'generated_at': timestamp,
            'weeks_tested': list(range(start_week, end_week + 1)),
            'total_weeks': len(all_results),
            'results_by_week': all_results
        }, f, indent=2)
    
    print(f"\n✅ Full backtest complete!")
    print(f"💾 Results saved to: {output_file}")
    
    # Generate summary report
    generate_summary_report(all_results, timestamp)

def generate_summary_report(results: List[Dict], timestamp: str):
    """Generate comprehensive summary report"""
    
    # Calculate aggregate statistics
    total_games = sum(r['total_games'] for r in results)
    total_winner_correct = sum(r['winner_correct'] for r in results)
    total_spread_7 = sum(r['spread_within_7'] for r in results)
    
    overall_winner_pct = (total_winner_correct / total_games) * 100 if total_games > 0 else 0
    overall_spread_pct = (total_spread_7 / total_games) * 100 if total_games > 0 else 0
    
    all_spread_errors = []
    for r in results:
        all_spread_errors.extend(r['spread_errors'])
    
    avg_spread_error = sum(all_spread_errors) / len(all_spread_errors) if all_spread_errors else 0
    
    # Create markdown report
    report_file = f"backtesting/Progressive_Backtest_Report_{timestamp}.md"
    
    with open(report_file, 'w') as f:
        f.write("# 🔬 Progressive Backtesting Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 Overall Performance\n\n")
        f.write(f"- **Total Games Tested:** {total_games}\n")
        f.write(f"- **Winner Accuracy:** {overall_winner_pct:.1f}%\n")
        f.write(f"- **Spread Accuracy (±7 pts):** {overall_spread_pct:.1f}%\n")
        f.write(f"- **Average Spread Error:** {avg_spread_error:.2f} points\n\n")
        
        f.write("---\n\n")
        f.write("## 📅 Week-by-Week Breakdown\n\n")
        
        for r in results:
            f.write(f"### Week {r['prediction_week']}\n\n")
            f.write(f"**Data Source:** Week {r['data_week']}\n\n")
            f.write(f"- Games Tested: {r['total_games']}\n")
            f.write(f"- Winner Accuracy: {r.get('winner_accuracy', 0):.1f}%\n")
            f.write(f"- Spread Accuracy (±7): {r.get('spread_accuracy_7', 0):.1f}%\n")
            f.write(f"- Spread Accuracy (±14): {r.get('spread_accuracy_14', 0):.1f}%\n")
            f.write(f"- Avg Spread Error: {r.get('avg_spread_error', 0):.2f} points\n\n")
    
    print(f"📄 Summary report saved to: {report_file}")
    
    # Create CSV for analysis
    csv_file = f"backtesting/progressive_backtest_{timestamp}.csv"
    
    # Flatten all game details
    csv_data = []
    for r in results:
        for game in r['game_details']:
            csv_data.append({
                'Week': r['prediction_week'],
                'Data_Week': r['data_week'],
                'Matchup': game['matchup'],
                'Actual_Score': game['actual_score'],
                'Actual_Margin': game['actual_margin'],
                'Predicted_Spread': game['predicted_spread'],
                'Predicted_Total': game['predicted_total'],
                'Spread_Error': game['spread_error'],
                'Total_Error': game['total_error'],
                'Winner_Correct': game['winner_correct']
            })
    
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_file, index=False)
    
    print(f"📊 CSV data saved to: {csv_file}")

if __name__ == "__main__":
    # Run backtest for all available weeks
    asyncio.run(run_full_backtest(start_week=2, end_week=14))
```

---

## ⏱️ **48-HOUR TIMELINE**

### **Day 1 (24 hours)**
- **Hour 0-4:** Modify `graphqlpredictor.py` with time-travel capability
- **Hour 4-6:** Create and run `fetch_historical_results.py`
- **Hour 6-12:** Build `progressive_backtest.py` core engine
- **Hour 12-16:** Test on Week 13 (single week validation)
- **Hour 16-20:** Debug and refine
- **Hour 20-24:** Run progressive backtest Weeks 2-10

### **Day 2 (24 hours)**
- **Hour 24-30:** Complete backtest Weeks 11-14
- **Hour 30-36:** Analyze results, identify patterns
- **Hour 36-40:** Generate comprehensive reports
- **Hour 40-44:** Compare against Week 13/14 actual performance
- **Hour 44-48:** Final documentation and presentation

---

## 🚀 **QUICK START COMMANDS**

```bash
# 1. Fetch historical results
python fetch_historical_results.py

# 2. Run single week test (Week 13)
python progressive_backtest.py --week 13

# 3. Run full progressive backtest
python progressive_backtest.py --start 2 --end 14

# 4. Analyze results
python analyze_backtest_results.py
```

---

## 📈 **EXPECTED OUTPUTS**

1. **JSON Files:** `backtesting/progressive_backtest_TIMESTAMP.json`
2. **Markdown Report:** `backtesting/Progressive_Backtest_Report_TIMESTAMP.md`
3. **CSV Data:** `backtesting/progressive_backtest_TIMESTAMP.csv`
4. **Performance Metrics:**
   - Week-by-week accuracy
   - Spread error trends
   - Model calibration analysis
   - Betting ROI simulation

---

## ✅ **SUCCESS CRITERIA**

- ✅ Model uses only historical data (no future information leakage)
- ✅ All 13 weeks tested (Weeks 2-14 using Weeks 1-13 data)
- ✅ Comprehensive accuracy metrics calculated
- ✅ Results match your existing Week 13 performance (~76% spread accuracy)
- ✅ Clear documentation of methodology

---

**Ready to implement?** This system will give you **legitimate backtesting** that respects your weekly data collection process! 🎯
