#!/usr/bin/env python3
"""
Compare Week 14 betting recommendations against actual game results
Analyzes which recommendations hit and calculates success rate
"""

import json
from datetime import datetime

def normalize_team_name(name):
    """Normalize team names for comparison"""
    # Remove common suffixes
    name = name.replace(" Volunteers", "").replace(" Commodores", "")
    name = name.replace(" Blue Devils", "").replace(" Demon Deacons", "")
    name = name.replace(" Fighting Irish", "").replace(" Cardinal", "")
    name = name.replace(" Buckeyes", "").replace(" Wolverines", "")
    name = name.replace(" Hoosiers", "").replace(" Boilermakers", "")
    name = name.replace(" Bulldogs", "").replace(" Yellow Jackets", "")
    name = name.replace(" Aggies", "").replace(" Longhorns", "")
    name = name.replace(" Ducks", "").replace(" Huskies", "")
    name = name.replace(" Rebels", "").replace(" Bulldogs", "")
    name = name.replace(" Tigers", "").replace(" Crimson Tide", "")
    return name.strip()

def parse_spread_recommendation(recommendation, away_team, home_team):
    """Parse the recommendation string to extract team and spread"""
    if "No strong edge" in recommendation:
        return None, None, None
    
    # Format: "Team -X.X at Sportsbook" or "OVER/UNDER X.X"
    if "OVER" in recommendation or "UNDER" in recommendation:
        return None, None, "total"  # Skip totals for now
    
    parts = recommendation.split(" at ")
    if len(parts) != 2:
        return None, None, None
    
    bet_info = parts[0].strip()
    sportsbook = parts[1].strip()
    
    # Extract team and spread
    bet_parts = bet_info.rsplit(" ", 1)
    if len(bet_parts) != 2:
        return None, None, None
    
    team = bet_parts[0].strip()
    spread = float(bet_parts[1])
    
    return team, spread, sportsbook

def check_spread_result(team, spread, away_team, away_score, home_team, home_score):
    """Check if the spread bet would have won"""
    normalized_team = normalize_team_name(team).lower().strip()
    normalized_away = normalize_team_name(away_team).lower().strip()
    normalized_home = normalize_team_name(home_team).lower().strip()
    
    # Determine if betting on away or home team using exact match first, then substring
    is_away = False
    if normalized_team == normalized_away:
        is_away = True
    elif normalized_team == normalized_home:
        is_away = False
    elif normalized_team in normalized_away and normalized_team not in normalized_home:
        is_away = True
    elif normalized_team in normalized_home and normalized_team not in normalized_away:
        is_away = False
    elif normalized_away in normalized_team and normalized_home not in normalized_team:
        is_away = True
    elif normalized_home in normalized_team and normalized_away not in normalized_team:
        is_away = False
    else:
        # Both match or neither match - use length heuristic
        away_match_len = len(normalized_away) if normalized_team in normalized_away or normalized_away in normalized_team else 0
        home_match_len = len(normalized_home) if normalized_team in normalized_home or normalized_home in normalized_team else 0
        is_away = away_match_len > home_match_len
    
    # Calculate actual margin
    actual_margin = int(away_score) - int(home_score)
    
    if is_away:
        # Betting on away team with spread
        # Away team wins bet if: (away_score + spread) > home_score
        bet_result = actual_margin + spread
        won = bet_result > 0
        return won, actual_margin, spread, "away"
    else:
        # Betting on home team with spread
        # Home team wins bet if: (home_score + abs(spread)) > away_score
        bet_result = -actual_margin + abs(spread)
        won = bet_result > 0
        return won, actual_margin, spread, "home"

