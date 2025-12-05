#!/usr/bin/env python3
"""
Convert Enhanced Coaches Data to Unified Format
Consolidates 72+ individual coach JSON files into coaches_enhanced_stats.json
"""
import json
import os
from pathlib import Path
from collections import defaultdict

def extract_vs_ranked_from_games(games):
    """Extract vs ranked performance from game history"""
    vs_ranked = {
        'wins': 0,
        'losses': 0,
        'total': 0
    }
    
    vs_top10 = {'wins': 0, 'losses': 0, 'total': 0}
    vs_top5 = {'wins': 0, 'losses': 0, 'total': 0}
    
    by_conference = {
        'ACC': {'wins': 0, 'losses': 0, 'total': 0},
        'Big Ten': {'wins': 0, 'losses': 0, 'total': 0},
        'Big 12': {'wins': 0, 'losses': 0, 'total': 0},
        'SEC': {'wins': 0, 'losses': 0, 'total': 0}
    }
    
    for game in games:
        # Check if opponent was ranked
        home_rank = game.get('homeRank')
        away_rank = game.get('awayRank')
        home_team = game.get('homeTeam')
        away_team = game.get('awayTeam')
        home_points = game.get('homePoints', 0)
        away_points = game.get('awayPoints', 0)
        
        # Skip games with missing data
        if home_points is None or away_points is None:
            continue
            
        # Determine if this team played a ranked opponent
        is_home = home_team == game.get('school_playing_for')
        opp_rank = away_rank if is_home else home_rank
        opp_conference = game.get('awayConference') if is_home else game.get('homeConference')
        
        if opp_rank and opp_rank <= 25:
            vs_ranked['total'] += 1
            
            # Determine win/loss
            won = (is_home and home_points > away_points) or (not is_home and away_points > home_points)
            if won:
                vs_ranked['wins'] += 1
            else:
                vs_ranked['losses'] += 1
            
            # Top 10 and Top 5
            if opp_rank <= 10:
                vs_top10['total'] += 1
                if won:
                    vs_top10['wins'] += 1
                else:
                    vs_top10['losses'] += 1
                    
            if opp_rank <= 5:
                vs_top5['total'] += 1
                if won:
                    vs_top5['wins'] += 1
                else:
                    vs_top5['losses'] += 1
            
            # By conference
            if opp_conference in by_conference:
                by_conference[opp_conference]['total'] += 1
                if won:
                    by_conference[opp_conference]['wins'] += 1
                else:
                    by_conference[opp_conference]['losses'] += 1
    
    return vs_ranked, vs_top10, vs_top5, by_conference

