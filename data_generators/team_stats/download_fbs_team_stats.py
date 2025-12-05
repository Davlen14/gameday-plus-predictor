#!/usr/bin/env python3
"""
Download All FBS Team Season Stats
Get comprehensive offensive and defensive stats for all FBS teams
"""

import requests
import json
from datetime import datetime

# REST API Key
REST_API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
BASE_URL = "https://api.collegefootballdata.com"

def download_team_season_stats():
    """Download comprehensive team season statistics"""
    
    print("📊 DOWNLOADING TEAM SEASON STATS")
    print("=" * 35)
    
    headers = {
        "Authorization": f"Bearer {REST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_stats = []
    
    try:
        response = requests.get(
            f"{BASE_URL}/stats/season",
            params={"year": 2025},
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            stats_data = response.json()
            
            print(f"✅ Downloaded {len(stats_data):,} stat records")
            
            # Show sample of what we got
            if stats_data:
                sample = stats_data[0]
                print(f"\n📊 SAMPLE STAT RECORD:")
                print(f"   Team: {sample.get('team')}")
                print(f"   Conference: {sample.get('conference')}")
                print(f"   Stat Name: {sample.get('statName')}")
                print(f"   Stat Value: {sample.get('statValue')}")
                
                # Count unique stats and teams
                unique_teams = set(record.get('team') for record in stats_data)
                unique_stats = set(record.get('statName') for record in stats_data)
                
                print(f"\n📈 DATA OVERVIEW:")
                print(f"   Unique teams: {len(unique_teams)}")
                print(f"   Unique stats: {len(unique_stats)}")
            
            return stats_data
            
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def download_advanced_team_stats():
    """Download advanced team statistics"""
    
    print(f"\n📊 DOWNLOADING ADVANCED TEAM STATS")
    print("=" * 35)
    
    headers = {
        "Authorization": f"Bearer {REST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/stats/season/advanced",
            params={"year": 2025},
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            advanced_data = response.json()
            
            print(f"✅ Downloaded {len(advanced_data)} advanced stat records")
            
            if advanced_data:
                sample = advanced_data[0]
                print(f"\n📊 SAMPLE ADVANCED RECORD:")
                print(f"   Team: {sample.get('team')}")
                print(f"   Conference: {sample.get('conference')}")
                
                # Show offensive stats
                if 'offense' in sample:
                    offense = sample['offense']
                    print(f"   Offensive stats: {list(offense.keys())[:5]}...")
                
                # Show defensive stats  
                if 'defense' in sample:
                    defense = sample['defense']
                    print(f"   Defensive stats: {list(defense.keys())[:5]}...")
            
            return advanced_data
            
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def process_team_stats(basic_stats, advanced_stats):
    """Process and organize team statistics"""
    
    print(f"\n🔄 PROCESSING TEAM STATISTICS")
    print("=" * 35)
    
    # Organize basic stats by team
    teams_basic = {}
    for record in basic_stats:
        team = record.get('team')
        if not team:
            continue
            
        if team not in teams_basic:
            teams_basic[team] = {
                'team': team,
                'conference': record.get('conference'),
                'season': record.get('season', 2025),
                'stats': {}
            }
        
        stat_name = record.get('statName')
        stat_value = record.get('statValue')
        
        if stat_name and stat_value is not None:
            teams_basic[team]['stats'][stat_name] = stat_value
    
    # Add advanced stats
    teams_complete = teams_basic.copy()
    
    for record in advanced_stats:
        team = record.get('team')
        if team in teams_complete:
            # Add offensive stats
            if 'offense' in record:
                offense = record['offense']
                for stat, value in offense.items():
                    teams_complete[team]['stats'][f"offense_{stat}"] = value
            
            # Add defensive stats
            if 'defense' in record:
                defense = record['defense']
                for stat, value in defense.items():
                    teams_complete[team]['stats'][f"defense_{stat}"] = value
    
    # Convert to list
    teams_list = list(teams_complete.values())
    
    print(f"✅ Processed stats for {len(teams_list)} teams")
    
    # Show stat categories
    if teams_list:
        sample_stats = teams_list[0]['stats'].keys()
        offensive_stats = [s for s in sample_stats if 'offense' in s.lower() or any(off in s.lower() for off in ['passing', 'rushing', 'receiving', 'scoring'])]
        defensive_stats = [s for s in sample_stats if 'defense' in s.lower() or any(d in s.lower() for d in ['sacks', 'interceptions', 'tackles'])]
        
        print(f"\n📊 STAT CATEGORIES:")
        print(f"   Total stats per team: {len(sample_stats)}")
        print(f"   Offensive stats: {len(offensive_stats)}")
        print(f"   Defensive stats: {len(defensive_stats)}")
        print(f"   Other stats: {len(sample_stats) - len(offensive_stats) - len(defensive_stats)}")
    
    return teams_list

def filter_fbs_teams(teams_list):
    """Filter for FBS teams only"""
    
    print(f"\n🏈 FILTERING FOR FBS TEAMS")
    print("=" * 30)
    
    # Define FBS conferences
    fbs_conferences = {
        'ACC', 'American Athletic', 'Big 12', 'Big Ten', 'Conference USA',
        'FBS Independents', 'MAC', 'Mountain West', 'Pac-12', 'SEC', 'Sun Belt'
    }
    
    fbs_teams = []
    other_teams = []
    
    for team in teams_list:
        conf = team.get('conference', '')
        if conf in fbs_conferences:
            fbs_teams.append(team)
        else:
            other_teams.append(team)
    
    print(f"✅ FBS team filtering:")
    print(f"   FBS teams: {len(fbs_teams)}")
    print(f"   Other teams: {len(other_teams)}")
    
    # Show FBS conferences represented
    fbs_conf_counts = {}
    for team in fbs_teams:
        conf = team.get('conference', 'Unknown')
        fbs_conf_counts[conf] = fbs_conf_counts.get(conf, 0) + 1
    
    print(f"\n🏟️ FBS CONFERENCE BREAKDOWN:")
    for conf, count in sorted(fbs_conf_counts.items()):
        print(f"   {conf}: {count} teams")
    
    return fbs_teams

def create_offensive_defensive_breakdown(fbs_teams):
    """Create separate offensive and defensive stat files"""
    
    print(f"\n⚔️ CREATING OFFENSE/DEFENSE BREAKDOWN")
    print("=" * 40)
    
    offensive_stats = []
    defensive_stats = []
    
    for team in fbs_teams:
        team_name = team['team']
        conference = team['conference']
        stats = team['stats']
        
        # Offensive stats
        offensive_record = {
            'team': team_name,
            'conference': conference,
            'season': 2025
        }
        
        # Defensive stats
        defensive_record = {
            'team': team_name,
            'conference': conference,
            'season': 2025
        }
        
        # Categorize stats
        for stat_name, stat_value in stats.items():
            stat_lower = stat_name.lower()
            
            # Offensive indicators
            if any(off_term in stat_lower for off_term in [
                'offense', 'passing', 'rushing', 'receiving', 'scoring', 
                'yards', 'touchdowns', 'completions', 'attempts', 'carries'
            ]) and not any(def_term in stat_lower for def_term in ['defense', 'allowed', 'against']):
                offensive_record[stat_name] = stat_value
            
            # Defensive indicators
            elif any(def_term in stat_lower for def_term in [
                'defense', 'sacks', 'interceptions', 'tackles', 'fumbles', 
                'allowed', 'against', 'tfl', 'qbhurries'
            ]):
                defensive_record[stat_name] = stat_value
            
            # General stats (add to both)
            else:
                offensive_record[stat_name] = stat_value
                defensive_record[stat_name] = stat_value
        
        offensive_stats.append(offensive_record)
        defensive_stats.append(defensive_record)
    
    print(f"✅ Created offense/defense breakdown:")
    print(f"   Offensive records: {len(offensive_stats)}")
    print(f"   Defensive records: {len(defensive_stats)}")
    
    return offensive_stats, defensive_stats

def save_fbs_team_stats(fbs_teams, offensive_stats, defensive_stats):
    """Save FBS team statistics in multiple formats"""
    
    print(f"\n💾 SAVING FBS TEAM STATISTICS")
    print("=" * 35)
    
    # Create comprehensive dataset
    fbs_dataset = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'season': 2025,
            'total_teams': len(fbs_teams),
            'data_source': 'College Football Data API',
            'api_calls_used': 2,
            'api_percentage': 0.04
        },
        'teams': fbs_teams
    }
    
    # Save main comprehensive file
    with open('fbs_team_stats_complete.json', 'w') as f:
        json.dump(fbs_dataset, f, indent=2)
    
    # Save offense-only file
    offensive_dataset = {
        'metadata': fbs_dataset['metadata'],
        'offensive_stats': offensive_stats
    }
    with open('fbs_offensive_stats.json', 'w') as f:
        json.dump(offensive_dataset, f, indent=2)
    
    # Save defense-only file
    defensive_dataset = {
        'metadata': fbs_dataset['metadata'],
        'defensive_stats': defensive_stats
    }
    with open('fbs_defensive_stats.json', 'w') as f:
        json.dump(defensive_dataset, f, indent=2)
    
    # Save teams-only (just the data, no metadata wrapper)
    with open('fbs_teams_stats_only.json', 'w') as f:
        json.dump(fbs_teams, f, indent=2)
    
    # Calculate file sizes
    import os
    
    complete_size = os.path.getsize('fbs_team_stats_complete.json') / (1024 * 1024)
    offense_size = os.path.getsize('fbs_offensive_stats.json') / (1024 * 1024)
    defense_size = os.path.getsize('fbs_defensive_stats.json') / (1024 * 1024)
    teams_size = os.path.getsize('fbs_teams_stats_only.json') / (1024 * 1024)
    
    print(f"✅ Files saved:")
    print(f"   📊 fbs_team_stats_complete.json: {complete_size:.1f} MB")
    print(f"   ⚔️ fbs_offensive_stats.json: {offense_size:.1f} MB")
    print(f"   🛡️ fbs_defensive_stats.json: {defense_size:.1f} MB")
    print(f"   🏈 fbs_teams_stats_only.json: {teams_size:.1f} MB")
    
    return complete_size

def create_react_team_stats(fbs_teams):
    """Create React-optimized team stats"""
    
    print(f"\n🚀 CREATING REACT-OPTIMIZED TEAM STATS")
    print("=" * 45)
    
    # Create rankings for key stats
    key_offensive_stats = [
        'totalYards', 'passingYards', 'rushingYards', 'pointsPerGame',
        'yardsPerPlay', 'thirdDownConversions', 'redZoneConversions'
    ]
    
    key_defensive_stats = [
        'totalYardsAllowed', 'passingYardsAllowed', 'rushingYardsAllowed',
        'pointsAllowed', 'sacks', 'interceptions', 'fumblesRecovered'
    ]
    
    # Create team rankings
    team_rankings = {}
    
    for team in fbs_teams:
        team_name = team['team']
        stats = team['stats']
        
        team_rankings[team_name] = {
            'team': team_name,
            'conference': team['conference'],
            'offensive_stats': {},
            'defensive_stats': {}
        }
        
        # Extract key offensive stats
        for stat in key_offensive_stats:
            if stat in stats:
                team_rankings[team_name]['offensive_stats'][stat] = stats[stat]
        
        # Extract key defensive stats
        for stat in key_defensive_stats:
            if stat in stats:
                team_rankings[team_name]['defensive_stats'][stat] = stats[stat]
    
    # Save React-optimized files
    with open('react_fbs_team_rankings.json', 'w') as f:
        json.dump(team_rankings, f, indent=2)
    
    # Create conference summaries
    conference_stats = {}
    for team in fbs_teams:
        conf = team['conference']
        if conf not in conference_stats:
            conference_stats[conf] = {
                'conference': conf,
                'teams': [],
                'team_count': 0
            }
        
        conference_stats[conf]['teams'].append(team['team'])
        conference_stats[conf]['team_count'] += 1
    
    with open('react_fbs_conferences.json', 'w') as f:
        json.dump(conference_stats, f, indent=2)
    
    print(f"✅ React-optimized files created:")
    print(f"   🏆 react_fbs_team_rankings.json")
    print(f"   🏟️ react_fbs_conferences.json")

if __name__ == "__main__":
    print("🏈 FBS TEAM SEASON STATS DOWNLOAD")
    print("=" * 40)
    
    # Download basic team stats
    basic_stats = download_team_season_stats()
    
    # Download advanced team stats
    advanced_stats = download_advanced_team_stats()
    
    if basic_stats and advanced_stats:
        # Process and combine stats
        all_teams = process_team_stats(basic_stats, advanced_stats)
        
        # Filter for FBS teams only
        fbs_teams = filter_fbs_teams(all_teams)
        
        if fbs_teams:
            # Create offensive/defensive breakdown
            offensive_stats, defensive_stats = create_offensive_defensive_breakdown(fbs_teams)
            
            # Save comprehensive data
            file_size = save_fbs_team_stats(fbs_teams, offensive_stats, defensive_stats)
            
            # Create React-optimized exports
            create_react_team_stats(fbs_teams)
            
            print(f"\n🎯 FBS TEAM STATS COMPLETE!")
            print(f"   📊 FBS teams: {len(fbs_teams)}")
            print(f"   💾 Main file size: {file_size:.1f} MB")
            print(f"   💰 API calls used: 2 (0.04% of monthly limit)")
            print(f"   📁 Files created: 6 JSON files")
            print(f"   🚀 Ready for comprehensive team analysis!")
        else:
            print(f"\n❌ No FBS teams found after filtering")
    else:
        print(f"\n❌ Failed to download team statistics")