def main():
    print("🏈 Analyzing Week 14 Betting Recommendations vs Actual Results\n")
    
    # Load predictions - using LATEST file with smart bet filtering
    with open('week14_enhanced_summaries_20251129_233957.json', 'r') as f:
        predictions = json.load(f)
    
    # Load actual results
    with open('week14_2025_scores.json', 'r') as f:
        results = json.load(f)
    
    # Build results lookup
    results_lookup = {}
    for game in results['games']:
        if game['status'] != 'Final':
            continue
        
        away = normalize_team_name(game['away_team']['name'])
        home = normalize_team_name(game['home_team']['name'])
        key = f"{away}@{home}"
        results_lookup[key] = game
    
    # Analyze each prediction
    total_recommendations = 0
    hits = 0
    misses = 0
    no_result = 0
    
    results_data = []
    
    for game in predictions['games']:
        if not game.get('success'):
            continue
        
        summary = game['summary']
        bottom_line = summary.get('bottom_line', {})
        recommendation = bottom_line.get('recommendation', '')
        
        if not recommendation or "No strong edge" in recommendation:
            continue
        
        total_recommendations += 1
        
        away_team = game['away_team']
        home_team = game['home_team']
        
        # Parse recommendation
        bet_team, bet_spread, sportsbook = parse_spread_recommendation(
            recommendation, away_team, home_team
        )
        
        if not bet_team or not bet_spread:
            continue
        
        # Find matching result
        away_norm = normalize_team_name(away_team)
        home_norm = normalize_team_name(home_team)
        
        result = None
        for key, r in results_lookup.items():
            r_away = normalize_team_name(r['away_team']['name'])
            r_home = normalize_team_name(r['home_team']['name'])
            
            if (away_norm in r_away or r_away in away_norm) and \
               (home_norm in r_home or r_home in home_norm):
                result = r
                break
        
        if not result:
            no_result += 1
            continue
        
        # Check if bet hit
        won, actual_margin, spread, bet_side = check_spread_result(
            bet_team, bet_spread,
            result['away_team']['name'], result['away_team']['score'],
            result['home_team']['name'], result['home_team']['score']
        )
        
        if won:
            hits += 1
            result_icon = "✅"
        else:
            misses += 1
            result_icon = "❌"
        
        # Get additional context
        grade = bottom_line.get('recommendation_grade', 'N/A')
        edge = bottom_line.get('recommendation_edge', 0)
        model_spread = bottom_line.get('model_spread', 'N/A')
        
        results_data.append({
            'matchup': f"{away_team} @ {home_team}",
            'recommendation': recommendation,
            'grade': grade,
            'edge': edge,
            'model_spread': model_spread,
            'actual_result': f"{result['away_team']['score']}-{result['home_team']['score']}",
            'actual_margin': actual_margin,
            'bet_spread': bet_spread,
            'won': won,
            'result_icon': result_icon
        })
    
    # Print results
    print("="*80)
    print("BETTING RECOMMENDATIONS RESULTS")
    print("="*80)
    
    for r in results_data:
        print(f"\n{r['result_icon']} {r['matchup']}")
        print(f"   Recommendation: {r['recommendation']}")
        print(f"   Grade: {r['grade']} | Edge: {r['edge']:+.1f} pts | Model: {r['model_spread']}")
        print(f"   Actual Result: {r['actual_result']} (Margin: {r['actual_margin']:+d})")
        print(f"   Bet Spread: {r['bet_spread']:+.1f} | Result: {'WON' if r['won'] else 'LOST'}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total Recommendations: {total_recommendations}")
    print(f"Games with Results: {hits + misses}")
    print(f"✅ Hits: {hits}")
    print(f"❌ Misses: {misses}")
    print(f"⏳ No Result Yet: {no_result}")
    
    if hits + misses > 0:
        win_rate = (hits / (hits + misses)) * 100
        print(f"\n🎯 WIN RATE: {win_rate:.1f}%")
        
        # Break down by grade
        strong_hits = sum(1 for r in results_data if r['grade'] == 'STRONG' and r['won'])
        strong_total = sum(1 for r in results_data if r['grade'] == 'STRONG')
        good_hits = sum(1 for r in results_data if r['grade'] == 'GOOD' and r['won'])
        good_total = sum(1 for r in results_data if r['grade'] == 'GOOD')
        slight_hits = sum(1 for r in results_data if r['grade'] == 'SLIGHT' and r['won'])
        slight_total = sum(1 for r in results_data if r['grade'] == 'SLIGHT')
        
        print(f"\nBy Grade:")
        if strong_total > 0:
            print(f"  🔥 STRONG: {strong_hits}/{strong_total} ({(strong_hits/strong_total)*100:.1f}%)")
        if good_total > 0:
            print(f"  ⭐ GOOD: {good_hits}/{good_total} ({(good_hits/good_total)*100:.1f}%)")
        if slight_total > 0:
            print(f"  ⚠️  SLIGHT: {slight_hits}/{slight_total} ({(slight_hits/slight_total)*100:.1f}%)")
    
    # Save detailed results
    output = {
        'generated_at': datetime.now().isoformat(),
        'total_recommendations': total_recommendations,
        'hits': hits,
        'misses': misses,
        'no_result': no_result,
        'win_rate': round((hits / (hits + misses)) * 100, 1) if hits + misses > 0 else 0,
        'results': results_data
    }
    
    output_file = 'week14_recommendations_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Detailed results saved to {output_file}")

if __name__ == "__main__":
    main()
