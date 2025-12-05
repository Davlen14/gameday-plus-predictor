#!/usr/bin/env python3
"""
Comprehensive Wide Receiver Analysis 2025
Enhanced analysis with ALL available WR metrics including receiving stats and advanced efficiency calculations.
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
class ComprehensiveWRStats:
    """Enhanced wide receiver statistics container with ALL metrics"""
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

# Enhanced WR Statistics Query - receiving category
WR_STATS_QUERY = """
query WRStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _eq: "WR" } }
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

def process_receiving_stats(wr: ComprehensiveWRStats, stat_type: str, stat_value: str):
    """Process receiving statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "REC":
            wr.receptions += int(float(stat_value))
        elif stat_type == "YDS":
            wr.receiving_yards += int(float(stat_value))
        elif stat_type == "TD":
            wr.receiving_tds += int(float(stat_value))
        elif stat_type == "AVG":
            # AVG is calculated later from total yards/receptions
            pass
        elif stat_type == "LONG":
            # Keep the longest reception across all games
            current_long = int(float(stat_value))
            wr.longest_reception = max(wr.longest_reception, current_long)
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(wr: ComprehensiveWRStats):
    """Calculate all comprehensive efficiency metrics for a wide receiver."""
    # Basic efficiency metrics
    if wr.receptions > 0:
        wr.yards_per_reception = wr.receiving_yards / wr.receptions
        wr.receiving_avg = wr.yards_per_reception  # Set the avg field
        wr.touchdown_rate = (wr.receiving_tds / wr.receptions) * 100
    
    if wr.games_played > 0:
        wr.yards_per_game = wr.receiving_yards / wr.games_played
        wr.receptions_per_game = wr.receptions / wr.games_played
    
    # Big play rate (20+ yard receptions - approximated by longest reception)
    if wr.longest_reception >= 20:
        wr.big_play_rate = min(25.0, wr.longest_reception / 4)  # Rough approximation
    
    # Conference performance
    if wr.conference_games > 0 and wr.games_played > 0:
        wr.conference_performance = (wr.conference_games / wr.games_played) * 100
    
    # Comprehensive efficiency score calculation
    # Factors: yards per reception, touchdown rate, volume, big plays
    base_score = 0.0
    
    if wr.receptions >= 5:  # Minimum threshold for meaningful analysis
        # Yards per reception component (0-100 scale)
        ypr_score = min(100, (wr.yards_per_reception / 20) * 100)
        
        # Volume component (0-50 scale)
        volume_score = min(50, (wr.receptions / 100) * 50)
        
        # Touchdown component (0-100 scale)
        td_score = min(100, wr.touchdown_rate * 10)
        
        # Big play component (0-50 scale)
        big_play_score = min(50, wr.big_play_rate * 2)
        
        # Combine components
        base_score = (ypr_score * 0.4) + (volume_score * 0.3) + (td_score * 0.2) + (big_play_score * 0.1)
    
    wr.comprehensive_efficiency_score = base_score

def fetch_wr_stats_for_team(team_id: int, team_name: str) -> List[ComprehensiveWRStats]:
    """Fetch and process WR stats for a specific team."""
    print(f"Fetching WR stats for {team_name}...")
    
    variables = {
        "teamId": team_id,
        "season": SEASON
    }
    
    result = make_graphql_request(WR_STATS_QUERY, variables)
    
    if result.get("errors"):
        print(f"❌ Error fetching WR stats for {team_name}: {result['errors']}")
        return []
    
    if not result.get("data") or not result["data"].get("gamePlayerStat"):
        return []
    
    # Group stats by athlete and aggregate across all games
    wr_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}
    
    for stat in result["data"]["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if not athlete_id:
            continue
        
        # Initialize WR if not exists
        if athlete_id not in wr_stats_dict:
            wr_stats_dict[athlete_id] = ComprehensiveWRStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()
        
        wr = wr_stats_dict[athlete_id]
        
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
            process_receiving_stats(wr, stat_type, stat_value)
    
    # Set final games played counts
    for athlete_id in wr_stats_dict:
        wr_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        wr_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each WR
    wr_list = list(wr_stats_dict.values())
    for wr in wr_list:
        calculate_comprehensive_metrics(wr)
    
    return wr_list

def main():
    """Main analysis function."""
    print("=" * 100)
    print("COMPREHENSIVE WIDE RECEIVER ANALYSIS 2025")
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
    all_wrs = []
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        team_wrs = fetch_wr_stats_for_team(team_id, team_name)
        all_wrs.extend(team_wrs)
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total WRs found: {len(all_wrs)}")
    
    # Filter for qualified WRs (minimum 5 receptions for broader analysis)
    qualified_wrs = [wr for wr in all_wrs if wr.receptions >= 5]
    print(f"Qualified WRs (5+ receptions): {len(qualified_wrs)}")
    
    # Also show breakdown by reception thresholds
    rec_25_plus = [wr for wr in all_wrs if wr.receptions >= 25]
    rec_15_plus = [wr for wr in all_wrs if wr.receptions >= 15]
    rec_10_plus = [wr for wr in all_wrs if wr.receptions >= 10]
    
    print(f"  • 25+ receptions: {len(rec_25_plus)} WRs")
    print(f"  • 15+ receptions: {len(rec_15_plus)} WRs") 
    print(f"  • 10+ receptions: {len(rec_10_plus)} WRs")
    print(f"  • 5+ receptions: {len(qualified_wrs)} WRs (using for analysis)")
    
    if not qualified_wrs:
        print("❌ No qualified WRs found!")
        return

    # Sort by different metrics
    comprehensive_sorted = sorted(qualified_wrs, key=lambda x: x.comprehensive_efficiency_score, reverse=True)
    yards_sorted = sorted(qualified_wrs, key=lambda x: x.receiving_yards, reverse=True)
    ypr_sorted = sorted(qualified_wrs, key=lambda x: x.yards_per_reception, reverse=True)
    td_sorted = sorted(qualified_wrs, key=lambda x: x.receiving_tds, reverse=True)
    volume_sorted = sorted(qualified_wrs, key=lambda x: x.receptions, reverse=True)

    # Generate timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save comprehensive analysis
    analysis_data = {
        "metadata": {
            "analysis_type": "comprehensive_wr_analysis",
            "season": SEASON,
            "timestamp": timestamp,
            "total_wrs": len(all_wrs),
            "qualified_wrs": len(qualified_wrs),
            "minimum_receptions": 5,
            "teams_analyzed": len(teams)
        },
        "all_wrs": [asdict(wr) for wr in qualified_wrs]
    }

    filename = f"player_metrics/wr/comprehensive_wr_analysis_{SEASON}_{timestamp}.json"
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
        ranking_filename = f"player_metrics/wr/wr_{ranking_name}_rankings_{SEASON}_{timestamp}.json"
        ranking_json = {
            "metadata": {
                "ranking_type": ranking_name,
                "season": SEASON,
                "timestamp": timestamp,
                "total_players": len(ranking_data)
            },
            "rankings": [asdict(wr) for wr in ranking_data]
        }
        with open(ranking_filename, 'w') as f:
            json.dump(ranking_json, f, indent=2)
        print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_filename}")

    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP WIDE RECEIVER PERFORMERS 2025")
    print("=" * 100)

    print(f"\n🥇 TOP 25 COMPREHENSIVE WR EFFICIENCY:")
    print("-" * 80)
    for i, wr in enumerate(comprehensive_sorted[:25], 1):
        print(f"{i:2d}. {wr.name:<25} ({wr.team:<30}) - {wr.comprehensive_efficiency_score:6.1f} eff")
        print(f"    📊 {wr.receptions:3d} rec, {wr.receiving_yards:4d} yards, {wr.receiving_tds:2d} TDs, {wr.yards_per_reception:4.1f} YPR")

    print(f"\n💨 TOP 15 YARDS PER RECEPTION (10+ receptions):")
    print("-" * 80)
    ypr_qualified = [wr for wr in ypr_sorted if wr.receptions >= 10]
    for i, wr in enumerate(ypr_qualified[:15], 1):
        print(f"{i:2d}. {wr.name:<25} ({wr.team:<30}) - {wr.yards_per_reception:5.1f} YPR")
        print(f"    🎯 {wr.receptions:3d} rec, {wr.receiving_yards:4d} yards, {wr.receiving_tds:2d} TDs, {wr.longest_reception:2d} long")

    print(f"\n🎯 TOP 15 TOUCHDOWN LEADERS:")
    print("-" * 80)
    for i, wr in enumerate(td_sorted[:15], 1):
        print(f"{i:2d}. {wr.name:<25} ({wr.team:<30}) - {wr.receiving_tds:2d} TDs")
        print(f"    📊 {wr.receptions:3d} rec, {wr.receiving_yards:4d} yards, {wr.yards_per_reception:4.1f} YPR, {wr.touchdown_rate:4.1f}% TD rate")

    print(f"\n📈 TOP 15 TOTAL RECEIVING YARDS:")
    print("-" * 80)
    for i, wr in enumerate(yards_sorted[:15], 1):
        print(f"{i:2d}. {wr.name:<25} ({wr.team:<30}) - {wr.receiving_yards:4d} yards")
        print(f"    📊 {wr.receptions:3d} rec, {wr.receiving_tds:2d} TDs, {wr.yards_per_reception:4.1f} YPR, {wr.yards_per_game:4.1f} YPG")

    print(f"\n🔥 TOP 15 VOLUME LEADERS (Total Receptions):")
    print("-" * 80)
    for i, wr in enumerate(volume_sorted[:15], 1):
        print(f"{i:2d}. {wr.name:<25} ({wr.team:<30}) - {wr.receptions:3d} receptions")
        print(f"    📊 {wr.receiving_yards:4d} yards, {wr.receiving_tds:2d} TDs, {wr.yards_per_reception:4.1f} YPR, {wr.receptions_per_game:4.1f} RPG")

    print(f"\n✅ Analysis complete! All files saved to player_metrics/wr/ directory.")

if __name__ == "__main__":
    main()
