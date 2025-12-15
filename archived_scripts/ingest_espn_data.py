"""
ESPN Data Ingestion Script
Ingests player rosters, player stats, and play-by-play data from ESPN API
Designed to work for all teams, testing with Ohio State first
"""

import sqlite3
import requests
import json
import time
from datetime import datetime
import sys

# ESPN API endpoints
ESPN_ROSTER_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/roster"
ESPN_PLAYER_STATS_URL = "http://sports.core.api.espn.com/v2/sports/football/leagues/college-football/athletes/{player_id}/statistics/0"
ESPN_GAME_SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={game_id}"

# Database path
DB_PATH = 'instance/coaches_master.db'

# Team ID mapping (ESPN ID to our team ID)
# For now, we'll use our team ID to fetch from our teams table
CURRENT_SEASON = 2024  # Default season for player stats


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_espn_team_id(our_team_id):
    """
    Get ESPN team ID from our teams table
    Our teams table uses ESPN IDs as the primary key
    """
    return our_team_id


def fetch_with_retry(url, max_retries=3, delay=2):
    """Fetch URL with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"  404 Not Found: {url}")
                return None
            else:
                print(f"  Attempt {attempt + 1}: Status {response.status_code}")
        except Exception as e:
            print(f"  Attempt {attempt + 1}: Error - {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(delay)
    
    return None


def ingest_team_roster(team_id, espn_team_id):
    """Ingest roster for a team"""
    print(f"\n{'='*60}")
    print(f"Ingesting roster for team {team_id} (ESPN ID: {espn_team_id})")
    print(f"{'='*60}")
    
    url = ESPN_ROSTER_URL.format(team_id=espn_team_id)
    data = fetch_with_retry(url)
    
    if not data or 'athletes' not in data:
        print(f"  No roster data found")
        return 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    players_added = 0
    
    # ESPN roster groups athletes by position
    for position_group in data['athletes']:
        if 'items' not in position_group:
            continue
        
        for athlete in position_group['items']:
            try:
                player_id = int(athlete['id'])
                name = athlete.get('displayName', '')
                jersey = athlete.get('jersey')
                
                # Position info
                position_info = athlete.get('position', {})
                position = position_info.get('name', '')
                position_abbr = position_info.get('abbreviation', '')
                
                # Class year
                class_year = None
                experience = athlete.get('experience', {})
                if experience:
                    class_year = experience.get('abbreviation')
                
                # Physical attributes
                height = athlete.get('height')
                weight = athlete.get('weight')
                
                # Hometown
                hometown_city = None
                hometown_state = None
                birthplace = athlete.get('birthPlace', {})
                if birthplace:
                    hometown_city = birthplace.get('city')
                    hometown_state = birthplace.get('state')
                
                # Headshot
                headshot_url = None
                headshot = athlete.get('headshot', {})
                if headshot:
                    headshot_url = headshot.get('href')
                
                # Status
                status = athlete.get('status', {}).get('type')
                
                # Insert or update player
                cursor.execute("""
                    INSERT OR REPLACE INTO players (
                        id, team_id, name, jersey, position, position_abbr,
                        class_year, height, weight, hometown_city, hometown_state,
                        headshot_url, status, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player_id, team_id, name, jersey, position, position_abbr,
                    class_year, height, weight, hometown_city, hometown_state,
                    headshot_url, status, datetime.now()
                ))
                
                players_added += 1
                
            except Exception as e:
                print(f"  Error processing player {athlete.get('displayName')}: {str(e)}")
                continue
    
    conn.commit()
    conn.close()
    
    print(f"  ✓ Added/updated {players_added} players")
    return players_added


