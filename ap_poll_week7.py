#!/usr/bin/env python3
"""
AP Poll Week 7 (2025) - College Football Rankings
Fetches and displays current AP Poll rankings
"""

import requests
import json
from datetime import datetime
import time

class APPollFetcher:
    def __init__(self, api_key=None):
        self.base_url = "https://api.collegefootballdata.com"
        self.current_year = 2025
        self.week = 7
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
            response.raise_for_status()
            
            print(f"Debug: Response status: {response.status_code}")
            print(f"Debug: Response text: {response.text[:200]}...")
            
            data = response.json()
            
            # Filter for AP Poll
            ap_polls = []
            for poll_week in data:
                for poll in poll_week.get('polls', []):
                    if poll.get('poll', '').upper() == 'AP TOP 25':
                        ap_polls.append({
                            'week': poll_week.get('week'),
                            'season': poll_week.get('season'),
                            'seasonType': poll_week.get('seasonType'),
                            'rankings': poll.get('ranks', [])
                        })
            
            return ap_polls
            
        except requests.RequestException as e:
            print(f"Error fetching AP Poll data: {e}")
            return []
    
    def display_rankings(self, rankings_data):
        """Display AP Poll rankings in a formatted way"""
        if not rankings_data:
            print("❌ No AP Poll data found")
            return
            
        for poll_data in rankings_data:
            week = poll_data.get('week')
            season = poll_data.get('season')
            rankings = poll_data.get('rankings', [])
            
            print("=" * 80)
            print(f"📊 AP TOP 25 POLL - WEEK {week}, {season}")
            print("=" * 80)
            print()
            
            if not rankings:
                print("❌ No rankings data available")
                continue
                
            print(f"{'Rank':<4} {'Team':<25} {'Record':<8} {'Points':<8} {'First Place':<12}")
            print("-" * 80)
            
            for team in rankings:
                rank = team.get('rank', 'NR')
                school = team.get('school', 'Unknown')
                conference = team.get('conference', '')
                points = team.get('points', 0)
                first_place_votes = team.get('firstPlaceVotes', 0)
                
                # Try to get record from additional data if available
                record = "N/A"
                
                print(f"{rank:<4} {school:<25} {record:<8} {points:<8} {first_place_votes:<12}")
            
            print()
            print("=" * 80)
    
    def find_team_ranking(self, team_name, rankings_data):
        """Find a specific team's ranking"""
        team_name_lower = team_name.lower()
        
        for poll_data in rankings_data:
            rankings = poll_data.get('rankings', [])
            week = poll_data.get('week')
            
            for team in rankings:
                school = team.get('school', '').lower()
                if team_name_lower in school or school in team_name_lower:
                    return {
                        'week': week,
                        'rank': team.get('rank'),
                        'school': team.get('school'),
                        'conference': team.get('conference'),
                        'points': team.get('points'),
                        'first_place_votes': team.get('firstPlaceVotes', 0)
                    }
        
            return None
    
    def fetch_multiple_weeks(self, year=2025, start_week=1, end_week=7):
        """
        Fetch AP Poll rankings for multiple weeks
        """
        all_polls = {}
        
        for week in range(start_week, end_week + 1):
            print(f"📥 Fetching AP Poll for Week {week}, {year}...")
            poll_data = self.fetch_ap_poll(week, year)
            
            if poll_data:
                all_polls[f"week_{week}"] = poll_data
                print(f"✅ Week {week} data fetched successfully")
            else:
                print(f"❌ Failed to fetch Week {week} data")
            
            # Add delay to respect API rate limits
            time.sleep(0.5)
        
        return all_polls

def main():
    print("🏈 AP POLL FETCHER - WEEKS 1-7")
    print("=" * 50)
    
    # Use your API key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/pusu"
    fetcher = APPollFetcher(api_key)
    
    # Fetch all weeks 1-7
    all_polls = fetcher.fetch_multiple_weeks(2024, 1, 7)
    
    if all_polls:
        # Save to JSON file
        output_file = "ap.json"
        with open(output_file, 'w') as f:
            json.dump(all_polls, f, indent=2)
        
        print(f"\n✅ AP Poll data for weeks 1-7 saved to {output_file}")
        print(f"📊 Total weeks fetched: {len(all_polls)}")
        
        # Display summary
        print("\n" + "=" * 50)
        print("📋 SUMMARY:")
        print("=" * 50)
        
        for week_key in sorted(all_polls.keys()):
            week_data = all_polls[week_key]
            week_num = week_key.replace('week_', '')
            rankings = week_data.get('ranks', [])
            print(f"Week {week_num}: {len(rankings)} teams ranked")
            
            # Show top 5 for each week
            print(f"  Top 5:")
            for i, team in enumerate(rankings[:5]):
                rank = team.get('rank', 'N/A')
                school = team.get('school', 'N/A')
                points = team.get('points', 'N/A')
                print(f"    {rank}. {school} ({points} pts)")
            print()
    else:
        print("❌ No poll data could be fetched")

if __name__ == "__main__":
    main()