#!/usr/bin/env python3
"""
Analyze Team Drive Data
Extract and analyze drive statistics for specific teams
"""

import json
import sys
from collections import defaultdict

def analyze_team_drives(drives_file, *teams):
    """Analyze drive statistics for specified teams"""
    
    print("\n" + "="*80)
    print(f"Checking Drive Analytics for {' and '.join(teams)} (2025 Season)")
    print("="*80 + "\n")
    
    # Load all drives
    with open(drives_file, 'r') as f:
        all_drives = json.load(f)
    
    for team in teams:
        print("="*80)
        print(f"📊 {team.upper()} - 2025 SEASON")
        print("="*80)
        
        # Filter drives where this team is on offense
        team_drives = [d for d in all_drives if d.get('offense') == team]
        
        print(f"  Total drives: {len(team_drives)}\n")
        
        if not team_drives:
            print(f"  ⚠️  No drives found for {team}\n")
            continue
        
        # Quarter analysis
        quarters = defaultdict(lambda: {'total': 0, 'scored': 0})
        
        for drive in team_drives:
            period = drive.get('startPeriod', 0)
            quarters[period]['total'] += 1
            if drive.get('scoring', False):
                quarters[period]['scored'] += 1
        
        print("📈 DRIVE SUCCESS BY QUARTER:")
        for q in sorted(quarters.keys()):
            if q > 0 and q <= 4:
                total = quarters[q]['total']
                scored = quarters[q]['scored']
                pct = (scored / total * 100) if total > 0 else 0
                print(f"  Q{q}: {scored}/{total} drives scored ({pct:.1f}%)")
        
        # Field position analysis
        field_zones = {
            'Own 1-20': {'total': 0, 'scored': 0},
            'Own 21-40': {'total': 0, 'scored': 0},
            'Own 41-Mid': {'total': 0, 'scored': 0},
            'Opp Territory': {'total': 0, 'scored': 0}
        }
        
        for drive in team_drives:
            start_yard = drive.get('startYardline', 0)
            scored = drive.get('scoring', False)
            
            if start_yard <= 20:
                zone = 'Own 1-20'
            elif start_yard <= 40:
                zone = 'Own 21-40'
            elif start_yard <= 50:
                zone = 'Own 41-Mid'
            else:
                zone = 'Opp Territory'
            
            field_zones[zone]['total'] += 1
            if scored:
                field_zones[zone]['scored'] += 1
        
        print("\n📍 FIELD POSITION SCORING:")
        for zone, stats in field_zones.items():
            total = stats['total']
            scored = stats['scored']
            if total > 0:
                pct = (scored / total * 100)
                print(f"  {zone}: {scored}/{total} scored ({pct:.1f}%)")
        
        # Drive outcomes
        outcomes = defaultdict(int)
        td_count = 0
        fg_count = 0
        punt_count = 0
        turnover_count = 0
        
        for drive in team_drives:
            result = drive.get('driveResult', 'UNKNOWN')
            outcomes[result] += 1
            
            if result == 'TD':
                td_count += 1
            elif result == 'FG':
                fg_count += 1
            elif result == 'PUNT':
                punt_count += 1
            elif result in ['INT', 'FUMBLE', 'INT TD', 'FUMBLE TD']:
                turnover_count += 1
        
        print("\n🎯 DRIVE OUTCOMES:")
        total = len(team_drives)
        print(f"  Touchdowns: {td_count} ({td_count/total*100:.1f}%)")
        print(f"  Field Goals: {fg_count} ({fg_count/total*100:.1f}%)")
        print(f"  Punts: {punt_count} ({punt_count/total*100:.1f}%)")
        print(f"  Turnovers: {turnover_count} ({turnover_count/total*100:.1f}%)")
        
        print("\n  All outcomes:")
        for outcome in sorted(outcomes.keys(), key=lambda x: outcomes[x], reverse=True):
            count = outcomes[outcome]
            pct = (count / total * 100)
            print(f"    {outcome}: {count} ({pct:.1f}%)")
        
        print()
    
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80 + "\n")

def extract_and_analyze(source_file, output_file, *teams):
    """Extract drives for specific teams and analyze them"""
    
    # Load all drives
    with open(source_file, 'r') as f:
        all_drives = json.load(f)
    
    # Extract drives for specified teams
    team_drives = []
    for drive in all_drives:
        offense = drive.get('offense', '')
        defense = drive.get('defense', '')
        
        if any(team in [offense, defense] for team in teams):
            team_drives.append(drive)
    
    # Save extracted drives
    with open(output_file, 'w') as f:
        json.dump(team_drives, f, indent=2)
    
    print(f"✅ Extracted {len(team_drives)} drives to {output_file}\n")
    
    # Analyze the drives
    analyze_team_drives(output_file, *teams)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_team_drives.py <team1> [team2] [team3] ...")
        print("Example: python analyze_team_drives.py Georgia Alabama")
        sys.exit(1)
    
    teams = sys.argv[1:]
    source_file = "data/power5_drives_only.json"
    output_file = f"{'_'.join([t.lower() for t in teams])}_drives.json"
    
    extract_and_analyze(source_file, output_file, *teams)
