#!/usr/bin/env python3
"""
Comprehensive Linebacker Analysis 2025
Enhanced analysis with ALL available LB metrics including defensive stats and advanced efficiency calculations.
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
class ComprehensiveLBStats:
    """Enhanced linebacker statistics container with ALL metrics"""
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
    interceptions: int = 0
    fumbles_forced: int = 0
    fumbles_recovered: int = 0
    
    # Calculated basic metrics
    tackles_per_game: float = 0.0
    sacks_per_game: float = 0.0
    tfl_per_game: float = 0.0
    interceptions_per_game: float = 0.0
    
    # Advanced efficiency metrics
    run_defense_impact: float = 0.0  # TFL + (tackles * 0.7) - weighted for LBs
    pass_rush_productivity: float = 0.0  # Sacks + QB hurries + PDs
    coverage_ability: float = 0.0  # INTs + PDs weighted
    turnover_creation: float = 0.0  # INTs + FF + FR
    linebacker_versatility: int = 0  # Tackles + TFL + sacks + INTs + PDs
    
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

# Enhanced LB Statistics Query - defensive category
LB_STATS_QUERY = """
query LBStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _in: ["LB", "MLB", "OLB", "ILB", "WLB", "SLB"] } }
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

def process_defensive_stats(lb: ComprehensiveLBStats, stat_type: str, stat_value: str):
    """Process defensive statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "TOT":  # Total tackles
            lb.tackles += int(float(stat_value))
        elif stat_type == "SOLO":  # Solo tackles (also count as tackles)
            lb.tackles += int(float(stat_value))
        elif stat_type == "TFL":  # Tackles for loss
            lb.tackles_for_loss += int(float(stat_value))
        elif stat_type == "SACKS":  # Sacks
            lb.sacks += int(float(stat_value))
        elif stat_type == "QB HUR":  # QB hurries
            lb.qb_hurries += int(float(stat_value))
        elif stat_type == "PD":  # Pass deflections
            lb.pass_deflections += int(float(stat_value))
        elif stat_type == "INT":  # Interceptions
            lb.interceptions += int(float(stat_value))
        elif stat_type == "FF":  # Fumbles forced
            lb.fumbles_forced += int(float(stat_value))
        elif stat_type == "FR":  # Fumbles recovered
            lb.fumbles_recovered += int(float(stat_value))
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(lb: ComprehensiveLBStats):
    """Calculate all comprehensive efficiency metrics for a linebacker."""
    # Basic efficiency metrics
    if lb.games_played > 0:
        lb.tackles_per_game = lb.tackles / lb.games_played
        lb.sacks_per_game = lb.sacks / lb.games_played
        lb.tfl_per_game = lb.tackles_for_loss / lb.games_played
        lb.interceptions_per_game = lb.interceptions / lb.games_played
    
    # Advanced metrics
    lb.run_defense_impact = lb.tackles_for_loss + (lb.tackles * 0.7)  # Weight tackles for LBs
    lb.pass_rush_productivity = lb.sacks + lb.qb_hurries + lb.pass_deflections
    lb.coverage_ability = (lb.interceptions * 3) + lb.pass_deflections  # Weight INTs higher
    lb.turnover_creation = lb.interceptions + lb.fumbles_forced + lb.fumbles_recovered
    lb.linebacker_versatility = lb.tackles + lb.tackles_for_loss + lb.sacks + lb.interceptions + lb.pass_deflections
    
    # Conference performance
    if lb.conference_games > 0 and lb.games_played > 0:
        lb.conference_performance = (lb.conference_games / lb.games_played) * 100
    
    # Comprehensive efficiency score calculation
    # Factors: run defense, pass rush, coverage, versatility
    base_score = 0.0
    
    if lb.games_played >= 3:  # Minimum threshold for meaningful analysis
        # Run defense component (0-40 scale) - tackles and TFL
        run_defense_score = min(40, (lb.tackles * 0.8) + (lb.tackles_for_loss * 5))
        
        # Pass rush component (0-25 scale) - sacks and hurries
        pass_rush_score = min(25, (lb.sacks * 8) + (lb.qb_hurries * 3))
        
        # Coverage component (0-20 scale) - INTs and PDs
        coverage_score = min(20, (lb.interceptions * 10) + (lb.pass_deflections * 4))
        
        # Versatility component (0-15 scale) - overall impact
        versatility_score = min(15, lb.linebacker_versatility * 0.3)
        
        # Combine components
        base_score = run_defense_score + pass_rush_score + coverage_score + versatility_score
    
    lb.comprehensive_efficiency_score = base_score

def fetch_lb_stats_for_team(team_id: int, team_name: str) -> List[ComprehensiveLBStats]:
    """Fetch and process LB stats for a specific team."""
    print(f"Fetching LB stats for {team_name}...")
    
    variables = {
        "teamId": team_id,
        "season": SEASON
    }
    
    result = make_graphql_request(LB_STATS_QUERY, variables)
    
    if result.get("errors"):
        print(f"❌ Error fetching LB stats for {team_name}: {result['errors']}")
        return []
    
    if not result.get("data") or not result["data"].get("gamePlayerStat"):
        return []
    
    # Group stats by athlete and aggregate across all games
    lb_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}
    
    for stat in result["data"]["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if not athlete_id:
            continue
        
        # Initialize LB if not exists
        if athlete_id not in lb_stats_dict:
            lb_stats_dict[athlete_id] = ComprehensiveLBStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()
        
        lb = lb_stats_dict[athlete_id]
        
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
            process_defensive_stats(lb, stat_type, stat_value)
    
    # Set final games played counts
    for athlete_id in lb_stats_dict:
        lb_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        lb_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each LB
    lb_list = list(lb_stats_dict.values())
    for lb in lb_list:
        calculate_comprehensive_metrics(lb)
    
    return lb_list

def main():
    """Main analysis function."""
    print("=" * 100)
    print("COMPREHENSIVE LINEBACKER ANALYSIS 2025")
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
    all_lbs = []
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        team_lbs = fetch_lb_stats_for_team(team_id, team_name)
        all_lbs.extend(team_lbs)
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total LBs found: {len(all_lbs)}")
    
    # Filter for qualified LBs (minimum 10 tackles for meaningful analysis)
    qualified_lbs = [lb for lb in all_lbs if lb.tackles >= 10]
    print(f"Qualified LBs (10+ tackles): {len(qualified_lbs)}")
    
    # Also show breakdown by tackle thresholds
    tackle_40_plus = [lb for lb in all_lbs if lb.tackles >= 40]
    tackle_25_plus = [lb for lb in all_lbs if lb.tackles >= 25]
    tackle_15_plus = [lb for lb in all_lbs if lb.tackles >= 15]
    
    print(f"  • 40+ tackles: {len(tackle_40_plus)} LBs")
    print(f"  • 25+ tackles: {len(tackle_25_plus)} LBs")
    print(f"  • 15+ tackles: {len(tackle_15_plus)} LBs") 
    print(f"  • 10+ tackles: {len(qualified_lbs)} LBs (using for analysis)")
    
    if not qualified_lbs:
        print("❌ No qualified LBs found!")
        return

    # Create output directory
    import os
    output_dir = "player_metrics/lb"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save comprehensive analysis
    comprehensive_file = f"{output_dir}/comprehensive_lb_analysis_2025_{timestamp}.json"
    comprehensive_data = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "season": SEASON,
            "total_lbs": len(all_lbs),
            "qualified_lbs": len(qualified_lbs),
            "minimum_tackles": 10
        },
        "lbs": [asdict(lb) for lb in qualified_lbs]
    }

    with open(comprehensive_file, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)
    print(f"✅ Comprehensive analysis saved: {comprehensive_file}")

    # Generate rankings
    rankings = {
        "comprehensive_efficiency_score": sorted(qualified_lbs, key=lambda x: x.comprehensive_efficiency_score, reverse=True),
        "total_tackles": sorted(qualified_lbs, key=lambda x: x.tackles, reverse=True),
        "total_sacks": sorted(qualified_lbs, key=lambda x: x.sacks, reverse=True),
        "tackles_for_loss": sorted(qualified_lbs, key=lambda x: x.tackles_for_loss, reverse=True),
        "run_defense_impact": sorted(qualified_lbs, key=lambda x: x.run_defense_impact, reverse=True),
        "linebacker_versatility": sorted(qualified_lbs, key=lambda x: x.linebacker_versatility, reverse=True)
    }

    # Save individual ranking files
    for ranking_name, ranking_data in rankings.items():
        ranking_file = f"{output_dir}/lb_{ranking_name}_rankings_2025_{timestamp}.json"
        ranking_export = {
            "metadata": {
                "ranking_type": ranking_name,
                "analysis_date": datetime.now().isoformat(),
                "season": SEASON,
                "total_players": len(ranking_data)
            },
            "rankings": [asdict(lb) for lb in ranking_data]
        }

        with open(ranking_file, 'w') as f:
            json.dump(ranking_export, f, indent=2)
        print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_file}")

    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP LINEBACKER PERFORMERS 2025")
    print("=" * 100)

    # Top 25 Comprehensive Efficiency
    print("\n🥇 TOP 25 COMPREHENSIVE LB EFFICIENCY:")
    print("-" * 80)
    for i, lb in enumerate(rankings["comprehensive_efficiency_score"][:25], 1):
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.comprehensive_efficiency_score:5.1f} eff")
        print(f"    🛡️  {lb.tackles:2d} tackles, {lb.sacks:2d} sacks, {lb.tackles_for_loss:2d} TFL, {lb.interceptions:2d} INTs, {lb.pass_deflections:2d} PDs")

    # Top 15 Total Tackles
    print(f"\n🛡️ TOP 15 TOTAL TACKLES:")
    print("-" * 80)
    for i, lb in enumerate(rankings["total_tackles"][:15], 1):
        tackles_per_game = lb.tackles_per_game if lb.games_played > 0 else 0
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.tackles:2d} tackles")
        print(f"    🛡️  {lb.sacks:2d} sacks, {lb.tackles_for_loss:2d} TFL, {tackles_per_game:.1f} TPG, {lb.games_played:2d} games")

    # Top 15 Sack Leaders
    print(f"\n💥 TOP 15 SACK LEADERS:")
    print("-" * 80)
    for i, lb in enumerate(rankings["total_sacks"][:15], 1):
        sacks_per_game = lb.sacks_per_game if lb.games_played > 0 else 0
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.sacks:2d} sacks")
        print(f"    💥  {lb.tackles:2d} tackles, {lb.tackles_for_loss:2d} TFL, {sacks_per_game:.1f} SPG, {lb.games_played:2d} games")

    # Top 15 Tackles for Loss
    print(f"\n🚫 TOP 15 TACKLES FOR LOSS:")
    print("-" * 80)
    for i, lb in enumerate(rankings["tackles_for_loss"][:15], 1):
        tfl_per_game = lb.tfl_per_game if lb.games_played > 0 else 0
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.tackles_for_loss:2d} TFL")
        print(f"    🚫  {lb.tackles:2d} tackles, {lb.sacks:2d} sacks, {tfl_per_game:.1f} TFLPG, {lb.games_played:2d} games")

    # Top 15 Run Defense Impact
    print(f"\n🏃‍♂️ TOP 15 RUN DEFENSE IMPACT:")
    print("-" * 80)
    for i, lb in enumerate(rankings["run_defense_impact"][:15], 1):
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.run_defense_impact:5.1f} impact")
        print(f"    🏃‍♂️  {lb.tackles_for_loss:2d} TFL + ({lb.tackles:2d} tackles × 0.7) = {lb.run_defense_impact:.1f}")

    # Top 15 Linebacker Versatility
    print(f"\n🎯 TOP 15 LINEBACKER VERSATILITY:")
    print("-" * 80)
    for i, lb in enumerate(rankings["linebacker_versatility"][:15], 1):
        print(f"{i:2d}. {lb.name:<25} ({lb.team:<35}) - {lb.linebacker_versatility:2d} versatility")
        print(f"    🎯  {lb.tackles:2d} tackles + {lb.tackles_for_loss:2d} TFL + {lb.sacks:2d} sacks + {lb.interceptions:2d} INTs + {lb.pass_deflections:2d} PDs")

    print(f"\n✅ Analysis complete! All files saved to {output_dir}/ directory.")

if __name__ == "__main__":
    main()