def ingest_player_stats(team_id):
    """Ingest stats for all players on a team"""
    print(f"\nIngesting player stats for team {team_id}...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all players for this team
    cursor.execute("SELECT id, name FROM players WHERE team_id = ?", (team_id,))
    players = cursor.fetchall()
    
    stats_added = 0
    
    for player in players:
        player_id = player['id']
        player_name = player['name']
        
        url = ESPN_PLAYER_STATS_URL.format(player_id=player_id)
        data = fetch_with_retry(url)
        
        if not data or 'splits' not in data:
            continue
        
        try:
            # Get season stats (categories[0] should be season stats)
            categories = data['splits'].get('categories', [])
            
            if not categories:
                continue
            
            # Initialize stats dict
            stats = {
                'player_id': player_id,
                'season': CURRENT_SEASON,
                'games_played': None,
            }
            
            # Parse all stat categories
            for category in categories:
                category_name = category.get('name', '').lower()
                stat_entries = category.get('stats', [])
                
                for stat in stat_entries:
                    stat_name = stat.get('name', '').lower().replace(' ', '_')
                    stat_value = stat.get('value')
                    
                    # Map ESPN stat names to our column names
                    stat_mapping = {
                        'games_played': 'games_played',
                        'completions': 'passing_completions',
                        'attempts': 'passing_attempts' if category_name == 'passing' else 'rushing_attempts' if category_name == 'rushing' else None,
                        'yards': 'passing_yards' if category_name == 'passing' else 'rushing_yards' if category_name == 'rushing' else 'receiving_yards' if category_name == 'receiving' else None,
                        'touchdowns': 'passing_tds' if category_name == 'passing' else 'rushing_tds' if category_name == 'rushing' else 'receiving_tds' if category_name == 'receiving' else None,
                        'interceptions': 'passing_interceptions' if category_name == 'passing' else 'interceptions' if category_name == 'defensive' else None,
                        'qbr': 'passing_rating',
                        'avg_yards': 'rushing_avg' if category_name == 'rushing' else 'receiving_avg' if category_name == 'receiving' else None,
                        'long': 'rushing_long' if category_name == 'rushing' else 'receiving_long' if category_name == 'receiving' else None,
                        'receptions': 'receiving_receptions',
                        'total_tackles': 'total_tackles',
                        'solo_tackles': 'solo_tackles',
                        'tackles_for_loss': 'tackles_for_loss',
                        'sacks': 'sacks',
                        'passes_defended': 'passes_defended',
                        'forced_fumbles': 'forced_fumbles',
                        'fumbles_recovered': 'fumbles_recovered',
                        'fumbles': 'fumbles',
                        'fumbles_lost': 'fumbles_lost',
                    }
                    
                    mapped_name = stat_mapping.get(stat_name)
                    if mapped_name:
                        stats[mapped_name] = stat_value
            
            # Only insert if we have meaningful stats
            if len(stats) > 3:  # More than just player_id, season, games_played
                # Build dynamic SQL based on available stats
                columns = list(stats.keys())
                placeholders = ','.join(['?' for _ in columns])
                column_names = ','.join(columns)
                
                cursor.execute(f"""
                    INSERT OR REPLACE INTO player_stats ({column_names})
                    VALUES ({placeholders})
                """, list(stats.values()))
                
                stats_added += 1
                
        except Exception as e:
            print(f"  Error processing stats for {player_name}: {str(e)}")
            continue
        
        # Small delay to be respectful to ESPN API
        time.sleep(0.1)
    
    conn.commit()
    conn.close()
    
    print(f"  ✓ Added/updated stats for {stats_added} players")
    return stats_added


def ingest_game_drives_and_plays(team_id):
    """Ingest drives and plays for all games of a team"""
    print(f"\nIngesting drives and plays for team {team_id}...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all games for this team from our games table
    # Assumes games table has espn_game_id column
    cursor.execute("""
        SELECT id, espn_game_id, home_team_id, away_team_id, game_date
        FROM games
        WHERE home_team_id = ? OR away_team_id = ?
        ORDER BY game_date DESC
    """, (team_id, team_id))
    
    games = cursor.fetchall()
    
    if not games:
        print(f"  No games found in database for team {team_id}")
        return 0, 0
    
    drives_added = 0
    plays_added = 0
    
    for game in games:
        game_id = game['id']
        espn_game_id = game['espn_game_id']
        
        if not espn_game_id:
            print(f"  Skipping game {game_id} - no ESPN game ID")
            continue
        
        url = ESPN_GAME_SUMMARY_URL.format(game_id=espn_game_id)
        data = fetch_with_retry(url)
        
        if not data or 'drives' not in data:
            print(f"  No drive data for game {espn_game_id}")
            continue
        
        try:
            # Process drives
            all_drives = []
            if 'previous' in data['drives']:
                all_drives.extend(data['drives']['previous'])
            if 'current' in data['drives']:
                all_drives.append(data['drives']['current'])
            
            for drive_data in all_drives:
                try:
                    drive_id = drive_data.get('id')
                    if not drive_id:
                        continue
                    
                    team_info = drive_data.get('team', {})
                    drive_team_id = int(team_info.get('id', 0))
                    
                    # Map ESPN team ID to our team ID (they should match)
                    # Find matching team in our database
                    cursor.execute("SELECT id FROM teams WHERE id = ?", (drive_team_id,))
                    team_row = cursor.fetchone()
                    if not team_row:
                        continue
                    
                    sequence = drive_data.get('sequenceNumber', 0)
                    description = drive_data.get('description')
                    yards = drive_data.get('yards', 0)
                    plays_count = len(drive_data.get('plays', []))
                    result = drive_data.get('result')
                    
                    # Start/end info
                    start_info = drive_data.get('start', {})
                    end_info = drive_data.get('end', {})
                    
                    start_period = start_info.get('period', {}).get('number')
                    start_clock = start_info.get('clock', {}).get('displayValue')
                    start_yardline = start_info.get('yardLine')
                    start_yards_to_endzone = start_info.get('yardsToEndzone')
                    
                    end_period = end_info.get('period', {}).get('number')
                    end_clock = end_info.get('clock', {}).get('displayValue')
                    end_yardline = end_info.get('yardLine')
                    end_yards_to_endzone = end_info.get('yardsToEndzone')
                    
                    time_elapsed = drive_data.get('timeElapsed', {}).get('displayValue')
                    
                    # Insert drive
                    cursor.execute("""
                        INSERT OR REPLACE INTO drives (
                            id, game_id, team_id, sequence, description, yards,
                            plays_count, result, start_period, start_clock,
                            start_yardline, start_yards_to_endzone, end_period,
                            end_clock, end_yardline, end_yards_to_endzone,
                            time_elapsed
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        drive_id, game_id, drive_team_id, sequence, description,
                        yards, plays_count, result, start_period, start_clock,
                        start_yardline, start_yards_to_endzone, end_period,
                        end_clock, end_yardline, end_yards_to_endzone, time_elapsed
                    ))
                    
                    drives_added += 1
                    
                    # Process plays in this drive
                    for play_data in drive_data.get('plays', []):
                        try:
                            play_id = play_data.get('id')
                            if not play_id:
                                continue
                            
                            sequence_num = play_data.get('sequenceNumber', 0)
                            
                            play_type = play_data.get('type', {})
                            type_id = play_type.get('id')
                            type_text = play_type.get('text')
                            
                            play_text = play_data.get('text', '')
                            away_score = play_data.get('awayScore', 0)
                            home_score = play_data.get('homeScore', 0)
                            
                            period = play_data.get('period', {}).get('number')
                            clock = play_data.get('clock', {}).get('displayValue')
                            
                            # Down and distance
                            down = play_data.get('start', {}).get('down')
                            distance = play_data.get('start', {}).get('distance')
                            yard_line = play_data.get('start', {}).get('yardLine')
                            yards_to_endzone = play_data.get('start', {}).get('yardsToEndzone')
                            
                            # Yards gained
                            yards_gained = play_data.get('statYardage')
                            
                            # Scoring play
                            scoring_play = 1 if play_data.get('scoringPlay') else 0
                            
                            # Insert play
                            cursor.execute("""
                                INSERT OR REPLACE INTO plays (
                                    id, drive_id, game_id, sequence_number, type_id,
                                    type_text, play_text, away_score, home_score,
                                    period, clock, down, distance, yard_line,
                                    yards_to_endzone, yards_gained, scoring_play
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                play_id, drive_id, game_id, sequence_num, type_id,
                                type_text, play_text, away_score, home_score,
                                period, clock, down, distance, yard_line,
                                yards_to_endzone, yards_gained, scoring_play
                            ))
                            
                            plays_added += 1
                            
                        except Exception as e:
                            print(f"  Error processing play {play_id}: {str(e)}")
                            continue
                    
                except Exception as e:
                    print(f"  Error processing drive: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"  Error processing game {espn_game_id}: {str(e)}")
            continue
        
        # Commit after each game
        conn.commit()
        
        # Small delay between games
        time.sleep(0.2)
    
    conn.close()
    
    print(f"  ✓ Added {drives_added} drives and {plays_added} plays")
    return drives_added, plays_added


def ingest_team_data(team_id):
    """Ingest all ESPN data for a team"""
    espn_team_id = get_espn_team_id(team_id)
    
    print(f"\n{'='*60}")
    print(f"Starting ESPN data ingestion for team {team_id}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    # 1. Ingest roster
    players = ingest_team_roster(team_id, espn_team_id)
    
    # 2. Ingest player stats
    stats = ingest_player_stats(team_id)
    
    # 3. Ingest drives and plays
    drives, plays = ingest_game_drives_and_plays(team_id)
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"Completed ESPN data ingestion for team {team_id}")
    print(f"  Players: {players}")
    print(f"  Player stats: {stats}")
    print(f"  Drives: {drives}")
    print(f"  Plays: {plays}")
    print(f"  Time elapsed: {elapsed:.1f}s")
    print(f"{'='*60}\n")
    
    return {
        'players': players,
        'stats': stats,
        'drives': drives,
        'plays': plays,
        'elapsed': elapsed
    }


def main():
    """Main execution"""
    # Check if team ID provided
    if len(sys.argv) > 1:
        team_id = int(sys.argv[1])
        print(f"Ingesting ESPN data for team {team_id} only...")
        ingest_team_data(team_id)
    else:
        # Get all teams
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, school FROM teams ORDER BY school")
        teams = cursor.fetchall()
        conn.close()
        
        print(f"Ingesting ESPN data for all {len(teams)} teams...")
        print("This will take a while. Press Ctrl+C to stop.\n")
        
        total_stats = {
            'players': 0,
            'stats': 0,
            'drives': 0,
            'plays': 0
        }
        
        for team in teams:
            team_id = team['id']
            team_name = team['school']
            
            try:
                result = ingest_team_data(team_id)
                total_stats['players'] += result['players']
                total_stats['stats'] += result['stats']
                total_stats['drives'] += result['drives']
                total_stats['plays'] += result['plays']
                
            except KeyboardInterrupt:
                print("\n\nStopped by user")
                break
            except Exception as e:
                print(f"\nError processing {team_name}: {str(e)}\n")
                continue
        
        print(f"\n{'='*60}")
        print("FINAL TOTALS")
        print(f"{'='*60}")
        print(f"  Total players: {total_stats['players']}")
        print(f"  Total player stats: {total_stats['stats']}")
        print(f"  Total drives: {total_stats['drives']}")
        print(f"  Total plays: {total_stats['plays']}")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
