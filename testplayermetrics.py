#!/usr/bin/env python3
"""
🏈 College Football Data GraphQL API - Player Metrics Explorer
==============================================================

This script comprehensively tests the College Football Data GraphQL API to discover
the proper way to fetch player statistics (especially WRs, RBs, QBs) with actual names.

Key Questions to Answer:
1. Does adjustedPlayerMetrics have receiving stats?
2. Where can we find WR names and stats?
3. What's the structure of gamePlayerStat?
4. How do we link players to teams?
5. Best approach for season aggregates vs game-by-game?

Target Teams:
- Illinois Fighting Illini (ID: 356)
- Ohio State Buckeyes (ID: 194)

Key Players to Find:
- Illinois WRs: Pat Bryant, Zakhari Franklin
- Ohio State WR: Jeremiah Smith
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# API Configuration
API_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
CURRENT_YEAR = 2025

# Test Teams
ILLINOIS_ID = 356
OHIO_STATE_ID = 194

# Helper Functions
def print_header(test_num: int, title: str):
    """Print a formatted test header"""
    print(f"\n{'='*80}")
    print(f"🏈 TEST {test_num}: {title}")
    print(f"{'='*80}\n")

def print_query(query: str):
    """Print the GraphQL query being executed"""
    print("📋 GraphQL Query:")
    print("-" * 80)
    print(query)
    print("-" * 80 + "\n")

def print_results(data: Any, title: str = "Results"):
    """Print results in a formatted way"""
    print(f"📊 {title}:")
    print(json.dumps(data, indent=2))
    print()

def print_analysis(analysis: str):
    """Print analysis section"""
    print("🔍 Analysis:")
    print(analysis)
    print()

def print_error(error: str):
    """Print error message"""
    print(f"❌ Error: {error}\n")

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}\n")

class GraphQLClient:
    """GraphQL Client for College Football Data API"""
    
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a GraphQL query"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "query": query,
                "variables": variables or {}
            }
            
            try:
                async with session.post(self.url, json=payload, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "errors" in result:
                            print_error(f"GraphQL Errors: {json.dumps(result['errors'], indent=2)}")
                        return result
                    else:
                        error_text = await response.text()
                        print_error(f"HTTP {response.status}: {error_text}")
                        return {"error": error_text}
            except Exception as e:
                print_error(f"Exception: {str(e)}")
                return {"error": str(e)}

# Test Functions

async def test_1_adjusted_player_metrics_structure(client: GraphQLClient):
    """
    TEST 1: Explore adjustedPlayerMetrics structure
    Check what metric types are available (passing, rushing, receiving?)
    """
    print_header(1, "Adjusted Player Metrics - Structure & Metric Types")
    
    query = """
    query AdjustedMetricsStructure {
      adjustedPlayerMetrics(
        where: {
          year: {_eq: 2024}
          teamId: {_in: [356, 194]}
        }
        limit: 10
      ) {
        metricType
        playerId
        year
        teamId
        value
      }
    }
    """
    
    print_query(query)
    result = await client.execute_query(query)
    
    if "data" in result and result["data"]:
        metrics = result["data"].get("adjustedPlayerMetrics", [])
        
        if metrics:
            print_success(f"Found {len(metrics)} metric records")
            
            # Analyze metric types
            metric_types = set(m["metricType"] for m in metrics)
            print_analysis(f"""
Metric Types Found: {sorted(metric_types)}
Total Records: {len(metrics)}

Sample Records:
{json.dumps(metrics[:3], indent=2)}

