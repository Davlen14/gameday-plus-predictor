#!/usr/bin/env python3
"""
Correct CFP Analysis - Based on Actual 2025 Bracket
Fixed to match real CFP matchups and predictions
"""

import sqlite3
from collections import defaultdict
import statistics

def analyze_team_performance(cursor, team, season=2025):
    """Get comprehensive team performance stats"""
    # Get all games for the team in the season
    cursor.execute("""
        SELECT opponent, result, coach_score, opponent_score, 
               opponent_sp_overall, opponent_fpi, is_home
        FROM games 
        WHERE school = ? AND season = ?
        ORDER BY week
    """, (team, season))
    
    games = cursor.fetchall()
    if not games:
        return None
    
    wins = len([g for g in games if g[1] == 'W'])
    losses = len([g for g in games if g[1] == 'L'])
    
    # Calculate scoring stats
    points_for = [g[2] for g in games if g[2] is not None]
    points_against = [g[3] for g in games if g[3] is not None]
    
    avg_points_for = statistics.mean(points_for) if points_for else 0
    avg_points_against = statistics.mean(points_against) if points_against else 0
    margin = avg_points_for - avg_points_against
    
    # Calculate strength of schedule
    opponent_ratings = [g[4] for g in games if g[4] is not None]
    sos = statistics.mean(opponent_ratings) if opponent_ratings else 0
    
    return {
        'record': f"{wins}-{losses}",
        'wins': wins,
        'losses': losses,
        'avg_points_for': avg_points_for,
        'avg_points_against': avg_points_against,
        'margin': margin,
        'sos': sos,
        'total_games': len(games)
    }

def get_head_to_head(cursor, team1, team2, years=5):
    """Get head-to-head record between two teams"""
    cursor.execute("""
        SELECT season, school, opponent, result, coach_score, opponent_score
        FROM games 
        WHERE (school = ? AND opponent = ?) OR (school = ? AND opponent = ?)
        AND season >= ?
        ORDER BY season DESC
    """, (team1, team2, team2, team1, 2025 - years))
    
    games = cursor.fetchall()
    
    team1_wins = 0
    team2_wins = 0
    recent_games = []
    
    for game in games:
        if game[1] == team1:  # team1 played
            if game[3] == 'W':
                team1_wins += 1
            else:
                team2_wins += 1
        else:  # team2 played
            if game[3] == 'W':
                team2_wins += 1
            else:
                team1_wins += 1
        
        recent_games.append({
            'season': game[0],
            'winner': team1 if (game[1] == team1 and game[3] == 'W') or (game[1] == team2 and game[3] == 'L') else team2,
            'score': f"{game[4]}-{game[5]}" if game[4] and game[5] else "N/A"
        })
    
    return {
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'total_games': len(games),
        'recent_games': recent_games[:3]  # Last 3 games
    }

def predict_matchup(team1_stats, team2_stats, h2h_data):
    """Predict outcome of matchup"""
    if not team1_stats or not team2_stats:
        return None
    
    # Base prediction on point margins
    margin_diff = team1_stats['margin'] - team2_stats['margin']
    
    # Adjust for strength of schedule
    sos_adj = (team1_stats['sos'] - team2_stats['sos']) * 0.1
    
    # Head-to-head adjustment
    h2h_adj = 0
    if h2h_data['total_games'] > 0:
        h2h_ratio = h2h_data['team1_wins'] / h2h_data['total_games']
        if h2h_ratio > 0.6:
            h2h_adj = 2.0  # Team1 dominates
        elif h2h_ratio < 0.4:
            h2h_adj = -2.0  # Team2 dominates
    
    predicted_margin = margin_diff + sos_adj + h2h_adj
    
    return {
        'predicted_winner': team1_stats if predicted_margin > 0 else team2_stats,
        'predicted_margin': abs(predicted_margin),
        'confidence': min(100, abs(predicted_margin) * 5)
    }

