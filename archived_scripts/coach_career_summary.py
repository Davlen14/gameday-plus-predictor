#!/usr/bin/env python3
"""
Universal Coach Career Summary Generator with AI Enhancement
Analyzes any coach's career from enhanced_coaches_v2 JSON files
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict
from google import genai

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyAXjMNN_vK2BpO4VQehdkCnivCAiat8lso"
client = genai.Client(api_key=GEMINI_API_KEY)

def load_coach_data(filepath):
    """Load the coach data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def print_header(title, char='='):
    """Print a formatted header"""
    print(f"\n{char * 80}")
    print(f"{title.center(80)}")
    print(f"{char * 80}\n")

def print_section(title):
    """Print a section header"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")

def get_coach_name(data):
    """Extract coach name from data"""
    if 'metadata' in data and 'coach' in data['metadata']:
        return data['metadata']['coach']
    return "Unknown Coach"

def summarize_basic_info(data):
    """Display basic coach information"""
    coach_name = get_coach_name(data)
    print_header(f"{coach_name.upper()} - COMPREHENSIVE CAREER ANALYSIS")

    meta = data.get('metadata', {})
    career = data.get('career_summary', {})

    print(f"👤 Coach: {coach_name}")
    print(f"🏫 Schools: {', '.join(meta.get('schools', []))}")
    print(f"📅 Analysis Generated: {meta.get('generated', datetime.now().isoformat())}")

    print(f"\n📊 CAREER OVERVIEW")
    print(f"   Overall Record: {career.get('record', 'N/A')}")
    print(f"   Win Percentage: {career.get('win_pct', 0):.1f}%")
    print(f"   Total Games: {career.get('games', 0)}")

def analyze_stints(data):
    """Analyze each coaching stint"""
    print_section("COACHING STINTS")

    stints = data.get('stints', [])

    for stint in stints:
        school = stint.get('school', 'Unknown')
        start = stint.get('start_year', '?')
        end = stint.get('end_year', 'Present')
        record = stint.get('record', '0-0')
        win_pct = stint.get('win_pct', 0)
        games = stint.get('games', 0)

        print(f"\n{'═' * 60}")
        print(f"  🏟️  {school} ({start}-{end})")
        print(f"{'═' * 60}")
        print(f"   Record: {record} ({win_pct:.1f}% in {games} games)")

def analyze_games(data):
    """Analyze game-level statistics"""
    print_section("GAME-BY-GAME ANALYSIS")

    games = data.get('games', [])
    if not games:
        print("No game data available")
        return

    school_name = data.get('metadata', {}).get('schools', ['Unknown'])[0]

    # Calculate basic stats - determine if home or away for each game
    total_games = len(games)
    wins = 0
    losses = 0
    total_points = 0
    total_opp_points = 0

    for g in games:
        is_home = g.get('homeTeam') == g.get('school') or (g.get('school') and g.get('school') in g.get('homeTeam', ''))
        is_away = g.get('awayTeam') == g.get('school') or (g.get('school') and g.get('school') in g.get('awayTeam', ''))

        if is_home:
            team_points = g.get('homePoints', 0)
            opp_points = g.get('awayPoints', 0)
        elif is_away:
            team_points = g.get('awayPoints', 0)
            opp_points = g.get('homePoints', 0)
        else:
            # Fallback - use first stint's school
            team_points = g.get('awayPoints', 0) if g.get('awayTeam', '').lower() in str(g.get('school', '')).lower() else g.get('homePoints', 0)
            opp_points = g.get('homePoints', 0) if g.get('awayTeam', '').lower() in str(g.get('school', '')).lower() else g.get('awayPoints', 0)

        total_points += team_points
        total_opp_points += opp_points

        if team_points > opp_points:
            wins += 1
        else:
            losses += 1

    # Home/Away/Neutral splits
    home_games = [g for g in games if g.get('location') == 'H']
    away_games = [g for g in games if g.get('location') == 'A']
    neutral_games = [g for g in games if g.get('location') == 'N']

    home_wins = sum(1 for g in home_games if g.get('result') == 'W')
    away_wins = sum(1 for g in away_games if g.get('result') == 'W')
    neutral_wins = sum(1 for g in neutral_games if g.get('result') == 'W')

    # Ranked opponent stats
    ranked_games = [g for g in games if g.get('opp_rank') and int(g.get('opp_rank', 999)) <= 25]
    ranked_wins = sum(1 for g in ranked_games if g.get('result') == 'W')

    # Close games (decided by 7 or less)
    close_games = []
    for g in games:
        points = g.get('points', 0)
        opp_points = g.get('opp_points', 0)
        if abs(points - opp_points) <= 7:
            close_games.append(g)
    close_wins = sum(1 for g in close_games if g.get('result') == 'W')

    print(f"\n📊 Overall Performance:")
    print(f"   Total Games: {total_games}")
    print(f"   Record: {wins}-{losses} ({wins/total_games:.1%})")

    print(f"\n⚡ Scoring Statistics:")
    print(f"   Points/Game: {total_points/total_games:.1f}")
    print(f"   Opp Points/Game: {total_opp_points/total_games:.1f}")
    print(f"   Point Differential: {(total_points - total_opp_points)/total_games:+.1f}")

    print(f"\n🏅 vs Ranked Opponents:")
    print(f"   Games: {len(ranked_games)}")
    if ranked_games:
        print(f"   Record: {ranked_wins}-{len(ranked_games)-ranked_wins} ({ranked_wins/len(ranked_games):.1%})")

    print(f"\n🏟️  Location Splits:")
    if home_games:
        print(f"   Home: {home_wins}-{len(home_games)-home_wins} ({home_wins/len(home_games):.1%})")
    if away_games:
        print(f"   Away: {away_wins}-{len(away_games)-away_wins} ({away_wins/len(away_games):.1%})")
    if neutral_games:
        print(f"   Neutral: {neutral_wins}-{len(neutral_games)-neutral_wins} ({neutral_wins/len(neutral_games):.1%})")

    print(f"\n🔥 Close Games (≤7 points):")
    print(f"   Games: {len(close_games)}")
    if close_games:
        print(f"   Record: {close_wins}-{len(close_games)-close_wins} ({close_wins/len(close_games):.1%})")

def analyze_signature_wins(data):
    """Highlight the most significant victories"""
    print_section("SIGNATURE WINS")

    analytics = data.get('analytics', {})
    sig_wins = analytics.get('signature_wins', [])

    if not sig_wins:
        print("No signature wins data available")
        return

    print(f"\n🌟 Career-Defining Victories: {len(sig_wins)}\n")

    for i, win in enumerate(sig_wins[:15], 1):
        season = win.get('season', '?')
        week = win.get('week', '?')
        opponent = win.get('opponent', 'Unknown')
        points = win.get('points', 0)
        opp_points = win.get('opp_points', 0)
        context = win.get('context', '')
        impact = win.get('impact', '')

        print(f"   {i}. {season} Week {week}: vs {opponent}")
        print(f"      Score: {points}-{opp_points}")
        if context:
            print(f"      Context: {context}")
        if impact:
            print(f"      Impact: {impact}")
        print()

def analyze_season_progression(data):
    """Show year-by-year progression"""
    print_section("SEASON-BY-SEASON PROGRESSION")

    games = data.get('games', [])
    if not games:
        return

    # Group by season
    seasons = defaultdict(list)
    for game in games:
        if 'season' in game:
            seasons[game['season']].append(game)

    print(f"\n📅 Year-by-Year Results:\n")
    print(f"   {'Year':<8} {'Record':<12} {'Win%':<8} {'Pts/G':<8} {'Opp Pts/G':<10} {'Notable':<20}")
    print(f"   {'─'*70}")

    for year in sorted(seasons.keys()):
        year_games = seasons[year]
        wins = sum(1 for g in year_games if g.get('result') == 'W')
        losses = len(year_games) - wins

        total_pts = sum(g.get('points', 0) for g in year_games)
        total_opp_pts = sum(g.get('opp_points', 0) for g in year_games)

        ppg = total_pts / len(year_games) if year_games else 0
        opp_ppg = total_opp_pts / len(year_games) if year_games else 0
        win_pct = wins/(wins+losses) if (wins+losses) > 0 else 0

        # Find notable games
        bowl_games = [g for g in year_games if 'bowl' in g.get('notes', '').lower()]
        ranked_wins = sum(1 for g in year_games if g.get('result') == 'W' and g.get('opp_rank') and int(g.get('opp_rank', 999)) <= 25)

        notable = ""
        if bowl_games:
            notable = "Bowl Game"
        if ranked_wins:
            notable = f"{ranked_wins} Ranked Win(s)"

        print(f"   {year:<8} {wins:>2}-{losses:<2} ({len(year_games):>2}g)  {win_pct:>6.1%}   {ppg:>5.1f}    {opp_ppg:>5.1f}      {notable[:18]:<20}")

def analyze_talent_and_draft(data):
    """Analyze talent rankings and NFL draft success"""
    print_section("TALENT & NFL PIPELINE")

    talent = data.get('talent_ratings', [])
    draft = data.get('draft_picks', [])
    rankings = data.get('rankings', [])

    if talent:
        print(f"\n💎 Talent Composite Ratings (Recent):")
        # Sort by year and show last 5
        sorted_talent = sorted(talent, key=lambda x: x.get('year', 0))[-5:]
        for t in sorted_talent:
            year = t.get('year', '?')
            rating = t.get('talent', 0)
            school = t.get('school', '?')
            print(f"   {year} {school}: {rating:.2f}")

    if draft:
        total_picks = len(draft)
        print(f"\n🏈 NFL Draft Pipeline: {total_picks} players drafted")

        # Group by school
        by_school = defaultdict(list)
        for pick in draft:
            school = pick.get('school', 'Unknown')
            by_school[school].append(pick)

        for school, picks in by_school.items():
            print(f"\n   {school}: {len(picks)} players")
            for pick in picks[:5]:  # Show first 5
                name = pick.get('name', 'Unknown')
                year = pick.get('year', '?')
                round_num = pick.get('round', '?')
                team = pick.get('team', '?')
                print(f"      • {name} - {year} Round {round_num} ({team})")

    if rankings:
        print(f"\n📈 Team Rankings (Recent):")
        sorted_rankings = sorted(rankings, key=lambda x: (x.get('season', 0), x.get('week', 0)))[-5:]
        for r in sorted_rankings:
            season = r.get('season', '?')
            week = r.get('week', '?')
            rank = r.get('rank', '?')
            school = r.get('school', '?')
            poll = r.get('poll', 'Unknown')
            print(f"   {season} Week {week}: #{rank} {school} ({poll})")

def generate_ai_insights(data):
    """Generate AI-powered insights using Gemini"""
    print_section("🤖 AI-ENHANCED INSIGHTS (Powered by Gemini)")

    try:
        coach_name = get_coach_name(data)
        career = data.get('career_summary', {})
        stints = data.get('stints', [])
        sig_wins = data.get('analytics', {}).get('signature_wins', [])[:5]
        games = data.get('games', [])

        # Calculate some key stats for context
        total_games = len(games)
        wins = sum(1 for g in games if g.get('result') == 'W')
        ranked_wins = sum(1 for g in games if g.get('result') == 'W' and g.get('opp_rank') and int(g.get('opp_rank', 999)) <= 25)

        prompt = f"""Analyze this college football coach's career comprehensively and provide deep insights:

