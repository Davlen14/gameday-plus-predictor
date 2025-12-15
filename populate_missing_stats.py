#!/usr/bin/env python3
"""
Populate missing box score stats in team_seasons table from College Football Data API.
Adds: possession_time, turnovers, penalty_yards, sacks, interceptions, tackles_for_loss, fumbles
"""

import sqlite3
import requests
import time
import sys
from pathlib import Path

# Configuration
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
API_BASE = "https://api.collegefootballdata.com"
DB_PATH = Path(__file__).parent / "instance" / "coaches_master.db"
YEAR = 2025
DELAY = 0.5  # seconds between API calls

# Stats mapping: API field -> DB column
STATS_MAP = {
    'possessionTime': 'possession_time',
    'possessionTimeOpponent': 'possession_time_opponent',
    'turnovers': 'turnovers',
    'turnoversOpponent': 'turnovers_opponent',
    'penaltyYards': 'penalty_yards',
    'sacks': 'sacks',
    'interceptions': 'interceptions',
    'tacklesForLoss': 'tackles_for_loss',
    'fumblesRecovered': 'fumbles_recovered',
    'fumblesLost': 'fumbles_lost'
}


def fetch_team_stats(team_name):
    """Fetch season stats for a team from College Football Data API"""
    url = f"{API_BASE}/stats/season"
    params = {'year': YEAR, 'team': team_name}
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {team_name}: {e}")
        return None


def parse_stats(api_data):
    """Parse API response into DB-ready dict"""
    stats = {}
    
    # Convert list of {statName, statValue} to dict
    for item in api_data:
        stat_name = item.get('statName')
        stat_value = item.get('statValue')
        
        if stat_name in STATS_MAP:
            db_column = STATS_MAP[stat_name]
            stats[db_column] = stat_value
    
    # Calculate turnover margin
    if 'turnovers_opponent' in stats and 'turnovers' in stats:
        stats['turnover_margin'] = stats['turnovers_opponent'] - stats['turnovers']
    
    return stats


def update_team_season(conn, team_id, year, stats):
    """Update team_seasons record with new stats"""
    if not stats:
        return False
    
    # Build UPDATE query dynamically
    set_clause = ', '.join([f"{col} = ?" for col in stats.keys()])
    values = list(stats.values())
    values.extend([team_id, year])
    
    query = f"""
        UPDATE team_seasons 
        SET {set_clause}
        WHERE team_id = ? AND season = ?
    """
    
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount > 0


def main():
    print(f"🏈 Populating missing stats for {YEAR} season...")
    print(f"📁 Database: {DB_PATH}")
    
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        sys.exit(1)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all FBS teams with team_seasons records
    query = """
        SELECT DISTINCT t.id, t.school 
        FROM teams t
        JOIN team_seasons ts ON t.id = ts.team_id
        WHERE ts.season = ?
        ORDER BY t.school
    """
    cursor.execute(query, (YEAR,))
    teams = cursor.fetchall()
    
    total = len(teams)
    print(f"📊 Found {total} teams to update\n")
    
    success_count = 0
    error_count = 0
    
    for i, (team_id, school) in enumerate(teams, 1):
        print(f"[{i}/{total}] {school}...", end=' ', flush=True)
        
        # Fetch from API
        api_data = fetch_team_stats(school)
        if not api_data:
            print("❌ API error")
            error_count += 1
            time.sleep(DELAY)
            continue
        
        # Parse stats
        stats = parse_stats(api_data)
        if not stats:
            print("⚠️  No stats found")
            error_count += 1
            time.sleep(DELAY)
            continue
        
        # Update database
        updated = update_team_season(conn, team_id, YEAR, stats)
        if updated:
            print(f"✅ Updated {len(stats)} fields")
            success_count += 1
        else:
            print("⚠️  No update")
            error_count += 1
        
        # Rate limiting
        time.sleep(DELAY)
    
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully updated: {success_count}/{total} teams")
    print(f"❌ Errors/skipped: {error_count}/{total} teams")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
