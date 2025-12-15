#!/usr/bin/env python3
"""
Generate FULL career timelines for coaches who have been at multiple schools.
Uses universal_coach_analyzer.py pattern to query by school, then merges data.
"""
import json
import subprocess
import os
from pathlib import Path

def load_fbs_teams():
    """Load FBS team data for colors and logos"""
    with open('fbs.json', 'r') as f:
        return {team['school']: team for team in json.load(f)}

def load_coach_headshots():
    """Load coach headshots"""
    with open('power5_coaches_headshots.json', 'r') as f:
        data = json.load(f)
        return {coach['name']: coach.get('headshot', '') for coach in data.get('coaches', [])}

def load_career_mappings():
    """Load coach career school mappings"""
    with open('coach_career_schools.json', 'r') as f:
        return json.load(f)['coaches']

def check_enhanced_file_exists(coach_name, school):
    """Check if enhanced coach file exists for a school"""
    # Normalize filename
    last_name = coach_name.split()[-1].lower()
    school_name = school.lower().replace(' ', '_').replace('ole_miss', 'ole_miss').replace('ohio_state', 'ohio_state')
    
    # Common patterns
    patterns = [
        f"enhanced_coaches/{last_name}_{school_name}.json",
        f"enhanced_coaches/{last_name}_{school.lower().replace(' ', '')}.json",
    ]
    
    for pattern in patterns:
        if os.path.exists(pattern):
            return pattern
    return None

def generate_school_data(coach_name, school, start_year, end_year):
    """Generate data for one school using universal_coach_analyzer.py"""
    print(f"\n🏫 Generating data for {coach_name} at {school} ({start_year}-{end_year})...")
    
    # Check if file already exists
    existing = check_enhanced_file_exists(coach_name, school)
    if existing:
        print(f"   ✓ Found existing file: {existing}")
        with open(existing, 'r') as f:
            return json.load(f)
    
    # Need to generate - use universal_coach_analyzer.py
    print(f"   ⚙️  Need to generate new file for {school}...")
    coach_first = coach_name.split()[0]
    coach_last = coach_name.split()[-1]
    
    try:
        result = subprocess.run(
            ['python3', 'universal_coach_analyzer.py', coach_first, coach_last, school],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"   ✓ Generated successfully")
            # Try to find the generated file
            generated = check_enhanced_file_exists(coach_name, school)
            if generated:
                with open(generated, 'r') as f:
                    return json.load(f)
        else:
            print(f"   ❌ Generation failed: {result.stderr[:200]}")
    except Exception as e:
        print(f"   ❌ Error generating: {e}")
    
    return None

def merge_career_data(coach_name, career_schools, teams_data, headshots):
    """Merge data from multiple schools into one career timeline"""
    print(f"\n📊 Merging career data for {coach_name}...")
    
    all_games = []
    all_rankings = []
    career_record = {"wins": 0, "losses": 0}
    career_summary = []
    
    for school_info in career_schools:
        school = school_info['school']
        start_year = school_info['start_year']
        end_year = school_info['end_year']
        
        # Get school data
        school_data = generate_school_data(coach_name, school, start_year, end_year)
        
        if not school_data:
            print(f"   ⚠️  No data for {school}, skipping...")
            continue
        
        # Extract games
        games = school_data.get('games', [])
        
        # Add school info to each game
        for game in games:
            game['coaching_school'] = school
            game['school_tenure'] = f"{start_year}-{end_year}"
        
        all_games.extend(games)
        
        # Extract rankings
        rankings = school_data.get('rankings', [])
        all_rankings.extend(rankings)
        
        # Update career record
        summary = school_data.get('summary', {})
        wins = summary.get('overall_record', {}).get('wins', 0)
        losses = summary.get('overall_record', {}).get('losses', 0)
        career_record['wins'] += wins
        career_record['losses'] += losses
        
        # Add to career summary
        team_data = teams_data.get(school, {})
        career_summary.append({
            'school': school,
            'years': f"{start_year}-{end_year}",
            'record': f"{wins}-{losses}",
            'win_pct': wins / (wins + losses) if (wins + losses) > 0 else 0,
            'teamColor': team_data.get('color', '#000000'),
            'teamLogo': team_data.get('logo', ''),
            'conference': team_data.get('conference', 'Unknown')
        })
        
        print(f"   ✓ {school}: {wins}-{losses} ({len(games)} games)")
    
    # Sort all games chronologically
    all_games.sort(key=lambda g: (g.get('season', 0), g.get('week', 0)))
    all_rankings.sort(key=lambda r: (r.get('poll', {}).get('season', 0), r.get('poll', {}).get('week', 0)))
    
    total_games = career_record['wins'] + career_record['losses']
    win_pct = career_record['wins'] / total_games if total_games > 0 else 0
    
    print(f"\n   📈 Career Total: {career_record['wins']}-{career_record['losses']} ({win_pct:.1%})")
    
    # Build timeline data for Highcharts
    timeline_data = []
    for ranking in all_rankings:
        poll = ranking.get('poll', {})
        season = poll.get('season')
        week = poll.get('week')
        rank = ranking.get('rank')
        
        if season and week and rank:
            # Create timestamp (approximate - use week as day of year estimate)
            timestamp = (season - 1970) * 365.25 * 24 * 60 * 60 * 1000 + (week * 7 * 24 * 60 * 60 * 1000)
            timeline_data.append([int(timestamp), rank])
    
    # Get current team info
    current_school = career_schools[-1]['school']
    current_team_data = teams_data.get(current_school, {})
    
    return {
        'coach': coach_name,
        'school': f"{len(career_schools)} Schools",
        'career_schools': career_summary,
        'teamColor': current_team_data.get('color', '#000000'),
        'teamLogo': current_team_data.get('logo', ''),
        'coachHeadshot': headshots.get(coach_name, ''),
        'data': timeline_data,
        'metadata': {
            'record': f"{career_record['wins']}-{career_record['losses']}",
            'win_pct': round(win_pct * 100, 1),
            'total_games': len(all_games),
            'total_rankings': len(all_rankings),
            'career_timeline': [f"{s['school']} ({s['years']}): {s['record']}" for s in career_summary]
        }
    }

def main():
    print("🏈 Generating Multi-School Career Timelines\n")
    
    # Load data
    teams_data = load_fbs_teams()
    headshots = load_coach_headshots()
    coaches = load_career_mappings()
    
    # Filter to coaches with multiple schools
    multi_school_coaches = [c for c in coaches if len(c['career']) > 1]
    
    print(f"📋 Found {len(multi_school_coaches)} coaches with multiple FBS schools:\n")
    for coach in multi_school_coaches:
        schools = [s['school'] for s in coach['career']]
        print(f"   • {coach['name']}: {' → '.join(schools)}")
    
    # Generate timelines
    output_dir = Path('frontend/src/data/coach_timelines')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for coach_info in multi_school_coaches:
        try:
            timeline = merge_career_data(
                coach_info['name'],
                coach_info['career'],
                teams_data,
                headshots
            )
            
            # Save timeline
            coach_last = coach_info['name'].split()[-1].lower()
            current_school = coach_info['current_team'].lower().replace(' ', '_')
            filename = f"{coach_last}_{current_school}_FULL_timeline.json"
            
            output_path = output_dir / filename
            with open(output_path, 'w') as f:
                json.dump(timeline, f, indent=2)
            
            print(f"\n✅ Saved: {output_path}\n")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ Error processing {coach_info['name']}: {e}\n")
            continue
    
    print(f"\n🎉 Complete! Generated {len(multi_school_coaches)} full career timelines")

if __name__ == '__main__':
    main()
