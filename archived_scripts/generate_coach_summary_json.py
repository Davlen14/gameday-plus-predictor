#!/usr/bin/env python3
"""
Generate Coach Career Summary as JSON for React Components
Outputs comprehensive analysis in JSON format
"""

import json
import sys
import os
from datetime import datetime
from google import genai
from collections import defaultdict

# Configure Gemini
GEMINI_API_KEY = "AIzaSyAXjMNN_vK2BpO4VQehdkCnivCAiat8lso"
client = genai.Client(api_key=GEMINI_API_KEY)

def load_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def get_game_result(game, school):
    """Determine if this was a win/loss and the score"""
    is_home = school.lower() in game.get('homeTeam', '').lower()

    if is_home:
        team_pts = game.get('homePoints', 0)
        opp_pts = game.get('awayPoints', 0)
        opponent = game.get('awayTeam', 'Unknown')
    else:
        team_pts = game.get('awayPoints', 0)
        opp_pts = game.get('homePoints', 0)
        opponent = game.get('homeTeam', 'Unknown')

    won = team_pts > opp_pts
    return won, team_pts, opp_pts, opponent, is_home

def generate_ai_summary(coach_name, summary_data):
    """Generate AI narrative summary"""
    try:
        prompt = f"""Provide a compelling 2-3 paragraph narrative summary of {coach_name}'s coaching career.

CAREER DATA:
- Record: {summary_data['career_stats']['record']}
- Win%: {summary_data['career_stats']['win_pct']:.1f}%
- Schools: {', '.join([s['school'] for s in summary_data['stints']])}
- Signature Wins: {len(summary_data.get('signature_wins', []))}
- NFL Draft Picks: {summary_data.get('nfl_draft_picks', 0)}

Write a compelling narrative that:
1. Summarizes their career trajectory and evolution
2. Highlights key achievements and defining moments
3. Discusses their coaching philosophy and impact
4. Provides context on their legacy

Keep it engaging and suitable for a sports analytics dashboard."""

        response = client.models.generate_content(
            model='gemini-2.0-flash-thinking-exp-1219',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Career summary for {coach_name}: {summary_data['career_stats']['wins']}-{summary_data['career_stats']['losses']} record across {summary_data['career_stats']['total_games']} games. Known for program building and player development."

def analyze_coach_to_json(filepath):
    """Analyze coach and return JSON structure"""
    data = load_data(filepath)

    # Extract basic info
    meta = data.get('metadata', {})
    career = data.get('career_summary', {})
    coach_name = meta.get('coach', 'Unknown Coach')

    # Initialize summary structure
    summary = {
        'coach_name': coach_name,
        'headshot': meta.get('headshot', ''),
        'schools': meta.get('schools', []),
        'generated': datetime.now().isoformat(),
        'career_stats': {},
        'stints': [],
        'game_analysis': {},
        'signature_wins': [],
        'season_progression': [],
        'nfl_pipeline': {},
        'talent_ratings': [],
        'ai_narrative': ''
    }

    # Career stats
    games = data.get('games', [])
    stints = data.get('stints', [])

    total_team_pts = 0
    total_opp_pts = 0
    wins = 0
    home_wins = 0
    away_wins = 0
    neutral_wins = 0
    home_games = 0
    away_games = 0
    neutral_games = 0
    close_wins = 0
    close_losses = 0

    for game in games:
        school = game.get('school', stints[0].get('school', 'Unknown') if stints else 'Unknown')
        won, team_pts, opp_pts, opponent, is_home = get_game_result(game, school)

        total_team_pts += team_pts
        total_opp_pts += opp_pts

        if won:
            wins += 1

        # Location stats
        is_neutral = game.get('neutralSite', False)
        if is_neutral:
            neutral_games += 1
            if won:
                neutral_wins += 1
        elif is_home:
            home_games += 1
            if won:
                home_wins += 1
        else:
            away_games += 1
            if won:
                away_wins += 1

        # Close games
        if abs(team_pts - opp_pts) <= 7:
            if won:
                close_wins += 1
            else:
                close_losses += 1

    total_games = len(games)
    losses = total_games - wins

    summary['career_stats'] = {
        'record': f"{wins}-{losses}",
        'wins': wins,
        'losses': losses,
        'total_games': total_games,
        'win_pct': (wins / total_games * 100) if total_games > 0 else 0,
        'points_per_game': round(total_team_pts / total_games, 1) if total_games > 0 else 0,
        'opp_points_per_game': round(total_opp_pts / total_games, 1) if total_games > 0 else 0,
        'point_differential': round((total_team_pts - total_opp_pts) / total_games, 1) if total_games > 0 else 0
    }

    # Stints
    for stint in stints:
        summary['stints'].append({
            'school': stint.get('school', 'Unknown'),
            'start_year': stint.get('start_year'),
            'end_year': stint.get('end_year', 'Present'),
            'record': stint.get('record', 'N/A'),
            'wins': stint.get('wins', 0),
            'losses': stint.get('losses', 0),
            'win_pct': stint.get('win_pct', 0),
            'games': stint.get('games', 0)
        })

    # Game analysis
    summary['game_analysis'] = {
        'home': {
            'games': home_games,
            'wins': home_wins,
            'losses': home_games - home_wins,
            'win_pct': round(home_wins / home_games * 100, 1) if home_games > 0 else 0
        },
        'away': {
            'games': away_games,
            'wins': away_wins,
            'losses': away_games - away_wins,
            'win_pct': round(away_wins / away_games * 100, 1) if away_games > 0 else 0
        },
        'neutral': {
            'games': neutral_games,
            'wins': neutral_wins,
            'losses': neutral_games - neutral_wins,
            'win_pct': round(neutral_wins / neutral_games * 100, 1) if neutral_games > 0 else 0
        },
        'close_games': {
            'total': close_wins + close_losses,
            'wins': close_wins,
            'losses': close_losses,
            'win_pct': round(close_wins / (close_wins + close_losses) * 100, 1) if (close_wins + close_losses) > 0 else 0
        }
    }

    # Signature wins
    analytics = data.get('analytics', {})
    sig_wins = analytics.get('signature_wins', [])

    for win in sig_wins:
        summary['signature_wins'].append({
            'season': win.get('season'),
            'week': win.get('week'),
            'opponent': win.get('opponent'),
            'context': win.get('context', ''),
            'impact': win.get('impact', '')
        })

    # Season progression
    seasons = defaultdict(list)
    for game in games:
        seasons[game['season']].append(game)

    for year in sorted(seasons.keys()):
        year_games = seasons[year]
        year_wins = 0
        year_pts = 0
        year_opp_pts = 0

        for game in year_games:
            school = game.get('school', stints[0].get('school', 'Unknown') if stints else 'Unknown')
            won, team_pts, opp_pts, _, _ = get_game_result(game, school)
            if won:
                year_wins += 1
            year_pts += team_pts
            year_opp_pts += opp_pts

        year_losses = len(year_games) - year_wins

        summary['season_progression'].append({
            'year': year,
            'games': len(year_games),
            'wins': year_wins,
            'losses': year_losses,
            'win_pct': round(year_wins / len(year_games) * 100, 1) if year_games else 0,
            'points_per_game': round(year_pts / len(year_games), 1) if year_games else 0,
            'opp_points_per_game': round(year_opp_pts / len(year_games), 1) if year_games else 0
        })

    # NFL Pipeline
    draft_picks = data.get('draft_picks', [])
    summary['nfl_pipeline'] = {
        'total_picks': len(draft_picks),
        'players': []
    }

    for pick in draft_picks[:15]:  # Top 15
        summary['nfl_pipeline']['players'].append({
            'name': pick.get('name', 'Unknown'),
            'year': pick.get('year'),
            'round': pick.get('round'),
            'pick': pick.get('pick'),
            'team': pick.get('team', 'Unknown')
        })

    summary['nfl_draft_picks'] = len(draft_picks)

    # Talent ratings
    talent = data.get('talent_ratings', [])
    sorted_talent = sorted(talent, key=lambda x: x.get('year', 0))[-5:]

    for t in sorted_talent:
        summary['talent_ratings'].append({
            'year': t.get('year'),
            'school': t.get('school'),
            'rating': round(t.get('talent', 0), 2)
        })

    # Generate AI narrative
    print(f"🤖 Generating AI narrative for {coach_name}...", file=sys.stderr)
    summary['ai_narrative'] = generate_ai_summary(coach_name, summary)

    return summary

def main():
    if len(sys.argv) < 2:
        print("❌ Error: No coach file specified", file=sys.stderr)
        print("\nUsage: python generate_coach_summary_json.py <path_to_coach_json> [output_file]", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python generate_coach_summary_json.py enhanced_coaches_v2/matt_campbell_master_v2.json", file=sys.stderr)
        print("  python generate_coach_summary_json.py enhanced_coaches_v2/matt_campbell_master_v2.json matt_campbell_summary.json", file=sys.stderr)
        sys.exit(1)

    input_filepath = sys.argv[1]

    if not os.path.exists(input_filepath):
        print(f"❌ Error: File not found: {input_filepath}", file=sys.stderr)
        sys.exit(1)

    # Determine output file
    if len(sys.argv) >= 3:
        output_filepath = sys.argv[2]
    else:
        # Auto-generate output filename
        coach_file = os.path.basename(input_filepath)
        coach_name = coach_file.replace('_master_v2.json', '').replace('_master.json', '')
        output_filepath = f"{coach_name}_summary.json"

    print(f"🔍 Analyzing: {os.path.basename(input_filepath)}", file=sys.stderr)

    # Generate summary
    summary = analyze_coach_to_json(input_filepath)

    # Write to file
    with open(output_filepath, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Summary generated: {output_filepath}", file=sys.stderr)
    print(f"📊 Coach: {summary['coach_name']}", file=sys.stderr)
    print(f"📈 Record: {summary['career_stats']['record']} ({summary['career_stats']['win_pct']:.1f}%)", file=sys.stderr)
    print(f"🏈 NFL Picks: {summary['nfl_draft_picks']}", file=sys.stderr)
    print(f"\n✨ Ready to import into React components!", file=sys.stderr)

if __name__ == "__main__":
    main()
