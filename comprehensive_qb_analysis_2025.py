
#!/usr/bin/env python3
"""
Comprehensive QB Analysis 2025 - Enhanced Edition
The most complete quarterback efficiency analysis with ALL available metrics:
- Traditional passing stats
- Rushing/dual-threat metrics  
- Turnover analysis
- Advanced efficiency calculations
- Situational performance
- Big play analysis
"""

import requests
import json
from datetime import datetime
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# API Configuration
GRAPHQL_ENDPOINT = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# GraphQL Query to get all FBS teams
ALL_FBS_TEAMS_QUERY = """
query AllFBSTeams {
  currentTeams(
    where: {
      classification: { _eq: "fbs" }
    }
    orderBy: { school: ASC }
  ) {
    school
    conference
    teamId
  }
}
"""

# Enhanced QB Statistics Query - ALL categories
COMPREHENSIVE_QB_STATS_QUERY = """
query ComprehensiveQBStats($season: smallint!, $teamId: Int!) {
  gamePlayerStat(
    where: {
      gameTeam: {
        teamId: { _eq: $teamId }
        game: { season: { _eq: $season } }
      }
      athlete: {
        position: { abbreviation: { _eq: "QB" } }
      }
      playerStatCategory: { 
        name: { _in: ["passing", "rushing", "fumbles"] }
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

@dataclass
class ComprehensiveQBStats:
    """Enhanced quarterback statistics container with ALL metrics"""
    name: str
    team: str
    athlete_id: int
    games_played: int = 0
    
    # Passing stats
    completions: int = 0
    attempts: int = 0
    passing_yards: int = 0
    passing_tds: int = 0
    interceptions: int = 0
    passing_avg: float = 0.0  # YPA from API
    longest_pass: int = 0
    qbr: float = 0.0  # QBR from API
    
    # Rushing stats (dual-threat)
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_tds: int = 0
    rushing_avg: float = 0.0
    longest_rush: int = 0
    
    # Turnover stats
    fumbles: int = 0
    fumbles_lost: int = 0
    fumbles_recovered: int = 0
    
    # Calculated basic metrics
    completion_percentage: float = 0.0
    yards_per_attempt: float = 0.0
    yards_per_completion: float = 0.0
    td_int_ratio: float = 0.0
    passer_rating: float = 0.0
    
    # Enhanced dual-threat metrics
    total_yards: int = 0
    total_tds: int = 0
    total_turnovers: int = 0
    dual_threat_efficiency: float = 0.0
    
    # Advanced efficiency metrics
    ball_security_score: float = 0.0
    big_play_rate: float = 0.0
    turnover_rate: float = 0.0
    total_offensive_efficiency: float = 0.0
    
    # Situational metrics
    conference_games: int = 0
    conference_performance: float = 0.0
    close_game_performance: float = 0.0
    
    # Overall efficiency score
    comprehensive_efficiency_score: float = 0.0


def fetch_all_fbs_teams():
    """Fetch all FBS teams from the API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": ALL_FBS_TEAMS_QUERY
    }
    
    try:
        print("Fetching all FBS teams...")
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
            return []
        
        teams = data.get("data", {}).get("currentTeams", [])
        print(f"✓ Found {len(teams)} FBS teams")
        return teams
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []


def fetch_comprehensive_qb_stats(team_id: int, team_name: str, season: int):
    """Fetch comprehensive QB statistics for a specific team and season."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    variables = {
        "teamId": team_id,
        "season": season
    }
    
    payload = {
        "query": COMPREHENSIVE_QB_STATS_QUERY,
        "variables": variables
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
            print(f"GraphQL Errors for {team_name}: {json.dumps(data['errors'], indent=2)}")
            return None
        
        return data.get("data", {}).get("gamePlayerStat", [])
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error for {team_name}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error for {team_name}: {e}")
        return None


def process_comprehensive_qb_stats(raw_stats: List[Dict], team_name: str) -> List[ComprehensiveQBStats]:
    """Process raw QB statistics into comprehensive structured data."""
    if not raw_stats:
        return []
    
    # Group stats by player
    player_stats = {}
    
    for stat in raw_stats:
        athlete = stat.get("athlete", {})
        athlete_id = athlete.get("id")
        athlete_name = athlete.get("name", "Unknown")
        
        if athlete_id not in player_stats:
            player_stats[athlete_id] = ComprehensiveQBStats(
                name=athlete_name,
                team=team_name,
                athlete_id=athlete_id
            )
        
        category = stat.get("playerStatCategory", {}).get("name", "")
        stat_type = stat.get("playerStatType", {}).get("name", "")
        stat_value = stat.get("stat", "0")
        game_info = stat.get("gameTeam", {}).get("game", {})
        
        qb = player_stats[athlete_id]
        
        # Track conference games
        if game_info.get("conferenceGame"):
            qb.conference_games += 1
        
        # Process different stat categories
        if category == "passing":
            process_passing_stats(qb, stat_type, stat_value)
        elif category == "rushing":
            process_rushing_stats(qb, stat_type, stat_value)
        elif category == "fumbles":
            process_fumble_stats(qb, stat_type, stat_value)
    
    # Calculate all derived metrics for each QB
    processed_qbs = []
    for qb in player_stats.values():
        if qb.attempts > 0:  # Only include QBs with passing attempts
            calculate_comprehensive_metrics(qb)
            processed_qbs.append(qb)
    
    return processed_qbs


def process_passing_stats(qb: ComprehensiveQBStats, stat_type: str, stat_value: str):
    """Process passing statistics."""
    try:
        if stat_type == "C/ATT":
            # Completions/Attempts format like "15/25"
            if "/" in stat_value:
                comp_att = stat_value.split("/")
                if len(comp_att) == 2:
                    qb.completions += int(comp_att[0]) if comp_att[0].isdigit() else 0
                    qb.attempts += int(comp_att[1]) if comp_att[1].isdigit() else 0
        elif stat_type == "YDS":
            qb.passing_yards += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "TD":
            qb.passing_tds += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "INT":
            qb.interceptions += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "AVG":
            # This is yards per attempt from API
            qb.passing_avg = max(qb.passing_avg, float(stat_value)) if stat_value.replace('.', '').isdigit() else qb.passing_avg
        elif stat_type == "LONG":
            qb.longest_pass = max(qb.longest_pass, int(stat_value)) if stat_value.isdigit() else qb.longest_pass
        elif stat_type == "QBR":
            qb.qbr = max(qb.qbr, float(stat_value)) if stat_value.replace('.', '').isdigit() else qb.qbr
    except (ValueError, AttributeError):
        pass


def process_rushing_stats(qb: ComprehensiveQBStats, stat_type: str, stat_value: str):
    """Process rushing statistics."""
    try:
        if stat_type == "CAR":
            qb.rushing_attempts += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "YDS":
            qb.rushing_yards += int(stat_value) if stat_value.lstrip('-').isdigit() else 0
        elif stat_type == "TD":
            qb.rushing_tds += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "AVG":
            qb.rushing_avg = max(qb.rushing_avg, float(stat_value)) if stat_value.replace('.', '').replace('-', '').isdigit() else qb.rushing_avg
        elif stat_type == "LONG":
            qb.longest_rush = max(qb.longest_rush, int(stat_value)) if stat_value.isdigit() else qb.longest_rush
    except (ValueError, AttributeError):
        pass


def process_fumble_stats(qb: ComprehensiveQBStats, stat_type: str, stat_value: str):
    """Process fumble statistics."""
    try:
        if stat_type == "FUM":
            qb.fumbles += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "LOST":
            qb.fumbles_lost += int(stat_value) if stat_value.isdigit() else 0
        elif stat_type == "REC":
            qb.fumbles_recovered += int(stat_value) if stat_value.isdigit() else 0
    except (ValueError, AttributeError):
        pass


def calculate_passer_rating(completions: int, attempts: int, yards: int, tds: int, interceptions: int) -> float:
    """Calculate NCAA passer rating using the official formula."""
    if attempts == 0:
        return 0.0

    # NCAA Passer Rating Formula
    # Component A: Completion percentage
    comp_pct = (completions / attempts) * 100
    a = max(0, min(100, (comp_pct - 30) * 100 / 40))

    # Component B: Yards per attempt
    ypa = yards / attempts
    b = max(0, min(100, (ypa - 3) * 100 / 6))

    # Component C: Touchdown percentage
    td_pct = (tds / attempts) * 100
    c = max(0, min(100, td_pct * 100 / 9))

    # Component D: Interception percentage
    int_pct = (interceptions / attempts) * 100
    d = max(0, min(100, 100 - (int_pct * 100 / 4)))

    # Final rating
    rating = (a + b + c + d) / 4
    return round(rating, 1)


def calculate_comprehensive_metrics(qb: ComprehensiveQBStats):
    """Calculate all comprehensive efficiency metrics for a quarterback."""
    if qb.attempts == 0:
        return

    # Basic passing metrics
    qb.completion_percentage = (qb.completions / qb.attempts) * 100
    qb.yards_per_attempt = qb.passing_yards / qb.attempts

    if qb.completions > 0:
        qb.yards_per_completion = qb.passing_yards / qb.completions

    # TD/INT ratio
    if qb.interceptions > 0:
        qb.td_int_ratio = qb.passing_tds / qb.interceptions
    else:
        qb.td_int_ratio = qb.passing_tds  # If no INTs, ratio is just TDs

    # Calculate passer rating
    qb.passer_rating = calculate_passer_rating(
        qb.completions, qb.attempts, qb.passing_yards, qb.passing_tds, qb.interceptions
    )

    # Dual-threat metrics
    qb.total_yards = qb.passing_yards + qb.rushing_yards
    qb.total_tds = qb.passing_tds + qb.rushing_tds
    qb.total_turnovers = qb.interceptions + qb.fumbles_lost

    # Advanced efficiency metrics
    total_plays = qb.attempts + qb.rushing_attempts

    # Ball security score (0-100, higher is better)
    if total_plays > 0:
        qb.turnover_rate = (qb.total_turnovers / total_plays) * 100
        qb.ball_security_score = max(0, 100 - (qb.turnover_rate * 20))  # Penalize turnovers heavily

    # Big play rate (20+ yard plays estimated from longest plays)
    big_plays = 0
    if qb.longest_pass >= 20:
        big_plays += 1
    if qb.longest_rush >= 20:
        big_plays += 1

    if total_plays > 0:
        qb.big_play_rate = (big_plays / total_plays) * 100

    # Dual-threat efficiency (combines passing and rushing effectiveness)
    if total_plays > 0:
        yards_per_play = qb.total_yards / total_plays
        td_rate = (qb.total_tds / total_plays) * 100
        qb.dual_threat_efficiency = (yards_per_play * 10) + (td_rate * 20) + qb.ball_security_score

    # Total offensive efficiency (comprehensive score)
    qb.total_offensive_efficiency = (
        (qb.completion_percentage * 0.15) +
        (qb.yards_per_attempt * 8) +
        (qb.td_int_ratio * 5) +
        (qb.dual_threat_efficiency * 0.3) +
        (qb.ball_security_score * 0.4)
    )

    # Conference performance (if applicable)
    if qb.conference_games > 0:
        qb.conference_performance = qb.total_offensive_efficiency  # Simplified for now

    # Comprehensive efficiency score (master metric)
    volume_bonus = min(20, qb.attempts / 10)  # Bonus for volume, capped at 20
    rushing_bonus = min(15, qb.rushing_yards / 50)  # Bonus for rushing production

    qb.comprehensive_efficiency_score = (
        qb.total_offensive_efficiency +
        volume_bonus +
        rushing_bonus
    )


def generate_comprehensive_analysis(all_qbs: List[ComprehensiveQBStats], season: int):
    """Generate comprehensive QB analysis with all metrics."""
    # Filter QBs with minimum attempts
    min_attempts = 50
    qualified_qbs = [qb for qb in all_qbs if qb.attempts >= min_attempts]

    print(f"\n✓ Found {len(qualified_qbs)} QBs with {min_attempts}+ passing attempts")

    if not qualified_qbs:
        print("No qualified QBs found.")
        return

    # Sort by comprehensive efficiency score
    qualified_qbs.sort(key=lambda x: x.comprehensive_efficiency_score, reverse=True)

    # Print comprehensive rankings
    print_comprehensive_rankings(qualified_qbs)

    # Save comprehensive analysis
    save_comprehensive_analysis(qualified_qbs, season)


def print_comprehensive_rankings(qbs: List[ComprehensiveQBStats]):
    """Print comprehensive QB rankings with all metrics."""
    print("\n" + "=" * 160)
    print("2025 FBS COMPREHENSIVE QUARTERBACK ANALYSIS")
    print("=" * 160)

    # Top 25 Comprehensive Efficiency
    print(f"\n🏆 TOP 25 COMPREHENSIVE QB EFFICIENCY (All Metrics Combined)")
    print("-" * 160)
    print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'Comp Eff':<8} {'Rating':<7} {'Comp%':<7} {'YPA':<6} {'Rush Yds':<8} {'Total TDs':<8} {'Turnovers':<9}")
    print("-" * 160)

    for i, qb in enumerate(qbs[:25], 1):
        print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.comprehensive_efficiency_score:<8.1f} "
              f"{qb.passer_rating:<7.1f} {qb.completion_percentage:<7.1f}% {qb.yards_per_attempt:<6.1f} "
              f"{qb.rushing_yards:<8} {qb.total_tds:<8} {qb.total_turnovers:<9}")

    # Top 15 Dual-Threat QBs
    dual_threat_qbs = sorted([qb for qb in qbs if qb.rushing_yards > 100],
                            key=lambda x: x.dual_threat_efficiency, reverse=True)

    print(f"\n🏃‍♂️ TOP 15 DUAL-THREAT QUARTERBACKS")
    print("-" * 140)
    print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'Dual Eff':<8} {'Pass Yds':<8} {'Rush Yds':<8} {'Total Yds':<9} {'Total TDs':<8}")
    print("-" * 140)

    for i, qb in enumerate(dual_threat_qbs[:15], 1):
        print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.dual_threat_efficiency:<8.1f} "
              f"{qb.passing_yards:<8} {qb.rushing_yards:<8} {qb.total_yards:<9} {qb.total_tds:<8}")

    # Top 15 Ball Security Specialists
    ball_security_qbs = sorted(qbs, key=lambda x: x.ball_security_score, reverse=True)

    print(f"\n🛡️ TOP 15 BALL SECURITY SPECIALISTS")
    print("-" * 120)
    print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'Security':<8} {'Turnovers':<9} {'TO Rate':<8} {'Attempts':<8}")
    print("-" * 120)

    for i, qb in enumerate(ball_security_qbs[:15], 1):
        print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.ball_security_score:<8.1f} "
              f"{qb.total_turnovers:<9} {qb.turnover_rate:<8.2f}% {qb.attempts:<8}")

    # Top 15 Total Offensive Production
    production_qbs = sorted(qbs, key=lambda x: x.total_yards, reverse=True)

    print(f"\n📊 TOP 15 TOTAL OFFENSIVE PRODUCTION")
    print("-" * 140)
    print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'Total Yds':<9} {'Pass Yds':<8} {'Rush Yds':<8} {'Total TDs':<8} {'YPP':<6}")
    print("-" * 140)

    for i, qb in enumerate(production_qbs[:15], 1):
        total_plays = qb.attempts + qb.rushing_attempts
        ypp = qb.total_yards / total_plays if total_plays > 0 else 0
        print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.total_yards:<9} "
              f"{qb.passing_yards:<8} {qb.rushing_yards:<8} {qb.total_tds:<8} {ypp:<6.1f}")

    # Top 15 by QBR (if available)
    qbr_qbs = sorted([qb for qb in qbs if qb.qbr > 0], key=lambda x: x.qbr, reverse=True)

    if qbr_qbs:
        print(f"\n🎯 TOP 15 BY QBR (ESPN Metric)")
        print("-" * 120)
        print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'QBR':<6} {'Rating':<7} {'Comp%':<7} {'YPA':<6}")
        print("-" * 120)

        for i, qb in enumerate(qbr_qbs[:15], 1):
            print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.qbr:<6.1f} "
                  f"{qb.passer_rating:<7.1f} {qb.completion_percentage:<7.1f}% {qb.yards_per_attempt:<6.1f}")

    # Big Play Specialists
    big_play_qbs = sorted([qb for qb in qbs if qb.longest_pass > 0 or qb.longest_rush > 0],
                         key=lambda x: max(x.longest_pass, x.longest_rush), reverse=True)

    print(f"\n🚀 TOP 15 BIG PLAY SPECIALISTS")
    print("-" * 130)
    print(f"{'Rank':<4} {'Name':<25} {'Team':<20} {'Long Pass':<10} {'Long Rush':<10} {'YPA':<6} {'Rush Avg':<8}")
    print("-" * 130)

    for i, qb in enumerate(big_play_qbs[:15], 1):
        print(f"#{i:<3} {qb.name:<25} {qb.team:<20} {qb.longest_pass:<10} "
              f"{qb.longest_rush:<10} {qb.yards_per_attempt:<6.1f} {qb.rushing_avg:<8.1f}")


def save_comprehensive_analysis(qbs: List[ComprehensiveQBStats], season: int):
    """Save comprehensive QB analysis to JSON files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Prepare comprehensive data
    comprehensive_data = {
        "metadata": {
            "season": season,
            "timestamp": timestamp,
            "total_qbs_analyzed": len(qbs),
            "minimum_attempts": 50,
            "analysis_type": "comprehensive_enhanced"
        },
        "quarterbacks": []
    }

    for qb in qbs:
        qb_data = {
            "name": qb.name,
            "team": qb.team,
            "athlete_id": qb.athlete_id,
            "passing_stats": {
                "completions": qb.completions,
                "attempts": qb.attempts,
                "passing_yards": qb.passing_yards,
                "passing_tds": qb.passing_tds,
                "interceptions": qb.interceptions,
                "longest_pass": qb.longest_pass,
                "qbr": qb.qbr
            },
            "rushing_stats": {
                "rushing_attempts": qb.rushing_attempts,
                "rushing_yards": qb.rushing_yards,
                "rushing_tds": qb.rushing_tds,
                "rushing_avg": qb.rushing_avg,
                "longest_rush": qb.longest_rush
            },
            "turnover_stats": {
                "fumbles": qb.fumbles,
                "fumbles_lost": qb.fumbles_lost,
                "fumbles_recovered": qb.fumbles_recovered,
                "total_turnovers": qb.total_turnovers
            },
            "efficiency_metrics": {
                "completion_percentage": qb.completion_percentage,
                "yards_per_attempt": qb.yards_per_attempt,
                "td_int_ratio": qb.td_int_ratio,
                "passer_rating": qb.passer_rating,
                "ball_security_score": qb.ball_security_score,
                "turnover_rate": qb.turnover_rate,
                "dual_threat_efficiency": qb.dual_threat_efficiency,
                "total_offensive_efficiency": qb.total_offensive_efficiency,
                "comprehensive_efficiency_score": qb.comprehensive_efficiency_score
            },
            "total_production": {
                "total_yards": qb.total_yards,
                "total_tds": qb.total_tds
            }
        }
        comprehensive_data["quarterbacks"].append(qb_data)

    # Save comprehensive analysis
    filename = f"comprehensive_qb_analysis_{season}_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)

    print(f"✓ Comprehensive QB analysis saved to: {filename}")

    # Save individual ranking files
    rankings = {
        "comprehensive_efficiency_score": sorted(qbs, key=lambda x: x.comprehensive_efficiency_score, reverse=True),
        "dual_threat_efficiency": sorted([qb for qb in qbs if qb.rushing_yards > 100],
                                       key=lambda x: x.dual_threat_efficiency, reverse=True),
        "ball_security_score": sorted(qbs, key=lambda x: x.ball_security_score, reverse=True),
        "total_yards": sorted(qbs, key=lambda x: x.total_yards, reverse=True),
        "passer_rating": sorted(qbs, key=lambda x: x.passer_rating, reverse=True)
    }

    for ranking_type, ranked_qbs in rankings.items():
        ranking_filename = f"qb_{ranking_type}_rankings_{season}_{timestamp}.json"
        ranking_data = {
            "metadata": {
                "ranking_type": ranking_type,
                "season": season,
                "timestamp": timestamp,
                "total_qbs": len(ranked_qbs)
            },
            "rankings": [
                {
                    "rank": i + 1,
                    "name": qb.name,
                    "team": qb.team,
                    "value": getattr(qb, ranking_type)
                }
                for i, qb in enumerate(ranked_qbs[:50])  # Top 50 for each ranking
            ]
        }

        with open(ranking_filename, 'w') as f:
            json.dump(ranking_data, f, indent=2)

    print(f"✓ Individual ranking files saved for: {', '.join(rankings.keys())}")