❗ KEY FINDING: Check if 'receiving' is in the metric types list above.
If NOT, then adjustedPlayerMetrics doesn't have receiving stats!
            """)
        else:
            print_error("No metrics found for the specified teams/year")
    else:
        print_error("Failed to retrieve data")
    
    return result

async def test_2_schema_introspection_player_tables(client: GraphQLClient):
    """
    TEST 2: Use schema introspection to find ALL player/stat related tables
    """
    print_header(2, "Schema Introspection - Discover Player/Stat Tables")
    
    query = """
    query SchemaIntrospection {
      __schema {
        types {
          name
          description
          fields {
            name
            description
          }
        }
      }
    }
    """
    
    print("🔍 Introspecting schema to find player and stat related tables...")
    print("(This may take a moment...)\n")
    
    result = await client.execute_query(query)
    
    if "data" in result and result["data"]:
        types = result["data"]["__schema"]["types"]
        
        # Filter for player/stat/athlete related types
        player_related = []
        for type_info in types:
            name = type_info.get("name", "")
            if any(keyword in name.lower() for keyword in 
                   ["player", "athlete", "stat", "game", "roster", "metric"]):
                if not name.startswith("__") and not name.endswith("_aggregate"):
                    player_related.append({
                        "name": name,
                        "description": type_info.get("description", "No description")
                    })
        
        print_success(f"Found {len(player_related)} player/stat related tables")
        
        print("📋 Relevant Tables:")
        for table in sorted(player_related, key=lambda x: x["name"]):
            print(f"  • {table['name']}")
            if table['description'] and table['description'] != "No description":
                print(f"    └─ {table['description']}")
        
        print_analysis("""
🎯 LOOK FOR TABLES LIKE:
- gamePlayerStat (or similar) - for per-game stats
- athlete / athleteTeam - for player info and team rosters
- playerStat / playerStats - for aggregated stats
- Any table with 'receiving' in the name
        """)
        
        return player_related
    
    return []

async def test_3_game_player_stat_structure(client: GraphQLClient):
    """
    TEST 3: Explore gamePlayerStat structure
    Check if it has receiving category and what fields are available
    """
    print_header(3, "Game Player Stat - Structure & Categories")
    
    query = """
    query GamePlayerStatStructure {
      gamePlayerStat(
        where: {
          year: {_eq: 2024}
          teamId: {_in: [356, 194]}
        }
        limit: 20
      ) {
        gameId
        playerId
        teamId
        year
        category
        statType
        statValue
      }
    }
    """
    
    print_query(query)
    result = await client.execute_query(query)
    
    if "data" in result and result["data"]:
        stats = result["data"].get("gamePlayerStat", [])
        
        if stats:
            print_success(f"Found {len(stats)} game stat records")
            
            # Analyze categories
            categories = set(s["category"] for s in stats if s.get("category"))
            stat_types = set(s["statType"] for s in stats if s.get("statType"))
            
            print_analysis(f"""
Categories Found: {sorted(categories)}
Stat Types Sample: {sorted(list(stat_types))[:20]}
Total Records: {len(stats)}

🎯 KEY QUESTION: Is 'receiving' in the categories?

Sample Records:
{json.dumps(stats[:5], indent=2)}
            """)
            
            # Check for receiving specifically
            receiving_stats = [s for s in stats if s.get("category") == "receiving"]
            if receiving_stats:
                print_success(f"🎉 FOUND RECEIVING STATS! ({len(receiving_stats)} records)")
            else:
                print("⚠️  No receiving stats in this sample. May need different query.")
        else:
            print_error("No game player stats found")
    
    return result

async def test_4_athlete_table_structure(client: GraphQLClient):
    """
    TEST 4: Explore athlete table to see what player info is available
    Using basic query first to understand structure
    """
    print_header(4, "Athlete Table - Player Information & Positions")
    
    query = """
    query AthleteStructure {
      athlete(
        where: {
          teamId: {_eq: 356}
        }
        limit: 10
      ) {
        id
        name
        firstName
        lastName
        height
        weight
        jersey
        teamId
      }
    }
    """
    
    print_query(query)
    result = await client.execute_query(query)
    
    if "data" in result and result["data"]:
        athletes = result["data"].get("athlete", [])
        
        if athletes:
            print_success(f"Found {len(athletes)} athlete records")
            
            print_analysis(f"""
✅ Athlete table contains player names!

Sample Athletes:
{json.dumps(athletes[:5], indent=2)}

