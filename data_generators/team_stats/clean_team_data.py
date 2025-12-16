#!/usr/bin/env python3
"""
Clean and Analyze the Downloaded Team Game Stats
Fix field mapping and create usable dataset
"""

import json
from collections import defaultdict

def analyze_raw_data():
    """Analyze the raw downloaded data to understand structure"""
    
    print("🔍 ANALYZING RAW DATA STRUCTURE")
    print("=" * 35)
    
    try:
        with open('comprehensive_team_game_stats.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Raw data file not found")
        return None
    
    print(f"📊 Total games: {len(data)}")
    
    # Analyze first game structure
    if data:
        game = data[0]
        print(f"\n🎮 SAMPLE GAME STRUCTURE:")
        
        # Show all game-level fields
        game_fields = {k: v for k, v in game.items() if k != 'teams'}
        print(f"   Game fields: {list(game_fields.keys())}")
        
        # Show game details
        print(f"   Game ID: {game.get('id')}")
        print(f"   Season: {game.get('season')}")
        print(f"   Week: {game.get('week')}")
        print(f"   Season Type: {game.get('seasonType')}")
        
        if 'teams' in game and game['teams']:
            team = game['teams'][0]
            print(f"\n🏈 SAMPLE TEAM STRUCTURE:")
            print(f"   All team fields: {list(team.keys())}")
            
            # Show team identification
            print(f"   Team ID: {team.get('teamId')}")
            print(f"   Team Name: {team.get('team')}")
            print(f"   School: {team.get('school')}")
            print(f"   Conference: {team.get('conference')}")
            print(f"   Home/Away: {team.get('homeAway')}")
            print(f"   Points: {team.get('points')}")
            
            if 'stats' in team and team['stats']:
                stats = team['stats']
                print(f"\n📈 STATS STRUCTURE:")
                print(f"   Total stats: {len(stats)}")
                
                # Group stats by category
                categories = {}
                for stat in stats:
                    cat = stat.get('category', 'unknown')
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(stat.get('stat'))
                
                print(f"   Categories: {list(categories.keys())}")
                
                # Show sample from each category
                for cat, stat_list in list(categories.items())[:5]:
                    print(f"     {cat}: {stat_list[:3]}")
    
    return data

def create_clean_dataset(raw_data):
    """Create a clean, usable dataset"""
    
    print(f"\n🧹 CREATING CLEAN DATASET")
    print("=" * 30)
    
    clean_records = []
    team_names = set()
    conferences = set()
    stat_categories = defaultdict(set)
    
    for game in raw_data:
        game_info = {
            'game_id': game.get('id'),
            'season': game.get('season'),
            'week': game.get('week'),
            'season_type': game.get('seasonType'),
            'start_date': game.get('startDate'),
            'neutral_site': game.get('neutralSite', False),
            'conference_game': game.get('conferenceGame', False),
            'attendance': game.get('attendance'),
            'venue': game.get('venue'),
            'completed': game.get('completed', True)
        }
        
        if 'teams' not in game or not game['teams']:
            continue
        
        for team_data in game['teams']:
            # Basic team info
            team_record = {
                **game_info,
                'team_id': team_data.get('teamId'),
                'team': team_data.get('team'),
                'school': team_data.get('school'),
                'conference': team_data.get('conference'),
                'home_away': team_data.get('homeAway'),
                'points': team_data.get('points'),
                'line_scores': team_data.get('lineScores', []),
                'post_win_prob': team_data.get('postWinProb'),
                'pregame_elo': team_data.get('pregameElo'),
                'postgame_elo': team_data.get('postgameElo')
            }
            
            # Track unique values
            if team_record['team']:
                team_names.add(team_record['team'])
            if team_record['conference']:
                conferences.add(team_record['conference'])
            
            # Extract stats
            if 'stats' in team_data and team_data['stats']:
                for stat in team_data['stats']:
                    category = stat.get('category', '')
                    stat_name = stat.get('stat', '')
                    stat_value = stat.get('value')
                    
                    if category and stat_name:
                        field_name = f"{category}_{stat_name}".replace(' ', '_').replace('-', '_')
                        team_record[field_name] = stat_value
                        stat_categories[category].add(stat_name)
            
            clean_records.append(team_record)
    
    print(f"✅ Created {len(clean_records)} clean team records")
    print(f"🏈 Unique teams: {len(team_names)}")
    print(f"🏟️ Conferences: {len(conferences)}")
    print(f"📊 Stat categories: {len(stat_categories)}")
    
    # Show sample teams
    sample_teams = sorted(list(team_names))[:10]
    print(f"\n📋 SAMPLE TEAMS:")
    for team in sample_teams:
        print(f"   • {team}")
    
    # Show conferences
    print(f"\n🏟️ CONFERENCES:")
    for conf in sorted(list(conferences))[:10]:
        print(f"   • {conf}")
    
    # Show stat categories
    print(f"\n📈 STAT CATEGORIES:")
    for category, stats in list(stat_categories.items())[:5]:
        print(f"   {category}: {len(stats)} stats")
        print(f"      Sample: {', '.join(list(stats)[:3])}")
    
    # Save clean dataset
    output_file = "clean_team_game_stats.json"
    with open(output_file, 'w') as f:
        json.dump(clean_records, f, indent=2)
    
    print(f"\n💾 Clean dataset saved to: {output_file}")
    
    return clean_records

def create_team_summaries(clean_records):
    """Create team season summaries from clean data"""
    
    print(f"\n🏆 CREATING TEAM SUMMARIES")
    print("=" * 30)
    
    team_summaries = defaultdict(lambda: {
        'games': 0,
        'wins': 0,
        'losses': 0,
        'total_points_for': 0,
        'total_points_against': 0,
        'home_games': 0,
        'away_games': 0,
        'neutral_games': 0,
        'conference_games': 0,
        'weeks': set(),
        'opponents': set(),
        'venues': set()
    })
    
    # Group records by game for win/loss determination
    games = defaultdict(list)
    for record in clean_records:
        if record['game_id']:
            games[record['game_id']].append(record)
    
    # Process each game
    for game_id, game_teams in games.items():
        if len(game_teams) != 2:
            continue  # Skip games without exactly 2 teams
        
        team1, team2 = game_teams
        
        # Determine winner
        points1 = team1.get('points', 0) or 0
        points2 = team2.get('points', 0) or 0
        
        # Update team1 summary
        if team1['team']:
            summary1 = team_summaries[team1['team']]
            summary1['team'] = team1['team']
            summary1['conference'] = team1['conference']
            summary1['games'] += 1
            summary1['total_points_for'] += points1
            summary1['total_points_against'] += points2
            summary1['weeks'].add(team1['week'])
            summary1['opponents'].add(team2['team'])
            if team1['venue']:
                summary1['venues'].add(team1['venue'])
            
            if team1['home_away'] == 'home':
                summary1['home_games'] += 1
            elif team1['home_away'] == 'away':
                summary1['away_games'] += 1
            else:
                summary1['neutral_games'] += 1
            
            if team1.get('conference_game'):
                summary1['conference_games'] += 1
            
            if points1 > points2:
                summary1['wins'] += 1
            else:
                summary1['losses'] += 1
        
        # Update team2 summary
        if team2['team']:
            summary2 = team_summaries[team2['team']]
            summary2['team'] = team2['team']
            summary2['conference'] = team2['conference']
            summary2['games'] += 1
            summary2['total_points_for'] += points2
            summary2['total_points_against'] += points1
            summary2['weeks'].add(team2['week'])
            summary2['opponents'].add(team1['team'])
            if team2['venue']:
                summary2['venues'].add(team2['venue'])
            
            if team2['home_away'] == 'home':
                summary2['home_games'] += 1
            elif team2['home_away'] == 'away':
                summary2['away_games'] += 1
            else:
                summary2['neutral_games'] += 1
            
            if team2.get('conference_game'):
                summary2['conference_games'] += 1
            
            if points2 > points1:
                summary2['wins'] += 1
            else:
                summary2['losses'] += 1
    
    # Convert to list and calculate derived stats
    team_list = []
    for team_name, summary in team_summaries.items():
        if summary['games'] > 0:
            summary['win_percentage'] = summary['wins'] / summary['games']
            summary['avg_points_for'] = summary['total_points_for'] / summary['games']
            summary['avg_points_against'] = summary['total_points_against'] / summary['games']
            summary['point_differential'] = summary['total_points_for'] - summary['total_points_against']
            summary['avg_point_differential'] = summary['point_differential'] / summary['games']
            
            # Convert sets to sorted lists
            summary['weeks'] = sorted(list(summary['weeks']))
            summary['opponents'] = sorted(list(summary['opponents']))
            summary['venues'] = sorted(list(summary['venues']))
            
            team_list.append(summary)
    
    # Sort by win percentage, then by point differential
    team_list.sort(key=lambda x: (x['win_percentage'], x['avg_point_differential']), reverse=True)
    
    print(f"✅ Created summaries for {len(team_list)} teams")
    
    # Show top 15 teams
    print(f"\n🏆 TOP 15 TEAMS:")
    print(f"{'#':<3} {'Team':<25} {'Record':<8} {'Win%':<6} {'PPG':<6} {'PAG':<6} {'Diff':<6}")
    print("-" * 70)
    
    for i, team in enumerate(team_list[:15], 1):
        wins = team['wins']
        losses = team['losses']
        win_pct = team['win_percentage']
        ppg = team['avg_points_for']
        pag = team['avg_points_against']
        diff = team['avg_point_differential']
        
        print(f"{i:<3} {team['team']:<25} {wins}-{losses:<7} {win_pct:.3f}  {ppg:.1f}  {pag:.1f}  {diff:+.1f}")
    
    # Save team summaries
    output_file = "team_season_summaries_clean.json"
    with open(output_file, 'w') as f:
        json.dump(team_list, f, indent=2)
    
    print(f"\n💾 Team summaries saved to: {output_file}")
    
    return team_list

def create_conference_summaries(team_summaries):
    """Create conference summaries"""
    
    print(f"\n🏟️ CREATING CONFERENCE SUMMARIES")
    print("=" * 35)
    
    conference_stats = defaultdict(lambda: {
        'teams': 0,
        'total_games': 0,
        'total_wins': 0,
        'total_points_for': 0,
        'total_points_against': 0,
        'teams_list': []
    })
    
    for team in team_summaries:
        conf = team.get('conference', 'Unknown')
        
        conf_summary = conference_stats[conf]
        conf_summary['conference'] = conf
        conf_summary['teams'] += 1
        conf_summary['total_games'] += team['games']
        conf_summary['total_wins'] += team['wins']
        conf_summary['total_points_for'] += team['total_points_for']
        conf_summary['total_points_against'] += team['total_points_against']
        conf_summary['teams_list'].append({
            'team': team['team'],
            'wins': team['wins'],
            'losses': team['losses'],
            'win_pct': team['win_percentage']
        })
    
    # Calculate conference metrics
    conf_list = []
    for conf_name, stats in conference_stats.items():
        if stats['teams'] > 0:
            stats['avg_win_percentage'] = stats['total_wins'] / (stats['total_games'] / 2) if stats['total_games'] > 0 else 0
            stats['avg_points_per_game'] = stats['total_points_for'] / stats['total_games'] if stats['total_games'] > 0 else 0
            stats['total_point_differential'] = stats['total_points_for'] - stats['total_points_against']
            
            # Sort teams within conference
            stats['teams_list'].sort(key=lambda x: x['win_pct'], reverse=True)
            
            conf_list.append(stats)
    
    # Sort conferences by average performance
    conf_list.sort(key=lambda x: x['avg_points_per_game'], reverse=True)
    
    print(f"✅ Created summaries for {len(conf_list)} conferences")
    
    # Show conference rankings
    print(f"\n🏟️ CONFERENCE RANKINGS:")
    print(f"{'#':<3} {'Conference':<25} {'Teams':<6} {'Avg PPG':<8} {'Point Diff':<12}")
    print("-" * 60)
    
    for i, conf in enumerate(conf_list[:10], 1):
        teams = conf['teams']
        ppg = conf['avg_points_per_game']
        diff = conf['total_point_differential']
        
        print(f"{i:<3} {conf['conference']:<25} {teams:<6} {ppg:.1f}    {diff:+,.0f}")
    
    return conf_list

if __name__ == "__main__":
    # Analyze raw data structure
    raw_data = analyze_raw_data()
    
    if raw_data:
        # Create clean dataset
        clean_records = create_clean_dataset(raw_data)
        
        # Create team summaries
        team_summaries = create_team_summaries(clean_records)
        
        # Create conference summaries
        conference_summaries = create_conference_summaries(team_summaries)
        
        print(f"\n🎯 DATA PROCESSING COMPLETE!")
        print(f"   📊 {len(clean_records)} clean team game records")
        print(f"   🏈 {len(team_summaries)} team season summaries")
        print(f"   🏟️ {len(conference_summaries)} conference summaries")
        print(f"   💎 Ready for advanced analytics!")
    else:
        print("❌ Failed to process data")