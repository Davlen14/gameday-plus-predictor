#!/usr/bin/env python3
"""
Test script for The Odds API integration with College Football GraphQL data
Fetches historical Week 5 betting lines and compares with GraphQL game data
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# College Football Data API credentials
CFB_API_KEY = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')

# The Odds API credentials (Pro tier)
ODDS_API_KEY = os.environ.get('ODDS_API_KEY', '48869290c1a6212d5289d6134917e7c7')

# API endpoints
ODDS_API_BASE = "https://api.the-odds-api.com/v4"
CFB_GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"


def fetch_cfb_week5_games():
    """Fetch Week 5 2025 games from College Football Data GraphQL API"""
    query = """
    query Week5Games {
        game(where: {season: {_eq: 2025}, week: {_eq: 5}, seasonType: {_eq: "regular"}}, 
             orderBy: {startDate: ASC}) {
            id
            homeTeam
            awayTeam
            homeTeamId
            awayTeamId
            startDate
            homePoints
            awayPoints
            lines {
                spread
                spreadOpen
                overUnder
                overUnderOpen
                provider {
                    name
                }
            }
            weather {
                temperature
                windSpeed
                precipitation
            }
        }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CFB_API_KEY}"
    }
    
    response = requests.post(
        CFB_GRAPHQL_URL,
        json={"query": query},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('game', [])
    else:
        print(f"❌ GraphQL Error: {response.status_code}")
        print(response.text)
        return []


def fetch_odds_api_ncaaf():
    """Fetch current NCAAF odds from The Odds API"""
    url = f"{ODDS_API_BASE}/sports/americanfootball_ncaaf/odds/"
    
    params = {
        'apiKey': ODDS_API_KEY,
        'regions': 'us',
        'markets': 'h2h,spreads,totals',
        'oddsFormat': 'american'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print(f"✅ The Odds API: {len(response.json())} games fetched")
        print(f"📊 Requests remaining: {response.headers.get('x-requests-remaining', 'N/A')}")
        return response.json()
    else:
        print(f"❌ The Odds API Error: {response.status_code}")
        print(response.text)
        return []


def normalize_team_name(name: str) -> str:
    """Normalize team names for matching between APIs"""
    # Common variations
    replacements = {
        "Miami (FL)": "Miami Hurricanes",
        "Miami": "Miami Hurricanes",
        "USC": "USC Trojans",
        "LSU": "LSU Tigers",
        "UCF": "UCF Knights",
        "BYU": "BYU Cougars",
        "SMU": "SMU Mustangs",
        "TCU": "TCU Horned Frogs",
    }
    
    return replacements.get(name, name)


def match_odds_to_games(cfb_games: List[Dict], odds_data: List[Dict]) -> List[Dict]:
    """Match The Odds API data to CFB GraphQL games"""
    matched_games = []
    
    for game in cfb_games:
        home_team = normalize_team_name(game['homeTeam'])
        away_team = normalize_team_name(game['awayTeam'])
        
        # Try to find matching game in Odds API
        for odds_game in odds_data:
            odds_home = odds_game.get('home_team', '')
            odds_away = odds_game.get('away_team', '')
            
            if home_team in odds_home or odds_home in home_team:
                if away_team in odds_away or odds_away in away_team:
                    # Extract bookmaker data
                    bookmakers = {}
                    for bookmaker in odds_game.get('bookmakers', []):
                        bookie_name = bookmaker.get('title')
                        markets = {}
                        
                        for market in bookmaker.get('markets', []):
                            market_key = market.get('key')
                            outcomes = market.get('outcomes', [])
                            markets[market_key] = outcomes
                        
                        bookmakers[bookie_name] = markets
                    
                    matched_games.append({
                        'cfb_data': game,
                        'odds_api_data': {
                            'commence_time': odds_game.get('commence_time'),
                            'bookmakers': bookmakers
                        }
                    })
                    break
    
    return matched_games


def compare_lines(matched_games: List[Dict]) -> Dict[str, Any]:
    """Compare CFB GraphQL lines with The Odds API lines"""
    comparison = {
        'total_games': len(matched_games),
        'games_with_discrepancies': [],
        'average_spread_difference': 0,
        'average_total_difference': 0
    }
    
    spread_diffs = []
    total_diffs = []
    
    for match in matched_games:
        cfb_game = match['cfb_data']
        odds_data = match['odds_api_data']
        
        # Get CFB lines (average across providers)
        cfb_lines = cfb_game.get('lines', [])
        if cfb_lines:
            cfb_spreads = [l['spread'] for l in cfb_lines if l.get('spread')]
            cfb_totals = [l['overUnder'] for l in cfb_lines if l.get('overUnder')]
            
            avg_cfb_spread = sum(cfb_spreads) / len(cfb_spreads) if cfb_spreads else None
            avg_cfb_total = sum(cfb_totals) / len(cfb_totals) if cfb_totals else None
            
            # Get Odds API consensus (we'll take DraftKings as reference)
            bookmakers = odds_data.get('bookmakers', {})
            
            game_comparison = {
                'matchup': f"{cfb_game['awayTeam']} @ {cfb_game['homeTeam']}",
                'cfb_spread': avg_cfb_spread,
                'cfb_total': avg_cfb_total,
                'odds_api_bookmakers': list(bookmakers.keys())
            }
            
            comparison['games_with_discrepancies'].append(game_comparison)
    
    return comparison


def main():
    """Main test function"""
    print("="*80)
    print("🏈 THE ODDS API + COLLEGE FOOTBALL GRAPHQL INTEGRATION TEST")
    print("="*80)
    print()
    
    # Fetch CFB Week 5 games from GraphQL
    print("📡 Fetching Week 5 games from College Football Data GraphQL...")
    cfb_games = fetch_cfb_week5_games()
    print(f"✅ Found {len(cfb_games)} Week 5 games\n")
    
    if cfb_games:
        # Show sample game
        sample = cfb_games[0]
        print(f"📋 Sample Game:")
        print(f"   {sample['awayTeam']} @ {sample['homeTeam']}")
        print(f"   Date: {sample['startDate']}")
        print(f"   Lines from GraphQL: {len(sample.get('lines', []))} sportsbooks")
        
        if sample.get('lines'):
            for line in sample['lines'][:3]:
                provider = line.get('provider', {}).get('name', 'Unknown')
                spread = line.get('spread', 'N/A')
                total = line.get('overUnder', 'N/A')
                print(f"      {provider}: Spread {spread}, Total {total}")
        print()
    
    # Fetch current odds from The Odds API
    print("📡 Fetching NCAAF odds from The Odds API...")
    odds_data = fetch_odds_api_ncaaf()
    print()
    
    if odds_data and isinstance(odds_data, list) and len(odds_data) > 0:
        print(f"📋 Sample Odds API Game:")
        sample_odds = odds_data[0]
        print(f"   {sample_odds.get('away_team')} @ {sample_odds.get('home_team')}")
        print(f"   Bookmakers: {len(sample_odds.get('bookmakers', []))}")
        for bookie in sample_odds.get('bookmakers', [])[:3]:
            print(f"      {bookie.get('title')}")
        print()
    
    # Match and compare
    if cfb_games and odds_data:
        print("🔗 Matching games between APIs...")
        matched = match_odds_to_games(cfb_games, odds_data)
        print(f"✅ Matched {len(matched)} games\n")
        
        # Compare lines
        comparison = compare_lines(matched)
        
        # Save results
        output = {
            'timestamp': datetime.now().isoformat(),
            'week': 5,
            'season': 2025,
            'cfb_games_count': len(cfb_games),
            'odds_api_games_count': len(odds_data),
            'matched_games_count': len(matched),
            'comparison': comparison,
            'sample_games': matched[:3] if matched else []
        }
        
        with open('week5_odds_comparison.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("💾 Results saved to week5_odds_comparison.json")
        print()
        print("="*80)
        print("✅ TEST COMPLETE")
        print("="*80)
    else:
        print("⚠️  Could not complete comparison - missing data from one or both APIs")


if __name__ == "__main__":
    main()
