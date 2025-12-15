#!/usr/bin/env python3
"""
Universal Coach Career Summary Generator with AI Enhancement
Provides an in-depth analysis of any coach's career using Gemini AI
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
    if 'metadata' in data and 'coach_name' in data['metadata']:
        return data['metadata']['coach_name']
    elif 'career_summary' in data and 'coach' in data['career_summary']:
        return data['career_summary']['coach']
    return "Unknown Coach"

def summarize_metadata(data):
    """Summarize coach metadata"""
    coach_name = get_coach_name(data)
    print_header(f"{coach_name.upper()} - COMPREHENSIVE CAREER ANALYSIS")

    meta = data.get('metadata', {})
    print(f"Coach: {coach_name}")
    print(f"Current Position: {meta.get('current_team', 'N/A')}")
    print(f"Career Span: {meta.get('first_year', 'N/A')} - {meta.get('last_year', 'Present')}")
    print(f"Analysis Generated: {meta.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")

def summarize_career(data):
    """Summarize overall career statistics"""
    print_section("CAREER SUMMARY")

    career = data.get('career_summary', {})

    print(f"\n📊 Overall Record:")
    print(f"   Games Coached: {career.get('games_coached', 'N/A')}")
    print(f"   Record: {career.get('wins', 0)}-{career.get('losses', 0)} ({career.get('win_pct', 0):.1%})")
    print(f"   Conference Championships: {career.get('conference_championships', 0)}")
    print(f"   Bowl Appearances: {career.get('bowl_appearances', 0)}")
    print(f"   Bowl Record: {career.get('bowl_wins', 0)}-{career.get('bowl_losses', 0)}")

    print(f"\n🎯 Performance Metrics:")
    if 'avg_sp_plus' in career:
        print(f"   Average SP+ Ranking: {career['avg_sp_plus']}")
    if 'best_season_win_pct' in career:
        print(f"   Best Season Win%: {career['best_season_win_pct']:.1%}")
    if 'ats_wins' in career:
        print(f"   Career ATS Record: {career['ats_wins']}-{career['ats_losses']}-{career.get('ats_pushes', 0)}")
    if 'ats_win_pct' in career:
        print(f"   ATS Win%: {career['ats_win_pct']:.1%}")

def analyze_stints(data):
    """Analyze coaching stints at different schools"""
    print_section("COACHING STINTS")

    stints = data.get('stints', [])
    if not stints:
        print("No stint data available")
        return

    for stint in stints:
        print(f"\n{'═' * 60}")
        print(f"  {stint.get('school', 'Unknown')} ({stint.get('start_year', 'N/A')}-{stint.get('end_year', 'Present')})")
        print(f"{'═' * 60}")

        print(f"\n📈 Record & Performance:")
        print(f"   Overall: {stint.get('wins', 0)}-{stint.get('losses', 0)} ({stint.get('win_pct', 0):.1%})")
        print(f"   Conference: {stint.get('conf_wins', 0)}-{stint.get('conf_losses', 0)}")

        if 'seasons' in stint:
            print(f"   Seasons: {len(stint['seasons'])}")

        # Pre-arrival context
        if 'pre_arrival' in stint:
            pre = stint['pre_arrival']
            prev_pct = pre.get('prev_3yr_win_pct', 0)
            current_pct = stint.get('win_pct', 0)
            print(f"\n🔍 Pre-Arrival Context:")
            print(f"   Previous 3 Years: {pre.get('prev_3yr_wins', 0)}-{pre.get('prev_3yr_losses', 0)} ({prev_pct:.1%})")
            print(f"   Turnaround Impact: {(current_pct - prev_pct) * 100:+.1f}%")

        # Notable achievements
        if 'achievements' in stint and stint['achievements']:
            print(f"\n🏆 Achievements:")
            for achievement in stint['achievements'][:5]:
                print(f"   • {achievement}")

        # Signature wins
        if 'signature_wins' in stint and stint['signature_wins']:
            print(f"\n⭐ Signature Wins ({len(stint['signature_wins'])}):")
            for win in stint['signature_wins'][:3]:
                opp = win.get('opponent', 'Unknown')
                score = f"{win.get('points', 0)}-{win.get('opp_points', 0)}"
                context = win.get('context', '')
                print(f"   • vs {opp} ({score}) - {context}")

def analyze_games(data):
    """Analyze game-by-game performance"""
    print_section("GAME ANALYSIS")

    games = data.get('games', [])
    if not games:
        print("No game data available")
        return

    # Calculate statistics
    total_games = len(games)
    wins = sum(1 for g in games if g.get('result') == 'W')
    losses = total_games - wins

    # Analyze by opponent rank
    ranked_games = [g for g in games if g.get('opp_rank') and g.get('opp_rank') <= 25]
    ranked_wins = sum(1 for g in ranked_games if g.get('result') == 'W')

    # Home/Away splits
    home_games = [g for g in games if g.get('location') == 'H']
    away_games = [g for g in games if g.get('location') == 'A']
    neutral_games = [g for g in games if g.get('location') == 'N']

    home_wins = sum(1 for g in home_games if g.get('result') == 'W')
    away_wins = sum(1 for g in away_games if g.get('result') == 'W')
    neutral_wins = sum(1 for g in neutral_games if g.get('result') == 'W')

    print(f"\n📊 Game Breakdown:")
    print(f"   Total Games: {total_games}")
    print(f"   Overall Record: {wins}-{losses} ({wins/total_games:.1%})")

    print(f"\n🏅 vs Ranked Opponents:")
    print(f"   Games: {len(ranked_games)}")
    if ranked_games:
        print(f"   Record: {ranked_wins}-{len(ranked_games)-ranked_wins}")
        print(f"   Win%: {ranked_wins/len(ranked_games):.1%}")

    print(f"\n🏟️  Home/Away Splits:")
    if home_games:
        print(f"   Home: {home_wins}-{len(home_games)-home_wins} ({home_wins/len(home_games):.1%})")
    if away_games:
        print(f"   Away: {away_wins}-{len(away_games)-away_wins} ({away_wins/len(away_games):.1%})")
    if neutral_games:
        print(f"   Neutral: {neutral_wins}-{len(neutral_games)-neutral_wins} ({neutral_wins/len(neutral_games):.1%})")

    # Analyze scoring
    total_points = sum(g.get('points', 0) for g in games)
    total_opp_points = sum(g.get('opp_points', 0) for g in games)

    print(f"\n⚡ Scoring:")
    print(f"   Points/Game: {total_points/total_games:.1f}")
    print(f"   Opp Points/Game: {total_opp_points/total_games:.1f}")
    print(f"   Point Differential: {(total_points - total_opp_points)/total_games:+.1f}")

def analyze_analytics(data):
    """Analyze advanced analytics"""
    print_section("ADVANCED ANALYTICS")

    analytics = data.get('analytics', {})

    if 'signature_wins' in analytics and analytics['signature_wins']:
        print(f"\n🌟 Career-Defining Wins: {len(analytics['signature_wins'])}")
        for i, win in enumerate(analytics['signature_wins'][:10], 1):
            season = win.get('season', 'N/A')
            opponent = win.get('opponent', 'Unknown')
            score = f"{win.get('points', 0)}-{win.get('opp_points', 0)}"
            impact = win.get('impact', '')
            print(f"   {i}. {season} vs {opponent} ({score})")
            if impact:
                print(f"      Impact: {impact}")

    if 'turnaround_metrics' in analytics:
        print(f"\n📈 Program Turnaround Metrics:")
        tm = analytics['turnaround_metrics']
        for key, value in tm.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

    if 'recruiting_impact' in analytics:
        print(f"\n🎓 Recruiting Impact:")
        ri = analytics['recruiting_impact']
        for key, value in ri.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

def analyze_talent_roi(data):
    """Analyze talent ROI and recruiting"""
    print_section("TALENT & RECRUITING")

    talent = data.get('talent_ratings', {})

    if talent:
        print(f"\n💎 Talent Ratings:")
        for school, ratings in talent.items():
            print(f"\n   {school}:")
            if isinstance(ratings, dict):
                for year, rating in sorted(ratings.items())[-5:]:
                    print(f"      {year}: {rating}")

    draft = data.get('draft_picks', {})
    if draft:
        total_picks = sum(len(picks) if isinstance(picks, list) else 0 for picks in draft.values())
        print(f"\n🏈 NFL Draft Picks: {total_picks}")
        for school, picks in draft.items():
            if picks and isinstance(picks, list):
                print(f"\n   {school}: {len(picks)} players")
                for pick in picks[:3]:
                    name = pick.get('name', 'Unknown')
                    year = pick.get('year', 'N/A')
                    round_num = pick.get('round', 'N/A')
                    print(f"      • {name} ({year}, Round {round_num})")

def analyze_betting_performance(data):
    """Analyze ATS and betting performance"""
    print_section("BETTING & ATS PERFORMANCE")

    games = data.get('games', [])
    if not games:
        print("No game data available")
        return

    # Calculate ATS record
    ats_games = [g for g in games if 'spread' in g and g.get('spread') is not None]
    ats_wins = 0
    ats_losses = 0
    ats_pushes = 0

    for game in ats_games:
        if 'ats_result' in game:
            if game['ats_result'] == 'W':
                ats_wins += 1
            elif game['ats_result'] == 'L':
                ats_losses += 1
            elif game['ats_result'] == 'P':
                ats_pushes += 1

    if ats_games:
        print(f"\n📈 Against The Spread (ATS):")
        print(f"   Record: {ats_wins}-{ats_losses}-{ats_pushes}")
        if (ats_wins + ats_losses) > 0:
            ats_pct = ats_wins / (ats_wins + ats_losses)
            print(f"   Win%: {ats_pct:.1%}")

        # Analyze as favorite vs underdog
        fav_games = [g for g in ats_games if g.get('spread', 0) < 0]
        dog_games = [g for g in ats_games if g.get('spread', 0) > 0]

        fav_covers = sum(1 for g in fav_games if g.get('ats_result') == 'W')
        dog_covers = sum(1 for g in dog_games if g.get('ats_result') == 'W')

        if fav_games:
            print(f"\n   As Favorite: {fav_covers}/{len(fav_games)} covers ({fav_covers/len(fav_games):.1%})")
        if dog_games:
            print(f"   As Underdog: {dog_covers}/{len(dog_games)} covers ({dog_covers/len(dog_games):.1%})")

def analyze_season_progression(data):
    """Analyze year-over-year progression"""
    print_section("SEASON-BY-SEASON PROGRESSION")

    games = data.get('games', [])
    if not games:
        return

    # Group by season
    seasons = defaultdict(list)
    for game in games:
        if 'season' in game:
            seasons[game['season']].append(game)

    if not seasons:
        return

    print(f"\n📅 Year-by-Year Results:")
    print(f"\n   {'Year':<8} {'Record':<12} {'Pts/G':<8} {'Opp Pts/G':<12} {'Bowl':<20}")
    print(f"   {'-'*60}")

    for year in sorted(seasons.keys()):
        year_games = seasons[year]
        wins = sum(1 for g in year_games if g.get('result') == 'W')
        losses = len(year_games) - wins

        total_pts = sum(g.get('points', 0) for g in year_games)
        total_opp_pts = sum(g.get('opp_points', 0) for g in year_games)

        ppg = total_pts / len(year_games) if year_games else 0
        opp_ppg = total_opp_pts / len(year_games) if year_games else 0

        bowl = next((g.get('notes', '') for g in year_games if 'bowl' in g.get('notes', '').lower()), '')

        win_pct = wins/(wins+losses) if (wins+losses) > 0 else 0
        print(f"   {year:<8} {wins:>2}-{losses:<2} ({win_pct:.3f})  {ppg:>5.1f}    {opp_ppg:>5.1f}        {bowl[:18]:<20}")

def generate_ai_insights(data, coach_name):
    """Generate AI-powered insights using Gemini"""
    print_section("🤖 AI-ENHANCED INSIGHTS (Powered by Gemini)")

    try:
        # Prepare summary data for AI
        career = data.get('career_summary', {})
        stints = data.get('stints', [])
        analytics = data.get('analytics', {})

        summary_text = f"""
