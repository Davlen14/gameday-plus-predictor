#!/usr/bin/env python3
"""
Generate timeline data for coaches from their enhanced JSON files
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Load FBS team data for colors and logos
def load_fbs_teams():
    """Load FBS team data with colors and logos"""
    fbs_path = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/fbs.json')
    with open(fbs_path) as f:
        return {team['school']: team for team in json.load(f)}

def load_coach_headshots():
    """Load coach headshot URLs"""
    headshots_path = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/data/power5_coaches_headshots.json')
    with open(headshots_path) as f:
        data = json.load(f)
        # Flatten all conferences into single dict
        headshots = {}
        for conference in ['big12', 'big10', 'sec', 'acc']:
            for coach in data.get(conference, []):
                key = f"{coach['coach']}_{coach['school']}"
                headshots[key] = coach.get('headshot_url', '')
        return headshots

def generate_timeline_data(coach_file_path, fbs_teams, coach_headshots):
    """Generate Highcharts-compatible timeline data from coach JSON"""
    with open(coach_file_path) as f:
        data = json.load(f)
    
    coach_name = data['metadata']['coach']
    school = data['metadata']['school']
    
    # Get team info from FBS data
    team_info = fbs_teams.get(school, {})
    team_color = team_info.get('primary_color', '#6b7280')
    team_logo = team_info.get('logos', [''])[0] if team_info.get('logos') else ''
    
    # Get coach headshot
    headshot_key = f"{coach_name}_{school}"
    coach_headshot = coach_headshots.get(headshot_key, '')
    
    # Process rankings data
    rankings = sorted(data['rankings'], key=lambda x: (x['poll']['season'], x['poll']['week']))
    
    ranking_data = []
    for r in rankings:
        season = r['poll']['season']
        week = r['poll']['week']
        # Approximate date: season year + (week * 7 days from Sept 1)
        base_date = datetime(season, 9, 1)
        approx_date = base_date + timedelta(days=(week - 1) * 7)
        
        # Highcharts uses milliseconds
        timestamp = int(approx_date.timestamp() * 1000)
        # Invert rank so #1 is highest
        inverted_rank = 26 - r['rank']
        
        ranking_data.append([timestamp, inverted_rank])
    
    # Get talent ratings for annotations
    talent_ratings = data['talent_ratings']
    
    # Get draft picks by year
    draft_by_year = {}
    for pick in data['draft_picks']:
        year = pick['year']
        if year not in draft_by_year:
            draft_by_year[year] = {
                'total': 0,
                'round1': 0,
                'picks': []
            }
        draft_by_year[year]['total'] += 1
        if pick['round'] == 1:
            draft_by_year[year]['round1'] += 1
        draft_by_year[year]['picks'].append(pick)
    
    # Find peak talent year
    peak_talent = max(talent_ratings, key=lambda x: x['talent'])
    
    # Find #1 rankings if any
    top_rankings = [r for r in rankings if r['rank'] == 1]
    
    # Find biggest draft years
    top_draft_years = sorted(draft_by_year.items(), key=lambda x: x[1]['total'], reverse=True)[:3]
    
    return {
        'coach': coach_name,
        'school': school,
        'teamColor': team_color,
        'teamLogo': team_logo,
        'coachHeadshot': coach_headshot,
        'data': ranking_data,
        'metadata': {
            'total_games': data['summary']['overview']['total_games'],
            'record': data['summary']['overview']['total_record'],
            'win_pct': data['summary']['overview']['win_pct'],
            'total_draft_picks': len(data['draft_picks']),
            'peak_talent': peak_talent,
            'top_rankings_count': len(top_rankings),
            'top_draft_years': [
                {
                    'year': year,
                    'total': info['total'],
                    'round1': info['round1']
                }
                for year, info in top_draft_years
            ]
        }
    }

def main():
    enhanced_dir = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/enhanced_coaches')
    output_dir = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/data/coach_timelines')
    output_dir.mkdir(exist_ok=True)
    
    # Load FBS teams data and coach headshots
    fbs_teams = load_fbs_teams()
    coach_headshots = load_coach_headshots()
    
    # Generate data for all coaches
    for coach_file in enhanced_dir.glob('*.json'):
        try:
            timeline_data = generate_timeline_data(coach_file, fbs_teams, coach_headshots)
            
            # Save to output directory
            output_file = output_dir / f"{coach_file.stem}_timeline.json"
            with open(output_file, 'w') as f:
                json.dump(timeline_data, f, indent=2)
            
            print(f"✅ Generated: {coach_file.stem}")
        except Exception as e:
            print(f"❌ Error processing {coach_file.stem}: {e}")
    
    print(f"\n✅ Timeline data generated in: {output_dir}")

if __name__ == '__main__':
    main()
