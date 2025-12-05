#!/usr/bin/env python3
"""
Comprehensive Tight End Analysis 2025
Enhanced analysis with ALL available TE metrics including receiving stats and advanced efficiency calculations.
"""

import requests
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# Configuration
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
GRAPHQL_ENDPOINT = "https://graphql.collegefootballdata.com/v1/graphql"
SEASON = 2025

@dataclass
class ComprehensiveTEStats:
    """Enhanced tight end statistics container with ALL metrics"""
    name: str
    team: str
    athlete_id: int
    games_played: int = 0
    
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_tds: int = 0
    receiving_avg: float = 0.0
    longest_reception: int = 0
    
    # Calculated basic metrics
    yards_per_reception: float = 0.0
    yards_per_game: float = 0.0
    receptions_per_game: float = 0.0
    
    # Advanced efficiency metrics
    catch_rate: float = 0.0  # Would need targets data
    big_play_rate: float = 0.0  # 20+ yard receptions
    red_zone_efficiency: float = 0.0
    touchdown_rate: float = 0.0  # TDs per reception
    
    # Situational metrics
    conference_games: int = 0
    conference_performance: float = 0.0
    
    # Overall efficiency score
    comprehensive_efficiency_score: float = 0.0

# Headers for GraphQL requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Query to get all FBS teams
ALL_TEAMS_QUERY = """
query AllFBSTeams {
  currentTeams(
    where: {
      classification: { _eq: "fbs" }
    }
    orderBy: { school: ASC }
  ) {
    teamId
    school
    conference
  }
}
"""

# Enhanced TE Statistics Query - receiving category
TE_STATS_QUERY = """
query TEStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _eq: "TE" } }
      }
      playerStatCategory: { 
        name: { _in: ["receiving"] }
      }
    }
  ) {
    athlete {
      id
      name
      position {
        abbreviation
        name
      }
    }
    gameTeam {
      teamId
      game {
        week
        season
        homeTeam
        awayTeam
        homePoints
        awayPoints
        conferenceGame
      }
    }
    playerStatCategory {
      name
    }
    playerStatType {
      name
    }
    stat
  }
}
"""

