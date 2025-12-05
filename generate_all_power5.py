#!/usr/bin/env python3
"""
Generate coaching profiles for ALL Power 5 + Independent coaches
Automatically discovers current coaches and generates comprehensive profiles
"""
import json
import subprocess
import os
from pathlib import Path
from datetime import datetime

def load_power5_teams():
    """Load Power 5 + Independent teams from fbs.json"""
    with open('fbs.json') as f:
        teams = json.load(f)
    
    power5_conferences = ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12', 'FBS Independents']
    p5_teams = [t for t in teams if t.get('conference') in power5_conferences]
    
    # Sort by conference for organized output
    p5_teams.sort(key=lambda x: (x.get('conference', ''), x.get('school', '')))
    
    return p5_teams

def load_all_coaches():
    """Load all coaching records from Coaches.json"""
    with open('Coaches.json') as f:
        return json.load(f)

def get_current_coach(school, all_coaches):
    """Get the most recent coach for a school"""
    school_coaches = [c for c in all_coaches if c.get('school') == school]
    
    if not school_coaches:
        return None
    
    # Sort by year descending
    school_coaches.sort(key=lambda x: int(x.get('year', 0)), reverse=True)
    
    latest = school_coaches[0]
    first_name = latest.get('first_name', '').strip()
    last_name = latest.get('last_name', '').strip()
    
    if not first_name or not last_name:
        return None
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'school': school,
        'latest_year': latest.get('year')
    }

def generate_coach_profile(coach_info, output_dir):
    """Generate comprehensive coach profile using universal_coach_analyzer.py"""
    first_name = coach_info['first_name']
    last_name = coach_info['last_name']
    school = coach_info['school']
    
    # Create safe filename
    safe_name = f"{last_name.lower().replace(' ', '_')}_{school.lower().replace(' ', '_').replace('&', 'and')}.json"
    output_file = os.path.join(output_dir, safe_name)
    
    # Skip if already exists
    if os.path.exists(output_file):
        print(f"  ⏭️  Skipping {first_name} {last_name} ({school}) - already exists")
        return output_file, True
    
    print(f"  🏈 Generating {first_name} {last_name} ({school})...")
    
    try:
        # Run universal_coach_analyzer.py
        result = subprocess.run(
            ['python3', 'universal_coach_analyzer.py', first_name, last_name, school],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout per coach
        )
        
        if result.returncode == 0:
            # Move output file to correct directory
            default_output = f"{last_name.lower().replace(' ', '_')}_{school.lower().replace(' ', '_')}.json"
            if os.path.exists(default_output):
                os.rename(default_output, output_file)
            
            print(f"     ✅ Success!")
            return output_file, True
        else:
            print(f"     ❌ Failed: {result.stderr[:100]}")
            return None, False
            
    except subprocess.TimeoutExpired:
        print(f"     ⏱️  Timeout (>2 minutes)")
        return None, False
    except Exception as e:
        print(f"     ❌ Error: {str(e)[:100]}")
        return None, False

def build_master_summary(coaches_dir):
    """Build master summary JSON from all generated coach files"""
    print("\n📋 Building master summary...")
    
    master = {
        "metadata": {
            "generated": str(datetime.now()),
            "total_coaches": 0,
            "by_conference": {},
            "data_source": "College Football Data GraphQL API"
        },
        "coaches": {},
        "rankings": {
            "by_win_pct": [],
            "by_total_wins": [],
            "by_tenure_years": []
        }
    }
    
    coach_list = []
    
    # Scan all JSON files in coaches directory
    for json_file in Path(coaches_dir).glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            metadata = data.get('metadata', {})
            summary = data.get('summary', {}).get('overview', {})
            
            coach_name = metadata.get('coach', 'Unknown')
            school = metadata.get('school', 'Unknown')
            
            # Extract quick stats
            quick_stats = {
                "school": school,
                "file": str(json_file.name),
                "record": summary.get('total_record', 'N/A'),
                "win_pct": summary.get('win_pct', 0),
                "total_games": summary.get('total_games', 0),
                "tenure": metadata.get('era', 'N/A'),
                "tenure_years": metadata.get('tenure_years', 0)
            }
            
            master['coaches'][coach_name] = quick_stats
            coach_list.append({
                'name': coach_name,
                'win_pct': quick_stats['win_pct'],
                'total_wins': int(summary.get('total_record', '0-0').split('-')[0]),
                'tenure_years': quick_stats['tenure_years']
            })
            
            master['metadata']['total_coaches'] += 1
            
        except Exception as e:
            print(f"  ⚠️  Error processing {json_file}: {e}")
    
    # Build rankings
    master['rankings']['by_win_pct'] = sorted(
        coach_list, 
        key=lambda x: x['win_pct'], 
        reverse=True
    )[:25]
    
    master['rankings']['by_total_wins'] = sorted(
        coach_list,
        key=lambda x: x['total_wins'],
        reverse=True
    )[:25]
    
    master['rankings']['by_tenure_years'] = sorted(
        coach_list,
        key=lambda x: x['tenure_years'],
        reverse=True
    )[:25]
    
    # Save master file
    with open('master_enhanced_coaches.json', 'w') as f:
        json.dump(master, f, indent=2)
    
    print(f"  ✅ Master summary saved: master_enhanced_coaches.json")
    print(f"  📊 Total coaches: {master['metadata']['total_coaches']}")
    
    return master

def main():
    """Main execution"""
    print("=" * 80)
    print("🏈 POWER 5 + INDEPENDENT COACHES - MASTER GENERATOR")
    print("=" * 80)
    
    # Create output directory
    coaches_dir = "enhanced_coaches"
    os.makedirs(coaches_dir, exist_ok=True)
    
    # Load data
    print("\n📊 Loading data...")
    power5_teams = load_power5_teams()
    all_coaches = load_all_coaches()
    
    print(f"  ✓ Found {len(power5_teams)} Power 5 + Independent teams")
    print(f"  ✓ Loaded {len(all_coaches)} coaching records")
    
    # Discover current coaches
    print("\n🔍 Discovering current coaches...")
    current_coaches = []
    
    for team in power5_teams:
        school = team['school']
        conference = team['conference']
        
        coach = get_current_coach(school, all_coaches)
        if coach:
            coach['conference'] = conference
            current_coaches.append(coach)
            print(f"  ✓ {school}: {coach['first_name']} {coach['last_name']}")
        else:
            print(f"  ⚠️  {school}: No coach found")
    
    print(f"\n📋 Found {len(current_coaches)} current coaches")
    
    # Generate profiles
    print(f"\n🚀 Generating comprehensive profiles...")
    print(f"   Output directory: {coaches_dir}/")
    print(f"   Estimated time: ~{len(current_coaches) * 0.7:.0f} minutes")
    print()
    
    generated = 0
    failed = 0
    skipped = 0
    
    for i, coach in enumerate(current_coaches, 1):
        print(f"[{i}/{len(current_coaches)}]", end=" ")
        
        result, success = generate_coach_profile(coach, coaches_dir)
        
        if success and result:
            if "already exists" in str(result):
                skipped += 1
            else:
                generated += 1
        else:
            failed += 1
    
    # Build master summary
    master = build_master_summary(coaches_dir)
    
    # Final report
    print("\n" + "=" * 80)
    print("✅ GENERATION COMPLETE!")
    print("=" * 80)
    print(f"📊 Statistics:")
    print(f"   Generated: {generated}")
    print(f"   Skipped (existing): {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Total: {generated + skipped + failed}")
    print(f"\n📁 Output:")
    print(f"   Individual files: {coaches_dir}/")
    print(f"   Master summary: master_enhanced_coaches.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
