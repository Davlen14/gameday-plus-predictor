#!/usr/bin/env python3
"""
Generate FULL CAREER coach profiles including all schools they've coached at
"""
import json
import subprocess
import time
from pathlib import Path

def query_gql(query):
    """Execute GraphQL query"""
    cmd = [
        'curl', '-s',
        'https://api.collegefootballdata.com/graphql',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({'query': query})
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ GraphQL Error: {result.stderr}")
        return {}
    
    try:
        return json.loads(result.stdout).get('data', {})
    except:
        print(f"❌ Failed to parse response")
        return {}

def get_coach_full_career(coach_first, coach_last):
    """Get ALL schools a coach has been at"""
    print(f"\n🔍 Finding full career for {coach_first} {coach_last}...")
    
    # Query for coach records across all schools
    q = f'''{{
        coach(where: {{
            firstName: {{_eq: "{coach_first}"}},
            lastName: {{_eq: "{coach_last}"}}
        }}, orderBy: {{year: ASC}}) {{
            year
            firstName
            lastName
            school
        }}
    }}'''
    
    data = query_gql(q)
    records = data.get('coach', [])
    
    if not records:
        print(f"   ❌ No career data found")
        return []
    
    # Group by school
    schools = {}
    for rec in records:
        school = rec['school']
        year = rec['year']
        if school not in schools:
            schools[school] = {'start': year, 'end': year, 'years': []}
        schools[school]['years'].append(year)
        schools[school]['start'] = min(schools[school]['start'], year)
        schools[school]['end'] = max(schools[school]['end'], year)
    
    print(f"   ✅ Found {len(schools)} schools:")
    for school, info in schools.items():
        print(f"      - {school}: {info['start']}-{info['end']} ({len(info['years'])} seasons)")
    
    return schools, records

def fetch_games_for_school(school, start_year, end_year):
    """Fetch all games for a school in date range"""
    print(f"   📅 Fetching {school} games ({start_year}-{end_year})...")
    
    all_games = []
    
    for year in range(start_year, end_year + 1):
        q = f'''{{
            game(where: {{
                season: {{_eq: {year}}},
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
        
        data = query_gql(q)
        games = data.get('game', [])
        all_games.extend(games)
        
        if games:
            print(f"      {year}: {len(games)} games")
        
        time.sleep(0.1)  # Rate limiting
    
    return all_games

def generate_full_career_profile(coach_first, coach_last, current_school):
    """Generate complete career profile"""
    print(f"\n{'='*60}")
    print(f"🏈 Generating FULL CAREER for {coach_first} {coach_last}")
    print(f"{'='*60}")
    
    # Get full career
    schools_data, coaching_records = get_coach_full_career(coach_first, coach_last)
    
    if not schools_data:
        return None
    
    # Fetch games from ALL schools
    all_games = []
    total_wins = 0
    total_losses = 0
    
    for school, info in schools_data.items():
        games = fetch_games_for_school(school, info['start'], info['end'])
        all_games.extend(games)
        
        # Calculate record at this school
        wins = 0
        losses = 0
        for game in games:
            if game['homeTeam'] == school:
                if game['homePoints'] > game['awayPoints']:
                    wins += 1
                else:
                    losses += 1
            elif game['awayTeam'] == school:
                if game['awayPoints'] > game['homePoints']:
                    wins += 1
                else:
                    losses += 1
        
        total_wins += wins
        total_losses += losses
        print(f"   📊 {school}: {wins}-{losses}")
    
    # Create comprehensive profile
    profile = {
        'metadata': {
            'generated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'coach': f"{coach_first} {coach_last}",
            'current_school': current_school,
            'career': 'full',
            'description': f'Complete career profile including all schools'
        },
        'summary': {
            'career_overview': {
                'coach': f"{coach_first} {coach_last}",
                'total_record': f"{total_wins}-{total_losses}",
                'win_pct': round(total_wins / (total_wins + total_losses) * 100, 1) if (total_wins + total_losses) > 0 else 0,
                'total_games': len(all_games),
                'schools': len(schools_data),
                'years': len(coaching_records)
            },
            'schools': [
                {
                    'school': school,
                    'start_year': info['start'],
                    'end_year': info['end'],
                    'seasons': len(info['years'])
                }
                for school, info in schools_data.items()
            ],
            'coaching_records': coaching_records
        },
        'games': all_games
    }
    
    # Save file
    output_dir = Path('enhanced_coaches')
    output_dir.mkdir(exist_ok=True)
    
    last_name = coach_last.lower().replace("'", "")
    school_slug = current_school.lower().replace(' ', '_').replace("'", "")
    filename = f"{last_name}_{school_slug}_FULL.json"
    output_file = output_dir / filename
    
    with open(output_file, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"\n✅ Saved: {output_file}")
    print(f"   Career: {total_wins}-{total_losses} ({profile['summary']['career_overview']['win_pct']}%)")
    print(f"   Schools: {len(schools_data)}")
    print(f"   Games: {len(all_games)}")
    
    return profile

def main():
    """Generate full career profiles for key coaches"""
    
    coaches_to_update = [
        ('Brian', 'Kelly', 'LSU'),  # Notre Dame + LSU
        ('Lane', 'Kiffin', 'Ole Miss'),  # Tennessee + USC + FAU + Ole Miss
        ('Lincoln', 'Riley', 'USC'),  # Oklahoma + USC
        ('Matt', 'Rhule', 'Nebraska'),  # Temple + Baylor + Nebraska
        ('Jimbo', 'Fisher', 'Texas A&M'),  # FSU + Texas A&M
        ('Dabo', 'Swinney', 'Clemson'),  # Full career at Clemson
        ('Kirby', 'Smart', 'Georgia'),  # Full career at Georgia
        ('Ryan', 'Day', 'Ohio State'),  # Full career at Ohio State
    ]
    
    print("="*60)
    print("🏈 FULL CAREER COACH PROFILE GENERATOR")
    print("="*60)
    print(f"Will generate profiles for {len(coaches_to_update)} coaches")
    print("This will fetch data from ALL schools they've coached at")
    print("="*60)
    
    for coach_first, coach_last, current_school in coaches_to_update:
        try:
            generate_full_career_profile(coach_first, coach_last, current_school)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"❌ Error processing {coach_first} {coach_last}: {e}")
            continue
    
    print("\n" + "="*60)
    print("✅ COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    main()
