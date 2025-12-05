"""
Quick test of ESPN player headshot integration
"""

from espn_player_service import ESPNPlayerService

# Test the service
service = ESPNPlayerService()

print("\n🏈 Testing ESPN Player Headshot Integration")
print("=" * 70)

# Test with a few teams
test_teams = ["Ohio State", "Michigan", "Alabama", "Georgia"]

for team in test_teams:
    print(f"\n📋 {team}:")
    roster = service.fetch_team_roster(team)
    if roster:
        # Show 3 players
        sample_players = list(roster.items())[:3]
        for name, data in sample_players:
            print(f"  ✓ {name} ({data['position']})")
            print(f"    {data['headshot_url']}")
    else:
        print(f"  ❌ No roster found")

# Test enrichment function
print("\n\n🎯 Testing Player Data Enrichment:")
print("=" * 70)

mock_player_data = {
    "home_players": {
        "qb": {"name": "Will Howard", "stats": {"passing_yards": 2500}},
        "wrs": [
            {"name": "Emeka Egbuka", "stats": {"receiving_yards": 800}},
            {"name": "Jeremiah Smith", "stats": {"receiving_yards": 750}}
        ]
    },
    "away_players": {
        "qb": {"name": "Davis Warren", "stats": {"passing_yards": 2200}},
        "wrs": [
            {"name": "Tyler Morris", "stats": {"receiving_yards": 650}}
        ]
    }
}

print("Before enrichment:")
print(f"  Ohio State QB: {mock_player_data['home_players']['qb']}")
print(f"  Michigan QB: {mock_player_data['away_players']['qb']}")

# Enrich data
enriched = service.enrich_player_data(mock_player_data['home_players'], "Ohio State")
enriched_away = service.enrich_player_data(mock_player_data['away_players'], "Michigan")

print("\nAfter enrichment:")
print(f"  Ohio State QB: {enriched['qb'].get('headshot_url', 'No headshot')}")
print(f"  Ohio State WR1: {enriched['wrs'][0].get('headshot_url', 'No headshot')}")
print(f"  Michigan QB: {enriched_away['qb'].get('headshot_url', 'No headshot')}")

print("\n✅ ESPN Player Headshot Integration Test Complete!")
