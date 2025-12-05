#!/usr/bin/env python3
"""
Comprehensive Defensive Back Analysis 2025
Enhanced analysis with ALL available DB metrics including defensive stats and advanced efficiency calculations.
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
class ComprehensiveDBStats:
    """Enhanced defensive back statistics container with ALL metrics"""
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
    interceptions_per_game: float = 0.0
    pass_deflections_per_game: float = 0.0
    coverage_disruption: float = 0.0  # INTs + PDs
    
    # Advanced efficiency metrics
    coverage_productivity: float = 0.0  # INTs + PDs + tackles
    ball_skills: float = 0.0  # INTs + PDs weighted
    turnover_creation: float = 0.0  # INTs + FF + FR
    defensive_impact: int = 0  # INTs + PDs + TFL + sacks
    
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

# Enhanced DB Statistics Query - defensive category
DB_STATS_QUERY = """
query DBStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _in: ["DB", "CB", "S", "FS", "SS"] } }
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

def process_defensive_stats(db: ComprehensiveDBStats, stat_type: str, stat_value: str):
    """Process defensive statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "TOT":  # Total tackles
            db.tackles += int(float(stat_value))
        elif stat_type == "SOLO":  # Solo tackles (also count as tackles)
            db.tackles += int(float(stat_value))
        elif stat_type == "TFL":  # Tackles for loss
            db.tackles_for_loss += int(float(stat_value))
        elif stat_type == "SACKS":  # Sacks
            db.sacks += int(float(stat_value))
        elif stat_type == "QB HUR":  # QB hurries
            db.qb_hurries += int(float(stat_value))
        elif stat_type == "PD":  # Pass deflections
            db.pass_deflections += int(float(stat_value))
        elif stat_type == "INT":  # Interceptions
            db.interceptions += int(float(stat_value))
        elif stat_type == "FF":  # Fumbles forced
            db.fumbles_forced += int(float(stat_value))
        elif stat_type == "FR":  # Fumbles recovered
            db.fumbles_recovered += int(float(stat_value))
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(db: ComprehensiveDBStats):
    """Calculate all comprehensive efficiency metrics for a defensive back."""
    # Basic efficiency metrics
    if db.games_played > 0:
        db.tackles_per_game = db.tackles / db.games_played
        db.interceptions_per_game = db.interceptions / db.games_played
        db.pass_deflections_per_game = db.pass_deflections / db.games_played
    
    # Advanced metrics
    db.coverage_disruption = db.interceptions + db.pass_deflections
    db.coverage_productivity = db.interceptions + db.pass_deflections + (db.tackles * 0.3)  # Weight tackles lower for DBs
    db.ball_skills = (db.interceptions * 3) + db.pass_deflections  # Weight INTs higher
    db.turnover_creation = db.interceptions + db.fumbles_forced + db.fumbles_recovered
    db.defensive_impact = db.interceptions + db.pass_deflections + db.tackles_for_loss + db.sacks
    
    # Conference performance
    if db.conference_games > 0 and db.games_played > 0:
        db.conference_performance = (db.conference_games / db.games_played) * 100
    
    # Comprehensive efficiency score calculation
    # Factors: coverage skills, ball skills, tackling, impact plays
    base_score = 0.0
    
    if db.games_played >= 3:  # Minimum threshold for meaningful analysis
        # Coverage component (0-40 scale) - INTs and PDs
        coverage_score = min(40, (db.interceptions * 10) + (db.pass_deflections * 4))
        
        # Ball skills component (0-30 scale) - weighted for INTs
        ball_skills_score = min(30, db.ball_skills * 2)
        
        # Tackling component (0-20 scale) - tackles and TFL
        tackling_score = min(20, (db.tackles * 0.5) + (db.tackles_for_loss * 3))
        
        # Impact plays component (0-10 scale) - sacks and turnovers
        impact_score = min(10, (db.sacks * 3) + (db.turnover_creation * 2))
        
        # Combine components
        base_score = coverage_score + ball_skills_score + tackling_score + impact_score
    
    db.comprehensive_efficiency_score = base_score

def fetch_db_stats_for_team(team_id: int, team_name: str) -> List[ComprehensiveDBStats]:
    """Fetch and process DB stats for a specific team."""
    print(f"Fetching DB stats for {team_name}...")
    
    variables = {
        "teamId": team_id,
        "season": SEASON
    }
    
    result = make_graphql_request(DB_STATS_QUERY, variables)
    
    if result.get("errors"):
        print(f"❌ Error fetching DB stats for {team_name}: {result['errors']}")
        return []
    
    if not result.get("data") or not result["data"].get("gamePlayerStat"):
        return []
    
    # Group stats by athlete and aggregate across all games
    db_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}
    
    for stat in result["data"]["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if not athlete_id:
            continue
        
        # Initialize DB if not exists
        if athlete_id not in db_stats_dict:
            db_stats_dict[athlete_id] = ComprehensiveDBStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()
        
        db = db_stats_dict[athlete_id]
        
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
            process_defensive_stats(db, stat_type, stat_value)
    
    # Set final games played counts
    for athlete_id in db_stats_dict:
        db_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        db_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each DB
    db_list = list(db_stats_dict.values())
    for db in db_list:
        calculate_comprehensive_metrics(db)
    
    return db_list

def main():
    """Main analysis function."""
    print("=" * 100)
    print("COMPREHENSIVE DEFENSIVE BACK ANALYSIS 2025")
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
    all_dbs = []
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        team_dbs = fetch_db_stats_for_team(team_id, team_name)
        all_dbs.extend(team_dbs)
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total DBs found: {len(all_dbs)}")
    
    # Filter for qualified DBs (minimum 5 tackles for broader analysis)
    qualified_dbs = [db for db in all_dbs if db.tackles >= 5]
    print(f"Qualified DBs (5+ tackles): {len(qualified_dbs)}")
    
    # Also show breakdown by tackle thresholds
    tackle_25_plus = [db for db in all_dbs if db.tackles >= 25]
    tackle_15_plus = [db for db in all_dbs if db.tackles >= 15]
    tackle_10_plus = [db for db in all_dbs if db.tackles >= 10]
    
    print(f"  • 25+ tackles: {len(tackle_25_plus)} DBs")
    print(f"  • 15+ tackles: {len(tackle_15_plus)} DBs") 
    print(f"  • 10+ tackles: {len(tackle_10_plus)} DBs")
    print(f"  • 5+ tackles: {len(qualified_dbs)} DBs (using for analysis)")
    
    if not qualified_dbs:
        print("❌ No qualified DBs found!")
        return

    # Create output directory
    import os
    output_dir = "player_metrics/db"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save comprehensive analysis
    comprehensive_file = f"{output_dir}/comprehensive_db_analysis_2025_{timestamp}.json"
    comprehensive_data = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "season": SEASON,
            "total_dbs": len(all_dbs),
            "qualified_dbs": len(qualified_dbs),
            "minimum_tackles": 5
        },
        "dbs": [asdict(db) for db in qualified_dbs]
    }

    with open(comprehensive_file, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)
    print(f"✅ Comprehensive analysis saved: {comprehensive_file}")

    # Generate rankings
    rankings = {
        "comprehensive_efficiency_score": sorted(qualified_dbs, key=lambda x: x.comprehensive_efficiency_score, reverse=True),
        "total_interceptions": sorted(qualified_dbs, key=lambda x: x.interceptions, reverse=True),
        "pass_deflections": sorted(qualified_dbs, key=lambda x: x.pass_deflections, reverse=True),
        "total_tackles": sorted(qualified_dbs, key=lambda x: x.tackles, reverse=True),
        "coverage_disruption": sorted(qualified_dbs, key=lambda x: x.coverage_disruption, reverse=True),
        "ball_skills": sorted(qualified_dbs, key=lambda x: x.ball_skills, reverse=True)
    }

    # Save individual ranking files
    for ranking_name, ranking_data in rankings.items():
        ranking_file = f"{output_dir}/db_{ranking_name}_rankings_2025_{timestamp}.json"
        ranking_export = {
            "metadata": {
                "ranking_type": ranking_name,
                "analysis_date": datetime.now().isoformat(),
                "season": SEASON,
                "total_players": len(ranking_data)
            },
            "rankings": [asdict(db) for db in ranking_data]
        }

        with open(ranking_file, 'w') as f:
            json.dump(ranking_export, f, indent=2)
        print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_file}")

    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP DEFENSIVE BACK PERFORMERS 2025")
    print("=" * 100)

    # Top 25 Comprehensive Efficiency
    print("\n🥇 TOP 25 COMPREHENSIVE DB EFFICIENCY:")
    print("-" * 80)
    for i, db in enumerate(rankings["comprehensive_efficiency_score"][:25], 1):
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.comprehensive_efficiency_score:5.1f} eff")
        print(f"    🛡️  {db.tackles:2d} tackles, {db.interceptions:2d} INTs, {db.pass_deflections:2d} PDs, {db.tackles_for_loss:2d} TFL")

    # Top 15 Interception Leaders
    print(f"\n🎯 TOP 15 INTERCEPTION LEADERS:")
    print("-" * 80)
    for i, db in enumerate(rankings["total_interceptions"][:15], 1):
        int_per_game = db.interceptions_per_game if db.games_played > 0 else 0
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.interceptions:2d} INTs")
        print(f"    🎯  {db.tackles:2d} tackles, {db.pass_deflections:2d} PDs, {int_per_game:.1f} IPG, {db.games_played:2d} games")

    # Top 15 Pass Deflection Leaders
    print(f"\n🚫 TOP 15 PASS DEFLECTION LEADERS:")
    print("-" * 80)
    for i, db in enumerate(rankings["pass_deflections"][:15], 1):
        pd_per_game = db.pass_deflections_per_game if db.games_played > 0 else 0
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.pass_deflections:2d} PDs")
        print(f"    🚫  {db.tackles:2d} tackles, {db.interceptions:2d} INTs, {pd_per_game:.1f} PDPG, {db.games_played:2d} games")

    # Top 15 Coverage Disruption
    print(f"\n🎭 TOP 15 COVERAGE DISRUPTION:")
    print("-" * 80)
    for i, db in enumerate(rankings["coverage_disruption"][:15], 1):
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.coverage_disruption:2d} disruption")
        print(f"    🎭  {db.interceptions:2d} INTs + {db.pass_deflections:2d} PDs = {db.coverage_disruption:2d} total")

    # Top 15 Ball Skills
    print(f"\n🏈 TOP 15 BALL SKILLS:")
    print("-" * 80)
    for i, db in enumerate(rankings["ball_skills"][:15], 1):
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.ball_skills:2.0f} ball skills")
        print(f"    🏈  {db.interceptions:2d} INTs × 3 + {db.pass_deflections:2d} PDs = {db.ball_skills:.0f} total")

    # Top 15 Total Tackles
    print(f"\n🛡️ TOP 15 TOTAL TACKLES:")
    print("-" * 80)
    for i, db in enumerate(rankings["total_tackles"][:15], 1):
        tackles_per_game = db.tackles_per_game if db.games_played > 0 else 0
        print(f"{i:2d}. {db.name:<25} ({db.team:<35}) - {db.tackles:2d} tackles")
        print(f"    🛡️  {db.sacks:2d} sacks, {db.tackles_for_loss:2d} TFL, {tackles_per_game:.1f} TPG, {db.games_played:2d} games")

    print(f"\n✅ Analysis complete! All files saved to {output_dir}/ directory.")

if __name__ == "__main__":
    main()
