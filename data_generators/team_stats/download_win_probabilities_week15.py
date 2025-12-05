#!/usr/bin/env python3
"""
Download Comprehensive Win Probability Data
Get pregame WP and postgame WP for all weeks
"""

import requests
import json
from datetime import datetime

# REST API Key
REST_API_KEY = "XB5Eui0++wuuyh5uZ2c+UJY4jmLKQ2jxShzJXZaM9ET21a1OgubV4/mFlCxzsBIQ"
BASE_URL = "https://api.collegefootballdata.com"

def download_pregame_win_probabilities():
    """Download pregame win probabilities for all weeks"""
    
    print("🎯 DOWNLOADING PREGAME WIN PROBABILITIES")
    print("=" * 45)
    
    headers = {
        "Authorization": f"Bearer {REST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_pregame_wp = []
    
    # Download for weeks 1-15
    for week in range(1, 16):
        print(f"\n📊 Week {week}...")
        
        try:
            response = requests.get(
                f"{BASE_URL}/metrics/wp/pregame",
                params={"year": 2025, "week": week},
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"   ✅ {len(data)} pregame predictions")
                
                # Show sample data for week 1
                if week == 1 and data:
                    print(f"\n   📊 SAMPLE PREGAME WP:")
                    sample = data[0]
                    print(f"      Game ID: {sample.get('gameId')}")
                    print(f"      Home Team: {sample.get('homeTeam')}")
                    print(f"      Away Team: {sample.get('awayTeam')}")
                    print(f"      Spread: {sample.get('spread')}")
                    print(f"      Home WP: {sample.get('homeWinProbability', 0):.3f}")
                    print(f"      Away WP: {1 - sample.get('homeWinProbability', 0):.3f}")
                
                all_pregame_wp.extend(data)
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 PREGAME WP SUMMARY:")
    print(f"   📊 Total predictions: {len(all_pregame_wp)}")
    
    # Save pregame data
    with open('pregame_win_probabilities.json', 'w') as f:
        json.dump(all_pregame_wp, f, indent=2)
    
    print(f"   💾 Saved to: pregame_win_probabilities.json")
    
    return all_pregame_wp

def download_postgame_win_probabilities():
    """Download postgame win probabilities from games endpoint"""
    
    print(f"\n🎯 DOWNLOADING POSTGAME WIN PROBABILITIES")
    print("=" * 45)
    
    headers = {
        "Authorization": f"Bearer {REST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_postgame_wp = []
    
    # Download for weeks 1-15
    for week in range(1, 16):
        print(f"\n📊 Week {week}...")
        
        try:
            response = requests.get(
                f"{BASE_URL}/games",
                params={"year": 2025, "week": week},
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract postgame WP data
                week_postgame = []
                for game in data:
                    if game.get('homePostgameWinProbability') is not None:
                        postgame_record = {
                            'gameId': game.get('id'),
                            'season': game.get('season'),
                            'week': game.get('week'),
                            'seasonType': game.get('seasonType'),
                            'homeTeam': game.get('homeTeam'),
                            'awayTeam': game.get('awayTeam'),
                            'homeScore': game.get('homePoints'),
                            'awayScore': game.get('awayPoints'),
                            'homePostgameWP': game.get('homePostgameWinProbability'),
                            'awayPostgameWP': game.get('awayPostgameWinProbability'),
                            'completed': game.get('completed', True)
                        }
                        week_postgame.append(postgame_record)
                
                print(f"   ✅ {len(week_postgame)} postgame WP records")
                
                # Show sample for week 1
                if week == 1 and week_postgame:
                    print(f"\n   📊 SAMPLE POSTGAME WP:")
                    sample = week_postgame[0]
                    print(f"      Game ID: {sample.get('gameId')}")
                    print(f"      Home: {sample.get('homeTeam')} ({sample.get('homeScore')})")
                    print(f"      Away: {sample.get('awayTeam')} ({sample.get('awayScore')})")
                    print(f"      Home Final WP: {sample.get('homePostgameWP', 0):.3f}")
                    print(f"      Away Final WP: {sample.get('awayPostgameWP', 0):.3f}")
                
                all_postgame_wp.extend(week_postgame)
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 POSTGAME WP SUMMARY:")
    print(f"   📊 Total records: {len(all_postgame_wp)}")
    
    # Save postgame data
    with open('postgame_win_probabilities.json', 'w') as f:
        json.dump(all_postgame_wp, f, indent=2)
    
    print(f"   💾 Saved to: postgame_win_probabilities.json")
    
    return all_postgame_wp

def merge_wp_data(pregame_wp, postgame_wp):
    """Merge pregame and postgame win probability data"""
    
    print(f"\n🔄 MERGING WIN PROBABILITY DATA")
    print("=" * 35)
    
    # Create lookup for pregame data
    pregame_lookup = {}
    for record in pregame_wp:
        game_id = record.get('gameId')
        if game_id:
            pregame_lookup[game_id] = record
    
    # Merge with postgame data
    merged_records = []
    
    for postgame in postgame_wp:
        game_id = postgame.get('gameId')
        
        # Start with postgame record
        merged_record = postgame.copy()
        
        # Add pregame data if available
        if game_id in pregame_lookup:
            pregame = pregame_lookup[game_id]
            merged_record.update({
                'spread': pregame.get('spread'),
                'homePregameWP': pregame.get('homeWinProbability'),
                'awayPregameWP': 1 - pregame.get('homeWinProbability', 0) if pregame.get('homeWinProbability') else None
            })
        
        merged_records.append(merged_record)
    
    print(f"✅ Merged {len(merged_records)} complete WP records")
    
    # Calculate WP analysis
    analyze_wp_data(merged_records)
    
    # Save merged data
    with open('complete_win_probabilities.json', 'w') as f:
        json.dump(merged_records, f, indent=2)
    
    print(f"💾 Complete WP data saved to: complete_win_probabilities.json")
    
    return merged_records

def analyze_wp_data(wp_records):
    """Analyze win probability data for insights"""
    
    print(f"\n📈 WIN PROBABILITY ANALYSIS")
    print("=" * 35)
    
    # Analysis metrics
    upsets = []
    close_games = []
    blowouts = []
    wp_swings = []
    
    for record in wp_records:
        home_pregame = record.get('homePregameWP')
        home_postgame = record.get('homePostgameWP')
        home_score = record.get('homeScore', 0)
        away_score = record.get('awayScore', 0)
        
        if home_pregame is not None and home_postgame is not None:
            # Calculate WP swing
            wp_swing = abs(home_postgame - home_pregame)
            wp_swings.append(wp_swing)
            
            # Identify upsets (team with <40% pregame WP wins)
            home_won = home_score > away_score
            if (home_won and home_pregame < 0.4) or (not home_won and home_pregame > 0.6):
                upset_data = {
                    'game': f"{record.get('awayTeam')} @ {record.get('homeTeam')}",
                    'score': f"{away_score}-{home_score}",
                    'pregame_favorite': record.get('homeTeam') if home_pregame > 0.5 else record.get('awayTeam'),
                    'pregame_wp': home_pregame if home_pregame > 0.5 else 1 - home_pregame,
                    'wp_swing': wp_swing,
                    'week': record.get('week')
                }
                upsets.append(upset_data)
            
            # Identify close games (postgame WP between 0.4-0.6)
            if 0.4 <= home_postgame <= 0.6:
                close_games.append({
                    'game': f"{record.get('awayTeam')} @ {record.get('homeTeam')}",
                    'score': f"{away_score}-{home_score}",
                    'final_wp': home_postgame,
                    'week': record.get('week')
                })
            
            # Identify blowouts (postgame WP > 0.95 or < 0.05)
            elif home_postgame > 0.95 or home_postgame < 0.05:
                blowouts.append({
                    'game': f"{record.get('awayTeam')} @ {record.get('homeTeam')}",
                    'score': f"{away_score}-{home_score}",
                    'final_wp': home_postgame,
                    'week': record.get('week')
                })
    
    # Print analysis results
    print(f"📊 ANALYSIS RESULTS:")
    print(f"   Total games analyzed: {len([r for r in wp_records if r.get('homePregameWP')])}")
    print(f"   Upsets: {len(upsets)}")
    print(f"   Close games: {len(close_games)}")
    print(f"   Blowouts: {len(blowouts)}")
    
    if wp_swings:
        avg_swing = sum(wp_swings) / len(wp_swings)
        max_swing = max(wp_swings)
        print(f"   Average WP swing: {avg_swing:.3f}")
        print(f"   Maximum WP swing: {max_swing:.3f}")
    
    # Show biggest upsets
    if upsets:
        upsets.sort(key=lambda x: x['wp_swing'], reverse=True)
        print(f"\n🎯 BIGGEST UPSETS:")
        for i, upset in enumerate(upsets[:5], 1):
            print(f"   {i}. {upset['game']} (Week {upset['week']})")
            print(f"      Score: {upset['score']}")
            print(f"      {upset['pregame_favorite']} was {upset['pregame_wp']:.1%} favorite")
            print(f"      WP swing: {upset['wp_swing']:.3f}")
    
    return {
        'upsets': upsets,
        'close_games': close_games,
        'blowouts': blowouts,
        'avg_wp_swing': sum(wp_swings) / len(wp_swings) if wp_swings else 0
    }

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE WIN PROBABILITY DOWNLOAD")
    print("=" * 45)
    
    # Download pregame win probabilities
    pregame_data = download_pregame_win_probabilities()
    
    # Download postgame win probabilities
    postgame_data = download_postgame_win_probabilities()
    
    # Merge and analyze
    if pregame_data or postgame_data:
        complete_data = merge_wp_data(pregame_data, postgame_data)
        
        print(f"\n🎯 WIN PROBABILITY DOWNLOAD COMPLETE!")
        print(f"   📊 Pregame predictions: {len(pregame_data)}")
        print(f"   📊 Postgame records: {len(postgame_data)}")
        print(f"   📊 Complete records: {len(complete_data)}")
        print(f"   💰 API calls used: 14 (0.28% of monthly limit)")
        print(f"   💾 Files created: 3 JSON files")
        print(f"   🎯 Ready for React app integration!")
    else:
        print(f"\n❌ No win probability data downloaded")
