import json

# Load the JSON
with open('frontend/src/data/comprehensive_power_rankings.json', 'r') as f:
    data = json.load(f)

# Add detailed_metrics structure to each team
for team_obj in data['teams']:
    stats = team_obj.get('stats', {})
    
    # Calculate derived metrics
    games = stats.get('games', 1)
    pass_attempts = stats.get('passAttempts', 1)
    rush_attempts = stats.get('rushingAttempts', 1)
    total_plays = stats.get('offense_plays', 1)
    
    # Build offensive_normalized metrics from stats
    team_obj['detailed_metrics'] = {
        'offensive_normalized': {
            'offense_ppa': (stats.get('offense_ppa', 0) + 1) * 50,  # Scale to 0-100
            'offense_success_rate': stats.get('offense_successRate', 0.5) * 100,
            'offense_explosiveness': stats.get('offense_explosiveness', 0) * 8,
            'yards_per_play': (stats.get('totalYards', 0) / total_plays) * 1.5,
            'yards_per_game': (stats.get('totalYards', 0) / games) / 10,
            'third_down_pct': (stats.get('thirdDownConversions', 0) / max(stats.get('thirdDowns', 1), 1)) * 100,
            'fourth_down_pct': (stats.get('fourthDownConversions', 0) / max(stats.get('fourthDowns', 1), 1)) * 100,
            'first_downs_per_game': (stats.get('firstDowns', 0) / games) * 2,
            'points_per_opportunity': stats.get('offense_pointsPerOpportunity', 0) * 15,
            'passing_success': stats.get('offense_passingPlays', {}).get('successRate', 0.5) * 100,
            'passing_ppa': (stats.get('offense_passingPlays', {}).get('ppa', 0) + 1) * 50,
            'passing_explosiveness': stats.get('offense_passingPlays', {}).get('explosiveness', 0) * 10,
            'completion_pct': (stats.get('passCompletions', 0) / pass_attempts) * 100,
            'yards_per_pass': (stats.get('netPassingYards', 0) / pass_attempts) * 10,
            'pass_td_rate': (stats.get('passingTDs', 0) / pass_attempts) * 1000,
            'interception_pct': 100 - ((stats.get('passesIntercepted', 0) / pass_attempts) * 1000),
            'rushing_success': stats.get('offense_rushingPlays', {}).get('successRate', 0.5) * 100,
            'rushing_ppa': (stats.get('offense_rushingPlays', {}).get('ppa', 0) + 1) * 50,
            'rushing_explosiveness': stats.get('offense_rushingPlays', {}).get('explosiveness', 0) * 10,
            'yards_per_rush': (stats.get('rushingYards', 0) / rush_attempts) * 15,
            'rush_td_rate': (stats.get('rushingTDs', 0) / rush_attempts) * 300,
            'line_yards': stats.get('offense_lineYards', 0) * 20,
            'second_level_yards': stats.get('offense_secondLevelYards', 0) * 30,
            'open_field_yards': stats.get('offense_openFieldYards', 0) * 30,
            'power_success': stats.get('offense_powerSuccess', 0.5) * 100,
            'stuff_rate': (1 - stats.get('offense_stuffRate', 0.15)) * 100,
            'standard_downs_success': stats.get('offense_standardDowns', {}).get('successRate', 0.5) * 100,
            'standard_downs_ppa': (stats.get('offense_standardDowns', {}).get('ppa', 0) + 1) * 50,
            'passing_downs_success': stats.get('offense_passingDowns', {}).get('successRate', 0.3) * 150,
            'passing_downs_ppa': (stats.get('offense_passingDowns', {}).get('ppa', 0) + 1) * 50,
            'turnover_margin': ((stats.get('turnoversOpponent', 0) - stats.get('turnovers', 0)) / games + 2) * 25,
            'possession_time_pct': (stats.get('possessionTime', 18000) / (stats.get('possessionTime', 18000) + stats.get('possessionTimeOpponent', 18000))) * 100,
            'avg_starting_field_position': stats.get('offense_fieldPosition', {}).get('averageStart', 70),
            'avg_predicted_points_start': (stats.get('offense_fieldPosition', {}).get('averagePredictedPoints', 1.2) + 1) * 30,
            'offense_havoc_total': stats.get('offense_havoc', {}).get('total', 0.08) * 600,
            'offense_havoc_front_seven': stats.get('offense_havoc', {}).get('frontSeven', 0.06) * 800,
            'offense_havoc_db': stats.get('offense_havoc', {}).get('db', 0.02) * 1500,
            'kick_return_avg': (stats.get('kickReturnYards', 0) / max(stats.get('kickReturns', 1), 1)) * 3,
            'punt_return_avg': (stats.get('puntReturnYards', 0) / max(stats.get('puntReturns', 1), 1)) * 5,
            'penalty_yards_per_game': 100 - ((stats.get('penaltyYards', 0) / games) / 2)
        },
        'defensive_normalized': {}
    }

# Save back
with open('frontend/src/data/comprehensive_power_rankings.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added detailed_metrics to {len(data['teams'])} teams")
print(f"📊 Sample: {data['teams'][0]['team']} Offensive EPA = {data['teams'][0]['detailed_metrics']['offensive_normalized']['offense_ppa']:.1f}")
