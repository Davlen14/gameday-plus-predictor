#!/usr/bin/env python3
"""
Download Power 5 Drive Data
Get comprehensive drive data for all Power 5 teams
"""

import requests
import json
from datetime import datetime

# REST API Key
REST_API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
BASE_URL = "https://api.collegefootballdata.com"

def download_all_drives():
    """Download all drives for all teams (we'll filter for Power 5 after)"""
    
    print("🚗 DOWNLOADING ALL DRIVES DATA")
    print("=" * 35)
    
    headers = {
        "Authorization": f"Bearer {REST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_drives = []
    
    # Download drives for weeks 1-14
    for week in range(1, 15):
        print(f"\n📊 Week {week}...")
        
        try:
            response = requests.get(
                f"{BASE_URL}/drives",
                params={
                    "year": 2025,
                    "week": week
                },
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                drives = response.json()
                
                # Add week and season info to each drive
                for drive in drives:
                    drive['week'] = week
                    drive['season'] = 2025
                
                all_drives.extend(drives)
                
                print(f"   ✅ {len(drives)} drives")
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 TOTAL DRIVES DOWNLOADED:")
    print(f"   📊 All drives: {len(all_drives):,}")
    
    return all_drives

def filter_power5_drives(all_drives):
    """Filter drives for Power 5 teams only"""
    
    print(f"\n💪 FILTERING FOR POWER 5 TEAMS")
    print("=" * 35)
    
    # Define Power 5 conferences
    power5_conferences = {
        'ACC', 'Big Ten', 'Big 12', 'SEC', 'Pac-12'
    }
    
    power5_drives = []
    power5_teams = set()
    
    for drive in all_drives:
        offense_conf = drive.get('offenseConference', '')
        defense_conf = drive.get('defenseConference', '')
        
        # Include drive if either team is Power 5
        if offense_conf in power5_conferences or defense_conf in power5_conferences:
            power5_drives.append(drive)
            
            # Track Power 5 team names
            if offense_conf in power5_conferences:
                power5_teams.add(drive.get('offense'))
            if defense_conf in power5_conferences:
                power5_teams.add(drive.get('defense'))
    
    print(f"✅ Power 5 filtering complete:")
    print(f"   📊 Power 5 drives: {len(power5_drives):,}")
    print(f"   🏈 Power 5 teams: {len(power5_teams)}")
    print(f"   📉 Size reduction: {((len(all_drives) - len(power5_drives)) / len(all_drives)) * 100:.1f}%")
    
    return power5_drives, sorted(list(power5_teams))

def analyze_power5_drives(power5_drives, power5_teams):
    """Analyze the Power 5 drive data"""
    
    print(f"\n📈 POWER 5 DRIVE ANALYSIS")
    print("=" * 30)
    
    # Conference breakdown
    conf_stats = {}
    for drive in power5_drives:
        for conf_field in ['offenseConference', 'defenseConference']:
            conf = drive.get(conf_field, '')
            if conf in ['ACC', 'Big Ten', 'Big 12', 'SEC', 'Pac-12']:
                if conf not in conf_stats:
                    conf_stats[conf] = {'drives': 0, 'scoring_drives': 0}
                conf_stats[conf]['drives'] += 1
                if drive.get('scoring'):
                    conf_stats[conf]['scoring_drives'] += 1
    
    print(f"🏟️ CONFERENCE BREAKDOWN:")
    for conf, stats in sorted(conf_stats.items()):
        drives = stats['drives']
        scoring = stats['scoring_drives']
        scoring_pct = (scoring / drives * 100) if drives > 0 else 0
        print(f"   {conf}: {drives:,} drives ({scoring_pct:.1f}% scoring)")
    
    # Top Power 5 teams by drive count
    team_drive_counts = {}
    for drive in power5_drives:
        for team_field in ['offense', 'defense']:
            team = drive.get(team_field, '')
            if team in power5_teams:
                team_drive_counts[team] = team_drive_counts.get(team, 0) + 1
    
    top_teams = sorted(team_drive_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n🏆 TOP 10 TEAMS BY DRIVE COUNT:")
    for i, (team, count) in enumerate(top_teams, 1):
        print(f"   {i:2d}. {team:<25} {count:,} drives")
    
    return conf_stats

def save_power5_data(power5_drives, power5_teams, conf_stats):
    """Save Power 5 drive data and create summary"""
    
    print(f"\n💾 SAVING POWER 5 DATA")
    print("=" * 25)
    
    # Create comprehensive Power 5 dataset
    power5_dataset = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'season': 2025,
            'weeks_covered': list(range(1, 15)),
            'total_drives': len(power5_drives),
            'total_teams': len(power5_teams),
            'conferences': ['ACC', 'Big Ten', 'Big 12', 'SEC', 'Pac-12'],
            'api_calls_used': 14,
            'api_percentage': 0.28
        },
        'drives': power5_drives,
        'teams': power5_teams,
        'conference_stats': conf_stats
    }
    
    # Save main Power 5 file
    with open('power5_drives_complete.json', 'w') as f:
        json.dump(power5_dataset, f, indent=2)
    
    # Save drives-only file (smaller, for direct analysis)
    with open('power5_drives_only.json', 'w') as f:
        json.dump(power5_drives, f, indent=2)
    
    # Create summary for React app
    summary = {
        'metadata': power5_dataset['metadata'],
        'summary_stats': {
            'total_drives': len(power5_drives),
            'conferences': list(conf_stats.keys()),
            'teams': power5_teams,
            'conference_breakdown': conf_stats
        }
    }
    
    with open('power5_drives_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Calculate file sizes
    import os
    
    complete_size = os.path.getsize('power5_drives_complete.json') / (1024 * 1024)
    drives_size = os.path.getsize('power5_drives_only.json') / (1024 * 1024)
    summary_size = os.path.getsize('power5_drives_summary.json') / (1024 * 1024)
    
    print(f"✅ Files saved:")
    print(f"   📊 power5_drives_complete.json: {complete_size:.1f} MB")
    print(f"   🚗 power5_drives_only.json: {drives_size:.1f} MB") 
    print(f"   📋 power5_drives_summary.json: {summary_size:.2f} MB")
    
    return complete_size

def create_react_optimized_exports(power5_drives):
    """Create React-optimized data exports"""
    
    print(f"\n🚀 CREATING REACT-OPTIMIZED EXPORTS")
    print("=" * 40)
    
    # Group drives by team for easier React usage
    teams_data = {}
    
    for drive in power5_drives:
        offense = drive.get('offense', '')
        defense = drive.get('defense', '')
        
        # Add to offense team data
        if offense:
            if offense not in teams_data:
                teams_data[offense] = {'offensive_drives': [], 'defensive_drives': []}
            teams_data[offense]['offensive_drives'].append(drive)
        
        # Add to defense team data  
        if defense:
            if defense not in teams_data:
                teams_data[defense] = {'offensive_drives': [], 'defensive_drives': []}
            teams_data[defense]['defensive_drives'].append(drive)
    
    # Calculate team efficiency stats
    team_efficiency = {}
    for team, data in teams_data.items():
        offensive = data['offensive_drives']
        defensive = data['defensive_drives']
        
        team_efficiency[team] = {
            'team': team,
            'offensive_drives': len(offensive),
            'defensive_drives': len(defensive),
            'offensive_scoring': len([d for d in offensive if d.get('scoring')]),
            'defensive_scoring_allowed': len([d for d in defensive if d.get('scoring')]),
            'offensive_scoring_pct': len([d for d in offensive if d.get('scoring')]) / len(offensive) * 100 if offensive else 0,
            'defensive_stop_pct': (len(defensive) - len([d for d in defensive if d.get('scoring')])) / len(defensive) * 100 if defensive else 0
        }
    
    # Save React-optimized files
    with open('react_power5_teams.json', 'w') as f:
        json.dump(teams_data, f, indent=2)
    
    with open('react_power5_efficiency.json', 'w') as f:
        json.dump(team_efficiency, f, indent=2)
    
    print(f"✅ React-optimized files created:")
    print(f"   🏈 react_power5_teams.json (by team)")
    print(f"   📊 react_power5_efficiency.json (team stats)")

if __name__ == "__main__":
    print("💪 POWER 5 DRIVE DATA DOWNLOAD")
    print("=" * 35)
    
    # Download all drives data
    all_drives = download_all_drives()
    
    if all_drives:
        # Filter for Power 5 only
        power5_drives, power5_teams = filter_power5_drives(all_drives)
        
        # Analyze the data
        conf_stats = analyze_power5_drives(power5_drives, power5_teams)
        
        # Save comprehensive data
        file_size = save_power5_data(power5_drives, power5_teams, conf_stats)
        
        # Create React-optimized exports
        create_react_optimized_exports(power5_drives)
        
        print(f"\n🎯 POWER 5 DRIVE DATA COMPLETE!")
        print(f"   📊 Total drives: {len(power5_drives):,}")
        print(f"   🏈 Power 5 teams: {len(power5_teams)}")
        print(f"   💾 Main file size: {file_size:.1f} MB")
        print(f"   💰 API calls used: 14 (0.28% of monthly limit)")
        print(f"   📁 Files created: 5 JSON files")
        print(f"   🚀 Ready for React app integration!")
    else:
        print(f"\n❌ Failed to download drive data")