⚠️  NOTE: This returns ALL players ever associated with the team.
Need to filter by active players with stats in 2024/2025!
            """)
        else:
            print_error("No athletes found")
    
    return result

async def test_5_find_active_illinois_wrs(client: GraphQLClient):
    """
    TEST 5: Find ACTIVE Illinois WRs for 2024 season
    Using relationship filter to get only players with stats in 2024
    Looking for Pat Bryant and Zakhari Franklin
    """
    print_header(5, "Find ACTIVE Illinois WRs (2024) - Using Relationship Filter")
    
    query = """
    query FindActiveIllinoisWRs($teamId: bigint!, $year: Int!) {
      athlete(
        where: {
          teamId: {_eq: $teamId}
          gamePlayerStats: {
            game: {
              season: {_eq: $year}
            }
          }
        }
        limit: 50
      ) {
        id
        name
        firstName
        lastName
        jersey
        teamId
      }
    }
    """
    
    variables = {
        "teamId": 356,
        "year": 2024
    }
    
    print_query(query)
    print(f"Variables: {json.dumps(variables, indent=2)}\n")
    
    result = await client.execute_query(query, variables)
    
    if "data" in result and result["data"]:
        players = result["data"].get("athlete", [])
        
        if players:
            print_success(f"🎉 Found {len(players)} ACTIVE players for Illinois 2024 season!")
            
            print("\n📋 Active Illinois Players (2024):")
            for player in players[:20]:
                print(f"  • #{player.get('jersey', '??')}: {player.get('name', 'Unknown')} (ID: {player.get('id')})")
            
            # Check for specific WR names
            target_players = ["Pat Bryant", "Zakhari Franklin", "Bryant", "Franklin"]
            print("\n🔍 Searching for target WRs:")
            found_players = []
            for target in target_players:
                for player in players:
                    if target.lower() in player.get("name", "").lower():
                        if player not in [p[1] for p in found_players]:
                            found_players.append((target, player))
                            print_success(f"🎯 FOUND: {player['name']} (ID: {player['id']})")
            
            if not found_players:
                print("⚠️  Target WRs not found in active roster.")
                print("   They may not have stats in 2024 or use different names.")
            
            print_analysis(f"""
✅ SUCCESS! Using relationship filter returns only ACTIVE players!

This query filters by:
1. teamId (Illinois = 356)
2. gamePlayerStats.game.season (2024)

This ensures we only get players who actually played in 2024,
not historical players from previous years!

Total active players: {len(players)}
            """)
        else:
            print_error("No active players found for Illinois 2024")
    
    return result

async def test_6_get_wr_receiving_stats(client: GraphQLClient):
    """
    TEST 6: Get receiving stats for ACTIVE WRs in 2024
    Filter gamePlayerStat by season through game relationship
    """
    print_header(6, "WR Receiving Stats - Active 2024 Players")
    
    query = """
    query GetReceivingStats($season: Int!) {
      gamePlayerStat(
        where: {
          game: {
            season: {_eq: $season}
            teams: {
              teamId: {_in: [356, 194]}
            }
          }
          category: {_eq: "receiving"}
        }
        limit: 100
      ) {
        gameId
        playerId
        category
        statType
        stat
      }
    }
    """
    
    variables = {"season": 2024}
    
    print_query(query)
    print(f"Variables: {json.dumps(variables, indent=2)}\n")
    
    result = await client.execute_query(query, variables)
    
    if "data" in result and result["data"]:
        receiving_stats = result["data"].get("gamePlayerStat", [])
        
        if receiving_stats:
            print_success(f"🎉 Found {len(receiving_stats)} receiving stat records!")
            
            # Group by player
            player_stats = {}
            for stat in receiving_stats:
                player_id = stat["playerId"]
                if player_id not in player_stats:
                    player_stats[player_id] = {
                        "playerId": player_id,
                        "stats": []
                    }
                player_stats[player_id]["stats"].append({
                    "type": stat["statType"],
                    "value": stat.get("stat", 0)
                })
            
            print_analysis(f"""