COACH: {coach_name}

CAREER STATS:
- Overall Record: {career.get('record', 'N/A')} ({career.get('win_pct', 0):.1f}% over {career.get('games', 0)} games)
- Schools: {', '.join([s.get('school', 'Unknown') for s in stints])}
- Wins vs Ranked Teams: {ranked_wins}

COACHING HISTORY:
{json.dumps([{
    'school': s.get('school'),
    'years': f"{s.get('start_year')}-{s.get('end_year', 'Present')}",
    'record': s.get('record'),
    'win_pct': f"{s.get('win_pct', 0):.1f}%"
} for s in stints], indent=2)}

TOP SIGNATURE WINS:
{json.dumps([{
    'season': w.get('season'),
    'opponent': w.get('opponent'),
    'context': w.get('context'),
    'impact': w.get('impact')
} for w in sig_wins], indent=2)}

Please provide:
1. A compelling narrative of this coach's career arc and trajectory
2. Deep analysis of their coaching philosophy, strengths, and tactical approach
3. Discussion of key turning points and program-defining moments
4. Comparison to peers and their standing in college football
5. Assessment of their legacy and historical impact
6. What makes them unique or distinctive as a coach
7. Future outlook and potential career trajectory

Be specific, insightful, and use the data provided. Write in an engaging, analytical style."""

        print("\n⏳ Generating AI analysis...\n")

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        print(response.text)

    except Exception as e:
        print(f"\n❌ Error generating AI insights: {e}")
        print("The standard analysis above provides comprehensive career details.")

def generate_final_summary(data):
    """Generate final summary"""
    print_header("REPORT COMPLETE", '=')

    coach_name = get_coach_name(data)
    career = data.get('career_summary', {})

    print(f"""
✅ Comprehensive analysis of {coach_name} completed successfully.

CAREER SNAPSHOT:
• Record: {career.get('record', 'N/A')} ({career.get('win_pct', 0):.1f}%)
• Games Coached: {career.get('games', 0)}
• Schools: {', '.join(data.get('metadata', {}).get('schools', []))}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

    print(f"{'═' * 80}\n")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Default to Matt Campbell
        filepath = "/Users/davlenswain/Desktop/Gameday_Graphql_Model/enhanced_coaches_v2/matt_campbell_master_v2.json"

    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        print("\nUsage: python coach_career_summary.py <path_to_coach_json>")
        print("\nExample: python coach_career_summary.py enhanced_coaches_v2/lane_kiffin_master.json")
        sys.exit(1)

    print(f"\n🔍 Loading coach data from: {os.path.basename(filepath)}\n")

    data = load_coach_data(filepath)

    # Run all analyses
    summarize_basic_info(data)
    analyze_stints(data)
    analyze_games(data)
    analyze_signature_wins(data)
    analyze_season_progression(data)
    analyze_talent_and_draft(data)
    generate_ai_insights(data)
    generate_final_summary(data)

if __name__ == "__main__":
    main()
