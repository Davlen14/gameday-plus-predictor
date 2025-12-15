"""
Fetch AP/Coaches Poll rankings by TEAM instead of by coach
This fills in missing rankings data for teams we don't have coaches for
"""

import requests
import sqlite3
import time
from typing import List, Dict

API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
API_URL = "https://api.collegefootballdata.com"

def fetch_rankings_for_team(team: str, year: int) -> List[Dict]:
    """Fetch rankings for a specific team and year"""
    url = f"{API_URL}/rankings"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "year": year,
        "seasonType": "regular"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        team_rankings = []
        for week_data in data:
            week = week_data.get('week')
            season = week_data.get('season')
            
            for poll in week_data.get('polls', []):
                for rank_entry in poll.get('ranks', []):
                    if rank_entry.get('school') == team:
                        team_rankings.append({
                            'season': season,
                            'week': week,
                            'rank': rank_entry.get('rank'),
                            'school': team
                        })
                        break  # Found team, move to next poll
        
        return team_rankings
    except Exception as e:
        print(f"Error fetching {team} {year}: {e}")
        return []

def insert_rankings(rankings: List[Dict], conn):
    """Insert rankings into database with dummy coach_id"""
    cursor = conn.cursor()
    
    for rank_data in rankings:
        # Use coach_id = 0 for team-based rankings (not tied to specific coach)
        cursor.execute("""
            INSERT OR IGNORE INTO rankings (coach_id, school, season, week, rank)
            VALUES (0, ?, ?, ?, ?)
        """, (
            rank_data['school'],
            rank_data['season'],
            rank_data['week'],
            rank_data['rank']
        ))
    
    conn.commit()

def main():
    # Teams to fetch - ALL FBS teams that could be ranked
    teams_to_fetch = [
        "Michigan", "Ohio State", "Alabama", "Georgia", "Clemson",
        "Notre Dame", "Penn State", "Oregon", "Texas", "Oklahoma",
        "LSU", "Florida", "USC", "Auburn", "Wisconsin",
        "Iowa", "Nebraska", "Minnesota", "Cincinnati", "Tennessee",
        "Florida State", "Miami", "Washington", "Michigan State", "Ole Miss",
        "Texas A&M", "Baylor", "TCU", "Kansas State", "Oklahoma State",
        "Utah", "Stanford", "UCLA", "Arizona State", "Colorado",
        "Missouri", "South Carolina", "Kentucky", "Arkansas", "Mississippi State",
        "Virginia Tech", "Louisville", "NC State", "North Carolina", "Pittsburgh",
        "UCF", "Houston", "BYU", "Boise State", "Fresno State"
    ]
    
    # Years to fetch - since 1990
    years = list(range(1990, 2026))
    
    conn = sqlite3.connect('instance/coaches_master.db')
    
    print("=" * 80)
    print("🏈 FETCHING TEAM RANKINGS")
    print("=" * 80)
    
    total_added = 0
    
    for team in teams_to_fetch:
        print(f"\n📊 {team}:")
        team_total = 0
        
        for year in years:
            rankings = fetch_rankings_for_team(team, year)
            if rankings:
                insert_rankings(rankings, conn)
                team_total += len(rankings)
                print(f"  {year}: {len(rankings)} weeks")
            
            time.sleep(0.5)  # Rate limiting
        
        total_added += team_total
        print(f"  Total: {team_total} rankings")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"✅ Added {total_added} total rankings")
    print("=" * 80)

if __name__ == "__main__":
    main()