def make_graphql_request(query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make a GraphQL request with error handling."""
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        response = requests.post(GRAPHQL_ENDPOINT, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"data": None, "errors": [str(e)]}

def process_receiving_stats(te: ComprehensiveTEStats, stat_type: str, stat_value: str):
    """Process receiving statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "REC":
            te.receptions += int(float(stat_value))
        elif stat_type == "YDS":
            te.receiving_yards += int(float(stat_value))
        elif stat_type == "TD":
            te.receiving_tds += int(float(stat_value))
        elif stat_type == "AVG":
            # AVG is calculated later from total yards/receptions
            pass
        elif stat_type == "LONG":
            # Keep the longest reception across all games
            current_long = int(float(stat_value))
            te.longest_reception = max(te.longest_reception, current_long)
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(te: ComprehensiveTEStats):
    """Calculate all comprehensive efficiency metrics for a tight end."""
    # Basic efficiency metrics
    if te.receptions > 0:
        te.yards_per_reception = te.receiving_yards / te.receptions
        te.receiving_avg = te.yards_per_reception  # Set the avg field
        te.touchdown_rate = (te.receiving_tds / te.receptions) * 100
    
    if te.games_played > 0:
        te.yards_per_game = te.receiving_yards / te.games_played
        te.receptions_per_game = te.receptions / te.games_played
    
    # Big play rate (20+ yard receptions - approximated by longest reception)
    if te.longest_reception >= 20:
        te.big_play_rate = min(25.0, te.longest_reception / 4)  # Rough approximation
    
    # Conference performance
    if te.conference_games > 0 and te.games_played > 0:
        te.conference_performance = (te.conference_games / te.games_played) * 100
    
    # Comprehensive efficiency score calculation
    # Factors: yards per reception, touchdown rate, volume, big plays
    base_score = 0.0
    
    if te.receptions >= 3:  # Minimum threshold for meaningful analysis (lower for TEs)
        # Yards per reception component (0-100 scale)
        ypr_score = min(100, (te.yards_per_reception / 18) * 100)  # Slightly lower expectation for TEs
        
        # Volume component (0-50 scale) - adjusted for TE expectations
        volume_score = min(50, (te.receptions / 60) * 50)  # Lower volume expectations for TEs
        
        # Touchdown component (0-100 scale)
        td_score = min(100, te.touchdown_rate * 10)
        
        # Big play component (0-50 scale)
        big_play_score = min(50, te.big_play_rate * 2)
        
        # Combine components
        base_score = (ypr_score * 0.4) + (volume_score * 0.3) + (td_score * 0.2) + (big_play_score * 0.1)
    
    te.comprehensive_efficiency_score = base_score

def fetch_te_stats_for_team(team_id: int, team_name: str) -> List[ComprehensiveTEStats]:
    """Fetch and process TE stats for a specific team."""
    print(f"Fetching TE stats for {team_name}...")
    
    variables = {
        "teamId": team_id,
        "season": SEASON
    }
    
    result = make_graphql_request(TE_STATS_QUERY, variables)
    
    if result.get("errors"):
        print(f"❌ Error fetching TE stats for {team_name}: {result['errors']}")
        return []
    
    if not result.get("data") or not result["data"].get("gamePlayerStat"):
        return []
    
    # Group stats by athlete and aggregate across all games
    te_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}
    
    for stat in result["data"]["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if not athlete_id:
            continue
        
        # Initialize TE if not exists
        if athlete_id not in te_stats_dict:
            te_stats_dict[athlete_id] = ComprehensiveTEStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()
        
        te = te_stats_dict[athlete_id]
        
        # Track unique games played
        game_team = stat.get("gameTeam", {})
        game = game_team.get("game", {})
        game_week = game.get("week")
        if game_week:
            games_played_dict[athlete_id].add(game_week)
            if game.get("conferenceGame", False):
                conference_games_dict[athlete_id].add(game_week)
        
        # Process stats by category - ACCUMULATE across all games
        category = stat.get("playerStatCategory", {}).get("name", "")
        stat_type = stat.get("playerStatType", {}).get("name", "")
        stat_value = stat.get("stat", "0")
        
        if category == "receiving":
            process_receiving_stats(te, stat_type, stat_value)
    
    # Set final games played counts
    for athlete_id in te_stats_dict:
        te_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        te_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each TE
    te_list = list(te_stats_dict.values())
    for te in te_list:
        calculate_comprehensive_metrics(te)
    
    return te_list

def main():
    """Main analysis function."""
    print("=" * 100)
    print("COMPREHENSIVE TIGHT END ANALYSIS 2025")
    print("=" * 100)
    
    # Fetch all FBS teams
    print("Fetching all FBS teams...")
    teams_result = make_graphql_request(ALL_TEAMS_QUERY)
    
    if teams_result.get("errors") or not teams_result.get("data"):
        print(f"❌ Failed to fetch teams: {teams_result.get('errors', 'No data returned')}")
        return
    
    teams = teams_result["data"]["currentTeams"]
    print(f"Found {len(teams)} FBS teams")
    
    # Process each team
    all_tes = []
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        team_tes = fetch_te_stats_for_team(team_id, team_name)
        all_tes.extend(team_tes)
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total TEs found: {len(all_tes)}")
    
    # Filter for qualified TEs (minimum 3 receptions for broader analysis)
    qualified_tes = [te for te in all_tes if te.receptions >= 3]
    print(f"Qualified TEs (3+ receptions): {len(qualified_tes)}")
    
    # Also show breakdown by reception thresholds
    rec_15_plus = [te for te in all_tes if te.receptions >= 15]
    rec_10_plus = [te for te in all_tes if te.receptions >= 10]
    rec_5_plus = [te for te in all_tes if te.receptions >= 5]
    
    print(f"  • 15+ receptions: {len(rec_15_plus)} TEs")
    print(f"  • 10+ receptions: {len(rec_10_plus)} TEs") 
    print(f"  • 5+ receptions: {len(rec_5_plus)} TEs")
    print(f"  • 3+ receptions: {len(qualified_tes)} TEs (using for analysis)")
    
    if not qualified_tes:
        print("❌ No qualified TEs found!")
        return

    # Sort by different metrics
    comprehensive_sorted = sorted(qualified_tes, key=lambda x: x.comprehensive_efficiency_score, reverse=True)
    yards_sorted = sorted(qualified_tes, key=lambda x: x.receiving_yards, reverse=True)
    ypr_sorted = sorted(qualified_tes, key=lambda x: x.yards_per_reception, reverse=True)
    td_sorted = sorted(qualified_tes, key=lambda x: x.receiving_tds, reverse=True)
    volume_sorted = sorted(qualified_tes, key=lambda x: x.receptions, reverse=True)

    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save comprehensive analysis
    analysis_data = {
        "metadata": {
            "analysis_type": "comprehensive_te_analysis",
            "season": SEASON,
            "timestamp": timestamp,
            "total_tes": len(all_tes),
            "qualified_tes": len(qualified_tes),
            "minimum_receptions": 3,
            "teams_analyzed": len(teams)
        },
        "all_tes": [asdict(te) for te in qualified_tes]
    }

    filename = f"player_metrics/te/comprehensive_te_analysis_{SEASON}_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    print(f"✅ Comprehensive analysis saved: {filename}")

    # Save individual rankings
    rankings = {
        "comprehensive_efficiency_score": comprehensive_sorted,
        "receiving_yards": yards_sorted,
        "yards_per_reception": ypr_sorted,
        "receiving_touchdowns": td_sorted,
        "total_receptions": volume_sorted
    }

    for ranking_name, ranking_data in rankings.items():
        ranking_filename = f"player_metrics/te/te_{ranking_name}_rankings_{SEASON}_{timestamp}.json"
        ranking_json = {
            "metadata": {
                "ranking_type": ranking_name,
                "season": SEASON,
                "timestamp": timestamp,
                "total_players": len(ranking_data)
            },
            "rankings": [asdict(te) for te in ranking_data]
        }
        with open(ranking_filename, 'w') as f:
            json.dump(ranking_json, f, indent=2)
        print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_filename}")

    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP TIGHT END PERFORMERS 2025")
    print("=" * 100)

    print(f"\n🥇 TOP 25 COMPREHENSIVE TE EFFICIENCY:")
    print("-" * 80)
    for i, te in enumerate(comprehensive_sorted[:25], 1):
        print(f"{i:2d}. {te.name:<25} ({te.team:<30}) - {te.comprehensive_efficiency_score:6.1f} eff")
        print(f"    📊 {te.receptions:3d} rec, {te.receiving_yards:4d} yards, {te.receiving_tds:2d} TDs, {te.yards_per_reception:4.1f} YPR")

    print(f"\n💨 TOP 15 YARDS PER RECEPTION (5+ receptions):")
    print("-" * 80)
    ypr_qualified = [te for te in ypr_sorted if te.receptions >= 5]
    for i, te in enumerate(ypr_qualified[:15], 1):
        print(f"{i:2d}. {te.name:<25} ({te.team:<30}) - {te.yards_per_reception:5.1f} YPR")
        print(f"    🎯 {te.receptions:3d} rec, {te.receiving_yards:4d} yards, {te.receiving_tds:2d} TDs, {te.longest_reception:2d} long")

    print(f"\n🎯 TOP 15 TOUCHDOWN LEADERS:")
    print("-" * 80)
    for i, te in enumerate(td_sorted[:15], 1):
        print(f"{i:2d}. {te.name:<25} ({te.team:<30}) - {te.receiving_tds:2d} TDs")
        print(f"    📊 {te.receptions:3d} rec, {te.receiving_yards:4d} yards, {te.yards_per_reception:4.1f} YPR, {te.touchdown_rate:4.1f}% TD rate")

    print(f"\n📈 TOP 15 TOTAL RECEIVING YARDS:")
    print("-" * 80)
    for i, te in enumerate(yards_sorted[:15], 1):
        print(f"{i:2d}. {te.name:<25} ({te.team:<30}) - {te.receiving_yards:4d} yards")
        print(f"    📊 {te.receptions:3d} rec, {te.receiving_tds:2d} TDs, {te.yards_per_reception:4.1f} YPR, {te.yards_per_game:4.1f} YPG")

    print(f"\n🔥 TOP 15 VOLUME LEADERS (Total Receptions):")
    print("-" * 80)
    for i, te in enumerate(volume_sorted[:15], 1):
        print(f"{i:2d}. {te.name:<25} ({te.team:<30}) - {te.receptions:3d} receptions")
        print(f"    📊 {te.receiving_yards:4d} yards, {te.receiving_tds:2d} TDs, {te.yards_per_reception:4.1f} YPR, {te.receptions_per_game:4.1f} RPG")

    print(f"\n✅ Analysis complete! All files saved to player_metrics/te/ directory.")

if __name__ == "__main__":
    main()
