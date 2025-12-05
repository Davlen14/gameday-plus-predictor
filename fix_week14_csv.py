#!/usr/bin/env python3
"""
Fix Week 14 CSV calculations - corrects spread edge, total edge, recommendations, and projected scores
"""

import csv
import sys

def parse_spread(spread_str, home_team, away_team):
    """Parse spread string like 'South Florida -32.1' or 'Michigan +9.8' to get numeric value from HOME perspective"""
    if not spread_str or spread_str == '':
        return None
    
    parts = spread_str.strip().rsplit(None, 1)  # Split on last space
    if len(parts) < 2:
        return None
    
    try:
        team_name = parts[0].strip()
        value = float(parts[-1])
        
        # Convert to home team perspective
        if team_name == home_team or team_name in home_team:
            # Already home perspective
            return value
        elif team_name == away_team or team_name in away_team:
            # Away perspective, flip sign
            return -value
        else:
            # Can't determine, return as-is
            return value
    except:
        return None

def calculate_projected_scores(model_spread, model_total):
    """Calculate actual projected scores from spread and total"""
    # model_spread is from home team perspective (negative = home favored)
    # Total = Home Score + Away Score
    # Spread = Home Score - Away Score
    
    # Solving: H + A = Total, H - A = Spread
    # H = (Total + Spread) / 2
    # A = (Total - Spread) / 2
    
    home_score = (model_total + model_spread) / 2
    away_score = (model_total - model_spread) / 2
    
    return away_score, home_score

def fix_csv():
    """Read CSV, fix calculations, write corrected version"""
    
    input_file = 'Week14_Game_Summaries.csv'
    output_file = 'FULLY_CORRECTED_PREDICTIONS.csv'
    
    print(f"📊 Reading {input_file}...")
    
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        for row in reader:
            rows.append(row)
    
    print(f"✅ Loaded {len(rows)} games")
    print(f"\n🔧 Fixing calculations...\n")
    
    fixed_count = 0
    
    for idx, row in enumerate(rows, 1):
        home_team = row['Home Team']
        away_team = row['Away Team']
        
        # Parse model spread and market spread
        model_spread_str = row['Model Spread']
        market_spread_str = row['Market Spread']
        
        model_spread_val = parse_spread(model_spread_str, home_team, away_team)
        market_spread_val = parse_spread(market_spread_str, home_team, away_team)
        
        model_total = float(row['Model Total'])
        market_total = float(row['Market Total'])
        
        # FIX 1: SPREAD EDGE CALCULATION
        # Formula: |Model Spread| - |Market Spread|
        if model_spread_val is not None and market_spread_val is not None:
            spread_edge = abs(model_spread_val) - abs(market_spread_val)
            row['Spread Edge'] = f"{spread_edge:+.1f}"
        else:
            spread_edge = 0
            row['Spread Edge'] = "0.0"
        
        # FIX 2: SPREAD RECOMMENDATION
        # Spread Edge = |Model Spread| - |Market Spread|
        # Positive edge means model sees favorite STRONGER than market
        # Negative edge means model sees favorite WEAKER than market (underdog value)
        
        if abs(spread_edge) >= 2.5:
            # Determine who the favorite is (negative spread = home favored, positive = away favored)
            home_favored_in_model = model_spread_val < 0
            
            if spread_edge > 0:
                # Model has favorite stronger - bet the FAVORITE
                if home_favored_in_model:
                    # Bet home team (the favorite) at market line
                    row['Recommended Spread Bet'] = f"{home_team} {market_spread_val:.1f}"
                else:
                    # Bet away team (the favorite) at market line  
                    row['Recommended Spread Bet'] = f"{away_team} {-market_spread_val:.1f}"
            else:
                # Model has favorite weaker - bet the UNDERDOG
                if home_favored_in_model:
                    # Home is favorite, so bet away (underdog) at market line
                    row['Recommended Spread Bet'] = f"{away_team} {-market_spread_val:.1f}"
                else:
                    # Away is favorite, so bet home (underdog) at market line
                    row['Recommended Spread Bet'] = f"{home_team} {market_spread_val:.1f}"
        else:
            row['Recommended Spread Bet'] = "No Edge"
        
        # FIX 3: TOTAL EDGE CALCULATION
        # Formula: Model Total - Market Total
        total_edge = model_total - market_total
        row['Total Edge'] = f"{total_edge:+.1f}"
        
        # FIX 4: TOTAL RECOMMENDATION
        # If positive: Model thinks OVER, If negative: Model thinks UNDER
        if abs(total_edge) >= 3.5:
            if total_edge > 0:
                row['Recommended Total Bet'] = f"OVER {market_total:.1f}"
            else:
                row['Recommended Total Bet'] = f"UNDER {market_total:.1f}"
        else:
            row['Recommended Total Bet'] = "No Edge"
        
        # FIX 5: PROJECTED SCORES
        # Calculate actual point projections from spread and total
        away_score, home_score = calculate_projected_scores(model_spread_val, model_total)
        row['Projected Away Score'] = f"{away_score:.1f}"
        row['Projected Home Score'] = f"{home_score:.1f}"
        row['Projected Total'] = f"{model_total:.1f}"
        
        fixed_count += 1
        
        # Show progress
        if idx % 10 == 0:
            print(f"  Processed {idx}/{len(rows)} games...")
    
    # Write corrected CSV
    print(f"\n💾 Writing corrected data to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ SUCCESS!")
    print(f"📊 Fixed {fixed_count} games")
    print(f"💾 Saved to: {output_file}")
    print(f"\n🔍 Key Fixes Applied:")
    print(f"  ✓ Spread Edge: Changed from addition to subtraction")
    print(f"  ✓ Spread Recommendations: Inverted logic (favorite when positive edge)")
    print(f"  ✓ Total Edge: Now uses actual total values, not spread values")
    print(f"  ✓ Total Recommendations: Added UNDER bets (not just OVER)")
    print(f"  ✓ Projected Scores: Changed from win probabilities to actual points")
    
    # Show some examples
    print(f"\n📋 Example Corrections (First 3 Games):\n")
    for i in range(min(3, len(rows))):
        row = rows[i]
        print(f"  {row['Away Team']} @ {row['Home Team']}")
        print(f"    Spread Edge: {row['Spread Edge']}")
        print(f"    Spread Bet: {row['Recommended Spread Bet']}")
        print(f"    Total Edge: {row['Total Edge']}")
        print(f"    Total Bet: {row['Recommended Total Bet']}")
        print(f"    Projected Score: {row['Projected Away Score']} - {row['Projected Home Score']}")
        print()

if __name__ == "__main__":
    try:
        fix_csv()
    except FileNotFoundError:
        print(f"❌ Error: Week14_Game_Summaries.csv not found!")
        print(f"   Make sure you're running this from the correct directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