Analyze this college football coach's career and provide deep insights:

Coach: {coach_name}
Career Record: {career.get('wins', 0)}-{career.get('losses', 0)} ({career.get('win_pct', 0):.1%})
Schools Coached: {', '.join([s.get('school', 'Unknown') for s in stints])}
Conference Championships: {career.get('conference_championships', 0)}
Bowl Appearances: {career.get('bowl_appearances', 0)}

Key Career Highlights:
{json.dumps(analytics.get('signature_wins', [])[:5], indent=2)}

Coaching Stints:
{json.dumps([{
    'school': s.get('school'),
    'years': f"{s.get('start_year')}-{s.get('end_year', 'Present')}",
    'record': f"{s.get('wins', 0)}-{s.get('losses', 0)}",
    'win_pct': s.get('win_pct', 0)
} for s in stints], indent=2)}

Provide:
1. A compelling narrative of this coach's career trajectory
2. Analysis of their coaching philosophy and strengths
3. Key turning points or defining moments
4. Comparison to peers in college football
5. Future outlook and legacy assessment
6. What makes them unique as a coach
        """

        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=summary_text
        )

        print(f"\n{response.text}")

    except Exception as e:
        print(f"\n❌ Error generating AI insights: {e}")
        print("Continuing with standard analysis...")

def generate_summary(filepath):
    """Generate comprehensive summary"""
    data = load_coach_data(filepath)
    coach_name = get_coach_name(data)

    summarize_metadata(data)
    summarize_career(data)
    analyze_stints(data)
    analyze_games(data)
    analyze_analytics(data)
    analyze_talent_roi(data)
    analyze_betting_performance(data)
    analyze_season_progression(data)

    # AI-Enhanced Insights
    generate_ai_insights(data, coach_name)

    # Final assessment
    print_header("REPORT COMPLETE", '=')
    print(f"\nAnalysis of {coach_name} completed successfully.")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n{'═' * 80}\n")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Default to Matt Campbell
        filepath = "/Users/davlenswain/Desktop/Gameday_Graphql_Model/enhanced_coaches_v2/matt_campbell_master_v2.json"

    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        print("\nUsage: python universal_coach_summarizer.py <path_to_coach_json>")
        print("\nExample: python universal_coach_summarizer.py enhanced_coaches_v2/matt_campbell_master_v2.json")
        sys.exit(1)

    generate_summary(filepath)

if __name__ == "__main__":
    main()
