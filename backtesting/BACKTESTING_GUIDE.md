# 🔮 Backtesting Guide

## What is Backtesting?

**Backtesting = Proving your model works by testing it on past games**

Think of it like this:
- ❌ "My model is good" (just trust me bro)
- ✅ "My model correctly predicted 58% of games last week" (data-backed proof)

## Why Backtest?

1. **Know if it actually works** - Does it beat random guessing (50%)?
2. **Compare to Vegas** - Can you beat the 52.4% breakeven?
3. **Find weaknesses** - Does it struggle with upsets? Close games?
4. **Build confidence** - Real track record beats theory

## How to Backtest YOUR Model

### Step 1: Get Past Game Results

Pick a week that already happened (e.g., Week 6 - Oct 5-12, 2025)

**Find scores here:**
- ESPN: https://www.espn.com/college-football/scoreboard
- CBS Sports: https://www.cbssports.com/college-football/scoreboard/
- NCAA: https://www.ncaa.com/scoreboard/football/fbs

### Step 2: Find Team IDs

Your team IDs are in `fbs.json`:

```bash
# Quick lookup
grep -i "georgia" fbs.json
grep -i "ohio state" fbs.json
```

Or use this helper:

```python
import json

with open('fbs.json') as f:
    teams = json.load(f)
    
# Search for a team
search = "georgia"
for team in teams:
    if search.lower() in team['school'].lower():
        print(f"{team['school']}: ID = {team['id']}")
```

### Step 3: Add Games to Backtest Script

Edit `backtest_week6.py` and add real games:

```python
WEEK_6_GAMES = [
    # (home_id, away_id, actual_home_score, actual_away_score, home_name, away_name)
    (61, 194, 31, 24, "Georgia", "Auburn"),
    (194, 333, 27, 21, "Ohio State", "Michigan State"),
    # ... add more
]
```

### Step 4: Run the Backtest

```bash
python backtest_week6.py
```

## What the Results Mean

### Winner Accuracy
```
58% = EXCELLENT (you're beating Vegas!)
55% = GOOD (profitable with proper bankroll)
52.4% = BREAKEVEN (need to win 52.4% to beat -110 juice)
50% = RANDOM (coin flip)
<50% = BAD (worse than guessing)
```

### Spread Error
```
<5 points = ELITE (Vegas-level)
5-7 points = GOOD (competitive)
7-10 points = OKAY (room for improvement)
>10 points = NEEDS WORK
```

### Brier Score
Measures probability calibration (0 = perfect, 1 = worst)
```
<0.15 = EXCELLENT
0.15-0.20 = GOOD
0.20-0.25 = OKAY
>0.25 = NEEDS CALIBRATION
```

## Quick Week 6 Example

Let's say Week 6 had these results:

**Game 1: Georgia vs Florida**
- Your prediction: Georgia -14, 65% win prob
- Actual: Georgia won 31-10 (won by 21)
- Result: ✅ Correct winner, spread error = 7 points

**Game 2: USC vs Washington**  
- Your prediction: USC -3, 58% win prob
- Actual: Washington won 24-20 (upset!)
- Result: ❌ Wrong winner, spread error = 7 points

**If you went 8-4 on Week 6:**
- That's 66.7% accuracy = ELITE territory!
- You'd be profitable betting at standard odds

## Pro Tips

### Start Small
- Test on **5-10 games** first (one week)
- Easy to gather data
- Fast to run
- Shows immediate results

### Then Go Bigger
- Test on **entire season** (Weeks 1-6)
- Requires more data collection
- Shows consistency over time
- More reliable stats

### Track Multiple Metrics
1. **Winner accuracy** - Are you picking the right team?
2. **Spread accuracy** - Are your margin predictions close?
3. **Total accuracy** - Are your over/under predictions good?
4. **Upset detection** - Can you spot underdogs?
5. **Confidence calibration** - When you say 70%, does it happen 70% of the time?

## What's a "Good" Result?

**For a brand new model (like yours):**

- 🎯 **52-54%** = "Hey, this works!"
- 🌟 **55-57%** = "This is actually good!"
- 🚀 **58%+** = "Holy shit, this is elite!"

**Context:**
- Vegas wins ~55% of the time
- Professional bettors happy with 54-56%
- 52.4% = breakeven at -110 odds
- 50% = random guessing

## Easy Next Steps

1. **Today**: Add 5 games from last week to `backtest_week6.py`
2. **Run it**: See your accuracy
3. **Share results**: "My model went 4/5 on Week 6!" sounds way better than "I think my model is good"
4. **Iterate**: If it's bad, you know what to fix

## Why This Matters

Without backtesting, you're essentially saying:
> "I built a fancy calculator that I think works correctly, but I've never actually tested it."

With backtesting, you can say:
> "I tested my model on 50 games and it correctly predicted 56% of winners with an average spread error of 6.2 points."

**Way more credible!** 💪

---

## Need Help Getting Started?

Run this to test a single game from last week:

```python
import asyncio
from graphqlpredictor import LightningPredictor

async def test_one_game():
    predictor = LightningPredictor(week=6)
    
    # Pick any game from last week - get IDs from fbs.json
    # Example: Test a game you know the result of
    home_id = 61  # Change this
    away_id = 194  # Change this
    
    prediction = await predictor.predict_game(home_id, away_id)
    
    print(f"Predicted: {prediction.home_team} {prediction.predicted_spread:+.1f}")
    print(f"Win Prob: {prediction.home_win_prob:.1%}")
    print(f"Total: {prediction.predicted_total:.1f}")
    print("\nNow compare to actual result!")

asyncio.run(test_one_game())
```

Then manually check if it was right! 🎯