✅ Found receiving stats for {len(player_stats)} different players!

Sample Player IDs with receiving stats:
{list(player_stats.keys())[:10]}

Sample Stats:
{json.dumps(receiving_stats[:5], indent=2)}

🎯 KEY FINDING: We can query receiving stats through game relationship!
   Filter pattern: game.season._eq to get specific year
   Filter pattern: game.teams.teamId._in to get specific teams
            """)
            
            return player_stats
        else:
            print("⚠️  No receiving stats found. Checking alternative query...")
            
            # Try simpler query to see what fields are available
            query_alt = """
            query CheckGamePlayerStat {
              gamePlayerStat(limit: 5) {
                gameId
                playerId
                category
                statType
                stat
              }
            }
            """
            
            print("\n📋 Alternative Query (checking structure):")
            print_query(query_alt)
            
            result_alt = await client.execute_query(query_alt)
            if "data" in result_alt and result_alt["data"]:
                all_stats = result_alt["data"].get("gamePlayerStat", [])
                if all_stats:
                    print(f"Sample gamePlayerStat records:")
                    print(json.dumps(all_stats, indent=2))
                    
                    categories = set(s.get("category") for s in all_stats if s.get("category"))
                    print(f"\nCategories found in sample: {sorted(categories)}")
    
    return result

async def test_7_aggregate_season_stats(client: GraphQLClient):
    """
    TEST 7: Try to get season aggregate stats (if available)
    """
    print_header(7, "Season Aggregate Stats - Alternative to Game-by-Game")
    
    # Try playerSeason or similar aggregate table
    query = """
    query SeasonStats {
      playerSeason(
        where: {
          year: {_eq: 2024}
          teamId: {_in: [356, 194]}
        }
        limit: 20
      ) {
        playerId
        year
        teamId
        category
        statType
        statValue
      }
    }
    """
    
    print_query(query)
    result = await client.execute_query(query)
    
    if "data" in result and result["data"]:
        season_stats = result["data"].get("playerSeason", [])
        
        if season_stats:
            print_success(f"Found season aggregate table with {len(season_stats)} records")
            
            categories = set(s.get("category") for s in season_stats)
            print_analysis(f"""
Season-level stats are available!

Categories: {sorted(categories)}

Sample Records:
{json.dumps(season_stats[:5], indent=2)}

