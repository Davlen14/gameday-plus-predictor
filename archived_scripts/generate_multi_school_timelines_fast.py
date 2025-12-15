#!/usr/bin/env python3
"""
Generate FULL career timelines - FAST VERSION using direct GraphQL queries
"""
import json
import requests
from pathlib import Path
from collections import defaultdict

GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

def query_gql(q):
    """Execute GraphQL query"""
    try:
        r = requests.post(
            GRAPHQL_URL,
            json={'query': q},
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        return r.json().get('data', {})
    except Exception as e:
        print(f"❌ Query error: {e}")
        return {}

def load_fbs_teams():
    """Load FBS team data"""
    with open('fbs.json', 'r') as f:
        return {team['school']: team for team in json.load(f)}

def load_coach_headshots():
    """Load coach headshots"""
    with open('power5_coaches_headshots.json', 'r') as f:
        data = json.load(f)
        headshots = {}
        # Iterate through all conferences
        for conference, coaches in data.items():
            for coach in coaches:
                coach_name = coach.get('coach', '')
                headshot_url = coach.get('headshot_url', '')
                if coach_name:
                    headshots[coach_name] = headshot_url
        return headshots

def load_career_mappings():
    """Load coach career mappings"""
    with open('coach_career_schools.json', 'r') as f:
        return json.load(f)['coaches']

def build_games_query(career_schools):
    """Build GraphQL query for all schools at once"""
    or_conditions = []
    
    for school_info in career_schools:
        school = school_info['school']
        start = school_info['start_year']
        end = school_info['end_year']
        
        # Home games
        or_conditions.append(
            f'{{homeTeam: {{_eq: "{school}"}}, season: {{_gte: {start}, _lte: {end}}}}}'
        )
        # Away games
        or_conditions.append(
            f'{{awayTeam: {{_eq: "{school}"}}, season: {{_gte: {start}, _lte: {end}}}}}'
        )
    
    or_clause = ', '.join(or_conditions)
    
    return f'''{{
        game(where: {{_or: [{or_clause}]}}, orderBy: {{season: ASC, week: ASC}}) {{
            season
            week
            seasonType
            homeTeam
            awayTeam
            homePoints
            awayPoints
            conferenceGame
            neutralSite
        }}
    }}'''

def build_rankings_query(career_schools):
    """Build GraphQL query for rankings across all schools"""
    or_conditions = []
    
    for school_info in career_schools:
        school = school_info['school']
        start = school_info['start_year']
        end = school_info['end_year']
        
        or_conditions.append(
            f'{{team: {{school: {{_eq: "{school}"}}}}, poll: {{season: {{_gte: {start}, _lte: {end}}}}}}}'
        )
    
    or_clause = ', '.join(or_conditions)
    
    return f'''{{
        pollRank(where: {{
            poll: {{pollType: {{name: {{_eq: "AP Top 25"}}}}}},
            _or: [{or_clause}]
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

def calculate_record(games, school):
    """Calculate W-L record for a specific school"""
    wins = 0
    losses = 0
    
    for game in games:
        is_home = game['homeTeam'] == school
        is_away = game['awayTeam'] == school
        
        if not (is_home or is_away):
            continue
        
        home_pts = game.get('homePoints', 0) or 0
        away_pts = game.get('awayPoints', 0) or 0
        
        if is_home:
            if home_pts > away_pts:
                wins += 1
            elif home_pts < away_pts:
                losses += 1
        else:  # is_away
            if away_pts > home_pts:
                wins += 1
            elif away_pts < home_pts:
                losses += 1
    
    return wins, losses

def load_enhanced_coach_data(coach_name, current_school):
    """Load enhanced coach data for draft picks"""
    coach_last = coach_name.split()[-1].lower()
    school_slug = current_school.lower().replace(' ', '_')
    enhanced_path = Path(f'enhanced_coaches/{coach_last}_{school_slug}.json')
    
    if enhanced_path.exists():
        with open(enhanced_path, 'r') as f:
            return json.load(f)
    return None

def generate_full_career_timeline(coach_name, career_schools, teams_data, headshots):
    """Generate complete career timeline with one GraphQL query"""
    print(f"\n📊 {coach_name}")
    print(f"   Schools: {' → '.join([s['school'] for s in career_schools])}")
    
    # Query all games at once
    print(f"   🔍 Fetching games...")
    games_query = build_games_query(career_schools)
    games_data = query_gql(games_query)
    all_games = games_data.get('game', [])
    print(f"   ✓ {len(all_games)} games")
    
    # Query all rankings at once
    print(f"   📊 Fetching rankings...")
    rankings_query = build_rankings_query(career_schools)
    rankings_data = query_gql(rankings_query)
    all_rankings = rankings_data.get('pollRank', [])
    print(f"   ✓ {len(all_rankings)} ranked weeks")
    
    # Calculate records by school
    career_summary = []
    total_wins = 0
    total_losses = 0
    
    for school_info in career_schools:
        school = school_info['school']
        wins, losses = calculate_record(all_games, school)
        total_wins += wins
        total_losses += losses
        
        team_data = teams_data.get(school, {})
        win_pct = wins / (wins + losses) if (wins + losses) > 0 else 0
        
        career_summary.append({
            'school': school,
            'years': f"{school_info['start_year']}-{school_info['end_year']}",
            'record': f"{wins}-{losses}",
            'win_pct': round(win_pct * 100, 1),
            'teamColor': team_data.get('primary_color', '#000000'),
            'teamLogo': team_data.get('logos', [''])[0] if team_data.get('logos') else '',
            'conference': team_data.get('conference', 'Unknown')
        })
        
        print(f"   • {school}: {wins}-{losses} ({win_pct:.1%})")
    
    # Build timeline data
    timeline_data = []
    for ranking in all_rankings:
        poll = ranking.get('poll', {})
        season = poll.get('season')
        week = poll.get('week')
        rank = ranking.get('rank')
        
        if season and week and rank:
            # Create timestamp
            timestamp = (season - 1970) * 365.25 * 24 * 60 * 60 * 1000 + (week * 7 * 24 * 60 * 60 * 1000)
            timeline_data.append([int(timestamp), rank])
    
    # Get current school info
    current_school = career_schools[-1]['school']
    current_team_data = teams_data.get(current_school, {})
    
    total_games = total_wins + total_losses
    career_win_pct = total_wins / total_games if total_games > 0 else 0
    
    print(f"   📈 Career: {total_wins}-{total_losses} ({career_win_pct:.1%})")
    
    # Calculate peak talent year and draft picks from enhanced data
    talent_by_year = defaultdict(lambda: {'talent': 0, 'count': 0})
    draft_by_year = defaultdict(lambda: {'total': 0, 'round1': 0})
    
    # Load enhanced coach data for draft picks
    current_school = career_schools[-1]['school']
    enhanced_data = load_enhanced_coach_data(coach_name, current_school)
    
    if enhanced_data and 'draft_picks' in enhanced_data:
        draft_picks = enhanced_data['draft_picks']
        print(f"   🏈 Processing {len(draft_picks)} draft picks...")
        
        for pick in draft_picks:
            year = pick.get('year')
            if year:
                draft_by_year[year]['total'] += 1
                if pick.get('round') == 1:
                    draft_by_year[year]['round1'] += 1
                
                # Estimate talent rating (draft position affects talent)
                overall = pick.get('overall', 100)
                talent_score = max(0, 100 - overall)  # Higher pick = higher talent
                talent_by_year[year]['talent'] += talent_score
                talent_by_year[year]['count'] += 1
    else:
        print(f"   ⚠️  No enhanced data found")
    
    print(f"   ✓ {sum(y['total'] for y in draft_by_year.values())} draft picks processed")
    
    # Find peak talent year
    peak_talent = {'year': None, 'talent': 0}
    for year, data in talent_by_year.items():
        avg_talent = data['talent'] / data['count'] if data['count'] > 0 else 0
        if avg_talent > peak_talent['talent']:
            peak_talent = {'year': year, 'talent': round(avg_talent, 1)}
    
    # Find top draft years
    top_draft_years = sorted(
        draft_by_year.items(), 
        key=lambda x: (x[1]['total'], x[1]['round1']), 
        reverse=True
    )[:3]
    
    # Count #1 rankings
    top_rankings_count = sum(1 for r in all_rankings if r.get('rank') == 1)
    
    return {
        'coach': coach_name,
        'school': f"{len(career_schools)} Schools",
        'career_schools': career_summary,
        'teamColor': current_team_data.get('primary_color', '#000000'),
        'teamLogo': current_team_data.get('logos', [''])[0] if current_team_data.get('logos') else '',
        'coachHeadshot': headshots.get(coach_name, ''),
        'data': timeline_data,
        'metadata': {
            'record': f"{total_wins}-{total_losses}",
            'win_pct': round(career_win_pct * 100, 1),
            'total_games': len(all_games),
            'total_rankings': len(all_rankings),
            'schools_coached': len(career_schools),
            'career_timeline': [f"{s['school']} ({s['years']}): {s['record']}" for s in career_summary],
            'peak_talent': peak_talent if peak_talent['year'] else None,
            'top_rankings_count': top_rankings_count,
            'top_draft_years': [
                {
                    'year': year,
                    'total': info['total'],
                    'round1': info['round1']
                }
                for year, info in top_draft_years
            ] if draft_by_year else []
        }
    }

def main():
    print("🏈 FAST Multi-School Career Timeline Generator\n")
    
    teams_data = load_fbs_teams()
    headshots = load_coach_headshots()
    coaches = load_career_mappings()
    
    # Filter to coaches with multiple FBS schools
    multi_school_coaches = [c for c in coaches if len(c['career']) > 1]
    
    print(f"📋 Generating timelines for {len(multi_school_coaches)} coaches")
    print("=" * 80)
    
    output_dir = Path('frontend/src/data/coach_timelines')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for coach_info in multi_school_coaches:
        try:
            timeline = generate_full_career_timeline(
                coach_info['name'],
                coach_info['career'],
                teams_data,
                headshots
            )
            
            # Save
            coach_last = coach_info['name'].split()[-1].lower()
            current_school = coach_info['current_team'].lower().replace(' ', '_')
            filename = f"{coach_last}_{current_school}_FULL_timeline.json"
            
            output_path = output_dir / filename
            with open(output_path, 'w') as f:
                json.dump(timeline, f, indent=2)
            
            print(f"   ✅ Saved: {filename}\n")
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            continue
    
    print("=" * 80)
    print(f"🎉 Complete!")

if __name__ == '__main__':
    main()