def main():
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print("🏆 2025 CFP BRACKET ANALYSIS - CORRECT VERSION")
    print("=" * 60)
    
    # Actual CFP bracket matchups
    first_round_games = [
        ("James Madison", "Oregon"),     # #12 vs #5
        ("Alabama", "Oklahoma"),         # #9 vs #8  
        ("Tulane", "Ole Miss"),         # #11 vs #6
        ("Miami", "Texas A&M")          # #10 vs #7
    ]
    
    top_4_seeds = [
        ("Indiana", 1),      # #1 seed
        ("Ohio State", 2),   # #2 seed  
        ("Georgia", 3),      # #3 seed
        ("Texas Tech", 4)    # #4 seed
    ]
    
    print("\n🎯 FIRST ROUND PREDICTIONS")
    print("=" * 40)
    
    first_round_winners = []
    
    for i, (team1, team2) in enumerate(first_round_games, 1):
        print(f"\nGame {i}: {team1} vs {team2}")
        
        team1_stats = analyze_team_performance(cursor, team1)
        team2_stats = analyze_team_performance(cursor, team2)
        h2h_data = get_head_to_head(cursor, team1, team2)
        
        if team1_stats and team2_stats:
            print(f"  {team1}: {team1_stats['record']} ({team1_stats['margin']:+.1f} margin)")
            print(f"  {team2}: {team2_stats['record']} ({team2_stats['margin']:+.1f} margin)")
            
            prediction = predict_matchup(team1_stats, team2_stats, h2h_data)
            if prediction:
                winner_name = team1 if prediction['predicted_winner'] == team1_stats else team2
                print(f"  🎯 PREDICTION: {winner_name} by {prediction['predicted_margin']:.1f}")
                first_round_winners.append(winner_name)
            
            if h2h_data['total_games'] > 0:
                print(f"  📚 H2H: {team1} {h2h_data['team1_wins']}-{h2h_data['team2_wins']} {team2}")
        else:
            print(f"  ⚠️  Missing data for one or both teams")
            first_round_winners.append(team1)  # Default
    
    print("\n🏆 TOP 4 SEEDS (Automatic Quarterfinal Berths)")
    print("=" * 50)
    
    for team, seed in top_4_seeds:
        stats = analyze_team_performance(cursor, team)
        if stats:
            print(f"#{seed} {team}: {stats['record']} ({stats['margin']:+.1f} margin, {stats['avg_points_for']:.1f} PPG)")
    
    print(f"\n🎮 QUARTERFINAL MATCHUPS")
    print("=" * 30)
    
    # Based on actual bracket structure
    quarterfinals = [
        ("Indiana", first_round_winners[1] if len(first_round_winners) > 1 else "Oklahoma/Alabama winner"),     # Rose Bowl
        ("Ohio State", first_round_winners[3] if len(first_round_winners) > 3 else "A&M/Miami winner"),        # Cotton Bowl  
        ("Georgia", first_round_winners[2] if len(first_round_winners) > 2 else "Ole Miss/Tulane winner"),     # Sugar Bowl
        ("Texas Tech", first_round_winners[0] if len(first_round_winners) > 0 else "Oregon/JMU winner")        # Orange Bowl
    ]
    
    for i, (seed, opponent) in enumerate(quarterfinals, 1):
        bowl_names = ["Rose Bowl", "Cotton Bowl", "Sugar Bowl", "Orange Bowl"]
        print(f"{bowl_names[i-1]}: #{i} {seed} vs {opponent}")
    
    print(f"\n📊 KEY INSIGHTS")
    print("=" * 20)
    
    # Find strongest first round team
    best_margin = -100
    best_team = ""
    for winner in first_round_winners:
        if winner in [team for team, _ in first_round_games]:
            stats = analyze_team_performance(cursor, winner)
            if stats and stats['margin'] > best_margin:
                best_margin = stats['margin']
                best_team = winner
    
    print(f"🔥 Strongest First Round Winner: {best_team} ({best_margin:+.1f} margin)")
    
    # Compare top seeds
    seed_stats = []
    for team, seed in top_4_seeds:
        stats = analyze_team_performance(cursor, team)
        if stats:
            seed_stats.append((team, stats['margin'], stats['avg_points_for']))
    
    seed_stats.sort(key=lambda x: x[1], reverse=True)
    print(f"🏆 Strongest Top Seed: {seed_stats[0][0]} ({seed_stats[0][1]:+.1f} margin)")
    
    conn.close()
    
    print(f"\n✅ Analysis complete with CORRECT 2025 CFP bracket!")

if __name__ == "__main__":
    main()