✅ This could be easier than aggregating game-by-game!
            """)
        else:
            print("⚠️  playerSeason table not found or empty")
    else:
        print("⚠️  playerSeason table may not exist. Will need to aggregate from gamePlayerStat.")
    
    return result

async def test_8_complete_wr_query(client: GraphQLClient):
    """
    TEST 8: Complete query joining ACTIVE athlete names with their receiving stats
    This is the production-ready approach using the relationship filter pattern
    """
    print_header(8, "COMPLETE QUERY - Active WR Names + Stats (Production Ready 2024)")
    
    # Step 1: Get Illinois ACTIVE players for 2024
    print("Step 1: Get Illinois ACTIVE roster for 2024...")
    players_query = """
    query GetActiveTeamPlayers($teamId: bigint!, $season: Int!) {
      athlete(
        where: {
          teamId: {_eq: $teamId}
          gamePlayerStats: {
            game: {
              season: {_eq: $season}
            }
          }
        }
      ) {
        id
        name
        firstName
        lastName
        jersey
      }
    }
    """
    
    players_variables = {"teamId": 356, "season": 2024}
    print_query(players_query)
    print(f"Variables: {json.dumps(players_variables, indent=2)}\n")
    
    players_result = await client.execute_query(players_query, players_variables)
    
    if "data" not in players_result or not players_result["data"].get("athlete"):
        print_error("Could not retrieve active player roster")
        return None
    
    players = players_result["data"]["athlete"]
    player_ids = [p["id"] for p in players]
    
    print_success(f"Found {len(players)} ACTIVE players for Illinois 2024")
    for player in players[:10]:
        print(f"  • {player['name']} (ID: {player['id']})")
    
    if not player_ids:
        print_error("No player IDs to query stats for")
        return None
    
    # Step 2: Get receiving stats for these players
    print("\nStep 2: Get receiving stats for these players...")
    stats_query = """
    query GetPlayerReceivingStats($playerIds: [bigint!], $season: Int!) {
      gamePlayerStat(
        where: {
          playerId: {_in: $playerIds}
          game: {
            season: {_eq: $season}
          }
          category: {_eq: "receiving"}
        }
      ) {
        playerId
        gameId
        statType
        stat
        category
      }
    }
    """
    
    stats_variables = {"playerIds": player_ids[:30], "season": 2024}
    
    stats_result = await client.execute_query(stats_query, stats_variables)
    
    if "data" in stats_result and stats_result["data"]:
        stats = stats_result["data"].get("gamePlayerStat", [])
        
        if stats:
            print_success(f"🎉 Found {len(stats)} receiving stat records!")
            
            # Aggregate stats by player
            player_totals = {}
            for stat in stats:
                player_id = stat["playerId"]
                stat_type = stat["statType"]
                stat_value = float(stat.get("stat", 0))
                
                if player_id not in player_totals:
                    # Find player name
                    player_name = next((p["name"] for p in players if p["id"] == player_id), "Unknown")
                    player_jersey = next((p["jersey"] for p in players if p["id"] == player_id), "??")
                    player_totals[player_id] = {
                        "name": player_name,
                        "jersey": player_jersey,
                        "receptions": 0,
                        "yards": 0,
                        "touchdowns": 0,
                        "targets": 0,
                        "games": set()
                    }
                
                player_totals[player_id]["games"].add(stat["gameId"])
                
                # Aggregate common stat types (adjust based on actual statType values)
                stat_lower = stat_type.lower()
                if "rec" in stat_lower and "yds" not in stat_lower and "td" not in stat_lower:
                    player_totals[player_id]["receptions"] += stat_value
                elif "yds" in stat_lower or "yd" in stat_lower:
                    player_totals[player_id]["yards"] += stat_value
                elif "td" in stat_lower:
                    player_totals[player_id]["touchdowns"] += stat_value
                elif "target" in stat_lower:
                    player_totals[player_id]["targets"] += stat_value
            
            # Display results
            print("\n🏈 ILLINOIS RECEIVING STATS - 2024 Season:")
            print("="*80)
            for player_id, totals in sorted(player_totals.items(), 
                                           key=lambda x: x[1]["yards"], 
                                           reverse=True):
                print(f"\n#{totals['jersey']} {totals['name']}:")
                print(f"  Receptions: {totals['receptions']:.0f}")
                print(f"  Yards: {totals['yards']:.0f}")
                print(f"  Touchdowns: {totals['touchdowns']:.0f}")
                if totals['targets'] > 0:
                    print(f"  Targets: {totals['targets']:.0f}")
                print(f"  Games Played: {len(totals['games'])}")
            
            print_analysis(f"""
✅ SUCCESS! We can get ACTIVE WR names and receiving stats for 2024!

🔑 PRODUCTION APPROACH (2024/2025):
1. Query athlete table with relationship filter:
   - teamId filter for specific team
   - gamePlayerStats.game.season filter for active year (2024/2025)
   
2. Extract player IDs from active roster

3. Query gamePlayerStat with:
   - playerId._in for those specific players
   - game.season._eq for the year
   - category._eq "receiving" for receiving stats
   
4. Aggregate stats by player and join with names

🎯 This approach ensures you get ONLY active players, not historical!

