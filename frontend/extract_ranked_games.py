import json

# Read the JSON file
with open('Currentweekgames.json', 'r') as f:
    data = json.load(f)

print("🏈 WEEK 8 RANKED MATCHUPS ANALYSIS")
print("=" * 60)

ranked_matchups = []
ranked_vs_ranked = []

for game in data['games']['all']:
    home_rank = game['homeTeam']['rank']
    away_rank = game['awayTeam']['rank']
    
    # If either team is ranked, it's a ranked matchup
    if home_rank is not None or away_rank is not None:
        game_info = {
            'away': game['awayTeam']['name'],
            'away_rank': away_rank,
            'home': game['homeTeam']['name'], 
            'home_rank': home_rank,
            'datetime': game['datetime']['formatted'],
            'conference_game': game['gameInfo']['conferenceGame']
        }
        
        ranked_matchups.append(game_info)
        
        # If both teams are ranked, it's ranked vs ranked
        if home_rank is not None and away_rank is not None:
            ranked_vs_ranked.append(game_info)

print(f"📊 SUMMARY:")
print(f"   • Total Ranked Matchups: {len(ranked_matchups)}")
print(f"   • Ranked vs Ranked Games: {len(ranked_vs_ranked)}")
print()

print("🔥 RANKED vs RANKED GAMES (Top Priority):")
print("-" * 50)
for i, game in enumerate(ranked_vs_ranked, 1):
    away_str = f"#{game['away_rank']} {game['away']}"
    home_str = f"#{game['home_rank']} {game['home']}"
    conf_badge = " [CONF]" if game['conference_game'] else ""
    print(f"{i}. {away_str} @ {home_str}{conf_badge}")
    print(f"   📅 {game['datetime']}")
    print()

print("⚡ ALL RANKED MATCHUPS:")
print("-" * 40)
for i, game in enumerate(ranked_matchups, 1):
    away_str = f"#{game['away_rank']} {game['away']}" if game['away_rank'] else game['away']
    home_str = f"#{game['home_rank']} {game['home']}" if game['home_rank'] else game['home']
    conf_badge = " [CONF]" if game['conference_game'] else ""
    print(f"{i:2}. {away_str} @ {home_str}{conf_badge}")

print()
print("🏆 HIGHEST RANKED MATCHUPS (Top 10):")
print("-" * 45)
# Sort by highest rank (lowest number)
top_matchups = sorted(ranked_matchups, key=lambda x: min([r for r in [x['away_rank'], x['home_rank']] if r is not None]))[:10]
for i, game in enumerate(top_matchups, 1):
    away_str = f"#{game['away_rank']} {game['away']}" if game['away_rank'] else game['away']
    home_str = f"#{game['home_rank']} {game['home']}" if game['home_rank'] else game['home']
    highest_rank = min([r for r in [game['away_rank'], game['home_rank']] if r is not None])
    print(f"{i:2}. {away_str} @ {home_str} (Highest: #{highest_rank})")

