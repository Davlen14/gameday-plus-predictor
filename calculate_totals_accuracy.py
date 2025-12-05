import json

# Load the week 14 data
with open('week14_enhanced_summaries_20251130_134718.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("WEEK 14 TOTALS: MODEL vs ACTUAL")
print("=" * 80)

games = data.get('games', [])

total_games = 0
total_difference = 0
results = []

for game_data in games:
    if not isinstance(game_data, dict):
        continue
    
    home_team = game_data.get('home_team', 'Unknown')
    away_team = game_data.get('away_team', 'Unknown')
    
    # Get predicted total
    predicted_total_obj = game_data.get('predicted_total', {})
    if isinstance(predicted_total_obj, dict):
        predicted_total = predicted_total_obj.get('model_total')
    else:
        predicted_total = predicted_total_obj
    
    # Get actual total from final scores
    final_score = game_data.get('final_score', {})
    if isinstance(final_score, dict):
        away_score = final_score.get('away_score')
        home_score = final_score.get('home_score')
        if away_score is not None and home_score is not None:
            actual_total = away_score + home_score
        else:
            actual_total = None
    else:
        actual_total = None
    
    if predicted_total is not None and actual_total is not None:
        total_games += 1
        difference = abs(predicted_total - actual_total)
        total_difference += difference
        
        # Determine if we got the over/under direction correct
        # For simplicity, using 0.5 as threshold
        predicted_ou = "PUSH"
        actual_ou = "PUSH"
        
        # Compare actual total to predicted total
        if actual_total > predicted_total:
            actual_ou = "OVER"
        elif actual_total < predicted_total:
            actual_ou = "UNDER"
        
        ou_correct = "✓" if actual_ou == "PUSH" or abs(actual_total - predicted_total) < 3 else "✗"
        
        results.append({
            'game': f"{away_team} @ {home_team}",
            'predicted': predicted_total,
            'actual': actual_total,
            'difference': difference,
            'result': actual_ou
        })
        
        print(f"\n{away_team} @ {home_team}")
        print(f"  Predicted Total: {predicted_total}")
        print(f"  Actual Total: {actual_total}")
        print(f"  Difference: {difference:.1f} points ({ou_correct})")
        print(f"  Result: Actual was {actual_ou} the prediction")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

if total_games > 0:
    avg_difference = total_difference / total_games
    print(f"Total Games Analyzed: {total_games}")
    print(f"Average Difference: {avg_difference:.2f} points")
    print(f"Total Cumulative Difference: {total_difference:.1f} points")
    
    # Calculate within ranges
    within_3 = sum(1 for r in results if r['difference'] <= 3)
    within_5 = sum(1 for r in results if r['difference'] <= 5)
    within_7 = sum(1 for r in results if r['difference'] <= 7)
    within_10 = sum(1 for r in results if r['difference'] <= 10)
    
    print(f"\nAccuracy Breakdown:")
    print(f"  Within 3 points: {within_3}/{total_games} ({within_3/total_games*100:.1f}%)")
    print(f"  Within 5 points: {within_5}/{total_games} ({within_5/total_games*100:.1f}%)")
    print(f"  Within 7 points: {within_7}/{total_games} ({within_7/total_games*100:.1f}%)")
    print(f"  Within 10 points: {within_10}/{total_games} ({within_10/total_games*100:.1f}%)")
else:
    print("No games with both predicted and actual totals found.")

print("=" * 80)