def process_coach_file(filepath, school_name):
    """Process a single enhanced coach JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        summary = data.get('summary', {})
        overview = summary.get('overview', {})
        games = data.get('games', [])
        
        # Extract basic info
        coach_name = overview.get('coach', 'Unknown Coach')
        total_record = overview.get('total_record', '0-0')
        win_pct = overview.get('win_pct', 0.0)
        total_games = overview.get('total_games', 0)
        
        # Parse record
        record_parts = total_record.split('-')
        career_wins = int(record_parts[0]) if len(record_parts) > 0 else 0
        career_losses = int(record_parts[1]) if len(record_parts) > 1 else 0
        
        # Get 2025 season data
        season_2025_games = [g for g in games if g.get('season') == 2025]
        season_2025_wins = sum(1 for g in season_2025_games 
                              if (g.get('homePoints') is not None and g.get('awayPoints') is not None) and
                                 ((g['homeTeam'] == school_name and g['homePoints'] > g['awayPoints']) or
                                  (g['awayTeam'] == school_name and g['awayPoints'] > g['homePoints'])))
        season_2025_losses = len(season_2025_games) - season_2025_wins
        season_2025_record = f"{season_2025_wins}-{season_2025_losses}"
        
        # Mark each game with the school for vs ranked analysis
        for game in games:
            game['school_playing_for'] = school_name
        
        # Extract vs ranked stats
        vs_ranked, vs_top10, vs_top5, by_conference = extract_vs_ranked_from_games(games)
        
        # Format records as "W-L-T"
        def format_record(stats):
            return f"{stats['wins']}-{stats['losses']}-0"
        
        coach_data = {
            'name': coach_name,
            'team': school_name,
            'conference': 'N/A',  # Will be filled from team data
            'careerRecord': total_record,
            'careerWinPct': round(win_pct, 1),
            '2025Record': season_2025_record,
            '2025Games': len(season_2025_games),
            'totalWins': career_wins,
            'overallRank': 999,  # Will be calculated after all coaches processed
            'winPctRank': 999,
            'totalWinsRank': 999,
            'current2025Rank': 999,
            'vsRanked': {
                'record': format_record(vs_ranked),
                'winPct': round(vs_ranked['wins'] / vs_ranked['total'], 3) if vs_ranked['total'] > 0 else 0.0,
                'totalGames': vs_ranked['total'],
                'vsTop10': {
                    'record': format_record(vs_top10),
                    'totalGames': vs_top10['total']
                },
                'vsTop5': {
                    'record': format_record(vs_top5),
                    'totalGames': vs_top5['total']
                },
                'byConference': {
                    conf: {
                        'record': format_record(stats),
                        'totalGames': stats['total']
                    } for conf, stats in by_conference.items()
                }
            }
        }
        
        return coach_data
        
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return None

def calculate_rankings(coaches):
    """Calculate national rankings for all coaches"""
    # Sort by career wins
    sorted_by_wins = sorted(coaches, key=lambda c: c['totalWins'], reverse=True)
    for rank, coach in enumerate(sorted_by_wins, 1):
        coach['totalWinsRank'] = rank
    
    # Sort by win percentage (minimum 20 games)
    eligible_coaches = [c for c in coaches if int(c['careerRecord'].split('-')[0]) + int(c['careerRecord'].split('-')[1]) >= 20]
    sorted_by_pct = sorted(eligible_coaches, key=lambda c: c['careerWinPct'], reverse=True)
    for rank, coach in enumerate(sorted_by_pct, 1):
        coach['winPctRank'] = rank
    
    # Overall rank (combination of wins and win pct)
    sorted_overall = sorted(coaches, key=lambda c: (c['totalWins'] * c['careerWinPct']), reverse=True)
    for rank, coach in enumerate(sorted_overall, 1):
        coach['overallRank'] = rank
    
    # 2025 season rank
    season_2025_coaches = [c for c in coaches if c['2025Games'] > 0]
    season_2025_wins = []
    for coach in season_2025_coaches:
        wins = int(coach['2025Record'].split('-')[0])
        season_2025_wins.append((coach, wins))
    
    sorted_2025 = sorted(season_2025_wins, key=lambda x: x[1], reverse=True)
    for rank, (coach, _) in enumerate(sorted_2025, 1):
        coach['current2025Rank'] = rank
    
    return coaches

def load_team_conferences():
    """Load team conference data from fbs.json"""
    try:
        with open('/Users/davlenswain/Desktop/Gameday_Graphql_Model/fbs.json', 'r') as f:
            fbs_data = json.load(f)
            return {team['school']: team.get('conference', 'N/A') for team in fbs_data}
    except:
        return {}

def main():
    """Main conversion process"""
    print("🏈 Enhanced Coaches Converter")
    print("=" * 60)
    
    enhanced_dir = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/enhanced_coaches')
    
    if not enhanced_dir.exists():
        print("❌ enhanced_coaches directory not found!")
        return
    
    # Load team conferences
    team_conferences = load_team_conferences()
    print(f"✅ Loaded {len(team_conferences)} team conferences")
    
    # Process all coach files
    coach_files = list(enhanced_dir.glob('*.json'))
    print(f"\n📂 Found {len(coach_files)} coach files")
    
    all_coaches = []
    
    for filepath in sorted(coach_files):
        # Extract school name from filename (e.g., "smart_georgia.json" -> "Georgia")
        filename = filepath.stem  # e.g., "smart_georgia"
        school_parts = filename.split('_')[1:]  # e.g., ["georgia"]
        school_name = ' '.join(word.capitalize() for word in school_parts)  # e.g., "Georgia"
        
        # Handle special cases
        if school_name == 'Ohio State':
            school_name = 'Ohio State'
        elif school_name == 'Texas Aandm':
            school_name = 'Texas A&M'
        elif school_name == 'Nc State':
            school_name = 'NC State'
        elif school_name == 'Boston College':
            school_name = 'Boston College'
        
        print(f"  📊 Processing: {school_name}...", end=' ')
        
        coach_data = process_coach_file(filepath, school_name)
        
        if coach_data:
            # Add conference data
            coach_data['conference'] = team_conferences.get(school_name, 'N/A')
            all_coaches.append(coach_data)
            print(f"✅ {coach_data['name']}")
        else:
            print(f"❌ Failed")
    
    # Calculate rankings
    print("\n🏆 Calculating national rankings...")
    all_coaches = calculate_rankings(all_coaches)
    
    # Save to new file
    output_path = '/Users/davlenswain/Desktop/Gameday_Graphql_Model/data/coaches_enhanced_stats.json'
    with open(output_path, 'w') as f:
        json.dump(all_coaches, f, indent=2)
    
    print(f"\n✅ Saved {len(all_coaches)} coaches to: coaches_enhanced_stats.json")
    
    # Show top 10 coaches
    print("\n🌟 Top 10 Coaches (Overall):")
    print("-" * 60)
    sorted_coaches = sorted(all_coaches, key=lambda c: c['overallRank'])
    for coach in sorted_coaches[:10]:
        print(f"  #{coach['overallRank']:2d} {coach['name']:25s} ({coach['team']:20s}) - {coach['careerRecord']} ({coach['careerWinPct']}%)")
    
    print("\n" + "=" * 60)
    print("✅ Conversion complete!")

if __name__ == '__main__':
    main()
