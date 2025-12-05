#!/usr/bin/env python3
"""
Simple Power 5 + Independent Coach Generator
Generates comprehensive profiles for all current FBS coaches
"""
import json
import subprocess
import os
import time
from pathlib import Path

def load_power5_teams():
    """Load Power 5 + Independent teams from fbs.json"""
    with open('fbs.json') as f:
        teams = json.load(f)
    
    power5_conferences = ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12', 'FBS Independents']
    p5_teams = [t for t in teams if t.get('conference') in power5_conferences]
    
    # Sort by conference
    p5_teams.sort(key=lambda x: (x.get('conference', ''), x.get('school', '')))
    
    return p5_teams

def generate_coach_for_school(school, conference, output_dir):
    """
    Generate comprehensive coach profile for a school
    The universal_coach_analyzer will auto-detect the current coach
    """
    print(f"🏈 {school} ({conference})...")
    
    # For now, we need coach names. Let's use the Coaches.json aggregated data
    coaches_data = json.load(open('Coaches.json'))
    
    # Find coach for this school
    coach_info = None
    for coach in coaches_data.get('coaches', []):
        if coach.get('team') == school:
            coach_info = coach
            break
    
    if not coach_info:
        print(f"   ⚠️  No coach data found for {school}")
        return None, False
    
    coach_name = coach_info.get('name', '')
    parts = coach_name.split()
    
    if len(parts) < 2:
        print(f"   ⚠️  Invalid coach name: {coach_name}")
        return None, False
    
    first_name = parts[0]
    last_name = ' '.join(parts[1:])
    
    # Create safe filename
    safe_name = f"{last_name.lower().replace(' ', '_')}_{school.lower().replace(' ', '_').replace('&', 'and')}.json"
    output_file = os.path.join(output_dir, safe_name)
    
    # Skip if already exists
    if os.path.exists(output_file):
        print(f"   ⏭️  Already exists")
        return output_file, True
    
    try:
        # Run universal_coach_analyzer.py with timeout
        result = subprocess.run(
            ['python3', 'universal_coach_analyzer.py', first_name, last_name, school],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        if result.returncode == 0:
            # Move to enhanced_coaches directory
            default_file = f"{last_name.lower().replace(' ', '_')}_{school.lower().replace(' ', '_')}.json"
            if os.path.exists(default_file):
                os.rename(default_file, output_file)
                print(f"   ✅ Generated: {coach_name}")
                return output_file, True
            else:
                print(f"   ⚠️  File not found after generation")
                return None, False
        else:
            error_msg = result.stderr[:150] if result.stderr else "Unknown error"
            print(f"   ❌ Failed: {error_msg}")
            return None, False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  Timeout (>90s)")
        return None, False
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return None, False

def main():
    """Main execution"""
    print("=" * 80)
    print("🏈 ENHANCED COACHES GENERATOR - Power 5 + Independents")
    print("=" * 80)
    
    # Create output directory
    output_dir = "enhanced_coaches"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load teams
    print("\n📊 Loading Power 5 + Independent teams...")
    teams = load_power5_teams()
    print(f"   ✓ Found {len(teams)} teams\n")
    
    # Show conference breakdown
    conferences = {}
    for team in teams:
        conf = team.get('conference', 'Unknown')
        conferences[conf] = conferences.get(conf, 0) + 1
    
    print("📋 Conference Breakdown:")
    for conf, count in sorted(conferences.items()):
        print(f"   {conf}: {count} teams")
    
    print(f"\n🚀 Starting generation...")
    print(f"   Output directory: {output_dir}/")
    print(f"   Estimated time: ~{len(teams) * 0.7:.0f} minutes\n")
    print("=" * 80 + "\n")
    
    generated = 0
    skipped = 0
    failed = 0
    start_time = time.time()
    
    for i, team in enumerate(teams, 1):
        school = team['school']
        conference = team['conference']
        
        print(f"[{i}/{len(teams)}] ", end="")
        
        result, success = generate_coach_for_school(school, conference, output_dir)
        
        if success:
            if result and "already exists" not in str(result):
                generated += 1
            else:
                skipped += 1
        else:
            failed += 1
        
        # Progress update every 10 teams
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(teams) - i) / rate if rate > 0 else 0
            print(f"\n   📊 Progress: {generated} generated, {skipped} skipped, {failed} failed")
            print(f"   ⏱️  ETA: {remaining/60:.1f} minutes\n")
    
    elapsed_total = time.time() - start_time
    
    # Final report
    print("\n" + "=" * 80)
    print("✅ GENERATION COMPLETE!")
    print("=" * 80)
    print(f"📊 Statistics:")
    print(f"   Generated: {generated}")
    print(f"   Skipped (existing): {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Total Processed: {len(teams)}")
    print(f"   Success Rate: {((generated + skipped) / len(teams) * 100):.1f}%")
    print(f"\n⏱️  Time:")
    print(f"   Total: {elapsed_total/60:.1f} minutes")
    print(f"   Average: {elapsed_total/len(teams):.1f} seconds per coach")
    print(f"\n📁 Output:")
    print(f"   Directory: {output_dir}/")
    print(f"   Files: {generated + skipped}")
    print("=" * 80)

if __name__ == "__main__":
    main()