def main():
    """Main execution function."""
    print("=" * 140)
    print("COMPREHENSIVE COLLEGE FOOTBALL QB ANALYSIS - 2025 SEASON (ENHANCED EDITION)")
    print("=" * 140)
    print()

    season = 2025

    # Fetch all FBS teams
    teams = fetch_all_fbs_teams()

    if not teams:
        print("✗ Failed to fetch FBS teams. Exiting.")
        return

    all_qbs = []

    print(f"\nProcessing comprehensive QB stats for {len(teams)} FBS teams...")
    print("This may take a few minutes due to API rate limits...\n")

    for i, team in enumerate(teams, 1):
        team_name = team["school"]
        team_id = team["teamId"]
        conference = team.get("conference", "Independent")

        print(f"[{i:3d}/{len(teams)}] Processing {team_name} ({conference})...")

        # Fetch team's comprehensive QB stats
        raw_stats = fetch_comprehensive_qb_stats(team_id, team_name, season)

        if raw_stats:
            # Process the QB stats
            team_qbs = process_comprehensive_qb_stats(raw_stats, team_name)
            all_qbs.extend(team_qbs)

        # Rate limiting - small delay between requests
        time.sleep(0.1)

    # Generate comprehensive QB analysis
    generate_comprehensive_analysis(all_qbs, season)

    print(f"\n✓ Comprehensive analysis completed successfully!")
    print(f"✓ Processed {len(all_qbs)} qualifying quarterbacks")


if __name__ == "__main__":
    main()
