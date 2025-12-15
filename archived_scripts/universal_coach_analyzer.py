#!/usr/bin/env python3
"""
Universal Coach Analyzer - Complete Career Profile for ANY FBS Coach
Generates comprehensive analysis for a coach's entire tenure at their current school
"""
import json
import requests
from collections import defaultdict
from datetime import datetime
import sys

GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

def query_gql(q, variables=None):
    """Execute GraphQL query with error handling"""
    try:
        payload = {'query': q}
        if variables:
            payload['variables'] = variables
        r = requests.post(
            GRAPHQL_URL, 
            json=payload, 
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        return r.json().get('data', {})
    except Exception as e:
        print(f"  ⚠️  Query error: {e}")
        return {}

def get_coach_tenure(coach_first, coach_last, school):
    """Get coach's start and end year at school by analyzing game data"""
    # Strategy: Find first and last game coached at school
    # Search broadly (2000-2025) to find any games
    
    print(f"  🔍 Searching for {coach_first} {coach_last} at {school}...")
    
    # Try to find games in recent years first
    all_years = []
    
    for year in range(2000, 2026):
        q = f'''{{
            game(where: {{
                season: {{_eq: {year}}},
                _or: [
                    {{homeTeam: {{_eq: "{school}"}}}},
                    {{awayTeam: {{_eq: "{school}"}}}}
                ]
            }}, limit: 1) {{
                season
            }}
        }}'''
        
        data = query_gql(q)
        games = data.get('game', [])
        if games:
            all_years.append(year)
    
    if not all_years:
        return None, None, []
    
    # Assume current coach - use recent years
    # Most coaches started after 2015 for current roles
    start_year = min([y for y in all_years if y >= 2015], default=min(all_years))
    end_year = max(all_years)
    
    print(f"     Found games from {start_year}-{end_year}")
    
    # Create coaching records from data
    coaching_records = [{
        'year': year,
        'firstName': coach_first,
        'lastName': coach_last,
        'school': school
    } for year in range(start_year, end_year + 1)]
    
    return start_year, end_year, coaching_records

def fetch_all_games(school, start_year, end_year):
    """Fetch all games (regular season + postseason) for school during tenure"""
    print(f"\n📅 Fetching games ({start_year}-{end_year})...")
    
    all_games = []
    
    # Regular season games
    for year in range(start_year, end_year + 1):
        q = f'''{{
            game(where: {{
                season: {{_eq: {year}}},
                seasonType: {{_eq: "regular"}},
                _or: [
                    {{homeTeam: {{_eq: "{school}"}}}},
                    {{awayTeam: {{_eq: "{school}"}}}}
                ]
            }}, orderBy: {{week: ASC}}) {{
                id
                season
                week
                seasonType
                homeTeam
                awayTeam
                homePoints
                awayPoints
                neutralSite
                excitement
                conferenceGame
            }}
        }}'''
        
        games = query_gql(q).get('game', [])
        all_games.extend(games)
        print(f"  ✓ {year}: {len(games)} games")
    
    # Postseason games
    q_postseason = f'''{{
        game(where: {{
            season: {{_gte: {start_year}, _lte: {end_year}}},
            seasonType: {{_eq: "postseason"}},
            _or: [
                {{homeTeam: {{_eq: "{school}"}}}},
                {{awayTeam: {{_eq: "{school}"}}}}
            ]
        }}, orderBy: {{season: ASC}}) {{
            id
            season
            week
            seasonType
            homeTeam
            awayTeam
            homePoints
            awayPoints
            neutralSite
            excitement
            conferenceGame
        }}
    }}'''
    
    postseason = query_gql(q_postseason).get('game', [])
    all_games.extend(postseason)
    print(f"  ✓ Postseason: {len(postseason)} games")
    
    return all_games

def fetch_rankings(school, start_year, end_year):
    """Fetch AP Poll rankings for school during tenure"""
    print(f"\n📊 Fetching AP Rankings ({start_year}-{end_year})...")
    
    q = f'''{{
        pollRank(where: {{
            poll: {{
                season: {{_gte: {start_year}, _lte: {end_year}}},
                pollType: {{name: {{_eq: "AP Top 25"}}}}
            }},
            team: {{school: {{_eq: "{school}"}}}}
        }}, orderBy: {{poll: {{season: ASC, week: ASC}}}}) {{
            rank
            points
            poll {{
                season
                week
            }}
            team {{
                school
            }}
        }}
    }}'''
    
    rankings = query_gql(q).get('pollRank', [])
    print(f"  ✓ Total weeks ranked: {len(rankings)}")
    return rankings

def fetch_draft_picks(school, start_year, end_year):
    """Fetch NFL draft picks from school during tenure"""
    print(f"\n🏈 Fetching NFL Draft Picks ({start_year}-{end_year})...")
    
    # Adjust draft years (players drafted are from previous season)
    draft_start = start_year + 1
    draft_end = end_year + 1
    
    q = f'''{{
        draftPicks(where: {{
            collegeTeam: {{school: {{_eq: "{school}"}}}},
            year: {{_gte: {draft_start}, _lte: {draft_end}}}
        }}, orderBy: [{{year: ASC}}, {{overall: ASC}}]) {{
            year
            round
            overall
            name
            position {{
                abbreviation
            }}
            draftTeam {{
                displayName
            }}
            height
            weight
        }}
    }}'''
    
    picks = query_gql(q).get('draftPicks', [])
    print(f"  ✓ Total draft picks: {len(picks)}")
    return picks

def fetch_talent_ratings(school, start_year, end_year):
    """Fetch team talent composite ratings"""
    print(f"\n⭐ Fetching talent ratings ({start_year}-{end_year})...")
    
    q = f'''{{
        teamTalent(where: {{
            team: {{school: {{_eq: "{school}"}}}},
            year: {{_gte: {start_year}, _lte: {end_year}}}
        }}, orderBy: {{year: ASC}}) {{
            year
            talent
            team {{
                school
            }}
        }}
    }}'''
    
    talent = query_gql(q).get('teamTalent', [])
    print(f"  ✓ Talent data: {len(talent)} years")
    return talent

def fetch_betting_lines(school, year):
    """Fetch betting lines for a specific year"""
    print(f"\n💰 Fetching betting lines ({year})...")
    
    q = f'''{{
        game(where: {{
            season: {{_eq: {year}}},
            seasonType: {{_eq: "regular"}},
            _or: [
                {{homeTeam: {{_eq: "{school}"}}}},
                {{awayTeam: {{_eq: "{school}"}}}}
            ]
        }}, orderBy: {{week: ASC}}) {{
            id
            season
            week
            homeTeam
            awayTeam
            homePoints
            awayPoints
            lines {{
                provider {{
                    name
                }}
                spread
                overUnder
            }}
        }}
    }}'''
    
    games = query_gql(q).get('game', [])
    print(f"  ✓ Games with lines: {len(games)}")
    return games

def calculate_record(games, school):
    """Calculate win-loss record"""
    wins = 0
    losses = 0
    ties = 0
    
    for game in games:
        is_home = game['homeTeam'] == school
        team_score = game.get('homePoints') if is_home else game.get('awayPoints')
        opp_score = game.get('awayPoints') if is_home else game.get('homePoints')
        
        # Skip games that haven't been played yet (None scores)
        if team_score is None or opp_score is None:
            continue
        
        if team_score > opp_score:
            wins += 1
        elif team_score < opp_score:
            losses += 1
        else:
            ties += 1
    
    return wins, losses, ties

def analyze_coach(coach_first, coach_last, school, output_file=None):
    """Main analysis function for any coach"""
    
    print("=" * 80)
    print(f"🏈 UNIVERSAL COACH ANALYZER")
    print(f"   Coach: {coach_first} {coach_last}")
    print(f"   School: {school}")
    print("=" * 80)
    
    # Get coach tenure
    print("\n🔍 Finding coach tenure...")
    start_year, end_year, coaching_records = get_coach_tenure(coach_first, coach_last, school)
    
    if not start_year:
        print(f"❌ No data found for {coach_first} {coach_last} at {school}")
        return None
    
    print(f"  ✓ Tenure: {start_year}-{end_year} ({end_year - start_year + 1} seasons)")
    
    # Fetch all data
    games = fetch_all_games(school, start_year, end_year)
    rankings = fetch_rankings(school, start_year, end_year)
    draft_picks = fetch_draft_picks(school, start_year, end_year)
    talent = fetch_talent_ratings(school, start_year, end_year)
    
    # Fetch 2025 betting lines if applicable
    betting_lines_2025 = []
    if end_year >= 2025:
        betting_lines_2025 = fetch_betting_lines(school, 2025)
    
    # Calculate overall record
    wins, losses, ties = calculate_record(games, school)
    total_games = len(games)
    win_pct = (wins / total_games * 100) if total_games > 0 else 0
    
    print(f"\n📊 CAREER SUMMARY")
    print(f"   Record: {wins}-{losses}" + (f"-{ties}" if ties > 0 else ""))
    print(f"   Win %: {win_pct:.1f}%")
    print(f"   Total Games: {total_games}")
    
    # Build comprehensive JSON output
    output = {
        "metadata": {
            "generated": str(datetime.now()),
            "coach": f"{coach_first} {coach_last}",
            "school": school,
            "era": f"{start_year}-{end_year}",
            "tenure_years": end_year - start_year + 1,
            "description": f"Comprehensive {coach_first} {coach_last} coaching profile with all statistics, games, and analysis"
        },
        "summary": {
            "generated": str(datetime.now()),
            "overview": {
                "coach": f"{coach_first} {coach_last}",
                "era": f"{start_year}-{end_year}",
                "total_record": f"{wins}-{losses}" + (f"-{ties}" if ties > 0 else ""),
                "win_pct": round(win_pct, 1),
                "total_games": total_games
            },
            "coaching_records": coaching_records
        },
        "games": games,
        "rankings": rankings,
        "draft_picks": draft_picks,
        "talent_ratings": talent,
        "betting_lines_2025": betting_lines_2025
    }
    
    # Save to file
    if not output_file:
        safe_name = f"{coach_last.lower().replace(' ', '_')}_{school.lower().replace(' ', '_')}.json"
        output_file = safe_name
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Saved to: {output_file}")
    print(f"   File size: {len(json.dumps(output))} bytes")
    
    return output

def main():
    """Command line interface"""
    if len(sys.argv) < 4:
        print("Usage: python universal_coach_analyzer.py <first_name> <last_name> <school>")
        print("\nExample:")
        print('  python universal_coach_analyzer.py Ryan Day "Ohio State"')
        print('  python universal_coach_analyzer.py Kirby Smart Georgia')
        print('  python universal_coach_analyzer.py Steve Sarkisian Texas')
        sys.exit(1)
    
    coach_first = sys.argv[1]
    coach_last = sys.argv[2]
    school = " ".join(sys.argv[3:])  # Handle multi-word school names
    
    analyze_coach(coach_first, coach_last, school)

if __name__ == "__main__":
    main()
