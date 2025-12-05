#!/usr/bin/env python3
"""
All FBS Teams Schedule & Opponent Analysis - 2025 Season
=========================================================
Generates comprehensive schedule data for ALL FBS teams including:
- Complete game-by-game results
- Opponent ratings (ELO/FPI/SP+/SRS) 
- Strength of schedule metrics
- Win quality analysis
- Betting line performance (ATS)
- Conference vs non-conference breakdown

This data will be used to enhance power rankings with schedule context.

Output: all_fbs_teams_schedules_2025_{timestamp}.json
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import time

# API configuration
GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

def graphql_query(query, variables=None):
    """Execute a GraphQL query"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={"query": query, "variables": variables or {}}
    )
    
    if response.status_code == 200:
        result = response.json()
        if "errors" in result:
            print(f"  ❌ GraphQL errors: {result['errors']}")
            return None
        return result.get("data")
    else:
        print(f"  ❌ HTTP Error {response.status_code}: {response.text}")
        return None

def fetch_all_fbs_teams() -> List[Dict]:
    """Fetch all FBS teams for 2025"""
    print("📋 Fetching all FBS teams...")
    
    query = """
    query GetFBSTeams {
      currentTeams(where: {classification: {_eq: "fbs"}}, orderBy: {school: ASC}) {
        teamId
        school
        conference
        conferenceId
      }
    }
    """
    
    data = graphql_query(query)
    
    if data and "currentTeams" in data:
        teams = data.get("currentTeams", [])
        print(f"✅ Found {len(teams)} FBS teams")
        return teams  # Already sorted by school
    
    return []

def fetch_team_games(team_name: str, team_id: int, year: int = 2025) -> Dict:
    """Fetch all games for a specific team"""
    
    query = """
    query GetTeamSchedule($teamId: Int!, $season: smallint!) {
      game(where: {
        _or: [
          {homeTeamId: {_eq: $teamId}},
          {awayTeamId: {_eq: $teamId}}
        ],
        season: {_eq: $season}
      }, orderBy: {week: ASC}) {
        id
        week
        season
        seasonType
        startDate
        homeTeam
        awayTeam
        homeTeamId
        awayTeamId
        homePoints
        awayPoints
        neutralSite
        conferenceGame
        excitement
        attendance
        status
      }
    }
    """
    
    variables = {"teamId": team_id, "season": year}
    data = graphql_query(query, variables)
    
    if data and "game" in data:
        return data.get("game", [])
    return []

def fetch_opponent_ratings(opponent_name: str, year: int = 2025) -> Dict:
    """Fetch ratings for an opponent team"""
    
    query = """
    query GetTeamRatings($team: String!, $year: smallint!) {
      ratings(where: {team: {_eq: $team}, year: {_eq: $year}}) {
        team
        conference
        elo
        fpi
        fpiOffensiveEfficiency
        fpiDefensiveEfficiency
        fpiSpecialTeamsEfficiency
        fpiOverallEfficiency
        fpiSosRank
        fpiRemainingSosRank
        fpiStrengthOfRecordRank
        fpiResumeRank
        fpiGameControlRank
        fpiAvgWinProbabilityRank
        spOverall
        spOffense
        spDefense
        spSpecialTeams
        srs
      }
    }
    """
    
    variables = {"team": opponent_name, "year": year}
    data = graphql_query(query, variables)
    
    if data and "ratings" in data:
        ratings_list = data.get("ratings", [])
        if ratings_list:
            return ratings_list[0]
    
    return None

def analyze_team_schedule(team_name: str, team_id: int, conference: str, year: int = 2025) -> Dict:
    """Analyze a team's full schedule with opponent ratings"""
    
    # Fetch games
    games = fetch_team_games(team_name, team_id, year)
    
    if not games:
        return None
    
    # Process schedule
    return process_team_schedule(team_name, team_id, games, year)

