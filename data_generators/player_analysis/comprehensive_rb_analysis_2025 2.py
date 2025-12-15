#!/usr/bin/env python3
"""
Comprehensive Running Back Analysis 2025
This script analyzes all running backs across FBS teams with rushing and receiving metrics.
"""

import requests
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any

# API Configuration
GRAPHQL_ENDPOINT = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

@dataclass
class ComprehensiveRBStats:
    """Enhanced running back statistics container with ALL metrics"""
    name: str
    team: str
    athlete_id: int
    games_played: int = 0
    
    # Rushing stats
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_tds: int = 0
    rushing_avg: float = 0.0
    longest_rush: int = 0
    
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_tds: int = 0
    receiving_avg: float = 0.0
    longest_reception: int = 0
    
    # Calculated basic metrics
    yards_per_carry: float = 0.0
    yards_per_reception: float = 0.0
    yards_per_touch: float = 0.0
    
    # Dual-threat metrics
    total_touches: int = 0
    total_yards: int = 0
    total_tds: int = 0
    scrimmage_yards: int = 0
    
    # Advanced efficiency metrics
    dual_threat_efficiency: float = 0.0
    big_play_rate: float = 0.0
    touchdown_rate: float = 0.0
    usage_efficiency: float = 0.0
    
    # Situational metrics
    conference_games: int = 0
    conference_performance: float = 0.0
    
    # Overall efficiency score
    comprehensive_efficiency_score: float = 0.0

# GraphQL Query for comprehensive RB stats
COMPREHENSIVE_RB_STATS_QUERY = """
query ComprehensiveRBStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _eq: "RB" } }
      }
      playerStatCategory: { 
        name: { _in: ["rushing", "receiving"] }
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

def make_graphql_request(query: str, variables: dict = None):
    """Make a GraphQL request and return the response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        
        if "errors" in data:
            print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
            return None
        
        return data.get("data", {})
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

