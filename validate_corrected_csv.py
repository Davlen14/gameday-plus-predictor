#!/usr/bin/env python3
"""
Validate FULLY_CORRECTED_PREDICTIONS.csv to ensure all calculations are correct
"""

import csv

def validate_csv():
    """Validate all calculations in corrected CSV"""
    
    file_path = 'FULLY_CORRECTED_PREDICTIONS.csv'
    
    print("=" * 60)
    print("🔍 VALIDATION REPORT - FULLY_CORRECTED_PREDICTIONS.csv")
    print("=" * 60)
    
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    total_games = len(rows)
    errors = []
    
    spread_edge_errors = 0
    total_edge_errors = 0
    projected_score_errors = 0
    recommendation_conflicts = 0
    over_count = 0
    under_count = 0
    no_total_edge_count = 0
    
    print(f"\n📊 Total Games Analyzed: {total_games}\n")
    print("Checking calculations...\n")
    
    for idx, row in enumerate(rows, 1):
        away = row['Away Team']
        home = row['Home Team']
        
        # Parse spreads
        model_spread_str = row['Model Spread']
        market_spread_str = row['Market Spread']
        
        # Extract numeric values
        try:
            model_spread_parts = model_spread_str.rsplit(None, 1)
            model_spread = float(model_spread_parts[-1])
            
            market_spread_parts = market_spread_str.rsplit(None, 1)
            market_spread = float(market_spread_parts[-1])
            
            # Adjust for perspective
            if away in model_spread_str or away.split()[0] in model_spread_str:
                model_spread = -model_spread  # Convert to home perspective
            if away in market_spread_str or away.split()[0] in market_spread_str:
                market_spread = -market_spread
            
            # Validate Spread Edge
            expected_spread_edge = abs(model_spread) - abs(market_spread)
            actual_spread_edge = float(row['Spread Edge'])
            
            if abs(expected_spread_edge - actual_spread_edge) > 0.2:
                spread_edge_errors += 1
                errors.append(f"{away} @ {home}: Spread Edge error - Expected {expected_spread_edge:+.1f}, Got {actual_spread_edge:+.1f}")
            
            # Validate Total Edge
            model_total = float(row['Model Total'])
            market_total = float(row['Market Total'])
            expected_total_edge = model_total - market_total
            actual_total_edge = float(row['Total Edge'])
            
            if abs(expected_total_edge - actual_total_edge) > 0.2:
                total_edge_errors += 1
                errors.append(f"{away} @ {home}: Total Edge error - Expected {expected_total_edge:+.1f}, Got {actual_total_edge:+.1f}")
            
            # Validate Projected Scores
            proj_away = float(row['Projected Away Score'])
            proj_home = float(row['Projected Home Score'])
            proj_total = float(row['Projected Total'])
            
            calculated_total = proj_away + proj_home
            calculated_spread = proj_home - proj_away
            
            if abs(calculated_total - proj_total) > 0.2:
                projected_score_errors += 1
                errors.append(f"{away} @ {home}: Projected Total mismatch - Sum={calculated_total:.1f}, Listed={proj_total:.1f}")
            
            if abs(calculated_spread - model_spread) > 0.2:
                projected_score_errors += 1
                errors.append(f"{away} @ {home}: Projected Spread mismatch - Calculated={calculated_spread:.1f}, Model={model_spread:.1f}")
            
            # Count total recommendations
            total_rec = row['Recommended Total Bet']
            if 'OVER' in total_rec:
                over_count += 1
            elif 'UNDER' in total_rec:
                under_count += 1
            elif 'No Edge' in total_rec:
                no_total_edge_count += 1
            
            # Validate recommendation logic
            spread_rec = row['Recommended Spread Bet']
            if 'No Edge' not in spread_rec and abs(expected_spread_edge) >= 2.5:
                # Check recommendation matches edge direction
                home_favored = model_spread < 0
                
                if expected_spread_edge > 0:
                    # Should recommend favorite
                    if home_favored:
                        if home not in spread_rec:
                            recommendation_conflicts += 1
                            errors.append(f"{away} @ {home}: Spread rec should be {home} (favorite), got {spread_rec}")
                    else:
                        if away not in spread_rec:
                            recommendation_conflicts += 1
                            errors.append(f"{away} @ {home}: Spread rec should be {away} (favorite), got {spread_rec}")
                else:
                    # Should recommend underdog
                    if home_favored:
                        if away not in spread_rec:
                            recommendation_conflicts += 1
                            errors.append(f"{away} @ {home}: Spread rec should be {away} (underdog), got {spread_rec}")
                    else:
                        if home not in spread_rec:
                            recommendation_conflicts += 1
                            errors.append(f"{away} @ {home}: Spread rec should be {home} (underdog), got {spread_rec}")
        
        except Exception as e:
            errors.append(f"{away} @ {home}: Parsing error - {e}")
    
    # Print summary
    print("=" * 60)
    print("📈 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total Games Analyzed: {total_games}")
    print(f"Spread Edge Errors: {spread_edge_errors} {'✓' if spread_edge_errors == 0 else '✗'}")
    print(f"Total Edge Errors: {total_edge_errors} {'✓' if total_edge_errors == 0 else '✗'}")
    print(f"Projected Score Errors: {projected_score_errors} {'✓' if projected_score_errors == 0 else '✗'}")
    print(f"Recommendation Conflicts: {recommendation_conflicts} {'✓' if recommendation_conflicts == 0 else '✗'}")
    print()
    print(f"Total Bet Breakdown:")
    print(f"  OVER recommendations: {over_count}")
    print(f"  UNDER recommendations: {under_count}")
    print(f"  No Edge: {no_total_edge_count}")
    print()
    
    # Check for specific games
    print("=" * 60)
    print("🎯 SPOT CHECK - KEY GAMES")
    print("=" * 60)
    
    key_games = ['Ohio State', 'Indiana', 'Rice']
    for game_team in key_games:
        for row in rows:
            if game_team in row['Away Team'] or game_team in row['Home Team']:
                print(f"\n{row['Away Team']} @ {row['Home Team']}")
                print(f"  Model Spread: {row['Model Spread']}")
                print(f"  Market Spread: {row['Market Spread']}")
                print(f"  Spread Edge: {row['Spread Edge']}")
                print(f"  Spread Bet: {row['Recommended Spread Bet']}")
                print(f"  Total Edge: {row['Total Edge']}")
                print(f"  Total Bet: {row['Recommended Total Bet']}")
                print(f"  Projected Score: {row['Projected Away Score']} - {row['Projected Home Score']}")
                break
    
    # Final verdict
    print()
    print("=" * 60)
    print("⚖️  FINAL VERDICT")
    print("=" * 60)
    
    total_errors = len(errors)
    
    if total_errors == 0:
        print("✅ FILE IS CLEAN - No corruption detected!")
        print("   All calculations are mathematically correct.")
        print("   Ready for betting analysis.")
    elif total_errors < 5:
        print(f"⚠️  MINOR ISSUES - {total_errors} issues found (low severity)")
        print("   File is mostly clean but review errors below.")
    else:
        print(f"❌ MAJOR ISSUES - {total_errors} critical errors found")
        print("   Review and fix errors below before using.")
    
    if errors:
        print()
        print("=" * 60)
        print("📋 SPECIFIC ERRORS FOUND")
        print("=" * 60)
        for error in errors[:20]:  # Show first 20
            print(f"  • {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    validate_csv()