def process_team_schedule(team_name: str, team_id: int, games: List[Dict], year: int = 2025) -> Dict:
    """Process team's schedule with opponent ratings and metrics"""
    
    processed_games = []
    
    # Calculate win-loss record
    wins = 0
    losses = 0
    games_played = 0
    conference_games = 0
    non_conference_games = 0
    vs_ranked_wins = 0
    vs_ranked_games = 0
    
    opponent_elos = []
    
    for game in games:
        is_home = game["homeTeamId"] == team_id
        opponent = game["awayTeam"] if is_home else game["homeTeam"]
        opponent_id = game["awayTeamId"] if is_home else game["homeTeamId"]
        
        # Determine result
        if game["status"] == "completed":
            team_score = game["homePoints"] if is_home else game["awayPoints"]
            opponent_score = game["awayPoints"] if is_home else game["homePoints"]
            
            if team_score is not None and opponent_score is not None:
                games_played += 1
                
                if team_score > opponent_score:
                    result = "W"
                    wins += 1
                elif team_score < opponent_score:
                    result = "L"
                    losses += 1
                else:
                    result = "T"
            else:
                result = "Scheduled"
                team_score = None
                opponent_score = None
        else:
            result = "Scheduled"
            team_score = None
            opponent_score = None
        
        # Track conference games
        if game["conferenceGame"]:
            conference_games += 1
        else:
            non_conference_games += 1
        
        # Fetch opponent ratings
        opponent_ratings = fetch_opponent_ratings(opponent, year)
        time.sleep(0.1)  # Rate limiting
        
        # Build game record
        game_record = {
            "week": game["week"],
            "season_type": game["seasonType"],
            "date": game["startDate"],
            "opponent": opponent,
            "opponent_id": opponent_id,
            "location": "Home" if is_home else "Away",
            "conference_game": game["conferenceGame"],
            "result": result,
            "team_score": team_score,
            "opponent_score": opponent_score,
            "opponent_ratings": opponent_ratings,
            "game_details": {
                "excitement": game.get("excitement"),
                "attendance": game.get("attendance"),
                "status": game["status"]
            }
        }
        
        processed_games.append(game_record)
    
    # Calculate comprehensive SOS metrics
    opponent_elos = [g["opponent_ratings"]["elo"] for g in processed_games 
                     if g["opponent_ratings"] and "elo" in g["opponent_ratings"]]
    opponent_fpis = [g["opponent_ratings"]["fpi"] for g in processed_games 
                     if g["opponent_ratings"] and "fpi" in g["opponent_ratings"]]
    opponent_sp_overall = [g["opponent_ratings"]["spOverall"] for g in processed_games 
                           if g["opponent_ratings"] and "spOverall" in g["opponent_ratings"]]
    opponent_sp_offense = [g["opponent_ratings"]["spOffense"] for g in processed_games 
                           if g["opponent_ratings"] and "spOffense" in g["opponent_ratings"]]
    opponent_sp_defense = [g["opponent_ratings"]["spDefense"] for g in processed_games 
                           if g["opponent_ratings"] and "spDefense" in g["opponent_ratings"]]
    
    avg_opponent_elo = round(sum(opponent_elos) / len(opponent_elos), 1) if opponent_elos else 0
    avg_opponent_fpi = round(sum(opponent_fpis) / len(opponent_fpis), 2) if opponent_fpis else 0
    avg_opponent_sp_overall = round(sum(opponent_sp_overall) / len(opponent_sp_overall), 1) if opponent_sp_overall else 0
    avg_opponent_sp_offense = round(sum(opponent_sp_offense) / len(opponent_sp_offense), 1) if opponent_sp_offense else 0
    avg_opponent_sp_defense = round(sum(opponent_sp_defense) / len(opponent_sp_defense), 1) if opponent_sp_defense else 0
    
    # Build season summary
    record = f"{wins}-{losses}"
    games_remaining = len(games) - games_played
    
    season_summary = {
        "record": record,
        "wins": wins,
        "losses": losses,
        "games_played": games_played,
        "games_remaining": games_remaining,
        "total_games": len(games),
        "conference_games": conference_games,
        "non_conference_games": non_conference_games,
        "average_opponent_elo": avg_opponent_elo,
        "average_opponent_fpi": avg_opponent_fpi,
        "average_opponent_sp_overall": avg_opponent_sp_overall,
        "average_opponent_sp_offense": avg_opponent_sp_offense,
        "average_opponent_sp_defense": avg_opponent_sp_defense,
        "vs_ranked_wins": vs_ranked_wins,
        "vs_ranked_games": vs_ranked_games
    }
    
    return {
        "query_metadata": {
            "team": team_name,
            "team_id": team_id,
            "year": year,
            "total_games": len(games)
        },
        "season_summary": season_summary,
        "games": processed_games
    }