def process_rushing_stats(rb: ComprehensiveRBStats, stat_type: str, stat_value: str):
    """Process rushing statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "CAR":
            rb.rushing_attempts += int(float(stat_value))
        elif stat_type == "YDS":
            rb.rushing_yards += int(float(stat_value))
        elif stat_type == "TD":
            rb.rushing_tds += int(float(stat_value))
        elif stat_type == "AVG":
            # AVG is calculated later from total yards/attempts
            pass
        elif stat_type == "LONG":
            # Keep the longest rush across all games
            current_long = int(float(stat_value))
            rb.longest_rush = max(rb.longest_rush, current_long)
    except (ValueError, TypeError):
        pass

def process_receiving_stats(rb: ComprehensiveRBStats, stat_type: str, stat_value: str):
    """Process receiving statistics - ACCUMULATE across all games."""
    try:
        if stat_type == "REC":
            rb.receptions += int(float(stat_value))
        elif stat_type == "YDS":
            rb.receiving_yards += int(float(stat_value))
        elif stat_type == "TD":
            rb.receiving_tds += int(float(stat_value))
        elif stat_type == "AVG":
            # AVG is calculated later from total yards/receptions
            pass
        elif stat_type == "LONG":
            # Keep the longest reception across all games
            current_long = int(float(stat_value))
            rb.longest_reception = max(rb.longest_reception, current_long)
    except (ValueError, TypeError):
        pass

def calculate_comprehensive_metrics(rb: ComprehensiveRBStats):
    """Calculate all comprehensive efficiency metrics for a running back."""
    # Basic efficiency metrics
    if rb.rushing_attempts > 0:
        rb.yards_per_carry = rb.rushing_yards / rb.rushing_attempts
        rb.rushing_avg = rb.yards_per_carry  # Set the avg field

    if rb.receptions > 0:
        rb.yards_per_reception = rb.receiving_yards / rb.receptions
        rb.receiving_avg = rb.yards_per_reception  # Set the avg field
    
    # Dual-threat metrics
    rb.total_touches = rb.rushing_attempts + rb.receptions
    rb.total_yards = rb.rushing_yards + rb.receiving_yards
    rb.total_tds = rb.rushing_tds + rb.receiving_tds
    rb.scrimmage_yards = rb.total_yards  # Same as total yards for RBs
    
    if rb.total_touches > 0:
        rb.yards_per_touch = rb.total_yards / rb.total_touches
        rb.touchdown_rate = (rb.total_tds / rb.total_touches) * 100
    
    # Big play analysis
    big_plays = 0
    if rb.longest_rush >= 20:
        big_plays += 1
    if rb.longest_reception >= 20:
        big_plays += 1
    
    if rb.total_touches > 0:
        rb.big_play_rate = (big_plays / rb.total_touches) * 100
    
    # Dual-threat efficiency (combines rushing and receiving effectiveness)
    rushing_efficiency = 0
    receiving_efficiency = 0
    
    if rb.rushing_attempts > 0:
        rushing_efficiency = (rb.yards_per_carry * 10) + (rb.rushing_tds * 20)
    
    if rb.receptions > 0:
        receiving_efficiency = (rb.yards_per_reception * 5) + (rb.receiving_tds * 25)
    
    rb.dual_threat_efficiency = rushing_efficiency + receiving_efficiency
    
    # Usage efficiency (rewards high production with reasonable usage)
    if rb.total_touches > 0:
        volume_bonus = min(20, rb.total_touches / 5)  # Bonus for usage up to 100 touches
        efficiency_score = (rb.yards_per_touch * 8) + (rb.touchdown_rate * 10)
        rb.usage_efficiency = efficiency_score + volume_bonus
    
    # Comprehensive efficiency score (master metric)
    base_efficiency = rb.dual_threat_efficiency
    usage_bonus = min(15, rb.usage_efficiency * 0.3)
    big_play_bonus = rb.big_play_rate * 2
    volume_bonus = min(25, rb.total_touches / 4)
    
    rb.comprehensive_efficiency_score = (
        base_efficiency + 
        usage_bonus + 
        big_play_bonus + 
        volume_bonus
    )

def calculate_passer_rating(completions: int, attempts: int, yards: int, tds: int, ints: int) -> float:
    """Calculate NCAA passer rating."""
    if attempts == 0:
        return 0.0
    
    try:
        # NCAA Passer Rating Formula
        comp_pct = (completions / attempts) * 100
        yards_per_att = yards / attempts
        td_pct = (tds / attempts) * 100
        int_pct = (ints / attempts) * 100
        
        # Component calculations
        a = max(0, min(100, (comp_pct - 30) * 100 / 40))
        b = max(0, min(100, (yards_per_att - 3) * 100 / 5))
        c = max(0, min(100, td_pct * 100 / 9))
        d = max(0, min(100, (2.375 - int_pct) * 100 / 2.375))
        
        rating = (a + b + c + d) / 4
        return round(rating, 1)
    except:
        return 0.0

def fetch_team_rb_stats(team_id: int, team_name: str, season: int = 2025) -> List[ComprehensiveRBStats]:
    """Fetch comprehensive RB stats for a specific team."""
    print(f"Fetching RB stats for {team_name}...")
    
    variables = {
        "season": season,
        "teamId": team_id
    }
    
    result = make_graphql_request(COMPREHENSIVE_RB_STATS_QUERY, variables)
    
    if not result or "gamePlayerStat" not in result:
        print(f"No data returned for {team_name}")
        return []
    
    # Group stats by athlete and aggregate across all games
    rb_stats_dict = {}
    games_played_dict = {}
    conference_games_dict = {}

    for stat in result["gamePlayerStat"]:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")

        if not athlete_id:
            continue

        # Initialize RB if not exists
        if athlete_id not in rb_stats_dict:
            rb_stats_dict[athlete_id] = ComprehensiveRBStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
            games_played_dict[athlete_id] = set()
            conference_games_dict[athlete_id] = set()

        rb = rb_stats_dict[athlete_id]

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

        if category == "rushing":
            process_rushing_stats(rb, stat_type, stat_value)
        elif category == "receiving":
            process_receiving_stats(rb, stat_type, stat_value)

    # Set final games played counts
    for athlete_id in rb_stats_dict:
        rb_stats_dict[athlete_id].games_played = len(games_played_dict[athlete_id])
        rb_stats_dict[athlete_id].conference_games = len(conference_games_dict[athlete_id])
    
    # Calculate comprehensive metrics for each RB
    rbs = list(rb_stats_dict.values())
    for rb in rbs:
        calculate_comprehensive_metrics(rb)
    
    return rbs

def fetch_all_teams(season: int = 2025) -> List[Dict[str, Any]]:
    """Fetch all FBS teams."""
    print("Fetching all FBS teams...")

    result = make_graphql_request(ALL_TEAMS_QUERY)
    
    if result and "currentTeams" in result:
        teams = result["currentTeams"]
        print(f"Found {len(teams)} FBS teams")
        return teams
    else:
        print("Failed to fetch teams")
        return []

def main():
    """Main execution function."""
    print("=" * 100)
    print("COMPREHENSIVE RUNNING BACK ANALYSIS 2025")
    print("=" * 100)
    
    # Fetch all teams
    teams = fetch_all_teams()
    if not teams:
        print("❌ Failed to fetch teams. Exiting.")
        return
    
    all_rbs = []
    
    # Process each team
    for i, team in enumerate(teams, 1):
        team_id = team["teamId"]
        team_name = f"{team['school']} ({team.get('conference', 'Independent')})"
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name}...")
        
        try:
            team_rbs = fetch_team_rb_stats(team_id, team_name)
            all_rbs.extend(team_rbs)
            
            # Rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error processing {team_name}: {e}")
            continue
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Total RBs found: {len(all_rbs)}")
    
    # Filter for qualified RBs (minimum 10 touches for broader analysis)
    qualified_rbs = [rb for rb in all_rbs if rb.total_touches >= 10]
    print(f"Qualified RBs (10+ touches): {len(qualified_rbs)}")

    # Also show breakdown by touch thresholds
    touch_25_plus = [rb for rb in all_rbs if rb.total_touches >= 25]
    touch_15_plus = [rb for rb in all_rbs if rb.total_touches >= 15]
    touch_20_plus = [rb for rb in all_rbs if rb.total_touches >= 20]

    print(f"  • 25+ touches: {len(touch_25_plus)} RBs")
    print(f"  • 20+ touches: {len(touch_20_plus)} RBs")
    print(f"  • 15+ touches: {len(touch_15_plus)} RBs")
    print(f"  • 10+ touches: {len(qualified_rbs)} RBs (using for analysis)")

    if not qualified_rbs:
        print("❌ No qualified RBs found!")
        return
    
    # Generate timestamp for files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save comprehensive analysis
    comprehensive_data = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "season": 2025,
            "total_rbs": len(all_rbs),
            "qualified_rbs": len(qualified_rbs),
            "minimum_touches": 10,
            "teams_analyzed": len(teams)
        },
        "running_backs": [asdict(rb) for rb in qualified_rbs]
    }
    
    filename = f"player_metrics/rb/comprehensive_rb_analysis_2025_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)
    
    print(f"✅ Comprehensive analysis saved: {filename}")
    
    # Generate individual ranking files
    rankings = {
        "comprehensive_efficiency_score": sorted(qualified_rbs, key=lambda x: x.comprehensive_efficiency_score, reverse=True),
        "dual_threat_efficiency": sorted([rb for rb in qualified_rbs if rb.receptions >= 10], 
                                       key=lambda x: x.dual_threat_efficiency, reverse=True),
        "rushing_efficiency": sorted([rb for rb in qualified_rbs if rb.rushing_attempts >= 50], 
                                   key=lambda x: x.yards_per_carry, reverse=True),
        "receiving_efficiency": sorted([rb for rb in qualified_rbs if rb.receptions >= 15], 
                                     key=lambda x: x.yards_per_reception, reverse=True),
        "total_yards": sorted(qualified_rbs, key=lambda x: x.total_yards, reverse=True)
    }
    
    for ranking_name, ranked_rbs in rankings.items():
        if ranked_rbs:  # Only create file if there are RBs in this category
            ranking_filename = f"player_metrics/rb/rb_{ranking_name}_rankings_2025_{timestamp}.json"
            ranking_data = {
                "metadata": {
                    "ranking_type": ranking_name,
                    "analysis_date": datetime.now().isoformat(),
                    "season": 2025,
                    "total_players": len(ranked_rbs)
                },
                "rankings": [asdict(rb) for rb in ranked_rbs[:50]]  # Top 50
            }
            
            with open(ranking_filename, 'w') as f:
                json.dump(ranking_data, f, indent=2)
            
            print(f"✅ {ranking_name.replace('_', ' ').title()} rankings saved: {ranking_filename}")
    
    # Display top performers
    print("\n" + "=" * 100)
    print("🏆 TOP RUNNING BACK PERFORMERS 2025")
    print("=" * 100)
    
    # Top 25 Comprehensive Efficiency
    print(f"\n🥇 TOP 25 COMPREHENSIVE RB EFFICIENCY:")
    print("-" * 80)
    top_comprehensive = sorted(qualified_rbs, key=lambda x: x.comprehensive_efficiency_score, reverse=True)[:25]
    
    for i, rb in enumerate(top_comprehensive, 1):
        print(f"{i:2d}. {rb.name:<25} ({rb.team:<25}) - {rb.comprehensive_efficiency_score:6.1f} eff")
        print(f"    📊 {rb.total_touches:3d} touches, {rb.total_yards:4d} yards, {rb.total_tds:2d} TDs, {rb.yards_per_touch:4.1f} YPT")
    
    # Top 15 Dual-Threat RBs
    dual_threat_rbs = [rb for rb in qualified_rbs if rb.receptions >= 10]
    if dual_threat_rbs:
        print(f"\n🔥 TOP 15 DUAL-THREAT RUNNING BACKS (10+ receptions):")
        print("-" * 80)
        top_dual_threat = sorted(dual_threat_rbs, key=lambda x: x.dual_threat_efficiency, reverse=True)[:15]
        
        for i, rb in enumerate(top_dual_threat, 1):
            print(f"{i:2d}. {rb.name:<25} ({rb.team:<25}) - {rb.dual_threat_efficiency:6.1f} eff")
            print(f"    🏃 {rb.rushing_yards:4d} rush yds ({rb.yards_per_carry:4.1f} YPC) | 🎯 {rb.receiving_yards:3d} rec yds ({rb.receptions:2d} rec)")
    
    # Top 15 Pure Rushers
    pure_rushers = [rb for rb in qualified_rbs if rb.rushing_attempts >= 50]
    if pure_rushers:
        print(f"\n💨 TOP 15 RUSHING EFFICIENCY (50+ attempts):")
        print("-" * 80)
        top_rushers = sorted(pure_rushers, key=lambda x: x.yards_per_carry, reverse=True)[:15]
        
        for i, rb in enumerate(top_rushers, 1):
            print(f"{i:2d}. {rb.name:<25} ({rb.team:<25}) - {rb.yards_per_carry:5.2f} YPC")
            print(f"    🏃 {rb.rushing_attempts:3d} att, {rb.rushing_yards:4d} yds, {rb.rushing_tds:2d} TDs, {rb.longest_rush:2d} long")
    
    # Top 15 Total Production
    print(f"\n📈 TOP 15 TOTAL SCRIMMAGE YARDS:")
    print("-" * 80)
    top_production = sorted(qualified_rbs, key=lambda x: x.total_yards, reverse=True)[:15]
    
    for i, rb in enumerate(top_production, 1):
        print(f"{i:2d}. {rb.name:<25} ({rb.team:<25}) - {rb.total_yards:4d} total yards")
        print(f"    📊 {rb.rushing_yards:4d} rush + {rb.receiving_yards:3d} rec = {rb.total_yards:4d} total, {rb.total_tds:2d} TDs")
    
    print(f"\n✅ Analysis complete! All files saved to player_metrics/rb/ directory.")

if __name__ == "__main__":
    main()
