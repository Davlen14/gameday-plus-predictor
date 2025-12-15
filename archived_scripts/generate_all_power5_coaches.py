#!/usr/bin/env python3
"""
Generate comprehensive coaching profiles for all Power 5 + Independent coaches
Based on the Ryanday.py template
"""

import json
import os
import sys
from pathlib import Path

# Add the GamedayPlus_Stats directory to path to import Ryanday module
stats_dir = Path.home() / "Desktop" / "GamedayPlus_Stats"
sys.path.insert(0, str(stats_dir))

# Import the coach analyzer (we'll need to modify Ryanday.py to be importable)
# For now, we'll use subprocess to call it

import subprocess
import time

def load_power5_teams():
    """Load Power 5 + Independent teams from fbs.json"""
    with open('fbs.json') as f:
        teams = json.load(f)
    
    power5_conferences = ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12', 'FBS Independents']
    return [t for t in teams if t.get('conference') in power5_conferences]

def load_coaches_json():
    """Load coaches from Coaches.json"""
    with open('Coaches.json') as f:
        return json.load(f)

def get_current_coach(school, coaches_data):
    """Get current coach for a school"""
    # Filter for current coaches (most recent year)
    school_coaches = [c for c in coaches_data if c.get('school') == school]
    if not school_coaches:
        return None
    
    # Sort by year descending to get most recent
    school_coaches.sort(key=lambda x: int(x.get('year', 0)), reverse=True)
    
    # Get the most recent coach
    latest = school_coaches[0]
    return {
        'name': latest.get('first_name', '') + ' ' + latest.get('last_name', ''),
        'first_name': latest.get('first_name'),
        'last_name': latest.get('last_name'),
        'school': school,
        'start_year': latest.get('year')
    }

def generate_coach_file(coach_name, school, output_dir):
    """
    Generate comprehensive coach profile using modified Ryanday.py logic
    
    For now, this will call the Ryanday.py script as a subprocess
    In production, you'd refactor Ryanday.py to be a class/module
    """
    print(f"🏈 Generating profile for {coach_name} ({school})...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Sanitize filename
    safe_name = coach_name.lower().replace(' ', '_').replace('.', '')
    output_file = os.path.join(output_dir, f"{safe_name}.json")
    
    # For now, return placeholder
    # TODO: Modify Ryanday.py to accept coach/school as CLI args
    print(f"   ⚠️  Placeholder - need to adapt Ryanday.py for multiple coaches")
    return None

def build_master_summary(coaches_dir):
    """Build master summary from all generated coach files"""
    master = {
        "metadata": {
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_coaches": 0,
            "conferences": {},
            "data_source": "College Football Data GraphQL API"
        },
        "coaches": {},
        "rankings": {
            "by_win_pct": [],
            "by_ats": [],
            "vs_ranked": []
        }
    }
    
    # Scan coaches directory
    coaches_files = list(Path(coaches_dir).rglob("*.json"))
    
    for coach_file in coaches_files:
        try:
            with open(coach_file) as f:
                data = json.load(f)
            
            coach_name = data['metadata']['coach']
            school = data['metadata']['school']
            
            # Extract quick stats
            summary = data.get('summary', {})
            overview = summary.get('overview', {})
            kpis = summary.get('key_performance_indicators', {})
            
            master['coaches'][coach_name] = {
                "school": school,
                "conference": data['metadata'].get('conference', 'Unknown'),
                "file": str(coach_file.relative_to(coaches_dir)),
                "quick_stats": {
                    "record": overview.get('total_record', 'N/A'),
                    "win_pct": overview.get('win_pct', 0),
                    "vs_ranked": kpis.get('vs_ranked', 'N/A'),
                    "ats_2025": kpis.get('ats_2025', 'N/A'),
                    "avg_margin": kpis.get('avg_margin', 0)
                }
            }
            
            master['metadata']['total_coaches'] += 1
            
        except Exception as e:
            print(f"⚠️  Error processing {coach_file}: {e}")
    
    return master

def main():
    """Main execution"""
    print("🏈 Power 5 + Independent Coaches Generator")
    print("=" * 60)
    
    # Load data
    print("\n📊 Loading data...")
    power5_teams = load_power5_teams()
    print(f"   Found {len(power5_teams)} Power 5 + Independent teams")
    
    coaches_data = load_coaches_json()
    print(f"   Loaded {len(coaches_data)} coaching records")
    
    # Create output structure
    coaches_dir = "coaches"
    os.makedirs(coaches_dir, exist_ok=True)
    
    # Generate profiles
    print(f"\n🎯 Generating coach profiles...")
    print(f"   Output directory: {coaches_dir}/")
    print()
    
    generated = 0
    skipped = 0
    
    for team in power5_teams[:5]:  # Start with first 5 for testing
        school = team['school']
        conference = team['conference']
        
        coach = get_current_coach(school, coaches_data)
        if not coach:
            print(f"⚠️  No coach found for {school}")
            skipped += 1
            continue
        
        coach_name = coach['name']
        
        # Create conference subdirectory
        conf_dir = os.path.join(coaches_dir, conference.lower().replace(' ', '_'))
        
        result = generate_coach_file(coach_name, school, conf_dir)
        if result:
            generated += 1
        else:
            skipped += 1
    
    print(f"\n✅ Generation complete!")
    print(f"   Generated: {generated}")
    print(f"   Skipped: {skipped}")
    
    # Build master summary
    if generated > 0:
        print(f"\n📋 Building master summary...")
        master = build_master_summary(coaches_dir)
        
        with open('master_power5_coaches.json', 'w') as f:
            json.dump(master, f, indent=2)
        
        print(f"   Saved to master_power5_coaches.json")

if __name__ == "__main__":
    main()