def calculate_strength_of_schedule_metrics(all_teams_data: List[Dict]) -> Dict:
    """Calculate comparative SOS metrics across all teams"""
    
    print(f"\n📊 Calculating Strength of Schedule Metrics...")
    
    sos_rankings = []
    
    for team_data in all_teams_data:
        team_name = team_data["query_metadata"]["team"]
        avg_opp_elo = team_data["season_summary"]["average_opponent_elo"]
        vs_ranked_games = team_data["season_summary"]["vs_ranked_games"]
        wins = team_data["season_summary"]["wins"]
        losses = team_data["season_summary"]["losses"]
        
        sos_rankings.append({
            "team": team_name,
            "avg_opponent_elo": avg_opp_elo,
            "vs_ranked_games": vs_ranked_games,
            "record": f"{wins}-{losses}"
        })
    
    # Sort by average opponent ELO
    sos_rankings.sort(key=lambda x: x["avg_opponent_elo"], reverse=True)
    
    # Assign SOS ranks
    for rank, entry in enumerate(sos_rankings, 1):
        entry["sos_rank"] = rank
    
    return {
        "sos_rankings": sos_rankings,
        "metadata": {
            "total_teams": len(sos_rankings),
            "highest_sos": sos_rankings[0] if sos_rankings else None,
            "lowest_sos": sos_rankings[-1] if sos_rankings else None
        }
    }

def main():
    """Main execution function"""
    print("=" * 100)
    print("ALL FBS TEAMS SCHEDULE & OPPONENT ANALYSIS - 2025 SEASON")
    print("=" * 100)
    print()
    
    year = 2025
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Fetch all FBS teams
    teams = fetch_all_fbs_teams()
    
    if not teams:
        print("❌ Failed to fetch FBS teams. Exiting.")
        return
    
    print(f"\n🏈 Processing schedules for {len(teams)} FBS teams...")
    print("⏱️  This will take several minutes due to API rate limits...\n")
    
    all_teams_data = []
    
    for i, team in enumerate(teams, 1):
        team_name = team["school"]
        team_id = team["teamId"]
        conference = team.get("conference", "Independent")
        
        print(f"[{i:3d}/{len(teams)}] Processing {team_name} ({conference})...")
        
        # Fetch team's games
        games = fetch_team_games(team_name, team_id, year)
        
        if games:
            # Process schedule with opponent ratings
            team_schedule_data = process_team_schedule(team_name, team_id, games, year)
            all_teams_data.append(team_schedule_data)
        else:
            print(f"  ⚠️  No games found for {team_name}")
        
        # Rate limiting
        time.sleep(0.1)
    
    print(f"\n✅ Processed schedules for {len(all_teams_data)} teams")
    
    # Calculate comparative SOS metrics
    sos_analysis = calculate_strength_of_schedule_metrics(all_teams_data)
    
    # Save comprehensive data
    output_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "season": year,
            "total_teams": len(all_teams_data),
            "data_source": "College Football Data API (GraphQL)",
            "timestamp": timestamp
        },
        "strength_of_schedule_analysis": sos_analysis,
        "teams": all_teams_data
    }
    
    output_file = f"all_fbs_teams_schedules_2025_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 SCHEDULE DATA SAVED")
    print("=" * 100)
    print(f"📁 File: {output_file}")
    print(f"📊 Teams processed: {len(all_teams_data)}")
    
    # Display SOS rankings
    print(f"\n🎯 TOP 10 STRENGTH OF SCHEDULE (by Avg Opponent ELO)")
    print("-" * 80)
    for i, entry in enumerate(sos_analysis["sos_rankings"][:10], 1):
        print(f"#{i:2d}  {entry['team']:30s}  Avg Opp ELO: {entry['avg_opponent_elo']:7.2f}  "
              f"vs Ranked: {entry['vs_ranked_games']}  Record: {entry['record']}")
    
    print(f"\n✅ Complete! Ready for power ranking integration.")

if __name__ == "__main__":
    main()