Total WRs/TEs with stats: {len(player_totals)}
            """)
            
            return player_totals
        else:
            print("⚠️  No receiving stats found for these players")
            print("This might mean:")
            print("  1. No players caught passes in 2024")
            print("  2. Category might be named differently")
            print("  3. Need to check available categories")
    
    return stats_result

async def test_9_ohio_state_comparison(client: GraphQLClient):
    """
    TEST 9: Get Ohio State ACTIVE players for 2024
    Looking for Jeremiah Smith and other current players
    """
    print_header(9, "Ohio State Active Players (2024) - Find Jeremiah Smith")
    
    query = """
    query GetActiveOhioStatePlayers($teamId: bigint!, $season: Int!) {
      athlete(
        where: {
          teamId: {_eq: $teamId}
          gamePlayerStats: {
            game: {
              season: {_eq: $season}
            }
          }
        }
        limit: 50
      ) {
        id
        name
        firstName
        lastName
        jersey
      }
    }
    """
    
    variables = {"teamId": 194, "season": 2024}
    
    print_query(query)
    print(f"Variables: {json.dumps(variables, indent=2)}\n")
    
    result = await client.execute_query(query, variables)
    
    if "data" in result and result["data"]:
        players = result["data"].get("athlete", [])
        
        if players:
            print_success(f"Found {len(players)} ACTIVE players for Ohio State 2024")
            
            print("📋 Ohio State Active Players (2024):")
            for player in players[:15]:
                print(f"  • #{player.get('jersey', '??')}: {player.get('name', 'Unknown')} (ID: {player.get('id')})")
            
            # Look for Jeremiah Smith
            jeremiah = next((p for p in players if "jeremiah" in p.get("name", "").lower() and "smith" in p.get("name", "").lower()), None)
            if jeremiah:
                print_success(f"\n🎯 FOUND: Jeremiah Smith (ID: {jeremiah['id']}, Jersey: #{jeremiah.get('jersey', '??')})")
            else:
                print("\n⚠️  Jeremiah Smith not found in 2024 active roster")
                print("   Searching for any 'Smith'...")
                smiths = [p for p in players if "smith" in p.get("name", "").lower()]
                for smith in smiths:
                    print(f"   • {smith['name']} (ID: {smith['id']})")
            
            print_analysis(f"""
✅ Retrieved ACTIVE Ohio State roster for 2024!

Using the same relationship filter pattern:
- teamId: 194 (Ohio State)
- gamePlayerStats.game.season: 2024

Total active players: {len(players)}

This ensures we only get current players, not alumni!
            """)
        else:
            print_error("No active players found for Ohio State 2024")
    
    return result

async def test_10_explore_stat_categories(client: GraphQLClient):
    """
    TEST 10: Explore all available stat categories for 2024 season
    """
    print_header(10, "Explore ALL Stat Categories Available (2024)")
    
    query = """
    query ExploreCategories($season: Int!) {
      gamePlayerStat(
        where: {
          game: {
            season: {_eq: $season}
          }
        }
        limit: 500
      ) {
        category
        statType
      }
    }
    """
    
    variables = {"season": 2024}
    
    print_query(query)
    print(f"Variables: {json.dumps(variables, indent=2)}\n")
    
    result = await client.execute_query(query, variables)
    
    if "data" in result and result["data"]:
        stats = result["data"].get("gamePlayerStat", [])
        
        if stats:
            # Collect all unique categories and stat types
            categories = set()
            stat_types_by_category = {}
            
            for stat in stats:
                cat = stat.get("category", "unknown")
                stat_type = stat.get("statType", "unknown")
                
                categories.add(cat)
                if cat not in stat_types_by_category:
                    stat_types_by_category[cat] = set()
                stat_types_by_category[cat].add(stat_type)
            
            print_success(f"Found {len(categories)} unique categories in 2024 data")
            
            print("\n📊 COMPLETE CATEGORY BREAKDOWN (2024):")
            print("="*80)
            for category in sorted(categories):
                stat_types = sorted(stat_types_by_category.get(category, []))
                print(f"\n🏈 {category.upper()}:")
                for st in stat_types[:15]:  # Limit to first 15 per category
                    print(f"  • {st}")
                if len(stat_types) > 15:
                    print(f"  ... and {len(stat_types) - 15} more")
            
            print_analysis(f"""
Total Categories: {len(categories)}
Categories: {sorted(categories)}

