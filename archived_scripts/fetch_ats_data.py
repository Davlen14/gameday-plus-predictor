#!/usr/bin/env python3
"""
Fetch Against The Spread (ATS) data from College Football Data API
"""

import requests
import json
import os
from datetime import datetime

def fetch_ats_data(year=2025, api_key=None):
    """
    Fetch ATS data for the specified year
    
    Args:
        year (int): The year to fetch data for
        api_key (str): Optional API key for authentication
    
    Returns:
        dict: ATS data from the API
    """
    url = f"https://api.collegefootballdata.com/teams/ats?year={year}"
    
    # Set up headers with API key if provided
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    print(f"Fetching ATS data for {year}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✓ Successfully fetched ATS data for {len(data)} teams")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching ATS data: {e}")
        return None

def save_to_json(data, filename="ats_data_2025.json"):
    """
    Save ATS data to JSON file
    
    Args:
        data: The data to save
        filename (str): The output filename
    """
    if data is None:
        print("No data to save")
        return
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Data saved to {filename}")
        
    except Exception as e:
        print(f"✗ Error saving data: {e}")

def main():
    """Main execution function"""
    year = 2025
    
    # Get API key from environment variable or use default
    api_key = os.getenv('CFBD_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    
    # Fetch the data
    ats_data = fetch_ats_data(year, api_key)
    
    if ats_data:
        # Save to JSON file
        save_to_json(ats_data, f"ats_data_{year}.json")
        
        # Print summary statistics
        print(f"\n{'='*50}")
        print(f"ATS Data Summary for {year}")
        print(f"{'='*50}")
        
        for team in ats_data[:5]:  # Show first 5 teams
            print(f"\nTeam: {team.get('team', 'N/A')}")
            print(f"  Conference: {team.get('conference', 'N/A')}")
            print(f"  Wins: {team.get('wins', 0)}")
            print(f"  Losses: {team.get('losses', 0)}")
            print(f"  Pushes: {team.get('pushes', 0)}")
        
        if len(ats_data) > 5:
            print(f"\n... and {len(ats_data) - 5} more teams")

if __name__ == "__main__":
    main()
