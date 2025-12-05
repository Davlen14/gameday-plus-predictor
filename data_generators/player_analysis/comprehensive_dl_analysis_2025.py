#!/usr/bin/env python3
"""
Comprehensive Defensive Line Analysis 2025
Enhanced analysis with ALL available DL metrics including defensive stats and advanced efficiency calculations.
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
class ComprehensiveDLStats:
    """Enhanced defensive line statistics container with ALL metrics"""
    name: str
    team: str
    athlete_id: int
    games_played: int = 0
    
    # Defensive stats
    tackles: int = 0
    tackles_for_loss: int = 0
    sacks: int = 0
    qb_hurries: int = 0
    pass_deflections: int = 0
    fumbles_forced: int = 0
    fumbles_recovered: int = 0
    
    # Calculated basic metrics
    tackles_per_game: float = 0.0
    sacks_per_game: float = 0.0
    tfl_per_game: float = 0.0
    pressure_rate: float = 0.0  # (sacks + hurries) / games
    
    # Advanced efficiency metrics
    pass_rush_productivity: float = 0.0  # Sacks + hurries + PD
    run_defense_impact: float = 0.0  # TFL + tackles
    turnover_creation: float = 0.0  # FF + FR
    disruptive_plays: int = 0  # Sacks + TFL + PD + FF
    
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

# Enhanced DL Statistics Query - defensive category
DL_STATS_QUERY = """
query DLStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _in: ["DL", "DE", "DT", "NT"] } }
      }
      playerStatCategory: { 
        name: { _in: ["defensive"] }
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

def process_defensive_stats(dl: ComprehensiveDLStats, stat_type: str, stat_value: str):
    """Process defensive statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "TOT":  # Total tackles
            dl.tackles += int(float(stat_value))
        elif stat_type == "SOLO":  # Solo tackles (also count as tackles)
            dl.tackles += int(float(stat_value))
        elif stat_type == "TFL":  # Tackles for loss
            dl.tackles_for_loss += int(float(stat_value))
        elif stat_type == "SACKS":  # Sacks
            dl.sacks += int(float(stat_value))
        elif stat_type == "QB HUR":  # QB hurries
            dl.qb_hurries += int(float(stat_value))
        elif stat_type == "PD":  # Pass deflections
            dl.pass_deflections += int(float(stat_value))
        elif stat_type == "FF":  # Fumbles forced
            dl.fumbles_forced += int(float(stat_value))
        elif stat_type == "FR":  # Fumbles recovered
            dl.fumbles_recovered += int(float(stat_value))
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(dl: ComprehensiveDLStats):
    """Calculate all comprehensive efficiency metrics for a defensive lineman."""
    # Basic efficiency metrics
    if dl.games_played > 0:
        dl.tackles_per_game = dl.tackles / dl.games_played
        dl.sacks_per_game = dl.sacks / dl.games_played
        dl.tfl_per_game = dl.tackles_for_loss / dl.games_played
        dl.pressure_rate = (dl.sacks + dl.qb_hurries) / dl.games_played
    
    # Advanced metrics
    dl.pass_rush_productivity = dl.sacks + dl.qb_hurries + dl.pass_deflections
    dl.run_defense_impact = dl.tackles_for_loss + (dl.tackles * 0.5)  # Weight TFL higher
    dl.turnover_creation = dl.fumbles_forced + dl.fumbles_recovered
    dl.disruptive_plays = dl.sacks + dl.tackles_for_loss + dl.pass_deflections + dl.fumbles_forced
    
    # Conference performance
    if dl.conference_games > 0 and dl.games_played > 0:
        dl.conference_performance = (dl.conference_games / dl.games_played) * 100
    
    # Comprehensive efficiency score calculation
    # Factors: pass rush, run defense, disruptive plays, turnover creation
    base_score = 0.0
    
    if dl.games_played >= 3:  # Minimum threshold for meaningful analysis
        # Pass rush component (0-40 scale) - sacks and hurries
        pass_rush_score = min(40, (dl.sacks * 8) + (dl.qb_hurries * 3))
        
        # Run defense component (0-30 scale) - TFL and tackles
        run_defense_score = min(30, (dl.tackles_for_loss * 6) + (dl.tackles * 1))
        
        # Disruptive plays component (0-20 scale)
        disruptive_score = min(20, dl.disruptive_plays * 2)
        
        # Turnover component (0-10 scale)
        turnover_score = min(10, dl.turnover_creation * 5)
        
        # Combine components
        base_score = pass_rush_score + run_defense_score + disruptive_score + turnover_score
    
    dl.comprehensive_efficiency_score = base_score

def fetch_dl_stats_for_team(team_id: int, team_name: str) -> List[ComprehensiveDLStats]:
    """Fetch and process DL stats for a specific team."""
    print(f"Fetching DL stats for {team_name}...")
    
    variables = {
        "teamId": team_id,
        "season": SEASON
    }
    
    result = make_graphql_request(DL_STATS_QUERY, variables)
    
    if result.get("errors"):
        print(f"❌ Error fetching DL stats for {team_name}: {result['errors']}")
        return []
    
    if not result.get("data") or not result["data"].get("gamePlayerStat"):
        return []
    
    # Group stats by athlete and aggregate across all games
    dl_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}
    
    for stat in result["data"]["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if not athlete_id:
            continue
        
        # Initialize DL if not exists
        if athlete_id not in dl_stats_dict:
            dl_stats_dict[athlete_id] = ComprehensiveDLStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()
        
        dl = dl_stats_dict[athlete_id]
        
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
        
        if category == "defensive":
            process_defensive_stats(dl, stat_type, stat_value)
    
    # Set final games played counts
    for athlete_id in dl_stats_dict:
        dl_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        dl_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each DL
    dl_list = list(dl_stats_dict.values())
    for dl in dl_list:
        calculate_comprehensive_metrics(dl)
    
    return dl_list

def main():
    """Main analysis function."""
    print("=" * 100)
    print("COMPREHENSIVE DEFENSIVE LINE ANALYSIS 2025")
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
    all_dls = []
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        team_dls = fetch_dl_stats_for_team(team_id, team_name)
        all_dls.extend(team_dls)
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total DLs found: {len(all_dls)}")
    
    # Filter for qualified DLs (minimum 5 tackles for broader analysis)
    qualified_dls = [dl for dl in all_dls if dl.tackles >= 5]
    print(f"Qualified DLs (5+ tackles): {len(qualified_dls)}")
    
    # Also show breakdown by tackle thresholds
    tackle_25_plus = [dl for dl in all_dls if dl.tackles >= 25]
    tackle_15_plus = [dl for dl in all_dls if dl.tackles >= 15]
    tackle_10_plus = [dl for dl in all_dls if dl.tackles >= 10]
    
    print(f"  • 25+ tackles: {len(tackle_25_plus)} DLs")
    print(f"  • 15+ tackles: {len(tackle_15_plus)} DLs") 
    print(f"  • 10+ tackles: {len(tackle_10_plus)} DLs")
    print(f"  • 5+ tackles: {len(qualified_dls)} DLs (using for analysis)")
    
    if not qualified_dls:
        print("❌ No qualified DLs found!")
        return

    # Sort by different metrics
    comprehensive_sorted = sorted(qualified_dls, key=lambda x: x.comprehensive_efficiency_score, reverse=True)
    sacks_sorted = sorted(qualified_dls, key=lambda x: x.sacks, reverse=True)
    tfl_sorted = sorted(qualified_dls, key=lambda x: x.tackles_for_loss, reverse=True)
    tackles_sorted = sorted(qualified_dls, key=lambda x: x.tackles, reverse=True)
    pressure_sorted = sorted(qualified_dls, key=lambda x: x.pass_rush_productivity, reverse=True)
    disruptive_sorted = sorted(qualified_dls, key=lambda x: x.disruptive_plays, reverse=True)

    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save comprehensive analysis
    analysis_data = {
        "metadata": {
            "analysis_type": "comprehensive_dl_analysis",
            "season": SEASON,
            "timestamp": timestamp,
            "total_dls": len(all_dls),
            "qualified_dls": len(qualified_dls),
            "minimum_tackles": 5,
            "teams_analyzed": len(teams)
        },
        "all_dls": [asdict(dl) for dl in qualified_dls]
    }

    filename = f"player_metrics/dl/comprehensive_dl_analysis_{SEASON}_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    print(f"✅ Comprehensive analysis saved: {filename}")

    # Save individual rankings
    rankings = {
        "comprehensive_efficiency_score": comprehensive_sorted,
        "total_sacks": sacks_sorted,
        "tackles_for_loss": tfl_sorted,
        "total_tackles": tackles_sorted,
        "pass_rush_productivity": pressure_sorted,
        "disruptive_plays": disruptive_sorted
    }

    for ranking_name, ranking_data in rankings.items():
        ranking_filename = f"player_metrics/dl/dl_{ranking_name}_rankings_{SEASON}_{timestamp}.json"
        ranking_json = {
            "metadata": {
                "ranking_type": ranking_name,
                "season": SEASON,
                "timestamp": timestamp,
                "total_players": len(ranking_data)
            },
            "rankings": [asdict(dl) for dl in ranking_data]
        }
        with open(ranking_filename, 'w') as f:
            json.dump(ranking_json, f, indent=2)
        print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_filename}")

    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP DEFENSIVE LINE PERFORMERS 2025")
    print("=" * 100)

    print(f"\n🥇 TOP 25 COMPREHENSIVE DL EFFICIENCY:")
    print("-" * 80)
    for i, dl in enumerate(comprehensive_sorted[:25], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.comprehensive_efficiency_score:6.1f} eff")
        print(f"    🛡️ {dl.tackles:3d} tackles, {dl.sacks:2d} sacks, {dl.tackles_for_loss:2d} TFL, {dl.qb_hurries:2d} hurries")

    print(f"\n💥 TOP 15 SACK LEADERS:")
    print("-" * 80)
    for i, dl in enumerate(sacks_sorted[:15], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.sacks:2d} sacks")
        print(f"    🛡️ {dl.tackles:3d} tackles, {dl.tackles_for_loss:2d} TFL, {dl.qb_hurries:2d} hurries, {dl.sacks_per_game:4.1f} SPG")

    print(f"\n🚫 TOP 15 TACKLES FOR LOSS LEADERS:")
    print("-" * 80)
    for i, dl in enumerate(tfl_sorted[:15], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.tackles_for_loss:2d} TFL")
        print(f"    🛡️ {dl.tackles:3d} tackles, {dl.sacks:2d} sacks, {dl.qb_hurries:2d} hurries, {dl.tfl_per_game:4.1f} TFLPG")

    print(f"\n🏃‍♂️ TOP 15 PASS RUSH PRODUCTIVITY:")
    print("-" * 80)
    for i, dl in enumerate(pressure_sorted[:15], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.pass_rush_productivity:2d} pressure")
        print(f"    💨 {dl.sacks:2d} sacks + {dl.qb_hurries:2d} hurries + {dl.pass_deflections:2d} PD = {dl.pass_rush_productivity:2d} total")

    print(f"\n⚡ TOP 15 DISRUPTIVE PLAYS:")
    print("-" * 80)
    for i, dl in enumerate(disruptive_sorted[:15], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.disruptive_plays:2d} disruptive")
        print(f"    ⚡ {dl.sacks:2d} sacks + {dl.tackles_for_loss:2d} TFL + {dl.pass_deflections:2d} PD + {dl.fumbles_forced:2d} FF")

    print(f"\n🛡️ TOP 15 TOTAL TACKLES:")
    print("-" * 80)
    for i, dl in enumerate(tackles_sorted[:15], 1):
        print(f"{i:2d}. {dl.name:<25} ({dl.team:<30}) - {dl.tackles:3d} tackles")
        print(f"    🛡️ {dl.sacks:2d} sacks, {dl.tackles_for_loss:2d} TFL, {dl.tackles_per_game:4.1f} TPG, {dl.games_played:2d} games")

    print(f"\n✅ Analysis complete! All files saved to player_metrics/dl/ directory.")

if __name__ == "__main__":
    main()