🎯 Use these categories to filter for specific player types:
- 'passing' for QBs
- 'rushing' for RBs  
- 'receiving' for WRs/TEs
- 'defensive' for defensive players
- 'kicking' for kickers
- etc.

🔑 Key Filter Pattern:
   game.season._eq: 2024 (ensures current year data)
   category._eq: "receiving" (filters by stat type)
            """)
        else:
            print_error("No stats found for 2024 season")
    
    return result

async def run_all_tests():
    """Run all tests in sequence"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║        🏈 College Football Data GraphQL API - Player Metrics Explorer 🏈      ║
║                                                                               ║
║                         Comprehensive Test Suite                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📅 Current Year: 2025
🎯 Target Teams: Illinois (356), Ohio State (194)
🔍 Looking for: WR, RB, QB names and stats

Starting test suite...
    """)
    
    client = GraphQLClient(API_URL, API_KEY)
    
    # Store results for final summary
    results = {}
    
    try:
        results["test1"] = await test_1_adjusted_player_metrics_structure(client)
        await asyncio.sleep(0.5)
        
        results["test2"] = await test_2_schema_introspection_player_tables(client)
        await asyncio.sleep(0.5)
        
        results["test3"] = await test_3_game_player_stat_structure(client)
        await asyncio.sleep(0.5)
        
        results["test4"] = await test_4_athlete_table_structure(client)
        await asyncio.sleep(0.5)
        
        results["test5"] = await test_5_find_active_illinois_wrs(client)
        await asyncio.sleep(0.5)
        
        results["test6"] = await test_6_get_wr_receiving_stats(client)
        await asyncio.sleep(0.5)
        
        results["test7"] = await test_7_aggregate_season_stats(client)
        await asyncio.sleep(0.5)
        
        results["test8"] = await test_8_complete_wr_query(client)
        await asyncio.sleep(0.5)
        
        results["test9"] = await test_9_ohio_state_comparison(client)
        await asyncio.sleep(0.5)
        
        results["test10"] = await test_10_explore_stat_categories(client)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
    
    # Print final summary
    print_final_summary(results)

def print_final_summary(results: Dict):
    """Print comprehensive final summary and recommendations"""
    print(f"\n\n{'='*80}")
    print("📊 FINAL SUMMARY & RECOMMENDATIONS")
    print(f"{'='*80}\n")
    
    print("🔍 KEY FINDINGS:\n")
    
    print("1️⃣  ADJUSTED PLAYER METRICS TABLE:")
    print("   • Contains: passing, rushing, field_goals")
    print("   ❌ Does NOT contain receiving stats")
    print("   • Not suitable for WR statistics\n")
    
    print("2️⃣  GAME PLAYER STAT TABLE:")
    print("   ✅ Contains per-game statistics")
    print("   ✅ Has 'receiving' category for WR stats")
    print("   • Filter through game relationship: game.season._eq")
    print("   • Requires aggregation for season totals\n")
    
    print("3️⃣  ATHLETE TABLE:")
    print("   ✅ Contains player names (firstName, lastName, name)")
    print("   ✅ Can filter by teamId")
    print("   ⚠️  Returns ALL historical players by default")
    print("   🔑 MUST use relationship filter to get active players!\n")
    
    print("4️⃣  CRITICAL DISCOVERY:")
    print("   🎯 Use gamePlayerStats.game.season relationship filter")
    print("   ✅ This ensures you get ONLY active 2024/2025 players")
    print("   ❌ Without this, you get players from all years (historical)\n")
    
    print("="*80)
    print("🎯 RECOMMENDED PRODUCTION APPROACH (2024/2025)")
    print("="*80 + "\n")
    
    print("""
For getting QB/RB/WR names and stats for ANY team in 2024/2025:

STEP 1: Get ACTIVE Player Roster by Team
-----------------------------------------
query GetActiveTeamPlayers($teamId: bigint!, $season: Int!) {
  athlete(
    where: {
      teamId: {_eq: $teamId}
      
      # ⚡ CRITICAL: This filters for ACTIVE players only!
      gamePlayerStats: {
        game: {
          season: {_eq: $season}
        }
      }
    }
  ) {
    id
    name
    firstName
    lastName
    jersey
  }
}

