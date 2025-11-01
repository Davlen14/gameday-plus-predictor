#!/usr/bin/env python3
"""
AP Poll Week 10 (2025) - College Football Rankings
Fetches and displays current AP Poll rankings
Updates data/ap.json with Week 10 rankings
"""

import requests
import json
from datetime import datetime
import time
import os

class APPollFetcher:
    def __init__(self, api_key=None):
        self.base_url = "https://api.collegefootballdata.com"
        self.current_year = 2025
        self.week = 10
        self.api_key = api_key
        
    def fetch_ap_poll(self, week=None, year=None):
        """Fetch AP Poll rankings for specified week and year"""
        week = week or self.week
        year = year or self.current_year
        
        url = f"{self.base_url}/rankings"
        params = {
            'year': year,
            'week': week,
            'seasonType': 'regular'
        }
        
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for poll in data:
                    if poll.get('season') == year and poll.get('week') == week:
                        for ranking in poll.get('polls', []):
                            if ranking.get('poll') == 'AP Top 25':
                                return ranking.get('ranks', [])
                
                print(f"⚠️ AP Poll not found for Week {week} {year}")
                return []
            else:
                print(f"❌ API Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return []
    
    def display_rankings(self, rankings):
        """Display AP Poll rankings in formatted table"""
        if not rankings:
            print("No rankings data available")
            return
        
        print(f"\n{'='*80}")
        print(f"🏈 AP POLL - WEEK {self.week} ({self.current_year})")
        print(f"{'='*80}\n")
        
        print(f"{'Rank':<6} {'Team':<30} {'Conf':<15} {'Record':<12} {'Points':<8} {'1st':<5}")
        print(f"{'-'*80}")
        
        for team in rankings:
            rank = team.get('rank', '--')
            school = team.get('school', 'Unknown')
            conference = team.get('conference', 'N/A')
            
            record = f"{team.get('wins', 0)}-{team.get('losses', 0)}"
            
            points = team.get('points', 0)
            first_place = team.get('firstPlaceVotes', 0)
            
            print(f"{rank:<6} {school:<30} {conference:<15} {record:<12} {points:<8} {first_place:<5}")
        
        print(f"\n{'='*80}\n")
    
    def save_to_json(self, rankings, filename=None):
        """Save rankings to JSON file"""
        if not filename:
            filename = f"ap_poll_week{self.week}_{self.current_year}.json"
        
        data = {
            'week': self.week,
            'season': self.current_year,
            'poll': 'AP Top 25',
            'fetched_at': datetime.utcnow().isoformat() + 'Z',
            'rankings': rankings
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Rankings saved to {filename}")
        
        return filename
    
    def update_ap_json(self, rankings):
        """Update data/ap.json with Week 10 rankings"""
        ap_json_file = "data/ap.json"
        
        try:
            with open(ap_json_file, 'r') as f:
                ap_data = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ {ap_json_file} not found, creating new file")
            ap_data = {}
        
        week_key = f"week_{self.week}"
        ap_data[week_key] = {
            'poll': 'AP Top 25',
            'season': self.current_year,
            'seasonType': 'regular',
            'week': self.week,
            'ranks': rankings
        }
        
        with open(ap_json_file, 'w') as f:
            json.dump(ap_data, f, indent=2)
        
        print(f"✅ Updated {ap_json_file} with Week {self.week} rankings")
        
        # Also update frontend copy
        frontend_ap_json = "frontend/src/data/ap.json"
        if os.path.exists(os.path.dirname(frontend_ap_json)):
            with open(frontend_ap_json, 'w') as f:
                json.dump(ap_data, f, indent=2)
            print(f"✅ Updated {frontend_ap_json} with Week {self.week} rankings")

def main():
    import os
    api_key = os.getenv('CFBD_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    
    print(f"🏈 Fetching AP Poll for Week 10 (2025)...\n")
    
    fetcher = APPollFetcher(api_key=api_key)
    
    rankings = fetcher.fetch_ap_poll()
    
    if rankings:
        fetcher.display_rankings(rankings)
        fetcher.save_to_json(rankings)
        fetcher.update_ap_json(rankings)
        
        print(f"\n✅ Week 10 AP Poll data ready for predictions!")
    else:
        print(f"\n❌ Could not fetch Week 10 rankings")
        print(f"💡 TIP: AP Poll data may not be available yet if Week 10 hasn't completed")

if __name__ == "__main__":
    main()
