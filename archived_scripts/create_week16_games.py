import os
import json
import requests

# Load API key (use same key as app.py)
api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')

# Fetch Week 16 games
url = "https://api.collegefootballdata.com/games?year=2025&week=16&seasonType=regular"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit(1)

games = response.json()

# Format for frontend
output = {"data": {"game": []}}
for g in games:
    output["data"]["game"].append({
        "id": g["id"],
        "season": g["season"],
        "week": g["week"],
        "seasonType": g["season_type"],
        "startDate": g["start_date"],
        "homeTeam": g["home_team"],
        "awayTeam": g["away_team"],
        "homeTeamId": g.get("home_id"),
        "awayTeamId": g.get("away_id"),
        "homePoints": g.get("home_points"),
        "awayPoints": g.get("away_points"),
        "weather": {
            "temperature": None,
            "windSpeed": None,
            "precipitation": None,
            "humidity": None
        }
    })

# Write to file
with open("frontend/public/week16_games.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"✓ Created week16_games.json with {len(output['data']['game'])} games")
print("\nGames included:")
for g in output["data"]["game"]:
    print(f"  - {g['awayTeam']} @ {g['homeTeam']}")