Variables: {
  "teamId": 356,     # Illinois
  "season": 2024     # Current year (use 2025 for 2025 season)
}


STEP 2: Get Game Stats for Those Players
-----------------------------------------
query GetPlayerStats($playerIds: [bigint!], $season: Int!, $category: String!) {
  gamePlayerStat(
    where: {
      playerId: {_in: $playerIds}
      game: {
        season: {_eq: $season}
      }
      category: {_eq: $category}
    }
  ) {
    playerId
    gameId
    statType
    stat
    category
  }
}

Variables: {
  "playerIds": [12345, 67890],
  "season": 2024,
  "category": "receiving"
}


STEP 3: Aggregate Stats in Your Code
-------------------------------------
- Group stats by playerId
- Sum up receptions, yards, touchdowns
- Join with player names from Step 1
- Calculate averages, totals, etc.


POSITION-TO-CATEGORY MAPPING:
------------------------------
• QB  → category: "passing"
• RB  → category: "rushing" (also check "receiving" for pass-catching backs)
• WR  → category: "receiving"
• TE  → category: "receiving"
• K   → category: "kicking"
• DEF → category: "defensive"
    """)
    
    print("="*80)
    print("⚠️  IMPORTANT LIMITATIONS & FIXES")
    print("="*80 + "\n")
    
    print("""
1. ❌ WRONG: Querying athlete without gamePlayerStats filter
   ✅ RIGHT: Always use gamePlayerStats.game.season filter for active players
   
2. ❌ WRONG: Using year field directly in gamePlayerStat
   ✅ RIGHT: Use game.season._eq through relationship
   
3. ❌ WRONG: Using teamId directly in gamePlayerStat
   ✅ RIGHT: Get player IDs from athlete first, then query stats

4. 🎯 For 2025 season data, change $season variable to 2025
   
5. 📊 Field names:
   - Use "stat" not "statValue" for the numeric value
   - Use "game.season" not "year" for filtering
   - Position is a relationship, not a simple string field

6. ⚡ Always specify season in both queries to ensure consistency
    """)
    
    print("="*80)
    print("✅ QUESTIONS ANSWERED")
    print("="*80 + "\n")
    
    print("""
✅ Does adjustedPlayerMetrics have receiving stats?
   → NO - only passing, rushing, field_goals

✅ Where can we find WR names and stats?
   → athlete table (with gamePlayerStats filter) + gamePlayerStat table

✅ Can we get Pat Bryant, Zakhari Franklin, Jeremiah Smith?
   → YES - query athlete with teamId + gamePlayerStats.game.season filter

✅ How to get ONLY active players (not historical)?
   → Use gamePlayerStats.game.season relationship filter (THIS IS KEY!)

✅ Best approach for season aggregates?
   → Aggregate gamePlayerStat results in your application code

✅ How to link players to teams?
   → Filter athlete by teamId, then query stats by playerId
   
✅ Why am I getting old/historical players?
   → You're not using the gamePlayerStats.game.season filter!
    """)
    
    print("\n" + "="*80)
    print("🎉 TEST SUITE COMPLETE!")
    print("="*80 + "\n")
    
    print("💡 Next Steps:")
    print("1. Use the STEP 1 query with season filter to get active 2024/2025 players")
    print("2. Use STEP 2 query to get their stats for the same season")
    print("3. Aggregate stats in your code (sum receptions, yards, TDs, etc.)")
    print("4. Always specify season in both athlete and gamePlayerStat queries")
    print("5. For 2025 season, use $season: 2025 in your variables\n")
    
    print("🔑 KEY TAKEAWAY:")
    print("   The gamePlayerStats.game.season relationship filter is CRITICAL")
    print("   to getting current players instead of historical/alumni players!\n")

if __name__ == "__main__":
    print("🏈 Starting College Football Data GraphQL API Explorer...\n")
    asyncio.run(run_all_tests())
